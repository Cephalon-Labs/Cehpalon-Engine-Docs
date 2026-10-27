"""Reviewed two-way Engine/Docs tracking. Remote writes require apply --execute.

JSON plans are data, never executable code or endpoint/path instructions. GitHub
does not offer an atomic transaction spanning issue and Project mutations: this
tool uses full-state optimistic guards, readback and resumable checkpoints. Keep
external writers idle during apply; final check-to-mutation races remain possible.
"""
import argparse
import copy
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path

import pull_tracking as pull

MAX_ISSUES = 1000
MAX_OPERATIONS = 12000
ISSUE_FIELDS = ('title', 'type', 'labels', 'assignees', 'state', 'milestone_number', 'body')
NUMERIC_FIELDS = ('Estimate low (h)', 'Estimate (h)', 'Estimate high (h)', 'Actual (h)', 'Remaining (h)')
METADATA = re.compile(r'\A# Engine issue #(\d+)\n\n<!-- cehpalon-tracking:v1 -->\n```json\n(.*?)\n```\n<!-- /cehpalon-tracking -->\n\n<!-- cehpalon-issue-body -->\n(.*)\Z', re.S)


def stamp():
    return datetime.now(timezone.utc).isoformat()


def parse_mirror(text, number, identity):
    match = METADATA.fullmatch(text)
    if not match or int(match[1]) != int(number):
        raise ValueError(f'Issue #{number}: expected editable v1 mirror; run a reviewed pull to migrate legacy headers first')
    metadata = json.loads(match[2])
    if set(metadata) != {'schema_version', 'repository', 'project_id', 'identity', 'issue', 'project'}:
        raise ValueError(f'Issue #{number}: unsupported metadata keys')
    if metadata['schema_version'] != 1 or metadata['repository'] != pull.REPO or metadata['project_id'] != pull.PROJECT_ID:
        raise ValueError('Mirror repository/project/schema is immutable')
    expected = {key: identity[key] for key in ('number', 'node_id', 'item_id', 'url')}
    if metadata['identity'] != expected:
        raise ValueError(f'Issue #{number}: immutable mirror identity changed; use an explicit migration mapping')
    if set(metadata['issue']) != set(ISSUE_FIELDS) - {'body'} or set(metadata['project']) != set(pull.PROJECT_FIELDS):
        raise ValueError(f'Issue #{number}: editable field set differs from schema')
    return {'issue': {**metadata['issue'], 'body': match[3]}, 'project': metadata['project']}


def validate_values(values, catalog):
    if set(values) != {'issue', 'project'} or set(values['issue']) != set(ISSUE_FIELDS) or set(values['project']) != set(pull.PROJECT_FIELDS):
        raise ValueError('Unsupported editable value schema')
    issue, project = values['issue'], values['project']
    if not isinstance(issue['title'], str) or not issue['title'].strip() or len(issue['title']) > 256 or any(x in issue['title'] for x in '\r\n'):
        raise ValueError('Issue title must be nonempty and single-line')
    if issue['type'] not in catalog['types'] or issue['state'] not in ('open', 'closed'):
        raise ValueError('Unknown native Issue Type or state')
    if not isinstance(issue['body'], str) or len(issue['body']) > 65536:
        raise ValueError('Issue body must be text within the API size limit')
    for key, known, required in [('labels', catalog['labels'], True), ('assignees', catalog['assignees'], False)]:
        value = issue[key]
        if not isinstance(value, list) or any(not isinstance(x, str) for x in value) or len(value) != len(set(value)) or (required and not value):
            raise ValueError(f'Invalid {key} list')
        if set(value) - set(known):
            raise ValueError(f'Unknown or unassignable {key}: {sorted(set(value) - set(known))}')
        issue[key] = sorted(value)
    milestone = issue['milestone_number']
    if isinstance(milestone, bool) or not isinstance(milestone, int) or str(milestone) not in catalog['milestones']:
        raise ValueError('Select an existing native milestone number')
    for name in pull.PROJECT_FIELDS:
        specification = catalog['fields'].get(name)
        if not specification:
            raise ValueError('Project field missing from current schema: ' + name)
        expected_type = 'NUMBER' if name in NUMERIC_FIELDS else ('TEXT' if name == 'Feature' else 'SINGLE_SELECT')
        if specification.get('data_type') != expected_type:
            raise ValueError('Project field data type differs from supported schema: ' + name)
        value = project[name]
        if name in NUMERIC_FIELDS:
            if value is not None and (isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0):
                raise ValueError('Hours must be nonnegative finite numbers or null: ' + name)
        elif name == 'Feature':
            if not isinstance(value, str) or not value.strip():
                raise ValueError('Feature must be nonempty text')
        elif value not in specification['options']:
            raise ValueError(f'Unknown Project {name} option: {value}')
    low, mid, high = [project[x] for x in ('Estimate low (h)', 'Estimate (h)', 'Estimate high (h)')]
    if all(x is not None for x in (low, mid, high)) and not low <= mid <= high:
        raise ValueError('Estimate low/mid/high ordering is invalid')


def validate_engine_references(values, engine_commit):
    body = values['issue']['body']
    if re.search(r'Cehpalon-Engine-(?:Docs|Samples)/(?:commit|commits)/', body, re.I):
        raise ValueError('Task/card commit references must belong only to Engine')
    journal = re.search(r'(?im)^## Engine commit journal\s*\n(.*?)(?=^## |\Z)', body, re.S | re.M)
    if journal and re.search(r'(?<![0-9a-f])[0-9a-f]{7,39}(?![0-9a-f])', journal[1], re.I):
        raise ValueError('Commit journal requires full 40-character Engine SHAs')
    for sha in sorted(set(re.findall(r'(?<![0-9a-f])[0-9a-f]{40}(?![0-9a-f])', body, re.I))):
        if not engine_commit(sha.lower()):
            raise ValueError('Non-Engine or unresolved commit SHA in task/card: ' + sha)


def state(row):
    return {'number': row['number'], 'node_id': row['node_id'], 'item_id': row['item_id'],
            'url': row['url'], 'updated_at': row.get('updated_at'), 'values': pull.editable(row)}


def require_membership(row, number):
    if isinstance(row['number'], bool) or row['number'] != int(number) or row['url'] != f'https://github.com/{pull.REPO}/issues/{int(number)}':
        raise ValueError('Destination does not prove Engine issue membership')
    if not row['node_id'] or not row['item_id']:
        raise ValueError('Destination issue/item identity is missing')


def operations(expected, desired):
    result = []
    for number in sorted(expected, key=int):
        before = copy.deepcopy(expected[number]['values'])
        native = {name: desired[number]['issue'][name] for name in ISSUE_FIELDS if before['issue'][name] != desired[number]['issue'][name]}
        if native:
            after = copy.deepcopy(before)
            after['issue'].update(native)
            result.append({'number': int(number), 'kind': 'issue', 'changes': native, 'before': before, 'after': after})
            before = after
        for name in pull.PROJECT_FIELDS:
            if before['project'][name] != desired[number]['project'][name]:
                after = copy.deepcopy(before)
                after['project'][name] = desired[number]['project'][name]
                result.append({'number': int(number), 'kind': 'project', 'changes': {name: desired[number]['project'][name]}, 'before': before, 'after': after})
                before = after
    if len(result) > MAX_OPERATIONS:
        raise ValueError('Operation bound exceeded; split and review the batch')
    return result


def plan_hash(plan):
    return pull.digest(pull.canonical({k: v for k, v in plan.items() if k != 'plan_sha256'}))


def make_plan(root, snapshot, snapshot_text, remote, catalog, engine_commit, migrations=None):
    previous = snapshot['issues']
    if snapshot.get('project_id') != pull.PROJECT_ID or not 0 < len(remote) <= MAX_ISSUES:
        raise ValueError('Snapshot identity or issue-count bound is invalid')
    if set(previous) - set(remote):
        raise ValueError('Tracked issues disappeared; no automatic deletion or issue recreation')
    mappings = migrations or {}
    if set(mappings) - set(previous):
        raise ValueError('Unused or unknown identity migration mapping')
    local_files, desired, expected, merge_notes = {}, {}, {}, []
    conflicts = []
    for number, row in remote.items():
        if not number.isascii() or not number.isdecimal() or int(number) <= 0 or str(int(number)) != number:
            raise ValueError('Invalid issue key')
        require_membership(row, number)
        path = root / 'tasks' / f'{int(number)}.md'
        if number not in previous:
            if path.exists():
                raise ValueError('Unanchored local mirror exists: ' + str(path))
            local_files[number] = None
            desired[number] = pull.editable(row)
            expected[number] = state(row)
            continue
        base = previous[number]
        old_identity = {key: base[key] for key in ('node_id', 'item_id')}
        new_identity = {key: row[key] for key in ('node_id', 'item_id')}
        if old_identity != new_identity:
            if mappings.get(number) != {'from': old_identity, 'to': new_identity}:
                raise ValueError(f'Issue #{number}: explicit exact identity migration mapping required')
        elif number in mappings:
            raise ValueError(f'Issue #{number}: migration does not change an identity')
        text = pull.read_tracking_text(path)
        local_files[number] = pull.digest(text)
        local = parse_mirror(text, number, base)
        original, upstream = pull.editable(base), pull.editable(row)
        merged = copy.deepcopy(upstream)
        for group in ('issue', 'project'):
            for name, old in original[group].items():
                ours, theirs = local[group][name], upstream[group][name]
                if ours == old:
                    selected = theirs
                elif theirs == old or ours == theirs:
                    selected = ours
                else:
                    conflicts.append({'number': int(number), 'field': group + '.' + name,
                                      'base': old, 'local': ours, 'remote': theirs})
                    continue
                merged[group][name] = selected
                if ours != old or theirs != old:
                    merge_notes.append({'number': int(number), 'field': group + '.' + name,
                                        'base': old, 'local': ours, 'remote': theirs, 'selected': selected})
        validate_values(merged, catalog)
        validate_engine_references(merged, engine_commit)
        desired[number], expected[number] = merged, state(row)
    if conflicts:
        raise ValueError('Three-way field conflicts require review: ' + json.dumps(conflicts, ensure_ascii=False))
    for values in desired.values():
        validate_values(values, catalog)
        validate_engine_references(values, engine_commit)
    plan = {'schema_version': 1, 'repository': pull.REPO, 'project_id': pull.PROJECT_ID,
            'created_at_utc': stamp(), 'snapshot_sha256': pull.digest(snapshot_text),
            'catalog_sha256': pull.digest(pull.canonical(catalog)), 'local_files': local_files,
            'remote_expected': expected, 'desired': desired, 'migrations': mappings,
            'merge_notes': merge_notes, 'operations': operations(expected, desired),
            'limits': {'max_issues': MAX_ISSUES, 'max_operations': MAX_OPERATIONS},
            'proof_boundary': 'Reviewed metadata synchronization only; no runtime maturity promotion'}
    plan['plan_sha256'] = plan_hash(plan)
    return plan


def local_fingerprints(root, numbers):
    result = {}
    for number in numbers:
        path = root / 'tasks' / f'{int(number)}.md'
        result[number] = pull.digest(pull.read_tracking_text(path)) if path.exists() else None
    return result


def check_local(root, files, snapshot_sha):
    if local_fingerprints(root, files) != files:
        raise ValueError('Local task edits changed since the reviewed plan/checkpoint')
    path = root / pull.SNAPSHOT_RELATIVE
    observed = pull.digest(pull.read_tracking_text(path)) if path.exists() else None
    if observed != snapshot_sha:
        raise ValueError('Local snapshot changed since the reviewed plan/checkpoint')


def guard_remote(rows, expected, transition=None):
    if set(rows) != set(expected):
        raise ValueError('Remote issue set changed since review')
    for number, before in expected.items():
        require_membership(rows[number], number)
        observed = state(rows[number])
        if transition is not None and number == str(transition['number']):
            identity_keys = ('number', 'node_id', 'item_id', 'url')
            if any(observed[x] != before[x] for x in identity_keys) or observed['values'] != transition['after']:
                raise ValueError(f'Readback/conflict for in-flight issue #{number}')
        elif observed != before:
            raise ValueError(f'Remote issue revision or Project fields changed since review: #{number}')


def validate_plan(plan, catalog, engine_commit):
    if plan.get('schema_version') != 1 or plan.get('repository') != pull.REPO or plan.get('project_id') != pull.PROJECT_ID:
        raise ValueError('Plan identity/schema does not match this program')
    if plan.get('plan_sha256') != plan_hash(plan):
        raise ValueError('Plan checksum changed; regenerate and review it')
    if plan['catalog_sha256'] != pull.digest(pull.canonical(catalog)):
        raise ValueError('Remote field/label/type/milestone/assignee schema changed since planning')
    keys = set(plan['remote_expected'])
    if not 0 < len(keys) <= MAX_ISSUES or keys != set(plan['local_files']) or keys != set(plan['desired']):
        raise ValueError('Plan issue sets/bounds differ')
    for number in keys:
        if not number.isascii() or not number.isdecimal() or int(number) <= 0 or str(int(number)) != number:
            raise ValueError('Invalid numeric issue key')
        row = plan['remote_expected'][number]
        require_membership(row, number)
        validate_values(plan['desired'][number], catalog)
        validate_engine_references(plan['desired'][number], engine_commit)
    if plan['operations'] != operations(plan['remote_expected'], plan['desired']):
        raise ValueError('Plan operation list does not match its exact reviewed value changes')


def _save_checkpoint(path, checkpoint):
    checkpoint['checkpoint_sha256'] = pull.digest(pull.canonical({k: v for k, v in checkpoint.items() if k != 'checkpoint_sha256'}))
    pull._atomic_json(path, checkpoint)


def _validate_checkpoint(plan, checkpoint):
    expected_hash = pull.digest(pull.canonical({k: v for k, v in checkpoint.items() if k != 'checkpoint_sha256'}))
    if checkpoint.get('checkpoint_sha256') != expected_hash:
        raise ValueError('Checkpoint checksum changed; review recovery state')
    index = checkpoint.get('next_operation')
    if isinstance(index, bool) or not isinstance(index, int) or not 0 <= index <= len(plan['operations']):
        raise ValueError('Invalid checkpoint operation position')
    phase = checkpoint.get('phase')
    if phase not in ('remote', 'local-reconcile', 'complete'):
        raise ValueError('Invalid checkpoint phase')
    inflight = checkpoint.get('inflight')
    if inflight is not None and (isinstance(inflight, bool) or inflight != index or index >= len(plan['operations'])):
        raise ValueError('Invalid in-flight checkpoint operation')
    if phase != 'remote' and (index != len(plan['operations']) or inflight is not None):
        raise ValueError('Local/complete checkpoint requires all reviewed remote operations')
    simulated = {n: copy.deepcopy(row['values']) for n, row in plan['remote_expected'].items()}
    for operation in plan['operations'][:index]:
        simulated[str(operation['number'])] = operation['after']
    if set(simulated) != set(checkpoint['remote_expected']):
        raise ValueError('Checkpoint issue identities differ from plan')
    for number, row in checkpoint['remote_expected'].items():
        if row['values'] != simulated[number] or any(row[key] != plan['remote_expected'][number][key] for key in ('number', 'node_id', 'item_id', 'url')):
            raise ValueError('Checkpoint state does not match completed plan operations')
    pending = checkpoint.get('local_transaction')
    if phase == 'remote' and pending is not None:
        raise ValueError('Remote checkpoint cannot adopt an unvalidated local transaction')
    if phase != 'complete' and (checkpoint.get('local_files') != plan['local_files'] or checkpoint.get('snapshot_sha256') != plan['snapshot_sha256']):
        raise ValueError('Checkpoint local anchors differ from the reviewed plan')
    if phase != 'remote':
        if not isinstance(pending, dict) or set(pending) != {'snapshot', 'mirror_hashes', 'snapshot_sha256'}:
            raise ValueError('Local/complete checkpoint lacks its exact final local transaction')
        if pending['snapshot_sha256'] != pull.digest(pending['snapshot']):
            raise ValueError('Checkpoint final snapshot content/hash differ')
        snapshot = json.loads(pending['snapshot'])
        if snapshot.get('schema_version') != 1 or snapshot.get('project_id') != pull.PROJECT_ID or set(snapshot.get('issues', {})) != set(simulated):
            raise ValueError('Checkpoint final snapshot identity differs from the plan')
        derived_hashes = {}
        for number, row in snapshot['issues'].items():
            if state(row) != checkpoint['remote_expected'][number] or pull.editable(row) != plan['desired'][number]:
                raise ValueError('Checkpoint final snapshot does not represent the reviewed target state')
            derived_hashes[number] = pull.digest(pull.render(row))
            if row.get('mirror_sha256') != derived_hashes[number]:
                raise ValueError('Checkpoint final mirror content/hash differ')
        if pending['mirror_hashes'] != derived_hashes:
            raise ValueError('Checkpoint final mirror anchors are not derived from its validated target state')
        if phase == 'complete' and (checkpoint.get('local_files') != derived_hashes or checkpoint.get('snapshot_sha256') != pending['snapshot_sha256']):
            raise ValueError('Complete checkpoint local anchors do not match the validated final transaction')


def _finish_local(root, rows, milestones, checkpoint, checkpoint_path):
    pending = checkpoint.get('local_transaction')
    if pending is None:
        reconciled = {number: {**row, 'mirror_sha256': pull.digest(pull.render(row)),
                              'remote_sha256': pull.digest(pull.canonical(row))} for number, row in rows.items()}
        snapshot = json.dumps({'schema_version': 1, 'observed_at_utc': stamp(), 'project_id': pull.PROJECT_ID,
                              'scope': 'Live two-way tracking readback only; no runtime proof',
                              'milestones': milestones, 'issues': reconciled}, ensure_ascii=False, indent=2) + '\n'
        pending = {'snapshot': snapshot, 'mirror_hashes': {n: pull.digest(pull.render(r)) for n, r in rows.items()},
                   'snapshot_sha256': pull.digest(snapshot)}
        checkpoint['local_transaction'] = pending
        checkpoint['phase'] = 'local-reconcile'
        _save_checkpoint(checkpoint_path, checkpoint)
    _validate_local_readback(pending, rows, milestones)
    current_files = local_fingerprints(root, checkpoint['local_files'])
    snapshot_path = root / pull.SNAPSHOT_RELATIVE
    current_snapshot = pull.digest(pull.read_tracking_text(snapshot_path)) if snapshot_path.exists() else None
    if current_files == pending['mirror_hashes'] and current_snapshot == pending['snapshot_sha256']:
        # The previous process committed locally but lost the final checkpoint acknowledgement.
        pass
    else:
        check_local(root, checkpoint['local_files'], checkpoint['snapshot_sha256'])
        planned = {root / 'tasks' / f'{int(n)}.md': pull.render(row) for n, row in rows.items()}
        expected = {root / 'tasks' / f'{int(n)}.md': value for n, value in checkpoint['local_files'].items()}
        planned[snapshot_path], expected[snapshot_path] = pending['snapshot'], checkpoint['snapshot_sha256']
        pull._commit_transaction(root, planned, expected)
    checkpoint['local_files'] = pending['mirror_hashes']
    checkpoint['snapshot_sha256'] = pending['snapshot_sha256']
    checkpoint['phase'] = 'complete'
    checkpoint['completed_at_utc'] = stamp()
    _save_checkpoint(checkpoint_path, checkpoint)


def _validate_local_readback(pending, rows, milestones):
    snapshot = json.loads(pending['snapshot'])
    if set(snapshot['issues']) != set(rows):
        raise ValueError('Checkpoint final snapshot issue set differs from fresh readback')
    for number, row in rows.items():
        if state(snapshot['issues'][number]) != state(row) or pending['mirror_hashes'].get(number) != pull.digest(pull.render(row)):
            raise ValueError('Checkpoint final local content differs from fresh validated readback')
    if pull.milestone_metadata(snapshot.get('milestones', [])) != pull.milestone_metadata(milestones):
        raise ValueError('Checkpoint final milestone metadata differs from fresh readback')


def apply_plan(root, plan, transport, checkpoint_path=None, execute=False, approve=None):
    """No default mutation. A failed/uncertain dispatch is resumed by exact readback."""
    if execute and approve != plan.get('plan_sha256'):
        raise ValueError('Execute requires the exact reviewed --approve plan SHA256')
    checkpoint_path = checkpoint_path or root / '.local/sync-checkpoints' / (plan['plan_sha256'] + '.json')
    checkpoint_path = local_json_path(root, checkpoint_path)
    with pull.exclusive_pull(root):
        catalog = transport.catalog()
        validate_plan(plan, catalog, transport.engine_commit)
        checkpoint = json.loads(checkpoint_path.read_text(encoding='utf-8')) if checkpoint_path.exists() else None
        if checkpoint is None:
            checkpoint = {'schema_version': 1, 'plan_sha256': plan['plan_sha256'], 'phase': 'remote', 'next_operation': 0,
                          'remote_expected': copy.deepcopy(plan['remote_expected']), 'inflight': None,
                          'local_files': plan['local_files'], 'snapshot_sha256': plan['snapshot_sha256']}
        elif checkpoint.get('schema_version') != 1 or checkpoint.get('plan_sha256') != plan['plan_sha256']:
            raise ValueError('Checkpoint belongs to a different reviewed plan')
        else:
            _validate_checkpoint(plan, checkpoint)
        rows, milestones = transport.read()
        if checkpoint['phase'] == 'complete':
            check_local(root, checkpoint['local_files'], checkpoint['snapshot_sha256'])
            guard_remote(rows, checkpoint['remote_expected'])
            _validate_local_readback(checkpoint['local_transaction'], rows, milestones)
            return {'status': 'already-applied', 'operations': 0}
        if checkpoint.get('local_transaction'):
            guard_remote(rows, checkpoint['remote_expected'])
            if not execute:
                return {'status': 'dry-run-local-reconcile', 'operations': 0}
            _finish_local(root, rows, milestones, checkpoint, checkpoint_path)
            return {'status': 'applied', 'operations': 0}
        check_local(root, checkpoint['local_files'], checkpoint['snapshot_sha256'])
        inflight = checkpoint.get('inflight')
        if inflight is not None:
            operation = plan['operations'][inflight]
            try:
                guard_remote(rows, checkpoint['remote_expected'])
            except ValueError:
                guard_remote(rows, checkpoint['remote_expected'], transition=operation)
                checkpoint['remote_expected'][str(operation['number'])] = state(rows[str(operation['number'])])
                checkpoint['next_operation'] = inflight + 1
            checkpoint['inflight'] = None
        else:
            guard_remote(rows, checkpoint['remote_expected'])
        if not execute:
            return {'status': 'dry-run', 'operations': len(plan['operations']) - checkpoint['next_operation'],
                    'plan_sha256': plan['plan_sha256']}
        _save_checkpoint(checkpoint_path, checkpoint)
        for index in range(checkpoint['next_operation'], len(plan['operations'])):
            operation = plan['operations'][index]
            check_local(root, checkpoint['local_files'], checkpoint['snapshot_sha256'])
            rows, milestones = transport.read()
            guard_remote(rows, checkpoint['remote_expected'])
            checkpoint['inflight'] = index
            _save_checkpoint(checkpoint_path, checkpoint)
            if operation['kind'] == 'issue':
                transport.patch_issue(operation['number'], operation['changes'])
            else:
                transport.patch_project(operation['number'], operation['changes'])
            rows, milestones = transport.read()
            guard_remote(rows, checkpoint['remote_expected'], transition=operation)
            checkpoint['remote_expected'][str(operation['number'])] = state(rows[str(operation['number'])])
            checkpoint['next_operation'], checkpoint['inflight'] = index + 1, None
            _save_checkpoint(checkpoint_path, checkpoint)
        rows, milestones = transport.read()
        guard_remote(rows, checkpoint['remote_expected'])
        _finish_local(root, rows, milestones, checkpoint, checkpoint_path)
        return {'status': 'applied', 'operations': len(plan['operations'])}


def local_json_path(root, path):
    """Only local JSON artifacts; plans cannot direct writes to source/task paths."""
    candidate = Path(path)
    if not candidate.is_absolute():
        candidate = root / candidate
    candidate = candidate.resolve()
    allowed = (root / '.local').resolve()
    if not allowed.is_relative_to(root.resolve()) or not candidate.is_relative_to(allowed) or candidate.suffix.lower() != '.json':
        raise ValueError('Plan/checkpoint/output artifacts must be JSON files inside this checkout .local directory')
    return candidate


class GitHubTransport:
    """Fixed Engine REST/Project operations only; never creates issues or items."""
    def __init__(self):
        self._catalog = None
        self._commits = {}
        self._rows = None

    def read(self):
        rows, milestones = pull.fetch()
        if not 0 < len(rows) <= MAX_ISSUES:
            raise ValueError('Issue count exceeds reviewed synchronization bound')
        for number, row in rows.items():
            require_membership(row, number)
        self._rows = rows
        return rows, milestones

    def catalog(self):
        def paged(path):
            return [item for page in pull.gh('api', path, '--paginate', '--slurp') for item in page]
        actor = pull.gh('api', 'user')['login']
        if actor != 'Cephalon-Neza':
            raise ValueError('Tracking writer identity must be Cephalon-Neza')
        repository = pull.gh('api', 'repos/' + pull.REPO)
        if repository['full_name'] != pull.REPO or not repository['private']:
            raise ValueError('Unexpected Engine repository identity/privacy')
        fields, cursor = {}, None
        while True:
            after = ',after:' + json.dumps(cursor) if cursor else ''
            query = '{node(id:' + json.dumps(pull.PROJECT_ID) + '){... on ProjectV2{fields(first:100' + after + '){pageInfo{hasNextPage endCursor} nodes{... on ProjectV2Field{id name dataType} ... on ProjectV2SingleSelectField{id name dataType options{id name}}}}}}}'
            page = pull.gh('api', 'graphql', '--input', '-', body={'query': query})['data']['node']['fields']
            for field in page['nodes']:
                if field.get('name') in pull.PROJECT_FIELDS:
                    if field['name'] in fields:
                        raise ValueError('Duplicate named Project field requires review: ' + field['name'])
                    fields[field['name']] = {'id': field['id'], 'data_type': field['dataType'],
                                             'options': {x['name']: x['id'] for x in field.get('options', [])}}
            if not page['pageInfo']['hasNextPage']:
                break
            cursor = page['pageInfo']['endCursor']
        milestones = paged(f'repos/{pull.REPO}/milestones?state=all&per_page=100')
        self._catalog = {'actor': actor, 'types': sorted(x['name'] for x in paged('orgs/Cephalon-Labs/issue-types?per_page=100') if x['is_enabled']),
                         'labels': sorted(x['name'] for x in paged(f'repos/{pull.REPO}/labels?per_page=100')),
                         'assignees': sorted(x['login'] for x in paged(f'repos/{pull.REPO}/assignees?per_page=100')),
                         'milestones': {str(x['number']): {'title': x['title'], 'state': x['state']} for x in milestones}, 'fields': fields}
        return self._catalog

    def engine_commit(self, sha):
        if sha not in self._commits:
            try:
                self._commits[sha] = pull.gh('api', f'repos/{pull.REPO}/commits/{sha}')['sha'] == sha
            except RuntimeError:
                self._commits[sha] = False
        return self._commits[sha]

    def patch_issue(self, number, changes):
        payload = {('milestone' if key == 'milestone_number' else key): value for key, value in changes.items()}
        pull.gh('api', f'repos/{pull.REPO}/issues/{int(number)}', '--method', 'PATCH', '--input', '-', body=payload)

    def patch_project(self, number, changes):
        # Use the item ID from the immediately guarded read. Never switch to a
        # newly migrated item behind the approved plan's immutable identity.
        row = self._rows[str(number)]
        name, value = next(iter(changes.items()))
        field = self._catalog['fields'][name]
        common = 'projectId:' + json.dumps(pull.PROJECT_ID) + ',itemId:' + json.dumps(row['item_id']) + ',fieldId:' + json.dumps(field['id'])
        if value is None:
            mutation = 'clearProjectV2ItemFieldValue(input:{' + common + '})'
        else:
            kind = 'number' if name in NUMERIC_FIELDS else ('text' if name == 'Feature' else 'singleSelectOptionId')
            encoded = value if kind != 'singleSelectOptionId' else field['options'][value]
            mutation = 'updateProjectV2ItemFieldValue(input:{' + common + ',value:{' + kind + ':' + json.dumps(encoded) + '}})'
        pull.gh('api', 'graphql', '--input', '-', body={'query': 'mutation{' + mutation + '{projectV2Item{id}}}'})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    pulling = commands.add_parser('pull')
    pulling.add_argument('--check', action='store_true')
    planning = commands.add_parser('plan')
    planning.add_argument('--output', required=True)
    planning.add_argument('--migrations')
    applying = commands.add_parser('apply')
    applying.add_argument('--plan', required=True)
    applying.add_argument('--checkpoint')
    applying.add_argument('--approve')
    applying.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    root, transport = pull.ROOT, GitHubTransport()
    if args.command == 'pull':
        with pull.exclusive_pull(root) as token:
            snapshot_text = pull.read_tracking_text(pull.SNAPSHOT) if pull.SNAPSHOT.exists() else None
            previous = json.loads(snapshot_text)['issues'] if snapshot_text else pull.legacy_anchor(root)
            rows, milestones = transport.read()
            pull.reconcile(root, previous, rows, args.check, milestones, pull.digest(snapshot_text) if snapshot_text else None, token)
        print('Verified' if args.check else 'Pulled', len(rows), 'Engine mirrors; no remote writes.')
    elif args.command == 'plan':
        output = local_json_path(root, args.output)
        with pull.exclusive_pull(root):
            text = pull.read_tracking_text(pull.SNAPSHOT)
            snapshot = json.loads(text)
            migrations = json.loads(local_json_path(root, args.migrations).read_text(encoding='utf-8')) if args.migrations else None
            rows, _ = transport.read()
            plan = make_plan(root, snapshot, text, rows, transport.catalog(), transport.engine_commit, migrations)
            pull._atomic_json(output, plan)
        print(json.dumps({'plan': str(output), 'plan_sha256': plan['plan_sha256'], 'remote_operations': len(plan['operations']), 'merge_notes': plan['merge_notes']}, ensure_ascii=False, indent=2))
    else:
        plan = json.loads(local_json_path(root, args.plan).read_text(encoding='utf-8'))
        checkpoint = local_json_path(root, args.checkpoint) if args.checkpoint else None
        print(json.dumps(apply_plan(root, plan, transport, checkpoint, args.execute, args.approve), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
