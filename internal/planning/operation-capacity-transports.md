# Operation capacity responses across HTTP and GraphQL

The [in-process budget](operation-concurrency-budget.md) gives authenticated application hosts an optional capacity limit. The two adapters recognize the reserved Core code `operation.capacity_exceeded` and apply the same generic message. Install the budget in the host's invocation bridge after required tenant authorization. The adapter checks and business-handler lifetime remain separate.

| Adapter | Response at saturation |
| --- | --- |
| HTTP adapter | HTTP 503 with a problem body and `code: operation.capacity_exceeded` |
| GraphQL adapter | HTTP 200 with `errors[].extensions.code: operation.capacity_exceeded` for an executed resolver |

Neither client receives capacity, queue or vendor details. The HTTP mapping has no `Retry-After` estimate because the Core limit releases on work and cleanup completion. Standard authorized business errors keep their existing status and message contracts.

The component suite starts a real loopback host with both adapters over one limit of one. The HTTP request holds the permit. Subsequent HTTP and GraphQL requests return the reserved error without opening another factory, and a GraphQL request succeeds after release. Separate adapter checks inject a reserved-code result with a sensitive-looking message and verify redaction. Existing tenancy checks cover authorization before admission and cleanup through cancellation and faults.

## Recorded evidence

The exact [runtime revision](https://github.com/Cephalon-Labs/Cehpalon-Engine/commit/e3726fdc6db5e7717437bff7d2d85d9c34b60d87) passed 515 local checks on Windows and 512 on WSL on the pinned SDK. It includes 52 HTTP and 47 GraphQL checks per host. The final Engine head adds documentation only. [Raw reports and checksums](../evidence/operation-capacity-transports/SHA256SUMS.txt)

This observation establishes correctness at the component boundary. Throughput, distributed budgets, provider qualification and the original benchmark acceptance remain pending.

GitHub Actions passed the [portable contract workflow](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44092534352) for Windows Server 2025 and Ubuntu 24.04 at the final Engine head. The separate [platform smoke workflow](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44092534435) passed 12 checks on each runner and left two real-provider checks unrun because the owned PostgreSQL and RabbitMQ connections were absent. Windows Server 2025 x64 appears on the [.NET 11 supported OS list](https://github.com/dotnet/core/blob/main/release-notes/11.0/supported-os.md). #3 stays Blocked for the remaining qualification.
