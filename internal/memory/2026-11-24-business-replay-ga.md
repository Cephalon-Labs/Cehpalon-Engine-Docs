# 2026-11-24 Business order replay and Small API GA build

- Samples PR #5 merged as `a8ad452677c48d87a125460c552ee01c3e044046`.
  Its tree matches hosted tested tree `630c667cf954487d0d790dc01b1e3ca4a0e509c2`.
  Hosted run 45245422430 passed joined recovery on Ubuntu 24.04 and
  locked Small API builds on Ubuntu 24.04 and Windows Server 2025.
- Joined recovery used exact Engine `6fe7254404cf6b148370bd95befe8331e8932354`,
  PostgreSQL 18.6 and RabbitMQ 4.4.0. The application stopped after publisher
  confirm before the outbox mark and stopped again as a Worker after SQL
  commit before ACK. A new Worker processed one redelivery and one
  republished copy without a second effect. Independent checks recorded
  A at reserved/revision 1/stock 8/one inbox row and B at pending/revision
  0/stock 20/empty inbox. Three graceful same-volume broker restarts and
  cleanup passed. This fixture kept PostgreSQL running.
- Active Small API build pins SDK 11.0.100 and Engine
  `5e92ac1c7fa1e150e7e97de6d68e94b31ffba053`. The portable package lock
  and historical evidence are unchanged. The orchestrator reads the
  scoped pin and also requires the SDK to match root global.json.
  Windows/WSL builds and 29 offline collector tests per host passed.
- No new timing run. GA functional conformance, the original dedicated
  application and separate driver allocations, and full Business
  identity/corpus/baseline gates remain open.

[Validation and receipts](../validation/business-replay-and-ga-build.md) ·
[Plan](../planning/business-replay-and-ga-build.md) ·
[Samples PR #5](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/pull/5)
