# Original benchmark readiness on 2026-11-24

Follow-up on 2026-11-24: [joined Business recovery and Small API GA build](business-replay-and-ga-build.md) records the scoped replay and build work after this readiness snapshot.

Full reference timing remains blocked. Windows and WSL use one i5-13500
workstation. WSL exposes 20 logical CPUs and about 31.22 GiB RAM. The
observed cgroup reports no CPU quota or memory cap. The Engine and
Samples repositories report zero registered self-hosted runners. The
organization-level runner inventory returned 403 with the current
permissions. A dedicated application allocation and a separate load
driver remain unverified.
[Live preflight](../evidence/durable-recovery/2026-11-24/benchmark/reference-environment.json)

## What is available

| Gate | Evidence and readiness |
| --- | --- |
| Small API #9/#11 | Canonical04 passed the original numerical gates in a shared WSL profile on the RC3 pins. The offline recheck covers all 120 startup observations, 20 idle processes with 1,200 reported RSS samples, 20 main runs and 12 timed diagnostics. The main series had 3,600,000 correct measured requests and diagnostics had 1,872,000. Engine startup p95 was 417.955 ms for HTTP and 863.722 ms for GraphQL. Engine GraphQL p95 CV was 4.769352% against the existing 10% ceiling. The reference verdict remains blocked. |
| Business #15 | The original API/Worker workload has yet to run. It needs the integrated order/outbox/worker/inbox path, identity, deterministic corpus and ledger, and a parity baseline. The app and infrastructure allocations and driver are separate under ADR-0003. Provider recovery receipts address discrete cases only. |
| Observability #18 | Current protected HTTPS proves controlled admission, held cleanup and fresh host activation. Local callback and counter cost evidence covers the declared component workloads. Reference workload and external exporter evidence remain open. |
| Tooling #20 | The retained exact last untraced series completed the declared 306 compiler rows including primers and 144 CLI launches per host. The Windows and WSL compiler series flagged 9 and 3 groups respectively above the historic 15% descriptive variance limit. CLI flagged zero on each. The recorded status is Observed / not qualified. |

The latest W1 Core/Composition guardrails separately passed 8/8 under
their declared shared-host component protocol. Their scope covers #5 and
#6. The broader #9/#11, #15, #18 and #20 criteria have independent
conditions.
[Small API thresholds](small-api-workload.md) · [Canonical04 report](../planning/w2-small-api-collector-readiness.md) · [Business protocol](business-workload.md) · [Observability drain](transactions-and-drain.md) · [Tooling report](../planning/tooling-traces.md) · [W1 component closure](w1-ga-closure.md)

## Reproduction checks and reference prerequisites

The Canonical04 replay recalculated nearest-rank startup p95, idle and
pair-specific latency/allocation limits, measured request counts and
population CV from the frozen observation tables. It checked all retained
table rows and the original reference classification. Per-request raw
reconciliation remains available in the historical audit.
[Offline replay and input hashes](../evidence/durable-recovery/2026-11-24/benchmark/canonical04-recheck.json) · [Historical raw audit](../evidence/small-api-collector/results/raw-audit/audit-final.md)

The current Samples checkout selects SDK 11.0.100 GA in global.json.
The Small API benchmark lock still selects 11.0.100-rc.3.26522.148 against
Engine 6804271d. The checked-in verifier refused this mismatch before
restore. The RC3 executable also stopped at SDK resolution against the
current root. The merged recovery tree has the same benchmark inputs as
the checked snapshot. Locked Release build-only runs passed on Windows and WSL
with archived Samples a3bd8b5c, Engine 6804271d and the exact RC3 SDK.
Both emitted byte-identical generated registries and produced the same
57-library runtime dependency graph. The builds were untimed.
[Current pin preflight](../evidence/durable-recovery/2026-11-24/benchmark/current-pin-preflight.json) · [Windows archived build](../evidence/durable-recovery/2026-11-24/benchmark/rc3-windows-build.json) · [WSL archived build](../evidence/durable-recovery/2026-11-24/benchmark/rc3-wsl-build.json)

The historical Small API orchestrator launches local processes, connects
to loopback, and records its reference gate as false. Reference execution
requires an app allocation with **2 dedicated vCPU and 2 GiB** on Linux
x64, and an independently allocated driver. The orchestrator must admit a
paired app/driver topology with equivalent TLS identity, connection
preparation, schedules, clocks, state, shutdown and raw accounting.
Review that topology with the existing paired order, 1,000 requests/s,
timeouts and thresholds before recording a reference result. A current
GA benchmark candidate also needs coherent SDK/Engine pins, locked
artifacts and the full untimed conformance gates before timing.
[Small API conformance ADR](../adr/ADR-0009-small-api-conformance-and-measurement.md) · [Business reference profile](../adr/ADR-0003-multitenant-business-profile.md)

No new timed workloads were launched during this recovery delivery. The
raw historical failure and successful observations remain valid within
their recorded source and environment scopes.
