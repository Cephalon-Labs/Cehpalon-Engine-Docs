from pathlib import Path
import collections
from datetime import datetime,timezone
import gzip
import hashlib
import json
import math
import statistics

LOCAL=Path('D:/Cephalon/Cehpalon-Engine-Samples/.local/benchmark-observation-03')
UNC=Path(r'\\wsl.localhost\Ubuntu\home\tom\.local\share\cehpalon-benchmark-runs\benchmark-observation-03')
ROOT=LOCAL if (LOCAL/'diagnostics/http/2000-engine/driver/preflight-requests.jsonl.gz').exists() else UNC
OUTPUT=Path('D:/Cephalon/.worktrees/w2-graphql-tuning/.local/tuning-audit03')
def load(path):return json.loads(path.read_text(encoding='utf-8'))
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def percentile(values,p):return sorted(values)[max(0,math.ceil(len(values)*p)-1)]
def cluster(values):
 groups=[]
 for value in values:
  if not groups or value!=groups[-1][-1]+1:groups.append([value])
  else:groups[-1].append(value)
 return groups

reports={};findings=[]
def check(value,message):
 if not value:findings.append(message)
for variant in ('baseline','engine'):
 directory=ROOT/'diagnostics/http'/('2000-'+variant)/'driver'
 accounting=load(directory/'preflight-evidence-accounting.json');summary=load(directory/'collector-preflight.json');preparation=load(directory/'collector-preparation.json')
 with gzip.open(directory/'preflight-requests.jsonl.gz','rt',encoding='utf-8') as stream:
  header=json.loads(next(stream));rows=[json.loads(line) for line in stream]
 frequency=header['frequency'];start=accounting['phaseStartedTicks'];end=accounting['requestsCompletedTicks']
 check(frequency==accounting['stopwatchFrequency']==1000000000,variant+': frequency differs')
 check(len(rows)==4000 and [x[0] for x in rows]==list(range(4000)),variant+': raw offered accounting mismatch')
 check(all(row[2]-start==row[0]*500000 for row in rows),variant+': offered schedule differs from2000/s')
 good=[row for row in rows if row[7]==''];drops=[row for row in rows if row[7]=='offered.dropped'];errors=collections.Counter(row[7] for row in rows if row[7])
 check(len(good)==summary['preflight']['correct'] and len(drops)==summary['preflight']['dropped'],variant+': raw counts differ from summary')
 check(summary['state']['passed'] is True,variant+': final planned state failed')
 check(all(row[3]==row[5]==row[6]==0 for row in drops),variant+': dropped row has sent/status/body work')
 ms=lambda ticks:(ticks-start)*1000/frequency
 completes=sorted(good,key=lambda row:row[4]);gaps=sorted([(right[4]-left[4],left,right) for left,right in zip(completes,completes[1:])],key=lambda item:item[0],reverse=True)
 group_reports=[]
 for group in cluster([row[0] for row in drops]):
  first,last=rows[group[0]],rows[group[-1]]
  group_reports.append({'first_index':group[0],'last_index':group[-1],'count':len(group),'scheduled_start_ms':ms(first[2]),'scheduled_end_ms':ms(last[2]),'observed_drop_start_ms':ms(first[4]),'observed_drop_end_ms':ms(last[4]),'indexes':group})
 before,after=accounting['clientBefore'],accounting['clientAfter'];span_ms=(after['observedTicks']-before['observedTicks'])*1000/frequency
 client={'snapshot_span_ms':span_ms,'cpu_delta_ms':after['cpuMilliseconds']-before['cpuMilliseconds'],'approximate_allocated_delta_bytes':after['allocatedBytesApproximate']-before['allocatedBytesApproximate'],'gc_delta':[after['gc'+str(i)]-before['gc'+str(i)] for i in range(3)],'threadpool_threads_before':before['threadPoolThreads'],'threadpool_threads_after':after['threadPoolThreads'],'threadpool_pending_before':before['threadPoolPendingWorkItems'],'threadpool_pending_after':after['threadPoolPendingWorkItems'],'threadpool_completed_work_items_delta':after['threadPoolCompletedWorkItems']-before['threadPoolCompletedWorkItems']}
 client['cpu_ms_per_snapshot_elapsed_ms']=client['cpu_delta_ms']/span_ms
 tls=preparation['tlsConnections'];check(all(x['protocol']=='Tls13' for x in tls),variant+': observed preparation TLS not1.3')
 observation=load(directory.parent/'observation.json')
 first_manifest=[]
 with gzip.open(directory/'offered-manifest.jsonl.gz','rt',encoding='utf-8') as stream:
  for _ in range(4000):first_manifest.append(json.loads(next(stream)))
 check(all(item['index']==index and item['operation']==rows[index][1] for index,item in enumerate(first_manifest)),variant+': offered manifest differs from raw operation/index')
 actual_state_audit=None
 if variant=='engine':
  final_state=load(directory.parent/'final-state.json')
  model=[{'id':index,'label':f'item-{index:05d}','revision':0,'amountMinorUnits':index*17} for index in range(1,10001)]
  planned_writes=0
  for offered in first_manifest:
   if offered['operation']=='set':
    before=model[offered['id']-1]
    check(before['revision']==offered['expectedRevision'],'Engine planned write revision mismatch')
    model[offered['id']-1]=dict(before,label=offered['label'],revision=before['revision']+1);planned_writes+=1
  expected_hash=hashlib.sha256(json.dumps(model,separators=(',',':')).encode()).hexdigest()
  check(final_state['records']==model and final_state['stateHash']==expected_hash,'Engine final retained snapshot differs from independent preflight model')
  check(final_state['writes']==planned_writes==200 and final_state['factories']==final_state['disposals']==4093,'Engine final business counters mismatch')
  actual_state_audit={'retained_record_count':len(final_state['records']),'planned_and_actual_writes':planned_writes,'expected_and_actual_state_sha256':expected_hash,'factories':final_state['factories'],'disposals':final_state['disposals'],'reads':final_state['reads'],'snapshot_sha256':digest(directory.parent/'final-state.json'),'independent_snapshot_replay_passed':final_state['records']==model}
 in_flight=[sum(row[3]>0 and row[3]<=dropped[4]<row[4] for row in good) for dropped in drops]
 hashes={file.name:digest(file) for file in directory.iterdir() if file.is_file()}
 optional_full=directory/'load-result.json';all_tls=None
 if optional_full.exists():
  final_telemetry=load(optional_full).get('tlsConnections',[])
  all_tls=[x for x in final_telemetry if start<=x.get('connectedTicks',-1)<=end]
 reports[variant]={
  'input_directory':str(directory),'raw_offered':len(rows),'correct':len(good),'error_kinds':dict(errors),'dropped':len(drops),'successful_offered_fraction':len(good)/len(rows),'state_validation':summary['state'],'summary_preflight':summary['preflight'],
  'dropped_operation_counts':dict(collections.Counter(row[1] for row in drops)),'drop_clusters':group_reports,'all_drop_indexes':[row[0] for row in drops],
  'sent_not_completed_count_reconstructed_at_every_drop':sorted(set(in_flight)),
  'first_completion':{'index':completes[0][0],'relative_ms':ms(completes[0][4])},
  'first10_completions':[{'index':row[0],'operation':row[1],'relative_ms':ms(row[4]),'sent_relative_ms':ms(row[3])} for row in completes[:10]],
  'largest_completion_gaps':[{'gap_ms':gap*1000/frequency,'left_index':left[0],'left_relative_ms':ms(left[4]),'right_index':right[0],'right_relative_ms':ms(right[4])} for gap,left,right in gaps[:5]],
  'success_sent_to_completed_p95_ms':percentile([(row[4]-row[3])*1000/frequency for row in good],.95),
  'client_snapshots':client,'client_before':before,'client_after':after,'phase_start_ticks':start,'requests_completed_ticks':end,'frequency':frequency,
  'raw_persistence_started_after_request_join':accounting['persistenceStartedTicks']>=end,'raw_persistence_duration_ms':(accounting['persistenceCompletedTicks']-accounting['persistenceStartedTicks'])*1000/frequency,
  'preparation_requests':len(preparation['requests']),'preparation_requests_correct':all(x['error'] is None and x['status']==200 for x in preparation['requests']),
  'preparation_tls_connection_count':len(tls),'preparation_tls_protocols':sorted(set(x['protocol'] for x in tls)),
  'retained_preflight_tls_events_from_later_full_report':all_tls,
  'tls_coverage_boundary':'collector-preparation.json is a pre-phase snapshot. A failed preflight produces neither warmup nor load report, so TLS events added during this failed phase are not retained by current source.',
  'driver_exit_code':observation['driver_exit_code'],'diagnostic_status':observation['diagnostic_status'],'timed_measurement_executed':observation['timed_measurement_executed'],
  'warmup_or_measurement_raw_files_exist':any((directory/name).exists() for name in ('warmup-result.json','warmup-requests.jsonl.gz','measured-requests.jsonl.gz','load-result.json')),
  'first4000_manifest_sha256':hashlib.sha256(json.dumps(first_manifest,separators=(',',':')).encode()).hexdigest(),'independent_final_state_replay':actual_state_audit,'input_file_sha256':hashes
 }

engine,baseline=reports['engine'],reports['baseline']
check(engine['correct']==3963 and engine['dropped']==37 and engine['error_kinds']=={'offered.dropped':37},'Engine failure counts differ from supplied outcome')
check(baseline['correct']==4000 and baseline['dropped']==0,'Adjacent baseline not4000/4000')
check(engine['first4000_manifest_sha256']==baseline['first4000_manifest_sha256'],'Compared preflight logical inputs differ')
check(engine['input_file_sha256']['offered-manifest.jsonl.gz']==baseline['input_file_sha256']['offered-manifest.jsonl.gz'],'Complete offered manifest bytes differ across variants')
check(engine['driver_exit_code']==-6 and engine['timed_measurement_executed'] is False and engine['warmup_or_measurement_raw_files_exist'] is False,'Failed preflight unexpectedly entered warmup/measurement')
check(engine['raw_persistence_started_after_request_join'] is True,'Failed raw persistence overlapped requests')
observations=[
 'The failed run retained4000 unique offered records:3963 correct and37 collector-created offered.dropped errors. Every dropped row has sentTicks0,httpStatus0,bodyBytes0; these are not server rejection responses.',
 'Drops occur in two early clusters: indexes129-161 at64.5-80.5ms, then178-181 at89-90.5ms. All37 drops reconstruct128 sent-but-not-completed requests at the drop timestamp, consistent with the declared admission cap.',
 'Engine first collector-observed completion is51.688269ms; the adjacent baseline first completion is2.205244ms. A29.299844ms completion gap follows the first Engine completion. These timestamps include the client read/validation path, not only server processing.',
 'The failed Engine collector client snapshots show one additional Gen0 collection and stable4ThreadPool workers, with pending work0 at both boundaries. The baseline has no collection delta and3-to-4 workers. Boundary snapshots cannot locate the transient or attribute a cause.',
 'Identical130 read-only preparation requests succeeded in both variants, but the retained preparation TLS snapshot has4 Engine connections versus128 baseline connections. Read-only parallel requests do not guarantee128 distinct pooled connections.',
 'The failed preflight source retains the pre-phase TLS snapshot only; connection events occurring during that failure are not persisted because no warmup/load result is emitted. Missing events cannot prove that no new handshake occurred.',
 'StatePASS is consistent with all dropped operations being reads35get/2list. It validates the planned mutations, not the37 omitted reads or the whole offered-work gate.',
 'The source intentionally throws after a failed collector preflight; driver-6 and absence of warmup/measured files confirm this was not a2000req/s steady-state measurement. No retry or rate reduction was performed.'
]
hypotheses=[
 'An early client/collector continuation or scheduling pause, a GC/JIT transient, server-side work, TLS connection creation, or shared-host contention could contribute. Existing traces do not identify where between send and collector completion the delay occurred.',
 'Different prepared connection counts make connection establishment a plausible investigation target, but the missing in-phase TLS telemetry prevents a causal conclusion for this failure.',
 'The single Gen0 delta is temporally unlocalized; it is not proof of a pause at the drop cluster. ThreadPool boundary counts are not proof of starvation or its absence.'
]
result={'observed_at_utc':datetime.now(timezone.utc).isoformat(),'audit_status':'consistent_with_retained_failed_preflight' if not findings else 'findings','scope':'Read-only forensic comparison of the failed Engine HTTP2000/s collector preflight and adjacent baseline; no build, retry, workload, source change, commit or remote write.','findings':findings,'variants':reports,'observed':observations,'hypotheses_not_proven':hypotheses,'prohibited_inferences':['Do not call this an Engine2000req/s capacity limit.','Do not assign a single root cause without server/client event evidence.','Do not score failed-preflight latency as a valid steady-state performance run.','Do not substitute this diagnostic for the unchanged1000req/s main series.','Numeric main/startup/idle outcomes do not qualify the shared reference environment or unblock#3.']}
(OUTPUT/'failed-http-engine-2000-preflight03.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
text=f'''# Failed HTTP Engine diagnostic at 2,000 req/s: forensic audit

Read-only inspection of retained canonical03 evidence. No code changes, builds, timed retry, commits or remote writes.

**The failure is retained and is not an Engine capacity result.** The collector observed 4,000 offered requests: 3,963 correct and 37 `offered.dropped`. All 37 were dropped before send (`sentTicks=0`, status/body bytes=0), with 128 sent-but-not-completed requests reconstructed at every drop. The driver exited `-6` through its deliberate preflight guard; neither the 60-second warmup nor the 180-second measurement was entered.

| Observation | Adjacent baseline | Failed Engine |
| --- | ---: | ---: |
| Correct / offered |4,000 / 4,000|3,963 / 4,000|
| Collector drops |0|37|
| First observed completion |{baseline['first_completion']['relative_ms']} ms|{engine['first_completion']['relative_ms']} ms|
| Largest gap between completions |{baseline['largest_completion_gaps'][0]['gap_ms']} ms|{engine['largest_completion_gaps'][0]['gap_ms']} ms|
| Client CPU across snapshot span |{baseline['client_snapshots']['cpu_delta_ms']:.3f} ms|{engine['client_snapshots']['cpu_delta_ms']:.3f} ms|
| Client GC delta Gen0/1/2 |0/0/0|1/0/0|
| ThreadPool workers before→after |3→4|4→4|
| Pending pool work at boundaries |0→0|0→0|
| Successful read-only preparation requests |130|130|
| Connections in pre-phase TLS snapshot |128|4|
| Planned mutation state |PASS|PASS|

Drop clusters are indexes 129–161 (33 requests; scheduled 64.5–80.5 ms) and 178–181 (four requests; 89–90.5 ms). The first Engine completion appears at 51.688269 ms, followed by a 29.299844 ms completion gap. The offered scheduler continues producing the declared 0.5 ms schedule; the backlog is observed in request completion, which includes client read/validation as well as network/server time. All dropped operations are reads (35 get, two list), so the planned mutation state can pass while the offered-work gate fails.

Both variants have byte-identical complete offered manifests and identical first 4,000 logical inputs. Independent replay of the 200 planned writes matches the failed Engine run's retained 10,000-record final snapshot and state hash, with 4,093 factories/disposals balanced. Raw persistence starts after request completion; gzip did not overlap this preflight. Preparation proves successful read-only requests, rather than a fixed number of simultaneous physical connections. Four Engine connections versus 128 baseline connections is observed. New TLS events during the failed phase were not retained: the current source writes that later snapshot into warmup/load results, which are absent on preflight failure.

Possible causes include a client/collector scheduling or GC/JIT transient, server-side delay, new TLS connections, or shared-host contention. The single Gen0 delta and boundary-only pool counts do not establish when a pause occurred. There are no server phase event traces or in-phase failed-run TLS events to identify a root cause. This single two-second failed preflight cannot establish an Engine 2,000 req/s limit or replace the unchanged 1,000 req/s acceptance series. No retry, filtering, threshold or rate adjustment was used in this audit. The shared reference environment and issue #3 remain Blocked regardless of other numeric passes.

Machine-readable evidence includes all 37 exact indexes, raw timing clusters, input hashes, pool/GC/CPU counters, comparison metrics and explicit hypotheses.
'''
(OUTPUT/'failed-http-engine-2000-preflight03.md').write_text(text,encoding='utf-8',newline='\n')
print(json.dumps({'status':result['audit_status'],'findings':findings,'drops':engine['all_drop_indexes'],'client_cpu_delta_ms':engine['client_snapshots']['cpu_delta_ms'],'prepared_tls_connections':{'baseline':baseline['preparation_tls_connection_count'],'engine':engine['preparation_tls_connection_count']}}))
