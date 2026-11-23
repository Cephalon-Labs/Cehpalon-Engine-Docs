# PostgreSQL runtime role and connection pool proof

Engine #7 and #12. The Business profile selected PostgreSQL with
transaction-local tenant scope and row-level security. This run exercises
that boundary in a disposable Samples fixture. PostgreSQL 18.6 used the
pinned Linux amd64 image, with Npgsql 10.0.3 under .NET 11.0.0 on WSL
Ubuntu 22.04.5. [Business profile](../adr/ADR-0003-multitenant-business-profile.md)

The fixture uses separate PostgreSQL table owner and runtime roles. It
enables and forces RLS on a table where both synthetic tenants have the
same order ID. The direct SQL probe validates tenant-scoped reads and
writes and savepoint rollback. A separate Npgsql process signs in with the
runtime role. The process checks that it lacks superuser, RLS bypass and
owner-role membership, and that the table reports RLS and forced RLS.

| Check | Observed result |
| --- | --- |
| Default execution | SQL rolled back setup. Both administrator-context pool cases passed. |
| Runtime login after commit | Same backend reused. The unscoped transaction saw zero rows. Tenant A and then tenant B each saw its own row for the shared order ID. |
| Runtime login after rollback | Same backend reused and the same zero-row and tenant-row assertions passed. |
| Direct SQL invocation with false flag | Both fixture roles and schema were rolled back. The two default pool cases passed. |
| Direct SQL invocation with true flag and missing password | psql exited with code 3 before the app opened its pool. Both fixture roles and schema were rolled back. |
| Ownership and cleanup | Each run used its own container. All four final runs verified that the container and volume were removed and the loopback port closed. |

Each runtime case additionally verified zero rows before the original
tenant scope was set and after commit or rollback before closing the
connection. These assertions show the effect of transaction scope and
reused connections under the real login. Trusted tenant resolution and
privilege assignment still rely on the application and deployment design.

The local fixture sources are pinned to Samples commit
`d430791a02355134a9610f22ea12d3376318fd7d`. The workflow changes in
Samples PR 2 leave those fixture sources unchanged. The initial WSL
wrapper attempt stopped before creating a container. That failure and
the subsequent precursor runs were retained locally. Public evidence
summarizes hashes and cleanup results from the reviewed final runs.
[Local observations](../evidence/postgresql-runtime-pool/2026-11-23/local-observations.json) · [Samples PR](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/pull/2)

GitHub Actions ran both modes on Ubuntu 24.04 from the PR head. It
confirmed one commit and one rollback receipt in each mode. PR 2 was
merged to Samples main after the run passed.
[Hosted run](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/actions/runs/45213986875) · [Hosted result and revisions](../evidence/postgresql-runtime-pool/2026-11-23/hosted.json)

Run from the Samples checkout with Docker and its pinned .NET SDK.

```powershell
pwsh -NoProfile -File multitenant-business/qualification/run-postgres-probes.ps1
pwsh -NoProfile -File multitenant-business/qualification/run-postgres-probes.ps1 -RuntimePool
```

The evidence covers this PostgreSQL fixture and Npgsql configuration.
Engine provider implementation, application migrations, query bounds,
production isolation, event and Worker paths, and the full Business
workload retain their own acceptance criteria. #7 remains Blocked and #12
remains Backlog, both at M0.
