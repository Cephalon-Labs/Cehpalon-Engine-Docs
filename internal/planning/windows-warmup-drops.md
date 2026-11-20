# Windows warmup drops: GC and scheduling evidence

The historical five drops are explained at the collector state-machine level: five already-overdue offers encountered occupied lanes in one 11.8 us catch-up burst. Their underlying historical GC/kernel cause remains unknown because that execution has no runtime or kernel trace. Four separately declared, instrumented warmups completed 6,000 reads with zero drops. No matching-drop retry was made and these are not replacement benchmark candidates.

Engine product source remains `5f8f252e901e85c50d7fc6f4b760e457965ce3bb`; SDK remains `11.0.100-rc.3.26522.148`. Changes are Samples diagnostic tooling and Docs. The original benchmark criteria, invalid Windows comparison attempts, #3 blocker and task metadata remain unchanged. [Declared protocol and preparation corrections](../validation/windows-warmup-drops.md).

## Historical mechanism

Replay uses the exact previously committed attempt-02 warmup rows: 1,495 passed and five dropped. At each drop, 32 prior requests have sent timestamps before the decision and completion timestamps after it. The five assigned predecessors are indexes 1158–1162. Their source-level busy flag cannot yet have been cleared because the completion row is written before the finally block clears it. This is recorded pending work, not proof that all 32 server handlers were running.

| Dropped offer | Predecessor | Offer lateness ms |
| ---: | ---: | ---: |
| 1190 | 1158 | 8.3570 |
| 1191 | 1159 | 6.3683 |
| 1192 | 1160 | 4.3685 |
| 1193 | 1161 | 2.3687 |
| 1194 | 1162 | 0.3688 |

The five scheduled deadlines span 8 ms, but recorded drop decisions span only 0.0118 ms. All five deadlines precede the first recorded drop. The producer's overdue-loop path has no awaited delay between the following four decisions. Thus a late producer resumption can expose a catch-up burst while earlier requests remain pending. This establishes the mechanism that rejected offers. It does not identify why those prior requests or the producer were delayed; no historical GC timing is invented.

## Scoped new capture

The current Windows token is unelevated and lacks SeSystemProfilePrivilege and SeDebugPrivilege. WPR is present, but kernel CSwitch/ReadyThread scoped capture readiness has not passed. No kernel session, elevation, driver or host setting change was attempted. EventPipe was attached only to held, newly owned server/client processes. The source/lock/registry and target/collector binary hashes are retained; private credentials travel through process pipes and are excluded from exports.

The diagnostic copy keeps generated Engine business/host/gateway sources and emitted registration unchanged. It adds numeric producer/request markers, native/managed thread identities, a preallocated before/after-QPC receipt ledger and server request DiagnosticListener stages using a numeric correlation header. This adds observable work and allocation, including hosting diagnostic metadata; all timings are perturbed. The ordinary comparison consumer is unchanged.

Every process keeps its PID alive until collector drain completes. Custom marker sequences and terminal counts reconcile, header PID/native TID match receipts, each event QPC lies inside its independent before/after receipt bracket, and relative-time/QPC slopes agree. Across the four warmups, 49,628 markers and 240 typed CLR suspension phase frames reconcile with zero reported loss/payload-read errors. The 60 full capture suspension episodes use actual GCSuspendEETraceData/GCNoUserDataTraceData templates (IDs 9/8/7/3, version 1). Clock slope residual is below 0.000000001 ms. A zero reported loss counter is not an unconditional physical completeness proof; marker closure and positive controls provide additional bounded checks.

GC phases are paired by process and CLR instance. Suspend-stop to restart-start is the narrower all-suspended interval; suspend-start to restart-stop also includes rendezvous/restart. A background GC lifetime alone is not a pause. GC/GC-prep reasons are kept separate from other suspensions. Recorded suspension can itself include OS scheduling of GC threads, so these windows do not form an exclusive GC-versus-scheduler causal partition. [CLR event definitions](https://learn.microsoft.com/en-us/dotnet/fundamentals/diagnostics/runtime-garbage-collection-events).

## All four fixed warmups

Each execution retains the original total capacity 64, 32 prepared TLS1.3/HTTP1.1 connections, mixed HTTP/GraphQL and both tenants, four cross-tenant denials and 1,500 offers at 500/s. Each completes 1,500 validated reads, zero drops, no new TLS connections, 1,532 handler constructions/disposals (including 32 preparation reads), zero writes/forbidden factories and one disposed host with closed empty admission. ABORT is intentional after warmup; no measured phase runs and its exit status is not treated as benchmark acceptance.

| Execution | Producer await windows | Longest producer await ms | Client GC inner overlap in that await ms | Longest request ms | Server GC inner overlap in that request ms |
| --- | ---: | ---: | ---: | ---: | ---: |
| 01-baseline | 201 | 16.2917 | 0.0000 | 5.3507 | 3.3106 |
| 02-listener | 201 | 15.9641 | 0.0000 | 36.0620 | 33.2155 |
| 03-listener | 200 | 16.2531 | 0.0000 | 25.4794 | 23.0161 |
| 04-baseline | 204 | 15.9854 | 0.0000 | 19.5485 | 16.3365 |

All 806 producer awaits and 6,000 request windows are retained, not just these maxima. Only one producer await overlaps a client GC inner interval; the longest await in every execution overlaps no recorded client or server GC envelope. Pending-work-item snapshots at both endpoints of those four maxima are zero with 20 ThreadPool threads; these endpoint observations do not prove an empty queue throughout the gap.

These await markers bracket Task.Delay(1) and its continuation, not an observed native timer-ready timestamp. The roughly 16 ms pattern is consistent with the documented Windows clock-resolution limitation of short Task.Delay calls; this is an inference, not a measured scheduler cause or exact resolution measurement. [Task.Delay contract](https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.task.delay). Timer readiness, ThreadPool dispatch and OS runnable time remain unseparated inside the uncovered interval.

Client GC inner windows overlap 54 request windows; server GC inner windows overlap 103. These counts are process-specific and must not be summed as exclusive causes. For example, execution 02 request 619 lasts 36.0620 ms and overlaps 33.2155 ms of server all-suspended time with no client GC envelope overlap. Execution 03 request 617 lasts 25.4794 ms, overlaps 23.0161 ms of server inner suspension, and its server hosting-stop marker precedes client completion by 24.0491 ms. Hosting-stop does not prove the response was flushed to the wire; that later interval also overlaps server suspension and cannot be assigned to the client scheduler. Conversely, execution 01 request 49 has 1.7985 ms client inner overlap with no server GC overlap; 1.2035 ms of it falls after the server hosting-stop marker. This separates recorded client and server suspension contexts without converting overlap into exclusive delay attribution.

TPL TaskScheduled/Transfer-to-TaskStarted envelopes are paired only within process/session/task identity, retaining reuse and missing-endpoint ambiguity. Captures contain 32 client envelopes and three/four server envelopes per execution, but none overlaps the actual warmup interval; they are primarily setup/lifecycle work. They provide no exact warmup request continuation lineage or OS ready-to-run time. ThreadPool worker/adjustment events and endpoint counters are supplementary observations, not a starvation diagnosis. The normalized exports retain those events for further audit. [EventPipe scope](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/eventpipe).

## Controls, corrections and validation

Four alternating synthetic control/observed pairs validate 10,000-marker loops, sleep/gate work, known forced GC and TPL scheduling. Forced collection is confined to these positive fixtures. The final four loop wall-time differences are +19.9258, +18.6032, +18.6248 and +18.6608 ms per 10,000 markers, with zero incremental measured caller-thread allocation. This is post-attach marker-loop observer cost, not total HTTPS tracing overhead; source startup/first markers and hosting-listener work are outside that loop but retained separately.

Preserve the initial diagnostic-tool compiler failure and unused preparation 01. Preparation 02's eight fixture captures contain valid markers/GC, but the original analyzer missed the /Transfer suffix; correcting the parser validates the same raw data without re-execution. One HTTPS preflight was inadvertently launched after that failed analysis command; it remains rejected because its initial server hook emitted no request stages. The corrected base-activity predicate/direct HttpContext handling and event-name/property-shape metadata validate all stages in preparation 03's fresh eight controls and one short HTTPS preflight before any fixed warmup capture. No failed preflight was relabeled as qualification.

Thirteen focused tests pass on Windows and WSL, including eleven marker/clock/loss mutation cases and five mutations of the actual historical offer rows. They cover GC phase ambiguity, persistent poisoning, process separation, task identity reuse and the actual transfer-opcode name. Full Windows trace analysis replays byte-identically on WSL; this is offline replay, not WSL runtime capture. Public exports round-trip every raw digest and reproduce all four warmup analyses plus both control series. Tracking regressions pass 60 tests. No safe Engine behavior patch is justified by these observations; only diagnostic correctness/coverage was changed.

Private original nettraces (20 files, 14,658,608 bytes) stay in ignored local storage with SHA-256 provenance. Public exports are allowlisted, omit credentials/other payload strings and pseudonymize pointer-like identities. Original and corrected analyses, all source freezes, incomplete/rejected attempts and successful controls remain available. New traces neither reconstruct the five historical drops nor close the original Windows comparison. #3 stays Blocked; #18/#20 stay In Progress/M0 with unchanged gates, dependencies, unknown actual hours and canonical benchmark criteria.

The remaining boundary is native timer-ready/managed continuation publication plus scoped OS switch/ready observations in the same owned execution. Collect those only after separate readiness/loss/cleanup controls on an appropriate Windows environment. Do not change GC flags, timer resolution, concurrency, offered rate or primers to produce a favorable pass.

[Immutable source, normalized exports, replay and SHA-256 evidence](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/62944912b0e8cf30b948377c16a7562b604a4923/tooling-small-api/evidence/2026-11-20-windows-warmup-drops). Large logical analysis/receipt/event files use lossless gzip; raw-integrity.json maps their original names and raw/stored digests.
