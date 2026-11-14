# Scoped scheduler entry/exit fixture

Date 2026-11-10. Engine #20, [ADR0031](../adr/ADR-0031-roslyn-same-execution-scheduler.md), [fixed protocol](../validation/scheduler-boundary-fixture.md). The prior [clock-bracket fixture](scheduler-clock-brackets.md) established bounded syscall-callback observations and source feasibility for the two scheduler hooks. This slice attaches those hooks to an owned synthetic leader and one dynamic worker. No Roslyn, Engine source, build, original benchmark, GC-policy or global host setting change occurred.

## Actual attachment and fixed results

The first ordered native01 attempt completed the capacity-negative and fresh positive cases. Exact fdinfo receipts bind `sched_entry_tp` and `sched_exit_tp`; the nine legacy lifecycle hooks retain their existing ABI and compiled bounds. Before task-storage admission, owner and root nonmember yield controls emitted nothing. After admission, each actor performed the fixed 64 yields in alternating CPU batches, created one worker, parked it in a private pipe read on CPU 1, then woke it from leader CPU 0 and joined it.

| Case | Boundary attempts | Retained | Publication losses | Legacy rows | Worker admissions/frees | Owned native FD closes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Capacity-negative, logical limit 1 | 184 | 1 | 183 | 24 | 1 / 1 | 32 |
| Fresh positive, limit 1024 | 182 | 182 | 0 | 20 | 1 / 1 | 32 |

Both full ledgers and terminal counts match their detached second reads/hashes. Unused slots are zero. Reported faults and recursion misses are zero; cleanup has no errors or forced actor kills. Held leader identity, ordinary credentials, alias cookie and post-reap storage absence reconcile. Source freezes cover 105 tool files and three interpreter/libc/BTF artifacts, unchanged around execution. The leader's final command-pipe read is observed before detachment, avoiding a race with its final scheduler entry.

The positive reservation-order classification conserves every boundary row:

| Observed category | Count |
| --- | ---: |
| Complete saved-invocation pairs, `is_switch=true` | 25 |
| Complete saved-invocation pairs, `is_switch=false` | 64 |
| Leader left-censored initial exit | 1 |
| Owned newborn exit prefix | 1 |
| Leader invocation open at detach | 1 |
| Unreturned retired-worker invocation at closed lifetime | 1 |
| Accounted rows: 2 x 89 pairs + 4 single boundaries | 182 |

Nine complete pairs begin and end on different emitter CPUs. They remain valid generation-local saved-invocation pairs; a CPU-only matcher would use the wrong relationship. All retained raw bools are 0/1. All observed entry-mode booleans are false, so native preempt-mode-true coverage remains unobserved. A separate offline assertion confirms entry(true) and exit(false) remain distinct, valid model fields. This finite positive sample has no recorded callback-body or per-generation adjacent fast-time reversals, and no CPU change within an individual callback body. These observations establish no universal timing guarantee.

The 64 no-switch pairs are observed coverage from the fixed yield opportunities, without claiming that each was independently identified as one specific syscall callsite. Had they been absent on the shared host, the declared result would have been unobserved runtime coverage, with no selected rerun. Offline no-switch and other adverse cases remain tested.

## Ownership and source interpretation

Boundary callbacks authenticate either the seeded current leader cookie (generation 0) or the private current-task member key plus exact birth check (worker generation 1) before owner field reads/output. The existing untyped-current helper35 private key convention is preserved; raw callback argument 0 is decoded solely as bool. The boundary ledger uses a separate ABI. The offline analyzer keeps pending invocations by generation. Retired members may still complete scheduling invocations during exit cleanup; retirement is not treated as immediate nonreturn.

Exact [scheduler source](https://github.com/microsoft/WSL2-Linux-Kernel/blob/d504d40ab83839cb61942a812a99d183c42227b9/kernel/sched/core.c#L6817) defines entry bool as the comparison with SM_PREEMPT. Entry(false) is not a general voluntary-blocking oracle. Exit bool records the saved invocation's `prev != next` branch, not uninterrupted CPU residence. The [raw declarations](https://github.com/microsoft/WSL2-Linux-Kernel/blob/d504d40ab83839cb61942a812a99d183c42227b9/include/trace/events/sched.h#L882) and exact BTF/raw link receipts identify the two named hooks.

The [newborn schedule_tail path](https://github.com/microsoft/WSL2-Linux-Kernel/blob/d504d40ab83839cb61942a812a99d183c42227b9/kernel/sched/core.c#L5258) explains why an owned newborn can have exit(true) before its own first entry. That category requires the separate complete birth/lifetime evidence and differs from the seeded leader's unknown initial prefix. The final retired-worker entry has no captured return before its independently closed lifetime. It is classified literally, without identifying the exact do_task_dead callsite from these callbacks. The leader's final open entry remains a right-censored detach boundary.

Pairing uses per-generation reservation order and explicit entry ordinal; it never sorts by CPU or timestamps. Backwards fast points are retained observations in the model, and do not manufacture/drop pairs. Numeric software-callback points do not establish exact physical CPU, blocked or runqueue duration. The fast and raw reference accessors share the kernel clocksource; no earlier synthetic bound is transferred to this capture or to historical Roslyn data.

## Verification and delivery

The pure parser was developed in an isolated worktree; its two files were integrated by the sole root writer. Sixteen parser edge cases plus four structural hook tests pass, and the complete focused regression passes 144 each on Windows and WSL. They cover cross-CPU pairing, true/false bools, newborn/seeded prefixes, returned-retired cleanup, unreturned tails, loss, malformed identities/ordinals/bools, nested/duplicate edges and timestamp reversal. The source audit passes 26 checks, an independent source interpretation replay passes 553 checks, and the independent raw data and bytecode replay passes 3,473 checks. The latter preserves its first failed assertion, which assumed identical historical builder source. The reviewed difference parameterizes the generation limit. The current lane uses the same limit of three, and the normalized instructions match the historical programs. Its first macro-name assertion failure, corrected audit and acquisition receipts are retained; no native attempt ran that audit code. Source readiness corrections (helper35 and held-leader/EAGAIN oracle) were completed before the first native freeze.

[Delivery](../evidence/scheduler-boundary-fixture/delivery.json) and the local Samples capsule retain the frozen protocol/source, raw ledgers, actor references, failed audit preparation, tests and independent reviews with SHA-256. Shared verifier copies redact actual kernel-address literals; exact local originals and hashes are retained. Source, BTF and loaded-byte receipts are observational provenance, without immutable running-image/JIT attestation.

## Next scope and limits

The two hooks now have actual bounded attachment and dynamic-worker evidence. Before using them with Roslyn, separately freeze a real CLR ThreadPool boundary fixture and new observer-overhead controls; the earlier collector overhead series does not quantify these additional callbacks. Preserve newborn, no-switch, migration, open-lifetime and data-loss controls and actual raw identities in that lane.

This synthetic slice establishes no GC pause total, exclusive GC/scheduler cause, Engine speedup, historical Roslyn qualification or general capture readiness. #20 stays In Progress/P2/M0 with Planned test/benchmark gates and null hours; #3's entire row stays Blocked, and the original benchmark is unchanged. Hosted CI is still payment/spending blocked before steps.

On 2026-11-15 the tracking dry run rejected the Engine repository privacy check. GitHub reported Public visibility for Engine, Docs and Samples. The issue update and both repository pushes remain pending. The proposed #20 body is ready locally, and the GitHub readback baseline remains the last observed private delivery.
