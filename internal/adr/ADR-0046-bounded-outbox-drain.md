# ADR-0046: Bounded manual outbox delivery with invocation-owned progress

**Status:** Accepted bounded continuation.
**Date:** 2026-11-21.
**Deciders:** Program integrator with independent scoped design review.
**Tracking:** #18 and #7/#8 regressions; #3/#20 unchanged.

## Context and decision

RelayAsync owns one bounded claim/publish/ack/release sequence. A host loop can exceed intended work, misreport a short batch as an empty backlog or lose earlier acknowledgements when a later batch fails. Add DrainAsync(context, maximumBatches=16, maximumRecords=2048, maximumPerBatch=128, cancellationToken=default) on the existing relay. Valid bounds:1..16batches,1..2048acknowledgements,1..128perbatch. Limits are experimental work caps, not throughput/latency qualification. Existing Activate/ActivateWithBudget/RelayAsync signatures remain. Existing relayTimeout starts separately for each batch; no new overall timer or total elapsed-time promise.

Require valid arguments, caller cancellation and a live audit-outbox/tenant/relay checked scope before any work. Each iteration rechecks cancellation/scope, requests min(perBatch,remainingRecords), then awaits the existing owned relay lifecycle. Count a successful batch and its returned acknowledgements before post-await cancellation/scope checks, so late failure retains actual progress. Stop on zero acknowledgements (NoProgress), record cap (RecordLimit) or batch cap (BatchLimit), in that precedence. Continue positive underfilled batches. NoProgress is not NoRowsClaimed/Drained/global emptiness: a returned empty lease or SKIP LOCKED may yield0 despite pending rows. Never inspect status/history or require those separate permissions.

Return immutable TenantChangeAuditOutboxDrainResult with Tenant, CompletedBatches, AcknowledgedCount and StopReason. These are acknowledgement observations, not unique business/delivery counts, snapshot freshness or authority. Single checked operation at entry is fresh; per-batch Demand checks revalidate that live scope, not a new identity/membership provider resolution. Expired/disposed/revoked-latched contexts stop subsequent work. Host policy still controls which operation is authorized for bulk delivery.

Once at least one batch invocation has started, wrap failure in TenantChangeAuditOutboxDrainException exposing Tenant, StartedBatches, CompletedBatches, CompletedAcknowledgedCount, InterruptedAcknowledgedCount, aggregate AcknowledgedCount, MayHaveDelivered and exact original PrimaryFailure/InnerException reference. All failures before the first batch invocation, including a changed scope at the first loop guard, remain ordinary. After StartedBatches>0, later loop/final failures carry accumulated progress; a started invocation still does not prove a provider claim or sink ran. No outer release or retry is installed: every called relay owns its own fenced cleanup. Earlier and partially acknowledged rows remain delivered; failure does not imply rollback. Raw inner errors stay trusted-host-only.

## Progress identity

A source ClaimAsync can rethrow a RelayException from an earlier call, including another tenant. Exception type/internal construction alone cannot prove current progress. Introduce a private per-invocation ledger for calls made by DrainAsync, through a private relay core retaining existing public entrypoints/semantics. Mark only the exact terminal RelayException emitted by the currently owned relay invocation. Aggregate interrupted acknowledgements/uncertainty only when that marker is reference-equal to the caught failure. Raw pre-handle forwarded errors remain original, with no borrowed partial totals. Completed prior batches remain counted. Allocate no new ledger for ordinary RelayAsync callers. Do not expose an arbitrary host callback as a progress/authority attestation.

## Options and consequences

| Option | Benefit | Cost/decision |
| --- | --- | --- |
| Host-defined unbounded loop | No framework code | Repeated limits/uncertainty errors; not selected |
| Bounded sequential helper | Reuses exact relay lifecycle, finite work and progress | Selected; no poison recovery or overall deadline |
| Durable deferral/quarantine | Can postpone bad records | Separate eligibility/status/storage/migration profile; deferred |

No implicit failed-batch retry, deadletter/drop, delay, schema/provider-interface change, background worker or extra status read. A poison record can still starve later records; the helper fails fast rather than retrying it. Source uses SKIP LOCKED and idempotent receipt fences as before. Runtime remains in existing Audit.cs, preserving17/32 scaffold input counts. New consumer DrainGateway uses generated Core/Composition dispatch and a separately configured operation grant; its additional registration intentionally changes the provider service registry hash while original security registry/legacy operation behavior remain intact.

The checked [PostgreSQL18 locking-clause documentation](https://www.postgresql.org/docs/18/sql-select.html#SQL-FOR-UPDATE-SHARE) describes skipped locked rows as an inconsistent data view suitable for queue consumers. Therefore a zero eligible claim is not a full-backlog snapshot; actual fixture controls establish only their observed concurrent state. No provider version upgrade follows from checking these semantics.

## Validation

Freeze source/protocol before SDK use. Preserve all current120outbox/56status contracts and651security/84provider cases. Add bounds/stop/underfill/cancellation/authority/partial/cleanup/replay and foreign-error-identity controls, actual PostgreSQL multi-batch partitioning, concurrent active-claim NoProgress and no status/history work. [Protocol](../validation/bounded-drain.md). GA/locked packages, original benchmark and M0/gates unchanged. Reviewed body-only7/8/18 sync/readback23 plus Project4 253field equality, main push/owned merged branch cleanup and original user hashes retained.
