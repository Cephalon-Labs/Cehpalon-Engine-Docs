# Optional audit read statistics

Declared 2026-11-23 under #18 with #7/#8 authority regressions. The read
timeout contract follows ADR-0051. A project may pass an owned collector to
the history, lookup and resource history readers. The optional collector
keeps four cumulative counters with independently sampled values and stores
no tenant, resource, principal, exception or payload information. A selected
Sample host may share one collector between receipt lookup and resource
history, independently of the timeout response flag. Counters apply after
reader prechecks and describe the reader outcome before response serialization.

Verify all three Engine readers, including initial denials and cancellation,
disabled activation, legacy and typed deadlines, caller-first cancellation,
foreign provider failures, awaited providers and concurrent sharing. Run the
HTTP and GraphQL contract suites and the existing offline and real-provider
wire suites with locked dependencies.

Use the owned PostgreSQL 18.7 fixture with Npgsql 10.0.3 on WSL. Run the 20
HTTPS timeout controls once with collection off, then run all 20 with it on.
For each transport and reader, verify typed and legacy deadline, foreign
provider timeout, caller cancellation and cross-tenant denial. Require an
observed backend lock wait before expiry or abort, quiescence with the lock
still held, and successful reuse. While a read is still active, the counter
must remain unchanged. Require zero SQL calls and zero counts on the
cross-tenant denial. A mixed GraphQL document must yield two successes on the
same collector. Disabled transports must leave the collector absent.

This is a correctness run. The existing timed benchmark protocol and gates,
issue #3 Blocked, and feature maturity continue to apply.

## Results

The locked .NET 11.0.100 build passed 262 Audit Trail, 53 HTTP and 49
GraphQL checks. The Samples offline and PostgreSQL wire suites each passed
eight checks. The Windows sample built with zero warnings and errors and
returned the setup guide when launched without arguments.

Both HTTPS modes passed all 20 scenarios with identical public outcome
codes and status. Each mode observed 12 real PostgreSQL lock waits and
verified backend quiescence before unlocking. Four cross-tenant requests
per mode issued no protected handler calls or SQL reads. The enabled mode
also verified 20 counter transitions, including a success after each
control. A mixed GraphQL document executed two separately authorized
reads and recorded two successes on the same collector. With both
transports disabled, the collector remained absent.

The seeded dataset contained 512 resource records and 128 distractors. A
plain provider timeout was injected after an actual SQL read to check its
classification. The fixture retained its data and stopped with its
loopback port closed. Counters were verified without a latency or
allocation measurement.

Hosted Engine checks passed at the same revision. The artifacts report
1,540 Windows and 1,537 Ubuntu component checks, including the three
targeted suites. The SDK and driver smoke jobs passed on both runners.

[Machine-readable reports and verifier](../evidence/audit-read-statistics/2026-11-23)
[Engine commit](https://github.com/Cephalon-Labs/Cehpalon-Engine/commit/f77c42b187483086e99a5ec5ade6bcd80b9ad738)
[Samples commit](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/commit/516861095f7950950ea8db8801596fa1ab194d67)
[Engine contract workflow](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/45158542258)
[Engine platform smoke workflow](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/45158542282)
