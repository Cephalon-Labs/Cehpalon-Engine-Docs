# Roslyn Emit GC episode replay

This replay uses the retained 306-row diagnostic and its 1,964 identity-bound waits. It checks all 45,272 phase rows against raw EventPipe bytes as decoded by the original reader. All rows reconcile into 11,318 strict four-phase sequences within native emitter generations. Grouping is scoped to the emitter and CLR instance because a suspend begin can precede the ThreadStore lock, a restart end follows release, and the debugger retry can produce restart events before the eventual suspend end. The analysis preserves uncertainty if the stream deviates from the expected phase sequence. [Suspend and restart source](https://github.com/dotnet/dotnet/blob/5254d8bcf59917edc1e1abc33bdf2442b77b1c70/src/runtime/src/coreclr/vm/threadsuspend.cpp#L5378)

| Classification | Sequences |
| --- | ---: |
| Reason 0 with retained stack samples between suspend end and restart begin | 10,509 |
| Reason 0 with no retained sample inside that interval | 682 |
| Reason 2, AppDomain shutdown | 40 |
| Reason 6, GC preparation, unresolved as a collection interval | 12 |
| Reason 1, blocking collection linked to one nonconcurrent GCStart/GCEnd pair | 64 |
| Reason 1, collection link unresolved under the strict filter | 11 |

The collector enabled managed stack sampling. Its exact pinned CoreCLR implementation calls SuspendEE with SUSPEND_OTHER and restarts after walking stacks. All 209,518 retained sample records fall inside reason-0 sequences with sample corroboration. Reason 0 alone leaves the specific caller unknown. The literal event prefix GC does not select a collection reason. [CoreCLR sample profiler](https://github.com/dotnet/dotnet/blob/5254d8bcf59917edc1e1abc33bdf2442b77b1c70/src/runtime/src/coreclr/vm/eventing/eventpipe/ep-rt-coreclr.cpp#L149) · [Runtime reason enum](https://github.com/dotnet/dotnet/blob/5254d8bcf59917edc1e1abc33bdf2442b77b1c70/src/runtime/src/coreclr/vm/threadsuspend.h#L169)

For the 64 accepted blocking links, the suspend reason, retained same-emitter identity, CLR instance, nonconcurrent type, depth and collection count corroborate one matched collection inside the phase pair. The counter at SuspendEE start is the current GC index. The strict gate looks for the next collection only; transitions with a background collection, skipped counts or preparation retain their own records. The 64 conservative inner intervals are disjoint in this trace. [GC count source](https://github.com/dotnet/dotnet/blob/5254d8bcf59917edc1e1abc33bdf2442b77b1c70/src/runtime/src/coreclr/gc/interface.cpp#L1855) · [CLR event schema](https://github.com/dotnet/dotnet/blob/5254d8bcf59917edc1e1abc33bdf2442b77b1c70/src/runtime/src/coreclr/vm/ClrEtwAll.man#L492)

| Wait observation | Waits |
| --- | ---: |
| At least one literal suspend/restart event in the original replay | 663 |
| Original awaited-task scheduler pair and literal boundary | 592 |
| Such task-pair waits with a literal boundary from sample-corroborated reason 0 | 592 |
| Positive overlap with a strict linked blocking-GC inner interval | 27 |
| Awaited-task scheduler pair and positive linked blocking-GC overlap in the caller wait | 26 |

The possible outer-envelope overlap covers the same 27 waits under this strict collection subset. Other kinds of GC activity remain unresolved here. A confirmed GC interval within the caller's wait does not identify why the awaited worker was delayed. In particular, the two conditions in the last row may occur at different instants inside the caller wait. These observations distinguish sampler-induced suspension evidence from source-linked collection evidence. Physical pause totals, exclusive GC/scheduler shares and an Engine optimization are still unsupported.

Passed 23 focused tests each on Windows and WSL. Raw replay matches every phase to its original index, while a separate audit verifies exact phase accounting, unchanged hashes and the joint counts above. The first source acquisition recorded three obsolete paths and their HTTP errors. A subsequent source lookup resolved the relevant moved files in the official pinned tree. Both receipts are retained. [Protocol](../validation/roslyn-gc-episodes.md) · [Delivery](../evidence/roslyn-gc-episodes/delivery.json)
