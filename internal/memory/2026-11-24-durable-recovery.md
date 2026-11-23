# 2026-11-24 durable provider recovery and original benchmark readiness

The user requested actual durable recovery proof and a check against the
original benchmarks. The two provider fixtures ran on synthetic data and
pinned versions. PostgreSQL 18.6 passed a controlled abrupt database stop
after an acknowledged A commit and while the B update was held open.
The same storage reported WAL recovery. A new application recovered A,
preserved B's original data and rechecked tenant isolation and pool scope.
The exact ordinary runner also passed. RabbitMQ 4.4.0 verified confirms,
unacknowledged redelivery, pending first delivery and retained
acknowledgements across two graceful restarts of one durable quorum
queue. Both fixtures verified owned cleanup.
[Provider recovery proof](../validation/durable-recovery.md)

Small API Canonical04 once again reconciled against the original numeric
thresholds using the retained observation tables. The archived locked
RC3 build succeeded on Windows and WSL, including identical generated
registry bytes. The current Samples GA SDK pin conflicts with the RC3
benchmark lock before restore. The live WSL allocation remains shared
and uncapped, and no independent reference driver was identified.
The legacy orchestrator launches local processes and loopback traffic.
The Business benchmark still needs the integrated workload and baseline.
The last untraced Tooling series still records compiler variance flags.
No new timed workload ran.
[Benchmark gates and current readiness](../validation/original-benchmark-readiness-2026-11-24.md)

For Business recovery, continue with the declared order plus outbox
transaction and inbox-backed replay through the actual Worker, then
reconcile business effects against the ledger. The joined workload,
external identity, benchmark and provider HA gates remain distinct.
