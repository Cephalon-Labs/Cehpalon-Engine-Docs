# Literal task event ordering in the Roslyn trace

2026-11-01, Engine #20, ADR0024. This is an offline replay of the complete ADR0023 execution and its pinned lineage output. Engine remains `55c630fc5d4c47258a1a2b0da4a16ce8bc42b9f7`. No workload target, build, capture, original benchmark, host setting or Engine code changed.

## Recorded ordering results

All 641,481 raw records were consumed; 63,325 distinct copied schedule/start/completion/wait references match their zero-based raw records with exact type, header, metadata and payload equality. All 19,527 execution-event histories, 2,372 paired waits, 306 Emit rows and 2,177 row-wait associations remain retained. The 2,345 main-caller and 27 nonmain waits are both reported. No category was selected for a favorable result.

The table compares the execution-start event timestamp with the wait-begin event timestamp. It does not describe when useful work actually began.

| Observed scope | Waits | Start event before wait-begin | Start event after wait-begin | Equal recorded time |
|---|---:|---:|---:|---:|
| All paired waits in the execution |2,372|1,223|1,149|0|
| Measured Emit caller waits |1,913|988|925|0|
| Measured waits with caller WaitForWorkers point context |527|444|83|0|
| Above subset also having compiler point context |486|444|42|0|
| Primer Emit caller waits |264|138|126|0|

All observed schedule events precede their wait-begin events. Among the 1,913 measured caller waits, 42 completion events precede wait-begin and 114 completion events follow wait-end. In the 527 WaitForWorkers-point subset, completion events all follow wait-begin; four follow wait-end. These are literal telemetry relations, not logical-state contradictions or proof of incorrect waiting.

Every main-caller wait uses an execution-start native header TID different from the waiter header TID. Five same-header cases occur only among the 27 nonmain waits, all with execution-start events after wait-begin. Recorded header equality/difference does not prove native lifetime or a particular inline callpath. All previous direct-callsite/native-lifetime flags remain false and queue/blocked/scheduler/CPU durations remain null.

## Source interpretation

Exact pinned [Task source](https://github.com/dotnet/dotnet/blob/5254d8bcf59917edc1e1abc33bdf2442b77b1c70/src/runtime/src/libraries/System.Private.CoreLib/src/System/Threading/Tasks/Task.cs) permits a task to complete between the initial completion check and wait-begin logging. Terminal-state publication/signalling may precede the completion event; attached-child paths add another distinction. A wait can time out before subsequent execution. These relations therefore remain accepted observations.

[TaskScheduler source](https://github.com/dotnet/dotnet/blob/5254d8bcf59917edc1e1abc33bdf2442b77b1c70/src/runtime/src/libraries/System.Private.CoreLib/src/System/Threading/Tasks/TaskScheduler.cs) emits schedule before QueueTask and may schedule inline without enqueueing. TaskStarted follows runtime prelude and precedes delegate invocation; TaskWait can contain inline execution, spinning or blocking. Recorded event gaps are not queue/runqueue, first-CPU, delegate-only, blocked or GC durations. Already-completed GetResult fast paths can omit waits, so this selected wait population does not cover every Roslyn join.

Equal recorded timestamps are a separate unresolved category; raw record order is never a temporal tie-break. No equal timestamps occurred in this population, while adversarial fixtures exercise that case. Source correspondence and matching headers remain observational evidence, not immutable loaded-binary/native-generation or exact callsite attestation.

## Verification, retention and delivery

The portable 92-case suite passes on Windows and WSL. It covers legal completion-before-wait and start-after-wait-end, ties, nonmain headers, poisoned/incomplete contexts, malformed metadata/types, deep raw-reference drift and negative CLI input/summary-hash drift. Independent raw oracle and complete record/subset/header comparison pass 547,776 checks with zero failures. All categories and identities match final replay02.

All analysis versions, source snapshots, source-contract downloads, fixture/negative CLI attempts and independent scripts/results remain losslessly retained in Samples `tooling-traces/evidence/2026-11-01-roslyn-task-ordering/retention.json`. The prior full capture capsule is referenced by revision/hash instead of copied. Exact staged payload/source hashes are verified. No new workload or favorable rerun occurred.

#3 stays Blocked; #20 stays In Progress/P2/M0 with its original dependencies, estimates, Test/Benchmark Planned and null hours. Existing Engine CI remains payment/spending rejected before any steps; no rerun or billing change. Original benchmark gates/status remain unchanged and unqualified. No provider, supported-Windows, production, reference or release qualification follows.

## Next evidence

The ordering distinguishes recorded event populations and prevents an after-wait start event being treated as a cause by itself. It cannot show useful work progress, runnable delay or the cause of post-start delay. Further bounded analysis must preserve native/clock/source limits; actual scheduler attribution still requires established transition access/conformance, and GC attribution requires applicable caller/build/binary evidence. There is no justified Engine optimization or original benchmark rerun from these counts alone.

[ADR0024](../adr/ADR-0024-roslyn-task-event-ordering.md), [delivery evidence](../evidence/roslyn-task-ordering/delivery.json), [prior lineage report](roslyn-task-lineage.md).
