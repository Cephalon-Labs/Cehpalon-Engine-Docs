# Requirement-to-task map

Source: [preserved user request](2026-10-27-user-request.md) and [2026-10-27 clarifications](../memory/2026-10-27-program-bootstrap.md). This map is planning coverage, not implementation coverage. All runtime capabilities start at M0.

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
