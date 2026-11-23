# Application-facing PostgreSQL order proof

The optional Samples executable uses the Engine tenant dispatcher with
synthetic identity sources and an actual Npgsql 10.0.3 connection to
PostgreSQL 18.6 on WSL. It runs a typed order read and conditional state
transition. Transactions set tenant scope locally and use explicit tenant
and order predicates. A restricted runtime role accesses a table with
forced row-level security. The exact Samples SHA tested was
`1bb96af512ae21f7a160a95c7d2d745086aaa573`, with Engine
`6fe7254404cf6b148370bd95befe8331e8932354`.
[Consumer source and replay](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/1bb96af512ae21f7a160a95c7d2d745086aaa573/multitenant-business/postgres) · [Runtime and source receipt](../evidence/postgresql-application-scope/2026-11-23/local-proof.json)

| Check | Exact local result |
| --- | --- |
| Migration | A fixture error after the SQL body left no schema. Explicit apply as the migrator succeeded, and repeating it was refused. The runtime role had separate credentials and limited grants. |
| Checked scope | Six invalid or denied cases performed zero store checkout and SQL attempts. The matrix includes a separate wrong-action case and pre-cancellation. |
| Read | Two tenant scopes saw different values under the same order ID. |
| Conditional update | The stale revision on an otherwise eligible order changed zero rows. An authorized A update committed and read back at the next revision. |
| Rollback | Cancellation after an actual B update and before commit left B's original state intact. |
| Pool and fixture lifetime | A lookup without scope after both operations reused the same backend and saw zero rows. The owned container and volume were removed and the loopback port closed. |

The run used .NET SDK 11.0.100 and runtime 11.0.0 with a locked Release
build. The execution evidence distinguishes confirmed commit and rollback
from the store's untested acknowledgement-fault branches. Earlier Git
preparation failures occurred before provider startup and were retained.
Full provider API, concurrent transaction, hosted CI, identity and
Business workload gates remain open. #7 remains Blocked and #12 remains
Backlog, both at M0. [Scope and next gates](../planning/postgresql-application-scope.md)

[Overlapping READ COMMITTED transactions and lock-wait cancellation](transactions-and-drain.md#postgresql-order-transactions)
