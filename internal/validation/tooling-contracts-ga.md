# Generated transport contract validation on .NET 11 GA

Tracking #20 and ADR-0014. The active offline contract verifier had been
pinned to the RC3 SDK and an earlier Engine SHA. It now selects .NET SDK
11.0.100 and clean Engine `c18757f7ef4df2c78c73e902aa39d05424e6bcff` for this
scoped proof. Earlier reference and measurement artifacts remain available.

The existing verifier generated and built a real Small API consumer for each
host. Both runs passed all 160 contract export checks and all 25 differential
checks comparing generated OpenAPI/schema behavior with authenticated HTTPS
requests. The proof covers config-selected artifacts, deterministic output,
disabled transport paths, runtime serializer and schema boundaries, and the
generated consumer specified by ADR-0014. The test completed using the
existing verifier code and dependencies selected by the clean Engine revision.

The portable-console and Small API default locks keep their currently
checked-in CI reference. This delivery updates the offline verifier lock.
The broader #20 profile and benchmark acceptance and the original benchmark
criteria remain in force.

[ADR-0014](../adr/ADR-0014-small-api-contract-export.md) · [Samples verifier](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/tooling-contracts) · [Retained results](../evidence/tooling-contracts-ga/2026-11-23)

## Canonical LF export

Engine `6fe7254404cf6b148370bd95befe8331e8932354` selects LF for offline
OpenAPI and export manifest JSON. Published GraphQL SDL was already LF.
The change applies to files in export directories. Console output and
the generated source observation continue to report their existing values.

Both clean hosts repeated all 160 export and 25 HTTPS/runtime checks.
The four profiles published eight artifacts in total. Every published file
matched byte for byte across Windows and WSL. The same files also matched
the earlier WSL output at `c18757f`. The replay rechecked manifest byte
counts and digests and confirmed the generated registry hash matched.
The generated `engine-source.json` records local checkout paths, which
differ between hosts by design.

[Engine change](https://github.com/Cephalon-Labs/Cehpalon-Engine/commit/6fe7254404cf6b148370bd95befe8331e8932354) · [Cross-host replay](../evidence/tooling-contracts-ga/2026-11-23/lf-cross-host.json)
