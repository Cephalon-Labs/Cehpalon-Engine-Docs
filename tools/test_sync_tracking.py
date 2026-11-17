"""Offline behavior tests for reviewed two-way sync; all transport is fake."""
import copy
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import pull_tracking as pull
import sync_tracking as sync

ENGINE_SHA = 'a' * 40


def catalog():
    options = {'Status': ['Backlog', 'Ready', 'In Progress', 'Review', 'Test', 'Benchmark', 'Blocked', 'Done'],
               'Priority': ['P0', 'P1', 'P2', 'P3'], 'Maturity': ['M0', 'M1', 'M2', 'M3', 'M4'],
               'Test gate': ['Planned', 'Passed', 'Failed', 'Blocked', 'Not required'],
               'Benchmark gate': ['Planned', 'Passed', 'Failed', 'Blocked', 'Not required']}
    fields = {}
    for name in pull.PROJECT_FIELDS:
        fields[name] = {'id': 'FIELD-' + name,
                        'data_type': 'NUMBER' if name in sync.NUMERIC_FIELDS else ('TEXT' if name == 'Feature' else 'SINGLE_SELECT'),
                        'options': {value: 'OPTION-' + value for value in options.get(name, [])}}
    return {'actor': 'Cephalon-Neza', 'types': ['Bug', 'Feature', 'Task'],
            'labels': ['area:governance', 'area:quality'], 'assignees': ['Cephalon-Neza', 'reviewer'],
            'milestones': {'1': {'title': 'W0', 'state': 'open'}, '2': {'title': 'W1', 'state': 'open'}}, 'fields': fields}


def row(number=1):
    return {'number': number, 'node_id': f'ISSUE-{number}', 'item_id': f'ITEM-{number}',
            'url': f'https://github.com/{pull.REPO}/issues/{number}', 'title': f'Task {number}',
            'body': 'Original body\n\n## Engine commit journal\n- `' + ENGINE_SHA + '`\n\n## Change history\n- Original\n\n',
            'state': 'open', 'type': 'Task', 'labels': ['area:quality'], 'assignees': ['Cephalon-Neza'],
            'milestone_number': 1, 'milestone': 'W0', 'updated_at': 'revision-1',
            'fields': {'Status': 'Ready', 'Priority': 'P0', 'Estimate low (h)': 1, 'Estimate (h)': 2,
                       'Estimate high (h)': 3, 'Actual (h)': None, 'Remaining (h)': None,
                       'Maturity': 'M0', 'Test gate': 'Planned', 'Benchmark gate': 'Not required', 'Feature': 'quality'}}


class FakeTransport:
    def __init__(self, rows):
        self.rows = copy.deepcopy(rows)
        self.schema = catalog()
        self.calls = []
        self.attempts = 0
        self.fail_before = None
        self.fail_after = None
        self.reads = 0
        self.on_read = None

    def catalog(self):
        return copy.deepcopy(self.schema)

    def read(self):
        self.reads += 1
        if self.on_read:
            self.on_read(self)
        return copy.deepcopy(self.rows), [{'number': 1, 'title': 'W0'}]

    def engine_commit(self, sha):
        return sha == ENGINE_SHA

    def mutate(self, kind, number, changes):
        self.attempts += 1
        if self.attempts == self.fail_before:
            raise OSError('Injected failure before transport write')
        value = self.rows[str(number)]
        if kind == 'issue':
            value.update(copy.deepcopy(changes))
            value['updated_at'] = 'revision-' + str(self.attempts + 1)
            value['milestone'] = self.schema['milestones'][str(value['milestone_number'])]['title']
        else:
            value['fields'].update(copy.deepcopy(changes))
            # Project-only mutations deliberately do NOT change issue updated_at.
        self.calls.append((kind, number, copy.deepcopy(changes)))
        if self.attempts == self.fail_after:
            raise OSError('Injected lost transport acknowledgement')

    def patch_issue(self, number, changes):
        self.mutate('issue', number, changes)

    def patch_project(self, number, changes):
        self.mutate('project', number, changes)


class TwoWayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / 'tasks').mkdir()
        self.base = row()
        self.rows = {'1': self.base}
        self.transport = FakeTransport(self.rows)
        self.snapshot_path = self.root / pull.SNAPSHOT_RELATIVE
        self.snapshot_path.parent.mkdir(parents=True)
        self.write_baseline(self.rows)

    def tearDown(self):
        self.temp.cleanup()

    def write_baseline(self, rows):
        previous = {}
        for number, value in rows.items():
            text = pull.render(value)
            (self.root / 'tasks' / f'{number}.md').write_text(text, encoding='utf-8', newline='\n')
            previous[number] = {**copy.deepcopy(value), 'mirror_sha256': pull.digest(text)}
        self.snapshot = {'schema_version': 1, 'project_id': pull.PROJECT_ID, 'issues': previous}
        self.snapshot_text = json.dumps(self.snapshot, ensure_ascii=False, indent=2) + '\n'
        self.snapshot_path.write_text(self.snapshot_text, encoding='utf-8', newline='\n')

    def local(self, changes=None, project=None, body=None):
        value = copy.deepcopy(self.base)
        value.update(changes or {})
        value['fields'].update(project or {})
        if body is not None:
            value['body'] = body
        (self.root / 'tasks/1.md').write_text(pull.render(value), encoding='utf-8', newline='\n')
        return value

    def plan(self, migrations=None):
        return sync.make_plan(self.root, self.snapshot, self.snapshot_text, self.transport.rows,
                              self.transport.catalog(), self.transport.engine_commit, migrations)

    def execute(self, plan):
        return sync.apply_plan(self.root, plan, self.transport, execute=True, approve=plan['plan_sha256'])

    def test_metadata_body_and_null_zero_roundtrip(self):
        body = self.base['body'] + 'Preserve exact trailing body spacing.  \n\n'
        self.local({'title': 'Changed title', 'type': 'Feature', 'labels': ['area:governance'],
                    'assignees': ['reviewer'], 'state': 'closed', 'milestone_number': 2},
                   {'Status': 'Done', 'Priority': 'P2', 'Estimate low (h)': 5, 'Estimate (h)': 6,
                    'Estimate high (h)': 7, 'Actual (h)': 0, 'Remaining (h)': 0,
                    'Maturity': 'M1', 'Test gate': 'Passed', 'Benchmark gate': 'Planned', 'Feature': 'governance'}, body)
        plan = self.plan()
        self.execute(plan)
        actual = self.transport.rows['1']
        self.assertEqual(body, actual['body'])
        self.assertEqual(('Feature', ['reviewer'], 2, 'closed'), (actual['type'], actual['assignees'], actual['milestone_number'], actual['state']))
        self.assertEqual(0, actual['fields']['Actual (h)'])
        self.assertEqual(0, actual['fields']['Remaining (h)'])
        saved = json.loads(self.snapshot_path.read_text(encoding='utf-8'))
        self.assertEqual(pull.editable(actual), pull.editable(saved['issues']['1']))
        parsed = sync.parse_mirror((self.root / 'tasks/1.md').read_text(encoding='utf-8'), '1', actual)
        self.assertEqual(body, parsed['issue']['body'])
        # Now clear measured zero intentionally; null must not be sent as zero.
        self.base, self.snapshot = copy.deepcopy(actual), saved
        self.snapshot_text = self.snapshot_path.read_text(encoding='utf-8')
        self.local(project={'Actual (h)': None, 'Remaining (h)': None})
        self.execute(self.plan())
        self.assertIsNone(self.transport.rows['1']['fields']['Actual (h)'])
        self.assertIsNone(self.transport.rows['1']['fields']['Remaining (h)'])

    def test_apply_defaults_to_dry_run_without_remote_or_checkpoint_writes(self):
        self.local({'title': 'Local title'})
        plan = self.plan()
        text = (self.root / 'tasks/1.md').read_text(encoding='utf-8')
        result = sync.apply_plan(self.root, plan, self.transport)
        self.assertEqual('dry-run', result['status'])
        self.assertEqual([], self.transport.calls)
        self.assertFalse((self.root / '.local/sync-checkpoints').exists())
        self.assertEqual(text, (self.root / 'tasks/1.md').read_text(encoding='utf-8'))

    def test_crlf_issue_body_and_trailing_newlines_are_preserved_without_spurious_change(self):
        self.base['body'] = 'CRLF body\r\n\r\n## Engine commit journal\r\n- `' + ENGINE_SHA + '`\r\n\r\n'
        self.rows = {'1': self.base}
        self.transport = FakeTransport(self.rows)
        self.write_baseline(self.rows)
        plan = self.plan()
        self.assertEqual([], plan['operations'])
        self.execute(plan)
        mirrored = pull.read_tracking_text(self.root / 'tasks/1.md')
        self.assertTrue(mirrored.endswith(self.base['body']))
        self.assertEqual(self.base['body'], self.transport.rows['1']['body'])
        self.assertEqual([], self.transport.calls)

    def test_execute_requires_exact_reviewed_hash(self):
        self.local({'title': 'Local title'})
        with self.assertRaisesRegex(ValueError, 'exact reviewed'):
            sync.apply_plan(self.root, self.plan(), self.transport, execute=True, approve='wrong')
        self.assertEqual([], self.transport.calls)

    def test_disjoint_remote_project_and_local_body_edits_merge(self):
        self.local(body=self.base['body'] + 'Local body addition\n')
        self.transport.rows['1']['fields']['Priority'] = 'P1'
        plan = self.plan()
        self.assertEqual('P1', plan['desired']['1']['project']['Priority'])
        self.assertEqual(1, len(plan['operations']))
        self.execute(plan)
        self.assertEqual('P1', self.transport.rows['1']['fields']['Priority'])
        self.assertTrue(self.transport.rows['1']['body'].endswith('Local body addition\n'))

    def test_divergent_same_field_is_a_three_way_conflict(self):
        self.local({'title': 'Local title'})
        self.transport.rows['1']['title'] = 'Remote title'
        with self.assertRaisesRegex(ValueError, 'Three-way field conflicts'):
            self.plan()
        self.assertEqual([], self.transport.calls)

    def test_converged_same_field_requires_no_duplicate_write(self):
        self.local({'title': 'Same title'})
        self.transport.rows['1']['title'] = 'Same title'
        plan = self.plan()
        self.assertEqual([], plan['operations'])
        self.execute(plan)
        self.assertEqual([], self.transport.calls)

    def test_project_only_drift_after_plan_stops_even_without_updated_at_change(self):
        self.local({'title': 'Local title'})
        plan = self.plan()
        original_revision = self.transport.rows['1']['updated_at']
        self.transport.rows['1']['fields']['Priority'] = 'P3'
        self.assertEqual(original_revision, self.transport.rows['1']['updated_at'])
        with self.assertRaisesRegex(ValueError, 'Project fields changed'):
            self.execute(plan)
        self.assertEqual([], self.transport.calls)

    def test_native_revision_or_body_drift_after_plan_stops(self):
        for change in [{'updated_at': 'someone-commented'}, {'body': 'Someone changed the body'}]:
            with self.subTest(change=change):
                self.transport.rows = copy.deepcopy(self.rows)
                self.local({'title': 'Local title'})
                plan = self.plan()
                self.transport.rows['1'].update(change)
                with self.assertRaisesRegex(ValueError, 'changed since review'):
                    self.execute(plan)
                self.assertEqual([], self.transport.calls)

    def test_local_edit_after_plan_is_preserved(self):
        self.local({'title': 'Local title'})
        plan = self.plan()
        self.local({'title': 'Another local title'})
        with self.assertRaisesRegex(ValueError, 'Local task edits changed'):
            self.execute(plan)
        self.assertEqual([], self.transport.calls)

    def test_local_edit_between_remote_operations_stops_remaining_writes(self):
        self.local({'title': 'Desired title'}, project={'Priority': 'P1'})
        plan = self.plan()
        later = self.base['body'] + 'New local author decision\n'

        def edit_during_readback(transport):
            if transport.reads == 3:
                self.local({'title': 'Desired title'}, project={'Priority': 'P1'}, body=later)

        self.transport.on_read = edit_during_readback
        with self.assertRaisesRegex(ValueError, 'Local task edits changed'):
            self.execute(plan)
        self.assertEqual(1, len(self.transport.calls))
        self.assertEqual('P0', self.transport.rows['1']['fields']['Priority'])
        self.assertTrue(pull.read_tracking_text(self.root / 'tasks/1.md').endswith(later))

    def test_remote_edit_between_operations_is_not_overwritten(self):
        self.local({'title': 'Desired title'}, project={'Priority': 'P1'})
        plan = self.plan()

        def external_write(transport):
            if transport.reads == 4:
                transport.rows['1']['body'] += 'External decision\n'

        self.transport.on_read = external_write
        with self.assertRaisesRegex(ValueError, 'changed since review'):
            self.execute(plan)
        self.assertEqual(1, len(self.transport.calls))
        self.assertTrue(self.transport.rows['1']['body'].endswith('External decision\n'))
        self.assertEqual('P0', self.transport.rows['1']['fields']['Priority'])

    def test_invalid_non_engine_or_short_sha_is_rejected_before_mutation(self):
        for invalid in ['b' * 40, 'abcdef123']:
            with self.subTest(invalid=invalid):
                self.local(body='## Engine commit journal\n- `' + invalid + '`\n')
                with self.assertRaisesRegex(ValueError, 'Engine|40-character'):
                    self.plan()
                self.assertEqual([], self.transport.calls)

    def test_apply_independently_revalidates_engine_sha_even_in_rehashed_plan(self):
        self.local({'title': 'Desired title'})
        plan = self.plan()
        plan['desired']['1']['issue']['body'] = '## Engine commit journal\n- `' + ('b' * 40) + '`\n'
        plan['operations'] = sync.operations(plan['remote_expected'], plan['desired'])
        plan['plan_sha256'] = sync.plan_hash(plan)
        with self.assertRaisesRegex(ValueError, 'Non-Engine'):
            self.execute(plan)
        self.assertEqual([], self.transport.calls)

    def test_editing_mirror_identity_is_rejected_without_mutation(self):
        path = self.root / 'tasks/1.md'
        text = pull.read_tracking_text(path).replace('"item_id": "ITEM-1"', '"item_id": "OTHER-ITEM"')
        path.write_text(text, encoding='utf-8', newline='\n')
        with self.assertRaisesRegex(ValueError, 'immutable mirror identity'):
            self.plan()
        self.assertEqual([], self.transport.calls)

    def test_exact_identity_mapping_adopts_existing_engine_issue_without_creation(self):
        self.transport.rows['1']['node_id'] = 'MIGRATED-ISSUE'
        self.transport.rows['1']['item_id'] = 'MIGRATED-ITEM'
        with self.assertRaisesRegex(ValueError, 'migration mapping required'):
            self.plan()
        mapping = {'1': {'from': {'node_id': 'ISSUE-1', 'item_id': 'ITEM-1'},
                          'to': {'node_id': 'MIGRATED-ISSUE', 'item_id': 'MIGRATED-ITEM'}}}
        self.execute(self.plan(mapping))
        self.assertEqual([], self.transport.calls)
        self.assertIn('MIGRATED-ITEM', (self.root / 'tasks/1.md').read_text(encoding='utf-8'))

    def test_migration_to_non_engine_destination_is_rejected(self):
        self.transport.rows['1']['url'] = 'https://github.com/other/repository/issues/1'
        with self.assertRaisesRegex(ValueError, 'Engine issue membership'):
            self.plan()
        self.assertEqual([], self.transport.calls)

    def test_partial_apply_resumes_without_repeating_completed_issue_patch(self):
        self.local(body=self.base['body'] + 'Local change\n', project={'Priority': 'P1', 'Actual (h)': 0})
        plan = self.plan()
        self.transport.fail_before = 2
        with self.assertRaisesRegex(OSError, 'before transport'):
            self.execute(plan)
        self.assertEqual(1, len(self.transport.calls))
        self.transport.fail_before = None
        self.execute(plan)
        self.assertEqual(1, sum(kind == 'issue' for kind, _, _ in self.transport.calls))
        self.assertEqual(('P1', 0), (self.transport.rows['1']['fields']['Priority'], self.transport.rows['1']['fields']['Actual (h)']))

    def test_lost_acknowledgement_resumes_by_exact_after_state(self):
        self.local({'title': 'Desired title'})
        plan = self.plan()
        self.transport.fail_after = 1
        with self.assertRaisesRegex(OSError, 'lost transport'):
            self.execute(plan)
        self.assertEqual('Desired title', self.transport.rows['1']['title'])
        self.transport.fail_after = None
        self.execute(plan)
        self.assertEqual(1, len(self.transport.calls))

    def test_concurrent_change_after_partial_apply_requires_review_without_rollback(self):
        self.local({'title': 'Desired title'}, project={'Priority': 'P1'})
        plan = self.plan()
        self.transport.fail_before = 2
        with self.assertRaises(OSError):
            self.execute(plan)
        self.transport.fail_before = None
        self.transport.rows['1']['body'] += 'External writer changed body\n'
        count = len(self.transport.calls)
        with self.assertRaisesRegex(ValueError, 'conflict|changed'):
            self.execute(plan)
        self.assertEqual(count, len(self.transport.calls))
        self.assertEqual('Desired title', self.transport.rows['1']['title'])
        self.assertTrue(self.transport.rows['1']['body'].endswith('External writer changed body\n'))

    def test_complete_reapply_is_idempotent_and_later_remote_edits_are_not_overwritten(self):
        self.local({'title': 'Desired title'})
        plan = self.plan()
        self.execute(plan)
        count = len(self.transport.calls)
        result = self.execute(plan)
        self.assertEqual('already-applied', result['status'])
        self.assertEqual(count, len(self.transport.calls))
        self.transport.rows['1']['fields']['Status'] = 'Review'
        with self.assertRaisesRegex(ValueError, 'changed since review'):
            self.execute(plan)
        self.assertEqual(count, len(self.transport.calls))

    def test_local_reconcile_failure_resumes_without_repeating_remote_write(self):
        self.local({'title': 'Desired title'})
        plan = self.plan()
        with patch('pull_tracking._commit_transaction', side_effect=OSError('Injected local staging failure')):
            with self.assertRaisesRegex(OSError, 'local staging'):
                self.execute(plan)
        self.assertEqual(1, len(self.transport.calls))
        self.execute(plan)
        self.assertEqual(1, len(self.transport.calls))
        self.assertIn('Desired title', (self.root / 'tasks/1.md').read_text(encoding='utf-8'))

    def test_lost_final_checkpoint_acknowledgement_recognizes_exact_local_commit(self):
        self.local({'title': 'Desired title'})
        plan = self.plan()
        save = sync._save_checkpoint

        def fail_final_ack(path, checkpoint):
            if checkpoint['phase'] == 'complete':
                raise OSError('Injected final checkpoint acknowledgement failure')
            return save(path, checkpoint)

        with patch('sync_tracking._save_checkpoint', side_effect=fail_final_ack):
            with self.assertRaisesRegex(OSError, 'final checkpoint'):
                self.execute(plan)
        self.assertIn('Desired title', (self.root / 'tasks/1.md').read_text(encoding='utf-8'))
        self.execute(plan)
        self.assertEqual(1, len(self.transport.calls))

    def test_source_and_executable_paths_cannot_be_used_as_checkpoint_output(self):
        self.local({'title': 'Desired title'})
        plan = self.plan()
        for path in [self.root / 'tools/sync_tracking.py', self.root / 'tasks/1.md', self.root / '.git/config', self.root / '.local/plan.py']:
            with self.subTest(path=path), self.assertRaisesRegex(ValueError, 'JSON files inside'):
                sync.apply_plan(self.root, plan, self.transport, checkpoint_path=path, execute=True, approve=plan['plan_sha256'])
        self.assertEqual([], self.transport.calls)

    def test_unknown_options_schema_changes_and_corrupt_plan_stop_before_mutation(self):
        self.local({'title': 'Desired title'})
        plan = self.plan()
        self.transport.schema['fields']['Priority']['options']['P4'] = 'OPTION-P4'
        with self.assertRaisesRegex(ValueError, 'schema changed'):
            self.execute(plan)
        self.transport.schema = catalog()
        plan['operations'][0]['changes']['title'] = 'Unreviewed title'
        with self.assertRaisesRegex(ValueError, 'checksum changed'):
            self.execute(plan)
        self.assertEqual([], self.transport.calls)

    def test_corrupt_checkpoint_does_not_weaken_remote_preconditions(self):
        self.local({'title': 'Desired title'}, project={'Priority': 'P1'})
        plan = self.plan()
        self.transport.fail_before = 2
        with self.assertRaises(OSError):
            self.execute(plan)
        checkpoint = self.root / '.local/sync-checkpoints' / (plan['plan_sha256'] + '.json')
        content = json.loads(checkpoint.read_text(encoding='utf-8'))
        content['remote_expected']['1']['values']['project']['Priority'] = 'P3'
        checkpoint.write_text(json.dumps(content), encoding='utf-8', newline='\n')
        self.transport.fail_before = None
        with self.assertRaisesRegex(ValueError, 'Checkpoint checksum changed'):
            self.execute(plan)
        self.assertEqual(1, len(self.transport.calls))

    def forged_checkpoint(self, plan, **changes):
        checkpoint = {'schema_version': 1, 'plan_sha256': plan['plan_sha256'], 'phase': 'remote',
                      'next_operation': 0, 'remote_expected': copy.deepcopy(plan['remote_expected']),
                      'inflight': None, 'local_files': copy.deepcopy(plan['local_files']),
                      'snapshot_sha256': plan['snapshot_sha256']}
        checkpoint.update(changes)
        path = self.root / '.local/sync-checkpoints' / (plan['plan_sha256'] + '.json')
        # Deliberately rehash the forged checkpoint: a checksum is not authority.
        sync._save_checkpoint(path, checkpoint)
        return checkpoint

    def test_rehashed_complete_checkpoint_cannot_skip_unapplied_operations(self):
        self.local({'title': 'Desired title'})
        plan = self.plan()
        self.forged_checkpoint(plan, phase='complete', next_operation=0)
        with self.assertRaisesRegex(ValueError, 'requires all reviewed remote operations'):
            self.execute(plan)
        self.assertEqual([], self.transport.calls)
        self.assertEqual(self.base['title'], self.transport.rows['1']['title'])

    def test_rehashed_checkpoint_cannot_replace_reviewed_local_edit_anchor(self):
        self.local({'title': 'Desired title'})
        plan = self.plan()
        later_body = self.base['body'] + 'Unreviewed local addition after plan\n'
        self.local({'title': 'Desired title'}, body=later_body)
        self.forged_checkpoint(plan, local_files={'1': pull.digest(pull.read_tracking_text(self.root / 'tasks/1.md'))})
        with self.assertRaisesRegex(ValueError, 'local anchors differ from the reviewed plan'):
            self.execute(plan)
        self.assertEqual([], self.transport.calls)
        self.assertTrue(pull.read_tracking_text(self.root / 'tasks/1.md').endswith(later_body))

    def test_rehashed_checkpoint_cannot_replace_reviewed_snapshot_anchor(self):
        self.local({'title': 'Desired title'})
        plan = self.plan()
        changed = self.snapshot_text + 'Unreviewed local snapshot edit\n'
        self.snapshot_path.write_text(changed, encoding='utf-8', newline='\n')
        self.forged_checkpoint(plan, snapshot_sha256=pull.digest(changed))
        with self.assertRaisesRegex(ValueError, 'local anchors differ from the reviewed plan'):
            self.execute(plan)
        self.assertEqual([], self.transport.calls)
        self.assertEqual(changed, pull.read_tracking_text(self.snapshot_path))

    def test_rehashed_unknown_phase_and_invalid_inflight_position_are_rejected(self):
        self.local({'title': 'Desired title'})
        plan = self.plan()
        for changes in [{'phase': 'unknown'}, {'inflight': 1}, {'inflight': True},
                        {'phase': 'local-reconcile', 'next_operation': 0}]:
            with self.subTest(changes=changes):
                self.forged_checkpoint(plan, **changes)
                with self.assertRaises(ValueError):
                    self.execute(plan)
                self.assertEqual([], self.transport.calls)

    def test_rehashed_complete_checkpoint_cannot_adopt_a_later_local_edit(self):
        self.local({'title': 'Desired title'})
        plan = self.plan()
        self.execute(plan)
        path = self.root / '.local/sync-checkpoints' / (plan['plan_sha256'] + '.json')
        checkpoint = json.loads(path.read_text(encoding='utf-8'))
        later = pull.read_tracking_text(self.root / 'tasks/1.md') + 'Later external decision\n'
        (self.root / 'tasks/1.md').write_text(later, encoding='utf-8', newline='\n')
        checkpoint['local_files']['1'] = pull.digest(later)
        sync._save_checkpoint(path, checkpoint)
        count = len(self.transport.calls)
        with self.assertRaisesRegex(ValueError, 'validated final transaction'):
            self.execute(plan)
        self.assertEqual(count, len(self.transport.calls))
        self.assertEqual(later, pull.read_tracking_text(self.root / 'tasks/1.md'))

    def test_project_field_type_mismatch_is_rejected_before_any_issue_write(self):
        self.local({'title': 'Desired title'})
        self.transport.schema['fields']['Actual (h)']['data_type'] = 'TEXT'
        with self.assertRaisesRegex(ValueError, 'field data type differs'):
            self.plan()
        self.assertEqual([], self.transport.calls)

    def test_illegal_numeric_bool_negative_and_nonfinite_values_do_not_plan(self):
        for invalid in [True, -1, float('nan'), float('inf')]:
            with self.subTest(invalid=invalid):
                self.local(project={'Actual (h)': invalid})
                with self.assertRaisesRegex(ValueError, 'finite numbers'):
                    self.plan()


class FixedTransportPayloadTests(unittest.TestCase):
    def test_catalog_rejects_visibility_or_identity_drift_before_fetching_schema(self):
        accepted = {'full_name': pull.REPO, 'visibility': 'public', 'private': False}
        for changed in ({'visibility': 'private', 'private': True},
                        {'visibility': 'internal', 'private': True},
                        {'private': True}, {'full_name': 'another/Engine'}):
            with self.subTest(changed=changed):
                response = {'login': 'Cephalon-Neza'}, accepted | changed
                transport = sync.GitHubTransport()
                with patch('pull_tracking.gh', side_effect=response) as call:
                    with self.assertRaisesRegex(ValueError, 'repository identity or visibility'):
                        transport.catalog()
                self.assertEqual(call.call_count, 2)

    def test_native_patch_uses_fixed_engine_endpoint_and_native_type_and_milestone(self):
        transport = sync.GitHubTransport()
        with patch('pull_tracking.gh', return_value={}) as call:
            transport.patch_issue(23, {'type': 'Task', 'milestone_number': 1, 'body': 'Exact body\n'})
        self.assertEqual('repos/' + pull.REPO + '/issues/23', call.call_args.args[1])
        self.assertEqual({'type': 'Task', 'milestone': 1, 'body': 'Exact body\n'}, call.call_args.kwargs['body'])

    def test_project_zero_updates_number_while_null_clears_existing_field(self):
        transport = sync.GitHubTransport()
        transport._catalog, transport._rows = catalog(), {'1': row()}
        with patch('pull_tracking.gh', return_value={}) as call:
            transport.patch_project(1, {'Actual (h)': 0})
            zero_query = call.call_args.kwargs['body']['query']
            transport.patch_project(1, {'Actual (h)': None})
            null_query = call.call_args.kwargs['body']['query']
        self.assertIn('number:0', zero_query)
        self.assertIn('updateProjectV2ItemFieldValue', zero_query)
        self.assertIn('clearProjectV2ItemFieldValue', null_query)
        self.assertNotIn('number:0', null_query)


class GitMirrorBytePreservationTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which('git'), 'Git is unavailable; index-byte regression requires Git')
    def test_real_repository_attributes_preserve_mixed_newline_body_in_git_index(self):
        git = shutil.which('git')
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run([git, '-C', str(root), 'init', '--quiet'], check=True, capture_output=True)
            subprocess.run([git, '-C', str(root), 'config', 'core.autocrlf', 'true'], check=True, capture_output=True)
            actual_attributes = Path(__file__).resolve().parents[1] / '.gitattributes'
            (root / '.gitattributes').write_bytes(actual_attributes.read_bytes())
            (root / 'tasks').mkdir()
            fixture = row()
            fixture['body'] = 'Exact CRLF issue body\r\nLine with trailing spaces.  \r\n\r\n'
            original = pull.render(fixture).encode('utf-8')
            self.assertIn(b'<!-- cehpalon-issue-body -->\nExact CRLF', original)
            self.assertTrue(original.endswith(b'  \r\n\r\n'))
            (root / 'tasks/1.md').write_bytes(original)
            subprocess.run([git, '-C', str(root), 'add', '--', '.gitattributes', 'tasks/1.md'], check=True, capture_output=True)
            blob = subprocess.run([git, '-C', str(root), 'show', ':tasks/1.md'], check=True, capture_output=True).stdout
            self.assertEqual(original, blob)


class PaginatedReadTests(unittest.TestCase):
    def setUp(self):
        self.values = [row(i) for i in range(1, 102)]
        self.rest = [{**value, 'html_url': value['url'], 'type': {'name': value['type']},
                      'labels': [{'name': name} for name in value['labels']],
                      'assignees': [{'login': name} for name in value['assignees']],
                      'milestone': {'number': 1, 'title': 'W0'}} for value in self.values]
        self.issue_pages = [self.rest[:100], self.rest[100:]]
        self.milestones = [{'number': 1, 'title': 'W0', 'state': 'open', 'description': '', 'due_on': None,
                            'open_issues': 101, 'closed_issues': 0},
                           {'number': 2, 'title': 'W1', 'state': 'open', 'description': '', 'due_on': None,
                            'open_issues': 0, 'closed_issues': 0}]
        self.items = []
        for value in self.values:
            field_values = []
            for name, content in value['fields'].items():
                if content is not None:
                    kind = 'number' if name in sync.NUMERIC_FIELDS else ('text' if name == 'Feature' else 'name')
                    field_values.append({'field': {'name': name}, kind: content})
            self.items.append({'id': value['item_id'], 'content': {'number': value['number'], 'id': value['node_id'],
                               'repository': {'nameWithOwner': pull.REPO}},
                               'fieldValues': {'pageInfo': {'hasNextPage': False}, 'nodes': field_values}})
        self.calls = []

    def fake_gh(self, *args, body=None):
        self.calls.append((args, body))
        if args[1].startswith('repos/') and '/issues?' in args[1]:
            return self.issue_pages
        if args[1].startswith('repos/') and '/milestones?' in args[1]:
            return [[self.milestones[0]], [self.milestones[1]]]
        query = body['query']
        if 'projectV2(number:4)' in query:
            second = 'after:"ITEM-CURSOR"' in query
            page = {'nodes': self.items[100:] if second else self.items[:100],
                    'pageInfo': {'hasNextPage': not second, 'endCursor': 'ITEM-CURSOR' if not second else None}}
            return {'data': {'organization': {'projectV2': {'id': pull.PROJECT_ID, 'title': 'Engine',
                    'public': False, 'closed': False, 'items': page}}}}
        second = 'after:"MILESTONE-CURSOR"' in query
        nodes = [{'number': 2, 'open': {'totalCount': 0}, 'closed': {'totalCount': 0}}] if second else [
                 {'number': 1, 'open': {'totalCount': 101}, 'closed': {'totalCount': 0}}]
        return {'data': {'repository': {'milestones': {'nodes': nodes,
                'pageInfo': {'hasNextPage': not second, 'endCursor': 'MILESTONE-CURSOR' if not second else None}}}}}

    def test_rest_issues_project_items_and_milestones_consume_all_pages(self):
        with patch('pull_tracking.gh', side_effect=self.fake_gh):
            rows, milestones = pull.fetch()
        self.assertEqual(101, len(rows))
        self.assertEqual('ITEM-101', rows['101']['item_id'])
        self.assertEqual([1, 2], [value['number'] for value in milestones])
        self.assertTrue(all('--paginate' in args and '--slurp' in args for args, body in self.calls if args[1] != 'graphql'))
        self.assertTrue(any('after:"ITEM-CURSOR"' in body['query'] for args, body in self.calls if body))
        self.assertTrue(any('after:"MILESTONE-CURSOR"' in body['query'] for args, body in self.calls if body))

    def test_duplicated_rest_issue_page_is_rejected(self):
        self.issue_pages = [[self.rest[0]], [self.rest[0]]]
        with patch('pull_tracking.gh', side_effect=self.fake_gh):
            with self.assertRaisesRegex(ValueError, 'pagination is duplicated'):
                pull.fetch()

    def test_item_field_value_overflow_is_rejected_instead_of_silently_truncated(self):
        self.items[0]['fieldValues']['pageInfo']['hasNextPage'] = True
        with patch('pull_tracking.gh', side_effect=self.fake_gh):
            with self.assertRaisesRegex(ValueError, 'field pagination'):
                pull.fetch()

    def test_rest_and_project_issue_node_identity_mismatch_is_rejected(self):
        self.items[0]['content']['id'] = 'OTHER-ISSUE'
        with patch('pull_tracking.gh', side_effect=self.fake_gh):
            with self.assertRaisesRegex(ValueError, 'identity observations disagree'):
                pull.fetch()


if __name__ == '__main__':
    unittest.main()
