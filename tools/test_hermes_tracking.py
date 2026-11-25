import sqlite3
import stat
import tempfile
import unittest
from collections import Counter
from contextlib import closing
from pathlib import Path
from types import SimpleNamespace
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

    def test_board_path_rejects_reparse_metadata_before_opening_database(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory).resolve()
            board = mirror.board_directory(home)
            board.mkdir(parents=True)
            original_lstat = Path.lstat
            for target in (board.parent.parent, board.parent, board):
                def classified(path):
                    if path == target:
                        return SimpleNamespace(st_mode=stat.S_IFDIR,
                                               st_file_attributes=stat.FILE_ATTRIBUTE_REPARSE_POINT)
                    return original_lstat(path)

                with self.subTest(path=target), patch.object(Path, 'lstat', classified):
                    with patch.object(mirror.sqlite3, 'connect') as connect:
                        with self.assertRaisesRegex(ValueError, 'Unexpected board path'):
                            mirror.read_board(home)
                        connect.assert_not_called()

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


    def test_capture_rejects_dangling_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            home = root / 'live'
            home.mkdir()
            target = root / 'missing.json'
            output = root / 'capture.json'
            try:
                output.symlink_to(target)
            except (OSError, NotImplementedError):
                self.skipTest('symlinks not available to this account')
            with patch('sys.argv', ['hermes_tracking', '--kanban-home', str(home),
                                   '--capture-plan', str(output)]), patch.object(mirror, 'read_board') as read_board:
                with self.assertRaises(FileExistsError):
                    mirror.main()
                read_board.assert_not_called()
            self.assertFalse(target.exists())
            self.assertTrue(output.is_symlink())

    def test_board_snapshot_reads_only_committed_wal_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory).resolve()
            board = mirror.board_directory(home)
            board.mkdir(parents=True)
            (board / 'board.json').write_text(f'{{"slug":"{mirror.BOARD}","archived":false}}')
            db = board / 'kanban.db'
            with closing(sqlite3.connect(db)) as writer:
                self.assertEqual(writer.execute('PRAGMA journal_mode=WAL').fetchone()[0], 'wal')
                writer.execute('PRAGMA wal_autocheckpoint=0')
                writer.execute('CREATE TABLE tasks (id, created_by, title, body, assignee, status)')
                writer.execute('PRAGMA wal_checkpoint(TRUNCATE)').fetchone()
                before = db.read_bytes()
                writer.execute("INSERT INTO tasks VALUES ('t_first','local','committed','body',NULL,'blocked')")
                writer.commit()
                writer.execute("UPDATE tasks SET title='uncommitted'")
                self.assertEqual(mirror.read_board(home)[0]['title'], 'committed')
                self.assertEqual(db.read_bytes(), before)

    def test_plan_snapshot_uses_only_detached_rows(self):
        card = mirror.Card('One', '<!-- cephalon-engine-mirror:issue:1 -->\n')
        rows = [dict(id='t_first', created_by=mirror.OWNER, title=card.title, body=card.body,
                     assignee=None, status='blocked')]
        with tempfile.TemporaryDirectory() as home, patch.object(mirror, 'load', return_value=(
                {'observed_at_utc': 'test'}, {'issue:1': card})), patch.object(
                mirror, 'read_board', side_effect=AssertionError('live board access')):
            path = Path(home) / 'rows.json'
            mirror.capture_rows(path, rows)
            with self.assertRaises(FileExistsError):
                mirror.capture_rows(path, [])
            before = path.read_bytes()
            with patch('sys.argv', ['hermes_tracking', '--plan-snapshot', str(path)]), patch('builtins.print') as output:
                mirror.main()
            self.assertIn('"edit": 0', output.call_args.args[0])
            self.assertEqual(path.read_bytes(), before)

    def test_guard_rejects_stale_row_at_update_and_rolls_back_audit(self):
        row = dict(id='t_first', created_by=mirror.OWNER, title='Old', body='old body',
                   assignee=None, status='blocked')
        with tempfile.TemporaryDirectory() as directory:
            db = Path(directory).resolve() / 'kanban.db'
            with closing(sqlite3.connect(db)) as writer, writer:
                writer.execute('CREATE TABLE tasks (id, created_by, title, body, assignee, status)')
                writer.execute('CREATE TABLE events (kind)')
                writer.execute('INSERT INTO tasks VALUES (?, ?, ?, ?, ?, ?)', tuple(row.values()))

            def hermes_edit(conn, task_id, *, title, body, board):
                self.assertEqual(board, mirror.BOARD)
                with conn:
                    conn.execute('BEGIN IMMEDIATE')
                    conn.execute("INSERT INTO events VALUES ('edited')")
                    conn.execute('UPDATE tasks SET title=?, body=? WHERE id=?', (title, body, task_id))
                return True

            def racing_edit(*args, **kwargs):
                with closing(sqlite3.connect(db)) as writer, writer:
                    writer.execute("UPDATE tasks SET assignee='manual'")
                return hermes_edit(*args, **kwargs)

            card = mirror.Card('New', 'new body')
            with self.assertRaisesRegex(ValueError, 'Mirror changed'):
                mirror.edit_card(db, row, card, racing_edit)
            with closing(sqlite3.connect(db)) as writer, writer:
                self.assertEqual(writer.execute('SELECT title, assignee FROM tasks').fetchone(), ('Old', 'manual'))
                self.assertEqual(writer.execute('SELECT * FROM events').fetchall(), [])
                writer.execute('UPDATE tasks SET assignee=NULL')
            mirror.edit_card(db, row, card, hermes_edit)
            with closing(sqlite3.connect(db)) as reader:
                self.assertEqual(reader.execute('SELECT title, body FROM tasks').fetchone(), ('New', 'new body'))
                self.assertEqual(reader.execute('SELECT * FROM events').fetchall(), [('edited',)])
                self.assertEqual(reader.execute("SELECT name FROM sqlite_master WHERE type='trigger'").fetchall(), [])

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
                mirror.subprocess, 'check_output', return_value='') as cli, patch.object(
                mirror, 'hermes_editor'), patch.object(mirror, 'edit_card') as edit:
            with self.assertRaisesRegex(ValueError, 'Mirror changed during apply'):
                mirror.main()
        cli.assert_not_called()
        edit.assert_not_called()


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
