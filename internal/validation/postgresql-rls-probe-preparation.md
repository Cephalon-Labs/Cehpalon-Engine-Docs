# PostgreSQL tenant isolation fixture preparation

2026-11-13. Engine issue [#12](https://github.com/Cephalon-Labs/Cehpalon-Engine/issues/12), ADR-0003, Engine revision `55c630fc5d4c47258a1a2b0da4a16ce8bc42b9f7`.

The [SQL probe](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/blob/cf8fddb725047c77b5dd1eb9f6397df871a2aba2/multitenant-business/qualification/postgres-rls-probe.sql) uses a disposable PostgreSQL 18.6 fixture database and distinct owner and runtime roles. It checks missing context, aggregate visibility with overlapping order IDs, rejection of cross-tenant inserts and updates, own-tenant writes and savepoint rollback. Fixture DDL is scoped to a transaction that rolls back on completion.

Provider execution is pending. The local session could not reach a Docker daemon, WSL denied access, and psql was unavailable on PATH. This preparation does not establish RLS, migration, driver pooling, benchmark or maturity gates.

After the SQL probe, run the Npgsql 10.0.3 checkout test. Capture the backend identity before returning and reopening the connection, check that the second transaction starts without tenant context, then verify tenant B sees only its row. Exercise both commit and rollback in separate fixed cases and retain results and provider identities.
