# Optional authentication, RBAC/ABAC and audit/history delivery

Date: 2026-11-20. User-authorized continuation of #7/#8/#18. Engine [fb7eab63466b4c27f89d32ca33b1a54b789b1c96](https://github.com/Cephalon-Labs/Cehpalon-Engine/commit/fb7eab63466b4c27f89d32ca33b1a54b789b1c96) is merged/pushed to main. [Requirements](../requirements/2026-11-20-optional-access-audit.md), [ADR0033](../adr/ADR-0033-optional-access-and-audit.md), [predeclared validation](../validation/optional-access-audit.md).

Consumers can now select a host JWT authentication bridge, RBAC-only, ABAC-only or combined policy, required operation audit persistence and tenant-scoped history. Plain public Core profiles remain available. The implementation reuses Core, Composition, generated typed gateways and the existing tenant dispatcher; selecting a protected endpoint while explicitly disabling security rejects before host/module factories.

## Delivered contracts and behavior

| Component | Consumer selection and trust boundary |
| --- | --- |
| Identity.AspNetCore | Optional `AspNetCoreJwtIdentitySource`: calls `AuthenticateAsync` for one explicit scheme, requires a successful matching ticket with one authenticated identity and unique valid iss/sub/nbf/exp claims. It ignores an arbitrary pre-set User flag. The established JWT handler owns signature, issuer/audience, algorithm/type, key and lifetime validation. |
| Authorization | Optional `RoleAttributeAccessPolicy`: exact operation/action/kind rule, any listed role AND every configured subject/resource/environment predicate. RBAC-only and ABAC-only are supported. No unconstrained rule, missing-attribute grant, wildcard admin bypass or policy decision cache. |
| Authority facts | Fresh configured source binds principal, tenant, membership version, resource kind/ID/version and validity. Policy validity caps the checked operation lease. Expiry or UTC rollback during required audit denies before business creation; subsequent lease invalidity remains latched. |
| Required audit | Optional `TenantAuditServices` on tenant dispatch. Await authorization record before business factories and terminal result after owned cleanup. Early denied/faulted attempts have no authorized tenant stamp. Independent bounded write token permits terminal recording after caller cancellation. |
| History | Optional consumer source behind `TenantAuditHistoryReader`. Requires checked audit-history/tenant/read scope, validates tenant-only pages capped at 200 and rechecks the lease after await. |

Rules and attributes are defensively copied, bounded and ordinal. Registered sources, policy, request freezing callbacks and stores are trusted application components; arbitrary request roles/attributes/tenant ownership never become authority. This is an in-process boundary, not a sandbox or atomic authorization/data transaction. Real data ports must use the checked context and implement their own transaction/revocation semantics.

Audit contains invocation ID, stage, observation time, fixed outcome and verified operation/principal/tenant/resource identifiers. It contains no raw token/claim bag, request/response body or exception message. Those identifiers can still be sensitive; applications own minimization, retention, protected query, encryption, archival and deletion. This is operation/outcome history, including mutations, rather than automatically captured before/after field values.

Pre-business persistence failure prevents execution. Terminal persistence failure surfaces `TenantAuditWriteException.OperationMayHaveExecuted`; it does not imply rollback or authorize automatic mutation retries. If business/cleanup and persistence both fail, both causes survive. Abrupt process loss may leave an authorization record without a terminal record. The sink must honor cancellation and provide the chosen durability/idempotency. No fire-and-forget, best-effort downgrade, automatic retry, transactional outbox, exactly-once or tamper-proof storage claim is made.

Unknown-operation/contract rejection and HTTP authentication middleware 401s occur outside this tenant invocation boundary; hosts configure separate authentication/access security logging. Cookie/OIDC browser login, account/password/MFA, session/refresh-token lifecycle and key rotation remain responsibilities of established host/IdP components. Other identity protocols remain pluggable through IIdentitySource.

## Actual validation

Pinned SDK is 11.0.100-rc.3.26522.148. Final builds restore locked dependencies and compile Release with zero warnings/errors from exact clean committed Engine source. No new external runtime package is added to the portable policy/audit modules; the host bridge uses Microsoft.AspNetCore.App. Existing pinned JwtBearer/Hot Chocolate packages serve the consumer proof.

| Check | Windows local observation | WSL Ubuntu execution |
| --- | ---: | ---: |
| Complete component suites | 576 passed, 0 failed | 573 passed, 0 failed |
| New access/audit suite, included above | 55 passed | 55 passed |
| Actual generated HTTPS/JWT consumer | 27 passed, 0 failed | 27 passed, 0 failed |
| Existing tracking tests | 60 passed on Windows | Not rerun for this Docs-only workflow |

The three-check component count difference is the existing platform-specific tooling corpus (151 Windows / 148 WSL), not a skipped access test. Source hashes match between hosts, and both actual consumer generated registries have SHA-256 `79a5a0ce4218c5d385d9da6de0f6a8cdd1a9cb40abf261e75621af51bb43744d`. No Roslyn/code-generation dependency appears in consumer runtime libraries.

Component negatives cover wrong principal/tenant/membership-version/resource-version, missing/expired/future facts, ordinal roles/attributes, fresh revocation, rule/attribute configuration mutation, provider fault/cancellation, policy expiry during audit, UTC rollback, required sink failure/timeout, terminal failure after cleanup, simultaneous operation/audit faults, cleanup denial mapped as infrastructure fault, independent cancellation tokens, foreign/unverified/oversized history pages and revoked retained contexts. Authentication mapping tests reject ambiguous schemes/identities/claims, malformed dates/subjects, oversized claim sets and spoofed flags while preserving infrastructure/cancellation semantics.

The actual consumer uses ephemeral test CA/TLS and real RS256 JwtBearer validation, two tenants sharing a resource ID, the same generated gateways under HTTP/GraphQL, separate and combined policies, fresh fixture revocation, tenant-isolated mutations, auditor-only history, pagination, required audit outage, and independently disabled audit/GraphQL/security/public profiles. No signing key/token/certificate is persisted. The memory authority and bounded 1,024-event history store are fixtures, not external IdP or durable database proof.

Hosted CI for this exact Engine SHA also completed successfully: [portable component/adapter contracts](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44701271301) and [platform SDK/driver smoke](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44701271294). These are their stated workflow proofs; they do not close #3 or full provider/production acceptance. No GitHub billing/usage step was skipped or rerun after rejection.

## Provenance, retained failures and limits

Consumer source is pinned at Samples `9be24a794c119906079a0445005ecafd530a355e`; complete public [raw outputs, manifests, generated registries, prior attempts and CI observations](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/59c76719e9c3b562d062ad02491f9e0641574cbf/security-api/evidence/2026-11-20) are pinned at delivery `59c76719e9c3b562d062ad02491f9e0641574cbf`. These Samples SHAs are technical provenance only; Engine issue commit journals contain Engine SHA only.

Retain the initial 50/51 component result from an invalid future-facts fixture (equal start/end), the earlier 572-check Windows run, the first WSL launch that could not interpret a Windows linked-worktree gitdir, the consumer compile failure from ambiguous Host and interface target-typed construction, and the 26-check consumer run before pagination was added. The corrected final source is tested completely; no failing result is overwritten. WSL uses a retained clean clone of the same Engine commit with a real .git directory. Initial standalone component output lacks a complete executing-source snapshot, a stated provenance limitation. A packaging guard caught Git text normalization before publication; scoped -text attributes and staged SHA checks preserve raw bytes. No functional test was rerun for packaging.

Both feature branches are merged/deleted; detached Engine worktree/clone and all .local attempts remain for audit. Four pre-existing Engine edits retain their original digests and are excluded from this delivery; unrelated Samples files are untouched. Original benchmarks, flags, thresholds, #20 qualification and the historical five-drop/GC/scheduler investigation are unchanged. This slice makes no measured performance-improvement claim. #3 stays Blocked, all umbrella features remain M0, original dependencies/gates and actual-hours nulls remain intact.

Final guarded sync and independent readback matched all 23 Engine mirrors. Only #7/#8/#18 bodies and update/digest fields changed; the other 20 complete rows/task files, all milestone data and issue metadata are unchanged. [Tracking guard](../evidence/optional-access-audit/final-tracking-guard.json).
