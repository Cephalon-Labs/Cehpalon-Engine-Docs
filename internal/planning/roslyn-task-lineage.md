# Roslyn task lineage in the retained full generator execution

2026-11-01, Engine #20, ADR0023. One complete WSL generator-only diagnostic execution adds the TPL channel to the original byte-identical prebuilt diagnostic driver. Engine stays at `55c630fc5d4c47258a1a2b0da4a16ce8bc42b9f7`; no rebuild, product patch, CLI lane or original benchmark rerun. Original compiler concurrency, GC, options, order, primers and thresholds are preserved.

## What the new channel establishes

The same execution records 641,481 raw events and 212,495 complete managed stack samples. Raw SampleProfiler and ETLX-extracted stack records have exact PID/native-TID/timestamp multiset parity. All 2,956 stage markers match sidecars with a nonempty conditional clock intersection; all 306 main Emit identities/order match the raw row corpus. The harness verifies 270 measurements, 36 primers, 12 seeds, three preflights and 18 postflights. Sixteen positional semantic/source/registry/order fields across all306rows match the previous corpus; timing and complete PE hashes are explicitly excluded from that comparison.

There are19,527 observed TPL schedule/start/completion execution-event histories,2,372 paired waits and65,697 totalTPLrecords (including continuation-complete events). Exact observed event versions match the pinned contract. The assembler reports zero malformed/poisoned histories or unfinished waits in this execution; this is not universal task coverage. EventPipe/ETLX loss, payload errors, truncated/empty stacks and provider errors are zero as reported/checked.

| Scope | Emit rows | Distinct caller waits in Emit | Waits with a caller WaitForWorkers point | Those waits with compiler-task point context |
|---|---:|---:|---:|---:|
| Primers |36|264|68|64|
| Measurements |270|1,913|527|486|

All2177selectedrowwaitassociations are distinct and lie wholly inside guaranteed Emit cores. The selected waits contain3,126distinct caller points and2,947distinct compiler points; measurement-only compiler points are2,573. Each measured row has at least one such context association. All candidate sets are retained: none of these selected data have multiple containing task/wait scopes, but fixtures prove that nested/inline ambiguity stays explicit. A single observed proc birth is descriptive partial sampling; **native lifetime proof remains false**. New tools use zero-based raw and stack record indices.

An explicit TPL awaitedTaskID joins a caller wait event to that task's execution native headers in this same process. A compiler-plus-ThreadPool frame sampled inside that execution and wait is a method-context co-observation. It does not prove the exact directly awaited WaitForWorkers callsite, permanent ownership of a ThreadPool thread, CPU/runnable state or why progress was delayed. Every output keeps direct_waitforworkers_callsite_proven=false, blocked_time/scheduler_delay=null. Missing points remain unknown.

The pinned [Roslyn MethodCompiler source](https://github.com/dotnet/roslyn/blob/8edf7bcd4f1594c3d68a6a567469f41dbd33dd1b/src/Compilers/CSharp/Portable/Compiler/MethodCompiler.cs) supports task-based fork/join and possible inline execution; the [exact TPL source](https://github.com/dotnet/dotnet/blob/5254d8bcf59917edc1e1abc33bdf2442b77b1c70/src/runtime/src/libraries/System.Private.CoreLib/src/System/Threading/Tasks/TplEventSource.cs) distinguishes task execution/wait events. Destination and ambient-origin scheduler identities remain separate. Execution-complete telemetry is not unconditional logical Task.IsCompleted proof for attached-child paths.

## Verification and retained attempts

The new runner's10focused guards pass on Windows and WSL; the analyzer's69adverse fixtures pass on both. Final independent replay audit passes1,262,459checks with zero failures, including full raw/sample/marker/row/point/task candidate verification. All capture source/binding checks and211binary hashes remained unchanged before/after. Frozen loaded function code/source is observational provenance, not immutable attestation of globals/defaults/imports or filesystem behavior.

Only one workload target was captured; there was no failed capture or favorable rerun. Offline analysis versions/replays and fixture-preparation attempts remain retained. Type guards, clock bounds and native-birth wording were strengthened before final replay; no new target was launched for those corrections. Lossless deterministic compression and staged-byte hash verification cover every retained payload. Existing prebuilt driver and preparation/build provenance remain available from the earlier wait evidence; the new manifest records their exact hashes.

## Limits and next evidence

There is no native syscall tracer or kernel scheduler-transition channel in this lane. It has a different perturbation profile from earlier strace-combined captures and cannot be compared for speedup, overhead or variance. No exclusive GC/scheduler percentage, worker starvation or avoidable Engine work is established. Legacy GC interpretation remains unaccepted; this parser's78GC-related envelopes/70pairingerrors are retained as legacy-model observations, not certified pauses and not replacements for prior23/21/83study.

Next bounded analysis can examine schedule/start/wait event ordering for the linked TaskIDs, preserving literal event observations rather than labeling queue/run/block durations. Actual runnable-to-running causality still needs separately established scheduler access, transition completeness, native identity and clocks; GC acceptance still needs applicable caller/build/binary evidence. Do not change global host permissions or rerun the unchanged original benchmark to seek a favorable result.

#3 remains Blocked; #20 stays In Progress/P2/M0 with original dependencies #2/#11, estimates, Test/Benchmark Planned and null hours. Existing Engine CI runs40993252408/40993252420 remain pre-step payment/spending rejections; no rerun or billing action. No provider, supported-Windows, production, reference or release qualification follows.

[ADR0023](../adr/ADR-0023-roslyn-task-lineage-diagnostics.md), [delivery evidence](../evidence/roslyn-task-lineage/delivery.json), Samples retention: `tooling-traces/evidence/2026-11-01-roslyn-task-lineage/retention.json`.
