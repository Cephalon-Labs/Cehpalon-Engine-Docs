# Same-execution Roslyn scheduler observations

Date 2026-11-07. Engine #20, [ADR0031](../adr/ADR-0031-roslyn-same-execution-scheduler.md), [frozen protocol](../validation/roslyn-scheduler-correlation.md).

The completed lane reuses the byte-identical prebuilt generator driver and pinned compiler/runtime inputs. It retains all 306 Emit rows, including 36 primers and 270 measurements, and all 2,956 stage markers. The same execution contains 667,188 parsed managed events, 233,835 stack records and 243,270 scoped scheduler rows. Managed marker parity, sample parity, payload and reported loss gates pass. TPL observes 19,466 complete execution-event histories, 65,562 records and zero malformed or unfinished waits.

The native ledger has two authenticated initial enrollments and 37 observed births. All 39 generations reach exit, terminal switch and free, with zero reported loss, faults and recursion misses. The initial main generation starts its coverage at enrollment. Its earlier lifetime remains unknown. Both detached ledger reads reconcile. The independent native audit passed 1,222,250 checks, and the preparation audit passed 132.

The first passive freeze stopped at Git's ownership guard before any target. The first actual Roslyn launch then stopped before scheduler attachment and EventPipe collector launch because CoreCLR had not yet mapped at the initial readiness sample. The exact runtime and stable-cohort readiness check corrected that preparation issue before the complete ordered conformance and capture. Failed receipts and source versions remain retained. Ordinary target identity is independently recorded. Collector identity and IPC ownership are source-enforced, with no separate collector proc-status or IPC-stat receipt.

## Recorded ordering and GC limits

Physical ticket order contains 740 adjacent timestamp reversals and 50 ties globally. Within a generation there are 13 reversals. The callback reads its timestamp after reserving a publication slot, so publication order and recorded-time order can differ. The offline model retains original slots and makes affected labels unknown through a later definite reset. It reports conditional recorded labels and identity-bound transition points. Those labels do not establish exact CPU or runqueue service.

GC suspend and restart boundaries retain exact event metadata and emitter headers. Literal overlap with a TPL wait or a scheduler label is retained, with no certified pause pairing. The earlier asymmetric/retry-path uncertainty remains. The new data supports explicit same-execution identity and point observations. Any optimization still needs evidence of safe avoidable Engine work.

## Identity-bound wait observations

All 1,909 distinct synchronous caller waits strictly contained in the guaranteed cores of the 270 measured Emit rows bind to the enrolled main generation. The clock-offset intersection is 1,671 ns wide. Whole retained point-corpus bindings include all 4,886 caller WaitForWorkers points, 10,973 compiler-pool points and 71 compiler-frame points without the pool label. These point counts include primers and other retained scopes; they are not measured-wait sample counts.

The target emits 48,056 literal GC suspend/restart boundaries, 12,014 of each retained boundary name. At least one boundary is strictly contained in 677 selected wait cores. This establishes co-occurrence only. Independent integer-clock brute-force association and partition accounting passed 5,727 checks. Worker task execution bindings remain in each wait record without constructing an exclusive worker or causal total.

The caller wait-core union is 5,304,379,677 ns. Its conservative recorded-label partition contains 97,069,588 ns running, 18,967,858 ns runnable and 5,188,342,231 ns unknown. These are conditional callback labels, with no certified CPU, blocked or scheduler-delay duration. The model deliberately leaves unfamiliar switch-state values unknown. The main actor's raw switch-out states include 8,193 (7,262 records) and 258 (2,303 records), alongside 0, 1, 2, the preemption bit and terminal 128. Exact host-kernel state-mask semantics require a separately declared decoder validation before refining those labels. Five main-generation ordering masks are small, explicit intervals; they do not explain away the much larger unknown partition.

## Verification and retention

The final 112 focused tests pass on both Windows and WSL. The original EventPipe helper self-test passed ten checks. Agent reviews supplied the independent native and preparation audits; the integrator completed the offline join and independent accounting review after two agents reached their execution limit. The audits' current-source equality statements refer to their recorded execution time. After capture, only the offline decoder among the 30 capture-frozen sources changed, adding explicit ordering masks; original and final versions remain retained.

Two partial offline analyses were stopped only at their owned analysis process: the first repeatedly scanned scheduler points, and the second reparsed GC clock fractions about 92 million times. The corrected offline implementation uses indexed point times and precomputed exact GC bounds. Full inputs are unchanged, the successful output is `scheduler-joins03`, and both partial outputs and source freezes are preserved. Initial test-discovery and audit-script preparation failures are also retained.

The [Samples evidence capsule](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/tooling-traces/evidence/2026-11-07-roslyn-scheduler) retains the original traces, binary ledger, all attempts, source freezes, joins and audits with lossless compression and SHA-256 manifests. Shared verifier-log copies mask only actual kernel-address literals; originals remain local with exact hashes. [Delivery](../evidence/roslyn-scheduler-correlation/delivery.json) identifies the final technical revision and retention manifest.

No Engine optimization is justified by this lane. General capture readiness remains false; this lane establishes only its bounded admitted population and recorded observations. Next validate the exact kernel switch-state masks and recorded timestamp/order contract on bounded fixtures, then revisit the retained Roslyn data. GC source pairing remains unresolved. The original untraced benchmark is not rerun or requalified. #20 remains In Progress/P2/M0, both gates Planned and hours null; #3's complete tracking row remains Blocked and unchanged. Hosted CI is still payment/spending blocked before steps.

## 2026-11-10 clarification

The [offline source and clock review](roslyn-scheduler-state-contract.md) validates exactly raw8193 and258 under an explicit profile and retains all original results and masks. It also establishes two additional limits: helper5 uses a fast accessor whose source permits backward observations, and the switch callback precedes context_switch. Reservation placement is a possible ordering mechanism and does not isolate the cause of the retained inversions. The earlier numerical observations remain historical legacy-profile results, with no certified physical-duration or causal promotion.
