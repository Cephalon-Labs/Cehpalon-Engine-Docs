# Scheduler collection readiness after worker-context analysis

2026-11-02, Engine #20, ADR0026. Engine stays at `55c630fc5d4c47258a1a2b0da4a16ce8bc42b9f7`. ADR0023-25 already narrow task and managed-stack context; more sparse-point categories will not supply missing scheduler transitions. This wave refreshes access/ABI evidence and prepares a concrete collection specification. No workload, active capture, benchmark, installation, mount, permission/sysctl/global tracing change or Engine patch occurred.

## Current host observations

Forty retained read-only commands confirm WSL kernel/perf6.18.54.1. Ordinary tom/UID1000 still receives Permission denied reading scheduler formats; capabilities remain zero and perf_event_paranoid=2. The existing Windows-owner one-shot `wsl --user root` path reads the eight formats successfully. Root file visibility is a planning candidate, not a successful perf_event_open, delivery, clock, loss or cleanup result. No capture is authorized by a readiness flag; every generated plan keeps active_capture_ready=false.

| Event | Observed ID | Payload fields used for static target filtering |
|---|---:|---|
| sched_switch |268|prev_pid OR next_pid|
| sched_waking |271|pid|
| sched_wakeup |270|pid|
| sched_wakeup_new |269|pid|
| sched_migrate_task |267|pid|
| sched_process_fork |262|parent_pid OR child_pid|
| sched_process_exit |265|pid|
| sched_process_free |266|pid|

Exact format stdout bytes, sizes, hashes, IDs, field layouts and print formats remain in the retained bundle. Earlier informal wakeup/new ID ordering was corrected against actual bundle; retained raw formats are authoritative. The existing global trace_clock remains local and tracer nop; neither was modified. A per-session CLOCK_MONOTONIC request must later be validated from actual attributes and actor marker brackets.

## Concrete review-only plan

Samples `tools/plan_scheduler_conformance.py` strictly parses every ABI/header line; rejects malformed/duplicate/zero-size/overlapping fields, unsupported signed-state/CPU/PID layouts, duplicate JSON keys, unsafe paths/hash drift and malformed TID sets. Its 4001/4002/4003 example TIDs are fictional offline test values, not live process/owner/birth leases.

The output describes per-event FDs on every online CPU (pid=-1), with payload-side filters. common_pid identifies the emitter and cannot replace wake target fields; process-only attachment can miss remote wakeups. Source [perf security](https://docs.kernel.org/admin-guide/perf-security.html) and the [perf_event_open interface](https://man7.org/linux/man-pages/man2/perf_event_open.2.html) describe access and per-CPU semantics.

FDs must open disabled with tracepoint type/config, CLOEXEC, no inheritance and forward non-overwrite buffers. Install every filter, check acknowledgments and actor leases, then enable all FDs before releasing the ordinary-user ready barrier. Abort closes only owned FDs. Unavailable private-filter readback stays explicit and requires positive/negative delivery proof. No unfiltered enable window is acceptable. No event FD is actually opened by this planning tool.

Filtered switch/fork samples still carry unowned counterparty PID/comm, and wake headers may identify an unowned emitter. Generic perf-record synthetic/task/mmap metadata may exceed tracepoint sample filters. The proposal uses explicitly audited FD attributes, no callchains/kcore or unrequested sideband, and does not pretend payload filters erase all counterpart data.

## Required next experiment

The [owned synthetic conformance protocol](scheduler-conformance-protocol.md) is proposed, not executed. It specifies ordinary-user actors and a collector-only one-shot privileged process, frozen source, pre-arm UID/PID/TID/starttime/namespace leases, disabled-open/filter-before-enable sequencing, switch/wake/migration/state/clock/loss gates and bounded cleanup.

A sacrificial actor from the declared static set must exit while collection is still armed; otherwise exit/free delivery cannot be tested. RCU-delayed free gets a fixed post-join deadline, with missing data unknown/failure rather than a favorable retry. Kernel payload IDs must be reconciled with NSpid and collector/target PID/time namespaces before filters. Initial/final states remain unknown until supported by complete transitions. New/unleased/reused IDs are not automatically admitted. Static actor conformance does not qualify a dynamically growing Roslyn ThreadPool.

LOST records may be emitted only after buffer space returns, so an absent terminal LOST record is not a zero-loss proof. Per-buffer/event counters, drain/overrun/throttle/decoder evidence and available independent lost-read accounting must be validated; unsupported accounting remains unknown. A separately declared intentional-overflow negative case precedes any positive collection qualification. No runnable/blocked/CPU/GC duration follows from current file reads or offline filters.

## Verification and handoff

80 portable fixtures pass on Windows and WSL; 47 independent retained-host checks and 503 actual-plan ABI/filter/hash/truth checks pass. The first fixture attempt75/76 failure is retained; malformed duplicate ID-header handling was fixed. Exact failed source bytes were recovered from documented reverse edits and matched the independently recorded SHA; this is byte recovery, not immutable execution attestation. All source/probe/format/example/mutation/review attempts are retained losslessly with staged-byte verification.

#3 remains Blocked; #20 stays In Progress/P2/M0 with original dependencies, estimates, Test/Benchmark Planned and null hours. Original benchmark status/gates remain unchanged/unqualified. Engine CI40993252408/40993252420 remain payment/spending rejected before steps; no rerun/billing action. No provider, supported-Windows, reference, production or release qualification follows.

[ADR0026](../adr/ADR-0026-scheduler-collection-readiness.md), [delivery evidence](../evidence/scheduler-readiness/delivery.json), [prior worker contexts](roslyn-worker-context.md).
