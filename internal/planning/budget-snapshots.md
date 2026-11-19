# Aggregate operation budget snapshots

Hosts can call `GetSnapshot()` on either operation budget for a detached value that describes a single observed state.

```csharp
OperationConcurrencySnapshot total = budget.GetSnapshot();
TenantOperationConcurrencySnapshot tenantTotals = tenantBudget.GetSnapshot();
```

The Core value contains the configured maximum, active operations and whether admissions are closed. It reads active count and closed state from the same atomic admission word. The tenant value contains its coherent total snapshot, configured per-tenant maximum and active tenant count under the same admission lock. The active tenant map drops each tenant after its final owned operation releases.

A slot stays active during handler cleanup. The tests retain a snapshot of two tenants during cleanup, release one and observe one active tenant, then verify that the earlier snapshot retains its original values. A concurrent admission/drain test checks bounded counts and permanent closure across 32 workers. Observed free capacity can change immediately after a read. Hosts still invoke the admission API for each operation and route protected work through fresh tenant authorization.

The generated Small API includes aggregate snapshots in its readiness file and its post-cleanup stopped report when a budget is configured. The separate drain fixture records held, closing and completed snapshots for both budget variants. Snapshot fields contain limits, counts and a flag. Host applications decide which observers can read these operational values.

The getters run on explicit observation. They add no automatic callbacks, exporter, network route or sampling loop. This delivery's correctness checks do not measure observer overhead or establish the canonical performance gate.

[Validation protocol](../validation/budget-snapshots.md)

## Results

The [exact Engine revision](https://github.com/Cephalon-Labs/Cehpalon-Engine/commit/46d07c9b9da9d38adbfc7f083ba1b3297d8ff82e) passed 520 Windows and 517 WSL component checks. Each actual generated Small API passed 159 verification checks, including the original 39-case suite, both capacity fixtures and held-write shutdown. The external serve process recorded an empty open budget at readiness and an empty closed budget after cleanup. [Samples reports and checksums](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/7f1dec699748e908452a80fbb6b9f0dc4f8e3e8a/tooling-small-api/evidence/2026-11-19-budget-snapshots)

Hosted portable contracts passed on Windows Server 2025 and Ubuntu 24.04. Hosted platform smoke passed 12 checks per host and skipped the real PostgreSQL and RabbitMQ fixtures. #3 stays Blocked. #18 and #20 remain In Progress and the canonical benchmark gates stay as recorded. [Portable CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44443260224) · [Platform CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44443260272)
