"""Read-only source/build provenance and conformance synthesis after the declared repeat."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,subprocess

OUT=Path(__file__).resolve().parent
SAMPLES=Path('D:/Cephalon/Cehpalon-Engine-Samples')
functional=json.loads((OUT/'functional-sequential02-audit.json').read_text())
staging=json.loads((OUT/'staging-audit02.json').read_text())
negative=json.loads((OUT/'conformance01-negative.json').read_text())
expected='a3bd8b5c5747440c81124774ac10b6451d88ff82'
findings=list(functional['findings'])+list(staging['findings']);builds={}
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
for host,short in [('windows','win'),('linux','linux')]:
 root=SAMPLES/'.local'/f'collector-conformance-{short}-02';manifest=json.loads((root/'manifest.json').read_text());summary=json.loads((root/'conformance/summary.json').read_text())
 assert manifest['samples_source_revision']==expected and manifest['source_state']=='exact clean committed source' and manifest['status']=='passed'
 assert len(manifest['source_sha256'])==15
 for name,digest in manifest['source_sha256'].items():
  content=subprocess.check_output(['git','show',expected+':'+name],cwd=SAMPLES)
  assert hashlib.sha256(content).hexdigest()==digest,(host,name)
 assembly=root/'artifacts/bin/SmallApi.Benchmark/release/SmallApi.Benchmark.dll'
 assert sha(assembly)==manifest['assembly_sha256']
 deps=json.loads(assembly.with_suffix('.deps.json').read_text());libraries=sorted(deps['libraries'])
 assert libraries==manifest['runtime_libraries']
 assert not any(any(word in name.lower() for word in ('codeanalysis','codegeneration')) for name in libraries)
 registry=root/'OperationRegistrations.g.cs.txt';text=registry.read_text();assert sha(registry)==manifest['generated_registry_sha256']
 operations=re.findall(r'"(catalog\.(?:get|list|set))"',text)
 assert sorted(operations)==['catalog.get','catalog.list','catalog.set'] and text.count('.Register<')==3
 builds[host]={'samples_source_revision':expected,'engine_revision':manifest['engine_revision'],'status':manifest['status'],'committed_input_hashes_verified':len(manifest['source_sha256']),'source_sha256':manifest['source_sha256'],'assembly_sha256':manifest['assembly_sha256'],'generated_registry_sha256':manifest['generated_registry_sha256'],'generated_registration_count':3,'generated_operation_ids':operations,'runtime_libraries':libraries,'compiler_only_runtime_graph_absent':True,'manifest_sha256':sha(root/'manifest.json'),'execution_started_at_utc':manifest['observed_at_utc'],'execution_completed_at_utc':summary['observedAtUtc'],'actual_stopwatch_frequency':json.loads((root/'conformance/predeclared.json').read_text())['stopwatchFrequency']}
assert builds['windows']['source_sha256']==builds['linux']['source_sha256']
parse=lambda value:datetime.fromisoformat(value.replace('Z','+00:00'))
assert parse(builds['linux']['execution_started_at_utc'])>=parse(builds['windows']['execution_completed_at_utc'])
assert staging['samples_source_revision']==expected and staging['app_assembly_sha256']==builds['linux']['assembly_sha256']
assert negative['reports']['win']['summary_status']=='failed' and negative['reports']['win']['summary_failed']==1
assert (SAMPLES/'.local/collector-conformance-win-01/conformance/baseline-http/case-results.json').is_file()
assert (SAMPLES/'.local/collector-conformance-linux-01/conformance/summary.json').is_file()
result={'observed_at_utc':datetime.now(timezone.utc).isoformat(),'status':'passed_with_retained_prior_negative_and_limits' if not findings else 'findings','findings':findings,'builds':builds,'sequential02_host_execution_nonoverlap_in_recorded_times':True,'functional':functional,'native_staging':staging,'retained01_negative_reference':str(OUT/'conformance01-negative.json'),'prior01_negative_summary':{'windows_failure':'baseline-http409 handler entry0.3382ms after abort; ACK0.5528ms/noMutation/owned completion do not satisfy in-flight condition','linux01':'passed','kept_separate':True},'repeat_boundary':'Complete sequential Windows02 thenLinux02 on unchangedsource/criteria, predeclared by root; no selective case substitution or inference that parallel activity caused01failure. Both01hosts remain retained.','qualification_boundary':'Public synthetic fixture; no real tenant/IdP/provider, reserved2CPU/2GiB, supported-Windows or native deployment qualification. Staging hashes establish bytes/link identity, not which module a future process actually loads. #3 remainsBlocked.','audit_activity':'Read-only local Git/file/JSON/hash analysis only; no SDK/runtime execution, builds, test reruns, network requests, benchmarks, commits or remote writes.'}
(OUT/'sequential02-precanonical-audit.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
w,l=functional['hosts']['windows'],functional['hosts']['linux']
lines=['# Sequential02 precanonical audit','',
 '**The complete sequential02 conformance matrix passes within its declared scope. The Windows01 negative outcome remains retained separately.**','',
 '| Host | Corpus executions | Included cancellations | Maximum recorded ACK | Maximum raw ACK | Repeat host cycles | Maximum shutdown | API-only exercise |',
 '| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
for host,row in functional['hosts'].items():lines.append(f'| {host} |4,000|400|{row["maximum_server_ack_after_abort_ms"]} ms|{row["maximum_server_ack_after_abort_raw_tick_reconstruction_ms"]} ms|120|{row["maximum_repeat_shutdown_ms"]} ms|20,000 requests|')
lines += ['',
 'Both hosts used source `a3bd8b5c5747440c81124774ac10b6451d88ff82`. All **15 input hashes per host** match the frozen Git blobs. Actual DLL hashes match the manifests; the emitted registry contains exactly the three catalog operations, and actual runtime dependency graphs contain no Roslyn/CodeGeneration library. Recorded execution times confirm Windows02 completed before Linux02 began.','',
 'Every lane contains indexes0–999 exactly once and the same frozen dataset/corpus. Independent expected-model replay matches the declared final hash. All cancellation records meet handler-before-abort, no early abort, raw and recorded acknowledgement under100ms, joined ownership and no-mutation assertions. Actual clock frequencies come from headers, not inference. Lifecycle rows balance factory/disposal and meet5seconds. API-only probes are zero; enabled GraphQL has positive lifecycle controls.','',
 f'Fresh native app-final-02: all **{staging["app_regular_files"]} files /{staging["app_bytes"]:,} bytes** were independently hashed against the clean Linux02 artifact tree and staging manifest. Its assembly hash is `{staging["app_assembly_sha256"]}`. All **4,178 native SDK files /549,400,671 bytes** and **1,668 symlink targets** were independently checked against bound staging manifests, with only the predeclared separator/normpath representation translation. No SDK was executed by the audit.','',
 'Retained prior outcome: Windows01 baseline-http409 entered the delayed handler0.3382ms after client abort. It failed the in-flight criterion despite ACK0.5528ms and successful cleanup. Linux01 passed. Both full01 results remain; neither was replaced by a favorable individual case. Root predeclared the entire sequential02 repeat with unchanged criteria. Parallel interference remains a possibility, not an established cause.','',
 'Limits:', '',
 '- The400 cancellations per host are included in4,000 executions. Positive response bodies/final live store hashes were checked by the running harness; raw case rows retain assertion/code/status rather than every response body.',
 '- The20,000 API exercise count per host derives from deterministic loops and completed checks, rather than20,000 separately retained response rows.',
 '- The120 lifecycle cycles are same-process host restarts; fresh-process startup measurement is separate. Invalid/all-off/cycle evidence here is pure compiler preflight.',
 '- Public fixture and staging identity do not establish tenant/IdP/provider, production, reserved resources, native deployment or listed-supported Windows proof. Actual runtime module mapping remains for the later process observation. #3 stays Blocked.',
 '- No audit build, test, request, timing, source change, commit or remote write was performed.', '',
 'Machine-readable report and reproducible scripts are alongside this file. Audit activity stops before the frozen12-probe timing matrix.']
(OUT/'sequential02-precanonical-audit.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
print(json.dumps({'status':result['status'],'source_inputs_per_host':15,'generated_operations_per_host':3,'counts':functional['totals'],'max_ack_ms':{name:row['maximum_server_ack_after_abort_ms'] for name,row in functional['hosts'].items()},'staging_app_files':67,'sdk_files':4178,'sdk_links':1668,'retained01_negative':True}))
