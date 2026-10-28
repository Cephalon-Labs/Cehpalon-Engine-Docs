"""Run after audit-functional03.py; verify committed build inputs and render readable scope."""
from pathlib import Path
import hashlib
import json
import subprocess

OUTPUT=Path(__file__).resolve().parent
SAMPLES=Path('D:/Cephalon/Cehpalon-Engine-Samples')
path=OUTPUT/'functional-evidence-audit03.json'
result=json.loads(path.read_text())
for host,report in result['hosts'].items():
 root=Path(report['evidence_root']);manifest=json.loads((root.parent/'manifest.json').read_text())
 for name,expected in manifest['source_sha256'].items():
  blob=subprocess.check_output(['git','show',manifest['samples_source_revision']+':'+name],cwd=SAMPLES)
  assert hashlib.sha256(blob).hexdigest()==expected,(host,name)
 report['exact_source_build_provenance']={'samples_source_revision':manifest['samples_source_revision'],'engine_revision':manifest['engine_revision'],'source_state':manifest['source_state'],'sdk':manifest['sdk'],'assembly_sha256':manifest['assembly_sha256'],'committed_input_hashes_verified':len(manifest['source_sha256']),'actual_stopwatch_frequency':json.loads((root/'predeclared.json').read_text())['stopwatchFrequency']}
path.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
lines=['# Canonical03 functional conformance audit','',
 'Read-only audit of the final tuning Windows/Linux conformance evidence. No builds, test reruns, measurements, source changes, commits or remote writes.','',
 '**No runtime evidence findings within the audited scope.**','',
 '| Host | Corpus executions | Included cancellations | Maximum recorded ACK | Maximum raw ACK | Repeat lifecycle cycles | Maximum shutdown | API-only exercise |',
 '| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |']
for host,report in result['hosts'].items():
 lines.append(f'| {host} |4,000|400|{report["maximum_server_ack_after_abort_ms"]} ms|{report["maximum_server_ack_after_abort_raw_tick_reconstruction_ms"]} ms|120|{report["maximum_repeat_shutdown_ms"]} ms|20,000 requests|')
lines += ['',
 'All four lanes per host retain exactly indexes 0–999 without omissions or duplicates, with the same frozen corpus and initial 10,000-record dataset. Recorded statuses and business codes match that manifest. Independent expected-model replay produces its declared final-state hash. Both exact-source build manifests match all 13 committed input hashes. The new headers retain actual Stopwatch frequencies: 10 MHz Windows and 1 GHz Linux; no frequency inference is needed.', '',
 'All 400 cancellation records per host have delayed-handler entry before client abort, no abort before the declared 50 ms boundary, acknowledgement under the unchanged 100 ms limit, completed ownership and no-mutation flags. Raw intervals also pass 100 ms; only representation comparison uses a 0.00011 ms tolerance for the recorded 100 ns TimeSpan fields. All 30 repeat cycles per lane meet the unchanged five-second shutdown limit and balance disposal. API-only GraphQL factory/service/diagnostic/executor/schema probes are zero, with positive controls for enabled profiles.', '',
 'Proof boundaries:', '',
 '- Cancellations are included within the 4,000 executions per host, not 400 additional executions.',
 '- The running harness checked response-body equality and actual final store state. Raw case rows retain status/code/assertion outcomes rather than every response body or final snapshot; independent replay here verifies the frozen expected model.',
 '- The 20,000 API-only requests per host are supported by deterministic source loops and completed checks rather than individual retained response rows.',
 '- The 120 repeat host lifecycles per host are same-process cycles. Fresh-process startup measurements are separate.',
 '- Invalid/all-off/cycle checks here are pure compiler preflight, not execution of this public host with invalid/all-off configuration.',
 '- The public synthetic fixture uses a fixed server-owned public identity. It establishes no tenant, JWT/real IdP, provider, database or production isolation. Unimplemented-provider traps do not qualify providers.',
 '- Windows26H2 remains observational; WSL is not native deployment proof. This audit does not unblock #3 or qualify the shared performance reference environment.', '',
 'The machine-readable report includes source/evidence hashes, per-lane counts, actual clock frequencies, timing maxima and ownership/probe details.']
(OUTPUT/'functional-evidence-audit03.md').write_text('\n'.join(lines)+'\n',encoding='utf-8',newline='\n')
print('Committed build-input hashes and readable functional audit finalized')
