# ADR-0041: Await mutation and required change-trail completion

Status: Accepted bounded continuation. Date2026-11-21. Tracking #18 and #7/#8 regressions.

## Context

ADR0040 validates declarations and offers a single-attempt preparation. An application can still mutate and forget CompleteAsync. The framework cannot observe arbitrary database effects or manufacture a truthful receipt when an application callback fails.

## Decision

Add optional TenantChangeAuditRecorder.ExecuteAsync<TResult>(context, mutation, cancellationToken). The callback returns a sealed immutable TenantChangeAuditMutation<TResult> envelope containing an explicit application/provider receipt, typed result and optional lazy state factory. Add runtime types to existing Audit.cs; fixed scaffold source inventories remain unchanged. Keep low-level APIs compatible.

Validate a null callback, Prepare and one final cancellation check before invoking mutation. These failures remain ordinary pre-effect failures. Invoke and await the trusted callback exactly once with the original token. After invocation begins, wrap all failures conservatively with TenantChangeAuditWriteException.MayHaveCommitted, without wrapping an existing such exception again. This includes synchronous exceptions, asynchronous failures, cancellation, null envelopes, invalid receipts, projection or persistence errors. Do not retry the callback or append.

When a callback returns its receipt, await preparation.CompleteAsync with CancellationToken.None. Existing private writeTimeout and live checked-scope/registry/receipt checks still apply. Then recheck the caller token before returning the typed result. This is an explicit helper policy: caller cancellation after receipt does not itself suppress required persistence, but may withhold a result after a successful append. Existing direct CompleteAsync(callerToken) still checks that token before append. Context expiry, a rejected receipt or private timeout can prevent or fail persistence. No unconditional append or delivery claim.

If the callback throws after partial effects without a receipt, report uncertainty and leave trail0; do not guess state or append a fabricated success. Applications need their own transaction/outbox, reconciliation and idempotency where required. The helper cannot force consumers to await it, stop uncooperative callbacks/providers, authorize future effects, prove a DB commit, hide write errors, or make business writes atomic with trails. Immutable envelopes do not freeze arbitrary TResult object graphs.

## Alternatives and evidence

Keep only manual preparation: compatible, but omission remains easy. Automatically wrap every handler or infer changes from operation names: rejected because project semantics, receipts and disabled-module behavior are explicit. Choose the optional typed helper with its declared uncertainty boundary.

The implementation follows the sequential [async/await model](https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/) and [.NET cooperative cancellation](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads); these platform references do not establish Engine behavior. [Frozen conformance protocol](../validation/audit-execution.md) and actual consumer evidence provide the scoped proof. Private deadlines are cooperative; a provider ignoring cancellation can remain pending. Separate helper invocations can each mutate/append; no cross-call idempotency. Optional overhead remains unmeasured; original benchmark gates unchanged.
