# ADR-0040: Validate audit declarations and prepare before mutation

Status: Accepted bounded continuation. Date2026-11-20. Tracking #18, #7/#8 regressions. Root integrates; separate Engine/consumer/read-only review agents.

## Context

ADR0039 keeps explicit post-receipt recording honest about possible committed effects. Its low-level API can discover an omitted rule after mutation. Applications also need concrete startup validation and a pre-effect check while preserving the later failure boundary.

## Decision

Expose immutable sorted DescribeOperations metadata from actual stored TenantOperationRegistry registrations, without invoking handler factories, freeze or target callbacks. Metadata descriptions are information, not authority. ActivateValidated checks every configured policy rule against actual operation/action/resource-kind metadata and every explicitly required operation ID for bounded unique existence and coverage before calling the sink factory. No CRUD/action inference. Disabled skips catalog, required-enumeration and provider work. Existing Activate and RecordAsync remain available.

Bind a validated recorder to the exact immutable registry instance used for dispatch. Existing per-registration origins are insufficient because two Build calls reuse registration objects. Carry the actual registry reference privately into checked contexts; no public authority property. Rebuilding an identical registry does not satisfy the binding. Hosts must share the frozen registry while retaining fresh request-local identity/security services and lazy handler factories.

Prepare(context, cancellationToken) synchronously checks cancellation, live checked scope, exact origin and matching rule before the application performs its mutation. It does no payload capture, append or provider-readiness check. Denial/cancellation remains ordinary pre-effect failure. The opaque preparation captures the original recorder and exact context; it neither reserves a transaction nor proves a commit.

CompleteAsync(receipt, valuesFactory, cancellationToken) atomically consumes the preparation before any receipt validation, callback or await. Every attempt consumes it, including invalid/null receipts, cancellation and failure. Concurrent losers/replays invoke no new values factory or append. Completion uses the captured context/owner and existing receipt/projection/persistence checks. All completion failures report MayHaveCommitted because effects or the first append may exist. This is at most one facade append attempt per preparation, not backend exactly-once or automatic retry.

## Alternatives and consequences

Keep only post-effect recording: retain for compatibility, but it cannot catch configuration errors before mutation. Infer required auditing from write/create names: insufficient for project-specific domain actions; rejected. Validate explicit declarations plus a checked preparation: chosen, adds application integration and an optional managed object without background work. Independent database/provider failure and authorization-to-effect races remain possible; atomicity/outbox/retention and durable idempotency are application/provider responsibilities. Optional overhead is unmeasured.

## Validation

[Protocol](../validation/audit-preparation.md), [requirement](../requirements/2026-11-20-audit-preparation.md). Controlled old-source baseline, actual registry/builder-alias controls, zero disabled/provider callbacks, pre-effect denial, single-use concurrent completion and post-mutation possible effects. Full clean Windows/WSL contracts and generated HTTPS regression corpus. [Interlocked.CompareExchange](https://learn.microsoft.com/en-us/dotnet/api/system.threading.interlocked.compareexchange) supplies atomic exchange; runtime evidence separately proves this implementation. Original gates, #3/#20 and M0 remain unchanged.
