"""Read-only remote/bootstrap checks; writes only a local observed evidence report."""
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
STATE = json.loads((ROOT / 'internal/evidence/bootstrap/github-state.json').read_text(encoding='utf-8'))
PLAN = json.loads((ROOT / 'internal/planning/backlog.json').read_text(encoding='utf-8'))
CHECKS = []


def command(*args, payload=None):
    p = subprocess.run(args, input=json.dumps(payload) if payload is not None else None,
                       capture_output=True, encoding='utf-8', text=True)
    if p.returncode:
        raise RuntimeError(p.stderr)
    return p.stdout.strip()


def api(path):
    return json.loads(command('gh', 'api', path))


def check(condition, description):
    CHECKS.append({'check': description, 'passed': bool(condition)})


for name in ['Cehpalon-Engine', 'Cehpalon-Engine-Docs', 'Cehpalon-Engine-Samples']:
    repo = api('repos/Cephalon-Labs/' + name)
    check(repo['private'] and repo['default_branch'] == 'main', name + ': private/main')
    check((WORKSPACE / name / 'LICENSE').read_text(encoding='utf-8').startswith('MIT License'), name + ': local MIT license')
    identity = command('git', '-C', str(WORKSPACE / name), 'log', '-1', '--format=%an|%ae|%cn|%ce')
    expected = 'Cephalon-Neza|272007299+Cephalon-Neza@users.noreply.github.com'
    check(identity == expected + '|' + expected, name + ': author and committer identity')

for path in WORKSPACE.rglob('*.md'):
    if '.git' in path.parts:
        continue
    text = path.read_text(encoding='utf-8')
    check('\ufffd' not in text, str(path.relative_to(WORKSPACE)) + ': UTF-8 text')
    for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
        if target.startswith(('https:', 'http:', 'mailto:', '#')):
            continue
        target = target.split('#', 1)[0].strip('<>')
        check((path.parent / target).exists(), str(path.relative_to(WORKSPACE)) + ': link ' + target)

issues = api('repos/Cephalon-Labs/Cehpalon-Engine/issues?state=all&per_page=100')
issues = {issue['number']: issue for issue in issues if 'pull_request' not in issue}
check(len(issues) == len(PLAN['tasks']) == 23, 'Exactly 23 planned Engine issues, no duplicate bootstrap issues')
query = '''{organization(login:"Cephalon-Labs"){projectV2(number:4){id title public closed items(first:100){nodes{id content{... on Issue{number url}} fieldValues(first:50){nodes{... on ProjectV2ItemFieldSingleSelectValue{name field{... on ProjectV2SingleSelectField{name}}} ... on ProjectV2ItemFieldNumberValue{number field{... on ProjectV2Field{name}}} ... on ProjectV2ItemFieldTextValue{text field{... on ProjectV2Field{name}}}}}}}}}}'''
result = json.loads(command('gh', 'api', 'graphql', '--input', '-', payload={'query': query}))
if result.get('errors'):
    raise RuntimeError(str(result['errors']))
project = result['data']['organization']['projectV2']
check(project['id'] == STATE['project_id'] and not project['public'] and not project['closed'], 'Project 4 identity/private/open')
items = {node['content']['number']: node for node in project['items']['nodes'] if node.get('content')}
check(len(items) == 23, 'Project has exactly the 23 Engine issues')
finalized = STATE.get('bootstrap_finalized', False)
for task in PLAN['tasks']:
    entry = STATE['issues'][task['key']]
    issue = issues[entry['number']]
    prefix = '#' + str(issue['number']) + ': '
    check(issue['title'] == task['title'], prefix + 'title')
    check(issue.get('type', {}).get('name') == task['type'], prefix + 'native Issue Type')
    check('area:' + task['area'] in [label['name'] for label in issue['labels']], prefix + 'labels')
    check('Cephalon-Neza' in [person['login'] for person in issue['assignees']], prefix + 'owner')
    check(issue['milestone']['number'] == STATE['milestones'][task['milestone']]['number'], prefix + 'milestone')
    expected_state = 'closed' if finalized and task['key'] == 'baseline' else 'open'
    check(issue['state'] == expected_state, prefix + 'native issue state')
    mirror = ROOT / 'tasks' / f"{issue['number']}.md"
    check(mirror.exists() and issue['body'] in mirror.read_text(encoding='utf-8'), prefix + 'Markdown matches remote issue body')
    check('{ISSUE_NUMBER}' not in issue['body'], prefix + 'resolved mirror reference')
    item = items[issue['number']]
    check(item['id'] == entry['item_id'], prefix + 'stable Project item identity')
    values = {v['field']['name']: v.get('name', v.get('number', v.get('text'))) for v in item['fieldValues']['nodes'] if v.get('field')}
    expected_status = 'In Progress' if task['key'] == 'baseline' else 'Backlog'
    if finalized:
        if task['key'] == 'baseline':
            expected_status = 'Done'
        elif task['key'] in ['architecture', 'platform', 'research', 'sync']:
            expected_status = 'Ready'
    for field, value in {'Status': expected_status, 'Priority': task['priority'], 'Maturity': 'M0',
                         'Estimate low (h)': task['estimate_low'], 'Estimate high (h)': task['estimate_high'],
                         'Estimate (h)': (task['estimate_low'] + task['estimate_high']) / 2,
                         'Feature': task['area'], 'Test gate': 'Passed' if finalized and task['key'] == 'baseline' else 'Planned',
                         'Benchmark gate': 'Planned' if task['benchmark_required'] else 'Not required'}.items():
        check(values.get(field) == value, prefix + field)
    check(values.get('Actual (h)') is None and values.get('Remaining (h)') is None, prefix + 'unmeasured actual/remaining hours are unset')
    journal = issue['body'].split('## Engine commit journal', 1)[1].split('## Change history', 1)[0]
    check(not re.search(r'(Docs|Samples).*[0-9a-f]{40}', journal), prefix + 'no Docs/Samples SHA in commit journal')

baseline = issues[STATE['issues']['baseline']['number']]
engine_sha = command('git', '-C', str(WORKSPACE / 'Cehpalon-Engine'), 'rev-parse', 'HEAD')
comments = api('repos/Cephalon-Labs/Cehpalon-Engine/issues/1/comments?per_page=100')
check(any(engine_sha in c['body'] for c in comments), 'Initial full Engine SHA traced in issue #1 comment')
if finalized:
    check(engine_sha in baseline['body'], 'Initial full Engine SHA recorded in #1 body and mirror')

report = {'observed_at_utc': datetime.now(timezone.utc).isoformat(), 'scope': 'Bootstrap metadata/documents only; no runtime tests, benchmark, CI pass or production proof',
          'engine_revision': engine_sha, 'checks_passed': sum(x['passed'] for x in CHECKS), 'checks_total': len(CHECKS),
          'success': all(x['passed'] for x in CHECKS), 'checks': CHECKS}
target = ROOT / 'internal/evidence/bootstrap/validation.json'
target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f"Bootstrap checks: {report['checks_passed']}/{report['checks_total']}; runtime proof: none")
for failure in [x for x in CHECKS if not x['passed']]:
    print('FAIL:', failure['check'])
raise SystemExit(0 if report['success'] else 1)
