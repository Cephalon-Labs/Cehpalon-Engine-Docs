# Roslyn same-object wait/setter handoff

Read the [report](../planning/roslyn-gc-event-object.md), [protocol](../validation/roslyn-gc-event-object.md) and [delivery](../evidence/roslyn-gc-event-object/delivery.json). One exact low-perturbation 306-row run recorded 2,035 receipts, 594 call/return pairs and one event token across all 847 object operands. Seventeen awaited-worker calls have same-object reset, wait, switch-out, set and wake order. Four distinct waits and linked blocking-GC episodes also pass emitter identity and strict suspend/restart phase edges.

Across all 64 blocking-GC episodes, 54 have both strict emitter edges and ten set receipts at the mapped restart-stop uncertainty edge. Never publish the private operand ledger. The exact setter site is before signal publication and the kernel waker is not observed. No physical split, variance cause, workload optimization or canonical benchmark result. Preserve #20 In Progress, #3 Blocked and original gates.
