"""Read-only post-run host/fairness audit. Never inspect dump/private-key bodies."""
from pathlib import Path
import collections
import datetime
import hashlib
import json
import os
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path('/mnt/d/Cephalon/Cehpalon-Engine-Samples')
ENGINE = Path('/mnt/d/Cephalon/Cehpalon-Engine')
OUT = Path('/mnt/d/Cephalon/.worktrees/w2-collector-probe/.local')
ATTEMPT = Path('/home/tom/.local/share/cehpalon-benchmark-runs/benchmark-observation-04')
sys.path.insert(0, str(ROOT / 'tools'))
from small_api_collector_evidence import validate_collector_preparation, validate_phase_telemetry

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def git_bytes(repo, revision, name):
    return subprocess.check_output(['git', 'show', revision + ':' + name], cwd=repo)

manifest = read(ATTEMPT / 'manifest.json')
summary = read(ATTEMPT / 'summary.json')
assert manifest['status'] == 'observations-complete'
revision = manifest['samples_revision']
assert revision == 'a3bd8b5c5747440c81124774ac10b6451d88ff82'
assert manifest['engine_revision'] == '6804271d429106864e01e4ec546a41dff771f84b'
for relative, digest in manifest['source_sha256'].items():
    prefix, name = relative.split('/', 1)
    repo, ref = (ROOT, revision) if prefix == 'samples' else (ENGINE, manifest['engine_revision'])
    assert hashlib.sha256(git_bytes(repo, ref, name)).hexdigest() == digest, relative

app_staging = read(ROOT / '.local/collector-final-app-staging-02.json')
sdk_staging = read(ROOT / '.local/startup-layout-sdk-staging.json')
app, sdk = Path(app_staging['target']), Path(sdk_staging['target'])
assert str(app) == manifest['deployment']['assembly_directory'] == manifest['deployment']['server_working_directory']
assert str(sdk / 'dotnet') == manifest['deployment']['dotnet']
assert manifest['assembly'] == str(app / 'SmallApi.Benchmark.dll')
assert manifest['assembly_sha256'] == app_staging['assembly_sha256'] == '742451b86f81c439938d93aad19a0f568133fe9ff2910bae4458f6633cdcfdd4'
approved = set()
for item in app_staging['files']:
    name = item['path']
    assert not ({'evidence'} & set(Path(name).parts)) and Path(name).suffix not in ('.pfx', '.dmp') and Path(name).name != 'core'
    file = app / name
    assert file.stat().st_size == item['bytes'] and sha(file) == item['sha256'], name
    approved.add(name)
assert len(approved) == 67
assert sha(app / 'SmallApi.Benchmark.deps.json') == manifest['deps_sha256']
assert sha(app / 'SmallApi.Benchmark.dll') == manifest['assembly_sha256']
deps = read(app / 'SmallApi.Benchmark.deps.json')
assert not any(any(word in name.lower() for word in ('codeanalysis', 'codegeneration')) for name in deps['libraries'])

builds = []
for platform in ('win', 'linux'):
    build = read(ROOT / f'.local/collector-conformance-{platform}-02/manifest.json')
    assert build['status'] == 'passed' and build['source_state'] == 'exact clean committed source' and build['samples_source_revision'] == revision
    for name, digest in build['source_sha256'].items():
        assert hashlib.sha256(git_bytes(ROOT, revision, name)).hexdigest() == digest, (platform, name)
    assert build['conformance']['failed'] == 0
    builds.append(build)
assert builds[0]['source_sha256'] == builds[1]['source_sha256']
assert builds[1]['assembly_sha256'] == manifest['assembly_sha256']

ready_files = list(ATTEMPT.rglob('ready.json'))
assert len(ready_files) == 172
counts = collections.Counter()
runtime_paths = set()
first_response_ciphers = collections.Counter()
for ready_path in ready_files:
    directory = ready_path.parent
    kind = directory.relative_to(ATTEMPT).parts[0]
    counts[kind] += 1
    ready = read(ready_path)
    state = read(directory / 'final-state.json')
    shutdown = read(directory / 'shutdown.json')
    loaded = read(directory / 'loaded-runtime.json')
    command = read(directory / 'invocation.json')['command']
    first = read(directory / 'first-response.json')
    assert command[:3] == ['taskset', '--cpu-list', '0,2']
    assert command[3] == str(sdk / 'dotnet') and command[4] == str(app / 'SmallApi.Benchmark.dll')
    assert not any(arg.startswith('--startup-trace=') for arg in command)
    variant = next(arg.split('=', 1)[1] for arg in command if arg.startswith('--variant='))
    transport = next(arg.split('=', 1)[1] for arg in command if arg.startswith('--transport='))
    assert ready['variant'] == state['variant'] == variant and ready['transport'] == state['transport'] == transport
    assert loaded['process_id'] == ready['processId'] and loaded['inspection_after_first_response']
    assert len(loaded['paths']) == 4 and all(path.startswith(str(sdk / 'shared') + '/') for path in loaded['paths'])
    runtime_paths.update(loaded['paths'])
    assert ready['tlsProtocol'] == 'Tls13' and ready['datasetId'] == 'cehpalon-small-api-v1'
    import base64
    assert hashlib.sha256(base64.b64decode(ready['rootCaDerBase64'])).hexdigest() == manifest['public_ca_sha256']
    assert first['http_status'] == 200 and first['tls_protocol'] == 'TLSv1.3'
    first_response_ciphers[first['tls_cipher'][0]] += 1
    assert len(state['records']) == 10000 and state['factories'] == state['constructors'] == state['disposals']
    probes = state['probes']
    assert probes['forbiddenFactories'] == 0
    if transport == 'http':
        assert all(probes[key] == 0 for key in ('graphQLFactories', 'graphQLServices', 'graphQLDiagnosticConstructors', 'graphQLExecutorInitializations', 'graphQLSchemasReady'))
    else:
        assert probes['graphQLExecutorInitializations'] == probes['graphQLSchemasReady'] == 1
    assert all(shutdown[key] for key in ('graceful', 'listener_closed', 'owned_handlers_balanced', 'disabled_probes_zero', 'passed'))
    assert shutdown['exit_code'] == 0 and shutdown['elapsed_ms'] <= 5000
assert counts == {'startup': 120, 'idle': 20, 'load': 20, 'diagnostics': 12}
sdk_files = {item['path']: item for item in sdk_staging['files']}
for path in runtime_paths | {str(sdk / 'dotnet'), str(sdk / 'host/fxr/11.0.0-rc.3.26522.148/libhostfxr.so')}:
    relative = str(Path(path).relative_to(sdk))
    assert sha(path) == sdk_files[relative]['sha256']

preparations = list(ATTEMPT.rglob('collector-preparation.json'))
assert len(preparations) == 52
physical = {}
phase_count = measured_brackets = 0
new_phase_tls_events = 0
post_phase_control_connections = 0
for file in preparations:
    directory = file.parent
    preparation = validate_collector_preparation(directory)
    assert len(preparation['tlsConnections']) == 129
    assert collections.Counter(item['pool'] for item in preparation['tlsConnections']) == {'control': 1, 'load': 128}
    for event in preparation['tlsConnections']:
        key = (str(directory.relative_to(ATTEMPT)), event['connectionId'])
        physical[key] = event
    phases = [path.name.removesuffix('-evidence-accounting.json') for path in directory.glob('*-evidence-accounting.json')]
    for phase in phases:
        report = validate_phase_telemetry(directory, phase)
        phase_count += 1
        new_phase_tls_events += len(report['newTlsConnectionIds'])
        if phase == 'measured':
            measured_brackets += 1
        for field in ('tlsConnectionsBefore', 'tlsConnectionsAfter'):
            for event in report[field]:
                key = (str(directory.relative_to(ATTEMPT)), event['connectionId'])
                assert key not in physical or physical[key] == event
                physical[key] = event
    result_path = directory / ('warmup-result.json' if (directory / 'warmup-result.json').exists() else 'load-result.json')
    result = read(result_path)
    if result_path.name == 'load-result.json':
        measured_accounting = read(directory / 'measured-evidence-accounting.json')
        after_ids = {event['connectionId'] for event in measured_accounting['tlsConnectionsAfter']}
        extras = [event for event in result['tlsConnections'] if event['connectionId'] not in after_ids]
        for event in extras:
            assert event['pool'] == 'control'
            assert measured_accounting['completionMetricsStartedTicks'] <= event['connectedTicks'] <= measured_accounting['completionMetricsCompletedTicks']
        post_phase_control_connections += len(extras)
    for event in result['tlsConnections']:
        key = (str(directory.relative_to(ATTEMPT)), event['connectionId'])
        assert key not in physical or physical[key] == event
        physical[key] = event
    assert not (directory / 'collector-failure.json').exists()
assert phase_count == 136 and measured_brackets == 32
pool_counts = collections.Counter(event['pool'] for event in physical.values())
cipher_counts = collections.Counter(event['cipher'] for event in physical.values())
assert all(event['protocol'] == 'Tls13' and event['httpVersion'] == '1.1' for event in physical.values())

owned_children = []
for item in Path('/proc').iterdir():
    if not item.name.isdecimal():
        continue
    try:
        args = (item / 'cmdline').read_bytes().split(b'\0')
    except OSError:
        continue
    if args and args[0].endswith(b'/dotnet') and any(b'SmallApi.Benchmark.dll' in arg for arg in args):
        owned_children.append(int(item.name))
assert not owned_children
extra_metadata = []
for item in app.iterdir():
    if item.name not in approved:
        extra_metadata.append({'path': str(item), 'bytes': item.stat().st_size, 'contents_read': False, 'copied': False})
report = {
    'observed_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status': 'passed', 'scope': 'Read-only host/fairness/runtime/physical-preparation metadata audit; no workloads, tests, builds or remote writes',
    'samples_revision': revision, 'engine_revision': manifest['engine_revision'],
    'frozen_source_hashes_verified': len(manifest['source_sha256']), 'source_inputs_per_conformance_host': len(builds[0]['source_sha256']),
    'app_files_verified': len(approved), 'evidence_or_compiler_libraries_in_runtime': False,
    'assembly_sha256': manifest['assembly_sha256'], 'server_groups': dict(counts),
    'all172_identity_runtime_lifetime_probes_verified': True, 'startup_trace_enabled_runs': 0,
    'runtime_mapped_modules_verified': sorted(runtime_paths), 'first_response_tls_ciphers': dict(first_response_ciphers),
    'physical_preparation_reports': len(preparations), 'each_preparation_physical_tls_scope': {'control': 1, 'load_held': 128},
    'held_response_semantics': '128 HTTP1.1 nonempty body leases with distinct first-use load TLS IDs, all headers before common release, body reads after release; all130 read preparations successful under shared30s deadline.',
    'phase_telemetry_reports_verified': phase_count, 'measured_server_metrics_after_join_before_persistence_brackets': measured_brackets,
    'new_tls_identity_events_across_phases': new_phase_tls_events,
    'new_control_tls_connections_during_postjoin_completion_metrics': post_phase_control_connections,
    'deduplicated_physical_driver_tls_connections': len(physical), 'deduplication_key': 'driver output directory plus connectionId; repeated preparation/phase/result snapshots counted once',
    'deduplicated_tls_pool_counts': dict(pool_counts), 'deduplicated_actual_tls_ciphers': dict(cipher_counts),
    'owned_benchmark_dotnet_children_remaining': owned_children,
    'unexpected_app_entries_metadata_only': extra_metadata,
    'numeric_budget_observations_passed': summary['numeric_budget_observations_passed'], 'reference_gate_passed': summary['reference_gate_passed'],
    'fairness_limits': [
        'Prepared connection identity history is not proof all connections remain alive indefinitely; the simultaneous held-response barrier is the observed readiness point.',
        'Baseline and Engine share one binary/package graph, representation types, handlers and pure fixture scaffolding; baseline bypasses Core dispatch/generated registration and Composition activation.',
        'Per-process loaded-runtime records verify four native SDK modules, not independent historical cwd/app mappings; configured cwd and app invocation/artifact hashes provide that provenance.',
        'Server allocation/CPU metrics bracket joined requests before raw persistence, but matching control/client instrumentation overhead is not zero.',
        'Public synthetic fixed-principal fixture does not establish protected tenant/IdP/provider proof.',
        'Shared WSL/nonreserved affinity/no2GiBcap remains nonqualifying; #3 stays Blocked regardless numeric outcomes.',
        'Power/sleep launcher release is independently checked by the primary integrator, not rerun here.',
    ],
    'audit_transport_failure': 'Initial Windows UNC metadata lookup failed with WinError121 after workloads had finished; native WSL reads succeeded. This is not a workload/code/benchmark failure.',
}
assert report['numeric_budget_observations_passed'] is True and report['reference_gate_passed'] is False
(OUT / 'canonical04-host-fairness-audit.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, indent=2))
