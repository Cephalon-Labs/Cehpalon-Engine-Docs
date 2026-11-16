# Same-object CoreCLR wait and setter during Roslyn Emit

One WSL 6.18.58.1 diagnostic run added the five-site process-scoped probe to the prior fixed Roslyn configuration. Its binary inventory, 306 ordered Emit rows and semantic outputs match the earlier exact-callsite run. Allocation telemetry remains null and stack sampling remains disabled. All 2,956 markers aligned across 377,275 managed records, with zero reported EventPipe/ETLX loss or payload errors. The native lifecycle, scheduler callback and site ledgers retained 74,684, 90,870 and 2,035 records respectively. All terminal counters and detached second reads reconciled, and cleanup completed. [Protocol](../validation/roslyn-gc-event-object.md)

All 2,035 site receipts bind to a unique native lifetime. They include 594 exact call/return pairs and 593 event-wait branch receipts. One exact invocation has no observed dedicated wait-branch receipt. The 847 object-bearing receipts, including 127 resets and 127 sets, all match one execution-local GCEvent token. The Windows and WSL replays were byte-identical, and 25 focused tests passed on each host. The raw operand register values are retained locally and the exported token ledger reconciles to every raw slot.

| Observed evidence in the same Roslyn execution | Distinct Emit waits |
| --- | ---: |
| Selected TPL waits | 1,957 |
| Positive guaranteed caller/task intersection | 1,805 |
| Awaited worker entered the exact CoreCLR wait callsite and switched inside it | 17 |
| Same-object reset, wait, switch-out and following set before waking and call return | 17 |
| The switch strictly encloses linked blocking GC and both reset and set match its emitter and mapped phase edges | 4 |

In each of the four strict waits the GC emitter reset the same event during the observed suspend phase, and the awaited worker subsequently reached the wait branch and switched out. That GC emitter entered the same object's set branch between the mapped restart edges. The worker's recorded waking, wakeup, switch-in and call return followed. The episodes and callsites are distinct. This is direct evidence of the CoreCLR event identity and setter thread for those observed waits. The exact flag publication, the kernel's wake caller, physical delay and the contribution to overall variance remain unmeasured. [Pinned event-site validation](coreclr-gc-event-object.md)

Among all 64 linked blocking-GC episodes, 54 have a unique reset and set by their emitter strictly inside the mapped suspend and restart brackets. All ten remaining setters fall within the mapped `RestartEEStop` uncertainty bracket. The other suspension classes and their edge cases are retained in the raw replay. This was a single traced diagnostic. #20 remains In Progress, #3 remains Blocked and the original benchmark gates apply. [Delivery](../evidence/roslyn-gc-event-object/delivery.json)
