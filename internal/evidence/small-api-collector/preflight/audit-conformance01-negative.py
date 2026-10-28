"""Retain the complete01 conformance outcome; no build/rerun/request/timing."""
from pathlib import Path
from datetime import datetime,timezone
import json

BASE=Path('D:/Cephalon/Cehpalon-Engine-Samples/.local')
OUT=Path(__file__).resolve().parent
reports={}
for host in ('win','linux'):
 root=BASE/f'collector-conformance-{host}-01';manifest=json.loads((root/'manifest.json').read_text());conformance=root/'conformance';summary=json.loads((conformance/'summary.json').read_text());declaration=json.loads((conformance/'predeclared.json').read_text());frequency=declaration['stopwatchFrequency']
 lane_counts=[];failed_rows=[]
 for variant in ('baseline','engine'):
  for transport in ('http','graphql'):
   lane=variant+'-'+transport;rows=json.loads((conformance/lane/'case-results.json').read_text());cycles=json.loads((conformance/lane/'lifecycle-cycles.json').read_text())
   lane_counts.append({'lane':lane,'corpus_rows':len(rows),'cancel_rows':sum(x['expectedCode']=='operation.cancelled' for x in rows),'failed_rows':sum(not x['passed'] for x in rows),'repeat_lifecycle_rows':len(cycles)})
   for row in rows:
    if not row['passed']:failed_rows.append({'lane':lane,'record':row,'handler_entry_relative_to_abort_ms':(row['handlerEnteredTimestamp']-row['actualAbortTimestamp'])*1000/frequency if 'handlerEnteredTimestamp'in row else None})
 reports[host]={'root':str(root),'manifest_status':manifest['status'],'summary_status':summary['status'],'summary_failed':summary['failed'],'samples_source_revision':manifest['samples_source_revision'],'source_inputs_declared':len(manifest['source_sha256']),'stopwatch_frequency':frequency,'lanes':lane_counts,'failed_rows':failed_rows}
assert reports['win']['summary_status']=='failed' and reports['win']['summary_failed']==1
assert reports['linux']['summary_status']=='passed' and reports['linux']['summary_failed']==0
failure=reports['win']['failed_rows'][0];row=failure['record']
assert failure['lane']=='baseline-http' and row['index']==409 and row['actualAbortTimestamp']==1962827142176 and row['handlerEnteredTimestamp']==1962827145558
result={'observed_at_utc':datetime.now(timezone.utc).isoformat(),'status':'negative_outcome_confirmed','reports':reports,'interpretation':'Windows01 does not pass the in-flight cancellation criterion: the handler entered0.3382ms after abort. Acknowledgement0.5528ms, no mutation and joined ownership do not repair that missing in-flight condition. Linux01 passed, but the full two-host01set has a retained negative outcome.','repeat_policy':'Root declared a complete sequential Windows02 thenLinux02 repeat on unchangedsource/criteria, with no concurrent builds/audits/hash work. Retain both01hosts; do not replace or select only the failed case.','causality_boundary':'Root reports concurrent conformance and metadata/staging work; interference is possible, not established as the cause. No code bug, supported-Windows pass, provider proof or #3 unblock inferred.','staging_boundary':'Independent native app/SDK byte/link audit passed separately; staging identity does not make failed conformance pass.'}
(OUT/'conformance01-negative.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
text=f'''# Retained conformance01 negative outcome

Windows01 completed all4,000 corpus executions (including400 cancellation cases) and120 repeated host lifecycles, but one case failed. Linux01 completed the same matrix with zero failures. These complete results remain retained.

Windows baseline-http case409:

- Actual client abort tick:1962827142176.
- Handler entry tick:1962827145558, **0.3382ms after abort** at the recorded10MHz clock.
- Server acknowledgement: {row['serverAckAfterAbortMilliseconds']}ms after abort.
- No-mutation flag: {row['noMutationAfterAck']}; owned handler completed: {row['ownedHandlerCompleted']}.

The acknowledgement and cleanup outcomes do not satisfy the missing handler-entered-before-abort condition. Windows01 therefore does not pass the declared in-flight cancellation criterion. The exact source remains unchanged.

Root reports simultaneous two-host conformance and metadata/staging work. Interference is possible, but is not proven as the cause. Root predeclared a complete sequential Windows02 thenLinux02 repeat with unchanged criteria and no concurrent builds/audits/hash work. Neither01host may be discarded, and no single-case favorable replacement is allowed. A staging identity pass does not promote conformance, platform or #3 status.

This audit issued no build, test, request or timing. Its activity stops before the sequential repeat begins.
'''
(OUT/'conformance01-negative.md').write_text(text,encoding='utf-8',newline='\n')
print(json.dumps({'status':result['status'],'windows_failure_index':row['index'],'entry_after_abort_ms':failure['handler_entry_relative_to_abort_ms'],'ack_after_abort_ms':row['serverAckAfterAbortMilliseconds'],'linux_status':reports['linux']['summary_status']}))
