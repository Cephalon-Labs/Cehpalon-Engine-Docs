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
