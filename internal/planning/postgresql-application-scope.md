# Application PostgreSQL slice for #7 and #12

The first read, write and migration slice has a local WSL provider proof. [Observed scope and limits](../validation/postgresql-application-scope.md)

Build an optional Business sample that performs a typed order read and a
bounded write using the PostgreSQL and Npgsql versions already selected for
the Business profile. Use an actual Engine tenant dispatcher and synthetic
identity sources. A provider operation requires the exact checked action,
resource kind and canonical order ID before opening a database connection.
Derive the tenant from the checked context. Use an ordinal text tenant key
and composite tenant/order key so Engine's opaque tenant IDs and order ID
reuse work together.
[Business profile](../adr/ADR-0003-multitenant-business-profile.md) ·
[Runtime-role and pool proof](../validation/postgresql-runtime-pool.md)

Own one Npgsql connection and transaction for each database operation. Set
the tenant scope transaction-locally with a bound value and use a bound
tenant and order key in each bounded query. The restricted runtime role
owns no application tables. Forced row-level security applies to the same
tenant key. Recheck the checked scope before committing. Treat a commit
without acknowledgement as an uncertain outcome, and avoid generic write
retry. The store exposes typed order operations and keeps the connection
and transaction private.
[Transaction boundary](../adr/ADR-0042-audit-transaction-outbox.md)

Apply the versioned schema explicitly under its own fixture role. Give the
runtime role the minimum order-table grants. Schema migration, runtime
startup and operations have separate lifecycles. The proof should include
initial migration and an atomic failure or equivalent rejected replay.
Record the precise migration and replay behavior implemented by the
fixture. The production migration strategy depends on later requirements.

Use the pinned disposable Linux PostgreSQL fixture. Verify that tenants A
and B can use the same order ID with distinct values, invalid scopes cause
zero provider checkout, a successful write affects a bounded row count,
and a controlled rollback leaves the previous state intact. Include
transaction scope clearing on a reused backend and cleanup of the owned
fixture. State the cases actually proved, including any reused evidence
from the prior pool probe.

Keep the first slice in Samples. #7 also needs the remaining protected
provider and lifecycle paths. #12 also needs the real provider contracts,
query/concurrency/migration evidence and other selected data capabilities.
Durable eventing, Worker, external identity, dedicated benchmark and
production deployment keep their own gates.
