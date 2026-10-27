"""Offline regression cases for tracking conflicts; no GitHub writes or calls."""
import copy
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import pull_tracking
from pull_tracking import (JOURNAL_RELATIVE, LOCK_RELATIVE, SNAPSHOT_RELATIVE,
                           digest, exclusive_pull, reconcile, reconcile_milestone_counts, render)


def row(number=1, body='Original issue body\n'):
    return {'number': number, 'node_id': f'ISSUE-{number}', 'item_id': f'ITEM-{number}',
            'title': f'Task {number}', 'url': f'https://github.com/example/engine/issues/{number}',
            'body': body, 'state': 'open', 'type': 'Task', 'labels': ['area:quality'],
            'assignees': ['Cephalon-Neza'], 'milestone': 'W0',
            'fields': {'Status': 'Ready', 'Priority': 'P0', 'Actual (h)': None}}


class ConflictTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / 'tasks').mkdir()
        self.original = row()
        self.path = self.root / 'tasks/1.md'
        self.path.write_text(render(self.original), encoding='utf-8', newline='\n')
        self.previous = {'1': {**self.original, 'mirror_sha256': digest(render(self.original))}}

    def tearDown(self):
        self.temp.cleanup()

    def test_stale_rest_milestone_counters_are_retained_without_overriding_agreeing_native_counts(self):
        rest = [{'number': 1, 'title': 'W0', 'open_issues': 1, 'closed_issues': 0}]
        graph = [{'number': 1, 'open': {'totalCount': 0}, 'closed': {'totalCount': 1}}]
        rows = {'1': {'milestone_number': 1, 'state': 'closed'}}
        result = reconcile_milestone_counts(rest, graph, rows)[0]
        self.assertEqual((0, 1), (result['open_issues'], result['closed_issues']))
        self.assertEqual((1, 0), (result['rest_reported_open_issues'], result['rest_reported_closed_issues']))
        self.assertFalse(result['rest_counter_consistent'])

    def test_disagreeing_graphql_and_native_issue_counts_stop_synchronization(self):
        rest = [{'number': 1, 'title': 'W0', 'open_issues': 1, 'closed_issues': 0}]
        graph = [{'number': 1, 'open': {'totalCount': 1}, 'closed': {'totalCount': 0}}]
        rows = {'1': {'milestone_number': 1, 'state': 'closed'}}
        with self.assertRaisesRegex(ValueError, 'observations disagree'):
            reconcile_milestone_counts(rest, graph, rows)

    def test_remote_only_change_updates_mirror_and_keeps_null_hours(self):
        changed = row(body='Remote decision changed\n')
        result = reconcile(self.root, self.previous, {'1': changed})
        self.assertIn('Remote decision changed', self.path.read_text(encoding='utf-8'))
        self.assertIsNone(result['1']['fields']['Actual (h)'])

    def test_local_and_remote_edits_stop_before_any_mirror_is_written(self):
        local = render(self.original) + '\nUser local decision\n'
        self.path.write_text(local, encoding='utf-8')
        second = row(2)
        with self.assertRaisesRegex(ValueError, 'Local tracking edit'):
            reconcile(self.root, self.previous, {'2': second, '1': row(body='Concurrent remote edit')})
        self.assertFalse((self.root / 'tasks/2.md').exists())
        self.assertEqual(local, self.path.read_text(encoding='utf-8'))

    def test_local_only_edit_is_preserved_and_not_silently_discarded(self):
        local = render(self.original) + 'Unpublished local notes\n'
        self.path.write_text(local, encoding='utf-8')
        with self.assertRaises(ValueError):
            reconcile(self.root, self.previous, {'1': self.original})
        self.assertEqual(local, self.path.read_text(encoding='utf-8'))

    def test_migrated_issue_or_item_requires_explicit_mapping(self):
        for field in ['node_id', 'item_id']:
            with self.subTest(field=field):
                changed = copy.deepcopy(self.original)
                changed[field] = 'MIGRATED'
                with self.assertRaisesRegex(ValueError, 'migration mapping'):
                    reconcile(self.root, self.previous, {'1': changed})
        self.assertEqual(render(self.original), self.path.read_text(encoding='utf-8'))

    def test_removed_remote_issue_does_not_delete_local_evidence(self):
        with self.assertRaisesRegex(ValueError, 'disappeared'):
            reconcile(self.root, self.previous, {})
        self.assertTrue(self.path.exists())

    def test_check_mode_detects_remote_drift_without_writing(self):
        with self.assertRaisesRegex(ValueError, 'Live GitHub differs'):
            reconcile(self.root, self.previous, {'1': row(body='Changed remotely')}, check_only=True)
        self.assertEqual(render(self.original), self.path.read_text(encoding='utf-8'))

    def test_unanchored_existing_file_is_not_overwritten(self):
        with self.assertRaisesRegex(ValueError, 'Unanchored'):
            reconcile(self.root, {}, {'1': self.original})

    def test_check_mode_accepts_unchanged_state_and_preserves_file(self):
        before = self.path.stat().st_mtime_ns
        reconcile(self.root, self.previous, {'1': self.original}, check_only=True)
        self.assertEqual(before, self.path.stat().st_mtime_ns)

    def test_post_preflight_edit_is_preserved_and_requires_review(self):
        prepare = pull_tracking._prepare_transaction
        local = render(self.original) + 'Editor changed this after preflight\n'

        def edit_after_staging(*args):
            prepared = prepare(*args)
            self.path.write_text(local, encoding='utf-8', newline='\n')
            return prepared

        with patch('pull_tracking._prepare_transaction', side_effect=edit_after_staging):
            with self.assertRaisesRegex(ValueError, 'after preflight'):
                reconcile(self.root, self.previous, {'1': row(body='Remote update\n')})
        self.assertEqual(local, self.path.read_text(encoding='utf-8'))
        self.assertTrue((self.root / JOURNAL_RELATIVE).exists())
        self.assertFalse((self.root / SNAPSHOT_RELATIVE).exists())
        with self.assertRaisesRegex(ValueError, 'Unresolved tracking recovery journal'):
            reconcile(self.root, self.previous, {'1': self.original})

    def test_partial_commit_keeps_recovery_copies_and_blocks_new_pull(self):
        replace = os.replace
        second = self.root / 'tasks/2.md'
        changed = row(body='Remote update\n')

        def fail_second_mirror(source, target):
            if Path(target) == second:
                raise OSError('Injected second mirror replacement failure')
            return replace(source, target)

        with patch('pull_tracking.os.replace', side_effect=fail_second_mirror):
            with self.assertRaisesRegex(OSError, 'second mirror'):
                reconcile(self.root, self.previous, {'1': changed, '2': row(2)})
        self.assertEqual(render(changed), self.path.read_text(encoding='utf-8'))
        self.assertFalse(second.exists())
        self.assertFalse((self.root / SNAPSHOT_RELATIVE).exists())
        journal = json.loads((self.root / JOURNAL_RELATIVE).read_text(encoding='utf-8'))
        self.assertEqual('needs-review', journal['status'])
        directory = self.root / journal['directory']
        first = journal['entries'][0]
        self.assertEqual(render(self.original).encode('utf-8'), (directory / first['before']).read_bytes())
        self.assertEqual(render(changed).encode('utf-8'), (directory / first['new']).read_bytes())
        with self.assertRaisesRegex(ValueError, 'Unresolved tracking recovery journal'):
            reconcile(self.root, self.previous, {'1': changed, '2': row(2)})

    def test_snapshot_failure_preserves_old_snapshot_and_recovery_manifest(self):
        snapshot = self.root / SNAPSHOT_RELATIVE
        snapshot.parent.mkdir(parents=True)
        original_snapshot = json.dumps({'issues': self.previous}) + '\n'
        snapshot.write_text(original_snapshot, encoding='utf-8', newline='\n')
        replace = os.replace
        changed = row(body='Remote update\n')

        def fail_snapshot(source, target):
            if Path(target) == snapshot:
                raise OSError('Injected snapshot replacement failure')
            return replace(source, target)

        with patch('pull_tracking.os.replace', side_effect=fail_snapshot):
            with self.assertRaisesRegex(OSError, 'snapshot replacement'):
                reconcile(self.root, self.previous, {'1': changed})
        self.assertEqual(original_snapshot, snapshot.read_text(encoding='utf-8'))
        self.assertEqual(render(changed), self.path.read_text(encoding='utf-8'))
        journal = json.loads((self.root / JOURNAL_RELATIVE).read_text(encoding='utf-8'))
        entry = next(x for x in journal['entries'] if x['target'] == SNAPSHOT_RELATIVE.as_posix())
        directory = self.root / journal['directory']
        self.assertEqual(original_snapshot.encode('utf-8'), (directory / entry['before']).read_bytes())
        self.assertEqual('staged', entry['state'])
        self.assertTrue((directory / entry['new']).exists())
        with self.assertRaisesRegex(ValueError, 'Unresolved tracking recovery journal'):
            reconcile(self.root, self.previous, {'1': changed})

    def test_cooperating_concurrent_run_cannot_acquire_lock(self):
        with exclusive_pull(self.root):
            self.assertTrue((self.root / LOCK_RELATIVE).exists())
            with self.assertRaisesRegex(ValueError, 'Another tracking pull'):
                reconcile(self.root, self.previous, {'1': self.original})
            self.assertEqual(render(self.original), self.path.read_text(encoding='utf-8'))
        self.assertFalse((self.root / LOCK_RELATIVE).exists())

    def test_success_commits_snapshot_last_and_retains_recovery_history(self):
        snapshot = self.root / SNAPSHOT_RELATIVE
        replace = os.replace
        committed = []
        changed = row(body='Remote update\n')

        def record_replacement(source, target):
            if Path(target) in [self.path, snapshot]:
                committed.append(Path(target))
            return replace(source, target)

        with patch('pull_tracking.os.replace', side_effect=record_replacement):
            result = reconcile(self.root, self.previous, {'1': changed})
        self.assertEqual([self.path, snapshot], committed)
        self.assertFalse((self.root / JOURNAL_RELATIVE).exists())
        self.assertFalse((self.root / LOCK_RELATIVE).exists())
        saved = json.loads(snapshot.read_text(encoding='utf-8'))
        self.assertEqual(result, saved['issues'])
        history = list((self.root / '.local/tracking-transactions').glob('*/journal.json'))
        self.assertEqual(1, len(history))
        journal = json.loads(history[0].read_text(encoding='utf-8'))
        self.assertEqual('completed', journal['status'])
        before = history[0].parent / journal['entries'][0]['before']
        self.assertEqual(render(self.original).encode('utf-8'), before.read_bytes())

    def test_snapshot_local_edit_since_fetch_stops_before_any_target_write(self):
        snapshot = self.root / SNAPSHOT_RELATIVE
        snapshot.parent.mkdir(parents=True)
        earlier = json.dumps({'issues': self.previous}) + '\n'
        local = earlier + 'Unreviewed snapshot note\n'
        snapshot.write_text(local, encoding='utf-8', newline='\n')
        with self.assertRaisesRegex(ValueError, 'after preflight'):
            reconcile(self.root, self.previous, {'1': row(body='Remote update\n')},
                      snapshot_expected=digest(earlier))
        self.assertEqual(render(self.original), self.path.read_text(encoding='utf-8'))
        self.assertEqual(local, snapshot.read_text(encoding='utf-8'))

    def test_edit_to_later_mirror_during_batch_is_not_overwritten(self):
        second = row(2)
        second_path = self.root / 'tasks/2.md'
        second_path.write_text(render(second), encoding='utf-8', newline='\n')
        previous = {**self.previous, '2': {**second, 'mirror_sha256': digest(render(second))}}
        local = render(second) + 'Editor changed the later mirror\n'
        replace = os.replace

        def edit_later_file_after_first_replace(source, target):
            result = replace(source, target)
            if Path(target) == self.path:
                second_path.write_text(local, encoding='utf-8', newline='\n')
            return result

        with patch('pull_tracking.os.replace', side_effect=edit_later_file_after_first_replace):
            with self.assertRaisesRegex(ValueError, 'after preflight'):
                reconcile(self.root, previous, {'1': row(body='Remote update\n'), '2': row(2, 'Second remote update\n')})
        self.assertEqual(local, second_path.read_text(encoding='utf-8'))
        self.assertTrue((self.root / JOURNAL_RELATIVE).exists())


if __name__ == '__main__':
    unittest.main()
