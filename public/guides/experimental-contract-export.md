# Experimental offline Small API contracts

After generating/building a Small API consumer, explicitly export its selected transport contracts:

```text
dotnet PortableConsumer.MyApi.dll --export-contracts --config appsettings.json --output <new-directory>
```

The output parent must exist and the destination must be new. Existing files/directories and observed link/device/known program-checkout content destinations are rejected. Outputs are deterministic for the same compiled source/configuration. Source/build/output parents must be trusted; these path checks are not a filesystem sandbox.

| Configuration | Artifacts |
| --- | --- |
| API-only | manifest.json + openapi.json |
| API+GraphQL | manifest.json + openapi.json + schema.graphql |
| GraphQL-only | manifest.json + schema.graphql |
| All-off | manifest.json |

OpenAPI3.1 describes the three selected HTTP business operations using their real typed mappings and the adapter serializer's JSON shapes. Health and GraphQL HTTP envelopes are outside that document. GraphQL SDL comes from the same actual typed schema builder used by serving. Selected GraphQL explicitly builds/disposes offline schema services; disabled GraphQL does no schema/service work. Export creates no host/listener, reads no TLS/JWT files, invokes no business handlers and grants no tenant authority. It does not enable HTTP introspection/schema endpoints.

Schemas are structural. Custom validators, duplicate-key/Unicode/body-limit parsing, all numeric parser bounds and fresh identity/tenant policy remain separate. A structurally valid request can still fail validation or authorization. Nullable successful response roots are preserved; HTTP request bodies must remain objects.

The generated Small API now has14source files and retains32observed Engine source inputs. The default portable console profile remains9files/17inputs. See the [actual differential proof](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/tooling-contracts), [Small API guide](experimental-small-api-cli.md) and [decision](../../internal/adr/ADR-0014-small-api-contract-export.md) for tested versions and boundaries. Full #9/#20/platform/provider/production acceptance remains open and #3 remains Blocked.
