# Developer documentation

This folder is reserved for developer-facing Markdown suitable for a future Astro documentation site.

Current status: experimental component guides are available; no stable runtime API, database provider, transport adapter or deployment target is certified by these documents.

Current source builds and generated consumers select .NET SDK **11.0.100** and .NET/ASP.NET Core **11.0.0**, with prerelease selection disabled. See the [GA build and historical replay guide](guides/dotnet11-ga-builds.md). Dated RC results keep their original versions and do not certify GA performance or supported-host/provider coverage.

The [protected HTTP/GraphQL guide](protected-http-graphql.md) describes the bounded experimental adapter and Small API integration, with explicit host authentication/tenant wiring and proof limits.

- [Experimental Core, Composition and operation code generation](guides/experimental-core-composition-codegen.md): tested bounded contracts and an executable in-process consumer, with explicit platform/profile/ownership limits.
- [Experimental tenant/identity boundary](guides/experimental-tenant-identity.md): fresh authority checks, checked context lifetime and cross-tenant fixture proof; no real IdP/provider qualification.
- [Experimental portable CLI](guides/experimental-portable-cli.md): one source-checkout console scaffold using Core/Composition/codegen, with explicit filesystem, profile and distribution limits.
- [Experimental Small API CLI profile](guides/experimental-small-api-cli.md): generated protected HTTPS consumer, profile-specific validation, optional GraphQL and fresh tenant fixtures; real IdP/provider/production qualification remains separate.
- [Experimental offline contract export](guides/experimental-contract-export.md): serializer-derived OpenAPI and actual GraphQL SDL for selected Small API operations, with explicit structural/authority limits.
- [Experimental tooling measurements](guides/experimental-tooling-measurements.md): actual generator/emit and fresh CLI process observations with fixed raw retention and qualification limits.

Publish guides with tested versions, supported profiles, runnable Samples and limitations when evidence exists. Keep research, internal planning, task mirrors, operational evidence and AI handoffs under internal folders.

- [Experimental public Small API measurements and limits](small-api-measurements.md)

- [Experimental configurable audit history and trails](guides/experimental-audit-trails.md): project-selected metadata/diff/snapshot modes, field redaction, checked tenant history and optional awaited mutation/trail execution and provider transaction/outbox relay and protected count-only status with explicit provider/commit limits.
