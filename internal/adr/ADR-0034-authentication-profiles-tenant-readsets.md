# ADR-0034: Consumer authentication profiles and explicit tenant read sets

Date: 2026-11-20. Accepted for the user's requested bounded implementation. Tracking #7/#8/#18; #3 remains Blocked, #20 and all original benchmarks unchanged.

## Context and user decision

The user requested configurable authentication including algorithm/JWT/JWK/JWS and asked how a logged-in user switches A to B or reads every tenant. JWT (claims format), JWS (signed representation), JWK/JWKS (key material/set) and signing algorithm are separate settings. Authentication establishes a principal; it never grants an arbitrary tenant or cross-tenant bypass.

## Decision

Provide a separate optional JwtBearer integration module over the established handler. Immutable profiles declare one scheme, exact issuer/audience/token type and one signing algorithm per profile/key family. Validate before loading keys or registering the handler. Support locally supplied public JWKS, caller-supplied security keys from a trusted secret/key service, and HTTPS authority metadata. Keep key/metadata locations host-configured; never follow token jku/x5u or dynamically choose algorithms/issuer from unverified claims. Reject unsigned tokens, weak/mismatched keys, private/symmetric material in public JWKS, duplicate/ambiguous key IDs and incompatible options. Existing handlers implement cryptography and metadata refresh. Symmetric secrets belong to a host secret provider, never public appsettings/JWKS. Signed compact JWT is the delivered profile; arbitrary JWS payloads, JWE and new algorithms require separately selected implementations/evidence.

Also provide an explicit authenticated-ticket mapper bridge for established cookie/custom schemes. Mapping requires the exact successful authentication scheme and bounded live identity; the framework does not implement passwords, token issuance or a new protocol. Host handlers remain responsible for their authentication/session/key lifecycle. Built-in strict JWT mapping stays available.

Switching is request-local selection: authorize tenant.select against the destination tenant's fresh membership/resource/policy and return the selected ID; no process/global/current-user mutable tenant state or new universal credential. Every following data request repeats tenant authorization. Parallel A/B requests and separate browser tabs keep independent checked contexts. A valid login can be denied B. Earlier A work retains only its original bounded A context, not B authority.

Reading a tenant set uses a separate explicitly registered read operation and fresh trusted read-set grant. Bind grant to principal, operation, kind, resource, validity and version; freeze at most 64 exact unique authorized tenants. Null selection means all tenants in that grant, never all database tenants. Caller-selected subsets cannot add tenants. No wildcard tenant, admin-role shortcut or write fanout. Registered read handlers are trusted application code; C# cannot prove their absence of writes.

Resolve original identity afresh at each tenant invocation, pin the batch principal/scheme, and run normal tenant membership/resource/RBAC/ABAC checks per tenant. Keep the batch validity lease bounded by grant/identity/maximum lifetime with monotonic invalidity. Collect privately and publish only a complete successful result; any denial/cancellation/fault discards partial response data. Earlier authorized reads may have executed before a later denial; this is not an atomic cross-database snapshot or instant distributed revocation. Per-tenant backends must scope every query/cache key. Over-limit grants reject rather than truncate or silently promote scope; larger catalog pagination is provider-specific future work.

When audit is enabled, require a control-plane grant record before read handlers, terminal outcome after the batch, and parent-linked normal tenant records. Control-plane records have no AuthorizedTenant and never appear in tenant history. Sink faults remain required-persistence failures with explicit possible-effects semantics. No tokens, key material, payloads or unverified tenant assertions are logged.

## Alternatives and consequences

- Reissue a universal all-tenant token or use tenant='*': easy to wire but violates resource-bound tenant checks; rejected.
- Keep a singleton current tenant: simple UI state but races across tabs/requests; rejected.
- Let a token select algorithms/keys: flexible but introduces confusion and attacker-controlled key lookup; rejected.
- Shared read-only fanout over existing boundaries: reuses business/data authorization with bounded cost and explicit incomplete/partial-read semantics; selected. Large global reporting and snapshot consistency need a provider-specific reporting capability.

Validate actual signed RSA/PSS/ECDSA/HMAC profiles with strict key-family and signature negatives, safe JWKS parsing, malformed profiles, disabled key factories, actual authenticated cookie mapping where selected, A/B switching, parallel isolation, explicit read-set grants/subsets, principal change/revocation/expiry, no partial response, audit lineage and HTTP/GraphQL generated consumers. No performance claim without a separately declared benchmark.

Primary sources: [JWT BCP](https://www.rfc-editor.org/rfc/rfc8725.html), [JWK](https://www.rfc-editor.org/rfc/rfc7517.html), [JWS](https://www.rfc-editor.org/rfc/rfc7515.html), [JwtBearer configuration](https://learn.microsoft.com/en-us/aspnet/core/security/authentication/configure-jwt-bearer-authentication).
