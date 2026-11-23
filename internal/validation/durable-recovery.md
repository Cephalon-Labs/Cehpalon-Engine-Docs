# PostgreSQL crash and RabbitMQ durable queue recovery

## Plan

Run separate, reproducible provider scenarios using disposable local
containers, loopback connectivity, the existing pinned images, and
synthetic identifiers. Freeze the expected state before each restart,
verify the fixture and its storage identity, and open fresh clients for
readback. Keep attempt logs private and publish bounded receipts. The
last step verifies removal of owned resources. The [Business workload](business-workload.md)
retains its separate cross-provider and performance gates.

## PostgreSQL order state

Run the existing migration, tenant and concurrent transaction tests
first. The recovery mode uses one application process to commit tenant
A's test update and acknowledge its result. A second update by tenant B
reaches a test gate after PostgreSQL returns the UPDATE row, with no path
from that gate to commit. A distinct runtime-role observer sees the live
backend idle in an open UPDATE transaction. The restart procedure
targets only the full verified ID of the newly created container.

The server is stopped abruptly and its exit status is checked. Restart
reuses the same container, pinned image and persistent volume. The proof
compares the PostgreSQL system identifier and verifies a changed
postmaster start, readiness and fresh WAL recovery markers. The
administrator reports fsync, synchronous commit and full page writes
enabled before and after restart under the fixture configuration.

A fresh application process opens the restricted runtime path. It checks
A's acknowledged update and exact revision, B's original state and
revision, and cross-tenant denial before store SQL. The pool checks
return an exact backend with empty tenant scope and zero visible rows
after each declared readback. This covers interrupted database process
recovery on intact storage. Commit-acknowledgement loss, physical power
loss, storage replacement, backup restore and failover remain separate
scenarios. [Previous concurrency controls](transactions-and-drain.md#postgresql-order-transactions)

The exact clean WSL run at Samples
`d7c35fb268a5b8b5192fe400cb3b86954afc371c` and Engine
`6fe7254404cf6b148370bd95befe8331e8932354` passed on PostgreSQL 18.6
and Npgsql 10.0.3 under .NET 11.0.0. PostgreSQL exited 137 after the
controlled stop. The same storage reported recovery and the fresh app
saw A at revision one and B at revision zero. The independent legacy
three-argument proof also passed in a separate fixture. Both runs
verified removal of the container and volume and closure of the
loopback listener. An early WSL preparation and a build with an empty
log stopped before provider work. The successful retries used the
same proof checks.
[PostgreSQL protocol and runner](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/blob/d7c35fb268a5b8b5192fe400cb3b86954afc371c/multitenant-business/postgres/RECOVERY-PROTOCOL.md) · [Local PostgreSQL receipt](../evidence/durable-recovery/2026-11-24/postgres/wsl.json)

## RabbitMQ durable messages

The exact clean Samples fixture `1a1dc96f1b1b5f7a7c438cd92e94561843c143d4`
passed on WSL with RabbitMQ 4.4.0, Erlang/OTP 29.1.2, RabbitMQ.Client
7.2.2 and .NET 11.0.0. One durable single-node quorum queue accepted
three mandatory persistent messages with publisher confirmation. The
test manually acknowledged one, left another delivered and unacknowledged,
and left the third pending. Broker counters independently showed one
ready and one unacknowledged.

After a graceful stop and restart with the same container and volume,
a fresh AMQP process saw the two expected messages. The held message
carried the redelivery flag, the pending message did not, and both
payloads and IDs matched. The acknowledged ID was absent. After
acknowledging both remaining messages, a second graceful restart left
the queue empty for another fresh process. The fixture verified removal
of the container, network and volume and closure of its loopback listener.

This lane uses controlled graceful stops. The initial attempt to prepare
an abrupt-stop script was rejected by the command tool. A missing
standalone transitive lock entry and an Erlang prelaunch failure stopped
the first two local attempts before message seeding. The corrected
standalone lock and startup check were used for the entire successful
run. Provider crash, multi-node failover and application inbox/outbox
reconciliation remain separate scenarios.
[Local RabbitMQ receipt](../evidence/durable-recovery/2026-11-24/rabbitmq/report.json) · [Protocol and runner](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/1a1dc96f1b1b5f7a7c438cd92e94561843c143d4/multitenant-business/recovery-broker)

## Hosted and merged

The PostgreSQL recovery and RabbitMQ recovery jobs passed on Ubuntu
24.04. The existing PostgreSQL overlap and Windows and Ubuntu HTTPS
drain jobs passed too. The hosted PostgreSQL receipt includes the
acknowledged and held pre-stop states, the joined old application,
same-storage WAL recovery, fresh readback and cleanup. The RabbitMQ
receipt independently matched the local confirmation, delivery,
acknowledgement and two-restart matrix. The hosted checkout tree matched
the tested branch head and merged Samples main.
[Recovery CI](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/actions/runs/45242006503) · [Regression CI](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/actions/runs/45242006388) · [PR and revision receipts](../evidence/durable-recovery/2026-11-24/hosted.json)

The two proofs establish provider recovery on their own retained
storage. The Business workflow still needs atomic order plus outbox,
Worker inbox deduplication and independent ledger reconciliation
across the restart. The original workload and reference gate remain
separate. [Benchmark readiness](original-benchmark-readiness-2026-11-24.md)
