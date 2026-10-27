# ADR-0007 — Tenant/identity contracts over Core

Date: 2026-10-27. Status: Accepted for the user-authorized portable subset of #7/#8. #3 and the existing full acceptance/dependency gates remain Blocked under ADR-0005. This is not an OIDC, real provider, browser or deployment qualification.

## Trust and invocation

Identity contracts are BCL-only immutable data: the principal key is the exact ordinal issuer/subject pair, an authentication scheme and a validity window. Constructors validate representation only; constructing a snapshot does not authenticate a caller. The host configures a trusted `IIdentitySource` and explicit issuer/scheme allowlists. It resolves identity afresh for every invocation. Raw bearer tokens, `ClaimsPrincipal`, headers and Core correlation metadata do not enter the portable trust contract as authority.

The tenant dispatcher performs these steps before creating a business handler:

1. Look up exact operation/request/response binding, take a trusted defensive request snapshot, and derive the untrusted tenant/resource selection from that same snapshot. Action and resource kind come from server registration, not request metadata.
2. Resolve current identity and validate its exact trust/time bounds.
3. Resolve current membership and require the same issuer/subject and requested tenant, active state and valid time window. No wildcard/admin role bypasses membership.
4. Resolve resource scope using the requested tenant plus resource kind/ID, then independently verify the returned actual tenant/kind/ID. Tenant-scoped duplicate resource IDs are valid; selection is not authority.
5. Evaluate the configured policy; absence of a policy denies. Semantic authorization failures return one generic denial rather than exposing membership/resource existence.
6. Mint an internal invocation lease bound to the operation/contracts/principal/tenant/action/resource and delegate through Core using an opaque invocation. Enforce UTC identity/membership validity and a monotonic elapsed lifetime cap; observed invalidity permanently revokes the lease. Recheck cancellation/lease validity before and after the business factory. Revoke after cleanup, including exceptions/cancellation.

`ITenantOperationHandler` receives a separate checked `TenantOperationContext`. Core `OperationContext` remains correlation metadata. The tenant registry does not expose its raw Core registry or a public constructor that can mint an authorized context. A retained context cannot be reused after the invocation or broadened to another tenant/resource/action. Handler resources remain newly owned per call and Core cleanup preserves execution/cleanup failures.

Every protected entrypoint must actually route through this boundary. Plain Core dispatch and code generation remain usable for public operations and do not automatically add authentication/tenant policy. The consumer's generated gateway deliberately delegates into the tenant dispatcher; bypassing it in trusted application wiring is not made safe by an attribute.

## Responsibility boundaries

The registered snapshot/selection callbacks, identity/membership/resource sources, policy, clock and handler factory are trusted application components. Snapshot callbacks must copy mutable state; the framework cannot deep-copy arbitrary generic object graphs or sandbox arbitrary C# handlers. Business/provider code must use checked scope rather than untrusted payload tenant fields. The operation lease checks in-process binding, activity and expiry; it does not supply atomic database authorization/read, distributed revocation or transaction isolation across awaits.

Expiry/revocation tests in this slice use fresh fixture sources and an injected clock. They are not proof of token/session/key lifecycle against an IdP. Real data filters/RLS, pooled connection reset, job/event envelopes, cache/retrieval access and issuer/token validation remain provider-specific acceptance work. Malformed/null/expired/misbound authority values deny before business work; provider infrastructure faults and caller cancellation remain distinct from successful authorization.

The separate Samples consumer uses generated Core gateway registration and a tenant-aware business handler. Pre-dispatch identity/membership/resource/policy denials may instantiate a stateless gateway needed to enter the boundary, but create no business handler and perform no business read/write. Expiry/cancellation observed after a factory has run instead cleans up the already owned handler; a handler-level denial is not a promise to undo earlier business effects. Cleanup faults must not be mapped into ordinary denial results. The fixtures have no real transport/provider or OIDC behavior.

## Protocol adapters and sources

Use established protocol implementations before emitting identity snapshots; do not add a JWT parser or signature algorithm here. An OIDC/JWT adapter must validate the intended issuer/audience, key/signature, token type and lifetime under its own qualified profile. OIDC issuer/subject comparisons are exact; an issuer path is part of the identity. The generic portable issuer field also permits non-OIDC service/fixture authorities and does not pretend to validate OIDC issuer syntax itself.

Primary references reviewed: [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html#IDToken), [issuer identity](https://openid.net/specs/openid-connect-core-1_0.html#IssuerIdentifier), [JWT BCP issuer/subject](https://www.rfc-editor.org/rfc/rfc8725.html#section-3.8), [audience validation](https://www.rfc-editor.org/rfc/rfc8725.html#section-3.9). The source facts justify adapter obligations; they do not establish that those adapters have been implemented or tested in this slice.
