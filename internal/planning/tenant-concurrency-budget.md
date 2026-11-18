# Total and per-tenant concurrency limits

Generated Small API can apply both limits to the same host.

```text
--serve --config <config.json> --certificate <server.pfx> --public-key <public.pem> --ready <ready.json> --max-concurrent-operations 2 --max-concurrent-operations-per-tenant 1
```

Both limits are positive integers. The tenant limit requires a host limit and must be no greater than it. The host applies both limits only when an entrypoint is active. Hosts using the library directly can share a `TenantOperationConcurrencyBudget` across protected dispatchers through `TenantOperationDispatcher.WithTenantConcurrencyBudget`.

Admission takes place after fresh authorization. The budget uses the tenant ID from the verified resource scope and adjusts the two counts atomically. The slot covers factory creation, handler execution and handler cleanup. When the tenant's last slot is released, the budget removes its key. It keeps no queue. Either limit returns the generic `operation.capacity_exceeded` response, so clients receive no detail about which limit was reached.

With a host limit of two and a tenant limit of one, a held authenticated HTTP write for Alice saturates her tenant. Bob can still read his own tenant over HTTP and GraphQL. Attempts to cross tenant boundaries return the established denial on both transports. The separate tenant component test holds two cleanup operations across dispatcher instances. A third tenant is refused while both slots are in use and admitted when one slot releases. Cancellation and cleanup faults also release capacity.

These limits apply within each shared budget instance. They reserve no slot for any particular tenant and offer no ordering between competing tenants. Distributed quotas, provider qualification and canonical performance gates remain open. [Validation protocol](../validation/tenant-concurrency-budget.md)

## Evidence

The [exact Engine revision](https://github.com/Cephalon-Labs/Cehpalon-Engine/commit/baaabf1af720b1c8f021b124663323e5b4c959d0) passed 517 local checks on Windows and 514 in WSL. The actual CLI-generated Small API passed 150 verification checks on each host, including the original 39-case self-test, the original shared-host capacity fixture and the new per-tenant fixture. Invalid and duplicate serve options fail before configuration or credentials. Valid limits on the all-off profile leave all activation counters at zero. [Samples reports and hashes](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/5d434b4cfb64f10c372c07f4d57f3a5836728bc2/tooling-small-api/evidence/2026-11-18-tenant-capacity)

Hosted portable checks passed on Windows Server 2025 and Ubuntu 24.04. Hosted platform smoke passed 12 checks per runner with two real-provider checks skipped on each. #3 remains Blocked. #18 remains In Progress at M0 and its canonical benchmark gates remain as recorded. [Portable CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44318184744) · [Platform CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44318184751)
