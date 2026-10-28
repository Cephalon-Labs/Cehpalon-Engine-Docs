"""Read-only evidence analysis. Run with WSL python3; never runs a workload."""
import collections, datetime, gzip, hashlib, json, pathlib, subprocess

S=pathlib.Path('/mnt/d/Cephalon/Cehpalon-Engine-Samples')
W=pathlib.Path('/mnt/d/Cephalon/.worktrees')
OUT=W/'w2-collector-readiness/.local/closure-audit04'
PROBE=pathlib.Path('/home/tom/.local/share/cehpalon-benchmark-runs/collector-readiness-probe-01')
CANON=pathlib.Path('/home/tom/.local/share/cehpalon-benchmark-runs/benchmark-observation-04')
REV='a3bd8b5c5747440c81124774ac10b6451d88ff82'
findings=[]
def check(ok, text):
    if not ok: findings.append(text)
def read(p): return json.loads(p.read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
    with gzip.open(p,'rt') as f:
        header=json.loads(next(f)); return header,[json.loads(x) for x in f]

audit={'observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
       'activity':'Read-only native WSL file/JSON/Git analysis; no workload, SDK, tests, builds, requests or remote writes.'}
pre=W/'w2-collector-readiness/.local/precanonical-audit04'
prior=read(pre/'sequential02-precanonical-audit.json')
for host,b in prior['builds'].items():
    check(b['samples_source_revision']==REV and b['committed_input_hashes_verified']==15,host+' provenance source/count')
    for file,expected in b['source_sha256'].items():
        blob=subprocess.check_output(['git','-C',str(S),'show',REV+':'+file])
        check(hashlib.sha256(blob).hexdigest()==expected,host+' frozen Git blob '+file)
    check(b['generated_registration_count']==3 and b['generated_operation_ids']==['catalog.get','catalog.list','catalog.set'],host+' generated registry')
    check(not any('CodeAnalysis' in x or 'CodeGeneration' in x for x in b['runtime_libraries']),host+' compiler-free runtime graph')
audit['reused_sequential02_audit']={'path':str(pre/'sequential02-precanonical-audit.json'),'sha256':sha(pre/'sequential02-precanonical-audit.json'),
    'fresh_frozen_git_blob_checks':30,'builds':prior['builds'],'functional':prior['functional'],'native_staging':prior['native_staging'],
    'scope':'Prior independently checked raw conformance/staging reused unchanged; no runtime rerun or large SDK rehash in closure audit.'}
for host,h in prior['functional']['hosts'].items():
    native_root=S/f'.local/collector-conformance-{("win" if host=="windows" else "linux")}-02/conformance'
    for file,expected in h['evidence_json_sha256'].items():
        check(sha(native_root/file)==expected,host+' unchanged conformance raw '+file)
    check(h['raw_corpus_cases']==4000 and h['raw_cancellation_records_included_in_corpus']==400 and h['repeat_lifecycle_cycles']==120 and h['api_only_exercise_requests_from_source_loop_and_completed_checks']==20000,host+' functional totals')
audit['reused_sequential02_audit']['fresh_raw_json_hashes_verified']=sum(len(h['evidence_json_sha256']) for h in prior['functional']['hosts'].values())
negative=read(pre/'conformance01-negative.json')
failed=negative['reports']['win']['failed_rows'][0]
check(failed['record']['index']==409 and failed['record']['passed'] is False and failed['record']['handlerEnteredBeforeAbort'] is False,'retained01 negative exact case')
audit['retained01_negative']={'path':str(pre/'conformance01-negative.json'),'sha256':sha(pre/'conformance01-negative.json'),'failed_case':failed,
    'interpretation':'Windows01 fails in-flight cancellation. Sequential02 is a whole predeclared repeat, not replacement of one case. No cause from concurrency is established.'}

probe_runs=[]; pids=[]; prefix_by_wire={}; manifest_hash_by_wire={}
for wire in ['http','graphql']:
    for pair in range(3):
        for variant in (['baseline','engine'] if pair!=1 else ['engine','baseline']):
            name=f'{wire}/{pair:02}-{variant}'; p=PROBE/'probes'/name; d=p/'driver'
            prep=read(d/'collector-preparation.json'); bar=prep['barrier']; r=read(d/'preflight-result.json'); a=read(d/'preflight-evidence-accounting.json')
            state=read(p/'final-state.json'); stop=read(p/'shutdown.json'); ready=read(p/'ready.json')
            pids.append(ready['processId']); check(ready['variant']==variant and ready['transport']==wire and ready['tlsProtocol']=='Tls13',name+' ready')
            check(prep['status']=='passed' and prep['readOnlyRequests']==prep['successfulReadOnlyRequests']==len(prep['requests'])==130,name+' prep130')
            held=[x for x in prep['requests'] if x['stage']=='held-load']; warm=[x for x in prep['requests'] if x['stage']=='warm-read']
            check(len(held)==128 and len(warm)==2,name+' prep stages')
            check(bar['passed'] and bar['poolScope']=='load' and all(bar[k]==128 for k in ['targetConnections','heldResponses','nonemptyHttp11Responses','tlsConnectionsAtBarrier','distinctConnectionCount']),name+' physical barrier')
            ids=set(bar['distinctConnectionIds']); tlsids=set(bar['loadTlsConnectionIdsAtBarrier'])
            check(len(ids)==len(tlsids)==128 and ids==tlsids=={x['connectionId'] for x in held},name+' connection ID corroboration')
            for x in prep['requests']:
                check(x['passed'] and x['status']==200 and x['bytes']>0 and x['httpVersion']=='1.1' and not x['connectionClose'] and (x['contentLength'] is None and x['chunked'] or (x['contentLength'] or 0)>0),name+' prep status/framing')
                check(x['startedTicks']<=x['headersReadyTicks']<=x['bodyReadStartedTicks']<=x['bodyCompletedTicks']<=x['completedTicks'],name+' prep row ordering')
            check(max(x['headersReadyTicks'] for x in held)<=bar['allHeadersReadyTicks']<=bar['releasedTicks']<=min(x['bodyReadStartedTicks'] for x in held),name+' all128 held before release')
            check(bar['completedTicks']>=max(x['completedTicks'] for x in held) and bar['deadlineSeconds']==30 and (prep['preparationCompletedTicks']-prep['preparationStartedTicks'])/prep['stopwatchFrequency']<=30,name+' prep deadline')
            check(r['status']=='passed' and r['mode']=='preflight-only' and r['rate']==2000 and r['seconds']==2 and r['plannedManifestOffers']==360000 and r['enteredPhases']==['preflight'] and r['warmupEntered'] is False and r['measuredEntered'] is False,name+' actual versus plan')
            check(not any('warmup-' in x.name or 'measured-' in x.name or x.name=='load-result.json' or x.name=='collector-failure.json' for x in d.iterdir()),name+' no later artifacts')
            h,raw=rows(d/'preflight-requests.jsonl.gz'); freq=h['frequency']; check(len(raw)==4000 and len(h['columns'])==8 and freq==1000000000,name+' raw count/header')
            first=raw[0][2]; counts=collections.Counter()
            for i,x in enumerate(raw):
                check(len(x)==8 and x[0]==i and x[2]==first+i*freq//2000 and x[2]<=x[3]<=x[4] and x[5]==200 and x[6]>0 and x[7]=='',name+f' raw row {i}')
                counts[x[1]]+=1
            check(counts=={'get':3200,'list':600,'set':200},name+' workload mix')
            with gzip.open(d/'offered-manifest.jsonl.gz','rt') as f:
                prefix=[json.loads(next(f)) for _ in range(4000)]
                manifest_count=4000+sum(1 for _ in f)
            check(manifest_count==360000,name+' planned manifest conservation')
            check(all(x[0]==m['index'] and x[1]==m['operation'] for x,m in zip(raw,prefix)),name+' manifest raw prefix')
            prefixhash=hashlib.sha256(json.dumps(prefix,sort_keys=True,separators=(',',':')).encode()).hexdigest()
            manifesthash=sha(d/'offered-manifest.jsonl.gz')
            if wire in prefix_by_wire: check(prefix_by_wire[wire]==prefixhash and manifest_hash_by_wire[wire]==manifesthash,name+' paired deterministic manifest')
            prefix_by_wire[wire]=prefixhash;manifest_hash_by_wire[wire]=manifesthash
            # Frozen Domain.cs Reset declares lower-case item-{id:D5}, revision0, amount=id*17.
            model=[{'id':i,'label':f'item-{i:05d}','revision':0,'amountMinorUnits':i*17} for i in range(1,10001)]
            for m in prefix:
                if m['operation']=='set':
                    item=model[m['id']-1]; check(item['revision']==m['expectedRevision'],name+' write expected revision'); item['label']=m['label'];item['revision']+=1
            check(state['records']==model,name+' independent 10000-record write replay')
            statehash=hashlib.sha256(json.dumps(model,separators=(',',':')).encode()).hexdigest()
            check(state['stateHash']==statehash=='8c849f782701cc524da2ebd0b9dcc78b81efef8ad6a14dfd437e1c2abd2ab9cc',name+' independently hashed final state')
            check(state['factories']==state['constructors']==state['disposals']==4130 and state['reads']==3930 and state['writes']==200,name+' handler balance/state counters')
            pr=state['probes'];check(pr['forbiddenFactories']==0 and (wire!='http' or all(pr[k]==0 for k in ['graphQLFactories','graphQLServices','graphQLDiagnosticConstructors','graphQLExecutorInitializations','graphQLSchemasReady'])),name+' disabled probes')
            check(a['phase']=='preflight' and a['offeredCount']==a['observedCount']==4000 and a['phaseFailure'] is None,name+' phase accounting')
            check(a['clientBefore']['observedTicks']<=a['phaseStartedTicks']<=a['requestsCompletedTicks']<=a['clientAfter']['observedTicks']<=a['persistenceStartedTicks']<=a['persistenceCompletedTicks'],name+' telemetry brackets')
            before=a['tlsConnectionsBefore'];after=a['tlsConnectionsAfter'];beforeids={x['connectionId'] for x in before};afterids={x['connectionId'] for x in after}
            check(beforeids<=afterids and set(a['newTlsConnectionIds'])==afterids-beforeids,name+' TLS accounting')
            check(len(before)==129 and {x['connectionId'] for x in before if x['pool']=='load'}==ids and len([x for x in before if x['pool']=='control'])==1,name+'129 pool scoped before TLS')
            check(all(x['protocol']=='Tls13' and x['httpVersion']=='1.1' and x['cipher'] and x['connectedTicks']<=a['clientAfter']['observedTicks'] and x['stopwatchFrequency']==freq for x in after),name+' strict TLS metadata')
            check(all(stop[k] for k in ['graceful','listener_closed','owned_handlers_balanced','disabled_probes_zero','passed']) and stop['exit_code']==0 and stop['elapsed_ms']<=5000,name+' owned shutdown')
            check(r['preflight']['offered']==r['preflight']['correct']==r['preflight']['successfulWithinDrain']==4000 and r['preflight']['errors']==r['preflight']['dropped']==0 and r['state']['passed'],name+' preflight report')
            probe_runs.append({'run':name,'process_id':ready['processId'],'actual':len(raw),'planned':manifest_count,'operations':dict(counts),'prepared_readonly':130,'held_physical_load':128,'tls_before':len(before),'tls_after':len(after),'new_tls':len(a['newTlsConnectionIds']),'state_hash':state['stateHash'],'shutdown_ms':stop['elapsed_ms'],'raw_sha256':sha(d/'preflight-requests.jsonl.gz'),'manifest_sha256':manifesthash})
check(len(probe_runs)==len(set(pids))==12,'12 fresh probe server processes')
audit['probe']={'runs':probe_runs,'actual_offered':sum(x['actual'] for x in probe_runs),'planned_offered':sum(x['planned'] for x in probe_runs),'warmup_measured_runs':0,'scope':'128 simultaneously held HTTP1.1 bodies plus fresh-load TLS128 prove readiness cohort; IDs corroborate, not per-request socket tracing. No capacity acceptance budget scored.'}
for root in [PROBE,CANON]:
    manifest=read(root/'manifest.json')
    check(manifest['samples_revision']==REV and manifest['engine_revision']=='6804271d429106864e01e4ec546a41dff771f84b' and manifest['assembly_sha256']==prior['native_staging']['app_assembly_sha256'],root.name+' frozen source/native binary binding')

proof=read(W/'w2-collector-readiness/.local/collector-proof/results01/proof.json');check(proof['passed']==10 and proof['failed']==0,'offline10')
shared=W/'w2-collector-probe/.local/collector-metadata-tests04.txt';sharedtext=shared.read_text();check('Ran 29 tests' in sharedtext and 'OK' in sharedtext,'shared29 transcript')
classifier=read(S/'.local/canonical-classifier-review.json');check(classifier['assertions']==16 and classifier['passed'] and all(x['passed'] for x in classifier['cases']),'classifier16')
peerroot=W/'w2-collector-adversarial/.local/collector-robustness-01';peer=read(peerroot/'summary.json')
check(len(peer['cases'])==5 and peer['passed'] and all(x['passed'] and x['exitCode']==1 for x in peer['cases']),'peer actual5')
for entry in peer['files']: check(sha(peerroot/entry['path'])==entry['sha256'], 'peer raw hash '+entry['path'])
pf=peerroot/'phase-503';failure=read(pf/'collector-failure.json');h,raw=rows(pf/'preflight-requests.jsonl.gz'); acct=read(pf/'preflight-evidence-accounting.json')
check(len(raw)==4000 and all(len(x)==8 and x[0]==i and x[5]==503 and x[7]=='http.503' for i,x in enumerate(raw)),'actual TLS503 raw4000')
check(failure['status']=='collector-preflight-failed' and failure['enteredPhases']==['preflight'] and not failure['warmupEntered'] and not failure['measuredEntered'] and failure['counts']['errors']==4000 and acct['clientBefore'] and acct['clientAfter'] and len(acct['tlsConnectionsBefore'])==len(acct['tlsConnectionsAfter'])==129,'503 failure telemetry')
audit['proof_closure']={'offline':proof,'shared_metadata_tests':{'count':29,'transcript':str(shared),'sha256':sha(shared)},'classifier':classifier,'peer_actual_tls':peer,'actual_503_raw_rows':4000,'scope':'Proof totals are different kinds of evidence, not benchmark/capacity trials. Peer DLL is a separate build of reviewed Driver source, not asserted bit-identical to canonical native binary.'}

diag=read(CANON/'diagnostic-summary.json'); observations=diag['observations']
check(len(observations)==12 and diag['attempted_runs']==diag['timed_measurement_runs']==12 and diag['collector_preflight_failures']==diag['timed_runs_with_capacity_or_contract_errors']==diag['shutdown_failures']==0,'canonical04 diagnostic accounting')
for x in observations: check(x['diagnostic_status']=='completed' and x['timed_measurement_executed'] and x['driver_exit_code']==0 and x['measured']['offered']==x['measured']['correct'] and x['measured']['errors']==x['measured']['dropped']==0,'canonical04 diagnostic '+x['transport']+str(x['rate'])+x['variant'])
old=pathlib.Path('/home/tom/.local/share/cehpalon-benchmark-runs/benchmark-observation-03/diagnostics/http/2000-engine/driver')
oh,oldraw=rows(old/'preflight-requests.jsonl.gz');drops=[x[0] for x in oldraw if x[7]=='offered.dropped']
check(drops==list(range(129,162))+list(range(178,182)) and len(oldraw)==4000,'retained03 raw37 drop exact indices')
oldprep=read(old/'collector-preparation.json');oldtls=oldprep.get('tlsConnections',[])
oldacct=read(old/'preflight-evidence-accounting.json')
newengine=CANON/'diagnostics/http/2000-engine/driver'
newprep=read(newengine/'collector-preparation.json');newacct=read(newengine/'preflight-evidence-accounting.json')
audit['forensic_comparison']={'canonical04_diagnostics':{'attempted':12,'timed':12,'measured_offered':sum(x['measured']['offered'] for x in observations),'errors':0,'drops':0,'runs':observations},
    'canonical03_http_engine2000':{'actual_preflight':4000,'correct':3963,'dropped':37,'drop_indices':drops,'warmup_measured_entered':False,'old_preparation_tls_events':len(oldtls),'failed_phase_accounting_exists':True,'failed_phase_client_gc_accounting_exists':bool(oldacct['clientBefore'] and oldacct['clientAfter']),'failed_phase_tls_before_after_present':'tlsConnectionsBefore' in oldacct and 'tlsConnectionsAfter' in oldacct,'failed_raw_sha256':sha(old/'preflight-requests.jsonl.gz')},
    'canonical04_http_engine2000_preflight':{'held_physical_load':newprep['barrier']['heldResponses'],'tls_at_barrier':newprep['barrier']['tlsConnectionsAtBarrier'],'phase_tls_before':len(newacct['tlsConnectionsBefore']),'phase_tls_after':len(newacct['tlsConnectionsAfter']),'new_phase_tls_ids':newacct['newTlsConnectionIds']},
    'interpretation':'Canonical04 measured HTTP Engine2000 completed after explicit128physical readiness and failure telemetry correction. This association does not identify a single cause or capacity ceiling; old03 has incomplete failed-phase connection telemetry. Diagnostic rate results have no acceptance latency/allocation gate; new evidence never repairs old failed37 drops.',
    'variation_note':'Main04 CV all under10%; Engine GraphQL04 4.76935% exceeds03 3.2616%, so no all-metric improvement claim.'}
audit['limits']=['Public fixed-identity synthetic fixture; no real tenant, IdP/provider or production qualification.',
    'Shared WSL/Windows observational evidence, no reserved reference2CPU/2GiB or supported-Windows qualification; Engine unchanged and #3 Blocked.',
    'Probe planned4.32M manifest offers are not executed4.32M requests: actual48k, prep1560 read-only calls outside schedules.',
    'Conformance400 cancellation cases are included in4000 per host;120 cycles are same-process, not fresh startup.',
    'Retained Windows01 negative remains; sequential02 pass does not establish cause of01 failure.',
    'No runtime reruns or new benchmarks were performed by this audit.']
audit['audit_script_correction']={'retained_attempt':'audit-script-label-defect-attempt01.json','cause':'Audit model incorrectly upper-cased Item; frozen Domain.cs line52 declares lower-case item-{id:D5}. Corrected only audit expected initialization; retained initial audit script/output. No workload rerun or evidence change.'}
audit['findings']=findings;audit['status']='passed_with_limits' if not findings else 'findings'
OUT.mkdir(parents=True,exist_ok=True);(OUT/'closure-audit04.json').write_text(json.dumps(audit,indent=2)+'\n')
print(json.dumps({'status':audit['status'],'findings':findings,'probe_actual':audit['probe']['actual_offered'],'probe_planned':audit['probe']['planned_offered'],'diagnostic_measured':audit['forensic_comparison']['canonical04_diagnostics']['measured_offered']}))
