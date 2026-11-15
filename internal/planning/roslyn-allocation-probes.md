# Precise allocation reads explain residual Roslyn trace suspensions

An offline replay of both #20 traces links all 660 caller-thread reason-0 suspension sequences in each trace to the diagnostic driver's precise allocation reads. The frozen driver calls `GC.GetTotalAllocatedBytes(precise: true)` twice per `Execute` invocation. There are 330 invocations across 12 preflight, 12 seed, 36 primer and 270 measurement rows. The first read takes place during setup before the compiler timer starts. The second follows the compiler timer end and precedes the setup marker, which is emitted after measurement. The pinned CoreCLR dispatch selects a native QCall that uses `SuspendEE(SUSPEND_OTHER)` to inspect the thread allocation contexts and then calls `RestartEE`. [Managed dispatch](https://github.com/dotnet/dotnet/blob/5254d8bcf59917edc1e1abc33bdf2442b77b1c70/src/runtime/src/coreclr/System.Private.CoreLib/src/System/GC.CoreCLR.cs#L446-L459) · [Native implementation](https://github.com/dotnet/dotnet/blob/5254d8bcf59917edc1e1abc33bdf2442b77b1c70/src/runtime/src/coreclr/vm/comutilnative.cpp#L929-L955)

The replay rebuilt the conditional EventPipe-to-Stopwatch clock bounds from all 2,956 markers in each trace. It matched the exact emitter identity and four raw phases to one pre-read and one post-read window per invocation. All 330 pre-read sequences in each trace were strictly within setup. An additional 50 sampled and 94 provider-only post-read sequences started strictly after the latest possible compiler timer end. The other post-read starts fall within the uncertainty at that clock edge. Every post-read sequence was assigned to one disjoint window before its setup marker. The attribution combines pinned source order and same-thread event placement. The phase records contain no direct native callsite receipt.

| Reason-0 accounting | Stack sampling on | Stack sampling off |
| --- | ---: | ---: |
| All reason-0 sequences | 11,191 | 660 |
| Caller sequences matched to the precise-read windows | 660 | 660 |
| Sequences on the other emitter with in-window sample records | 10,509 | 0 |
| Sequences on the other emitter without in-window sample records | 22 | 0 |
| Bound Emit waits strictly containing any phase of a matched precise-read sequence | 0 | 0 |

The 22 sequences without corroborating sample records share the sampled run's other emitter with the corroborated sequences. They retain that observation without a direct sample match. The precise-read suspensions explain the residual reason-0 population, but their phase boundaries do not participate in the selected Emit wait joins. The 64 previously linked blocking-GC sequences per trace and observed wait overlaps remain separate evidence. There is still no causal or physical duration estimate for GC or scheduler delay during Emit. [GC replay](roslyn-gc-episodes.md) · [Provider-only comparison](roslyn-without-stack-sampling.md)

Windows and WSL replayed both runs with byte-identical match records and summaries. The Samples capsule contains the exact receipts, source provenance and analysis hashes. This delivery changes the offline analysis only. It runs no new workload, makes no Engine optimization and retains the benchmark protocol and #20 acceptance gates. [Delivery](../evidence/roslyn-allocation-probes/delivery.json)

The subsequent diagnostic omitted both reads with stack sampling still off. Raw reason-0 starts fell to zero while all 306 ordered Emit outputs matched the prior run. [Controlled omission](roslyn-without-allocation-probes.md)
