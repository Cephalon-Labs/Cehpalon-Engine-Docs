# Continuation scope: local authentication key-ring lifecycle

Date: 2026-11-20. User instruction: ต่อเลย ยาวๆไป. This continues the explicitly requested optional authentication/JWE/tenant/audit capability; it is not a new requirement for a particular external IdP or KMS.

Selected ready #8 work: online local signing/decryption key publication, overlap, retirement and withdrawal without host restart, with coherent immutable snapshots and explicit expiry/failure behavior. Reuse the existing algorithms, standard cryptography, Core/Composition/gateways and tenant/audit boundaries. #7/#18 receive regression evidence. No public key-management API, background credential discovery, new algorithm or production provider claim.

[ADR0036](../adr/ADR-0036-local-keyring-lifecycle.md) and [protocol](../validation/local-keyring-lifecycle.md) define actual semantics: fresh validation only, one version of both key roles, no expired/withdrawn fallback, and no retroactive cancellation of completed/cached authentication or admitted work. Keep #3 Blocked, #20 full row, all metadata/M0/dependencies/gates/unknown hours and original benchmark criteria unchanged.
