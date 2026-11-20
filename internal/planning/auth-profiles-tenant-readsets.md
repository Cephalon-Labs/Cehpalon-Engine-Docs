# Configurable authentication and tenant selection/read sets

Date: 2026-11-20. User-authorized #7/#8/#18 continuation. Engine main [e37689759f0987a1e381790ade0c031e52823ab1](https://github.com/Cephalon-Labs/Cehpalon-Engine/commit/e37689759f0987a1e381790ade0c031e52823ab1) includes tenant/read-set commit [39ee1c16fb292969f84d9640cc3b7ee8bb7195b8](https://github.com/Cephalon-Labs/Cehpalon-Engine/commit/39ee1c16fb292969f84d9640cc3b7ee8bb7195b8). [User refinement](../requirements/2026-11-20-auth-profiles-tenant-readsets.md), [ADR0034](../adr/ADR-0034-authentication-profiles-tenant-readsets.md), [predeclared protocol](../validation/auth-profiles-tenant-readsets.md).

## How consumers choose authentication

JWT is the claims-token format, JWS supplies signed representation, JWK/JWKS represents keys, and the algorithm selects the cryptographic operation. The separate optional Identity.JwtBearer module freezes a validated profile from typed settings or appsettings:

```json
{
  "Authentication": {
    "Api": {
      "Scheme": "ApiBearer",
      "Issuer": "https://identity.example/realm",
      "Audience": "orders-api",
      "Algorithm": "PS256",
      "TokenType": "at+jwt",
      "KeySource": "AuthorityMetadata",
      "Authority": "https://identity.example/realm"
    }
  }
}
```

Use `JwtAuthenticationProfile.FromConfiguration(section)` and call `AddCehpalonJwtBearer` only inside the selected security module. Unknown/nested fields, unsupported/unsigned algorithms and incompatible key-source arguments reject before key providers. Each scheme has one exact configured algorithm; multiple schemes can have separate trusted profiles. A token never chooses a new algorithm or trust endpoint.

| Key source | Host supplies | Validation boundary |
| --- | --- | --- |
| PublicJwks | Trusted public JWKS callback | At most 16 identified public RSA/EC verification keys, exact alg/use, canonical bounded material, unique kids; private/octet/remote-reference/unknown fields reject. |
| ProvidedKeys | Trusted key/secret-service callback | Bounded snapshots of RSA/EC or symmetric keys with exact family/strength and unique IDs. HMAC secrets stay outside public JSON/JWKS. |
| AuthorityMetadata | Configured HTTPS Authority/optional MetadataAddress | Established metadata retrieval/cache/refresh; exact configured token issuer/audience/type/algorithm still enforced. No token-provided jku/x5u lookup. |

Supported identifiers are RS256/384/512, PS256/384/512, ES256/384/512 and HS256/384/512. Actual representative signature tests cover RS256, PS256, ES256 and HS256; a supported identifier alone does not qualify a real issuer/provider. Local key selection requires kid, with no arbitrary-key fallback. RSA material needs at least 2048 actual bits and bounded exponent; EC curve/coordinate size must match. Audience trailing-slash equivalence is disabled, clock skew is zero, and SaveToken/IncludeErrorDetails are false. Key byte count cannot establish entropy/secrecy, and the host must separate key usage across schemes/algorithms. Local sets can contain controlled old/new verification keys; real rollover, metadata outage and revocation need provider-specific proof.

The strict JWT bridge enters existing identity/tenant dispatch. `AspNetCoreIdentitySource` with `IAuthenticatedTicketIdentityMapper` also supports established cookie/custom handlers, authenticating the exact configured scheme first. `TicketPropertyIdentityMapper` maps fixed issuer, unique subject and authenticated ticket validity. Mapped identity lifetime, scheme, cancellation and rollback are rechecked. Other protocols/algorithms remain extensible through established host handlers and IIdentitySource. This does not implement arbitrary JWS payload authentication, JWE, passwords, MFA, browser login, session/refresh-token lifecycle or production cookie policy. Cookie hosts own CSRF protection and secure persistent key/session management.

## One login, switching tenants

`RegisterTenantSelection` exposes a checked `tenant.select` observation: destination membership, resource owner and policy must pass afresh. A successful A→B response returns B's ID; it does not mutate a singleton/current-user tenant or mint a reusable tenant credential. The principal remains the same authenticated login.

The client includes the selected tenant in each subsequent request. Each request repeats authority checks; a later revocation denies B even after successful selection. A/B browser tabs or in-flight calls keep independent checked contexts. A request already admitted to A does not acquire B authority when the UI switches. Login alone is insufficient to enter B. The transport bridge uses a request-owned fixed accessor rather than mutating the ambient HttpContextAccessor holder in parallel resolvers.

## Reading all authorized tenants

`TenantReadSetDispatcher` accepts a separately registered `TenantReadSetOperation`, a fresh `ITenantReadSetSource` grant bound to principal/operation/resource kind/ID/version/validity, and an optional caller subset. Membership of A+B does not itself supply this aggregate grant. Null selection means every tenant in the grant, not every database tenant. An explicit subset must be nonempty, unique and contained; wildcard/admin metadata cannot expand it.

The implementation bounds a grant to 64 tenants and runs sequentially through normal tenant membership/resource/RBAC/ABAC checks. Identity source resolution is repeated per child and pinned to the original principal/scheme; host authentication services may cache the authenticated ticket within that request. Grant/identity/maximum lifetime bound the batch and child contexts. Queries and selectors are frozen before awaits. Trusted data ports must filter by the checked context; keys must include tenant where appropriate.

Rows are collected privately and returned only on complete success. A late B denial, cancellation or fault returns no partial A data, although an earlier authorized A read may have executed. Trusted registered read handlers must stay read-only; C# is not sandboxed. No write fanout, atomic cross-database snapshot or instantaneous distributed revocation is claimed. Over-limit sets reject instead of truncating; larger catalogs/paged reporting require a provider-specific bounded continuation capability.

Required audit adds a control-plane authorization/terminal pair before/after collection and parent-linked normal tenant events. Root records have no AuthorizedTenant and cannot appear in tenant-scoped history. Terminal audit observes processing; persistence and response delivery are not atomic. If expiry/cancellation occurs during the final required write, rows are still withheld even if a Succeeded processing observation was persisted. Sink faults retain possible-effects semantics and concurrent execution/cleanup failures.

## Tests and observed evidence

Pinned SDK 11.0.100-rc.3.26522.148, locked Release builds, zero warnings/errors, exact clean committed Engine and consumer sources.

| Checks | Windows | WSL Ubuntu |
| --- | ---: | ---: |
| Full component suites | 668 passed | 665 passed |
| AuthProfile, included above | 55 passed | 55 passed |
| TenantReadSet, included above | 37 passed | 37 passed |
| Actual generated HTTPS consumer | 50 passed | 50 passed |
| Tracking | 60 passed locally | Not rerun |

The component count difference remains the existing tooling platform corpus, 151 versus 148. Every final source digest and emitted consumer registry matches across hosts; registry SHA-256 is `b06b7682639d4b3888b37f52b15b545028f46ce34f556cae8c9e3eb8785edc06`. Compiler/codegen packages do not appear in consumer runtime libraries. Actual Web SDK item evaluation after archiving verifies that evidence is excluded from Compile/Content/None.

Tests include actual standard-handler RSA/PSS/ECDSA/HMAC validation and signature/issuer/audience/algorithm/key-ID negatives; strict public JWKS and provided-key snapshots; disabled providers; real encrypted ephemeral cookies; same-login selection/revocation; held parallel HTTP A/B and GraphQL sibling fields; distinct read-set grant/subset/all-eligible scopes; mid-batch principal/membership change, expiry/cancellation, no partial output, cleanup and required root/child audit failures. The ephemeral cookie fixture exposes no login route and writes no persistent key ring. No actual signing key/token/certificate is included in evidence.

Bounded read-only agent review caught and root regressions fixed three provider issues: diagnostic JWK ToString cloning, padded weak RSA material inflating KeySize, and default metadata issuer expansion. Review also identified the sample's ambient accessor mutation, now replaced and covered by parallel tests. [Review evidence](../evidence/auth-profiles-tenant-readsets/boundary-review.json) distinguishes source inspection from executed tests; no complete security certification is implied.

Exact Engine hosted CI also passed [portable contracts](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44707316128) and [SDK/driver smoke](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44707316237). These workflow scopes do not close #3 or all IdP/provider/platform acceptance. No billing/usage-blocked step was skipped or retried.

Consumer source is Samples `958a7c662997ab25ea5442fb6dcadfcb28110db2`; [complete retained evidence](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/13792cf28c545bd2df513cd3e070a239822de1f2/security-api/evidence/2026-11-20-auth-readsets) is pinned at delivery `13792cf28c545bd2df513cd3e070a239822de1f2`. Samples revisions are technical provenance, not issue commit journal entries.

Retain all initial compile attempts (missing extension namespace, nullable metadata assignment, abstract test fixture), intermediate passing runs and the agent consumer hybrid overlay. Initial auth-dev01 lacks a full source inventory; dev02/03 frozen copies match their recorded source digests, and dev04 froze executing source before its run. Development mixtures are not exact final evidence. A read-only sync dry run once reported an old Engine SHA unresolved; direct API verified the same SHA with quota available, and the unchanged reviewed plan then passed. Its original transport cause remains unknown, not mislabeled billing or a missing commit.

Engine and Samples feature branches are merged/deleted, with detached source/worktrees/raw retained. Four pre-existing Engine edits retain exact digests; unrelated Samples portable-core files are untouched. Keep #3 Blocked, #20 full row and every original metadata/dependency/M0/gate/unknown actual-hours value. No original benchmark workload, threshold or flag changed and no performance improvement is inferred.

Final independent readback verified all 23 Engine mirrors. Only #7/#8/#18 bodies and update/digest fields changed; the other 20 complete rows/numeric task bytes, all issue metadata and milestones remain unchanged. [Final tracking guard](../evidence/auth-profiles-tenant-readsets/final-tracking-guard.json). All three repositories remain public MIT and Project 4 private.
