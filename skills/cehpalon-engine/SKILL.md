---
name: cehpalon-engine
description: Plan, implement, document and verify the Cehpalon Engine three-repository program with configuration-selected modules, shared business handlers, traceable Engine issues and evidence-bound feature maturity. Use only for this program.
---

# Cehpalon Engine shared working rules

This is the canonical project skill for all participating AI tools. A tool must load it explicitly or through its supported entry file; do not assume every vendor automatically discovers SKILL.md.

## Start from current evidence

- Read `internal/memory/README.md`, the relevant latest handoff, Engine issue, requirements and ADRs in this Docs repository. Verify local paths, Git state, remote heads and relevant CI before using older conclusions.
- The current workspace is `D:\Cephalon` with `Cehpalon-Engine`, `Cehpalon-Engine-Docs` and plural `Cehpalon-Engine-Samples`. Historical paths, projects, issue IDs and maturity are not the current baseline.
- Preserve the user's explicit choices. Keep observed facts, accepted requirements and proposed design separate. Research is not runtime proof.

## Architecture invariants

- Reuse business handlers/contracts across supported profiles. Keep host, transport, database, broker and AI vendor objects outside portable business contracts.
- Config selects a compatible capability set. Validate the graph and build an immutable plan before activation. Reject incompatible selections with actionable diagnostics.
- Explicitly disabled modules must do no module-owned factory, constructor, connection, endpoint or background work. Prove this; shared dependencies required elsewhere must be distinguished.
- Changing transports/topologies/providers preserves only the semantics declared in their compatibility contracts. Do not hide differences in consistency, retries, transactions, queries, streaming or lifetime.
- Tenant and authorization boundaries apply to every supported entrypoint and state/event/cache/retrieval/tool path.

## Delivery and traceability

- Engine owns issues, milestones and Project cards. Docs owns requirements, ADRs, task mirrors, memory and evidence. Samples owns real consumer proofs. Synchronize relevant changes within the same delivery.
- Every task needs native Type, Labels and Priority plus acceptance criteria, dependencies, estimated hours, actual-hours evidence, tests and benchmark applicability. Unknown actual hours stay unknown.
- Use `tasks/<Engine-issue-number>.md`. Reopen/update an existing card for changes to its existing scope, preserving before/after/reason; avoid duplicate tracking cards.
- Use the [reviewed two-way workflow](../../internal/standards/tracking-sync-usage.md): pull current state, edit native/project metadata or body, review a bounded plan, dry run, apply the exact approved plan hash, then read back. Existing user authorization covers in-scope updates; the tool's concrete plan review does not imply an additional user confirmation requirement.
- Preserve task-body and raw-evidence bytes, including LF/CRLF. Do not format them through Markdown/EOL normalizers. Keep plans/checkpoints/private fixture state under ignored `.local`; hashes do not authorize replacing later edits or skipping operations.
- Every Engine commit must be linked by full Engine SHA to its relevant Engine issue(s) and task mirror(s). Do not journal Docs or Samples SHAs in task/card commit references and do not create a Docs self-hash loop.
- Git author and committer: `Cephalon-Neza <272007299+Cephalon-Neza@users.noreply.github.com>`. Set repository-local identity; do not silently change global identity.
- Keep these three repositories private and MIT unless the user changes that decision. Package preparation does not itself authorize public release or NuGet publication.

## Evidence and handoff

- Follow `internal/standards/delivery-and-maturity.md`. Maturity is scoped to feature/provider/version/host/profile; no blanket pass from a happy path or unrelated provider.
- Predeclare benchmark workload, baseline, thresholds and analysis; preserve raw output and invalid/failed attempts. Do not filter outliers, select only favorable reruns or relax thresholds to claim a pass.
- CI blocked before execution is blocked, not a test pass or a code failure. Record the Engine revision and the actual proof boundary.
- Record decisions and continuation context in `internal/memory/` after meaningful work; public guides contain only supported behavior and clear experimental status.

## Multiple AI tools

- Separate AI-assisted development coordination from runtime AI/Agent features. A vendor role or model name is not evidence of review quality or security assurance.
- Delegated work needs a bounded assignment. Isolate branches/worktrees when agents edit code; designate one integrator/remote writer for each wave. Read-only research can run independently.
- Each handoff states changed files, validation results, assumptions, limitations and next work. Do not overwrite another agent's changes or store credentials in handoffs.
- Vendor entry files point to these rules; vendor SDK/CLI support is only claimed after testing with the actual supported tool/version.
