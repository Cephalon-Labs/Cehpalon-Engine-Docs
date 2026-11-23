# Business order replay and Small API GA build

The [test plan](../planning/business-replay-and-ga-build.md) fixed the
replay checkpoints and build evidence before execution.

## Recovery from order and outbox through Worker and inbox

The local matrix used disposable PostgreSQL 18.6 and a single-node
RabbitMQ 4.4.0 quorum queue with pinned images, SDK 11.0.100, Npgsql
10.0.3 and RabbitMQ.Client 7.2.2. The Samples consumer uses the Engine
tenant dispatcher and a synthetic identity. Its restricted PostgreSQL
runtime sets a transaction-local tenant, and the four fixture tables
enforce row-level security. The controller independently queries the
four tables and the broker across the recovery boundaries.

| Checkpoint | Durable state and observations |
| --- | --- |
| Order creation | Tenant A's pending order at revision 0 and its unpublished outbox event appeared in the same transaction. Stock was 10 and the inbox was empty. |
| Publisher stops after confirm | The controlled process exited with code 76 before marking the outbox. The database still showed unpublished and the broker had one ready message after both the exit and the first same-volume restart. |
| Publisher retry | A fresh publisher sent the identical outbox event and marked the single row published after confirmation. The broker held two copies. |
| Worker stops before ACK | The controlled process exited with code 77 after committing the inbox insert, one stock decrement and one order transition in one transaction. Tenant A was reserved at revision 1 with stock 8 and one inbox row. The client disconnect returned the unacknowledged delivery to the queue before the second graceful broker restart. |
| Fresh Worker and final restart | The Worker observed one broker redelivery and one initial delivery of the separately published copy. It acknowledged both after the duplicate checks committed. Order, stock and inbox matched the original Worker-commit snapshot. The queue was empty after a third graceful restart. |

All nine ledger checkpoints passed. Tenant B had the same order ID and
SKU and stayed pending at revision 0 with stock 20 and no outbox or
inbox rows. The test also checked a cross-tenant operation was rejected
before PostgreSQL access, and verified that the owned containers,
volumes, bridge and loopback listeners were gone. The three RabbitMQ
restarts used the same container and volume with fresh broker processes.
PostgreSQL stayed up in this joined scenario. The earlier provider proof
covers a separate PostgreSQL crash/WAL recovery case.

The fixture proves one business effect under these two delivery windows
for the selected event. Application and broker failures here are the
controlled process exits and graceful broker restarts described above.
Multi-node failover, power loss, SQL failure between statements, poison
handling, full HTTP/identity integration and Business workload timing
have separate acceptance requirements.
The first WSL run exited successfully, but its temporary workspace
disappeared before the report was copied. The complete matrix was
repeated on the integrated source in persistent storage. The retained
WSL and hosted reports agree on all 15 source hashes, phase exits, SQL
rows, broker counters, restart and cleanup observations.
[First WSL retention note](../evidence/business-replay-ga/2026-11-24/business-replay-local-wsl-initial-retention.txt) · [Local recovery receipt](../evidence/business-replay-ga/2026-11-24/business-replay-local-wsl.json) · [Hosted Ubuntu recovery receipt](../evidence/business-replay-ga/2026-11-24/business-replay-hosted-ubuntu.json) · [Provider recovery](durable-recovery.md) · [Samples proof](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/multitenant-business/order-replay-proof)

## Small API build on .NET 11 GA

The active sample now uses SDK 11.0.100 with Engine revision
`5e92ac1c7fa1e150e7e97de6d68e94b31ffba053`. The build verifier and
measurement orchestrator use the sample's Engine lock. The orchestrator
requires its observed SDK to match both that lock and root
`global.json`. A forced package-lock re-evaluation returned the original
bytes.

On Windows and WSL, locked Release restore/build succeeded against clean
commits. Both builds generated the same registry bytes and had the same
57 runtime libraries and 16 source hashes. Their application assemblies
have distinct hashes recorded in the receipts. Both target
Microsoft.NETCore.App and Microsoft.AspNetCore.App 11.0.0. Offline
collector tests passed 29 of 29 per host. This round ran build-only and
collector unit tests. The GA functional conformance matrix remains open.
[Local GA summary](../evidence/business-replay-ga/2026-11-24/small-api-local-build-summary.json) · [Windows](../evidence/business-replay-ga/2026-11-24/small-api-local-windows-build.json) · [WSL](../evidence/business-replay-ga/2026-11-24/small-api-local-wsl-build.json)

The frozen baseline covers the model, workload driver, correctness
matrix, wire protocol, host, entry point, collector validation and the
protocol documents. The only change among those inputs is the
orchestrator's Engine/SDK pin handling. Historical results remain tied to
their recorded RC3 inputs.
[Frozen baseline](../evidence/business-replay-ga/2026-11-24/frozen-benchmark-baseline.json) · [Exact criteria readback](../evidence/business-replay-ga/2026-11-24/original-criteria-readback.json)

Reference qualification still requires the declared dedicated Linux
2-vCPU/2-GiB application allocation and a separate load driver. No
benchmark timing was collected in this round. The existing Small API
schedule still requires 1,000 requests/s, 60 seconds of warmup,
180 seconds of measurement and five alternating pairs per transport, plus
its original startup, idle, latency, allocation, error and variance gates.
The Business workload still requires its original identity, corpus,
baseline, failure and reference environment gates.
[Small API protocol](small-api-workload.md) · [Business protocol](business-workload.md) · [Previous readiness check](original-benchmark-readiness-2026-11-24.md)

## GitHub Actions and integration

The hosted run passed the entire recovery matrix on Ubuntu 24.04 and
the two locked GA builds on Ubuntu 24.04 and Windows Server 2025.
The replay receipt verified nine ledger checkpoints and three graceful
same-volume restarts. The two GA receipts agree on registry bytes, the
57-library runtime graph and the exact input paths. Git checkout line
endings account for the different raw hash of Directory.Build.targets
on the hosted Linux and Windows workers. The merged Samples main tree
matches the pull-request merge tree that produced all three receipts.
[Samples PR #5](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/pull/5) · [Hosted run](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/actions/runs/45245422430) · [Merged tree readback](../evidence/business-replay-ga/2026-11-24/hosted-integration-readback.json) · [Hosted build on Ubuntu](../evidence/business-replay-ga/2026-11-24/small-api-hosted-ubuntu-build.json) · [Hosted build on Windows](../evidence/business-replay-ga/2026-11-24/small-api-hosted-windows-build.json)
