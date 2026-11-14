# PostgreSQL probe execution

Engine #12, ADR-0003. From the Samples review branch and its root, run:

```powershell
pwsh -File multitenant-business/qualification/run-postgres-probes.ps1
```

The [runner](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/blob/9e8269b534c8160251b7db576320293af1ce4eb2/multitenant-business/qualification/run-postgres-probes.ps1) requires Docker with linux/amd64 support and the pinned .NET SDK. It starts the W0-pinned PostgreSQL image on an ephemeral loopback port, verifies server version 18.6, runs the RLS and Npgsql probes, then removes the owned container and its anonymous volumes.

2026-11-13 preflight: PowerShell parse passed. The Docker daemon pipe was unavailable, so execution stopped before creating a container. Live RLS and pool evidence remains pending.

A Windows PowerShell harness substituting Docker and dotnet commands passed four scenarios: successful orchestration, SQL failure, Npgsql failure, and SDK mismatch. It checked that SQL failure stops before the Npgsql probe, that the prior connection environment is restored and cleanup is requested after attempted execution, and that SDK mismatch stops before container creation. Both the default and desktop-linux Docker daemon pipes were absent on the host. These are control-flow results only; no database connection or actual container cleanup was exercised.

## Hosted attempt on 2026-11-14

[GitHub Actions run 43540842877](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/actions/runs/43540842877) ran against Samples workflow revision `4263ee896e69067af6520880c3d2f49ae89fbbdd`. GitHub marked the job failed with zero recorded steps and no available log blob. The underlying startup reason is unverified. This attempt establishes no PostgreSQL result. The local Docker Desktop Linux engine pipe also remained unavailable. Keep the live RLS and pool verification pending.
