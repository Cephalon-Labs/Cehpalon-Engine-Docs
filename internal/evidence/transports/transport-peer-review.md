# W2 transport peer review

Scope: read-only review of the in-progress HTTP/GraphQL adapters and protected Small API fixture for Engine #9/#11. No remote writes, source modifications, commits, benchmark measurements, or maturity promotion were made by this reviewer.

## Verified observations

- Shared project skill, current handoff, ADR0007, tasks9/11 and original W0 Small API protocol read.
- Live #3 remains OPEN with the supported-Windows blocker. Runs40529181479/40529181491 at Engine90d136dea3a76545e2994f64e2b3f6e096d83285 are completed/failure. Jobs122276951583/122276952169 in40529181479 each have zero steps; exact annotations report payments/spending rejection. No rerun performed.
- Independently executed the HTTP agent's compiled DLL:41/41 passed on local Windows. This is observational Windows proof, not the supported-Windows gate. Raw report: `http-peer.json` alongside this report. Test DLL SHA256:0DBD1F193A82C122678747D9FA953554122ED17C7ED949E16DF183B78781BFC7. Adapter DLL SHA256:F593ADD52BC43E6E58122FB88EDF572D1610DE7B974EF2684738E6DFEB19CE38.

## Findings sent to owners and inspected after correction

1. HTTP malformed escaped UTF16 / raw invalid UTF8: JsonDocument.Parse accepts inputs whose decoded string/property access throws InvalidOperationException. Initial outer catch produced500. Independent .NET11 repro confirmed three escaped-surrogate cases and two invalidUTF8 cases. HTTP now catches only structural decode invalidity and returns400validation.failed; trusted validator/dispatcher faults remain safe500. Regression cases passed in the independent41-check execution.
2. GraphQL initially passed arbitrary GraphQLException from host dispatcher/validator through to clients. Current resolver creates public adapter errors after the infrastructure try/catch; unexpected vendor exceptions now sanitize to internal.error. Agent added a private-message GraphQLException regression case. Final network suite execution remains integrator/owner evidence.
3. GraphQL initially lacked the HTTP adapter's post-dispatch cancellation check and only forwarded HttpContext.RequestAborted. Current resolver links HTTP and HC resolver cancellation and checks before/after awaited dispatch.
4. GraphQL envelope structural walk initially did not decode string values or normalize escaped-surrogate InvalidOperationException. Current walk decodes values/names, rejects ambiguous duplicate fields, and narrows parser catches. Final network tests remain integrator/owner evidence.
5. Small API initially checked subject length only. Signed whitespace/control subjects could reach PrincipalId validation as infrastructure failures. Current ExactClaims constructs representation-only PrincipalId/IdentitySnapshot within a safe argument-validation guard; authentication still comes from the established JWT validator, never that constructor.

## Functional matrix needed in integrated proof

- Actual HTTP POSTs for API-only and API+GraphQL, using the same typed operation bindings, generated Core gateways, fresh tenant dispatcher and business handler source.
- Anonymous/bad signature/issuer/audience/type/lifetime/duplicate or malformed subject rejection before business activation.
- Both cross-tenant directions, same resource ID in A/B, metadata spoofing, revoked membership, wrong resource owner and missing policy; denial must produce zero business factories/read/write. Stateless gateway/authority lookup counters are distinct.
- Validation, not-found, conflict, update and ordered pagination parity; normalize semantic error code while preserving declared REST versus GraphQL wire differences.
- Request abort observed in delayed business operation; no delayed mutation after cancellation. Time-based W0 thresholds require separately collected timing evidence.
- Strict JSON,16KiB+1 with declared and streamed bodies, GraphQL schema/IDE/GET/batch/incremental rejection and cost/depth enforcement.
- Invalid/all-off composition before host creation; API-only no GraphQL registration/services/schema/executor and forbidden module factory traps untouched throughout startup/requests/shutdown.404 alone is insufficient.
- Shutdown closes owned listener and balances business lifetime disposal.

## Proof boundaries

The protected two-tenant fixture intentionally differs from W0's public10,000-record lane: it has two10,000-record tenant catalogs and pinned local JWT authentication. Do not call it an unchanged W0 workload. Current startup timers/managed-process observations are diagnostics unless measured under the predeclared full protocol. Full1000-case corpus,100 timed cancellations/profile,30 restarts, dedicated baseline/Engine pairs, startup/RSS protocol, real IdP/provider lifecycle and supported-Windows remain unproved unless separately executed and recorded.

The initial Small API GraphQL counter counted the registration branch, not independent executor/schema construction. Report branch/DI absence as the actual evidence or add explicit lifecycle instrumentation. Source/package presence in output does not imply activation.

No remaining concrete HTTP source finding after correction. GraphQL and Small API final integrated execution remain to be read from the integrator's exact-source proof, and this review does not replace it.

## Final source reread

Latest Small API now includes the GraphQL-only/API-disabled profile and corrected catalog Builder API. Fixed issuer/audience/type/algorithm/lifetime validation, generated gateway to fresh tenant dispatch, per-tenant compound keys, guarded catalog actions, preactivation all-off/invalid handling and owned listener disposal have no remaining concrete finding in this scoped review. Integrator reports37/37 network checks on an earlier integration build; that count is integrator evidence, not independently rerun here. Latest source must receive final exact-source execution after the additional profile/claims edits.

Two bounded test additions were recommended to the integrator: signed whitespace/control subject401 regressions and an untrusted-CA rejection alongside the existing wrong-host rejection. Adapter owner was asked to distinguish configured depth8 from an exercised depth-limit regression if their flat test schema cannot reach depth9. These are coverage recommendations, not claims of an exploitable current defect.
