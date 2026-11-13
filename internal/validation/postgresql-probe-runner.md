# PostgreSQL probe execution

Engine #12, ADR-0003. From the Samples review branch and its root, run:

```powershell
pwsh -File multitenant-business/qualification/run-postgres-probes.ps1
```

The [runner](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/blob/9e8269b534c8160251b7db576320293af1ce4eb2/multitenant-business/qualification/run-postgres-probes.ps1) requires Docker with linux/amd64 support and the pinned .NET SDK. It starts the W0-pinned PostgreSQL image on an ephemeral loopback port, verifies server version 18.6, runs the RLS and Npgsql probes, then removes the owned container and its anonymous volumes.

2026-11-13 preflight: PowerShell parse passed. The Docker daemon pipe was unavailable, so execution stopped before creating a container. Live RLS and pool evidence remains pending.
