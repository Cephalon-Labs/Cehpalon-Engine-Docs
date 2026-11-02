# Static owned scheduler collector conformance

2026-11-03. Engine #20, [ADR0029](../adr/ADR-0029-static-scheduler-conformance.md). Engine remains `55c630fc5d4c47258a1a2b0da4a16ce8bc42b9f7`; #3 remains Blocked. One frozen negative-then-positive matrix completed with fresh ordinary-user static populations. This establishes bounded synthetic collection observations, not dynamic Roslyn, GC cause, an Engine optimization or original benchmark qualification.

## Actual ordered cases

Root ran the exact frozen command once, after passive preparation and source/input review. Both sessions used one UID/GID1000 controller with four precreated worker threads. Every live thread was mapped from local TID to global scheduler payload TID in that execution using a task-attached gettid event. Each session then opened160schedulerFDs (eight events across20onlineCPUs), disabled initially, with every payload filter/ring/identity check acknowledged before the first enable. Actor release followed the last enable. Root was collector only; no host configuration, package installation or permission/clock/tracefs change occurred.

| Case | Parsed SAMPLE records | Sum of terminal counts | Sum of terminal LOST | Emitted LOST reports | Throttle records |
|---|---:|---:|---:|---:|---:|
| Fixed overflow negative |177|103790|103613|0|0|
| Fresh positive |3211|3211|0|0|0|

The negative used exactly10,000 handoff rounds and250ms without draining, one data page per FD, under its fixed deadline. It observed nonzero independent terminal loss, then fully closed/joined before positive. No adaptive pressure or repeat occurred. The zero emitted LOST reports alongside103613 terminal lost publications demonstrates why absence of a final LOST record is insufficient. These totals span per-FD publications, not unique physical scheduler events or task durations; emitted and terminal loss are never added together. Count/sample/lost equality in this negative is an observation, not a universal conservation law.

Actual delivery of LOST/throttle record layouts was not exercised in either case. Their decoders have source/offline support; terminal read-format loss detection is the positive negative-case observation here.

The positive used64data pages per FD, with1ms requested drain cadence and recorded actual cadence/collector usage. All per-FD conservative gates passed: zero terminal loss, unknown record types, throttle records or decoder errors, count==parsedSAMPLE, stable complete drain/counter/FD-ID checks and0<running==enabled. Time accounting equality is perf-context evidence, not upstream event completeness, uninterrupted wall-time service or host CPU availability. No original benchmark or compiler/GC/concurrency change occurred.

## Controlled transitions and lifetime

The fixed positive phases completed100A/Bhandoff rounds,1000yields each,10000integer iterations each with checksums, eight affinity alternations with readbacks, one controlled nonmember fork/exit/join, and an armed sacrificial thread exit followed by a fixed2second RCU tail. The newly forked child stayed outside static S.

Within worker marker windows, A had119 and B157 literal sleep→sched_wakeup→switch-in chains, with zero unresolved edges in those selected windows. These are native recorded chains, not one-to-one business handoff rounds or useful-work/CPU/GC durations. The model preserves initial/final/missing/equal-time/conflicting edges as unknown instead of reconstructing or selecting favorable pairs. State256 is runnable preemption R+, not sleeping. The raw matched-switch histogram may include an unowned previous-task counterpart; only actor-specific edge queries use owned actor PIDs.

No R+256 record occurred in this actual positive case; that decoder rule is supported by exact source and offline adverse fixtures, not positive preemption delivery here.

All eight migration steps had recorded candidates; changing steps1–7 required exactly one record with the expected previous/new singleton CPUs inside each worker bracket. The first step could already have the requested affinity. Parent-side fork delivery and nonmember exclusion passed. A literal sacrificial exit, terminal X/Z switch-out and delayed free candidate occurred within the declared retirement deadline; the retired proc entry was observed absent after the tail. Post-exit records remain unassigned lifecycle candidates, not actor work. No recorded generation reuse was admitted; PIDFDs do not reserve numeric IDs and absence of a reuse record is not universal absence.

Precreated actors cannot exercise their own new-task wake after arming. `sched_wakeup_new` owned delivery remains UNEXERCISED/UNKNOWN, despite all eight channels being configured. No all-eight positive-delivery or dynamic ThreadPool readiness claim follows. The controlled child globalID1125 was not admitted to S; old positive actor IDs are exited and cannot be reused as filters in a later execution.

## Preparation, review and artifacts

Fresh passive preparation retained kernel release6.18.54.1-microsoft-standard-WSL2, eight exact scheduler formats plus gettid format, Python/privateatomic/source hashes, resource limits and zero time offsets. The20CPU positive mapping footprint40.625MiB fit the existing64MiB conservative memlock gate, and180descriptor capacity fit10240. These are capacity observations, not reservations or complete kernel binary attestation. Verified private libatomic was reused by explicit path/hash; no installation or loader-cache changes.

Core158portable adverse fixtures, root analysis56fixtures and independent literal-edge18fixtures pass on Windows/WSL. Root completed the independent author's16mocked control/cleanup fixtures and14pure resource guards per platform after two agents hit usage limits. One control-fixture rejection handler initially omitted FileExistsError; that failure/source is retained and the narrow fixture correction was rerun. Earlier model missing-edge cases failed2/18 and remain retained; corrected unknown handling passed. Source/actor/orchestrator versions and all preparation/failed/raw attempts are preserved. Scope and actual-artifact review are in [delivery evidence](../evidence/static-scheduler/delivery.json).

The primary took over the incomplete collector and added passive preparation/resource/kernel checks; a separate source reviewer inspected the final frozen candidate and prepared inputs before the actual run. Retained individual environment/proc readbacks and failures close the prior ADR0028 post-read snapshot gap. Library/source/format/namespace checks remain observational; they are not a hostile-host sandbox or immutable execution attestation.

The independent actual raw oracle passed79,568checks over320channels/ten thread bootstraps, binding2,308consumed file hashes. It independently reproduced both native-chain counts and zero selected-window unknown annotations. Initial audit01 compared sparse state counts to explicit zero-valued dictionary keys; exact nonzero counts agreed, that preparation mismatch/source/log remain, and corrected audit02 passed without changing or rerunning the capture.

An additional bounded scope audit found312waking and312wakeup records where global target PID differed from global emitter common_pid;27waking and4wakeup records also had sampleCPU different from payloadtargetCPU. These support the frozen payload-filtered population's distinct emitter/target semantics, not complete dynamic ownership or latency causality. Total retained native output49,238,964bytes across2,303files was below the shared256MiB budget. These are file/record checks, not an aggregate qualification score.

## Next boundary

Before a real Roslyn lane, separately design and freeze dynamic-thread admission/birth coverage, retain every generation/lease/mapping and guarantee scoped remote-wakeup/state coverage with explicit unknowns. Static proof does not authorize automatic child expansion or reuse of exited IDs. A full same-execution CLR/task/GC/scheduler diagnostic lane and runtime branch/build/binary correspondence remain necessary before attributing Emit worker waits or proposing a causal Engine change. Guest scheduling states alone do not establish host-vCPU service or useful compiler work.

#20 stays In Progress/P2/M0 with existing dependencies, estimates, Planned Test/Benchmark gates and null actual/remaining hours. #3 entire row stays Blocked; other tracking rows/metadata are preserved. Original workload/thresholds/primers/flags/GC/concurrency and Observed/unqualified benchmark status remain unchanged. Hosted Engine runs remain old pre-step payment/spending rejections; no rerun/billing action or provider/supported-Windows/reference/production/release qualification.
