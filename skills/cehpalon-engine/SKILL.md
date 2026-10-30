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
- Generated operation registrations remain typed and lazy: code generation does not activate modules or provide tenant authority. Deduplicate declarations by semantic symbol identity, validate partial declarations together, and prove emitted consumers compile. Display names are not unique symbol identities.
- Tenant and authorization boundaries apply to every supported entrypoint and state/event/cache/retrieval/tool path.
- Caller metadata and constructed identity/membership DTOs are not authority. Protected operations must route through configured fresh identity/membership/resource/policy checks; plain Core/codegen remains unprotected unless wired to that boundary. Checked scopes are in-process capabilities, not a sandbox or atomic provider authorization.
- Lease invalidity must latch permanently; enforce UTC validity plus a monotonic elapsed cap. Keep cleanup faults distinct from semantic access denial and preserve both execution/cleanup errors.
- Transport adapters require explicit typed bindings and host-established authentication. A principal flag or adapter registration is not tenant authority; protected bridges must invoke fresh tenant dispatch. Unexpected vendor exceptions must be redacted, and HTTP plus GraphQL cancellation must reach the handler.
- A disabled GraphQL plan must skip both vendor service registration and endpoint mapping. Source/package presence is not activation; report actual registration/service/factory observations separately from vendor constructor probes. A protected tenant fixture does not replace the original public W0 workload or its full performance gates.

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

## Portable scaffolding continuation rules

- A scaffold must build and run as an actual generated consumer. Registration text checks and recorder labels alone do not establish transport/provider profiles. Keep the experimental portable-request-reply console proof separate from the three sample lanes and full #20 qualification.
- Keep user-selected names independent of generated namespace and framework assembly identities. Prove compiler/framework/Engine collision names with actual SDK builds and runs; a successful compile alone missed the System facade runtime collision.
- Recognize discovered program checkout boundaries using observed Git markers, not directory names alone: hosted runners can have same-named wrapper directories. Treat source/output parents and inherited SDK/MSBuild policy as trusted; observed hashes and path checks are not immutable attestation or a filesystem/build sandbox.
- Web profiles must validate capability plans before host/credential access. Keep ephemeral self-test identity separate from normal serving with caller-provided trust. Post-activation failures must report actual activation/cleanup counters; do not replace them with a new zero-valued recorder.
- Include embedded source-template bytes in source inventories and pin their line endings explicitly. `.cs.txt` resources are runtime-bearing generator inputs even when a verifier only recognizes `.cs` files by default. Prove Windows TLS key loading through actual external serving, not only a self-test with a different loader.
- Export transport contracts from actual serializer/type metadata and the same typed catalog used by runtime mapping. Explicit GraphQL schema compilation has positive construction/disposal work; disabled transports have none. Structural schemas do not replace parser limits, validation lambdas or fresh tenant authority, and offline export must not open network introspection endpoints.
- Preserve nullable successful response roots when deriving public HTTP schemas; constrain request bodies separately to the adapter's object-only rule. Return detached metadata and never expose mutable serializer options. Concurrency claims require actual independently scheduled workers, not only async calls that may finish synchronously.

## Measurement lessons from Small API

- Keep public functional/performance fixtures distinct from protected tenant fixtures. Baselines may share representation types, packages and pure fixture metadata; declare that scope and verify they bypass the measured dispatch/activation paths. Same-binary RSS is not stripped-distribution footprint.
- Freeze codec buffering, connection preparation, actual TLS telemetry, clock continuity and real private-file permissions before the complete attempt. A collector preflight failure is retained evidence, never a hidden retry. Affinity is not dedicated resources.
- Check all offered records/manifests, state, lifecycle and all five CV values. Startup absolute failure, invalid CV and nonqualifying reference environment remain separate negative outcomes even when every request is correct and individual pairs pass. Preserve raw failure/audit attempts, representation-rounding corrections and their proof limits.

## Tooling measurement continuation rules

- Compare generated compilation with an independently authored typed registry and symmetric compiler state. Declare parsing, authoring, reference and edit preparation exclusions; DriverRun+Emit versus prepared Emit does not measure human productivity or full SDK builds. Verify actual emitted runtime semantics and keep cache tracking outside timed drivers.
- Freeze exact primers, pairs, order, versions, repetition means and percentile estimator before timing. Keep CPU quantization zeros and process-wide allocation noise. Scope variability flags by workload; a CLI-only flag cannot summarize generator groups. Correctness completion, descriptive timing and qualification are separate results.
- Snapshot the actual harness/lock/protocol from the first preparation attempt; a hash alone does not recover an older script. Exclude compiler/analyzer/CLI runtime dependencies by their actual families, since a valid generated consumer name can contain tooling words. Preserve failures and fix preparation before a complete fixed attempt.
- Keep every complete candidate, including regressed variance and mean costs. An equivalent-options runtime may share serializer metadata; quantify allocation rather than asserting full rebuilds. A source-method split or small recorder saving does not establish JIT/GC causality. A justified new source revision needs a separately predeclared complete attempt, never a favorable unchanged-source rerun or selection of the best intermediate result.

## Tooling trace continuation rules

- Verify collection using a separate synthetic owned target before fixed lanes. Resume every suspended diagnostic port through that same endpoint; a default-PID acknowledgment is not proof another port resumed. Normalize Windows environment names case-insensitively in child copies, isolate collector/analyzer ports, respect disabled IPC policy and resolve executable paths before changing cwd.
- Subscribe actual CLR templates and retain event ID/opcode/version/template metadata. Positive JIT/GC/stack fixtures and zero reported loss are separate from pairing completeness. Keep ambiguous/incomplete episodes and PID/clock/source/owned-cleanup checks; sampled thread stacks are residency, not kernel CPU evidence.
- Record observer overhead and real clock/cadence. Avoid repeated global thread enumeration; an initial pinned-thread fallback excludes later threads. Sampled proc counters, raw syscall intervals, physical-disk latency and exact scheduling events are different evidence. Separate executions cannot be fused as causal overlap.
- Freeze executing launch source separately from later on-disk snapshots; record approved differences explicitly. Keep every failed/partial lane and repeat the full fixed lane only for a stated collection correction, never select favorable rows. Preserve raw traces losslessly with deterministic compression/hashes and avoid build/private/credential material.
- GC overlap and background JIT do not isolate avoidable Engine work. Preserve publication durability, authority boundaries, compiler concurrency and selected schema work. If no safe product patch is justified, record that conclusion; a separately predeclared unchanged-source full benchmark is an observation, not a code speedup or qualification.

- strace startup can spawn probe children before the tracee. Proc child presence alone is not target identity: join successful exact-host raw execve with stable live ownership/image before leasing, then never switch identity. Header visibility follows resume; only that bounded wait may tolerate a successful target/tracer exit.
- Test source-freeze code on the actual Python/runtime versions before live capture; code-object APIs differ across versions. Malformed wait identities require persistent compatible-key poisoning, and reused native TIDs cannot support favorable temporal pairs. Use caller-only fields for caller claims: process-wide matched-TID/background unions are different observations.
- Same method IL/signature/EH records do not establish equal complete binaries or resolved runtime behavior; keep debug/build/metadata differences explicit. Finding vendor Emit/worker-wait context does not justify changing concurrency, GC, selected schema or authority/publication semantics; do not add unchanged-source benchmark runs without a new declared evidentiary reason.

## Startup/variance continuation rules

- Declare SDK/shared-runtime, app, working/content root and raw-output filesystems separately on WSL. Verify staged bytes/links and actual loaded runtime paths. Native storage may improve observations without proving reserved resources/native deployment or an Engine-code speedup. Never move key load, full readiness verification or first-request initialization outside the existing startup clock to claim a pass.
- Exclude repository evidence/audit sources from Web SDK default compile/content/package items; preserve raw evidence in the repository. Publish readiness only after complete writes with no overwrite; transient observation retries remain bounded and counted.
- Keep measurement/control/persistence clocks explicit. Same preparation request policy does not establish equal physical connection readiness. Retain failure-phase telemetry when available and state missing-event limits; a single dropped collector preflight is not a server capacity ceiling.
- Keep numerical acceptance, diagnostic failed attempts and platform/reference qualification separate. Preserve higher mean metrics as well as lower CV; buffering recorder output has an abrupt-loss limit. No best-rerun selection, latency floors or retroactive threshold changes.

## Collector readiness continuation rules

- Prove physical HTTP1.1 readiness with simultaneous unread nonempty response leases and distinct first-use TLS identities, then fully validate/drain before fixed offered traffic. Separate control/load histories explicitly; cumulative handshakes do not prove later live sockets.
- Retain failed-phase TLS/client/raw accounting and a structured stage/count-consistent rejection. Unknown crashes, incomplete rows/metadata or later-phase artifacts cannot be relabeled as a known failed preflight. Managed failures join children before reporting; abrupt loss still invalidates buffered evidence.
- Run time-sensitive conformance sequentially on a shared host without competing owned builds/audits. A handler that enters after client abort does not prove in-flight cancellation even with fast ACK/no mutation. Preserve the failure and predeclare any justified complete matrix repeat with unchanged gates; never search favorable cases/runs.
- Completion-metrics control TLS handshakes can fall inside allocation/CPU metrics brackets. Disclose matching nonzero instrumentation overhead and distinguish request latency/client snapshots from control/persistence boundaries. Successful new observations do not reconstruct missing past events or isolate a single cause.
