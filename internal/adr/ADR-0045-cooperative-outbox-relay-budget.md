# ADR-0045: Optional cooperative audit outbox relay budget

**Status:** Accepted bounded continuation under the user's existing audit/outbox request.
**Date:** 2026-11-21.
**Deciders:** Program integrator, with independent scoped design review.
**Tracking:** #18; #7/#8 boundary regressions. #3/#20 unchanged.

## Context

Relay lease checks bound authority after awaits, but cannot request cancellation of a blocked provider/sink. [Cooperative cancellation](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads) requires the participant to observe a supplied token; a timeout is not forced termination. Existing callers and provider interfaces must retain their behavior unless a project explicitly selects the new option. Current GA baseline and packages stay unchanged.

## Decision

Retain the original TenantChangeAuditOutboxRelay.Activate CLR signature and delegate through one private activation helper with null budget. Add distinct ActivateWithBudget(bool enabled, TimeSpan? relayTimeout, sourceFactory=null, sinkFactory=null, leaseDuration=null, timeProvider=null). A separate name avoids optional-overload ambiguity and retains the original compiled entrypoint, without claiming general ABI qualification. Disabled returns null before argument/factory work. Enabled configured bounds are positive<=1minute and checked before factories; null creates no new work-budget or linked token sources and retains legacy cancellation/fault behavior; the existing private cleanup budget remains. Keep runtime in existing Audit.cs to preserve scaffold inventories.

For configured calls, start private CancellationTokenSource before ClaimAsync and link with caller cancellation for claim, sink and acknowledge. Retain timer through final success validation. Check caller first, then private budget, alongside existing scope/lease checks. A private expiry during independent cleanup can withhold success even after all acknowledgements; retain counts rather than imply rollback. Release always uses its existing separate5second token, even when caller/private signals are set. Await uncooperative I/O to completion, then reject late success; no Task.WhenAny/abandoned task or latency promise. Existing timeProvider remains the lease UTC/monotonic clock, not the new system timer's clock.

Classify observed OperationCanceledException only for configured budget calls: requested caller becomes caller-token OperationCanceledException; otherwise requested private timer becomes generic TimeoutException retaining trusted-host inner diagnostics. Preserve unrelated exceptions even if a deadline has since elapsed; other provider OCE remains original when neither signal is requested. Caller precedence when both signals are observed does not establish which caused an I/O exit. Old null-budget calls retain original errors/tokens without normalization.

Claim failures before a handle exists retain the raw pre-lease exception shape, with configured cancellation classification; the trusted source owns partial-acquisition cleanup/expiry. When Claim returns a known lease after timeout/caller cancellation, assign it before rejecting, then release under the independent token. Late null also rejects rather than reports0. Known-lease failures belong in TenantChangeAuditOutboxRelayException.PrimaryFailure; ReleaseFailure stays separate. MayHaveDelivered becomes true once sink invocation is attempted, even if no acknowledgement succeeds. Sink/ack failure may already have delivered or acknowledged; no rollback/exactly-once claim. Existing tenant, fresh relay scope, lease fence and idempotent receipt rules remain.

## Options considered

| Option | Compatibility | Behavior | Decision |
| --- | --- | --- | --- |
| Implicitly reinterpret lease duration as I/O timeout | Changes legacy calls | Mixes authority/lease and cancellation policies | Rejected |
| Abandon work at a timeout with Task.WhenAny | Returned work can continue mutating | Loses completion/cleanup accounting | Rejected |
| Distinct activation with nullable cooperative budget | Original CLR entrypoint retained; provider contracts unchanged | Requests cancellation, awaits owned work, retains uncertainty | Selected |

## Consequences and action items

Projects choose a budget separately from the authority lease. Expired work can still hold resources until an uncooperative provider returns. Timer/signal races are checkpoint observations, not causal/freshness guarantees. Raw inner diagnostic messages stay trusted-host-only and must not be serialized to public responses. No retry/deadletter/renewal/schema migration/background service is added.

Implement contract tests for disabled/invalid/null paths, all awaited phases, late known/null claims, caller precedence/token identity, unrelated faults, ack uncertainty, independent cleanup and foreign/expired scopes. Actual PostgreSQL consumer tests retain all60 original cases and prove opt-in behavior with actual provider progress/barriers, cancellation/quiescence, replay/dedup and tenant denial. [Predeclared validation](../validation/relay-budget.md). All runtime maturity/gates remain M0/planned or blocked at their existing values.
