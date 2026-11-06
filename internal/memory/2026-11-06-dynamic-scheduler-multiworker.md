# Multiworker dynamic scheduler handoff

Start with [ADR0030](../adr/ADR-0030-dynamic-scheduler-admission.md), [fixed multiworker protocol](../validation/dynamic-scheduler-multiworker.md) and [delivery](../evidence/dynamic-scheduler-multiworker/delivery.json). Refresh private repository heads, Project 4 and CI.

One ordered negative/positive attempt passed on pinned WSL. Loss-negative counted 72 attempts, one retained birth and 71 capacity losses. Positive captured 58/58 with zero losses or faults. Both proved three admissions and frees, zero reported recursion misses, matching detached counts and ledger hashes, nonmember exclusion and 28 descriptor closes. A parents B, both park, A is freed while B remains blocked, then C is admitted after B is freed. All three complete the controlled CPU 0 to CPU 1 wake and lifecycle. Native IDs were distinct. Offline fixtures cover numeric reuse after free, collision while live and stale records. Seventy-two offline cases pass per Windows and WSL. Shared verifier logs redact internal addresses with exact raw provenance.

Next establish controlled CLR ThreadPool admission and lifecycle plus measured collection overhead. The fixture is synthetic and leaves pointer reuse, full Roslyn readiness and GC/scheduler attribution unresolved. Keep #3 Blocked, #20 In Progress/P2/M0, original gates, dependencies, benchmark and null hours.
