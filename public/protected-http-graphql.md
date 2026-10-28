# Experimental protected HTTP and GraphQL

The supported experimental integration pattern is: validate Composition configuration, establish authentication with the protocol implementation, map explicit typed operation bindings, then bridge each call through fresh `TenantOperationDispatcher` checks. Core code generation registers stateless gateways; it does not authenticate or select tenants itself.

The HTTP project has no GraphQL dependency. Map typed POST operations only for enabled API entrypoints. Use the same `OperationBinding<TRequest,TResponse>` for explicitly named GraphQL query/mutation fields. Add GraphQL services and map its endpoint only when that module is enabled. The host is responsible for suppressing disabled registration, schema/executor creation and owned background work. A shared host dependency is different from an API entrypoint: GraphQL-only need not enable API.

Bindings contain a server-owned operation ID and a pure validator. Business request/response types stay free of HttpContext/vendor objects. GraphQL infers public DTO fields, so changing those fields changes the schema contract. Both transports require host-established authentication; never synthesize a trusted principal from caller headers. The dispatcher interface is an integration port, not an authorization mechanism.

The bounded JSON limit is16KiB. HTTP maps intentional error codes to statuses; GraphQL exposes semantic codes under `errors[].extensions.code` with normal GraphQL response semantics. Protocol parse/coercion/complexity errors may differ. Missing authority and cross-tenant denials remain generic. Business error messages are trusted disclosure contracts; unexpected exceptions are redacted. Cancellation reaches the business call but does not undo completed effects.

Opt-in GraphQL uses HotChocolate16.7.1, authenticated POST only, depth8/cost1000, no GET/schema download/introspection/IDE/WebSocket/batching/multipart/incremental execution. These constraints cover the explicit operation catalog, not arbitrary additional application schemas or middleware.

The [Small API consumer](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/small-api) demonstrates the exact pinned integration with ephemeral JWT/TLS fixtures and two tenant catalogs. It has API-only, API+GraphQL, GraphQL-only and all-off checks. Source/package files on disk do not imply activation. The protected fixture is separate from the original W0 public benchmark. Real IdP/provider lifecycle, full performance and supported-Windows acceptance remain outstanding; #3 stays Blocked and full features remain M0.

See [ADR0008](../internal/adr/ADR-0008-protected-http-graphql-adapters.md) and [current evidence](../internal/planning/w2-transports-small-api.md).
