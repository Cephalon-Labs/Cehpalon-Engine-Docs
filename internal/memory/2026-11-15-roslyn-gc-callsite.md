# Roslyn GC wait callsite handoff

Read the [report](../planning/roslyn-gc-callsite.md), [protocol](../validation/roslyn-gc-callsite.md) and [delivery](../evidence/roslyn-gc-callsite/delivery.json). One intact diagnostic corpus of 306 rows used the pinned low-perturbation driver. The process-scoped callsite ledger recorded 1,128 receipts, 564 pairs in 29 admitted generations and zero unresolved endpoints. All native loss, fault and recursion counts were zero. Detached reads and cross-host offline joins matched.

There are 24 measured Emit waits with exact awaited-worker callsite and strict nested scheduler switches. In six, the entire linked blocking-GC interval is between those scheduler receipts, with waking after mapped RestartEEStart. This identifies the runtime path in those six waits. It leaves physical GC/scheduler duration and variance cause open. Preserve #20 In Progress, #3 Blocked and original benchmark gates.
