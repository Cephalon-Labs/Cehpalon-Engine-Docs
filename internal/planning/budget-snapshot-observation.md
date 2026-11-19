# Budget snapshot observation

Engine #18 now has an explicit component command for aggregate snapshot cost.

```text
dotnet Tenancy.Components.dll --observe-budget-snapshots --output=<new-json-path>
```

The [fixed protocol](../validation/budget-snapshot-observation.md) exercises the Core and tenant getters in four controlled states. Two real dispatches remain held in owned cleanup during the middle states. Five repetitions run 1,000,000 reads per lane and stage. Prebuilt delegates fold every field into a checksum. Cached-value lanes run the same loop to expose its baseline cost.

Both host runs completed all 80 measured intervals with valid checksums, ownership counts and state transitions. All intervals recorded zero caller-thread allocated bytes. The medians below include delegate and checksum cost, in ns/read.

| Host and state | Cached Core | Core getter | Cached tenant | Tenant getter |
| --- | ---: | ---: | ---: | ---: |
| Windows idle/open | 4.906 | 10.210 | 8.812 | 33.055 |
| Windows cleanup/open | 1.562 | 1.339 | 1.562 | 15.946 |
| Windows cleanup/closed | 1.562 | 1.339 | 1.562 | 15.938 |
| Windows drained | 1.561 | 1.339 | 1.562 | 15.952 |
| WSL idle/open | 1.452 | 1.837 | 7.900 | 34.217 |
| WSL cleanup/open | 1.343 | 1.568 | 1.565 | 16.435 |
| WSL cleanup/closed | 1.348 | 1.567 | 1.571 | 16.449 |
| WSL drained | 1.349 | 1.586 | 1.573 | 16.587 |

The first stage is higher on several lanes. On Windows, the Core getter's paired difference from the cached lane is negative in the later stages. Stage order, runtime warmup and baseline code paths limit interpretation of small differences. The raw series retains all five samples and signed paired differences. Separate runs would be needed to isolate a cause. These observations cover one reading thread with stable budget state. Contention, serialization, exporters and request throughput remain open.

The Engine revision passed 520 Windows and 517 WSL component checks. The existing default tenant benchmark passed all five guardrails on both hosts. The analyzer accepts both complete series and rejects four altered inputs covering a missing stage, duplicated measurement, checksum corruption and negative allocation.

The delivered change adds the explicit observation command and its analyzer. #18 remains In Progress at M0, with canonical benchmark acceptance pending.

The [retained series and source provenance](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/738481eb442db563eebbf6fa187cc1c160ce5780/tenant-identity/evidence/2026-11-19-snapshot-observation) includes original input files, analysis, build source manifests, executable hashes and a SHA-256 index. The analyzer script records each input digest and signed paired differences. Two secret-scanner candidates in the manifests were verified against the source-file SHA-256 at the Engine revision.

Hosted portable and platform jobs passed on Windows Server 2025 and Ubuntu 24.04. Platform smoke passed 12 cases per runner and left the live PostgreSQL and RabbitMQ cases unrun. #3 remains Blocked. No GitHub usage or billing action was skipped. [Portable CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44536162501) · [Platform CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44536162485)
