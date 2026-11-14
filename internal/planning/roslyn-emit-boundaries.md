# Roslyn Emit scheduler and GC co-occurrence

The fixed diagnostic corpus completed on WSL 6.18.58.1 with the pinned Roslyn driver and a separate checkout of Engine 55c630f. The enlarged CLR control passed before the one Roslyn run. All 306 Emit rows, 270 measured rows, 2,956 markers and 643,837 parsed EventPipe events passed their completeness checks. Both native ledgers reported zero losses, faults and recursion misses. The 226,844 lifecycle rows established 35 identities, including two initial enrollments. The 175,352 boundary records reconcile to 87,642 pairs, 33 prefixes and 35 retired tails. Nineteen pairs have a retired endpoint and are excluded from correlation. Independent raw replay verified every boundary row and pair. [Frozen protocol](../validation/roslyn-emit-boundaries.md)

| Strictly contained observations within selected Emit waits | Waits |
| --- | ---: |
| Identity-bound caller wait cores | 1,964 |
| Caller scheduler callback pair | 1,654 |
| Awaited task scheduler callback pair in the intersection with its observed execution core | 592 |
| Literal GC suspend or restart boundary | 663 |
| Caller pair and literal GC boundary | 663 |
| Awaited task pair and literal GC boundary | 592 |

The 991 waits with a caller pair and without a contained literal GC boundary are a distinct set of observations. A GC interval could span or touch a wait edge without contributing a contained boundary. Each awaited-task pair above lies inside the intersection of the worker task and caller wait cores. All 592 such waits also contain at least one literal GC boundary somewhere in the caller wait core. This does not place a whole GC pause inside the worker invocation. Counts preserve strict mapping and coverage limits. All pairs are software callback observations, including no-switch returns. GC boundary records establish co-occurrence, while physical scheduler delay, GC pause length and exclusive attribution remain unresolved.

The focused suite passes 24 tests on each of Windows and WSL. The new ledger shares the fixture-validated kernel profile and admits only generations already authenticated by the existing capture flow. The retained CLR median overhead applies to the pipe experiment. This run gives no Roslyn overhead estimate or performance qualification. Engine had uncommitted work in its main checkout, so the diagnostic binds a clean detached checkout of the existing pinned commit. Preparation, both detached ledgers, EventPipe, join outputs and raw replay were retained. [Delivery](../evidence/roslyn-emit-boundaries/delivery.json)

The later reason-aware replay found 592 task-pair waits with sample-corroborated suspension boundaries and 26 with overlap against the strict linked blocking-GC subset. See the [GC replay and limits](roslyn-gc-episodes.md).

The same corpus then completed with the stack sampler disabled. Reason-0 sequences dropped to 660, with 64 linked blocking-GC sequences and 23 caller waits overlapping a linked GC interval. [Provider-only comparison](roslyn-without-stack-sampling.md)
