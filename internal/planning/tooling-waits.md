# Same-process tooling waits — observed in Emit, no safe Engine patch isolated

Continuation of #20 after the [prior trace report](tooling-traces.md), under [ADR0019](../adr/ADR-0019-tooling-same-process-wait-traces.md). The prior75targets and original full benchmark remain retained, with unresolved variability. This wave asks whether long compiler rows contain same-caller managed/native waits rather than assuming a GC/JIT/physical-IO cause. Engine remains55c630fc5d4c47258a1a2b0da4a16ce8bc42b9f7. #3 remains Blocked; all original tracking gates/M0/dependencies/estimates/nullhours stay unchanged.

## New evidence boundary

A fixed Linux lane combines EventPipe, selected syscall/futex tracing and proc samples in the same managed process: one entire generator matrix plus all8CLIscenarios×3rotated/reversed rounds,25targets. Target PID/birth/parent/group/session and executable are verified under one directly owned strace leader. Observer readiness precedes EventPipe session creation and same-reverse-port resume. No unrelated PID attachment, global trace/session cancellation, privilege/root/policy changes or reference-machine claim.

Explicit runtimeWaitHandle keyword0x40000000000 extends the prior mask to0x411C14FCCBD/Verbose5; this was not enabled in old captures. WaitHandleStart301/Stop302 pairs use only unique PID/CLR/nativeTID identity. Stop lacks an object token. Unknown identity, nested starts, orphan stops, reversed timing and known reused thread numbers poison compatible temporal claims persistently, rather than selecting a favorable later pair. Unknown numeric WaitSource is retained without asserting Monitor/Task ownership. A managed wait elapsed interval is not CPU time or a proven lock owner.

Native outcomes distinguish WAIT/WAKE, success/timeout/EAGAIN/interruption/restart/unknown. strace wall includes ptrace/scheduling overhead; syscall returns are not kernel blocked-time measurements, and native loss remains unknown. Overlapping GC/JIT/managed/native intervals are bounded unions, not an additive exclusive budget. Every row and uncertain/unassigned interval stays retained.

Generator/synthetic targets add post-body UTC reads bracketed by Stopwatch alongside original startup/marker anchors. For each queried body, all anchors in its nearest full preceding/following bracket must support the declared strict constant-offset intersection, including100ns UTC and microsecond native print precision. Incompatibility gives unsupported_constant_offset/unassigned native overlap; it may reflect slew/precision rather than a proven clock step. Endpoint consistency still cannot rule out unseen wall-clock excursions. CLI binaries have no custom markers, so their conclusions are same-PID lifetime counts/distributions only; no precise EventPipe/native temporal join is claimed. Proc counter values remain partial lifetime observations and are not prorated into phases.

## Collector verification and source freeze

The separate synthetic Linuxx64fixture has seven main-TID spans:startup,cpu,managed-wait,native-futex-wait,explicit-gc-conformance-only,file-write-read,result. An unsignalled managed event times out while one separately armed CPU worker runs and is joined. Direct futexWAIT_PRIVATE expectsETIMEDOUT110. Known file bytes/hash/read/write/FD closure are checked. ForcedGC is strictly synthetic; no real workload or benchmark forces GC.

Actual synthetic capture01:7markers,213pairedJIT/1GCenvelope/EEerrors0/512managed samples, reported EventPipe loss0,2unique WaitHandle pairs/errors0, allowned cleanup. New offline analysis verifies managed overlap83.517ms inside92.421ms body and controlled native timeout conditional interval80.139–80.145ms inside86.400ms body. All7strict clock models supported conditionally;4096bytes each direction and two closed FDlifetimes match. These perturbed setup results are not latency acceptance or a workload speedup.

Initial collector852bd9passed25offline tests on both actual WindowsPython3.11 and Linux3.10.12; incompatibility with co_qualname was caught beforelivecapture and corrected. The actual missing-tool launcher fails before spawning target children and verifies6loaded modules. Both collector revisions record import-time bytes/function inventory+code fingerprints and before/after binary/source hashes. Globals/defaults/imported bindings remain outside attestation. Offline analyzer2ba6d391… passes41fixtures and two peer reviews, including malformed identity/TID reuse/clock/outcome/FD guards; every consumed input is hashed. Streaming avoids retaining irrelevant runtime event payloads in memory. All earlier mock/analysis failures are kept; frozen synthetic raw was replayed, never regenerated to select favorable output.

## Existing binary/GC ambiguity study

Offline inspection of five retained prior55/final55assembly pairs found equal complete managed method records:Tooling.Components376,CLI178,consumer599,generator36,Core30. IL bytes/signatures/flags/locals/stack/EH records agree; whole-file SHA/MVID/timestamps/CodeView paths/GUIDs differ. String/user-string heaps and managed resource bytes agree. Consumer informational version names different Samples revisions; other metadata tables/GUID heaps are not assumed identical. [Exact metadata comparison](../evidence/tooling-waits/pe-comparison.json) retains all values and comparison-only path normalization. Equal IL records do not prove equal full binaries, resolved runtime semantics or a timing cause. Nothing was rebuilt or changed for this study.

A separate per-TID pairing study of the old Linux trace recovers ten additional GC candidates, but the exact installed runtime commit source was unavailable. Published current implementation is not substituted for pinned contract proof. The original conservative analyzer and reports remain unchanged; candidates are retained as hypotheses, not newly certified pause intervals.

## Fixed combined lane findings

Corrected full02 completed all25targets and all25offline analyses:306generator rows(270measurements+36primers),18groups,2,956markers and24CLIcases. All306strict per-row constant-offset models are supported conditionally. No data from failed full01 is stitched into02. [Full same-execution findings](../evidence/tooling-waits/combined-linux02-findings.md) preserve all row/group/CLI values and scope limits.

Across270measured compiler rows, summed diagnostic wall is93,019.972ms. The following are physically capped overlap unions per row, summed across disjoint rows; **do not add or subtract these overlapping dimensions to derive CPU, exclusive blocked time or causes**.

| Observed dimension | Positive measured rows | Summed overlap ms | Fraction of summed diagnostic wall |
|---|---:|---:|---:|
| Caller managed WaitHandle pairs |76|19,400.635|20.856%|
| Caller eligible native syscall wall intervals |270|30,984.475–30,999.991|33.309–33.326%|
| Paired GC suspension envelopes |13|321.309|0.345%|

Every observed19,400.635ms caller managed wait falls within PE Emit; none of the135measured RunGenerators spans has paired caller WaitHandle overlap. This is not proof those stages have no other waits/GC. Measured stage sums are1,743.339ms RunGenerators and91,276.236ms Emit. During completed caller waits in measured stages,288caller managed residency sample observations contain Compilation.Emit/task-wait/ManualResetEventSlim.Wait, and283contain MethodCompiler.WaitForWorkers. This locates observed context in Roslyn Emit. It does not identify worker starvation, a physical lock owner, OS on-CPU work or avoidable Engine code.

The generator has466wait starts/465stops/465complete pairs plus one unfinished backgroundTID851 start; callerTID754 is separate. Cross-thread sums/background activity do not establish caller stall. The field same_tid_managed_wait_native_observed_overlap is **process-wide matched-TID co-observation**, including background/idle workers. Its88.36% is not caller-only and cannot be reported as88%caller blocking or a particular futex-to-managed-object causal match.

All24CLI traces preserve lifetime-only scope. The six selected GraphQL exports each have a complete main-TID pair and one unfinished background wait. All18other cases have no observed managed WaitHandle pair; this is collected-channel evidence, not universal absence. AllsixGraphQL traces show3,744HotChocolate JIT intervals and expected schema/executor residency; the18others show none observed. Selected schema work agrees with existing guards and disposal, so no disabled-module activation or unnecessary Engine action is established.

[Independent integrity audit](../evidence/tooling-waits/independent-integrity-audit.json) passes852,454checks across25targets: approved6afsource bytes/71compiledfunction fingerprints before/after, actual binaries/Engine/fixture/input pins, every proc PID/birth/group/session, all976,930EventPipe records/counts/PIDs/hashes with reportedEventPipe/ETLXloss0,2,956marker+UTC payloads, all306source/registry/ID/order rows against BOTH prior diagnostic and lastcanonicalLinux data, and24frozenCLI outputs/artifactbytes/counters. Neither PE hashes nor timing/counters are assumed equal to earlier runs.

Attribution remains partial: aggregateEEpairingerrors1,669/JIT1; generatorEE1,637 and23pairedGCenvelopes prevent GC absence claims. There are seven unfinished background wait starts across the lane,36,448proc samples/sixthread-read races/21normal-exit andfourterminal-unavailable observer statuses. Native incomplete/unparsed/UTF-replacement counts are0, but kernel loss remains unknown. Conditional clocks and sampled lifetime are not reference/platform/production proof.

No safe avoidable Engine operation is isolated. Keep Engine55 unchanged, compiler concurrency/tiering/GC/primers, selected schema generation, authority/module guards and durable publication. No unchanged-source original benchmark is repeated under this ADR. The prior complete series remains the last untraced observation (Windows9/Linux3unstable generator groups;CLI0/0), not a result of these perturbed traces.


The first full lane01 stopped after12completed cases before round1export-both observer/collector startup: generic child discovery selected a transient strace startup helper3129 while the retained successful managedexecve was3130. Liveexec/birth safeguards refused collection; ownedgroup cleanup completed and a separate read-only check found no remaining proc entry for the actual execPID. The failed lane and all already-valid raw generator/CLI files remain distinct; they are never stitched into final output. strace5.16published source test_ptrace_seize forks a probe child before tracee startup. New discovery must anchor to successful exact exec+live leased ownership, with new negative fixtures and an entire25-targetrepeat02. This is collector preparation evidence, not an Engine variance cause.

Read-only follow-up checked all25earlier separate native01cases: every reported PID agrees with the first successful execve PID. No historical case mismatch was observed; its existing partial-lifetime limits and generic-discovery susceptibility remain documented.


## Delivery and tracking

Corrected collector3350325d… passes41mock checks on eachWindowsPython3.11/Linux3.10, with exec-anchored target lease and only post-resume header waiting allowed after tracer0. Synthetic02 and frozen analyzer2ba…replay pass seven stages/controlled waits/exact4096IO; offline analyzer41fixtures/two peer reviews pass. All code/source/failed mock and analysis attempts are retained. No source edits occurred during final fixed capture; final per-lane source/binary hashes match.

Original #20 In Progress/P2/M0, W5/#2/#11 dependencies, fullTest+BenchmarkPlanned,40–80estimate(midpoint60), actual/remaining null stay unchanged. #3 body/editable row remains identical Blocked. Engine55component40993252408/platform40993252420 retain prior payment/spending rejection before steps; no forced unchanged CI, billing change, provider/supportedWindows/reference/production/IDE/distribution/AOT/public release. New Samples/Docs commits are technical provenance, never Engine task/card journal entries.

See [delivery metadata](../evidence/tooling-waits/delivery.json) and [lossless raw evidence](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/tooling-traces/evidence/2026-10-30-waits). Raw traces, failed01, corrected02, synthetic/negative setup, source snapshots, analysis/audit scripts and every original output are retained with original/stored hashes. DerivedETLX/build/private/clone material excluded. Next stronger performance work requires a controlled reference environment or a newly scoped causal worker/GC study, with a predeclared protocol; repeated unchanged runs until CV drops remain unjustified.

Final live CI readback clarifies job counts:2 jobs per Engine run,4 total across the component/platform pair, all0 steps with payment/spending annotations. Read the earlier compact4jobs wording as the component/platform pair total, not4 per run; historical raw records remain retained. No job was rerun.
