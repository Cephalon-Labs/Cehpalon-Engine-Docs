from pathlib import Path
from datetime import datetime,timezone
import json,subprocess,hashlib
root=Path(__file__).resolve().parents[1]
out=root/'internal/evidence/small-api-collector/results'
api=lambda path:json.loads(subprocess.check_output(['gh','api',path],text=True,encoding='utf-8'))
report={'observed_at_utc':datetime.now(timezone.utc).isoformat(),'engine_revision':'6804271d429106864e01e4ec546a41dff771f84b','access':'Authenticated gh API; connector404 unavailable for these private repositories. Read-only refresh; no CI reruns or billing mutation.','runs':[]}
for run_id in (40622737320,40622737252):
    run=api(f'repos/Cephalon-Labs/Cehpalon-Engine/actions/runs/{run_id}')
    assert run['head_sha']==report['engine_revision']
    jobs=api(f'repos/Cephalon-Labs/Cehpalon-Engine/actions/runs/{run_id}/jobs')
    rows=[]
    for job in jobs['jobs']:
        annotations=api(f"repos/Cephalon-Labs/Cehpalon-Engine/check-runs/{job['id']}/annotations")
        assert len(job['steps'])==0 and job['conclusion']=='failure'
        assert any('payments' in a.get('message','') and 'spending limit' in a.get('message','') for a in annotations)
        rows.append({'id':job['id'],'name':job['name'],'conclusion':job['conclusion'],'steps':job['steps'],'annotations':annotations})
    report['runs'].append({'run_id':run_id,'head_sha':run['head_sha'],'jobs':rows})
report.update(classification='Blocked before execution; not a code failure or CI pass',job_count=sum(len(x['jobs']) for x in report['runs']),executed_steps=0)
(out/'hosted-ci-readback.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
repos=[]
for name in ('Cehpalon-Engine','Cehpalon-Engine-Samples','Cehpalon-Engine-Docs'):
    repo=api('repos/Cephalon-Labs/'+name)
    assert repo['private'] and repo['license']['spdx_id']=='MIT'
    repos.append({'name':name,'private':repo['private'],'license':repo['license']['spdx_id'],'default_branch':repo['default_branch']})
(out/'repository-readback.json').write_text(json.dumps({'observed_at_utc':datetime.now(timezone.utc).isoformat(),'repositories':repos},indent=2)+'\n',encoding='utf-8')
retained=Path('D:/Cephalon/Cehpalon-Engine-Samples/small-api-benchmark/evidence/2026-10-28-collector/execution-retention-manifest.json')
link={'compiled_samples_source':'a3bd8b5c5747440c81124774ac10b6451d88ff82','engine_revision':report['engine_revision'],'retained_samples_revision':'1aba2cf704d3137d1e11886fe87cc4c46b214c85','url':'https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/1aba2cf704d3137d1e11886fe87cc4c46b214c85/small-api-benchmark/evidence/2026-10-28-collector','manifest_sha256':hashlib.sha256(retained.read_bytes()).hexdigest(),'files':2640,'bytes':1335210272,'boundary':'Raw retained bytes in private Samples. Full source SHA here is technical provenance, never an Engine task/card commit-journal entry. No Docs self-hash loop.'}
(out/'raw-evidence-link.json').write_text(json.dumps(link,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'jobs_blocked_before_steps':report['job_count'],'steps':0,'private_mit_repositories':len(repos),'raw_revision':link['retained_samples_revision']}))
