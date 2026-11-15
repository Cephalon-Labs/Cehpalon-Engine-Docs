# CoreCLR newborn callsite fixture handoff

Read the [report](../planning/coreclr-gc-wait-newborn.md), [protocol](../validation/coreclr-gc-wait-newborn.md) and [delivery](../evidence/coreclr-gc-wait-newborn/delivery.json). A single TGID-scoped uprobe-multi link attached the two pinned sites before the creation of two owned workers. Fresh scheduler generations 4 and 5 recorded complete lifetimes and two and six callsite pairs. A same-image peer exercised two pairs without any leak. Both target no-GC arms were empty.

Initial audit rejected 16 receipts on pre-existing owned threads. The corrected offline replay accounted for these eight pairs separately from the newborns, and all 32 receipts reconciled with no losses, faults or recursion misses. Keep the original failed audit report and frozen source. No second capture. Full Roslyn capacity and task/GC join remain ahead, with no physical wait or benchmark outcome. Keep #20 In Progress, #3 Blocked and original gates.
