# Synthetic task-to-thread conformance

2026-11-01, Engine #20, ADR0022. This wave verifies a task-lineage mechanism on an isolated synthetic target. It does not yet identify the Roslyn worker behind a production/generator Emit wait. Engine remains `55c630fc5d4c47258a1a2b0da4a16ce8bc42b9f7`; original compiler concurrency, GC, benchmark workload/primers/flags/thresholds and #3 Blocked are preserved.

## Result and proof boundary

The corrected complete plain then TPL pair passes all seven declared cases: scheduled Task.Run, already-completed GetResult, synchronous wait, forced inline execution, nested parent/child, exception and running-task cancellation. The raw trace has seven complete schedule/start/completion execution-event sequences and seven synchronous task-wait brackets, plus the completed task with no fabricated lifecycle or wait. All 52 marker records agree exactly with sidecar payloads and native headers, with a nonempty common clock-offset intersection. EventPipe/ETLX reported loss and payload read errors are zero. Owned target/releaser threads join successfully.

Forced-inline task4 executes on caller native TID900 while its destination scheduler ID is2 and execution-origin scheduler ID is1. This is a positive counterexample to treating every TaskWait bracket as blocked time or using one scheduler ID meaning across all events. Nested child6 executes on TID928 while parent5 executes/waits on TID926; the main caller is900. These IDs describe this observed process only. A completed GetResult emits no wait; absence of an event is not a zero-delay measurement.

The assembler uses a single owned-process scope and TaskID lifetime, retaining distinct destination and ambient scheduler contexts. It rejects malformed metadata, duplicate/reused IDs, clock reversal, incompatible execution headers, caller-context changes and incomplete histories. Malformed numeric/string identities poison compatible task keys without accepting those malformed identities. Unknown additional TPL IDs are counted separately, while provider-error/invalid IDs are errors. Schedule/start/complete observations are execution-event lifetimes, not unconditional logical Task.IsCompleted proof for attached-child paths.

Single-pair target stopwatch observations are plain391.254881 ms and traced388.316922 ms, including synchronization/markers but excluding final sidecar/report serialization. CPU/allocation counters were not recorded and remain null. Process-and-collection clocks have different brackets. No overhead estimate, speedup, variance result or performance acceptance follows.

## Failed preparation and independent checks

Pair01 is retained as invalid conformance: semantics and parser loss gates passed, but EventSource rejected an undefined marker keyword. Before rebuilding, correction01 declared the nested keyword fix and complete positive marker/error gates; the entire unchanged seven-case plain/TPL pair was repeated as pair02. The offline verifier rejects pair01 for its provider error. Nothing is stitched or selected from pair01.

Eighty-six fixtures pass on each Windows and WSL, and an independent raw audit passes 560 checks across 7,677 records (52 markers and 42 TPL events). Independent fixtures exercise inline/nested/exceptional histories, metadata/type/loss/count errors, persistent poisoning, ID reuse and unfinished events. Verifier negative fixtures and an independent raw audit are retained with final reviewed source hashes in the delivery evidence. Failed fixture-preparation attempts and superseded analysis sources remain alongside final results. The initial assembler source was recovered by reversing two recorded edits from a retained version and matching its independently recorded SHA256; this recovers bytes, not immutable execution attestation.

## GC contract review

The exact [VMR runtime source](https://github.com/dotnet/dotnet/blob/5254d8bcf59917edc1e1abc33bdf2442b77b1c70/src/runtime/src/coreclr/vm/threadsuspend.cpp) and EventPipe writer chain support ordinary EE native headers as emitter TIDs, not paused-worker identities. Suspend Begin occurs before ThreadStore locking and Restart End after unlocking, so outer envelopes can interleave. Debugger retry paths can emit restart phases before SuspendStop and retry without a fresh Begin. Four-phase sequencing is therefore not universal.

All 12,147 records of each retained EE phase have matching event IDs/opcodes/version1; there are zero metadata mismatches. This validates metadata correspondence, not all pause pairing. Prior 23 envelopes, 21 full-phase agreements and 83 same-initiator hypotheses remain separate and unpromoted. Accepting successful inner SuspendStop to RestartStart observations needs applicable caller paths, runtime build/GC-mode correspondence, stable lifetimes, retry absence and capture completeness; source reading does not establish binary attestation or per-worker CPU/cause.

## Reproduction and next work

Samples contains `tooling-traces/TaskConformance`, `tools/capture_task_conformance.py`, `tools/analyze_tooling_tasks.py`, `tools/verify_task_conformance.py` and portable adverse fixtures. Exact raw traces, source/binary hashes, original protocol/correction, sidecars, failed attempts and independent reports are retained losslessly under `tooling-traces/evidence/2026-11-01-task-conformance/retention.json`. Builds/captures are Linux/WSL synthetic proof only; Python fixture validation on Windows does not unblock supported-Windows #3.

Next: separately declare a bounded Roslyn task-lineage diagnostic lane after reviewing observer overhead/coverage and source freezes. Scheduler-transition tracing still lacks established ordinary-user access and explicit clock/loss conformance; do not silently change host permissions. Without that channel, a task link cannot establish runnable delay or an exclusive GC/scheduler cause. Do not rerun the original benchmark until a justified product change calls for the unchanged full comparison.

Existing Engine CI remains payment/spending rejected before steps; no rerun or billing change. #20 remains In Progress/P2/M0, dependencies #2/#11, original estimates, Test/Benchmark Planned and null hours.

[ADR0022](../adr/ADR-0022-synthetic-task-lineage-conformance.md), [delivery](../evidence/task-lineage-conformance/delivery.json).
