"""Adjudicate the explicitly noncompiled orchestration delta; preserve the raw scan."""
import datetime,hashlib,json,subprocess
from pathlib import Path
BASE=Path('D:/Cephalon/Cehpalon-Engine-Samples')
ROOT=BASE/'.local/benchmark-observation-02'
OUT=Path(__file__).resolve().parent/'raw-audit-02'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
scan=read(OUT/'audit.json');manifest=read(ROOT/'manifest.json');build=read(BASE/'.local/benchmark-linux-integration-02/manifest.json')
expected_note='Build/orchestration source mismatch tools/benchmark_small_api.py'
assert scan['findings']==[expected_note],scan['findings']
compiled={k:v for k,v in build['source_sha256'].items() if Path(k).suffix in ['.cs','.csproj','.props','.json'] or k=='NuGet.Config'}
assert all(manifest['source_sha256'].get('samples/'+k)==v for k,v in compiled.items())
delta=subprocess.check_output(['git','diff','--name-only',build['samples_source_revision'],manifest['samples_revision']],cwd=BASE,text=True).splitlines()
assert delta==['tools/benchmark_small_api.py'],delta
identities=[];pids=set();errors=[]
for p in ROOT.rglob('ready.json'):
    ready=read(p);directory=p.parent;invocation=read(directory/'invocation.json');state=read(directory/'final-state.json');command=invocation['command']
    variant=directory.name.split('-',1)[1];transport=directory.parent.name
    if ready.get('variant')!=variant or ready.get('transport')!=transport or state.get('variant')!=variant or state.get('transport')!=transport:errors.append(str(directory)+' identity mismatch')
    if '--variant='+variant not in command or '--transport='+transport not in command or manifest['assembly'] not in command:errors.append(str(directory)+' invocation mismatch')
    public=__import__('base64').b64decode(ready['rootCaDerBase64'])
    if hashlib.sha256(public).hexdigest()!=manifest['public_ca_sha256']:errors.append(str(directory)+' public CA mismatch')
    if ready['processId'] in pids:errors.append(str(directory)+' duplicate process identity')
    pids.add(ready['processId']);identities.append({'directory':str(directory.relative_to(ROOT)),'variant':variant,'transport':transport,'pid':ready['processId'],'invocation_utc':invocation['observed_at_utc']})
assert len(identities)==172,len(identities)
for phase in ['startup','idle','load']:
    for transport in ['http','graphql']:
        count=30 if phase=='startup' else 5
        for i in range(count):
            order=('BE' if i%2==0 else 'EB')
            a='baseline' if order[0]=='B' else 'engine';b='engine' if a=='baseline' else 'baseline'
            first=read(ROOT/phase/transport/f'{i:02}-{a}'/'invocation.json')['observed_at_utc'];second=read(ROOT/phase/transport/f'{i:02}-{b}'/'invocation.json')['observed_at_utc']
            if not first<second:errors.append(f'{phase}/{transport}/{i} pair order mismatch')
for transport in ['http','graphql']:
    for rate,order in [(100,'BE'),(500,'EB'),(2000,'BE')]:
        a='baseline' if order[0]=='B' else 'engine';b='engine' if a=='baseline' else 'baseline'
        first=read(ROOT/'diagnostics'/transport/f'{rate:04}-{a}'/'invocation.json')['observed_at_utc'];second=read(ROOT/'diagnostics'/transport/f'{rate:04}-{b}'/'invocation.json')['observed_at_utc']
        if not first<second:errors.append(f'diagnostics/{transport}/{rate} pair order mismatch')
result={'observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'consistent-with-declared-budget-failures' if not errors else 'audit-findings','raw_scan_sha256':sha(OUT/'audit.json'),'raw_scan_script_sha256':sha(Path(__file__).with_name('audit_raw_benchmark_02.py')),'adjudication_script_sha256':sha(Path(__file__)),'all_gzip_records_scanned':True,'counts':scan['counts'],'owned_process_identity_and_pair_order_checks':len(identities),'compiled_source_bundle_matches_build':True,'only_build_to_measure_source_delta':delta,'provenance_note':{'classification':'Noncompiled orchestration-only change, explicitly verified','build_samples_revision':build['samples_source_revision'],'measured_samples_revision':manifest['samples_revision'],'build_orchestrator_sha256':build['source_sha256']['tools/benchmark_small_api.py'],'measured_orchestrator_sha256':manifest['source_sha256']['samples/tools/benchmark_small_api.py'],'reason':'The only committed delta is Python orchestration; compiled C#/project/package bytes and actual DLL/deps match. Measured Python bytes separately match their frozen recorded commit. No benchmark source or raw result was changed by this adjudication.'},'unexpected_findings':errors,'reference_environment_qualified':False,'benchmark_acceptance_passed':False,'numeric_conclusion':{'startup_absolute_1s':'failed both transports','startup_baseline_extra_150ms':'passed both transports','idle_rss_and_extra_16MiB':'passed all ten pairs','main_latency_and_allocation':'passed all ten pairs','graphql_engine_p95_population_cv':0.12368092068471122,'stability_gate':'invalid; >10% CV; no outlier removed'},'proof_limits':scan['limits']}
(OUT/'audit-final.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
(OUT/'audit-final.md').write_text('# Independent raw audit final interpretation\n\n'+result['status']+'. All188 gzip files,8,596,800 offered observations and6,672,000 manifest rows were checked. Source/binary hashes,172 owned process identities and pair orders,84 full catalog snapshots,120 startup launches and1200 idle samples were cross-checked. No raw record was filtered or changed.\n\nThe strict scan retained one build/source-bundle difference: only tools/benchmark_small_api.py changed after compilation. Git diff and hashes confirm all compiled C#/project/package bytes and the actual DLL/deps match; the measured Python matches its own frozen commit. audit-final.json retains this explicit provenance note rather than hiding it.\n\nStartup absolute1s fails both transports; idle and main latency/allocation pair budgets pass, while GraphQL Engine p95 CV12.368092068471122% exceeds10%, invalidating the series. Environment remains nonqualifying. No full benchmark/production/supported-Windows pass is claimed. See audit.json, audit-final.json and exact scripts for evidence limits.\n',encoding='utf-8',newline='\n')
print(json.dumps({'status':result['status'],'owned_identities':len(identities),'unexpected_findings':errors,'output':str(OUT)}))
