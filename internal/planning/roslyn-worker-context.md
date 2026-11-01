# Awaited execution stack contexts

2026-11-01, Engine #20, ADR0025. This offline analysis reuses the complete ADR0023 trace and pinned ADR0023/0024 lineage/order artifacts. Engine remains `55c630fc5d4c47258a1a2b0da4a16ce8bc42b9f7`. No workload, build, capture, original benchmark, host permission/settings or Engine code changed.

## Observation scope

All 641,481 raw records, 63,325 copied task/wait references and 212,495 stack records are checked. The TPL model is rebuilt from raw events and equals the prior model. Raw SampleProfiler versus ETLX PID/TID/time multisets match exactly. All 2,956 markers and 306 rows/2,177 row-wait associations remain.

Global queries contain points strictly inside both an awaited task's observed execution-event window and the caller's TPL wait bracket, matching execution header native TID. Row queries additionally require strict guaranteed Emit-core interior. Exact boundary points, empty/disjoint windows and missing samples stay unassigned/unknown. All containing execution candidates remain; no innermost ownership choice. These counts do not replace ADR0023 closed-interval/cohort-specific compiler-plus-ThreadPool observations.

| Query scope | Queries | With strict points | Without strict points: unknown | Distinct points |
|---|---:|---:|---:|---:|
| All global waits |2,372|681|1,691|3,658|
| Main caller, global intersection |2,345|676|1,669|3,653|
| Nonmain waits, global intersection |27|5|22|5|
| All selected Emit row associations |2,177|624|1,553|3,100|
| Measurements, additional Emit core |1,913|547|1,366|2,706|
| Primers, additional Emit core |264|77|187|394|

The 56 global queries whose execution/wait event windows are disjoint remain explicit; they are not zero-work or zero-wait observations. No repeated point-query associations occurred in this selected data, but fixtures preserve overlapping/nested scopes and separate associations from unique points.

## Nonexclusive ANY-frame labels

The finite 42-method dictionary and namespace rules were hashed before replay. Every match preserves full frame, rule ID, catalog reference and serialized depth. A compiler ancestor can coexist with synchronization or other frames; depth is not native leaf or on-CPU state.

| Label among measured Emit-core points | Distinct points |
|---|---:|
| MethodCompiler family frame |2,604|
| Other CodeAnalysis namespace frame |2,651|
| Fallback other frame context |53|
| Dictionary managed-wait entry frame |0 observed|
| Dictionary runtime-preparation / explicit-GC request entry |0 observed|

Labels overlap; their counts must not be added or interpreted as time shares. In the full global scope one point matches WaitHandle.WaitOneNoCheck and Monitor.Enter alongside a ClsComplianceChecker frame; it is outside the selected Emit row scope. This is a managed entrypoint observation, not a blocked duration or lock-owner finding. No sampled label is not proof the corresponding behavior was absent. In particular 1,366 measured queries have no strict sample, and even a compiler frame can be present while a thread is off CPU or paused.

All 27 nonmain TPL waits are separately retained. Six same-header temporal intersections were found: five are explicitly flagged as the very same wait query, and only one is a different wait. None has a reported originating TaskID equal to the outer awaited TaskID. These are raw-header/context comparisons, not inferred causal dependencies or native-lifetime proof. All direct-callsite/native-lifetime/dependency proof flags remain false and CPU/blocked/runqueue/GC durations remain null.

## Source and verification

Exact pinned runtime sources support fast-return/async/inline paths in wait/awaiter APIs. Preparation entrypoints do not establish JIT CPU and explicit GC requests do not establish suspension. [TaskAwaiter source](https://github.com/dotnet/dotnet/blob/5254d8bcf59917edc1e1abc33bdf2442b77b1c70/src/runtime/src/libraries/System.Private.CoreLib/src/System/Runtime/CompilerServices/TaskAwaiter.cs) and the retained source manifest provide URL/status/hash provenance. A guessed Monitor source URL404 is retained as a lookup failure, not absence.

103 portable adverse fixtures pass on Windows and WSL, including generic-owner spoofing, overlapping labels, nested execution candidates, strict boundaries, empty core, no-sample and dedup cases. A separate no-production-import raw audit passes 539,519 checks: all raw references, sample multisets, complete global/row membership, candidate sets, exact frame labels/catalog/depth, native-header intersections and summaries. Root replay matches all seven agent output file hashes. Source interpretation review includes 15 classifier checks at its documented checkpoint.

All source/analysis/fixture/review attempts and the pre-replay dictionary/strict-boundary declarations are retained losslessly in Samples `tooling-traces/evidence/2026-11-01-roslyn-worker-context/retention.json`. Earlier full raw capsules are referenced by hash/revision without duplicate capture. Exact staged hashes are checked. Agents exhausted usage after preparing/running their work; root completed final replay, independent raw audit and integration.

## Decision and remaining evidence

The available samples narrow observed managed method contexts but do not determine useful work progress, physical blocking, CPU/runnable delay, GC pause or the cause of the original variance. No safe avoidable Engine work has been isolated. Scheduler attribution still requires scoped access and transition/loss/clock conformance; GC attribution requires applicable branch/build/binary evidence. A new controlled experiment must be declared separately. No unchanged-source benchmark rerun is justified by these point counts.

#3 remains Blocked; #20 stays In Progress/P2/M0 with original dependencies, estimates, Test/Benchmark Planned and null hours. Existing Engine CI remains payment/spending rejected before steps; no billing action/rerun. Original benchmark gates/status remain unchanged/unqualified. No provider, supported-Windows, production, reference or release qualification follows.

[ADR0025](../adr/ADR-0025-awaited-worker-stack-context.md), [delivery evidence](../evidence/roslyn-worker-context/delivery.json), [prior ordering](roslyn-task-ordering.md).
