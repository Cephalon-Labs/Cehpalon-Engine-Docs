import sqlite3
import tempfile
import unittest
from collections import Counter
from contextlib import closing
from pathlib import Path
from unittest.mock import patch

import hermes_tracking as mirror

ROOT = Path(__file__).resolve().parents[1]


class HermesTrackingTest(unittest.TestCase):
    def test_project_snapshot_produces_unique_read_only_references(self):
        snapshot, cards = mirror.load(ROOT)
        self.assertEqual(Counter(k.split(':')[0] for k in cards),
                         {'issue': len(snapshot['issues']), 'milestone': len(snapshot['milestones']), 'docs': 1})
        for key, card in cards.items():
            self.assertTrue(card.body.startswith(f'<!-- cephalon-engine-mirror:{key} -->\n'))
            self.assertIn(snapshot['observed_at_utc'], card.body)
        for n, issue in snapshot['issues'].items():
            self.assertIn(issue['url'], cards[f'issue:{n}'].body)
            self.assertIn(issue['item_id'], cards[f'issue:{n}'].body)

    def test_reconciliation_noop_update_and_create(self):
        a = mirror.Card('One', '<!-- cephalon-engine-mirror:issue:1 -->\ntext')
        b = mirror.Card('Two', '<!-- cephalon-engine-mirror:issue:2 -->\ntext')
        rows = [{'id': 't_first', 'created_by': mirror.OWNER, 'title': a.title, 'body': a.body,
                 'assignee': None, 'status': 'blocked'}]
        self.assertEqual(mirror.plan({'issue:1': a}, rows), [])
        self.assertEqual(mirror.plan({'issue:1': mirror.Card('Changed', a.body), 'issue:2': b}, rows),
                         [('edit', 'issue:1', 't_first'), ('create', 'issue:2', None)])

    def test_rejects_duplicates_local_tasks_missing_source_or_runnable_rows(self):
        card = mirror.Card('One', '<!-- cephalon-engine-mirror:issue:1 -->\ntext')
        row = {'id': 't_first', 'created_by': mirror.OWNER, 'title': card.title, 'body': card.body,
               'assignee': None, 'status': 'blocked'}
        for desired, rows in [({'issue:1': card}, [row, dict(row, id='t_second')]),
                              ({'issue:1': card}, [dict(row, created_by='user')]), ({}, [row]),
                              ({'issue:1': card}, [dict(row, assignee='default')]),
                              ({'issue:1': card}, [dict(row, status='archived')])]:
            with self.subTest(rows=rows, desired=desired), self.assertRaises(ValueError):
                mirror.plan(desired, rows)

    def test_read_board_is_read_only_and_rejects_incomplete_or_redirected_board(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory).resolve()
            board = home / 'kanban' / 'boards' / mirror.BOARD
            self.assertIsNone(mirror.read_board(home))
            self.assertFalse(board.exists())
            board.mkdir(parents=True)
            db = board / 'kanban.db'
            meta = board / 'board.json'
            meta.write_text(f'{{"slug":"{mirror.BOARD}","archived":false}}')
            with self.assertRaises(ValueError):
                mirror.read_board(home)
            with closing(sqlite3.connect(db)) as conn, conn:
                conn.execute('CREATE TABLE tasks (id, created_by, title, body, assignee, status)')
                conn.execute("INSERT INTO tasks VALUES ('task','local','title','body',NULL,'todo')")
            before = db.read_bytes()
            self.assertEqual(mirror.read_board(home)[0]['status'], 'todo')
            self.assertEqual(db.read_bytes(), before)
            # A second name for the database must be rejected. A hard link
            # exercises this with no Windows symlink privilege requirement.
            other = home / 'other.db'
            other.hardlink_to(db)
            with self.assertRaises(ValueError):
                mirror.read_board(home)

            other.unlink()
            is_symlink = Path.is_symlink
            with patch.object(Path, 'is_symlink', lambda path: path == db or is_symlink(path)):
                with self.assertRaises(ValueError):
                    mirror.read_board(home)

    def test_subprocess_environment_pins_target_and_drops_worker_overrides(self):
        home = Path('/isolated')
        env = mirror.write_env(home, {'HERMES_KANBAN_DB': '/company.db',
                                      'HERMES_KANBAN_BOARD': 'cephalon-company',
                                      'HERMES_KANBAN_ATTACHMENTS_ROOT': '/company-files',
                                      'OTHER': 'keep'})
        self.assertEqual(env, {'HERMES_KANBAN_HOME': str(home),
                               'HERMES_KANBAN_BOARD': mirror.BOARD,
                               'HERMES_KANBAN_DB': str(home / 'kanban' / 'boards' / mirror.BOARD / 'kanban.db'),
                               'OTHER': 'keep'})


    def test_apply_stops_before_second_write_if_first_does_not_persist(self):
        cards = {f'issue:{n}': mirror.Card(str(n), f'<!-- cephalon-engine-mirror:issue:{n} -->\n')
                 for n in (1, 2)}
        with patch.object(mirror, 'read_board', return_value=[]), patch.object(mirror, 'load', return_value=(
                {'observed_at_utc': 'test'}, cards)), tempfile.TemporaryDirectory() as home, patch(
                'sys.argv', ['hermes_tracking', '--apply', '--kanban-home', home]), patch.object(
                mirror.subprocess, 'check_output', return_value='') as cli:
            with self.assertRaises(ValueError):
                mirror.main()
        self.assertEqual(cli.call_count, 1)

    def test_apply_rejects_content_drift_before_edit(self):
        card = mirror.Card('Desired', '<!-- cephalon-engine-mirror:issue:1 -->\n')
        row = dict(id='t_first', created_by=mirror.OWNER, title='Old', body=card.body,
                   assignee=None, status='blocked')
        with patch.object(mirror, 'read_board', side_effect=[[row], [dict(row, title='Manual edit')], [row]]), patch.object(
                mirror, 'load', return_value=({'observed_at_utc': 'test'}, {'issue:1': card})), tempfile.TemporaryDirectory() as home, patch(
                'sys.argv', ['hermes_tracking', '--apply', '--kanban-home', home]), patch.object(
                mirror.subprocess, 'check_output', return_value='') as cli:
            with self.assertRaises(ValueError):
                mirror.main()
        self.assertEqual(cli.call_count, 0)


    def test_noop_apply_rejects_replacement_card_at_final_readback(self):
        card = mirror.Card('Desired', '<!-- cephalon-engine-mirror:issue:1 -->\n')
        row = dict(id='t_first', created_by=mirror.OWNER, title=card.title, body=card.body,
                   assignee=None, status='blocked')
        with patch.object(mirror, 'read_board', side_effect=[[row], [dict(row, id='t_new')]]), patch.object(
                mirror, 'load', return_value=({'observed_at_utc': 'test'}, {'issue:1': card})), tempfile.TemporaryDirectory() as home, patch(
                'sys.argv', ['hermes_tracking', '--apply', '--kanban-home', home]):
            with self.assertRaisesRegex(ValueError, 'final readback'):
                mirror.main()


if __name__ == '__main__':
    unittest.main()
