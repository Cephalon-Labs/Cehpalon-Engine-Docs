# Requirement-to-task map

Source: [preserved user request](2026-10-27-user-request.md) and [2026-10-27 clarifications](../memory/2026-10-27-program-bootstrap.md). This map is planning coverage, not implementation coverage. All runtime capabilities start at M0.

The [2026-11-20 user refinement](2026-11-20-optional-access-audit.md) adds optional authentication, RBAC/ABAC and operation audit/history under existing REQ-05/#7/#8 and REQ-10/#18. [ADR0033](../adr/ADR-0033-optional-access-and-audit.md) defines the bounded portable/local consumer slice and remaining provider/lifecycle gates.

W0 refinement has a [decision package with four ADRs and three workload protocols](../planning/w0-decisions.md) and [bounded SDK/artifact qualification](../planning/w0-qualification-and-sync.md). REQ-03/04/13 now have an experimental [W1 Core/Composition/code-generation slice](../planning/w1-core-composition-codegen.md). This is partial implementation coverage, not full requirement acceptance: full transport/provider and identity lifecycle acceptance, all three original lane workloads and #3 supported-Windows proof remain outstanding.

| Requirement | Initial Engine issues | First proof / boundary |
| --- | --- | --- |
| REQ-01 — comparative software/kernel/runtime/server/OS/pattern research | #2, #4, #21 | Official-source comparison, scope and predeclared experiments; no exhaustive study or superiority claim |
| REQ-02 — .NET 11 implementation research and .NET 12 horizon | #3 | Exact current SDK/provider qualification; unstable future APIs remain research |
| REQ-03 — host-agnostic small core and reusable business logic | #5, #6 | No host/provider objects in portable contracts; consumer contract tests |
| REQ-04 — select topology/pattern/architecture/transport via appsettings | #2, #6, #9, #10 | Validated compatible profiles; zero activation when disabled; no universal semantic equivalence |
| REQ-05 — tenancy, identity and security across every supported path | #7, #8, #21 | Real positive/negative isolation and authorization tests per adapter/provider |
| REQ-06 — API, GraphQL, gRPC, JSON-RPC, SSE and Worker | #9, #10, #14 | Per-protocol conformance, streaming/error/cancellation mappings and Worker lifecycle |
| REQ-07 — data/document/database and cache extensibility | #12, #13 | Capability-specific ports; provider/version tests for transactions, query and cache semantics |
| REQ-08 — eventing, scaling, driven architectures and workflow | #2, #14, #15 | Outbox/inbox, duplicate/crash/recovery, ordering and distributed consistency boundaries |
| REQ-09 — AI, agent behavior, retrieval and provider choice | #16, #17 | Model/retrieval/tool capability matrix, tenant scopes, budgets and bounded evaluations |
| REQ-10 — observability, reliability and resource performance | #18, #21 | Traces/logs/metrics, failure visibility, declared fair baseline and raw evidence |
| REQ-11 — server/serverless/edge/container/cloud/proxy/Kubernetes | #19 | Host/version capability matrix; startup/shutdown/health/scaling constraints |
| REQ-12 — small to very large projects, scale/autoscale | #11, #15, #19, #21 | Distinct sample workloads and deployment proofs; no capacity promise without load results |
| REQ-13 — CLI, scaffolding, codegen and less bootstrap code | #20 | Generated consumers build and match selected profile; measure developer steps/code |
| REQ-14 — private MIT repositories, GitHub Project/milestones/tasks | #1, #23 | Metadata and remote readback; native Type, Labels, Priority and Markdown mirrors |
| REQ-15 — per-task person-hours, subtasks, tests, benchmark and M0–M4 | #1, #21, #23 | Estimates separated from null actuals; acceptance checklist and evidence per capability |
| REQ-16 — every Engine commit trace, existing-card revisions, code/docs consistency | #1, #23 | Full Engine-only SHA journal, explicit change history and conflict-aware synchronization |
| REQ-17 — persistent memory and shared AI guidance across vendors | #1, #23 | Canonical SKILL, vendor entry files, current-state handoff; no assumption all tools auto-load it |
| REQ-18 — internal/public docs and future Astro | #22, #23 | Internal evidence separated from tested developer guides; website build is later scope |
| REQ-19 — all three real E2E sample families | #11, #15, #17 | Small API; multitenant API/Worker/SQL; AI/Agent/Retrieval with shared Core |
| REQ-20 — NuGet preparation and long-term evolution | #2, #22 | Local pack/install/upgrade, versioned contracts and migration/deprecation policy; publication is separate |

Issue references above belong to `Cephalon-Labs/Cehpalon-Engine`. Detailed acceptance criteria and estimates are mirrored under `tasks/<issue-number>.md`.

REQ-05 now has a [portable tenant/identity contract slice](../planning/w1-tenant-identity.md) with cross-tenant fixture tests. Its protected HTTP/GraphQL continuation is described below. Real IdP/provider isolation and full #7/#8 acceptance remain outstanding.

REQ-04/05/06/12/19 now also have a bounded [protected HTTP/GraphQL and Small API slice](../planning/w2-transports-small-api.md), using generated Core gateways and shared guarded business handlers. This covers actual localhost JWT/HTTPS fixture requests and disabled-entrypoint checks, not all transports/providers, the original W0 workload, native deployment or supported-Windows proof. #9/#11 remain open for their full gates and overall maturity remains M0.

REQ-04/06/10/12/19 now have a [complete Small API conformance/measurement continuation](../planning/w2-small-api-conformance-benchmark.md): 4000 public-fixture cases per observational host, cancellation/lifecycle/disabled checks, all startup/idle/load and diagnostic attempts retained. This is execution coverage, not full acceptance: absolute startup failed, Engine GraphQL CV12.3681% invalidates the performance series, shared WSL reference preflight remains Blocked and #3 remains Blocked. The public fixture does not establish tenant/provider/production proof.

REQ-04/06/10/12/19 continuation: [startup/variance tuning and complete attempt03](../planning/w2-small-api-tuning.md) now pass original numerical startup/idle/main/CV gates in a declared native-storage WSL profile; Engine GraphQL CV3.2616%. All12diagnostic attempts retained,11timed plus one HTTP Engine2000/s preflight37drops. These observations do not clear reference/#3 qualification or liftM0; no isolated Engine-code/all-metric speedup or provider/production claim.

Latest REQ-04/06/10/12/19 evidence: [physical collector readiness and complete canonical04](../planning/w2-small-api-collector-readiness.md). All52driver barriers prove128distinct held load TLS responses; failed-phase telemetry and guard rejection are independently exercised. All120startup/20idle/20main/12actuallytimeddiagnostics retained,5.472Mmeasuredcorrect/zeroerrors or drops, original numerical gates pass. Engine GraphQL CV4.769352% is valid but higher than03. Full sequential02 functional matrices pass bothhosts after retaining Windows01's one failed cancellation case. Reference/#3/full9/11 remainBlocked/M0; no provider/production promotion.

REQ-13 portable continuation: [experimental CLI scaffolding](../planning/portable-cli-scaffolding.md) creates one real console consumer using unchanged Core/Composition and generated typed registrations. The bounded proof covers actual consumer builds/runs, disabled/invalid config, lifecycle, failure-safe file publication and name/path collisions. It does not deliver transport schemas, the three provider lanes, distribution or the full tooling benchmark. #20 remains In Progress/M0 with original dependencies/gates; #3 remains Blocked.

REQ-04/05/06/13/19 continuation: [Small API CLI profile](../planning/small-api-cli-profile.md) generates an actual protected HTTPS consumer through unchanged Core/Composition/codegen and fresh tenant dispatch, with API-only/combined/GraphQL-only/off configuration and real tenant/disabled-module tests. This is a fixture-backed scaffold, separate from real IdP/provider, arbitrary transport-schema generation, all three lane qualification or production hosting. Full #20 gates and #3 Blocked remain unchanged.

REQ-04/06/13 continuation: [offline transport contract export](../planning/tooling-contract-export.md) adds selected OpenAPI3.1/JSON shapes from the actual HTTP serializer and SDL from the actual pinned GraphQL schema, sharing the runtime typed catalog and comparing artifacts with HTTPS/schema behavior. Disabled modules produce no artifact/service work. Structural schemas do not replace parser limits, validators or tenant authority. Full #9/#20/platform/provider/distribution gates and M0 remain unchanged; #3 remains Blocked.

REQ-10/13 observational continuation: [tooling benchmark](../planning/tooling-benchmark.md) measures actual generator plus emit against independently authored typed registration emit, and actual source-checkout CLI new/validate/selected offline export processes. The fixed matrix checks emitted/runtime/output correctness and retains every primer, measurement and failed attempt. Shared-host timing is Observed with descriptive variability flags, not a numerical performance qualification. Full #20 Test/Benchmark Planned, M0 and #3 Blocked remain unchanged; authoring/IDE/full-build/distribution/provider proof remains separate.

REQ-10/13 [variance investigation](../planning/tooling-variance.md): both full follow-up candidates passed correctness and retained all original criteria, but the variance goal remains unresolved. Final unstable generator counts Windows7/Linux4 and Windows export-off CV16.64% do not establish an improvement. Full gates/M0/#3 Blocked remain unchanged; source work reduction and a small recorder allocation saving are separate from timing/GC causality.

REQ-10/13 [process-scoped trace continuation](../planning/tooling-traces.md): fixed75diagnostic targets, positive synthetic collector conformance and independent50target runtime integrity/semantic replay retain all loss/pairing/clock/observer limits. Some slow manual/generated compiler rows overlap GC; no safe Engine optimization is isolated. Selected GraphQL work agrees with module guards. Final unchanged-source original benchmark is observational only; full #20 gates/M0 and #3 Blocked remain unchanged.

REQ-10/13 [same-process wait continuation](../planning/tooling-waits.md): corrected full25targetLinuxlane and852454checkindependentintegrityaudit preserveall306generatorrows/24CLIoutputs andsource/ownership/clocklimits. Observed caller managed waits lieinEmit; noavoidableEngineoperation orspeedup isolated. Lastoriginalbenchmarkunchanged, full#20gates/M0/#3Blocked preserved.
