# 2026-10-27 — New program baseline

Timezone: Asia/Bangkok. Status: initial planning and GitHub/repository setup; see validation evidence for the final observed metadata checks.

## User decisions

- The request was supplied in an attached text file and preserved in `internal/requirements/2026-10-27-user-request.md`.
- The three requested URLs under Cephalon-Labs are intentional. The user explicitly clarified that repositories, Project, milestones and tasks had not yet been created. Start a new baseline; do not restore historical implementation/maturity/task state from memory.
- The user selected all three proposed sample families: Small API, multitenant business API/Worker/SQL, and AI/Agent/Retrieval.
- Preserve configuration-driven selection, shared business handlers/contracts, selective activation, Engine-only commit journals, synchronized Docs/Samples and persistent shared AI rules.
- Prior private/MIT and Cephalon-Neza identity preferences remain in effect; the user has not changed them. No public release, paid provider provisioning or NuGet publication is part of this planning/bootstrap.

## Observed state and changes

- Current workspace: `D:\Cephalon\Cehpalon-Engine`, `D:\Cephalon\Cehpalon-Engine-Docs`, `D:\Cephalon\Cehpalon-Engine-Samples`. All three directories were empty at the start.
- Both connector and authenticated GitHub CLI initially returned 404 for the requested repos. The CLI authenticated account was Cephalon-Neza. After the user's clarification, the repos were created as private.
- Project created: `Cehpalon-Engine`, organization Project **4**, ID `PVT_kwDOEDryKs4Bo6sb`, https://github.com/orgs/Cephalon-Labs/projects/4 . Historical Project 3 does not identify this new baseline.
- Created six W0–W5 workstream milestones and 23 Engine issues, with native Type, Labels, Priority, estimates and task-specific gates. Actual hours remain null; no person-hours were measured.
- Canonical shared skill: `skills/cehpalon-engine/SKILL.md`; each repo has AGENTS.md and Claude/Gemini entry files. Other tools must load the same guidance through their supported context mechanism; no vendor runtime integration is claimed.
- Primary integrated two bounded read/research/document-writing agent assignments; only primary performed remote writes.
- [Engine commit trace](../evidence/bootstrap/engine-commit-journal.md) records only Engine SHA. Repository bootstrap is not feature maturity.

## Research findings

- Microsoft announced .NET 11 RC3 on 2026-10-25 and recommends RC2 users update for security fixes. Requalify current SDK and provider versions; do not reuse old RC2 SDK pins blindly. See sources in the program plan.
- The system SDK installation visible through PATH has maximum SDK 10.0.402 and no .NET 11. This does not inventory all private SDK locations. No SDK was installed during bootstrap.
- .NET 12 is a separate planning/research track; do not expose unverified future APIs as supported contracts.
- Comparative study is official-source document review only, not installation, benchmark, security audit or production proof.

## Proof boundaries

- Runtime source and executable samples are not implemented; runtime feature maturity remains M0.
- Bootstrap verification covers skill syntax, local document links, task/Project metadata, native issue types, author identity and Git alignment where explicitly reported. It does not establish runtime test passes, CI execution or benchmark results.
- Proposed engineering standards and future capability/provider choices must be refined and recorded in ADRs before the implementation tasks that depend on them.

## Resume

1. Read this handoff, `internal/planning/2026-10-27-program-plan.md`, requirements coverage, live Engine issues/Project 4 and current Git state.
2. Continue W0 requirements/architecture (#2), platform qualification (#3), comparative study (#4), quality plan (#21) and conflict-aware sync (#23), respecting dependencies and actual statuses.
3. Select the first concrete business workflow, workload/SLO and provider/version/host set across the three sample lanes. Startup config plus redeploy is the proposed first boundary; live topology changes need a separate design.
4. Do not rerun the bootstrap initializer as a general sync tool. Fetch current state, detect conflict and maintain observed-state mirrors without recreating IDs.
