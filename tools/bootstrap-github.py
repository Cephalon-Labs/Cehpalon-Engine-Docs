"""Bootstrap the explicitly authorized new program, preserving remote identifiers.

Run once against the newly created Project. Checkpoint after every issue creation.
This is a bootstrap tool, not a general bidirectional synchronizer. Review conflicts
before later synchronization; do not use this to overwrite independently edited work.
"""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWNER = 'Cephalon-Labs'
REPO = OWNER + '/Cehpalon-Engine'
PROJECT_NUMBER = 4
PROJECT_ID = 'PVT_kwDOEDryKs4Bo6sb'
STATE_PATH = ROOT / 'internal/evidence/bootstrap/github-state.json'
PLAN = json.loads((ROOT / 'internal/planning/backlog.json').read_text(encoding='utf-8'))
TASKS = PLAN['tasks']
STATE = json.loads(STATE_PATH.read_text(encoding='utf-8')) if STATE_PATH.exists() else {'project_number': PROJECT_NUMBER, 'project_id': PROJECT_ID, 'issues': {}}
if STATE.get('bootstrap_finalized'):
    raise SystemExit('Bootstrap is finalized. Fetch current state and use a conflict-aware synchronization workflow instead.')


def run(*args, payload=None):
    command = ['gh', *map(str, args)]
    result = subprocess.run(command, input=json.dumps(payload, ensure_ascii=False) if payload is not None else None,
                            text=True, encoding='utf-8', capture_output=True)
    if result.returncode:
        raise RuntimeError(f'{command[:4]} failed: {result.stderr.strip()} {result.stdout[:500]}')
    value = json.loads(result.stdout) if result.stdout.strip() else None
    if isinstance(value, dict) and value.get('errors'):
        raise RuntimeError(str(value['errors']))
    return value


def api(path, method='GET', body=None):
    args = ['api', path, '--method', method]
    if body is not None:
        args += ['--input', '-']
    return run(*args, payload=body)


def graphql(query):
    return api('graphql', 'POST', {'query': query})['data']


def checkpoint():
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(STATE, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


MILESTONES = {
    'W0': 'W0 - Baseline and Research', 'W1': 'W1 - Core and Composition',
    'W2': 'W2 - Transports and Small API', 'W3': 'W3 - State and Durable Business',
    'W4': 'W4 - AI and Operations', 'W5': 'W5 - Tooling and Distribution',
}
milestones = {m['title']: m for m in api(f'repos/{REPO}/milestones?state=all&per_page=100')}
for code, title in MILESTONES.items():
    if title not in milestones:
        milestones[title] = api(f'repos/{REPO}/milestones', 'POST', {
            'title': title, 'description': f'{code} workstream. Not a calendar week or delivery-date promise. See Docs program plan for scope and evidence gates.'})
STATE['milestones'] = {code: milestones[title] for code, title in MILESTONES.items()}
checkpoint()

existing_labels = {x['name'] for x in api(f'repos/{REPO}/labels?per_page=100')}
for area in sorted({t['area'] for t in TASKS}):
    name = 'area:' + area
    if name not in existing_labels:
        api(f'repos/{REPO}/labels', 'POST', {'name': name, 'color': '1D7667', 'description': f'Cehpalon {area} capability/workstream'})

field_list = run('project', 'field-list', PROJECT_NUMBER, '--owner', OWNER, '--format', 'json')['fields']
fields = {f['name']: f for f in field_list}
statuses = ['Backlog', 'Ready', 'In Progress', 'Review', 'Test', 'Benchmark', 'Blocked', 'Done']
if [x['name'] for x in fields['Status']['options']] != statuses:
    if run('project', 'item-list', PROJECT_NUMBER, '--owner', OWNER, '--format', 'json')['totalCount']:
        raise RuntimeError('Project already has items; review status migration instead of replacing options.')
    options = [{'name': x, 'color': 'GRAY', 'description': x + ' delivery phase'} for x in statuses]
    query = 'mutation{updateProjectV2Field(input:{fieldId:' + json.dumps(fields['Status']['id']) + ',singleSelectOptions:'
    query += '[' + ','.join('{name:' + json.dumps(x['name']) + ',color:GRAY,description:' + json.dumps(x['description']) + '}' for x in options) + ']}){projectV2Field{... on ProjectV2SingleSelectField{id name options{id name}}}}}'
    graphql(query)

specs = {
    'Priority': ('SINGLE_SELECT', ['P0', 'P1', 'P2', 'P3']),
    'Estimate (h)': ('NUMBER', None), 'Estimate low (h)': ('NUMBER', None),
    'Estimate high (h)': ('NUMBER', None), 'Actual (h)': ('NUMBER', None),
    'Remaining (h)': ('NUMBER', None), 'Maturity': ('SINGLE_SELECT', ['M0', 'M1', 'M2', 'M3', 'M4']),
    'Test gate': ('SINGLE_SELECT', ['Planned', 'Passed', 'Failed', 'Blocked', 'Not required']),
    'Benchmark gate': ('SINGLE_SELECT', ['Planned', 'Passed', 'Failed', 'Blocked', 'Not required']),
    'Feature': ('TEXT', None),
}
for name, (data_type, options) in specs.items():
    if name not in fields:
        args = ['project', 'field-create', PROJECT_NUMBER, '--owner', OWNER, '--name', name, '--data-type', data_type, '--format', 'json']
        if options:
            args += ['--single-select-options', ','.join(options)]
        run(*args)
fields = {x['name']: x for x in run('project', 'field-list', PROJECT_NUMBER, '--owner', OWNER, '--format', 'json')['fields']}
STATE['fields'] = fields
checkpoint()

for task in TASKS:
    if task['key'] not in STATE['issues']:
        dependency_text = ', '.join('#' + str(STATE['issues'][key]['number']) for key in task['dependencies']) or 'None'
        checks = '\n'.join('- [ ] ' + text for text in task['acceptance'])
        benchmark = 'Required; predeclare protocol before measurement. Not run.' if task['benchmark_required'] else 'Not required for this task: planning/documentation/tooling-readiness scope has no runtime performance claim.'
        body = f'''<!-- cehpalon-task: {task['key']} -->
## Outcome
{task['title']}

## Scope and acceptance criteria
{checks}

## Tracking
- Type: {task['type']} (native issue type)
- Labels: area:{task['area']}
- Priority: {task['priority']} (Project field)
- Milestone: {MILESTONES[task['milestone']]}
- Owner: Cephalon-Neza
- Dependencies: {dependency_text}
- Parent: None; acceptance checklist defines the initial work breakdown.
- Feature/function: {task['area']}
- Estimated person-hours: {task['estimate_low']}–{task['estimate_high']} (low confidence; planning midpoint {(task['estimate_low'] + task['estimate_high']) / 2:g})
- Estimate assumptions: first bounded capability slice, including relevant implementation, tests and docs; refine after architecture/provider choices. Not universal provider coverage or a delivery-date promise.
- Actual person-hours: null (not measured; do not infer from AI or CI duration)
- Remaining estimate: null (not yet refined)
- Maturity before / observed: M0; runtime/provider/version/host proof not established
- Maturity target: define per supported capability/profile before implementation

## Validation
- Test required: Yes; task-appropriate review/metadata/link checks for documents, contract/E2E/failure checks for runtime.
- Test result: Not run for this planned task.
- Benchmark: {benchmark}
- Evidence: add immutable Engine revision, locked dependencies, commands, results and proof limits when run.

## References
- [Program plan](https://github.com/{OWNER}/Cehpalon-Engine-Docs/blob/main/internal/planning/2026-10-27-program-plan.md)
- [Delivery and maturity](https://github.com/{OWNER}/Cehpalon-Engine-Docs/blob/main/internal/standards/delivery-and-maturity.md)
- [Task mirror](https://github.com/{OWNER}/Cehpalon-Engine-Docs/blob/main/tasks/{{ISSUE_NUMBER}}.md)

## Engine commit journal
No Engine commit linked yet. Record each related full Engine SHA here and in the task mirror; Docs/Samples SHAs are excluded.

## Change history
- 2026-10-27: Created from the user-authorized new baseline and all three selected sample lanes. Historical task IDs and test results were not imported.
'''
        issue = api(f'repos/{REPO}/issues', 'POST', {
            'title': task['title'], 'body': body, 'type': task['type'],
            'labels': ['area:' + task['area']], 'assignees': ['Cephalon-Neza'],
            'milestone': STATE['milestones'][task['milestone']]['number']})
        STATE['issues'][task['key']] = {'number': issue['number'], 'node_id': issue['node_id'], 'url': issue['html_url'], 'body': body}
        checkpoint()
        if not issue.get('type') or issue['type']['name'] != task['type']:
            raise RuntimeError('Native issue type was not persisted; issue checkpoint retained for repair.')
        body = body.replace('{ISSUE_NUMBER}', str(issue['number']))
        api(f"repos/{REPO}/issues/{issue['number']}", 'PATCH', {'body': body})
        STATE['issues'][task['key']]['body'] = body
        checkpoint()
        print(f"Created #{issue['number']}: {task['key']}", flush=True)

for task in TASKS:
    issue = STATE['issues'][task['key']]
    if 'item_id' not in issue:
        item = run('project', 'item-add', PROJECT_NUMBER, '--owner', OWNER, '--url', issue['url'], '--format', 'json')
        issue['item_id'] = item['id']
        checkpoint()
    if not issue.get('fields_initialized'):
        status = 'In Progress' if task['key'] == 'baseline' else 'Backlog'
        selections = {'Status': status, 'Priority': task['priority'], 'Maturity': 'M0', 'Test gate': 'Planned',
                      'Benchmark gate': 'Planned' if task['benchmark_required'] else 'Not required'}
        values = {}
        for name, selected in selections.items():
            option = next(x for x in fields[name]['options'] if x['name'] == selected)
            values[name] = '{singleSelectOptionId:' + json.dumps(option['id']) + '}'
        for name, number in [('Estimate (h)', (task['estimate_low'] + task['estimate_high']) / 2),
                             ('Estimate low (h)', task['estimate_low']), ('Estimate high (h)', task['estimate_high'])]:
            values[name] = '{number:' + str(number) + '}'
        values['Feature'] = '{text:' + json.dumps(task['area']) + '}'
        mutations = []
        for index, (name, value) in enumerate(values.items()):
            mutations.append('v' + str(index) + ':updateProjectV2ItemFieldValue(input:{projectId:' + json.dumps(PROJECT_ID)
                + ',itemId:' + json.dumps(issue['item_id']) + ',fieldId:' + json.dumps(fields[name]['id'])
                + ',value:' + value + '}){projectV2Item{id}}')
        graphql('mutation{' + ' '.join(mutations) + '}')
        issue['fields_initialized'] = True
        checkpoint()
        print(f"Project fields set for #{issue['number']}", flush=True)
    mirror = f"# #{issue['number']} — {task['title']}\n\nGitHub: {issue['url']}  \nProject: https://github.com/orgs/{OWNER}/projects/{PROJECT_NUMBER}  \nProject item ID: `{issue['item_id']}`  \nStatus at initial sync: {'In Progress' if task['key'] == 'baseline' else 'Backlog'}\n\n" + issue['body']
    (ROOT / 'tasks' / f"{issue['number']}.md").write_text(mirror, encoding='utf-8')

STATE['scope'] = 'Observed bootstrap state; refresh before later synchronization. Actual/Remaining hours unset intentionally.'
checkpoint()
print(f'Bootstrap prepared {len(TASKS)} issue mirrors. Readback validation still required.', flush=True)
