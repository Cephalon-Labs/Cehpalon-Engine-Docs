# ADR-0036: Optional local JWT/JWE key-ring lifecycle

Date: 2026-11-20. Accepted bounded continuation of the user's authentication/JWE work and latest instruction to continue. Tracking #8, tenant/audit regressions #7/#18. #3 stays Blocked and #20/original benchmark gates remain intact.

## Context

Static profiles freeze key callbacks at registration. They can include an old/new overlap set, but changing that set requires rebuilding the host. The next useful independent #8 slice is explicit local publication and withdrawal of signing/decryption keys, with coherent validation and precise limits rather than a blanket real IdP/KMS lifecycle claim.

## Decision

Add an explicit RotatingKeyRing key source and distinct selected registration. Static providers/metadata and a local ring cannot be mixed. A trusted host factory supplies one ring at activation; it starts empty and denies until an explicit valid publication. No background refresh, token-driven key URL, network retry, management endpoint or new cryptographic algorithm/dependency.

A publication validates/copies the complete signing and decryption sets together against the frozen profile before an atomic compare-and-swap update. Reuse existing key-count/family/strength/ID/material-separation rules. Publisher supplies expected current version, UTC validity and both sets; an internally assigned monotonically increasing version prevents stale concurrent publishers/ABA. Invalid candidates do not replace the current valid set. Withdrawal clears it and advances version; disposal permanently closes it. Old/new overlap is an explicit complete set, then retirement removes the old key. Key values/private data are not exposed by ring metadata.

Reject future/expired/malformed validity and overlong publication windows. Bound snapshot lifetime by UTC expiry and monotonic elapsed time from successful publication; clock rollback/negative elapsed/clock faults must not revive the same snapshot. Invalidity latches until an explicit new publication. Default maximum snapshot lifetime is five minutes, configurable up to one hour. A failed refresh/invalid candidate may leave a still-valid current set active until its declared expiry; withdrawal is the explicit immediate local control. No expired/withdrawn last-known-good fallback.

Each token validation captures one immutable snapshot for both key roles. Clone validation parameters for that invocation and replace all ring-dependent resolvers/validators; do not mutate shared options or accidentally capture again through virtual overload dispatch. Disable metadata/static-key/LKG fallback for this mode. Standard parser/crypto and exact signed/JWE profile rules remain. Before successful token-handler completion, verify that the same snapshot/version is still current and valid; an intervening publication/withdrawal/expiry denies that validation. Final-gate ordering is the decision linearization point, not atomic response delivery.

Standard validated results can expose mutable key/validation-parameter objects. Use request-owned copies for both roles and a fresh non-caching cryptographic factory for this mode, so neither the active ring nor a shared provider cache can be changed through a prior result. SignatureValidator override delegates that bypass the pinned key selection are incompatible and fail closed. Existing static profiles retain their original behavior. This local isolation adds unmeasured work; it is not a performance optimization or a C# sandbox.

This does not revoke already completed/cached authentication, a host OnTokenValidated callback after token-handler completion, an issued cookie/session or already admitted business operations. ASP.NET may cache AuthenticateAsync within one request. Every later request/tenant entry still follows its configured identity and tenant boundary, but distributed/session revocation and provider transactions need separate mechanisms. Private copies may remain referenced by in-flight results/crypto caches; no all-copy zeroization or HSM/nonexportable-key claim.

## Trade-offs and alternatives

- Restart with a static key set: smallest state surface, remains the default; insufficient for explicit online local withdrawal.
- Resolve signing/decryption keys independently per callback: simpler provider wiring but can mix versions across a nested token; rejected.
- Automatically keep old snapshots on failure: availability benefit but can prolong withdrawn/expired authority; rejected after expiry/withdrawal.
- Atomic validated local snapshots: chosen. Adds bounded synchronization/copy work and fail-closed retries when updates intersect validation. No performance improvement is claimed without measurement.

## Validation and sources

[Protocol](../validation/local-keyring-lifecycle.md): actual signed/JWE old/new overlap and retirement, invalid publication atomicity, expected-version races, expiry/rollback/fault/disposal, per-validation coherence and held validation withdrawal, no fallback/mixed source, input mutation/separation, disabled factory and fresh tenant/audit regressions. Full components and actual generated HTTPS HTTP/GraphQL on exact committed Windows/WSL source; keep all attempts and raw output. No credentials/token material in public evidence.

Primary references: [TokenValidationParameters](https://learn.microsoft.com/en-us/dotnet/api/microsoft.identitymodel.tokens.tokenvalidationparameters), [pinned copy constructor](https://github.com/AzureAD/azure-activedirectory-identitymodel-extensions-for-dotnet/blob/8.19.2/src/Microsoft.IdentityModel.Tokens/TokenValidationParameters.cs), [JWT key/algorithm requirements](https://www.rfc-editor.org/rfc/rfc8725.html). Clone copies references/delegates; request-local replacement is part of the implementation contract, not proof that every arbitrary custom provider is immutable.
