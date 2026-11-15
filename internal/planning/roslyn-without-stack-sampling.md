# Roslyn Emit with EventPipe stack sampling disabled

One provider-only execution completed on WSL 6.18.58.1 against Engine `55c630fc5d4c47258a1a2b0da4a16ce8bc42b9f7`. The existing diagnostic corpus passed all 306 Emit rows, including 270 measured rows. All 2,956 markers matched their sidecar spans. There were 383,066 managed events, 40,464 JIT start-to-load intervals and 64,998 TPL records. The parser reported zero EventPipe/ETLX loss or payload errors, and the TPL replay reported zero errors or unfinished waits. The collector listed only the three explicit providers. An independent replay found zero raw SampleProfiler records and an empty parsed stack stream. [Frozen protocol](../validation/roslyn-without-stack-sampling.md)

All 211 inventoried binaries matched the earlier run. The native channels used the same hook order and owner scope. They collected 73,960 lifecycle records across 34 identities and 93,786 boundary records. Terminal counters reported zero losses, faults and recursion misses, with matching detached reads. Boundary records reconcile to 46,860 callback pairs, 32 newborn prefixes and 34 retired tails. Sixteen complete pairs with a retired endpoint were excluded. Of 1,913 selected waits, 1,910 bound to a caller identity with a positive guaranteed clock core. The three remaining waits have a nonpositive guaranteed core and remain explicit.

| Observations within each execution | With stack sampling | Without stack sampling |
| --- | ---: | ---: |
| Raw stack samples | 209,518 | 0 |
| Complete reason-0 suspension sequences | 11,191 | 660 |
| Reason-0 sequences with corroborating sample records | 10,509 | 0 |
| Strictly linked blocking GC sequences | 64 | 64 |
| Reason-1 sequences with unresolved collection link | 11 | 11 |
| Reason-2 shutdown sequences | 40 | 40 |
| Reason-6 GC preparation sequences | 12 | 12 |
| Bound caller waits with a scheduler callback pair | 1,654 / 1,964 | 1,640 / 1,910 |
| Bound caller waits overlapping a linked blocking-GC inner interval | 27 / 1,964 | 23 / 1,910 |
| Waits with an awaited-task scheduler pair | 592 | 66 |
| Those waits whose caller core also overlaps a linked blocking-GC interval | 26 / 592 | 10 / 66 |

The off-mode replay accounted for all 3,148 phase records exactly once. The source-linked replay identifies CoreCLR stack sampling as one reason-0 source, and the provider-only run leaves 660 reason-0 sequences with no SampleProfiler activity in the captured stream. Their triggers remain unresolved. The sampled run had 682 reason-0 sequences without an in-window sample, but there is no episode-level matching between executions. [Source-linked GC replay](roslyn-gc-episodes.md)

The awaited-task scheduler pairs are strictly inside the observed task execution and caller wait intersection. GC overlap is measured against the caller wait core. This does not establish simultaneous GC and callback activity in the worker interval or time attributable to either mechanism. The traces differ in execution and sampling perturbation, so record and overlap differences do not establish a speedup, exclusive scheduler/GC shares, physical suspension duration or the cause of Emit variance. #20 remains In Progress and the original benchmark is pending under its existing gates. [Delivery](../evidence/roslyn-without-stack-sampling/delivery.json)

A later replay linked the 660 residual sequences to the driver's two precise allocation reads per invocation. None supplied a contained phase to a selected Emit wait. [Precise allocation read replay](roslyn-allocation-probes.md)
