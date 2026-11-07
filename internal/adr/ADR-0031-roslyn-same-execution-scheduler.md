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
