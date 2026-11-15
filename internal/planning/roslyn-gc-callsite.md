# CoreCLR GC wait callsite observed during Roslyn Emit

One diagnostic Roslyn execution on WSL 6.18.58.1 used the exact driver and binary inventory from the run without stack sampling and precise allocation reads. All 306 ordered Emit rows and semantic outputs matched the earlier run, including the emitted PE and registry hashes. The managed channel aligned all 2,956 markers and reported zero EventPipe/ETLX loss or payload errors. Zero stack samples and zero raw reason-0 starts were observed. No Engine source or benchmark settings changed. [Protocol](../validation/roslyn-gc-callsite.md)

The third native channel attached to the owned process before runtime resume and collected 1,128 receipts at the two pinned instructions. All receipts bound to 29 scheduler generations and reconciled to 564 call/return pairs, with no orphan returns, open calls or ambiguous lifetime links. The lifecycle ledger held 74,840 rows and the scheduler callback ledger held 94,824 rows. All three native ledgers passed terminal counters and detached equality. The coordinator closed 39 owned resources without errors.

| Evidence in the same execution | Distinct Emit waits |
| --- | ---: |
| Selected TPL caller/task waits | 1,937 |
| Positive guaranteed intersection of caller wait and awaited task lifetime | 1,807 |
| Complete `WaitUntilGCComplete` callsite pair on the awaited task's worker inside that intersection | 24 |
| Such waits with a scheduler switch strictly enclosed by the callsite pair | 24 |
| Such waits where a callsite pair overlaps a linked blocking-GC inner interval | 13 |
| Such waits with the full linked blocking-GC inner interval strictly between the nested scheduler entry and return receipts | 6 |

The 24 waits have 30 distinct exact callsite pairs and 44 distinct associations with nested scheduler switches. Each of the six strict cases has a distinct callsite pair and a distinct linked GC episode on a separate emitter thread. All six worker sequences were switch-out, waking, wakeup and switch-in in both native slot and recorded clock order. Waking followed the mapped `RestartEEStart` upper edge. In these observed waits the worker traversed `WaitUntilGCComplete`, switched out during that call and woke after GC restart began. Windows and WSL produced byte-identical outputs. Both passed 19 focused tests and a separate raw-ledger audit reproduced the six joins. [Pinned callsite proof](coreclr-gc-wait-callsite.md) · [Delivery](../evidence/roslyn-gc-callsite/delivery.json)

The six cases establish that this CoreCLR path participates in those observed Emit waits. They leave per-thread physical blocking duration, excess runnable delay, the contribution to variance, and generalization to other waits unresolved. Callback timing is conditional on the recorded clock model. This was a traced diagnostic execution. The original benchmark and acceptance gates are pending. #20 remains In Progress and #3 remains Blocked.
