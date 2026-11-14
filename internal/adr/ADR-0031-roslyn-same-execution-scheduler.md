# ADR-0031 Join Roslyn task observations to scoped scheduler identities

- Status. Accepted for one bounded diagnostic lane
- Date. 2026-11-07
- Deciders. Cehpalon program, Engine #20

## Context and decision

ADR0030 established kernel birth, target-side wake/switch, retirement, loss rejection and a real CLR ThreadPool callback. The retained Roslyn TPL execution has no scheduler channel. Run the full original generator diagnostic corpus again with CLR/TPL and a process-scoped scheduler ledger in the same execution. Reuse the byte-identical prebuilt driver, locked compiler inputs and established EventPipe parser.

An existing main caller and startup worker have a left-censored lifetime when capture begins. Bind a stable, held ordinary process cohort through pidfds while the runtime's reverse diagnostic port is suspended. The first syscall by an authenticated pre-arm task enrolls its current kernel identity and emits a distinct initial record. Record earlier state as unknown. Post-arm children keep complete birth records. Require caller enrollment before each measured interval being classified. Generation keys remain private. Bounded raw hook membership checks happen before task field reads. A finite cohort cannot establish coverage of every short-lived unbound runtime thread.

The EventPipe collector starts only after lifecycle hooks and initial enrollment hooks are armed. It and the managed target run at UID/GID 1000 with a private owned reverse-port directory. Root owns BPF descriptors and scoped proc verification. Extend the existing capture helper with disabled-by-default lifecycle hooks and child identity options, and update its pinned historical caller to the exact new helper hash. This keeps the original entrypoint behavior and puts scheduler attachment before diagnostic resume.

## Trade-offs and consequences

The separate historical EventPipe and scheduler captures cannot establish overlap from the same execution. Combining the channels adds instrumentation overhead, which has only been measured for the bounded CLR fixture. Scheduler capacity is fixed before launch. Any overflow or collection fault invalidates complete classification. Missing thread or clock coverage produces an explicit unknown result.

Match EventPipe points to exact MONOTONIC intervals using all marker/sidecar brackets. A native TID link requires strict containment in one owned generation. Preserve generation boundaries, reuse ambiguity and unknown prefixes. Scheduler residency describes guest execution states. Same-execution overlap with a GC event is a literal observation. The old GC pairing models remain uncertified because suspend/restart source paths have asymmetric calls and retries. Preserve GC boundary events and unknowns without constructing a pause total or subtracting an exclusive scheduler share.

The actual ledger contains recorded timestamps that reverse physical ticket order. Mask each visible inversion or tie through the next unambiguous state-setting point and preserve the original slots. Any remaining interval label is conditional on recorded callback timestamps. Report identity-bound points and transitions as the primary native evidence. Exact CPU, blocked and scheduler-delay durations need further timestamp validation.

## Actions

Validate the enlarged profile on a separate controlled CLR actor, run one full generator lane, audit the original corpus and raw channels, then classify only bounded observations. Keep #3 Blocked and #20's metadata, planned gates, null hours and original benchmark. Product changes require evidence of safe avoidable Engine work.

## 2026-11-10 offline state-contract continuation

Accept the [bounded offline protocol](../validation/roslyn-scheduler-state-contract.md) and [source/clock review](../planning/roslyn-scheduler-state-contract.md). A separately selected profile adds only exact raw8193 and258 conditional sleep-state labels; legacy remains default and recorded-order masks remain unchanged. Physical scheduler duration and causality remain uncertified. The helper5 fast-clock and pre-context-switch callback contracts supply additional timing limitations; publication placement alone does not explain the observed reversals. Require a separately frozen error-envelope/boundary protocol before physical-duration claims, with no unchanged Roslyn rerun merely to improve labels.

## 2026-11-10 owned callback clock controls

Accept the separately frozen [clock-bracket protocol](../validation/scheduler-clock-brackets.md) and [bounded observations](../planning/scheduler-clock-brackets.md). One negative/fresh positive sys_enter-only owned actor pair compares inner callback-body fast points with containing raw non-fast monotonic reference reads. The accessors share a clocksource; finite brackets do not establish universal or historical errors or physical switch timing. The source/BTF-feasible sched_entry_tp/sched_exit_tp hooks require a later explicit attachment/current-invocation/lifecycle gate; CPU-only pairing is invalid and newborn/no-switch paths need controls.

## 2026-11-10 scoped scheduler entry/exit fixture

Accept the [fixed boundary fixture](../validation/scheduler-boundary-fixture.md) and [observed result](../planning/scheduler-boundary-fixture.md). Two current-task hooks use a separate ABI with owned leader/private generation identities; classify per-generation invocation order, including seeded/newborn prefixes and returned-retired/unreturned tails. Native false coverage is observed or unobserved from fixed yield opportunities, with no favorable repeat. Physical duration and GC attribution remain uncertified. A CLR ThreadPool boundary fixture and fresh overhead controls must be separately scoped before a Roslyn lane.

## 2026-11-15 CLR ThreadPool boundary fixture

The [CLR fixture](../planning/clr-threadpool-boundary.md) binds the named managed callback to worker-only scheduler boundary records and measures incremental observer overhead. The new WSL profile is pinned to this fixture. The resulting callback observations provide the basis for a separately frozen Roslyn lane with its own timing and GC gates.

## 2026-11-15 Roslyn boundary correlation

The [full diagnostic lane](../planning/roslyn-emit-boundaries.md) adds scheduler entry and return to the authenticated lifecycle ledger. It matches pairs to strict EventPipe wait and task cores. Retain GC overlap as literal co-occurrence and require an independently verified CLR suspend/restart pairing contract for timing or attribution.
