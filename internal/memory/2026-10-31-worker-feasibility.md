# Worker trace feasibility handoff

User requested continuing #20 with original gates and #3 Blocked. Root integrated two bounded read-only agent reviews and a passive probe.

# Worker task lineage and scheduler trace feasibility

2026-10-31, Engine #20, ADR0021. This wave inventories capabilities and exact source contracts before any new target/capture. Engine remains `55c630fc5d4c47258a1a2b0da4a16ce8bc42b9f7`. No Engine patch, benchmark, permissions, kernel settings, billing or GC/compiler-concurrency changes.

## Correction to the previous lookup

The installed runtime revision is available in the official **dotnet/dotnet VMR**, under `src/runtime`, rather than the previously tried dotnet/runtime repository. Previous HTTP404 responses are retained as URL-specific failures; they do not establish source unavailability. The [exact threadsuspend.cpp](https://github.com/dotnet/dotnet/blob/5254d8bcf59917edc1e1abc33bdf2442b77b1c70/src/runtime/src/coreclr/vm/threadsuspend.cpp) and six related source files were retrieved with HTTP200 and content hashes. This improves source correspondence but does not attest loaded binary contents or certify the old GC model.

SuspendEE emits its begin event before acquiring the ThreadStore lock; competing initiators can therefore produce overlapping begins. SuspendEE and RestartEE are asymmetric calls, and retry/abort paths require review. These functions alone do not establish that suspend and restart must use the same initiating native TID. Preserve the legacy 23 envelopes/1,637 errors, two disputed ends and supplementary 83 hypotheses; neither model is newly accepted. Do not retroactively replace old raw outputs.

## Task lineage candidate

Exact [TplEventSource](https://github.com/dotnet/dotnet/blob/5254d8bcf59917edc1e1abc33bdf2442b77b1c70/src/runtime/src/libraries/System.Private.CoreLib/src/System/Threading/Tasks/TplEventSource.cs) exposes schedule7v1/start8/complete9v1/waitbegin10v3/waitend11. A candidate diagnostic subscription is `System.Threading.Tasks.TplEventSource:0x43:5` (Tasks, TaskTransfer, TaskStops); this is a proposal, not tested collection. Avoid activity flow/set-ID/debug keywords in the first declared experiment. Enabling the provider still updates AsyncInstrumentation defaults and adds telemetry, so perturbation must be measured.

The existing parser retains arbitrary dynamic event payloads, native header TID, IDs, versions and template metadata, but has no task assembler or ActivityID/RelatedActivityID output. Previous captures did not enable TPL, so lineage cannot be recovered retrospectively. A future implementation must use PID/process-generation, task-scheduler/task identity and lifetime consistently, reject reused/malformed/unfinished task records, and retain unknowns.

TaskAwaiter.GetResult may enter InternalWait only for an incomplete task. The synchronous wait event interval can include inline task execution or spinning as well as blocking; completed tasks may emit no wait. TaskWaitBegin/End therefore cannot be renamed blocked-worker time. Positive task lifecycle fixtures, inline/completed/exceptional paths, parent/child/continuation cases and observed loss are required before joining a Roslyn task to a worker.

## Host readiness observations

Current WSL kernel is 6.18.54.1-microsoft-standard-WSL2 with matching perf. UID1000 has zero effective/permitted/ambient capabilities; perf has no file capabilities. perf_event_paranoid=2; tracefs exists but is root-owned mode0700. Reads of sched_switch/sched_wakeup formats and available_events fail with Permission denied; empty successful perf-list output is not proof events are absent. Kernel configuration enables PERF_EVENTS/FTRACE/EVENT_TRACING/SCHED_INFO/BPF_EVENTS but CONFIG_SCHEDSTATS is not set. Do not use old zero proc values as proof of enabled delay accounting.

The reusable Samples `tools/probe_tooling_scheduler.py` performs passive file reads only and distinguishes missing, denied, unavailable and readable observations. All five requested event-format paths are denied on this host. It always leaves active collection, event delivery/loss/clock joins and causal readiness unproven, even if every format is readable. Windows inventory is not applicable to Linux scheduler tracing; this is not supported-Windows proof for #3. Twelve guards pass on Windows and WSL.

## Next executable protocol

A separately predeclared synthetic owned target should first validate TPL lifecycle emission/parser pairing and observer overhead. Kernel transition tracing additionally requires scoped host access that is not established here; do not change global perf/sysctl settings merely to obtain a run. An actual scheduler lane needs sched_switch plus wakeup/waking, fork/exit and migration coverage, stable process/TID births, loss/overrun accounting, explicit clock anchors and bounded ownership/cleanup.

Only after those gates pass should a complete unchanged diagnostic workload run in the same execution with task/scheduler/GC streams. Uncovered initial/final states, migration gaps, missing wakeups and clock uncertainty remain unknown. A separate run cannot be fused with the old capture to manufacture overlap. Original benchmark remains unchanged and unqualified; no speedup or exclusive GC/scheduler share is claimed.

[ADR0021](../adr/ADR-0021-worker-lineage-scheduler-feasibility.md), [delivery evidence](../evidence/worker-trace-feasibility/delivery.json). #3 remains Blocked; #20 metadata, dependencies, gates, estimates and null hours are preserved.
