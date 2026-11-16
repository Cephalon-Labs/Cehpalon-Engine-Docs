# In-process operation concurrency budget

Engine [#18](https://github.com/Cephalon-Labs/Cehpalon-Engine/issues/18) moves to In Progress for the portable source slice in [ADR-0032](../adr/ADR-0032-operation-concurrency-budget.md).

## Use and scope

Construct an `OperationConcurrencyBudget` with a positive limit and share it across routes that run work against the same resource. Use its `DispatchAsync` with an existing Core dispatcher or pass it to the protected `TenantOperationDispatcher` constructor. Separate budget instances apply independent limits. The budget covers handler creation, execution and owned cleanup. Saturation returns `operation.capacity_exceeded` without creating a handler or retaining the request. Protected dispatch performs fresh identity, tenant and operation authorization before admission. On the plain route, admission precedes the typed registry lookup. No default Small API profile enables the budget.

## Validation

[Engine main revision](https://github.com/Cephalon-Labs/Cehpalon-Engine/commit/2bd9cfcaf4b9328a76b36102c094de6f7fd97e17) passed 512 local checks on Windows and 509 on Ubuntu 22.04 under WSL with SDK `11.0.100-rc.3.26522.148`. Cases cover shared capacity, 32 concurrent callers, saturation without factory calls, cleanup completion and failures, cancellation and fresh cross-tenant denials under saturation. The real source-generator fixture dispatches through a generated typed gateway. An actual CLI-generated Small API consumer passed locked restore, Release build and 39 self-tests on Windows. With both transports disabled, offline export produced only the manifest and recorded zero registrations, factory invocations and dispatches.

[Raw observations, contract reports, experimental patch and SHA-256 index](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/e636195e4d274c749c881f5df458733c01bb980a/tooling/evidence/2026-11-16-dispatch-concurrency-budget) include both source revisions. The [fixed component protocol](../validation/operation-concurrency-budget.md) compared an unbounded synchronous dispatch with a budget of two in five alternating pairs of 100,000 serial calls after warmup.

| Source revision | Host | Median unbounded ns/op | Median budgeted ns/op |
| --- | --- | ---: | ---: |
| Delivered `2bd9cfc` | Windows | 57.59 | 173.43 |
| Delivered `2bd9cfc` | WSL | 104.65 | 252.97 |
| Experiment `cbfb082` | Windows | 56.01 | 210.82 |
| Experiment `cbfb082` | WSL | 66.71 | 193.36 |

Every measured lane recorded 56 bytes of caller-thread allocation per operation. The experiment's completed-dispatch fast path had mixed timing across hosts, so the delivered revision uses the simpler async admission path. The measurements cover serial dispatch at the component boundary. Workload throughput, resource isolation between tenants, distributed limits, transport-level overload mapping and canonical qualification remain open. The formal #5 and #6 dependencies and the original benchmark gate remain in place.

The [portable contracts](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/43788484819) and [SDK smoke](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/43788484810) workflow jobs stopped before any steps. GitHub attributes this to failed recent account payments or the spending limit. The local results do not cover the supported Windows driver matrix in #3.
