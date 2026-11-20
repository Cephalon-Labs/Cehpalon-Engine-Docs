# ADR-0035: Optional nested signed JWE authentication

Date: 2026-11-20. Accepted bounded extension of #8 with #7/#18 regression coverage. User request: รองรับ jwe ด้วยนะครับ. #3 remains Blocked; #20, maturity, dependencies and original benchmark gates stay unchanged.

## Context

ADR0034 delivered configurable signed JWT profiles and explicitly deferred JWE. The user now authorizes encrypted tokens. Encryption supplies confidentiality/integrity for the recipient but does not replace authenticated issuer/signature, audience, lifetime or tenant authority. The pinned IdentityModel8.19.2 API has distinct signing, key-management and content-encryption controls; an algorithm identifier appearing in a constant does not prove creation/decryption support on the actual platform.

## Decision

Add explicit Signed (existing default) and EncryptedSigned token-protection profiles. Configure inner signing Algorithm separately from outer KeyManagementAlgorithm and ContentEncryptionAlgorithm. A selected encrypted profile requires a compact JWE containing a signed JWT and rejects plaintext signed-token downgrade; a signed profile rejects encrypted input. The established IdentityModel implementation performs all cryptography. No custom cipher, signature primitive, alternate package upgrade or silent algorithm substitution.

Initial conformance targets the actually supported authenticated AES-CBC-HMAC content suite A256CBC-HS512 with explicit dir or RSA-OAEP key management, after positive actual SDK probes. dir needs its full 512-bit content key. Unsupported GCM/OAEP256 choices reject rather than being rewritten to another algorithm. Probes and their creation-versus-validation limitations remain separate from conformance claims. RSA1_5 and unauthenticated/unknown algorithms are not selected. Additional pairs require their own source/runtime evidence.

The outer untrusted header is parsed with established bounded library/BCL facilities only to enforce the configured profile and select an already configured key ID. Fix exact alg/enc/type/content-type, bounded compact/header sizes and permitted nesting; reject ambiguity, compression/critical extensions and token-provided key endpoints. ValidAlgorithms alone is not a key-management allowlist: pinned source calls algorithm validation for the content enc/derived symmetric key and for the inner JWS signature. Enforce these roles separately, as well as the explicit outer key-management gate. Require and validate the inner JWS, exact issuer/audience/type/lifetime and configured signing key independently before exposing claims to IIdentitySource.

Use a distinct trusted decryption-key callback; decryption secrets/private keys never come from public JWKS or unverified token URLs. Freeze/validate supported key representation, key IDs, family, size and intended operation before handler activation. Enforce signing/encryption key separation in the supported profile, with explicit limitations for external providers. The host owns secret provider/key lifetime and real rotation/revocation. Disabled or structurally invalid profiles perform no module-owned key-provider work; invalid material cannot be detected before its trusted source is loaded.

Successful decryption/inner authentication still enters the same fresh tenant membership/resource/RBAC/ABAC boundary. Switch/read-set grants and audit semantics remain unchanged. Audit contains only operation metadata; neither ciphertext, plaintext claims/body, keys nor tokens are logged. Public authentication failures remain generic; no timing-oracle or universal security guarantee is inferred from response tests.

## Alternatives and consequences

- Allow encrypted unsigned claims as identity: does not authenticate an issuer that holds a separate signing key, so rejected for this profile.
- Accept plaintext when an encrypted profile is selected: creates downgrade/confusion risk, so rejected.
- Upgrade dependencies or implement new crypto solely to expand an identifier list: broadens the pinned program and proof surface, so deferred.
- Explicit nested signed encryption over existing handlers: chosen. Adds decrypt cost and key lifecycle responsibility, with no unmeasured performance claim. Real IdP/encrypted token interoperability, HSM/KMS, metadata outages and production deployment need separate qualification.

## Validation and sources

[Predeclared conformance protocol](../validation/nested-signed-jwe.md). Validate stock-library positive decrypt+inner authentication on Windows and WSL and actual generated HTTPS HTTP/GraphQL consumers; include downgrade, wrong/tampered algorithm/content/key/cipher/tag, unsigned/bad inner claims, header bounds/ambiguity, key separation, cancellation, disabled factories, cross-tenant/switch/read-set and audit redaction cases.

Primary sources: [JWE](https://www.rfc-editor.org/rfc/rfc7516.html), [nested JWT requirements](https://www.rfc-editor.org/rfc/rfc8725.html#section-3.3), [pinned IdentityModel8.19.2 source](https://github.com/AzureAD/azure-activedirectory-identitymodel-extensions-for-dotnet/tree/8.19.2). Source selection is not runtime qualification.

Pinned capability note: [AuthenticatedEncryptionProvider](https://github.com/AzureAD/azure-activedirectory-identitymodel-extensions-for-dotnet/blob/8.19.2/src/Microsoft.IdentityModel.Tokens/Encryption/AuthenticatedEncryptionProvider.cs) has a GCM decryption path while its GCM encryption method throws NotSupportedException. The selected scope therefore does not claim that GCM decryption is universally unavailable; it does not offer unproven GCM round-trip conformance through this helper. Initial independent probes run on a .NET10 diagnostic host are source/capability corroboration, not replacement for the pinned SDK11 final runs.
