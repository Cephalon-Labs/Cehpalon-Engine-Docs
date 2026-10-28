# Independent W2 benchmark review

Scope: read-only source/protocol/environment review for #9/#11. No workload measurement, source mutation, container start, billing change or remote write performed by this reviewer.

## Environment preflight

Observed Ubuntu22.04.5 under WSL2 Linux6.18.54.1, uid1000. Effective process/cgroup CPUs0-19;20 logical CPUs over10 reported SMT cores. Pairs0/1,2/3,...18/19 are siblings. cgroupv2 root and `/non-systemd` report unlimited `cpu.max` and `memory.max`; user cannot write the cgroup root. Memory available is a shared roughly31GiB VM. Raw read-only facts retained in `environment-preflight.txt`.

The declared W0 reference of2 dedicated vCPU/2GiB is not established by these settings. `taskset` can constrain owned processes to a CPU set but does not reserve CPUs, prevent Windows/WSL host contention, or enforce a memory limit. Docker CPU/memory controls could constrain an owned container but do not prove exclusive host CPUs. `RLIMIT_AS` is a virtual-address-space ceiling, not a2GiB RSS/cgroup memory limit. No unrelated process should be stopped or global CPU/memory settings changed to manufacture qualification.

For local observations only, app affinity0,2 and driver4,6 uses distinct reported cores and avoids placing driver on app SMT siblings. Record topology and chosen logical CPUs; never describe this as dedicated reservation. Capture throttling/steal/system load observations and preserve all invalid attempts. A local matched comparison may report results, but must retain an invalid/unqualified reference-environment classification and leave #3 Blocked.

## Frozen protocol requirements

- Same10,000-record public fixture, immutable ordered request manifest hash and expected outcomes before adapter mapping; protected20,000-record fixture remains separate.
- Native Minimal API/direct HotChocolate handler baseline with identical parsing/validation/error/cancellation/owned disposal behavior. Reusing Engine adapters would narrow the comparison and must not be called the declared bare baseline.
- HTTP and GraphQL series separate; five pairs each in BE,EB,BE,EB,BE order, warm60s, reseed/drain barrier, measured180s, open-loop1000req/s,1s timeout,128 outstanding cap. Offered requests dropped at cap remain explicit failures; delayed scheduler dispatch retains scheduled-to-completed latency.
- Writer lanes remain serialized per lane with predetermined IDs/revisions. No dynamic retries or conflict suppression. Validate acknowledged mutations and final state/record count; a successful status without semantic payload validation is insufficient.
- Startup30 fresh processes per variant, process-start through readiness plus first verified request; not in-process restarts or machine-cold claims. No build/download inside timed interval.
- Idle after startup/warmup:120s idle then60samples at1Hz, same instrumentation and RSS definition in both variants. Preserve CPU/GC/allocation observations and instrumentation limitations.
-100cancel requests/profile:5s cancellable handler delay, client abort at50ms from request start, actual monotonic abort/ack timestamps and<=100ms observation gate, no delayed write after acknowledgement. Separate handler-not-entered cases rather than claiming them as successful in-handler cancellation.
-30 cleanup cycles/profile<=5s with owned handler balance and listener closure, distinct from fresh-process startup measurement.
- No parallel agent builds/collectors/qualification while any measured run is in progress. Invalidity causes full affected protocol rerun, never selective outlier removal or relaxed thresholds.

## Source findings and final reread

Read the benchmark host/domain/native codec in `w2-samples-bench`, conformance module in `w2-samples-corpus`, and integrator `small-api-benchmark/Driver.cs` in the main Samples checkout. This reviewer did not execute their correctness or benchmark workloads; owner/integrator exact-source runs remain canonical.

Corrections requested and reread:

1. Native baseline initially used one permissive content-type reader for both protocols. It now matches strict HTTP media/charset/content-encoding behavior separately from GraphQL's vendor-compatible behavior. Shared typed validators/domain contracts remain equal, while native baseline execution does not call Engine adapter execution.
2. Full-state snapshots initially preceded allocation/CPU counter capture. Host now exposes a cheap metrics endpoint, reads metrics before large snapshot work, and leaves full snapshot verification outside the measured interval. Fixed instrumentation still needs equal placement and honest overhead disclosure.
3. Fresh processes initially generated two RSA keys and CA/leaf certificates inside startup. Host now supports generating a private ignored fixture before timing and reusing it in both variants; loading the same certificate remains part of process startup. No certificate trust-store bypass or global trust install is used.
4. The conformance timer could round down a submillisecond remaining delay and abort before its50ms target. The owner added a monotonic loop with ceil timestamp/minimum1ms delay until the declared deadline. Actual abort jitter and server acknowledgement timestamps remain retained.
5. Raw host reports initially serialized `Probes` public fields with default `IncludeFields=false`, producing empty objects. Owner reports/final source confirms `Wire.Json.IncludeFields=true`; the integrator must copy the latest source before freeze. This was an evidence serialization gap, not a business-handler defect.

Conformance source freezes independent model/data/request hashes before constructing hosts, accounts for all1000 ordered cases in each baseline/Engine × HTTP/GraphQL lane, joins server-owned handler disposal after abort, compares final catalog to a precomputed model, and separates30 in-process lifecycle cycles from fresh-process startup. Its invalid/all-off configuration checks honestly prove pure plans; actual configurable all-off benchmark host startup is not implemented. The earlier protected consumer has a separate actual all-off host proof, which must not be silently relabeled as this public profile.

Driver source uses the declared80/15/5 mix and32 serialized writer lanes, records all offered requests including cap drops, anchors timeouts to scheduled time, and retains scheduled/sent/completed observations. Its version-history label formula matches the declared lane/slot/revision algorithm; final verification independently checks all10000 keys and planned acknowledged outcomes. HTTP and GraphQL manifest hashes include wire payload hashes and therefore differ by design; equality is required for baseline/Engine within each wire. Optional logical-manifest hashing would strengthen cross-wire auditability. Exit code0 preserves complete failed-budget runs, so the orchestrator must classify report correctness/errors/drops/drain/state rather than interpreting process exit as pass.

Actual HotChocolate16.7.1 XML and a metadata-only reflection executable confirm public virtual `ExecutionDiagnosticEventListener.ExecutorCreated(string,IRequestExecutor)`. The owner now counts that real callback and a non-null observed schema, plus diagnostic-listener constructor calls. Those are actual executor/schema-ready observations; they are not an independent schema-constructor hook. `TypeInterceptor.OnAfterCreateSchemaInternal` is internal in this exact lock and cannot be overridden externally. The official [instrumentation documentation](https://chillicream.com/docs/hotchocolate/server/instrumentation) describes the supported listener registration/event model. Actual API metadata observations are retained in `.local/hc-api/result.txt`.

No remaining concrete runtime/domain/driver correctness finding was identified in the scoped source reread. Final integrated source hashes, actual conformance results, measurement validity and numeric budget outcomes remain the integrator's responsibility. Do not promote this source review into reference-environment, supported-Windows, performance or production qualification.
