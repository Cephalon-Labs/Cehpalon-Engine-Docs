# Graceful drain for operation budgets

From its shutdown path, the host calls `DrainAsync()` on its shared `OperationConcurrencyBudget` or `TenantOperationConcurrencyBudget` to close admission and wait for owned cleanup. The close takes effect during the call. Subsequent authorized calls receive the existing generic `operation.capacity_exceeded` result, even while the budget has spare slots. Protected dispatch still performs fresh authorization first. Long-lived hosts that start a new admission lifetime create a new budget.

Concurrent drain callers observe one completion. A cancellation token controls the individual pending wait. Closing is permanent even if that token is already canceled. Admitted operations preserve their execution result or exception and keep the slot until owned cleanup finishes, including a faulting cleanup. The drain task completes once the final slot releases.

The generated Small API closes admissions before stopping Kestrel and waits for admitted operations within the existing five-second shutdown window. Its separate `--self-test-drain` exercises protected writes held across shutdown with each budget variant. The component tests separately observe rejection below the numeric cap, cleanup faults, independent canceled waits and closure across dispatchers.

[Validation protocol](../validation/operation-budget-drain.md)

## Results

The exact Engine revision passed 519 Windows and 516 WSL component checks. The CLI-generated consumer passed 153 checks per host, including the original 39-case self-test and two held-write shutdown cases. Each case observed one HTTP 200, one write, one handler disposal and one host disposal.

Five paired synchronous samples per revision observed 56 B/op on the direct and budgeted paths. The table shows the median for each path and the median of the paired differences in ns/op.

| Host and revision | Direct | Budgeted | Median paired difference |
| --- | ---: | ---: | ---: |
| Windows before | 56.28 | 172.24 | 115.96 |
| Windows with drain | 59.10 | 175.92 | 113.47 |
| WSL before | 72.43 | 215.11 | 137.99 |
| WSL with drain | 65.95 | 224.84 | 153.73 |

The paired difference moved in opposite directions on the two hosts. This component observation covers normal synchronous Core dispatch only. Throughput and canonical benchmark acceptance remain open. [Samples reports and checksums](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/719baa8f49bf925b8cd4fa3cbeca18d832fd0337/tooling-small-api/evidence/2026-11-18-budget-drain)

Hosted portable contracts passed on Windows Server 2025 and Ubuntu 24.04. Hosted platform smoke passed 12 checks per host and left live PostgreSQL and RabbitMQ fixtures unrun. #3 stays Blocked. [Portable CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44331765909) · [Platform CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44331765969)
