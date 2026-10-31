# Emit worker continuation

User authorized agents to separate GC/scheduler evidence, test and sync #20 while retaining #3 Blocked and original gates.

# Emit worker waits: GC and scheduler evidence

2026-10-31, ADR0020, Engine #20. Engine stays at `55c630fc5d4c47258a1a2b0da4a16ce8bc42b9f7`. The retained complete combined-linux02 generator was reanalysed offline; no build, target, capture or original benchmark was run.

The evidence narrows worker context but does not determine whether GC or scheduler delay caused the caller wait. No safe Engine optimization is isolated. Keep compiler concurrency, GC, selected schema, authority and publication semantics unchanged.

## Observations

All 505,810 runtime records, 107,929 stack records, 2,956 stage spans and 306 Emit rows (270 measured, 36 primers) remain represented. Exact compiler-plus-ThreadPool frames produce 8,195 point observations on 22 native TIDs over the whole execution. Measured Emit has witnesses in 242/270 rows; the remaining 28 are unknown. Of 80 measured completed caller-wait/Emit intersections, 67 contain a caller WaitForWorkers point; 53 of these have compiler worker witnesses. The other 13 keep unknown caller context. Task IDs linking each awaited task to its worker were not captured.

The 379 queries (306 Emit and 73 caller-wait queries including primers) contain 5,390 worker-point associations referring to 3,357 distinct points. Query scopes overlap. The pinned [Roslyn source](https://github.com/dotnet/roslyn/blob/8edf7bcd4f1594c3d68a6a567469f41dbd33dd1b/src/Compilers/CSharp/Portable/Compiler/MethodCompiler.cs) supports the Task.Run/WaitForWorkers frame interpretation, not specific task ownership.

The old GC model retains 23 envelopes and 1,637 errors unchanged. Two envelopes use an end event from another initiator TID and omit RestartStart; raw indices and both interpretations are retained. Only 21 agree at all four timestamps with the supplementary same-initiator hypotheses. There are 83 GC-labelled supplementary suspension episodes, not 83 distinct collections. Exact installed runtime source could not be obtained, so neither model is certified pause truth. The previous measured compiler-wall overlap of 321.309097 ms remains a legacy-model observation, not validated total pause time. The supplementary 2,387.723305 ms is a separate hypothesis; it cannot replace the old result or establish total GC time.

The scheduler analyzer requires adjacent full proc read windows, stable birth/lifetime and a point witness within each query. Measured Emit produces 56,761 endpoint-pair associations with stored CPU increments of 13.530237401 s and runqueue increments of 12.075896 ms. Measured witnessed waits produce 24,205 associations with 4.338697347 s and 2.957289 ms respectively. These are stored-counter changes, **not durations or lower bounds within Emit/wait**; overlapping groups must not be added. One wait-worker query has insufficient endpoint pairs and all nine metrics remain null.

Matching-name [WSL proc source](https://github.com/microsoft/WSL2-Linux-Kernel/blob/linux-msft-wsl-6.18.54.1/fs/proc/base.c) prints stored counters; [scheduler accounting](https://github.com/microsoft/WSL2-Linux-Kernel/blob/linux-msft-wsl-6.18.54.1/kernel/sched/stats.h) may credit prior waiting at dequeue/arrival. Tag-name agreement does not attest the installed binary. Zero counters do not prove enabled accounting or absence of waiting. No exclusive GC/scheduler percentage, starvation diagnosis or GC-free residual follows.

## Verification and retention

Classifier: 20 focused guards pass on Windows and WSL; scheduler: 30 focused fixtures pass on both. An independent 19-case suite preserves a 100 ms stored credit inside a 10 ms query while phase duration/lower bound stay null. Independent raw point audit passes 294,835 checks; independent endpoint replay passes 1,078,247 checks across 19,300 proc samples. Its 85,265 pair-query associations reference 60,427 distinct endpoint pairs (24,838 repeats).

Root replay of both final tools matches agent output hashes exactly. The first independent scheduler audit stopped on an indentation error; original source/log and the corrected copy are retained. All superseded tool attempts and source contracts remain losslessly hashed in Samples `tooling-traces/evidence/2026-10-31-emit-workers/retention.json`; original raw capture stays in the previous evidence prefix. No favorable selection, event filtering or benchmark threshold changes occurred.

Original full benchmark remains Observed/unqualified (generator unstable cases Windows 9/Linux 3, CLI 0/0). No new benchmark pass is claimed. Existing Engine CI runs 40993252408 and 40993252420 remain rejected for payment/spending before any steps; no billing action or rerun occurred. #3 remains Blocked. #20 remains In Progress/P2/M0, dependencies #2/#11, original estimates, Planned test/benchmark gates and null hours.

## Next evidence needed

A separately declared experiment would need a version-specific runtime suspension contract and same-execution task lineage plus scheduler transition accounting to bound actual worker progress. Decide feasibility and perturbation before any new capture. Retain the original full benchmark protocol; only a justified product change would warrant the full unchanged comparison.

[ADR0020](../adr/ADR-0020-emit-worker-gc-scheduler-analysis.md) and [machine evidence](../evidence/tooling-emit-workers/delivery.json).
