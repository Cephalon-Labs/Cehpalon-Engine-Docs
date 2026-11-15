# Roslyn diagnostic run without precise allocation reads

One provider-only run on WSL 6.18.58.1 tested the prior source attribution by omitting both calls to `GC.GetTotalAllocatedBytes(precise: true)`. Stack sampling was off in both runs. Locked restore and the build succeeded against a clean pinned Engine checkout. At execution, only the staged `TraceDriver.dll` and its PDB differed from the prior driver package. The same Engine and Roslyn dependencies were loaded. Allocation fields are explicitly null in the report and row journal. All 306 ordered Emit rows, including actual IDs, generated registry and emitted PE hashes, matched the prior run. Preflight, state seeds and postflight matched in full. [Frozen protocol](../validation/roslyn-without-allocation-probes.md)

| Observed suspension and wait quantities | Precise reads | Reads omitted |
| --- | ---: | ---: |
| Raw reason-0 suspension starts | 660 | 0 |
| Raw reason-1 collection suspension starts | 75 | 75 |
| Raw reason-2 shutdown suspension starts | 40 | 40 |
| Raw reason-6 GC preparation suspension starts | 12 | 14 |
| Strictly linked blocking GC sequences | 64 | 62 |
| Selected Emit waits bound to a positive caller clock core | 1,910 / 1,913 | 1,930 / 1,932 |
| Bound caller waits overlapping linked blocking GC | 23 / 1,910 | 30 / 1,930 |
| Waits with an awaited-task scheduler pair | 66 | 64 |
| Those waits whose caller core overlaps linked blocking GC | 10 / 66 | 18 / 64 |

The independent raw scan found zero reason-0 starts and zero SampleProfiler events. All 516 suspend/restart phase records reconciled to 129 ordered quartets. Thirteen reason-1 sequences retained unresolved links to collection records. The managed parser processed 385,848 records and aligned all 2,956 markers. The native capture retained 71,790 lifecycle records across 41 identities and 97,210 callback receipts. EventPipe, ETLX and native terminal checks reported zero loss. The native hook order and ownership scope matched the preceding run. The Windows replay, 13 focused analyzer and hook tests, and WSL compilation and capture checks passed.

The targeted removal corroborates the allocation-read attribution. The linked blocking-GC overlap remains observable when both measurement perturbations are absent. GC overlap uses the caller's wait core and a scheduler pair uses the observed caller/task intersection. These counts do not establish overlap at the worker callback itself, any physical delay attributable to either mechanism, or a performance gain. This diagnostic omitted allocation telemetry and does not qualify the original benchmark. #20 remains In Progress and #3 remains Blocked. [Prior attribution](roslyn-allocation-probes.md) · [Delivery](../evidence/roslyn-without-allocation-probes/delivery.json)

The subsequent offline replay located 27 overlaps within the caller/task intersection and placed the entire inner GC interval between worker entry and return receipts in 15 waits. [Worker interval replay](roslyn-gc-task-intervals.md)
