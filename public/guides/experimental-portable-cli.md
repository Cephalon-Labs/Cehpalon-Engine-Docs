# Experimental portable CLI

The source-checkout CLI supports one console profile, `portable-request-reply`. It creates a public in-process operation using existing Core, Composition and generated typed registrations. Configuration is checked before activation; disabled modules do no module-owned work. Tenant authority and transport/provider integration require separate explicit wiring.

Build `src/Cehpalon.Engine.Tooling/Cehpalon.Engine.Tooling.csproj` in the Engine checkout with the SDK pinned by `global.json`. Invoke the resulting `cehpalon.dll` with that SDK:

```text
dotnet cehpalon.dll --help
dotnet cehpalon.dll new --name MyApp --output <new-directory> --engine-root <Engine-checkout>
dotnet cehpalon.dll validate --config <generated-directory>/appsettings.json
```

The output parent must already exist; the destination must be new. Names use an uppercase ASCII letter followed by ASCII letters/digits, at most64characters, excluding reserved device names. Existing files/directories are never merged or overwritten. Observed symlink/reparse ancestors and known Engine/Docs/Samples checkout content destinations are rejected; ignored `.local` output is available for retained trials. These checks do not establish a hostile-filesystem security boundary.

The CLI writes nine fixed source/configuration files; it does not build, install, download or start services. To run the generated consumer, deliberately restore/build `Consumer.csproj` with the pinned SDK, then run its assembly with `appsettings.json` or `appsettings.off.json` as the configuration argument. The generated README contains the concrete commands. Source references use the checkout path and its observed hashes; later edits to that checkout can change subsequent builds.

The output assembly uses `PortableConsumer.<Name>` and source uses the fixed namespace `PortableConsumers.Generated`, avoiding compiler/framework/Engine name collisions. Generated projects inherit ordinary SDK/MSBuild build policy, so source/output parents and inherited customizations must be trusted. Source paths with MSBuild metacharacters such as `$`, `%` or `;` are rejected; spaces, Unicode and XML-escaped `&` are covered by the consumer proof.

The [executable Samples proof](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/tooling) verifies the real CLI, actual emitted registry, compiler-free runtime graph, enabled/disabled configuration and cleanup. Read its locked Engine revision and final evidence before treating any local observation as current.

This experimental subset leaves full #20 profiles/transport schemas/tooling benchmark, distribution/global-tool installation, NativeAOT/trimming and listed-supported Windows qualification outstanding. Overall runtime maturity remains M0 and #3 remains Blocked. No timing or production claim is made.
