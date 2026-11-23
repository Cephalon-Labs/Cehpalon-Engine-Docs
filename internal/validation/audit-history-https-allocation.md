# Paired HTTPS audit history measurement

Declared 2026-11-23 under #18. Compare Engine
887c529c5975e37bd53082896b56d7eff448dbbc with
4dedaeec12a6ae1e0d0d9313d79aa5d62113e7fa. Build the same audit-outbox and
security consumer sources in separate Release roots using .NET SDK 11.0.100
on WSL x64. The experiment uses the existing protected resource-history host,
fixture CA/JWT validation and indexed PostgreSQL storage. The canonical
benchmark protocol, Project gates and #3 remain in force.

Use a new owned PostgreSQL 18.7 container and local volume from the retained
digest, bound to WSL loopback. Keep Pooling=false, the default planner and
configuration, and the existing Npgsql lock, schema and SQL. Provision once per
attempt using the before binary. Both lanes read the same schema and data
without writes during measurement. The corpus has 256 matching rows and 64
other-resource rows per tenant. A/B share receipt IDs and a resource ID while
field values identify their tenant. Rows contain eight allowed fields (one
redacted) and an unknown field. Reuse the same selection for both protocols.

Run an untimed preflight for both binaries before the complete matrix. Require
CA and hostname verification, reads for both owners, generic denials in both
cross-tenant directions, a missing operation grant, revoked and restored
membership, anonymous rejection and rejection of a mismatched cursor. Every
rejected request must have zero handler, query and result deltas. Repeat those
controls for each host and protocol before sampling.

Four pairs alternate revision order AB, BA, AB, BA. Each lane has a fresh
server process. Test HTTP and GraphQL at 25 and 200 rows, rotating workload
order by pair and using the same order within a pair. Each workload uses one
verified persistent TLS connection and sends 20 warmups then 100 sequential
measured requests, alternating A and B. Start after receipt 8. Check every
response for exact keys, scope, projection and continuation. Canonical
response digests must agree across revisions and transports for the same
tenant and page size. Retain all 3,200 measured requests, 640 warmups, 144
controls and their batch start/end counters.

Measure client latency from send to the complete response using a monotonic
clock, before JSON validation. Measure server process-wide managed allocations
using precise total-allocated-byte snapshots over each batch with the client
in a separate process. Snapshot/control overhead and background allocations
are included. Record GC collection counts and require one completed provider
query and handler per measured response. This does not measure PostgreSQL
allocations, working set, individual operation allocations, saturation,
new-connection latency, or native Windows database performance.

Report nearest-rank p50/p95/p99 for each batch and the median paired percent
changes, including regressions. Report allocated bytes per request as a batch
mean and paired percent changes. Treat this as descriptive local evidence with
no new statistical acceptance threshold. Preserve complete and failed
attempts. Stop on any failed control or validity check. Record any correction
before starting another complete attempt.

Preflight 01 stopped before creating any indexed rows or HTTP hosts. The
seed command attempted indexed setup against a schema that did not yet exist
(PostgreSQL SQLSTATE 3F000). Preflight 02 calls the existing base fixture
initializer before indexed setup, matching the normal consumer provisioning
sequence. The workloads, timings, counters and acceptance checks are unchanged.

Preflight 02 seeded all rows but stopped before its first HTTPS request. The
WSL Python 3.10 HTTPS connection does not implement the context-manager
protocol. Preflight 03 wraps it in contextlib.closing and uses the same .NET
binaries and the same test matrix, with a fresh schema.
