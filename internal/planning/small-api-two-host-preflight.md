# Small API two-host TLS preflight plan

Predeclared 2026-11-24 for the .NET 11 GA Small API fixture and original
W0 workload. Unit and integration gates apply before any reference
timing is eligible.

- Preserve the local loopback mode, case inputs, collector, rate
  schedule, lifecycle budget checks and scoring. Add a Linux
  controller on the app host and launch the existing .NET driver
  on a second Linux machine under a pinned SSH host key. The
  app uses a dedicated private IPv4 listener and a short-lived fixture
  certificate with that IP in its SAN. Use the standard .NET chain
  and endpoint checks with only the fixture CA.
- Keep the server key on the app host. Transfer only the public CA
  and verify identical locked build artifacts on the driver. Retain
  complete or partial structured evidence with bounded ownership
  and cancellation at both ends.
- Run fresh baseline and Engine lanes in HTTP and GraphQL order.
  Each validates the original 128 held TLS 1.3 / HTTP 1.1 load
  connections, all 130 read-only preparations, a two-second collector
  preflight at 1,000 requests/s, and exact offered work and final state.
  Freeze the full 180-second planned manifest and validate its first
  2,000 rows against the actual schedule. The preflight never enters
  timed warmup or measurement.
- Exercise certificate trust, IP mismatch, a peer outside the fixture
  admission list, SSH host-key mismatch, incomplete evidence or
  disconnected job cleanup, and unavailable dedicated resources.
  A local isolated network can exercise both actual protocols.
  It cannot qualify the physical/resource partition.
- Require evidence of a native Linux app allocation with two dedicated
  CPUs and a 2 GiB memory limit, controller separation, a distinct
  Linux driver host, and sufficient collector behavior. Reconcile
  effective app process topology and limits over the attempt. The
  full W0 matrix can enter only after the reference preflight passes.
  Use the original phase order, pair schedule, limits and scoring.

[W0 workload](../validation/small-api-workload.md) ·
[Collector readiness](../adr/ADR-0011-small-api-collector-connection-readiness.md) ·
[Prior GA conformance and resource inventory](../validation/small-api-ga-conformance.md)
