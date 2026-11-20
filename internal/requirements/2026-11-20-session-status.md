# Optional session-status continuation

User instruction: continue substantial engine work after opt-in authentication/JWE/key-ring delivery. Existing user scope includes configurable authentication, tenant switching/read sets and audit/history. Root selected the next bounded #8 session-lifecycle slice, with #7/#18 regression proofs; the user did not prescribe a new OAuth endpoint or session provider.

Consumers may explicitly decorate a trusted identity source with a fresh host-supplied session-status port. Session IDs come from successful configured authentication/ticket mapping, bind exact issuer/subject/scheme, and are unique per login/generation. Missing/inactive/misbound/expired status denies; faults/cancellation remain faults/cancellation. Cached authentication tickets must not skip fresh protected-operation checks. Preserve tenant boundaries/read-set identity coherence and required audit without raw session identifiers.

Local contract and actual generated HTTPS samples only. No new token issuer/password/logout endpoint, blacklist/store, real IdP/OAuth introspection adapter, distributed revocation/transaction or benchmark qualification. #3 remains Blocked; #20 and original gates/metadata/M0/unknown actual hours stay unchanged.
