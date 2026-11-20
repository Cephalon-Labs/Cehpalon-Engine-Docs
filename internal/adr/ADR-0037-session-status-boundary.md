# ADR-0037: Optional fresh session-status identity boundary

Status: Accepted for the bounded continuation authorized by the user; provider/host/production qualification remains open.
Date: 2026-11-20. Tracking #8, #7/#18 regression coverage. Root integrates; separate implementation, consumer and read-only review agents.

## Context

The local key-ring completion gate governs token validation. A successfully authenticated ticket may later be cached, while tenant dispatch resolves identity afresh. A session lookup only inside a JWT handler would miss those later operations and established cookie/custom ticket paths. Consumers need an explicit port to their own session authority without a framework-owned account/token/session database.

## Decision

Add optional immutable SessionId metadata to IdentitySnapshot through a new five-argument constructor while preserving the existing exact four-argument signature. Session metadata is bounded opaque text, never authority by construction. Keep new portable definitions in the existing IdentityContracts.cs so fixed scaffold source inventories remain valid. Legacy sources keep SessionId=null and no session lookup unless explicitly decorated.

Add SessionStatusSnapshot bound to exact principal (issuer/subject), authentication scheme and session ID, active flag and validity interval. A configured IIdentitySessionStatusSource receives the authenticated identity. SessionValidatingIdentitySource decorates IIdentitySource and resolves that authority on every protected identity resolution without cache or stale fallback. Anonymous/sessionless identities skip the port and deny in this selected mode. Null/inactive/misbound/not-yet-valid/expired responses deny. Infrastructure exceptions and cancellation propagate through existing fault/cancellation paths.

Require a positive maximumObservationLifetime of at most five minutes, explicitly chosen by the application. Capture UTC/timestamp before upstream I/O. At completion reject backward UTC/timestamps, negative or exhausted elapsed budget and expired representations. Intersect returned validity with original identity/status windows and both startUTC+cap and completionUTC+(cap-observedElapsed), using overflow-safe arithmetic. This consumes slow lookups even if UTC stalls. Returned immutable identity retains SessionId and clamps its lower validity bound to the completion UTC observation, so later rollback into the lookup interval fails normal trust checks; later tenant/policy leases inherit its UTC expiry. The budget is checked when awaits complete; it does not time out an uncooperative provider. Provider I/O deadlines and cancellation cooperation belong to the host/source, and the portable decorator observes its supplied CancellationToken (HTTP passes request cancellation). No background renewal or continuously subscribed revocation capability is added.

Keep original JWT constructor behavior. A separate explicit four-argument overload selects a unique authenticated session claim. A SessionBoundTicketIdentityMapper wraps an existing established cookie/custom mapper using that same successful ticket. No caller header, HttpContext.User flag, tenant ID, role or unauthenticated token parsing supplies session authority. Read-set per-child fresh identity resolution must compare and preserve ordinal SessionId, including null: the same user switching login session during an aggregate is rejected, without partial response rows. Earlier authorized reads may have executed.

Session IDs must be unique per login/generation and must not be reused/reactivated while older credentials may exist. A response-only version cannot prevent credential replay; omit such a misleading generation guarantee. The provider owns persistent revocation/tombstones, credential generation binding, logout/account-disable policy, consistency and cross-node invalidation. This port is not an OAuth introspection or revocation protocol implementation.

## Options considered and trade-offs

- JWT TokenValidated callback only: smaller integration, but misses cached-ticket and later tenant-operation checks; unsuitable as the sole guard.
- Framework-owned token blacklist/session database/logout endpoint: expands account, storage, consistency and security scope; defer to established providers/application policy.
- Fresh portable identity decorator over a trusted status port: selected. Reuses tenant/switch/read-set entrypoints and existing audit; adds provider latency/failure per identity resolution. Its cost has not been benchmarked.

## Consequences and limits

Session observation is not atomic with later membership/policy/audit awaits, business admission, provider transactions or response delivery. The original observation monotonic origin is not propagated through those later awaits: the cap bounds source observation and the returned UTC interval, not an end-to-end admission/revocation deadline when UTC later stalls. Revocation after the observation can race subsequent admission until the bounded lease ends; already admitted work may finish. Rechecks happen at declared protected entrypoints, not arbitrary C# calls. Plain Core/codegen remains unprotected unless routed through the trusted boundary. Host AuthenticateAsync/HttpContext.User/cached cookies may still report authentication: this decorator does not clear tickets, sign out the host or automatically guard ordinary RequireAuthorization routes. Every other entrypoint needs an explicitly equivalent session check. Protected tenant operations use the existing generic access.denied response (HTTP403), not a new global HTTP401/logout protocol. No real provider/distributed revocation or production guarantee follows.

Normal required operation audit records denial/fault/cancellation outcomes with verified tenant-history rules. Raw SessionId/tokens/keys/claim bags never enter framework audit. Session-management/logout audit and durable storage remain the host/provider's responsibility. Disabled composition must activate zero session-owned factory/provider work. Original benchmarks, #3/#20, M0 and metadata are unchanged.

## Validation and sources

[Predeclared protocol](../validation/session-status-boundary.md), [requirement](../requirements/2026-11-20-session-status.md). Validate exact source on pinned SDK Windows/WSL, all previous components/consumer cases, new malformed binding/time/cancel/fault/cache/parallel/session-swap tests and actual generated HTTPS HTTP/GraphQL signed/JWE paths. Retain every attempt and executing source without credentials.

Primary references: [ASP.NET cookie backend changes](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/cookie#react-to-back-end-changes), [OAuth introspection RFC7662](https://www.rfc-editor.org/rfc/rfc7662.html), [OAuth revocation RFC7009](https://www.rfc-editor.org/rfc/rfc7009.html). Established handlers/providers own those protocols; this decision supplies a local integration boundary only.
