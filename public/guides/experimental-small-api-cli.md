# Experimental Small API CLI profile

The source-checkout CLI can generate a fixture-backed protected HTTPS Small API using existing Core, Composition, generated typed gateways, tenant dispatch and HTTP/GraphQL adapters. It is an experimental local development profile with synthetic memberships and in-memory data. Real IdP/provider integration and production qualification remain separate.

```text
dotnet cehpalon.dll new --profile small-api --name MyApi --output <new-directory> --engine-root <Engine-checkout>
dotnet cehpalon.dll validate --profile small-api --config <generated-directory>/appsettings.json
```

The CLI writes fourteen fixed files, including the [offline contract exporter](experimental-contract-export.md), performs no restore/build/install/network operation and preserves the no-overwrite/path safeguards of the [portable CLI](experimental-portable-cli.md). Its selected32source-input hashes are observations of an editable checkout, not immutable attestations. Use trusted source/output parents and inherited SDK/MSBuild policy. The default profile remains `portable-request-reply` when `--profile` is omitted.

The emitted Web project has API-only configuration by default. `appsettings.graphql.json` enables API+GraphQL, `appsettings.graphql-only.json` enables only GraphQL and `appsettings.off.json` disables all entrypoints. Configuration compiles before activation. Unsupported Worker/database/cache/broker/AI/retrieval selections reject before host work. Disabled GraphQL skips vendor service registration and endpoint mapping; its packages may still exist on disk. All-off creates no host/store/listener and reads no credential files.

Build `Consumer.csproj` deliberately with the pinned SDK. The generated README provides two explicit modes:

```text
dotnet PortableConsumer.MyApi.dll --self-test --output <new-result.json>
dotnet PortableConsumer.MyApi.dll --serve --config appsettings.json --certificate <server.pfx> --public-key <RSA-public.pem> --ready <new-ready.json>
```

Self-test creates temporary localhost TLS/JWT fixtures and sends real HTTPS requests. Serve requires your certificate/private key in PFX and an RSA public PEM, with PFX password supplied through `CEHPALON_TLS_PASSWORD`. It binds loopback on an assigned port and publishes a new readiness file without credentials. It does not implicitly generate a serving identity or issue client tokens. Type `stop` then Enter, or use Ctrl+C, to await owned cleanup. All-off skips credential access; failed readiness publication cleans up an already-started host and reports its actual counters.

JWT must match the documented fixture issuer/audience, RS256 signature, access-token type, lifetime and unambiguous claims. The fresh membership fixture grants Alice only tenant-a and Bob only tenant-b; identical resource IDs are isolated. Request headers and tenant DTO fields never grant authority. Replace these fixture authority/data implementations with properly qualified sources before using protected business data; do not loosen signature validation to make a demo request work.

See the [generated consumer proof](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/tooling-small-api) for exact source lock, commands, tenant/disabled-module cases and evidence. This profile does not establish full transport-schema generation, tooling performance, packaging/global-tool installation, AOT/trimming or production readiness. #3 remains Blocked and umbrella maturity remains M0.
