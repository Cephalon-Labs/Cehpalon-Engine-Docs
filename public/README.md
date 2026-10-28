# Developer documentation

This folder is reserved for developer-facing Markdown suitable for a future Astro documentation site.

Current status: experimental component guides are available; no stable runtime API, database provider, transport adapter or deployment target is certified by these documents.

The [protected HTTP/GraphQL guide](protected-http-graphql.md) describes the bounded experimental adapter and Small API integration, with explicit host authentication/tenant wiring and proof limits.

- [Experimental Core, Composition and operation code generation](guides/experimental-core-composition-codegen.md): tested bounded contracts and an executable in-process consumer, with explicit platform/profile/ownership limits.
- [Experimental tenant/identity boundary](guides/experimental-tenant-identity.md): fresh authority checks, checked context lifetime and cross-tenant fixture proof; no real IdP/provider qualification.

Publish guides with tested versions, supported profiles, runnable Samples and limitations when evidence exists. Keep research, internal planning, task mirrors, operational evidence and AI handoffs under internal folders.

- [Experimental public Small API measurements and limits](small-api-measurements.md)
