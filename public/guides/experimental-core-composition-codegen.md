# Experimental Core, Composition and code generation

Status: experimental W1 component slice; not a stable NuGet API or production/transport/provider qualification. Use the exact Engine revision and SDK recorded in the current evidence. No package has been published.

The Engine keeps business handlers independent of web/provider SDKs. A handler implements `IOperationHandler<TRequest,TResponse>` and returns `OperationResult<TResponse>`. Mark it with `[Operation("calculator.add")]` to request build-time typed registration. Roslyn produces lazy factory registrations; it does not create handlers, enable modules or implement business logic.

```xml
<ProjectReference Include="PATH/TO/Cehpalon.Engine.Core.csproj" />
<ProjectReference Include="PATH/TO/Cehpalon.Engine.Composition.csproj" />
<ProjectReference Include="PATH/TO/Cehpalon.Engine.CodeGeneration.csproj"
                  OutputItemType="Analyzer" ReferenceOutputAssembly="false" />
```

After providing an `IOperationHandlerFactory` that returns a **new owned handler per call**, registration is one generated call in the consuming assembly:

```csharp
var builder = new OperationRegistryBuilder();
Cehpalon.Engine.Generated.OperationRegistrations.RegisterAll(builder, factory);
var dispatcher = new OperationDispatcher(builder.Build());
var response = await dispatcher.DispatchAsync<AddNumbers, Sum>(
    "calculator.add", new(20, 22), new OperationContext("request-correlation"), token);
```

Factories are lazy. The dispatcher checks ID, cancellation, lookup and exact contract types before creating a handler, then owns its disposal. Business failure is an explicit result; cancellation and unexpected exceptions retain exception semantics. Correlation metadata is not identity/tenant authority. Do not return shared/pooled/DI-scope-owned instances under this ownership contract.

Compose pure `ModuleDescriptor` metadata separately. Compile trusted plain startup JSON with `CompositionCompiler.Compile(json, catalog)` and require a successful immutable plan before passing module factories to `PlanActivator.ActivateAsync`. Schema1 accepts only `Modular` / `SingleProcess` / `RequestReply`. Other topology/event/streaming profiles are rejected rather than silently mapped to request/reply.

```json
{
  "Cehpalon": {
    "SchemaVersion": 1,
    "Architecture": "Modular",
    "Topology": "SingleProcess",
    "Pattern": "RequestReply",
    "Modules": {
      "api": { "Enabled": true },
      "graphql": { "Enabled": false },
      "worker": { "Enabled": false }
    }
  }
}
```

Explicit false forbids activation, including as another module's dependency. Support modules may become implicit dependencies; entrypoints need explicit selection. Plan activation preflights registrations before callbacks; failures/cancellation release acquired resources in reverse order. Factories must clean up any partial allocation they have not returned. A lease does not roll back external business effects.

This first compiler consumes plain JSON, not the complete effective `IConfiguration` provider stack. It does not implement environment/command-line merging, live reload, atomic reconfiguration, real HTTP/GraphQL/Worker maps or tenant/authorization policy. Those require the corresponding adapter/profile capabilities and tests.

Use the [executable portable consumer](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/portable-core) for complete build/ownership examples. Its API/GraphQL/Worker names are in-process module recorders. The three real sample lanes remain separate work. See [ADR-0005](../../internal/adr/ADR-0005-w1-portable-core-composition.md) and [ADR-0006](../../internal/adr/ADR-0006-incremental-operation-code-generation.md) for supported shapes, diagnostics and proof limits.
