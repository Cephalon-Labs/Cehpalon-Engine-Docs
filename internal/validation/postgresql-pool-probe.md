# PostgreSQL pooled tenant context probe

2026-11-13. Engine #12, ADR-0003, Engine revision `55c630fc5d4c47258a1a2b0da4a16ce8bc42b9f7`.

[Probe source](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/blob/24c1c1e7d9747d442c9443827d0871a78da976b9/multitenant-business/qualification/PostgresPoolProbe.cs). Build passed on Windows using SDK 11.0.100-rc.3.26522.148 and locally cached Npgsql 10.0.3 with online audit disabled for the offline build. Provider execution remains pending.

Use a disposable PostgreSQL 18.6 fixture. Supply its connection string through `CEPHALON_PROBE_POSTGRES` and run `dotnet run --file multitenant-business/qualification/PostgresPoolProbe.cs` from Samples. The probe checks a fresh transaction before the original connection closes, then opens a second connection and requires the same backend PID. Both commit and rollback cases check that the next transaction starts with no tenant context and can set its own context.

This probe checks transaction-local context and pool reuse. Run the adjacent SQL RLS probe separately for row visibility and write isolation. Real-provider, migration and benchmark gates remain pending.
