# Roslyn raw-state contract and recorded-clock review

Date 2026-11-10. Engine #20, [ADR0031](../adr/ADR-0031-roslyn-same-execution-scheduler.md), [fixed offline protocol](../validation/roslyn-scheduler-state-contract.md). This slice reuses the complete successful 2026-11-07 capture and keeps its original outputs. No native target, BPF attachment, build or benchmark was launched; Engine source is unchanged.

## Source and captured argument contract

The Microsoft release tag `linux-msft-wsl-6.18.54.1` resolves to immutable source revision `d504d40ab83839cb61942a812a99d183c42227b9`. Six kernel files were retained with provenance and SHA-256. The two cached scheduler headers match the immutable-commit copies. Source-contract review passes 21 checks. The captured switch-out bytecode independently matches raw argument 3 at context offset 24, followed by a private preemption bit from argument 0. [Raw callback declaration](https://github.com/microsoft/WSL2-Linux-Kernel/blob/d504d40ab83839cb61942a812a99d183c42227b9/include/trace/events/sched.h#L222).

| Raw retained value | Exact source definition | Added conditional label |
| --- | --- | --- |
| 8193 / 0x2001 | TASK_INTERRUPTIBLE plus TASK_FREEZABLE | off_cpu_sleep_state |
| 258 / 0x102 | TASK_UNINTERRUPTIBLE plus TASK_WAKEKILL, also TASK_KILLABLE | off_cpu_sleep_state |

The [state definitions](https://github.com/microsoft/WSL2-Linux-Kernel/blob/d504d40ab83839cb61942a812a99d183c42227b9/include/linux/sched.h#L103) permit those exact two additions. Freezable does not establish that freezing occurred; killable does not identify IO, GC or any wait cause. Raw argument state differs from the formatted perf state, whose preemption sentinel is 0x100. This collector instead adds private bit 0x80000000. Mixing these encodings would misread raw 258.

The added `wsl618-observed-sleep-v1` profile must be selected explicitly. It selects an assumed source contract, without discovering or attesting arbitrary input kernels; this evidence covers only frozen capture02. The default remains `legacy`. All other combined values, unknown bits, preemption handling and existing ambiguity masks retain their previous behavior. Exhaustive 16-bit state and corresponding preempt inputs are covered, alongside initial-prefix, wake-in-progress, tie and mask tests. Final focused tests pass 118 each on Windows and WSL.

The scheduler's [pending-signal path](https://github.com/microsoft/WSL2-Linux-Kernel/blob/d504d40ab83839cb61942a812a99d183c42227b9/kernel/sched/core.c#L6546) updates the state passed to the trace when cancellation leaves the task runnable. Proxy execution can retain mutex-blocked tasks on the runqueue. The label therefore remains conditional raw-state interpretation and cannot certify physical blocked or runqueue time. Tag, recorded release, BTF and captured-byte checks provide provenance; exact installed-image or executing-JIT attestation is absent.

## Fixed pair and complete accounting

The ordered offline pair runs legacy first, then the explicit profile, against identical frozen raw ledger and managed lineage. Legacy wait bytes match the original `scheduler-joins03` exactly, and its summary matches after removing the new explicit profile metadata. All 39 identities, 1,909 caller queries, literal GC associations, point bindings and recorded-order masks stay identical. The raw-only independent audit imports no production decoder and passes 95,601 checks, including every caller partition and all 1,820 overlapping worker partitions. Labels change in 1,455 caller queries and 569 worker overlaps, strictly from unknown to the two declared raw-state labels.

The following nanosecond values are unions of conditional recorded callback labels in selected wait cores. They are not certified physical scheduler service or delay.

| Conditional recorded label | Legacy | Explicit source profile |
| --- | ---: | ---: |
| running_observed | 97,069,588 | 97,069,588 |
| runnable_observed | 18,967,858 | 18,967,858 |
| off_cpu_sleep_state | 0 | 5,122,566,326 |
| unknown | 5,188,342,231 | 65,775,905 |
| Total selected caller-core union | 5,304,379,677 | 5,304,379,677 |

Independent supplementary accounting assigns all remaining 65,775,905 ns to 1,653 union-clipped intervals preceded by a recorded waking point. This is a literal point category, with no certified physical wake latency, GC or scheduler cause.

The 48,056 literal GC boundaries and 677 waits containing a boundary are unchanged. Neither profile supplies a certified GC pause total or an exclusive GC/scheduler share. A smaller unknown label partition is an analysis correction, with no measured Engine speedup.

## Timestamp contract clarification

Independent raw replay reproduces 740 global reversals, 50 ties and 13 within-generation reversals. Every reversal pair crosses emitter CPUs; per-CPU subsequences have zero reversals and ties in this retained ledger. The five main-generation masks intersect the selected caller-core union by exactly zero nanoseconds. These observations allow comparison with unchanged masks, but do not isolate why recorded time and reservation order disagree.

The nine emitting programs place helper 5 after slot reservation and helper 8. The published [helper implementation](https://github.com/microsoft/WSL2-Linux-Kernel/blob/d504d40ab83839cb61942a812a99d183c42227b9/kernel/bpf/helpers.c#L177) calls `ktime_get_mono_fast_ns()`. Its [timekeeping source](https://github.com/microsoft/WSL2-Linux-Kernel/blob/d504d40ab83839cb61942a812a99d183c42227b9/kernel/time/timekeeping.c#L425) explicitly allows backward observations during some updates. Reservation placement and this clock behavior are possible mechanisms, with no evidence selecting one as the cause of any particular inversion.

The [switch trace call](https://github.com/microsoft/WSL2-Linux-Kernel/blob/d504d40ab83839cb61942a812a99d183c42227b9/kernel/sched/core.c#L6941) precedes `context_switch`. Its in/out callback timestamps do not mark exact CPU dispatch or withdrawal. The existing masks expose visible conflicts; they do not bound all timestamp error. This clarifies the earlier report's placement explanation without altering its retained results.

## Delivery and next scope

The [Samples capsule](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/tooling-traces/evidence/2026-11-10-scheduler-state-contract) retains source acquisitions, frozen inputs/source, both complete analyses, tests and independent reviews with deterministic compression and SHA-256. Its [delivery](../evidence/roslyn-scheduler-state-contract/delivery.json) identifies the technical revision and manifest. Original native/managed traces and redacted verifier copies remain in the prior capsule; no new kernel-address redaction is introduced in this offline slice. Source tag acquisition fallback is recorded and no failed workload is hidden.

Next work for physical scheduler-duration claims needs a separately frozen clock-error and switch-boundary protocol with entry/exit/sequence/CPU observations and an independently justified error envelope. A repeated unchanged Roslyn run or a favorable zero-reversal fixture cannot resolve that source-level limitation. GC pause pairing remains separately unresolved. No Engine optimization follows solely from the refined labels. #20 remains In Progress/P2/M0 with Planned gates and null actual/remaining hours, #3's entire row stays Blocked, and the original benchmark is unchanged. Hosted CI remains payment/spending blocked before steps.
