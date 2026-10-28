from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import statistics

SAMPLES=Path('D:/Cephalon/Cehpalon-Engine-Samples')
OUTPUT=Path('D:/Cephalon/.worktrees/w2-collector-readiness/.local/precanonical-audit04')
SOURCES={'windows':SAMPLES/'.local/collector-conformance-win-02/conformance','linux':SAMPLES/'.local/collector-conformance-linux-02/conformance'}
findings=[]
def check(value,message):
 if not value:findings.append(message)
def load(path):return json.loads(path.read_text(encoding='utf-8'))
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def canonical(value):return json.dumps(value,separators=(',',':'),ensure_ascii=True).encode('utf-8')

reports={}
for system,root in SOURCES.items():
 declaration=load(root/'predeclared.json');summary=load(root/'summary.json');cases=load(root/'ordered-corpus.json');dataset=load(root/'dataset.json')
 check(summary['status']=='passed' and summary['failed']==0,system+': summary failed')
 check(declaration==summary['declaration'],system+': declared protocol differs from summary')
 check(digest(root/'dataset.json')==declaration['datasetSha256'],system+': dataset hash mismatch')
 check(digest(root/'ordered-corpus.json')==declaration['orderedCorpusSha256'],system+': ordered corpus hash mismatch')
 check(len(cases)==1000 and [x['index'] for x in cases]==list(range(1000)),system+': corpus missing/duplicate/out-of-order cases')
 initial=[{'id':i,'label':f'item-{i:05d}','revision':0,'amountMinorUnits':i*17} for i in range(1,10001)]
 check(dataset==initial,system+': fixed10000record initial dataset differs')
 model={item['id']:dict(item) for item in dataset};positive_writes=0
 for case in cases:
  code=case['expectedCode'];request=case['input'];operation=case['operation'];expected=None
  if code=='success':
   if operation=='get':expected=dict(model[request['id']])
   elif operation=='list':expected={'items':[dict(model[i]) for i in range(request['page']*20+1,request['page']*20+21)]}
   else:
    before=model[request['id']];check(before['revision']==request['expectedRevision'],f'{system}: model write revision mismatch at{case["index"]}')
    expected=dict(before,label=request['label'],revision=before['revision']+1);model[request['id']]=dict(expected);positive_writes+=1
   check(expected==case['expectedValue'],f'{system}: independently replayed expected success differs at{case["index"]}')
  elif code=='resource.conflict':check(model[request['id']]['revision']!=request['expectedRevision'],f'{system}: false conflict expectation at{case["index"]}')
  elif code=='resource.not_found':check(request['id'] not in model,f'{system}: false missing record expectation at{case["index"]}')
  elif code=='validation.failed':check(request.get('id',1)<=0 or len(request.get('label',''))>64,f'{system}: false validation expectation at{case["index"]}')
  else:check(code=='operation.cancelled' and request['label']=='must-not-be-written',f'{system}: undeclared outcome at{case["index"]}')
  if case['index']%10 in (0,7):
   number=int.from_bytes(hashlib.sha256((declaration['seed']+':'+str(case['index'])).encode()).digest()[:8],'big')
   check(request['id']==1+number%10000,f'{system}: SHA256seed read ID differs at{case["index"]}')
 check(positive_writes==100,system+': expected mutation count differs')
 final_hash=hashlib.sha256(canonical([model[i] for i in range(1,10001)])).hexdigest()
 check(final_hash==declaration['finalDatasetSha256'],system+': independently replayed expected final state hash differs')
 expected_counts=Counter(x['expectedCode'] for x in cases)
 check(expected_counts==Counter({'success':500,'resource.conflict':100,'resource.not_found':100,'validation.failed':200,'operation.cancelled':100}),system+': wrong declared category count')
 lane_reports=[];all_cancel=[];all_cycles=[];all_files={}
 for variant in ('baseline','engine'):
  for transport in ('http','graphql'):
   lane=variant+'-'+transport;directory=root/lane;rows=load(directory/'case-results.json');checks=load(directory/'checks.json');cycles=load(directory/'lifecycle-cycles.json');probes=load(directory/'main-host-probes.json')
   check(len(rows)==1000 and [x['index'] for x in rows]==list(range(1000)),f'{system}/{lane}: omitted/duplicate/reordered raw case')
   check(all(x['passed'] is True for x in rows),f'{system}/{lane}: failed raw case')
   for row,case in zip(rows,cases):
    check(row['operation']==case['operation'] and row['expectedCode']==case['expectedCode'],f'{system}/{lane}: raw case not identical to frozen manifest at{row["index"]}')
    if case['expectedCode']!='operation.cancelled':
     check(row['actualCode']==case['expectedCode'],f'{system}/{lane}: wrong raw business outcome at{row["index"]}')
     expected_status=200 if transport=='graphql' or case['expectedCode']=='success' else {'resource.not_found':404,'resource.conflict':409,'validation.failed':400}[case['expectedCode']]
     check(row['status']==expected_status,f'{system}/{lane}: unexpected status at{row["index"]}')
   cancel=[x for x in rows if x['expectedCode']=='operation.cancelled']
   check(len(cancel)==100,f'{system}/{lane}: not100cancelrecords')
   frequencies=[]
   for row in cancel:
    started,scheduled,aborted,entered,ack=(row[k] for k in ('requestStartedTimestamp','scheduledAbortTimestamp','actualAbortTimestamp','handlerEnteredTimestamp','serverAcknowledgedTimestamp'))
    frequency=declaration['stopwatchFrequency'];frequencies.append(frequency)
    check(started<=entered<=aborted and aborted>=scheduled,f'{system}/{lane}: delayed handler/abort ordering invalid at{row["index"]}')
    check(row['actualAbortAfterStartMilliseconds']>=50,f'{system}/{lane}: early abort at{row["index"]}')
    check(0<=row['serverAckAfterAbortMilliseconds']<=100 and ack>=aborted,f'{system}/{lane}: cancellation acknowledgement outside100ms at{row["index"]}')
    check(abs((scheduled-started)*1000/frequency-50)<.001,f'{system}/{lane}: raw scheduled deadline differs from50ms at{row["index"]}')
    check((ack-aborted)*1000/frequency<=100,f'{system}/{lane}: raw ack interval exceeded100ms at{row["index"]}')
    check(abs((ack-aborted)*1000/frequency-row['serverAckAfterAbortMilliseconds'])<=.00011,f'{system}/{lane}: raw ack interval differs from recorded100ns-quantized ms at{row["index"]}')
    check(abs((aborted-started)*1000/frequency-row['actualAbortAfterStartMilliseconds'])<=.00011,f'{system}/{lane}: raw abort interval differs from recorded100ns-quantized ms at{row["index"]}')
    check(row['handlerEnteredBeforeAbort'] and row['noMutationAfterAck'] and row['ownedHandlerCompleted'] and row['failure'] is None,f'{system}/{lane}: late mutation/unjoined ownership/entry failure at{row["index"]}')
   check(len(set(frequencies))==1,f'{system}/{lane}: raw clockfrequency inconsistent')
   all_cancel += [dict(row,lane=lane) for row in cancel]
   check(len(cycles)==30 and [x['cycle'] for x in cycles]==list(range(30)),f'{system}/{lane}: lifecycle omitted/duplicate cycle')
   check(all(x['passed'] and 0<=x['shutdownMilliseconds']<=5000 and x['factories']==x['disposals']==1 for x in cycles),f'{system}/{lane}: lifecycle threshold/ownership failure')
   all_cycles += [dict(row,lane=lane) for row in cycles]
   check(all(x['passed'] for x in checks),f'{system}/{lane}: negative/state/shutdown check failed')
   check(probes['forbiddenFactories']==0 and probes['hostFactories']==probes['apiFactories']==1,f'{system}/{lane}: forbidden/host factory counts differ')
   graph_keys=('graphQLFactories','graphQLServices','graphQLDiagnosticConstructors','graphQLExecutorInitializations','graphQLSchemasReady')
   if transport=='http':
    check(all(probes[key]==0 for key in graph_keys),f'{system}/{lane}: disabled GraphQL activation occurred')
    check(any(x['name']=='10000 API requests retain zero disabled registrations/factories' and x['passed'] for x in checks),f'{system}/{lane}: missing10000activation exercise completion')
   else:check(all(probes[key]>=1 for key in graph_keys),f'{system}/{lane}: enabled GraphQL lifecycle probes absent')
   lane_reports.append({'lane':lane,'raw_cases':len(rows),'cancellation_records':len(cancel),'maximum_ack_ms':max(x['serverAckAfterAbortMilliseconds'] for x in cancel),'minimum_actual_abort_after_start_ms':min(x['actualAbortAfterStartMilliseconds'] for x in cancel),'maximum_actual_abort_after_start_ms':max(x['actualAbortAfterStartMilliseconds'] for x in cancel),'actual_declared_stopwatch_frequency_hz':frequencies[0],'lifecycle_cycles':len(cycles),'maximum_shutdown_ms':max(x['shutdownMilliseconds'] for x in cycles),'probes':probes,'host_checks':len(checks)})
 configuration=load(root/'configuration-preflight.json');check(len(configuration)==5 and all(x['passed'] for x in configuration),system+': pure configuration preflight mismatch')
 for file in root.rglob('*.json'):all_files[file.relative_to(root).as_posix()]=digest(file)
 worst=max(all_cancel,key=lambda x:x['serverAckAfterAbortMilliseconds']);slowest=max(all_cycles,key=lambda x:x['shutdownMilliseconds'])
 reports[system]={'evidence_root':str(root),'summary_status':summary['status'],'dataset_sha256':digest(root/'dataset.json'),'ordered_corpus_sha256':digest(root/'ordered-corpus.json'),'independently_replayed_expected_final_sha256':final_hash,'raw_corpus_cases':sum(x['raw_cases'] for x in lane_reports),'raw_cancellation_records_included_in_corpus':len(all_cancel),'maximum_server_ack_after_abort_ms':worst['serverAckAfterAbortMilliseconds'],'worst_cancel_lane':worst['lane'],'worst_cancel_case_index':worst['index'],'repeat_lifecycle_cycles':len(all_cycles),'maximum_repeat_shutdown_ms':slowest['shutdownMilliseconds'],'maximum_shutdown_lane':slowest['lane'],'maximum_shutdown_cycle':slowest['cycle'],'api_only_exercise_requests_from_source_loop_and_completed_checks':20000,'configuration_pure_preflight_checks':len(configuration),'lanes':lane_reports,'evidence_json_sha256':all_files}

for system,report in reports.items():
 raw_values=[]
 for lane in report['lanes']:
  rows=load(Path(report['evidence_root'])/lane['lane']/'case-results.json')
  for row in rows:
   if row['expectedCode']=='operation.cancelled':
    frequency=load(Path(report['evidence_root'])/'predeclared.json')['stopwatchFrequency']
    raw_values.append((row['serverAcknowledgedTimestamp']-row['actualAbortTimestamp'])*1000/frequency)
 report['maximum_server_ack_after_abort_raw_tick_reconstruction_ms']=max(raw_values)
check(reports['windows']['dataset_sha256']==reports['linux']['dataset_sha256'],'Crosshost dataset identity differs')
check(reports['windows']['ordered_corpus_sha256']==reports['linux']['ordered_corpus_sha256'],'Crosshost ordered manifest differs')
source_hashes={name:digest(SAMPLES/'small-api-benchmark'/name) for name in ('Conformance.cs','Domain.cs','BenchmarkHost.cs','Wire.cs')}
boundaries=[
 'The400cancellationcases per host are INCLUDED in4000corpus executions; do not addthem again as4400cases.',
 'Actual Stopwatch frequency is now retained in each predeclared header. Raw intervals are checked against the unchanged100ms gate. Only representation comparison allows0.00011ms for100ns TimeSpan quantization.',
 'Responsebody equality andactualfinalstorestate were checked bytheexecutionharness. Raw case rows retain status/code andassertion outcomes, not allresponse bodies oractual final snapshots; thisaudit independently replays the frozen expected model, not absent response bytes.',
 'The20000API-only requests per host are supported by deterministic10000request loops andtwo completed high-level checks, not20000separately retained response records.',
 'The120repeat lifecycle cycles per host are same-process host restarts, separate from benchmark fresh-process startup measurements.',
 'Invalid/all-off/cycle evidence here is pure Composition compiler preflight. It does not itself execute a public BenchmarkHost with anall-off/invalid configuration; protectedconsumer host tests are separate.',
 'This is apublic synthetic10000record fixture withfixed server-owned public identity; it doesnotprove JWT/realIdP/tenant/provider/database/production isolation.',
 'Zero forbidden factory andGraphQL lifecycle probes coverthese explicitfixture paths; unimplemented provider traps are notproviderqualification.',
 'Windows26H2 remains observational andWSL doesnotclearsupported-Windows#3. No qualification orperformance promotion inferred fromthisfunctional audit.'
]
result={'observed_at_utc':datetime.now(timezone.utc).isoformat(),'status':'passed_with_explicit_boundaries' if not findings else 'findings','scope':'Read-only independent audit of final03functional JSON records and current source checks; no build,rerun,measurement,commit orremote write.','findings':findings,'source_files_audited_sha256':source_hashes,'hosts':reports,'totals':{'raw_corpus_executions':sum(r['raw_corpus_cases'] for r in reports.values()),'cancellations_included_in_corpus':sum(r['raw_cancellation_records_included_in_corpus'] for r in reports.values()),'same_process_lifecycle_cycles':sum(r['repeat_lifecycle_cycles'] for r in reports.values()),'api_only_exercise_requests_from_completed_checks':40000},'proof_boundaries':boundaries}
(OUTPUT/'functional-sequential02-audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
lines=['# Final02functional evidence audit','',f'ObservedUTC: {result["observed_at_utc"]}. Read-only; no builds,reruns,measurement,commits orremote writes.','',f'Status: {result["status"]}. Findings: {len(findings)}.','', '| Host | Corpus executions | Included cancellations | Maximum serverack afterabort | Repeat cycles | Maximum shutdown | API-onlyexercise |','| --- | ---: | ---: | ---: | ---: | ---: | ---: |']
for host,row in reports.items():lines.append(f'| {host} | {row["raw_corpus_cases"]} | {row["raw_cancellation_records_included_in_corpus"]} | {row["maximum_server_ack_after_abort_ms"]}ms | {row["repeat_lifecycle_cycles"]} | {row["maximum_repeat_shutdown_ms"]}ms |20000|')
lines+=['',f'Rawtick reconstruction maxima: Windows{reports["windows"]["maximum_server_ack_after_abort_raw_tick_reconstruction_ms"]}ms; Linux{reports["linux"]["maximum_server_ack_after_abort_raw_tick_reconstruction_ms"]}ms. Recorded .NET TimeSpan millisecond fields in thetable arequantized to100ns; bothraw andrecordedintervals satisfy100ms.','', 'Bothhosts have identical initialdataset and orderedcorpus hashes. All1000indexes perlane are accounted for, allrecorded outcomes match thefrozen manifest, all400cancellationrecords perhost satisfy theunchanged100ms acknowledgementlimit andserver-entry/abort ordering withjoined ownership/no mutation flags. Theindependently replayed expected model produces thedeclared finalstate hash. Enabled/disabled actualGraphQL lifecycle probes match eachprofile. All30repeat cycles perlane pass5second shutdown withbalanced ownership.','', 'Proof boundaries:','']+['- '+item for item in boundaries]
if findings:lines+=['','Findings:','']+['- '+item for item in findings]
(OUTPUT/'functional-sequential02-audit.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'status':result['status'],'findings':findings,'counts':result['totals'],'maximum_ack_ms':{host:row['maximum_server_ack_after_abort_ms'] for host,row in reports.items()},'maximum_shutdown_ms':{host:row['maximum_repeat_shutdown_ms'] for host,row in reports.items()}}))
