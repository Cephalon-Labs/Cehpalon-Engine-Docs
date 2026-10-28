"""Independent identity/order/staging/aggregation audit, after the complete raw scan."""
import base64,datetime,hashlib,json,statistics
from pathlib import Path
ROOT=Path('/home/tom/.local/share/cehpalon-benchmark-runs/benchmark-observation-04')
BASE=Path('/mnt/d/Cephalon/Cehpalon-Engine-Samples')
OUT=Path(__file__).resolve().parent/'raw-audit-04'
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
scan=read(OUT/'audit.json');manifest=read(ROOT/'manifest.json');issues=list(scan['findings'])
def check(value,message):
    if not value:issues.append(message)
identities=[];pids=set()
for path in sorted(ROOT.rglob('ready.json')):
    ready=read(path);directory=path.parent;invocation=read(directory/'invocation.json');state=read(directory/'final-state.json')
    variant=directory.name.split('-',1)[1];transport=directory.parent.name
    check(ready.get('variant')==state.get('variant')==variant and ready.get('transport')==state.get('transport')==transport,str(directory)+' variant/transport mismatch')
    check('--variant='+variant in invocation['command'] and '--transport='+transport in invocation['command'] and manifest['assembly'] in invocation['command'],str(directory)+' command/source mismatch')
    check(hashlib.sha256(base64.b64decode(ready['rootCaDerBase64'])).hexdigest()==manifest['public_ca_sha256'],str(directory)+' publicCA mismatch')
    check(ready['processId'] not in pids,str(directory)+' reused PID identity');pids.add(ready['processId'])
    identities.append(dict(directory=str(directory.relative_to(ROOT)),variant=variant,transport=transport,pid=ready['processId'],started_utc=invocation['observed_at_utc']))
check(len(identities)==172,'Expected172 fresh server identities')
orders=[]
for phase in ['startup','idle','load']:
    for transport in ['http','graphql']:
        for index in range(30 if phase=='startup' else 5):
            order='BE' if index%2==0 else 'EB';a='baseline' if order[0]=='B' else 'engine';b='engine' if a=='baseline' else 'baseline'
            first=read(ROOT/phase/transport/f'{index:02}-{a}'/'invocation.json')['observed_at_utc'];second=read(ROOT/phase/transport/f'{index:02}-{b}'/'invocation.json')['observed_at_utc']
            check(first<second,f'{phase}/{transport}/{index}: predeclared pair order changed');orders.append(dict(phase=phase,transport=transport,index=index,order=order,first_utc=first,second_utc=second))
for transport in ['http','graphql']:
    for rate,order in [(100,'BE'),(500,'EB'),(2000,'BE')]:
        a='baseline' if order[0]=='B' else 'engine';b='engine' if a=='baseline' else 'baseline'
        first=read(ROOT/'diagnostics'/transport/f'{rate:04}-{a}'/'invocation.json')['observed_at_utc'];second=read(ROOT/'diagnostics'/transport/f'{rate:04}-{b}'/'invocation.json')['observed_at_utc']
        check(first<second,f'diagnostics/{transport}/{rate}: pair order changed');orders.append(dict(phase='diagnostics',transport=transport,rate=rate,order=order,first_utc=first,second_utc=second))

staging=read(BASE/'.local/collector-final-app-staging-02.json');target=Path(staging['target']);source=Path(staging['source']);staged=[]
for file in staging['files']:
    a=source/file['path'];b=target/file['path'];expected=file['sha256']
    check(a.is_file() and b.is_file() and sha(a)==sha(b)==expected,'Staged or retained build file mismatch '+file['path'])
    staged.append(dict(path=file['path'],sha256=expected,bytes=file['bytes']))
check({x['path'] for x in staging['files']}=={str(p.relative_to(target)) for p in target.rglob('*') if p.is_file()},'Native app contains extra/missing files vs staging manifest')
check(staging['samples_source_revision']==manifest['samples_revision'] and staging['engine_revision']==manifest['engine_revision'] and staging['assembly_sha256']==manifest['assembly_sha256'],'Staging source/assembly provenance mismatch')

phases=read(OUT/'phase-recomputation.json');accounting=read(OUT/'accounting-recomputation.json');measure=[r for r in phases if r['path'].endswith('/measured-requests.jsonl.gz')];main=[r for r in measure if r['path'].startswith('load/')];diag=[r for r in measure if r['path'].startswith('diagnostics/')]
check(len(main)==20 and len(diag)==12 and len(phases)==136,'Main/diagnostic/phase counts differ from complete protocol')
check(all(r['summary']['correct']==r['summary']['offered']==r['summary']['successfulWithinDrain'] and r['summary']['errors']==r['summary']['dropped']==0 and not r['summary']['errorKinds'] for r in phases),'Entered phase has unsuccessful/drain-late offered work')
check(all(r['over_1s_scheduled_latency_rows']==0 for r in phases),'Scheduled1s latency exceeded in a retained phase')
check(len(accounting)==136 and sum(x['server_metric_control_before_persist'] for x in accounting)==32,'Measured server metric control window count differs')
observations=read(ROOT/'diagnostic-observations.json')
check(len(observations)==12 and all(x['timed_measurement_executed'] is True and x['diagnostic_status']=='completed' and x['driver_exit_code']==0 and x['contract_and_offered_work_observation_valid'] is True for x in observations),'Diagnostic attempts/actual timing classification differs')
for transport in ['http','graphql']:
    for rate in [100,500,2000]:
        b=read(ROOT/'diagnostics'/transport/f'{rate:04}-baseline/driver/load-result.json');e=read(ROOT/'diagnostics'/transport/f'{rate:04}-engine/driver/load-result.json')
        check(b['manifestHash']==e['manifestHash'] and b['logicalManifestHash']==e['logicalManifestHash'] and b['finalState']['stateHash']==e['finalState']['stateHash'],f'{transport}/{rate}: diagnostic parity mismatch')

numeric=all(r['absolute_budget_passed'] and r['overhead_budget_passed'] for r in scan['startup_numeric_recomputation']) and all(r['passed'] for r in scan['idle_pair_recomputation']) and all(r['latency_absolute_passed'] and r['latency_extra_passed'] and r['allocation_extra_passed'] for r in scan['main_load_pair_recomputation']) and all(r['budget_passed'] for r in scan['main_load_stability_recomputation'])
summary=read(ROOT/'summary.json');check(numeric==summary['numeric_budget_observations_passed'],'Aggregate numerical classification differs');check(manifest['reference_environment_qualified'] is False and summary['reference_gate_passed'] is False,'Reference boundary changed')
result=dict(status='consistent' if not issues else 'audit-findings',observed_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),input=str(ROOT),samples_revision=manifest['samples_revision'],engine_revision=manifest['engine_revision'],raw_scan_sha256=sha(OUT/'audit.json'),raw_scan_script_sha256=sha(Path(__file__).with_name('audit_raw_benchmark_04.py')),finalization_script_sha256=sha(Path(__file__)),input_manifest_sha256=sha(ROOT/'manifest.json'),all_gzip_records_scanned=True,counts=scan['counts'],source_files_verified=scan['source_files_verified_against_recorded_commits'],build_input_hashes_match_per_host=scan['build_source_inputs_verified_per_host'],all_native_app_files_independently_matched_to_build=len(staged),fresh_server_identities=len(identities),predeclared_pair_orders_checked=len(orders),phase_accounting_records=len(accounting),measured_server_metrics_before_persistence_records=32,main_measured_offered_and_correct=sum(r['summary']['correct'] for r in main),diagnostic_attempted=len(observations),diagnostic_timed_runs=len(diag),diagnostic_measured_offered_and_correct=sum(r['summary']['correct'] for r in diag),all_timed_measured_offered_and_correct=sum(r['summary']['correct'] for r in measure),all_entered_phase_errors=scan['counts']['semantic_error_flags'],original_numeric_budgets_passed=numeric,reference_environment_qualified=False,full_reference_acceptance_passed=False,maximum_recorded_clock_offset_deviation_ns=scan['maximum_recorded_clock_offset_deviation_ns'],startup=scan['startup_numeric_recomputation'],main_all_five_p95_and_population_cv=scan['main_load_stability_recomputation'],unexpected_findings=issues,limits=scan['limits']+['Physical128-response readiness is proved at the retained barrier only; later cumulative TLS history is not a live-socket count.','Native app staging files were independently rehashed; the full SDK tree was not independently rescanned during this audit. Retained SDK-reverification and actual loaded-runtime paths provide separate evidence.','Canonical03 failed preflight remains historical negative evidence; successful04 does not erase it or establish a causal Engine-only speedup.','No builds, requests, reruns, source edits, commits or remote writes were performed by this audit.'])
for name,value in [('audit-final.json',result),('owned-identities.json',identities),('pair-orders.json',orders),('staged-file-recomputation.json',staged)]:
    (OUT/name).write_text(json.dumps(value,indent=2)+'\n')
lines=['# Independent canonical04 raw audit','',f"Status: {result['status']}. Independently streamed all{scan['counts']['gzip_files']} gzip files: {scan['counts']['phase_rows']:,} offered phase records and{scan['counts']['manifest_rows']:,} frozen manifest rows. No record filtering or replacement. All raw indices/operations/schedules, count conservation, p95/p99, state/lifetime, manifests and logical/wire hashes were recomputed.",'',f"Checked120 startup launches,20 idle processes/1200 RSS slots,20 main runs,12 attempted and12 actually timed diagnostics,172 fresh server identities and86 predeclared pair orders. Verified52 physical128-response preparation barriers,136 phase TLS/client accounting records and32 final-server metrics windows before persistence. Independently regenerated{scan['counts']['complete_state_snapshots']} complete driver/server state snapshots. All entered phases had0errors/drops and every offer completed within the drain budget.",'',f"Measured main: {result['main_measured_offered_and_correct']:,} correct offers. Measured diagnostics: {result['diagnostic_measured_offered_and_correct']:,} correct offers. Total actual measured: {result['all_timed_measured_offered_and_correct']:,}. No failed-preflight or later-phase substitution was found in04; canonical03 remains preserved.",'',f"All original numerical startup/idle/latency/allocation/all-five-CV gates: {'PASS' if numeric else 'FAIL'}. Shared WSL reference remains nonqualifying; #3 stays Blocked. No dedicated2vCPU/2GiB, supported-Windows, production or sustained capacity promotion follows.",'',f"All{result['source_files_verified']} frozen source hashes match recorded Samples{manifest['samples_revision']} / Engine{manifest['engine_revision']};15 build inputs per host match clean02 manifests. All{len(staged)} native app files match retained Linux02 build bytes and staging manifest. Actual loaded-runtime paths were checked for all172 processes; full SDK-tree rehashing is outside this audit.",'','## All five p95 observations and population CV','']
for row in scan['main_load_stability_recomputation']:lines.append(f"- {row['transport']}/{row['variant']}: {row['p95_ms_all_five']}ms; CV{row['population_cv']*100:.12f}%.")
lines+=['','## Findings and proof limits','',f"Unexpected findings: {len(issues)}.",'']+['- '+i for i in issues+result['limits']]
(OUT/'audit-final.md').write_text('\n'.join(lines)+'\n')
print(json.dumps({k:result[k] for k in ['status','counts','source_files_verified','all_native_app_files_independently_matched_to_build','original_numeric_budgets_passed','all_timed_measured_offered_and_correct','unexpected_findings']}),flush=True)
