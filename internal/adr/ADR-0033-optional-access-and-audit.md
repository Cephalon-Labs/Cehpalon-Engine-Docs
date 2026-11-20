# ADR-0033: Optional authentication, RBAC/ABAC and tenant audit history

Status: Accepted for the user-authorized portable/local sample slice; provider and supported-host qualification remain open.
Date: 2026-11-20
Tracking: Engine #8 (identity/policy), #18 (audit/history), #7 tenant boundary reused. #3 remains Blocked.

## Context

The user explicitly requested optional authentication, RBAC, ABAC and audit/history for framework consumers. ADR0007 already denies missing identity/membership/resource/policy authority before creating business handlers. Public Core dispatch remains available. We must not treat a constructed principal, request metadata, role header or caller-selected resource owner as authority.

## Decision

Add a BCL-only Authorization module implementing ITenantAccessPolicy and its optional leased decision contract. Freeze bounded rules once, look up the exact operation/action/resource kind, and resolve fresh principal/tenant/membership-version/resource-version-bound facts from a configured trusted source. Rules require any configured role AND every configured attribute predicate. RBAC-only and ABAC-only rules are supported; an unconstrained rule is invalid. Missing attributes/rules/facts, wrong binding and expired facts deny. The leased decision carries its observed lower validity bound and fact expiry into dispatch: expiry or UTC rollback while awaiting audit denies before business creation, and fact expiry caps the checked operation lease. Equality is ordinal and typed by subject/resource/environment scope; no expression execution, wildcard role escalation, cross-tenant administrator bypass or decision cache.

Add an optional ASP.NET Core JWT identity adapter that calls AuthenticateAsync with an explicit host-configured scheme. Only a successful ticket for that exact scheme and one authenticated identity can be mapped. Require one each of iss/sub/nbf/exp with bounded representation, integral dates and a valid lifetime. Cryptographic signature, issuer/audience/algorithm/key validation belongs to the established JwtBearer handler. The portable contracts never parse tokens. Anonymous, malformed or expired authenticated representations deny; infrastructure exceptions/cancellation remain faults/cancellation. Host maps no inbound claims when using the standard claim names.

Add optional tenant audit services to TenantSecurityServices. When absent, no sink factory, identity/history persistence or additional audit envelope is created. When enabled, persist authorization success before invoking business work, then a terminal success/rejection/denial/cancellation/fault event after owned cleanup; early denial/fault has one terminal event. Events contain structured identifiers/outcomes only, no token, raw claims, request/response body or exception message. Denied/unverified tenants are never stamped as authorized tenant history. Persistence is required: pre-execution failure prevents business work; terminal persistence failure is surfaced with an explicit may-have-executed flag. Preserve both execution and audit errors. Each write has an independent bounded cancellation token so caller cancellation still permits terminal recording; the trusted sink must honor cancellation. Abrupt process loss can leave an authorization record without a terminal record. This is not a transactional outbox, exactly-once delivery, tamper-proof log or rollback guarantee.

Add a checked history facade over a consumer-provided store. Read requires an active audit-history/read scope, passes the checked tenant to the store, enforces a bounded page and rejects foreign/unverified-tenant records. Recheck the lease after the asynchronous store call. Actual retention, durable transactions, encryption, access policy, redaction, idempotency and archival remain store/application responsibilities. Sample memory storage is fixture-only.

## Options considered and trade-offs

- Host-only security: least framework coupling, but duplicates the same portable role/attribute/audit boundary across transports. Keep protocol authentication in the host while sharing policy and audit contracts.
- New expression language and account/password/token issuer: broad flexibility but substantially larger parser, lifecycle and security scope. Reuse established authentication and explicit bounded policy predicates instead.
- Best-effort fire-and-forget audit: lower response coupling but silently loses evidence and cleanup ownership. Choose awaited required persistence with explicit partial-effect failure semantics.
- Mandatory security on plain Core: prevents public profiles and changes existing behavior. Keep optional composition; protected operations must use TenantOperationDispatcher.

## Consequences and validation

Consumers may replace authority/authentication/audit providers independently. Disabled modules must activate zero module-owned factories or endpoints. Fresh policy lookup can incur provider latency and audit writes can fail an otherwise successful request; there is no unmeasured performance claim. Validate real signed-token localhost requests, both HTTP and GraphQL, roles/attributes, tenant mismatch, missing/expired/revoked facts, cancellation, sink failures, cleanup, history leakage, disabled modules and generated typed gateway compilation. Keep original benchmark gates and unknown person-hours unchanged. No real IdP, external durable audit provider or production qualification is implied.

Primary references: [ASP.NET authentication](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/), [resource authorization](https://learn.microsoft.com/en-us/aspnet/core/security/authorization/resource-based), [role authorization](https://learn.microsoft.com/en-us/aspnet/core/security/authorization/roles), [OWASP logging](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html).
