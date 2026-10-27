# ADR-0005 — Portable Core/Composition development while platform qualification is blocked

Date: 2026-10-27. Status: Accepted for the user-authorized W1 experimental slice. Engine issues #5/#6; #3 remains Blocked.

The user authorized Core/Composition development that can proceed independently of the missing supported-Windows proof. Existing #5 → #3 and #6 → #5 dependencies remain recorded. They gate full acceptance/platform claims; they do not prevent designing, compiling or exercising the portable subset with the already pinned private SDK. This refines the earlier blanket pre-implementation gate without accepting an untested Windows platform or relaxing #3.

## Contracts

- `Cehpalon.Engine.Core` targets net11.0 and references only the base framework. Request/reply handlers receive typed request, immutable correlation metadata and cancellation. They return a valid success or explicit business error. Context metadata is not trusted tenant/identity authority; #7/#8 remain separate work.
- An ordinal immutable registry maps canonical operation IDs to exact request/response types and lazy factories. Lookup/type/cancellation guards precede factory execution. Each invocation owns the new handler returned by its factory and releases it on success/failure/cancellation; shared or pooled handler factories are outside this ownership contract.
- Expected dispatch failures are structured; caller cancellation and unexpected handler failures retain their exception semantics. Cleanup errors must not erase the original failure. No reflection scanning, host objects, provider objects or ambient global tenant state enter Core.
- `Cehpalon.Engine.Composition` is a separate BCL-only assembly. It compiles trusted startup appsettings JSON to a validated immutable plan before activation. No Core reference is needed to validate a generic module graph.
- Schema1 supports only `Modular` / `SingleProcess` / `RequestReply`. The `Cehpalon` section is strict; unrelated top-level host sections are permitted. Duplicate/ambiguous keys, unsupported profiles, unknown modules, invalid dependency graphs and explicitly disabled dependencies fail before callbacks. Support dependencies may be implicit; entrypoints require explicit selection.
- Activation preflights all required registrations, creates only enabled module resources in deterministic dependency order, and rolls back acquired resources in reverse order on failure/cancellation. The returned lease owns reverse-order idempotent cleanup. This is not rollback of arbitrary external business side effects.

API-only, API+GraphQL and Worker-only tests in this slice use module recorders. They verify graph/activation semantics and zero module-owned work when disabled; they do not implement or certify HTTP, GraphQL or Worker adapters. Provider/identity/tenant/remote/event/streaming contracts are not inferred from request/reply dispatch.

## Validation and readiness

Contract tests include malformed inputs, type/lookup boundaries, cancellation, immutable snapshots, concurrent calls, activation preflight/rollback/disposal and disabled-module counters. A real consumer compiles generated operation registrations and reuses one business handler through in-process callers. A predeclared [component benchmark protocol](../validation/w1-component-protocol.md) measures only the bounded paths.

Local Windows26H2 remains observational. WSL Ubuntu22.04.5 is the local listed-distribution tier. Hosted CI is unpassed until jobs actually execute; the existing account payments/spending-limit blocker is not a code failure. Umbrella features remain M0 while full scope/dependencies are outstanding. No public API stability, production readiness, NuGet publication or supported-Windows qualification is granted by this ADR.

The original acceptance checklists, estimates and unknown actual-hours values remain intact; refine them with scoped evidence rather than inventing completion or duplicate cards.

[Delivered slice, exact-source results and remaining gates](../planning/w1-core-composition-codegen.md).
