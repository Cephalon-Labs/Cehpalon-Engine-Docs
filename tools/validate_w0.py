"""Validate W0 documents, provenance and observed tracking; no remote writes."""
import argparse
import hashlib
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from pull_tracking import canonical, digest, fetch, render

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
CHECKS = []


def check(value, message):
    CHECKS.append({'check': message, 'passed': bool(value)})


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--final', action='store_true', help='Also require W0 document tasks completed in live tracking')
    args = parser.parse_args()
    candidates = read_json(ROOT / 'internal/validation/provider-candidates.json')
    check(candidates['runtime_maturity'] == 'M0' and not candidates['common']['provider_runtime_qualified'], 'Candidate inventory claims no runtime qualification')
    check(len(candidates['profiles']) == 3, 'All three selected sample lanes present')
    for profile in candidates['profiles']:
        base = ROOT / 'internal/validation'
        check((base / profile['adr']).is_file() and (base / profile['protocol']).is_file(), profile['id'] + ': ADR/protocol pair')
    for path in (ROOT / 'internal/adr').glob('ADR-*.md'):
        content = path.read_text(encoding='utf-8')
        check('Accepted for W0 planning' in content and 'M0' in content, path.name + ': W0 decision and proof boundary')

    sdk = read_json(ROOT / 'internal/evidence/w0/dotnet-11-candidate.json')
    source = ROOT / 'internal/evidence/w0/dotnet-11-releases-source.json'
    check(hashlib.sha256(source.read_bytes()).hexdigest() == sdk['source_sha256'], 'Preserved .NET metadata source hash')
    release = next(x for x in read_json(source)['releases'] if x['sdk']['version'] == sdk['sdk'])
    check(release['runtime']['version'] == candidates['platform']['runtime'] and sdk['sdk'] == candidates['platform']['sdk'], 'SDK/runtime candidate matches preserved official metadata')
    check(all(re.fullmatch('[a-fA-F0-9]{128}', item['hash']) for item in sdk['candidate_files']), 'SDK published expected SHA512 values are well formed; binaries unverified')

    models = read_json(ROOT / 'internal/evidence/w0/model-candidates.json')
    for artifact, filename in zip(models['artifacts'], ['qwen-generation-source.json', 'qwen-embedding-source.json']):
        model_source = ROOT / 'internal/evidence/w0' / filename
        metadata = read_json(model_source)
        declared = next(x for x in metadata['siblings'] if x['rfilename'] == artifact['file'])
        check(hashlib.sha256(model_source.read_bytes()).hexdigest() == artifact['source_sha256'], artifact['file'] + ': metadata source hash')
        check(metadata['sha'] == artifact['revision'] and declared['lfs']['sha256'] == artifact['expected_file_sha256'] and declared['lfs']['size'] == artifact['expected_file_bytes'], artifact['file'] + ': pinned publisher metadata identity')
        check(artifact['binary_bytes_verified'] is False, artifact['file'] + ': no binary verification claim')

    tool_tests = read_json(ROOT / 'internal/evidence/w0/tracking-tool-tests.json')
    check(tool_tests['result'] == 'Passed' and tool_tests['tests_run'] >= 15 and tool_tests['failures'] == 0 and tool_tests['errors'] == 0, f"Recorded offline tracking suite: {tool_tests['tests_run']} passed, no runtime claim")
    for filename, expected in tool_tests['source_sha256'].items():
        check(hashlib.sha256((ROOT / filename).read_bytes()).hexdigest() == expected, filename + ': tested tool source hash unchanged')

    for repo_name in ['Cehpalon-Engine', 'Cehpalon-Engine-Docs', 'Cehpalon-Engine-Samples']:
        root = WORKSPACE / repo_name
        for path in root.rglob('*.md'):
            if any(part in {'.git', '.local'} for part in path.parts):
                continue
            content = path.read_text(encoding='utf-8')
            check('\ufffd' not in content, str(path.relative_to(WORKSPACE)) + ': UTF-8')
            for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', content):
                if target.startswith(('https:', 'http:', 'mailto:', '#')):
                    continue
                target = target.split('#', 1)[0].strip('<>')
                check((path.parent / target).exists(), str(path.relative_to(WORKSPACE)) + ': local link ' + target)
        for name, expected in [('user.name', 'Cephalon-Neza'), ('user.email', '272007299+Cephalon-Neza@users.noreply.github.com')]:
            observed = subprocess.check_output(['git', '-C', str(root), 'config', '--local', name], text=True).strip()
            check(observed == expected, repo_name + ': local Git ' + name)

    rows, milestones = fetch()
    snapshot = read_json(ROOT / 'internal/evidence/tracking/github-observed.json')
    check(len(rows) == 23 and len(milestones) == 6, 'Stable issue/milestone population; no duplicate bootstrap creation')
    check(snapshot['milestones'] == milestones, 'Live milestone metadata matches observed snapshot')
    sha_cache = {}
    for number, row in rows.items():
        previous = snapshot['issues'].get(number, {})
        mirror = ROOT / 'tasks' / f'{number}.md'
        prefix = '#' + number + ': '
        check(mirror.read_text(encoding='utf-8') == render(row), prefix + 'live issue/Project metadata equals task mirror')
        check(previous.get('remote_sha256') == digest(canonical(row)), prefix + 'observed remote fingerprint current')
        check(row['fields'].get('Maturity') == 'M0', prefix + 'runtime maturity remains M0')
        check(row['fields'].get('Actual (h)') is None, prefix + 'unknown actual person-hours unset')
        journal = row['body'].split('## Engine commit journal', 1)[1].split('## Change history', 1)[0]
        for sha in set(re.findall(r'\b[a-f0-9]{40}\b', journal)):
            if sha not in sha_cache:
                result = subprocess.run(['gh', 'api', 'repos/Cephalon-Labs/Cehpalon-Engine/commits/' + sha, '--jq', '.sha'], capture_output=True, text=True)
                sha_cache[sha] = result.returncode == 0 and result.stdout.strip() == sha
            check(sha_cache[sha], prefix + 'journal SHA belongs to Engine')
        if args.final and number in ['2', '4', '21']:
            check(row['state'] == 'closed' and row['fields'].get('Status') == 'Done' and row['fields'].get('Test gate') == 'Passed', prefix + 'W0 document scope completed after validation')
        if args.final and number in ['3', '23']:
            check(row['state'] == 'open' and row['fields'].get('Status') != 'Done', prefix + 'remaining qualification/full sync scope stays open')

    engine_sha = subprocess.check_output(['git', '-C', str(WORKSPACE / 'Cehpalon-Engine'), 'rev-parse', 'HEAD'], text=True).strip()
    result = {'observed_at_utc': datetime.now(timezone.utc).isoformat(), 'engine_revision': engine_sha,
              'scope': 'W0 document/provenance/tracking verification only; no SDK binary or model byte verification, runtime test, benchmark, hosted CI or production proof',
              'success': all(x['passed'] for x in CHECKS), 'checks_passed': sum(x['passed'] for x in CHECKS), 'checks_total': len(CHECKS), 'checks': CHECKS}
    (ROOT / 'internal/evidence/w0/validation.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    print(f"W0 document/provenance/tracking checks: {result['checks_passed']}/{result['checks_total']}; runtime proof: none")
    for failure in [x for x in CHECKS if not x['passed']]:
        print('FAIL:', failure['check'])
    raise SystemExit(0 if result['success'] else 1)


if __name__ == '__main__':
    main()
