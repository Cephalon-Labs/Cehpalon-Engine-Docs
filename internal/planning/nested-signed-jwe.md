# Optional nested signed JWE delivery

Date: 2026-11-20. User explicitly requested JWE. Engine main [7311f5bd02fb94cdf4e0711ce168a3eb646237fd](https://github.com/Cephalon-Labs/Cehpalon-Engine/commit/7311f5bd02fb94cdf4e0711ce168a3eb646237fd) integrates implementation [b8e52078710287d50e190042dd3a0304ba68e30c](https://github.com/Cephalon-Labs/Cehpalon-Engine/commit/b8e52078710287d50e190042dd3a0304ba68e30c). [Requirement](../requirements/2026-11-20-jwe.md), [ADR0035](../adr/ADR-0035-nested-signed-jwe.md), [protocol](../validation/nested-signed-jwe.md). Scope #8 with #7/#18 regression coverage; #3 remains Blocked.

## Consumer configuration and behavior

JWE is opt-in. The existing Signed default remains available; EncryptedSigned requires encrypted input containing a separately signed JWT, with no plaintext fallback:

```json
{
  "Authentication": {
    "Scheme": "Bearer",
    "Issuer": "https://issuer.example/realm",
    "Audience": "example-api",
    "Algorithm": "RS256",
    "TokenType": "at+jwt",
    "KeySource": "PublicJwks",
    "TokenProtection": "EncryptedSigned",
    "KeyManagementAlgorithm": "RSA-OAEP",
    "ContentEncryptionAlgorithm": "A256CBC-HS512"
  }
}
```

Freeze with `JwtAuthenticationProfile.FromConfiguration(section)`, then select the module and call `AddCehpalonJwtBearer(profile, publicJwks: trustedSigningKeys, decryptionKeys: trustedPrivateKeyProvider)`. Keys never belong in public appsettings. The source callbacks are explicit, independently validated and called only by selected registration. Invalid settings/provider combinations reject before callbacks; invalid key material necessarily requires loading its trusted source.

Delivered pairs in pinned IdentityModel8.19.2 are **RSA-OAEP + A256CBC-HS512** and **dir + A256CBC-HS512**. RSA-OAEP means the explicit OAEP/SHA-1 identifier, not RSA-OAEP-256. RSA decryption requires an identified exportable private key with at least 2048 actual bits; direct mode needs exactly 64 secret bytes. Up to 16 distinct decryption keys are snapshotted. Nonexportable/HSM keys and zeroization of every managed/private copy are not promised; applications own key-provider lifetime, access and production lifecycle.

The stock creation API rejects RSA-OAEP-256 and GCM creation in the observed paths. Its source contains GCM decryption support, so this is not a claim that GCM decryption is universally impossible. These unqualified choices reject in the helper instead of being silently mapped to another pair. No package/SDK upgrade or custom cryptographic provider was introduced to expand the list.

Outer typ must equal configured TokenType and cty must be JWT. Key management alg, content enc and key ID are independently enforced. Local decryption is exact-kid only; no token URL or public JWKS private-key discovery. Direct compact format requires an empty encrypted-key segment; wrapped RSA format requires a nonempty one. Duplicate/unknown/crit/zip/remote-reference fields reject. Wire tokens are bounded to 64 KiB and protected outer/inner headers to 4 KiB. A successful result explicitly contains one encrypted outer and one signed unencrypted inner.

The established implementation performs authenticated decryption and signature validation. The algorithm callback has separate roles for content encryption with its derived CEK and the inner signing algorithm/key; a shared permissive algorithm union is insufficient. Signing/decryption IDs and actual material must differ, including mathematically equivalent RSA integer encodings. Local reuse rejects at registration; metadata signing-key reuse rejects during signature validation. Converted/raw metadata RSA strength uses actual modulus bits, and raw EC checks the configured named curve.

Decrypted claims still pass exact issuer/audience/type/lifetime and the existing identity trust, fresh tenant membership/resource/RBAC/ABAC, switching and explicit read-set checks. Encryption grants no extra tenant access. Audit remains verified operation metadata; no raw token, ciphertext, decrypted claim bag/body or key is written to evidence or logs by this feature. Protocol authentication failures remain outside tenant operation audit, under host security logging. JWE does not replace HTTPS, IdP/session revocation or provider data isolation.

## Exact test results

Pinned SDK11.0.100-rc.3.26522.148, locked Release, zero warnings/errors, exact clean committed sources on both hosts:

| Check | Windows | WSL Ubuntu |
| --- | ---: | ---: |
| Complete component suites | 723 passed | 720 passed |
| JWE suite, included above | 55 passed | 55 passed |
| Actual generated HTTPS HTTP/GraphQL consumer | 90 passed | 90 passed |
| Tracking tests | 60 passed | Not rerun |

The existing tooling platform split remains 151 versus 148; no JWE cases were skipped to explain it. Final source hashes and actual emitted registry match across hosts; registry digest `b06b7682639d4b3888b37f52b15b545028f46ce34f556cae8c9e3eb8785edc06` is unchanged because business gateways are reused. No compiler/codegen runtime dependency leaked. Post-archive Web SDK evaluation excludes evidence from Compile/Content/None.

The actual consumer retains all previous 50 checks and adds 40 JWE checks. Both pairs pass real HTTPS HTTP/GraphQL authentication. Wrong decryption/signature key, unknown kid, plaintext downgrade, unapproved alg/enc, tampered ciphertext/tag/header, unsigned/raw/deeper-nested or misbound inner data and disabled providers are negative cases. Existing cross-tenant, tenant selection/read-set/audit checks run after decryption. Each JWE profile observed 6 business factories/6 disposals, 21 audit events, one signing callback and one decryption callback; the original fixture's 29/29 and 96 events are separately scoped. A late B denial still withholds earlier A response rows.

Read-only review and regressions fixed three representation/policy gaps: direct unused segment malleability in stock validation, padded-exponent aliases bypassing raw RSA separation comparison, and padded weak metadata RSA after standard JWK conversion inflating KeySize. [Review evidence](../evidence/nested-signed-jwe/boundary-review.json) distinguishes actual execution from source inspection. Outer duplicate-header execution uses a MAC-invalid token, so valid-MAC outer duplicate rejection is a reviewed source guard rather than separately executed proof. The inner duplicate is re-signed/re-encrypted. No practical forged-claims exploit, timing-oracle guarantee or exhaustive security certification is claimed.

Exact Engine CI passed [portable contracts](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44712792297) and [SDK/driver smoke](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44712792353). They do not close #3 or real IdP/KMS/HSM/rotation/provider acceptance. No billing/usage step was skipped or unchanged rejected job rerun.

Consumer source is Samples `a6377d21188621d93be80a00cf83350a13b4ee6c`; [public raw outputs, source freezes, manifests, prior attempts and CI observations](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/ea7f2fe05cbf0bb8220c07c694308e809fd858c3/security-api/evidence/2026-11-20-jwe) are pinned at delivery `ea7f2fe05cbf0bb8220c07c694308e809fd858c3`. Samples SHAs are technical provenance only. Engine issue journals contain the two full Engine SHAs.

Preserve preliminary unsupported crypto/compile probes, intermediate 48/51/54/55 contracts, development consumer89 overlay and unexecuted early draft separately from final qualification. Initial capability probes lack a complete snapshot of every earlier executing source revision; outputs and latest available source remain with this limitation. Later contract attempts and development consumer froze source before runs. Root checked public exports for actual compact tokens/private key material and staged digests; no binaries or private credentials were published.

Feature branches are merged/deleted and detached worktrees/raw retained. Four pre-existing Engine edits retain their digests; unrelated Samples portable-core files are untouched. All original workloads/thresholds/flags, #20 entire row, M0, dependencies, metadata/gates and unknown actual person-hours remain unchanged. No benchmark or performance improvement claim accompanies this security feature.

Final guarded apply and independent readback matched all 23 Engine mirrors. Only #7/#8/#18 bodies and update/digest fields changed; other 20 complete rows/numeric task bytes and all issue metadata/milestones remain unchanged. [Final tracking guard](../evidence/nested-signed-jwe/final-tracking-guard.json). All three repositories are public MIT and Project 4 remains private.
