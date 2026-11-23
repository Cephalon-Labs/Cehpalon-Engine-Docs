# 2026-11-23 audit receipt collector contention

The user asked to plan and continue the Engine roadmap. GitHub heads and
tracking superseded the earlier working-tree handoff. #3, #5 and #6 were
already closed. #18 remained the active telemetry slice. Engine, Docs and
Samples base heads were verified before using a separate Docs worktree.

At clean Engine 6fe7254, Windows and WSL each completed the predeclared
three-mode audit receipt experiment with 1, 2 and 4 worker threads. All
67.2 million reads per host reconciled. With two workers, median shared
minus disabled was 18.45 ns/read on Windows and 18.82 on WSL. The
four-worker WSL series had wider variation and a negative paired result
for each shared contrast. The fixture used synchronous empty results and
no network provider. The run documents component throughput and leaves
#18 open with M0 and existing gates. [Validation](../validation/audit-read-contention.md)

The larger #18 scope still needs trace/log propagation, an explicit
sensitive-data contract and supported-path shutdown/recovery proof.
[Proposed first trace and log delivery](../planning/observability-trace-correlation.md). #20
depends on #11, including its separately allocated Linux reference setup.
The next Business lane proof builds on the #7/#12 PostgreSQL preparation,
before durable eventing or a complete Worker sample.
