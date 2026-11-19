# Opt-in budget metrics

Both `OperationConcurrencyBudget` and `TenantOperationConcurrencyBudget` expose `CreateMetrics()`. The returned `System.Diagnostics.Metrics.Meter` belongs to the caller and should be disposed with its observation scope. The optional meterName parameter lets the host give stable names to separate resource budgets.

```csharp
using var metrics = tenantBudget.CreateMetrics("MyApp.DatabaseBudget");
```

The default meter names are `Cehpalon.Engine.Core.Budget` and `Cehpalon.Engine.Tenancy.Budget`. The instruments use integer observable gauges.

| Instrument | Unit | Value |
| --- | --- | --- |
| cehpalon.operation_budget.active | {operation} | Admitted operations including owned cleanup |
| cehpalon.operation_budget.capacity | {operation} | Configured total limit |
| cehpalon.operation_budget.closed | none | 1 after permanent closure, otherwise 0 |
| cehpalon.operation_budget.active_tenants | {tenant} | Tenant identities currently holding slots |
| cehpalon.operation_budget.tenant_capacity | {operation} | Configured per-tenant limit |

The last two gauges belong to tenant budgets. The Engine adds no measurement tags. Creating the meter registers instruments, and the collector chooses when to observe. Hosts should choose stable resource meter names appropriate for their operational audience.

Each gauge samples its own value. Concurrent operations can move between gauge callbacks. `GetSnapshot()` provides the coherent aggregate value for callers that need one observed state. The metrics contract covers aggregate resource use. It provides no tenant authority or admission reservation.

The actual listener tests hold operations through cleanup, collect their open and closed states, wait for drain and verify zero active counts. They also check custom naming, empty measurement tags, stopping observations after meter disposal and successful dispatch after a collector callback fails. [Validation protocol](../validation/budget-metrics.md)

The `MeterListener.RecordObservableInstruments()` API invokes the observable instruments enabled on that listener. Disposing a Meter disables its instruments. [Microsoft MeterListener documentation](https://learn.microsoft.com/dotnet/api/system.diagnostics.metrics.meterlistener) · [Microsoft Meter documentation](https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.metrics.meter?view=net-11.0-pp)

## Results

The final [Engine revision](https://github.com/Cephalon-Labs/Cehpalon-Engine/commit/b87c75856313f3c90a38a20a0c59a2ca088a7e96) passed 521 component checks on Windows and 518 on WSL. The actual generated Small API passed 159 checks per host, including all 39 original self-test cases and the snapshot/drain proofs. The original tenant guardrails passed 5/5 and the prior snapshot observer output validated against its existing analyzer on both hosts.

One listener enabled the Core meter's three instruments and the tenant meter's five instruments. Each host recorded 80 collections and 640 validated callbacks across four controlled states. The table gives the median collection time in microseconds, including validation callbacks.

| State | Windows | WSL |
| --- | ---: | ---: |
| idle/open | 5.650 | 4.104 |
| cleanup/open | 4.100 | 5.066 |
| cleanup/closed | 2.050 | 4.183 |
| drained | 1.400 | 2.033 |

The first collection was retained. It took 851.500 microseconds on Windows and 819.918 microseconds on WSL, with 24 current-thread allocated bytes on each host. The remaining 79 collections per host recorded zero current-thread allocation. All durations, including the maximum collection durations and the complete first-stage series, are preserved.

Each collection followed a requested 10 ms sleep outside measurement. Actual median start-to-start cadence across the stages was about 15.5 ms on Windows and 10.1 ms on WSL. These observations describe the caller's collection and validation on stable budget states. Concurrent exporters, serializing measurements, periodic callbacks during production traffic and the canonical performance gate remain open.

The [retained reports and SHA-256 index](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/4e34c149549da0a18233eee8c79f1ff34ea1019b/tenant-identity/evidence/2026-11-19-budget-metrics) include source manifests, preparation records, the raw series, actual cadence and generated consumer proofs. Four altered datasets were rejected for a missing collection, wrong callback count, nonincreasing clock and wrong state. No timing rerun or first-sample exclusion was used.

Hosted portable and platform workflows passed for the final revision on Windows Server 2025 and Ubuntu 24.04. Platform smoke recorded 12 passed checks and two unrun real PostgreSQL/RabbitMQ fixture checks per host. #3 remains Blocked. There were no GitHub usage or billing skips. [Portable CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44561657750) · [Platform CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44561657816)
