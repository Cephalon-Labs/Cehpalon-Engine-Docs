# Portable CLI/scaffolding continuation — #20

Date: 2026-10-29 (Asia/Bangkok). Experimental bounded subset; full #20 remains In Progress/M0 and #3 remains Blocked.

## Selection and accepted boundary

The live Project 4 readback had zero Ready cards. Two agents selected the portable subset of existing #20 because Core, Composition and operation registration generation already exist and can be exercised without platform qualification. The user's authorization covers this implementation; it does not clear original #20 dependencies #2/#11, W5, full transport-schema/profile acceptance or #3. Priority P2 and40–80h estimate/midpoint60 remain; actual/remaining hours remain null.

[ADR0012](../adr/ADR-0012-portable-cli-scaffolding.md) and the [correctness protocol](../validation/portable-cli-scaffolding-protocol.md) define one console profile, `portable-request-reply`. Timing benchmark is Not required for this bounded file-generation/correctness slice because no runtime algorithm/performance claim changes. Full #20 tooling benchmark remains Planned; previous Small API observations are neither repeated nor substituted for it.

## Implementation

The `cehpalon` executable has strict `new`, `validate`, `--help` and `--version` commands. It writes exactly nine deterministic files, observes hashes of17selected Engine inputs, copies pinned SDK/feed policy and emits explicit source ProjectReferences. CodeGeneration is an analyzer-only reference. The CLI runs no shell, compiler, downloader, installation or service.

Existing destinations are rejected; fixed files are created in an owned sibling stage and published with a no-overwrite move. Cleanup verifies the absolute owned stage and deletes only expected plain files; unexpected entries are retained. Tests inject failures before/after each of nine writes, publication failure, competing destination creation and unknown stage content, preserving unrelated bytes. Observed symlink/reparse ancestry, device namespaces, unsupported MSBuild source-path metacharacters and known Engine/Docs/Samples content destinations are rejected. Trusted parents and normal inherited SDK/MSBuild policy remain required; this is not a hostile filesystem/build sandbox or complete alias/TOCTOU defense.

The generated consumer validates configuration through unchanged Composition before supplying factories. App depends on core and builds the actual generated typed/lazy registry inside its activation factory. It dispatches one shared echo handler through unchanged Core, then disposes handler/modules before reporting counters. Optional is an explicitly documented negative fixture whose factory throws if selected; no optional provider is implemented. All-off and invalid config report zero activation/dispatch counters. The example is public and unprotected: generated metadata is not tenant authority.

Consumers use a fixed `PortableConsumers.Generated` namespace and `PortableConsumer.<Name>` assembly name to avoid compiler/framework/Engine name collisions. Source hashes are observations of selected editable checkout bytes, not immutable Git or distribution attestations. The Samples verifier independently locks the actual clean Engine revision, makes a real local clone in a Unicode/ampersand/space source path, invokes the actual CLI, restores/builds the emitted project and checks the emitted registry/runtime graph and runtime counters.

## Review and retained attempts

Independent review led to redacted static diagnostic paths/messages (unknown config keys could otherwise echo input), structured malformed SDK/feed failures, device namespace rejection, MSBuild path metacharacter refusal and real consumer package-lock checks. The ineffective late `ImportDirectoryBuildProps` flag was removed; ordinary inherited policy is explicitly trusted. Timeout logs/commands are retained by the harness even on command timeout. Valid-name compiler repros rejected `Program`/`Console` under the original template and `OperationContext`/`ModuleRole` under an intermediate name-derived namespace. The final namespace is independent of the requested name, with an actual eight-name build/run corpus; no extra restriction was imposed on otherwise valid names.

The Windows integration02 corpus also retained an actual `System` consumer runtime failure: its unprefixed assembly resolved to the framework `System` facade, causing MissingMethodException before entrypoint. The final assembly prefix addresses this distinct runtime identity collision. The failed entire attempt remains failed; final verification repeats the complete bounded matrix.

New hosted CI actually executed at the intermediate Engine revision, unlike the older payment-rejected runs. Platform smoke passed12checks with2Not run cases on each hosted OS. Portable contracts built successfully and passed the existing347checks, then failed exactly one Tooling `.local` case per host: a same-named outer runner directory was mistaken for a checkout. The correction recognizes discovered checkout roots only when an observed `.git` file/directory exists. A two-level same-name fixture reproduces that layout and checks allowed output; sibling checkout refusal still uses actual marker fixtures. Both failed hosted artifacts remain retained. Complete local/hosted validation of the corrected revision is recorded below; no failed series is relabeled as a pass.

Agent worktrees and original attempts remain at `.worktrees/tooling-cli` and `.worktrees/tooling-tests`. Preliminary component/consumer runs are explicitly uncommitted integration evidence. They cannot substitute for final clean revision results. Compiled artifacts, private fixture directories and local clone object databases are excluded from committed raw evidence; command logs, result JSON, generated registry and consumer lock are retained.

## Validation and tracking

Final Engine revision: `39ae0cc6ae56045a9d3d24f94eb564efa5941254`. The preceding Engine commits `3974c7d8099945e4446e210e04bca2ab630f3174` (initial CLI/contracts) and `b921a6d1cde5ec5d138d8efe84b760d6241de461` (name collision correction) are all journaled under #20. Core/Composition/generator runtime library semantics are unchanged.

| Exact-revision host | Component checks | Tooling subset within that total | Actual CLI-generated consumer proof |
| --- | --- | --- | --- |
| Local Windows | 462 passed /0failed | 115 passed | 70checks; enabled/off/invalid plus8collision-name build/runs |
| Local WSL Linux | 459 passed /0failed | 112 passed | 70checks; same matrix run sequentially after Windows |
| Hosted windows-2025 | 462 passed /0failed | 115 passed | Not run on hosted CI; existing compiler fixture passed |
| Hosted ubuntu-24.04 | 459 passed /0failed | 112 passed | Not run on hosted CI; existing compiler fixture passed |

Three extra tests are Windows-specific path alias checks; they are not silently counted as Linux passes. Each local consumer matrix makes an actual clean clone at a source path with Unicode, spaces and ampersand, verifies17observed source inputs, checks an actual emitted registry and package lock, and observes a runtime graph containing only the consumer/Core/Composition. The app-on case has core1/app1/optional0factories, handler1construction/1disposal/1dispatch and2module disposals; off and invalid dependency cases have allzero counters.

Corrected hosted [component CI40754466014](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/40754466014) and [platform smoke40754466002](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/40754466002) passed. Both downloaded component manifests have source hashes independently checked against exact committed Git blobs. Platform smoke is12passed/0failed/2Not run per hosted OS; it is bounded SDK/package/localhost evidence, not real PostgreSQL/RabbitMQ connection qualification or full #3 clearance. Older payment-rejected runs remain unpassed; no forced rerun or billing action was performed.

Final exact-revision results, raw retention and readback are recorded in [delivery evidence](../evidence/tooling/delivery.json). Local evidence and independently executed hosted CI are distinct. NativeAOT/trimming, global-tool/package installation, arbitrary inherited build policies, transport schemas, real providers and production readiness remain unproven. Full #20 acceptance remains unchecked and full Test/Benchmark fields remain Planned. #3 body/editable metadata remain unchanged/Blocked as requested; the new hosted platform evidence requires separate review against its full qualification checklist. No public/NuGet release, dependency/estimate change or maturity promotion is authorized or claimed.

The [tracking readback](../evidence/tooling/tracking-readback.json) confirms exactly one reviewed body operation on #20, dry run then exact-plan-hash apply (`02889e1725cb08000c6f08304723b9e7052dc33030ce75a169a700aa911c64b3`), followed by23verified mirrors. #3 body and editable metadata are byte/value identical to the pre-wave snapshot; #20 metadata and full gates are unchanged. All three new Engine journal commits resolve in Engine. Docs/Samples revisions are technical provenance in delivery evidence, not card journal entries.

Retained plain raw evidence: Engine139files/703015bytes, hosted CI92files/482873bytes and Samples863files/1294041bytes plus their manifests. Every Samples raw entry independently matches its committed Git blob and SHA256. These counts exclude compiled artifacts, clone object databases and private fixture state; original local attempts/worktrees remain. Samples technical delivery revision is recorded in the delivery manifest without a Docs self-hash loop.
