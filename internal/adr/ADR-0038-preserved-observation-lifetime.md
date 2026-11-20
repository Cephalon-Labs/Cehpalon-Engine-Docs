# ADR-0038: Preserve restrictive observation origins through tenant work

Status: Accepted bounded continuation. Date2026-11-20. Tracking #8/#7/#18. Existing constructors/properties, original benchmark gates and #3/#20 remain intact.

## Context

ADR0037 explicitly limited source observation validity to the lookup and returned UTC interval. A later membership/policy/audit await could consume the original monotonic budget while UTC stalled, then start a fresh tenant lease. Root and a read-only design agent selected a restrictive lifetime constraint carried with the authenticated identity to close that documented gap.

## Decision

Keep immutable public identity metadata and exact existing constructor/property shape. SessionValidatingIdentitySource privately attaches a finite set of clock-origin constraints; ordinary public DTO construction does not authenticate or mint such constraints. Each constraint retains the trusted original clock/timestamp, completion UTC window, native elapsed ceiling and shared permanent invalidity latch. Native remaining time is min(maxObservationLifetime-completionElapsed, returnedExpiryUtc-completionUtc), so the initial shorter identity/status expiry remains effective under stalled UTC. Clock reads and last UTC/timestamp/elapsed updates occur under its lock; partial rollback, expiry/exhaustion latch denial. First clock exception latches then propagates, later checks deny. No arbitrary callbacks, background workers, network or status refresh occur during constraint checks.

Public WithValidity only narrows UTC bounds and preserves the same constraint references. IntersectValidity requires exact principal/scheme/session binding, intersects UTC and combines at most16 distinct reference-deduplicated constraints; mismatch/disjoint/overflow fails closed without truncation. SatisfiesObservationConstraints returns true for unconstrained representations and explicitly does not authenticate or replace issuer/scheme/ordinary UTC trust validation. Arbitrary trusted-host DTO reconstruction can discard constraints; this remains outside a C# sandbox guarantee.

Existing IdentityTrustPolicy and AuthorizationLease retain/check constraints. Nested session sources retain inherited origins and matching-session ticket mapping preserves the original object. Parent read-set lease and each child carry both parent and fresh constraints, so fresh lookup cannot restart the parent's budget. UTC narrowing does not mint a new monotonic TTL for arbitrary narrowed dates. The grant/membership/policy source's own missing origins are not invented by this session-specific feature.

Check observation validity after policy before authorization audit, again after audit and before handler construction, on checked context access and after successful Core/budget completion including owned cleanup. A final guard-only successful-result check also follows required terminal-audit persistence, matching the read-set boundary. Expired successful results become access.denied; business failure, cancellation, cleanup and persistence faults keep precedence. A terminal event records the processing outcome computed before its persistence; expiry during that persistence may withhold the response without rewriting the earlier Succeeded fact or inventing a second terminal stage. It is not an atomic response-delivery receipt. Effects may already exist. Expiry during required audit can leave authorization plus terminal-denial records without business execution; authorization records are not proof of handler admission.

## Alternatives and consequences

A second leased-source interface would duplicate resolution and ownership across every wrapper; chosen private restrictive constraints reuse existing entrypoints. Flat bounded sets avoid recursive lock graphs; evaluate one lock at a time. Legacy identities do no observation clock work. Optional locking/checking/copy cost is unmeasured. This is not an I/O timeout, live revocation subscription, database rollback, atomic response or distributed provider guarantee.

## Validation

[Protocol](../validation/observation-lifetime.md). Preserve old9850bed controlled stalled-UTC admissions, then require equivalent fixed denials. Cover all authority/audit waits, native shorter expiry, nested/copy/parent-child preservation, shared latches/concurrency/faults and post-cleanup success withholding. Exact full Windows/WSL and generated HTTPS tests; preserve failed attempts/source. [TimeProvider timestamp](https://learn.microsoft.com/en-us/dotnet/api/system.timeprovider.gettimestamp) and [elapsed time](https://learn.microsoft.com/en-us/dotnet/api/system.timeprovider.getelapsedtime) describe the BCL clock mechanism, not runtime proof of this implementation.
