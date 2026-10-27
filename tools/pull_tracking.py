"""Pull live Engine/Project tracking into Docs, refusing unreviewed local edits.

No remote mutations or issue creation. An existing issue/item identity change is
an explicit migration conflict. Initial anchors come from the frozen bootstrap.

Cooperating runs use an exclusive lock. Writes are staged, backed up and replaced
atomically per file, with the snapshot committed last. A failed/interrupted batch
leaves a recovery journal and blocks another pull until explicitly reviewed.
This is not a multi-file filesystem transaction: an external editor does not
honor our lock, and can still edit between the final hash check and replacement.
Keep editors idle during a reviewed pull; retained copies support recovery but
cannot promise capture of an arbitrary external edit made in that final window.
"""
import argparse
import hashlib
import json
import os
import subprocess
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = 'Cephalon-Labs/Cehpalon-Engine'
PROJECT_ID = 'PVT_kwDOEDryKs4Bo6sb'
SNAPSHOT = ROOT / 'internal/evidence/tracking/github-observed.json'
SNAPSHOT_RELATIVE = Path('internal/evidence/tracking/github-observed.json')
LOCK_RELATIVE = Path('.local/tracking-pull.lock')
JOURNAL_RELATIVE = Path('.local/tracking-pull-journal.json')
_UNSET = object()


def digest(value):
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'))


def require_unchanged_local(current, expected, path):
    if digest(current) != expected:
        raise ValueError(f'Local tracking edit conflicts with the last sync: {path}; preserve and reconcile it before pulling.')


def require_identity(old, new, number):
    for name in ('node_id', 'item_id'):
        if old.get(name) != new.get(name):
            raise ValueError(f'Issue #{number} {name} changed; review the migration mapping explicitly. No duplicate issue will be created.')


@contextmanager
def exclusive_pull(root):
    """Serialize cooperating runs; stale locks require explicit owner review."""
    path = root / LOCK_RELATIVE
    path.parent.mkdir(parents=True, exist_ok=True)
    token = uuid.uuid4().hex
    try:
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as error:
        raise ValueError(f'Another tracking pull or an unreviewed stale lock exists: {path}') from error
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8', newline='\n') as stream:
            json.dump({'token': token, 'pid': os.getpid(),
                       'started_at_utc': datetime.now(timezone.utc).isoformat()}, stream)
            stream.flush()
            os.fsync(stream.fileno())
        if (root / JOURNAL_RELATIVE).exists():
            raise ValueError(f'Unresolved tracking recovery journal: {root / JOURNAL_RELATIVE}; review retained copies and current files before another pull.')
        yield token
    finally:
        # Never remove a lock whose ownership was replaced or cannot be read.
        try:
            if json.loads(path.read_text(encoding='utf-8')).get('token') == token:
                path.unlink()
        except (OSError, ValueError):
            pass


def _require_lock(root, token):
    path = root / LOCK_RELATIVE
    try:
        owned = json.loads(path.read_text(encoding='utf-8')).get('token') == token
    except (OSError, ValueError):
        owned = False
    if not owned:
        raise ValueError('Tracking pull does not own the cooperating-run lock')


def _text_from_bytes(value):
    # Match Path.read_text's universal-newline interpretation used by anchors.
    return value.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')


def _read_existing(path):
    try:
        return path.read_bytes()
    except FileNotFoundError:
        return None


def _require_expected(path, expected, current):
    observed = digest(_text_from_bytes(current)) if current is not None else None
    if observed != expected:
        raise ValueError(f'Local tracking edit after preflight: {path}; no replacement of this file was performed.')


def _write_durable(path, content):
    with path.open('xb') as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())


def _atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    _write_durable(temporary, (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
    os.replace(temporary, path)


def _persist_journal(root, directory, journal):
    # A crash between the two copies is recoverable by inspecting entry hashes.
    _atomic_json(directory / 'journal.json', journal)
    _atomic_json(root / JOURNAL_RELATIVE, journal)


def _prepare_transaction(root, planned, expected):
    directory = root / '.local/tracking-transactions' / uuid.uuid4().hex
    directory.mkdir(parents=True)
    entries = []
    for index, (path, content) in enumerate(planned.items()):
        current = _read_existing(path)
        _require_expected(path, expected[path], current)
        prefix = f'{index:04d}'
        before = prefix + '.before'
        after = prefix + '.new'
        staged = prefix + '.staged'
        if current is not None:
            _write_durable(directory / before, current)
        encoded = content.encode('utf-8')
        # Keep the new copy too: os.replace consumes the separate staged copy.
        _write_durable(directory / after, encoded)
        _write_durable(directory / staged, encoded)
        entries.append({'target': path.relative_to(root).as_posix(),
                        'expected_text_sha256': expected[path], 'existed': current is not None,
                        'before': before if current is not None else None,
                        'before_bytes_sha256': hashlib.sha256(current).hexdigest() if current is not None else None,
                        'new': after, 'new_bytes_sha256': hashlib.sha256(encoded).hexdigest(),
                        'staged': staged, 'state': 'staged'})
    journal = {'schema_version': 1, 'status': 'prepared',
               'created_at_utc': datetime.now(timezone.utc).isoformat(),
               'directory': directory.relative_to(root).as_posix(), 'entries': entries,
               'recovery': 'Compare current target hashes with retained before/new copies. Reconcile intentionally; never overwrite an unexpected file. Retain the reviewed journal before removing the active recovery marker. A stale run lock also requires owner review.'}
    return directory, journal


def _commit_transaction(root, planned, expected):
    directory, journal = _prepare_transaction(root, planned, expected)
    # No target has changed before this active journal is durably staged.
    _persist_journal(root, directory, journal)
    try:
        for entry in journal['entries']:
            target = root / entry['target']
            target.parent.mkdir(parents=True, exist_ok=True)
            # Last optimistic check immediately before atomic replacement.
            # An external non-cooperating editor can still race this boundary.
            _require_expected(target, entry['expected_text_sha256'], _read_existing(target))
            os.replace(directory / entry['staged'], target)
            entry['state'] = 'replaced'
            _persist_journal(root, directory, journal)
        journal['status'] = 'completed'
        _persist_journal(root, directory, journal)
        (root / JOURNAL_RELATIVE).unlink()
    except BaseException as error:
        journal['status'] = 'needs-review'
        journal['failure'] = type(error).__name__ + ': ' + str(error)
        try:
            _persist_journal(root, directory, journal)
        except OSError:
            # The already-written active journal and retained copies remain the
            # recovery source even if the error prevents an updated journal.
            pass
        raise


def gh(*args, body=None):
    result = subprocess.run(['gh', *map(str, args)], text=True, encoding='utf-8', capture_output=True,
                            input=canonical(body) if body is not None else None)
    if result.returncode:
        raise RuntimeError(result.stderr.strip())
    value = json.loads(result.stdout)
    if isinstance(value, dict) and value.get('errors'):
        raise RuntimeError(str(value['errors']))
    return value


def reconcile_milestone_counts(rest_milestones, graphql_milestones, rows):
    """Retain REST counters, but use independently agreeing issue/GraphQL counts."""
    indexed = {item['number']: item for item in graphql_milestones}
    result = []
    for milestone in rest_milestones:
        graph = indexed.get(milestone['number'])
        if graph is None:
            raise ValueError('Milestone identity missing from GraphQL; review before syncing')
        members = [row for row in rows.values() if row['milestone_number'] == milestone['number']]
        observed = {state: sum(row['state'] == state for row in members) for state in ['open', 'closed']}
        if observed != {state: graph[state]['totalCount'] for state in ['open', 'closed']}:
            raise ValueError('Concurrent issue/milestone observations disagree; retry from fresh state instead of asserting synchronization')
        result.append({**milestone, 'rest_reported_open_issues': milestone['open_issues'],
                       'rest_reported_closed_issues': milestone['closed_issues'],
                       'open_issues': observed['open'], 'closed_issues': observed['closed'],
                       'count_source': 'GraphQL milestone issue connections verified against fetched native issue states',
                       'rest_counter_consistent': (milestone['open_issues'], milestone['closed_issues']) == (observed['open'], observed['closed'])})
    return result


def fetch():
    pages = gh('api', f'repos/{REPO}/issues?state=all&per_page=100', '--paginate', '--slurp')
    issues = [x for page in pages for x in page if 'pull_request' not in x]
    milestone_pages = gh('api', f'repos/{REPO}/milestones?state=all&per_page=100', '--paginate', '--slurp')
    milestones = [{k: x[k] for k in ('number', 'title', 'state', 'description', 'due_on', 'open_issues', 'closed_issues')}
                  for page in milestone_pages for x in page]
    items, cursor = [], None
    while True:
        after = ',after:' + json.dumps(cursor) if cursor else ''
        query = '''{organization(login:"Cephalon-Labs"){projectV2(number:4){id title public closed items(first:100AFTER){pageInfo{hasNextPage endCursor} nodes{id content{... on Issue{number id repository{nameWithOwner}}} fieldValues(first:50){nodes{... on ProjectV2ItemFieldSingleSelectValue{name field{... on ProjectV2SingleSelectField{name}}} ... on ProjectV2ItemFieldNumberValue{number field{... on ProjectV2Field{name}}} ... on ProjectV2ItemFieldTextValue{text field{... on ProjectV2Field{name}}}}}}}}}}'''.replace('AFTER', after)
        project = gh('api', 'graphql', '--input', '-', body={'query': query})['data']['organization']['projectV2']
        if project['id'] != PROJECT_ID or project['public'] or project['closed']:
            raise ValueError('Unexpected Project identity, privacy or lifecycle; review before syncing.')
        items.extend(project['items']['nodes'])
        page = project['items']['pageInfo']
        if not page['hasNextPage']:
            break
        cursor = page['endCursor']
    indexed = {}
    for item in items:
        content = item.get('content')
        if not content or content.get('repository', {}).get('nameWithOwner') != REPO:
            raise ValueError('Project contains a draft or non-Engine item; review its tracking scope explicitly.')
        number = content['number']
        if number in indexed:
            raise ValueError(f'Duplicate Project item for issue #{number}')
        indexed[number] = item
    rows = {}
    for issue in issues:
        number = issue['number']
        if number not in indexed:
            raise ValueError(f'Engine issue #{number} is absent from Project; link it explicitly before syncing.')
        item = indexed[number]
        fields = {v['field']['name']: v.get('name', v.get('number', v.get('text')))
                  for v in item['fieldValues']['nodes'] if v.get('field')}
        if not issue.get('type') or not issue['labels'] or not issue.get('milestone') or fields.get('Priority') not in ['P0', 'P1', 'P2', 'P3']:
            raise ValueError(f'Issue #{number} lacks native Type, Labels, Milestone or Priority')
        rows[str(number)] = {'number': number, 'node_id': issue['node_id'], 'item_id': item['id'],
                            'title': issue['title'], 'url': issue['html_url'], 'body': issue['body'],
                            'state': issue['state'], 'updated_at': issue['updated_at'], 'type': issue['type']['name'],
                            'labels': sorted(x['name'] for x in issue['labels']), 'assignees': sorted(x['login'] for x in issue['assignees']),
                            'milestone': issue['milestone']['title'], 'milestone_number': issue['milestone']['number'], 'fields': fields}
    if len(rows) != len(indexed):
        raise ValueError('Project/Engine issue sets differ')
    query = '{repository(owner:"Cephalon-Labs",name:"Cehpalon-Engine"){milestones(first:100,states:[OPEN,CLOSED]){pageInfo{hasNextPage} nodes{number open:issues(states:OPEN){totalCount} closed:issues(states:CLOSED){totalCount}}}}}'
    graph = gh('api', 'graphql', '--input', '-', body={'query': query})['data']['repository']['milestones']
    if graph['pageInfo']['hasNextPage']:
        raise ValueError('More than 100 milestones; add reviewed pagination support before syncing')
    return rows, reconcile_milestone_counts(milestones, graph['nodes'], rows)


def render(row):
    fields = row['fields']
    metadata = {'GitHub': row['url'], 'Project': 'https://github.com/orgs/Cephalon-Labs/projects/4',
                'Project item ID': row['item_id'], 'Status': fields.get('Status'), 'Native issue state': row['state'],
                'Type': row['type'], 'Labels': ', '.join(row['labels']), 'Priority': fields.get('Priority'),
                'Milestone': row['milestone'], 'Owner': ', '.join(row['assignees']),
                'Estimated hours (low/mid/high)': f"{fields.get('Estimate low (h)')} / {fields.get('Estimate (h)')} / {fields.get('Estimate high (h)')}",
                'Actual hours': fields.get('Actual (h)'), 'Remaining estimate': fields.get('Remaining (h)'),
                'Maturity': fields.get('Maturity'), 'Test gate': fields.get('Test gate'), 'Benchmark gate': fields.get('Benchmark gate')}
    header = '\n'.join('- ' + key + ': ' + ('null' if value is None else str(value)) for key, value in metadata.items())
    return f"# #{row['number']} — {row['title']}\n\n{header}\n\n" + row['body'].rstrip() + '\n'


def legacy_anchor(root):
    state = json.loads((root / 'internal/evidence/bootstrap/github-state.json').read_text(encoding='utf-8'))
    plan = json.loads((root / 'internal/planning/backlog.json').read_text(encoding='utf-8'))
    result = {}
    for task in plan['tasks']:
        entry = state['issues'][task['key']]
        number = entry['number']
        text = f"# #{number} — {task['title']}\n\n- GitHub: {entry['url']}\n- Project: https://github.com/orgs/Cephalon-Labs/projects/4\n- Project item ID: `{entry['item_id']}`\n- Status at observed sync: {entry['status']}\n\n" + entry['body']
        result[str(number)] = {'node_id': entry['node_id'], 'item_id': entry['item_id'], 'mirror_sha256': digest(text)}
    return result


def reconcile(root, previous, rows, check_only=False, milestones=None,
              snapshot_expected=_UNSET, _lock_token=None):
    if _lock_token is None:
        with exclusive_pull(root) as token:
            return reconcile(root, previous, rows, check_only, milestones, snapshot_expected, token)
    _require_lock(root, _lock_token)
    if (root / JOURNAL_RELATIVE).exists():
        raise ValueError('Unresolved tracking recovery journal; review before another pull')
    snapshot_path = root / SNAPSHOT_RELATIVE
    if snapshot_expected is _UNSET:
        original_snapshot = _read_existing(snapshot_path)
        snapshot_expected = digest(_text_from_bytes(original_snapshot)) if original_snapshot is not None else None
    if set(previous) - set(rows):
        raise ValueError('Tracked issues disappeared; review deletion/migration explicitly. No files were deleted.')
    planned, expected = {}, {}
    for number, row in rows.items():
        path = root / 'tasks' / f'{number}.md'
        if number in previous:
            require_identity(previous[number], row, number)
            if not path.exists():
                raise ValueError(f'Tracked local mirror missing: {path}')
            require_unchanged_local(path.read_text(encoding='utf-8'), previous[number]['mirror_sha256'], path)
            expected[path] = previous[number]['mirror_sha256']
        elif path.exists():
            raise ValueError(f'Unanchored existing task mirror: {path}')
        else:
            expected[path] = None
        content = render(row)
        if check_only and (not path.exists() or path.read_text(encoding='utf-8') != content):
            raise ValueError(f'Live GitHub differs from Docs mirror: #{number}; run reviewed pull')
        planned[path] = content
    reconciled = {number: {**row, 'mirror_sha256': digest(render(row)), 'remote_sha256': digest(canonical(row))} for number, row in rows.items()}
    if not check_only:
        # Insertion order commits the snapshot after all mirrors. A partial
        # batch is never silently adopted as a new baseline on the next run.
        planned[snapshot_path] = json.dumps({'schema_version': 1,
            'observed_at_utc': datetime.now(timezone.utc).isoformat(), 'project_id': PROJECT_ID,
            'scope': 'Live tracking metadata only; no runtime proof',
            'milestones': milestones or [], 'issues': reconciled}, ensure_ascii=False, indent=2) + '\n'
        expected[snapshot_path] = snapshot_expected
        _commit_transaction(root, planned, expected)
    return reconciled


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Read live state and fail on drift without updating mirrors or snapshot')
    args = parser.parse_args()
    with exclusive_pull(ROOT) as token:
        original_snapshot = SNAPSHOT.read_text(encoding='utf-8') if SNAPSHOT.exists() else None
        previous = json.loads(original_snapshot)['issues'] if original_snapshot is not None else legacy_anchor(ROOT)
        rows, milestones = fetch()
        reconcile(ROOT, previous, rows, args.check, milestones,
                  digest(original_snapshot) if original_snapshot is not None else None, token)
    print(f"{'Verified' if args.check else 'Pulled'} {len(rows)} live issues and {len(milestones)} milestones; no remote mutations.")


if __name__ == '__main__':
    main()
