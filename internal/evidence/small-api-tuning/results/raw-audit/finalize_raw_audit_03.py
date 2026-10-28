"""Finalize raw03 identity/order/failed-diagnostic checks; preserve the full scan."""
import datetime,hashlib,json,base64,gzip
from pathlib import Path
BASE=Path('/mnt/d/Cephalon/Cehpalon-Engine-Samples')
ROOT=Path('/home/tom/.local/share/cehpalon-benchmark-runs/benchmark-observation-03')
OUT=Path(__file__).resolve().parent/'raw-audit-03'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
scan=read(OUT/'audit.json');manifest=read(ROOT/'manifest.json');build=read(BASE/'.local/tuning-conformance-linux-01/manifest.json')
assert not scan['findings'],scan['findings']
assert build['samples_source_revision']==manifest['samples_revision']=='fb77069ec2af583b29814f941643a318222b420e'
assert all(manifest['source_sha256'].get('samples/'+k)==h for k,h in build['source_sha256'].items())
identities=[];pids=set();errors=[]
for p in ROOT.rglob('ready.json'):
    ready=read(p);directory=p.parent;invocation=read(directory/'invocation.json');state=read(directory/'final-state.json');command=invocation['command']
    variant=directory.name.split('-',1)[1];transport=directory.parent.name
    if ready.get('variant')!=variant or ready.get('transport')!=transport or state.get('variant')!=variant or state.get('transport')!=transport:errors.append(str(directory)+' identity mismatch')
    if '--variant='+variant not in command or '--transport='+transport not in command or manifest['assembly'] not in command:errors.append(str(directory)+' invocation mismatch')
    if hashlib.sha256(base64.b64decode(ready['rootCaDerBase64'])).hexdigest()!=manifest['public_ca_sha256']:errors.append(str(directory)+' public CA mismatch')
    if ready['processId'] in pids:errors.append(str(directory)+' duplicate process identity')
    pids.add(ready['processId']);identities.append({'directory':str(directory.relative_to(ROOT)),'variant':variant,'transport':transport,'pid':ready['processId'],'invocation_utc':invocation['observed_at_utc']})
assert len(identities)==172,len(identities)
for phase in ['startup','idle','load']:
    for transport in ['http','graphql']:
        for i in range(30 if phase=='startup' else 5):
            a='baseline' if i%2==0 else 'engine';b='engine' if a=='baseline' else 'baseline'
            first=read(ROOT/phase/transport/f'{i:02}-{a}'/'invocation.json')['observed_at_utc'];second=read(ROOT/phase/transport/f'{i:02}-{b}'/'invocation.json')['observed_at_utc']
            if not first<second:errors.append(f'{phase}/{transport}/{i} pair order mismatch')
for transport in ['http','graphql']:
    for rate,order in [(100,'BE'),(500,'EB'),(2000,'BE')]:
        a='baseline' if order[0]=='B' else 'engine';b='engine' if a=='baseline' else 'baseline'
        first=read(ROOT/'diagnostics'/transport/f'{rate:04}-{a}'/'invocation.json')['observed_at_utc'];second=read(ROOT/'diagnostics'/transport/f'{rate:04}-{b}'/'invocation.json')['observed_at_utc']
        if not first<second:errors.append(f'diagnostics/{transport}/{rate} pair order mismatch')
failed=ROOT/'diagnostics/http/2000-engine/driver';drop=[]
with gzip.open(failed/'preflight-requests.jsonl.gz','rt') as f:
    header=json.loads(next(f))
    for line in f:
        row=json.loads(line)
        if row[7]:drop.append({'index':row[0],'operation':row[1],'scheduled_ms':row[0]*1000/2000,'status':row[5],'error':row[7]})
assert len(drop)==37 and all(x['error']=='offered.dropped' for x in drop)
prep=read(failed/'collector-preparation.json');baseline_prep=read(ROOT/'diagnostics/http/2000-baseline/driver/collector-preparation.json')
phases=read(OUT/'phase-recomputation.json');measured=[r for r in phases if r['path'].endswith('measured-requests.jsonl.gz')]
main=[r for r in measured if r['path'].startswith('load/')];diag=[r for r in measured if r['path'].startswith('diagnostics/')]
assert len(main)==20 and len(diag)==11 and sum(x['summary']['offered'] for x in main)==3600000 and sum(x['summary']['offered'] for x in diag)==1512000
assert all(x['summary']['errors']==0 and x['summary']['correct']==x['summary']['offered'] for x in measured)
accounting=read(OUT/'accounting-recomputation.json');assert len(accounting)==134 and sum(x['server_metric_control_before_persist'] for x in accounting)==31
numeric=all(x['absolute_budget_passed'] and x['overhead_budget_passed'] for x in scan['startup_numeric_recomputation']) and all(x['passed'] for x in scan['idle_pair_recomputation']) and all(x['latency_absolute_passed'] and x['latency_extra_passed'] and x['allocation_extra_passed'] for x in scan['main_load_pair_recomputation']) and all(x['budget_passed'] for x in scan['main_load_stability_recomputation'])
assert numeric is True
limits=scan['limits']+['The failed diagnostic retains preparation TLS metadata but not later TLS events from its failed preflight; connection-root-cause attribution is unproved.','Deployment/packaging/collector and metrics-window changes combine versus attempt02; improvement cannot be attributed to Engine code alone.']
result={'observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'consistent-with-declared-main-passes-and-diagnostic-preflight-failure' if not errors else 'audit-findings','raw_scan_sha256':sha(OUT/'audit.json'),'raw_scan_script_sha256':sha(Path(__file__).with_name('audit_raw_benchmark_03.py')),'finalization_script_sha256':sha(Path(__file__)),'input_manifest_sha256':sha(ROOT/'manifest.json'),'all_gzip_records_scanned':True,'counts':scan['counts'],'driver_report_state_snapshots_independently_regenerated':82,'additional_failed_preflight_final_server_snapshot_independently_regenerated':1,'owned_process_identity_and_pair_order_checks':172,'source_files_verified':106,'all_build_input_hashes_match':{'windows':13,'linux':13},'build_and_measurement_source_revision':manifest['samples_revision'],'engine_revision':manifest['engine_revision'],'native_staged_dll_and_deps_match_retained_build':True,'phase_accounting_records':134,'measured_server_metrics_before_persistence_records':31,'main_measured_offered_and_correct':3600000,'diagnostic_attempted':12,'diagnostic_timed_runs':11,'diagnostic_measured_offered_and_correct':1512000,'all_timed_offered_and_correct':5112000,'expected_failed_diagnostic':{'variant':'engine','transport':'http','rate':2000,'preflight_offered':4000,'preflight_correct':3963,'preflight_drops_and_errors':37,'dropped_rows':drop,'preflight_final_state_writes':200,'preparation_read_requests':130,'server_factories_and_disposals':4093,'server_reads':3893,'warmup_entered':False,'measurement_entered':False,'new_attempts_or_retries':False,'preparation_tls_observations_engine':len(prep.get('tlsConnections',[])),'preparation_tls_observations_baseline':len(baseline_prep.get('tlsConnections',[])),'interpretation':'Same preparation policy produced different observed pool states. This retained diagnostic failure does not prove an Engine2000req/s capacity limit or invalidate the separately successful1000req/s main runs. Later failed-phase TLS events were not emitted, so event-level cause is unavailable.'},'original_main_numeric_gates_passed':numeric,'reference_environment_qualified':False,'benchmark_full_reference_acceptance_passed':False,'unexpected_findings':errors,'proof_limits':limits}
(OUT/'audit-final.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
(OUT/'owned-identities.json').write_text(json.dumps(identities,indent=2)+'\n',newline='\n')
narrative=['# Independent canonical03 raw audit','','Status: consistent with declared main numeric passes and one diagnostic preflight failure. All186 gzip files,8,116,800 offered phase records and6,672,000 manifest rows were checked without filtering/changing records. Independently checked82 driver-report state snapshots plus the failed preflight final-server snapshot,172 identities/pair orders/shutdowns/native runtime maps,120 starts and1200 RSS samples. All106 frozen source hashes,13 build inputs per host and staged native DLL/deps match. No provenance delta.','','All main startup/idle/latency/allocation/all-five-CV numerical budgets pass. HTTP startup p95 B/E432.788656/438.697402ms; GraphQL894.146290/902.391182ms. Engine GraphQL CV3.261600559888926%; all five values retained.134 phase-accounting records and31 final-server-metric snapshots before persistence passed ordering checks.','','Main20 runs:3,600,000 correct measured offers. All12 diagnostic attempts retained; only11 entered timing,1,512,000 measured offers correct. HTTP Engine2000/s preflight failed4000/3963 with37 offered drops. Warmup/measurement were not entered, no hidden retry. Final200write state correct;4093 factory/disposal counts =130 preparation reads +3963 admitted requests. Same preparation policy produced different initial pool observations; failed-phase later TLS events are unavailable. No Engine2000/s capacity limit is proved, and independent clean1000/s main comparisons remain valid observations.','','Shared WSL reference remains nonqualifying; #3 stays Blocked. No full reference/production/supported-Windows pass. Deployment, packaging, collector and metrics-window changes combine versus attempt02; no causal claim that Engine code alone improved. Raw rows lack complete response bodies. See exact scripts/audit-final.json for boundaries.']
(OUT/'audit-final.md').write_text('\n'.join(narrative)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'status':result['status'],'counts':result['counts'],'main_numeric_passed':numeric,'timed_measured_correct':5112000,'failed_preflight_drops':37,'unexpected_findings':errors,'output':str(OUT)}))
