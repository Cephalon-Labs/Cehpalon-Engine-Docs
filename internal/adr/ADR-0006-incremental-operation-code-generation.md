# ADR-0006 — Compile-time operation registrations

Date: 2026-10-27. Status: Accepted for the first experimental code-generation slice of #20 supporting #5/#6. CLI/scaffolding/transport schema generation remain future work under the existing #20 card.

Use a Roslyn `IIncrementalGenerator` and `ForAttributeWithMetadataName` to inspect explicit `[Operation("id")]` handler declarations. The generator emits typed registry calls sorted by canonical operation ID; runtime code does not depend on Roslyn or scan assemblies. It does not create endpoints, enable modules, execute handlers, generate business logic or bypass identity/tenant policy.

Generated `Cehpalon.Engine.Generated.OperationRegistrations.RegisterAll(builder, factory)` is internal to the consuming assembly. It registers lazy typed factories using the Core `IOperationHandlerFactory` contract; registration does not instantiate handlers. The consumer supplies factory ownership/lifetimes explicitly.

Duplicate/invalid IDs, ambiguous handler contracts and unsupported generic/inaccessible/file-local declarations are compiler errors with source locations. Unsafe candidates suppress registry output. Generated names use fully qualified escaped symbols; output is deterministic for equivalent declarations, independent of syntax order/culture. Compiler tests must compile the emitted consumer code, not merely compare text.

The analyzer targets netstandard2.0 and pins `Microsoft.CodeAnalysis.CSharp` 4.14.0 as a private compile-time dependency. This is a deliberate conservative API floor, not a latest-version assertion. Lock/hash/license inventory and an actual build under the pinned SDK establish the observed compatibility boundary; IDE/compiler versions not tested remain unqualified.

Primary sources reviewed: [Roslyn incremental design](https://github.com/dotnet/roslyn/blob/main/docs/features/incremental-generators.md), [incremental cookbook](https://github.com/dotnet/roslyn/blob/main/docs/features/incremental-generators.cookbook.md), [exact Roslyn NuGet package](https://www.nuget.org/packages/Microsoft.CodeAnalysis.CSharp/4.14.0). These describe generator APIs and package targets; they do not establish Cehpalon runtime or AOT compatibility.

No NativeAOT/trimming/IDE/incrementality-performance/distribution claim follows from deterministic emitted source or a netstandard target. Those require their own builds/protocols. Actual code-generation diagnostics and end-to-end in-process consumer proof are recorded with Engine source hashes/revision.

Implementation review confirmed that display names are not semantic identities: distinct file-local/normal symbols can share them. Retain semantic identity, check every candidate before deduplication, validate attributes across the whole partial symbol, and reject reserved namespaces as well as types. See the [delivered source and independent before/after proof](../planning/w1-core-composition-codegen.md).
