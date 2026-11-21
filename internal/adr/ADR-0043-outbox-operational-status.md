# ADR-0043: Optional protected outbox operational status

Status: Accepted bounded continuation. Date2026-11-21. Tracking #18 with #7/#8 regressions; root sole remote writer.

## Decision

Add immutable TenantChangeAuditOutboxStatus with Tenant, ObservedAtUtc, Pending, Available, Claimed, ExpiredClaims, Delivered and nullable OldestPendingAtUtc. Claimed means active unexpired claims; Available includes unclaimed and expired-claim pending rows. All counts are nonnegative, Available<=Pending, Claimed=Pending-Available and ExpiredClaims<=Available, using overflow-safe subtraction. OldestPendingAtUtc is null exactly when Pending0 and otherwise no later than ObservedAtUtc. Normalize offsets to UTC. DTO construction is information, not authority; provider timestamps do not establish client freshness or a distributed clock guarantee.

ITenantChangeAuditOutboxStatusSource.ReadAsync(tenant,token) returns one provider-reported snapshot. TenantChangeAuditOutboxStatusReader.Activate(enabled,factory,readTimeout) returns null for Disabled without factory/argument work; enabled validates a positive<=1minute read budget before calling the provider factory. Default5seconds. Runtime types stay in existing Audit.cs to preserve fixed scaffold source inventories17/32 and avoid vendor objects in portable contracts.

Reader.ReadAsync requires a fresh checked audit-outbox/tenant/inspect context. Relay, writer and field-history permission alone do not grant inspect. Demand the exact active scope before I/O, verify the returned owner and non-null snapshot, then demand scope/cancellation again before publishing. Pass a linked caller/private deadline token to the provider. Caller cancellation remains caller OperationCanceledException; private expiry without caller cancellation becomes TimeoutException, including cooperative source cancellation and late successful completion by a source ignoring cancellation. Preserve unrelated provider failures. Timeout Message is generic, while its inner provider cancellation exception remains available to trusted-host diagnostics; do not serialize/log raw inner errors to public responses. Existing adapters must retain their unexpected-error redaction. If both tokens are requested, caller cancellation wins. This is cooperative I/O budgeting, not forced completion, global revocation or atomic response delivery. Do not cache, poll, start workers or expose endpoints automatically.

## PostgreSQL proof

The optional consumer reads status in one parameterized SQL statement for one tenant. A materialized single clock observation classifies all claims consistently, and aggregate filters calculate counts plus minimum pending database enqueue time. Add database-generated enqueued_at only to newly created owned fixture schemas; do not migrate historical retained data. Explicit [PostgreSQL date/time semantics](https://www.postgresql.org/docs/18/functions-datetime.html) and [aggregate FILTER behavior](https://www.postgresql.org/docs/18/tutorial-agg.html) inform the implementation; source/runtime proof remains separate. A snapshot reflects that provider statement, not continuously current backlog, global health or automatic recovery.

Keep prior transaction/outbox37 and HTTPS651 cases. Add actual status lifecycle, empty tenant, scoped permission, wrong-owner rejection, read-only sideeffects and consistent concurrent aggregate cases. Use the same verified owned PostgreSQL18.7/Npgsql10.0.3 fixture and existing Windows-loopback-proxy/WSL-direct topology; no provider upgrade, new host settings, production or supported-Windows #3 qualification. [Protocol](../validation/outbox-status.md).

## Project synchronization

Read live Project4 items with pagination, compare all23 issue/item identities and Status/Priority/estimates/actual/remaining/Maturity/Test gate/Benchmark gate/Feature against task mirrors and observed snapshot. Update only evidence-backed intended changes through reviewed two-way sync. Existing broad gates remain unchanged; explicitly record equality rather than forcing field writes solely to show activity.
