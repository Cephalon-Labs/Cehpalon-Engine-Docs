# Tooling observational benchmark protocol

Declared 2026-10-30 (Asia/Bangkok) before canonical timing. Scope existing #20, ADR0015; #3 body/editable metadata remain unchanged/Blocked. Full gates/dependencies/estimates/null hours/M0 stay unchanged. SDK11.0.100-rc.3.26522.148, Roslyn4.14.0, existing packages and actual Engine revision are pinned. Run complete Windows then Linux matrices sequentially with no competing owned timed workload. No old Small API load/startup benchmark rerun.

## Compiler comparison

Fixtures have1,3,32valid typed operations. Cases in order: each size followed by fresh, no-op, edit; caseIndex0..8. Both paths emit real PE with the same valid business contracts. Independent authored manual registration source is cross-checked against canonical generated registration AST and actual runtime lazy-factory0/dispatchN/disposalN behavior before and after timing. Runtime/compiler-only dependency separation is checked. Actual diagnostics and emit success are verified every iteration; PE/generated/source hashes are retained.

Timed generated scope is DriverRun+Emit; manual scope is Emit of the already-authored equivalent registry. Common source parsing, metadata loading, manual registry authoring/parsing and edited-tree preparation are outside clocks. This is generation/compilation overhead over prepared manual code, not full SDK build or human developer productivity.

- Fresh: new input/driver/manual compilation graphs each pair; process/JIT/reference caches are still primed.
- No-op: retain the exact input+driver and manual compilation; no-op cache tracking is a separate unmeasured preflight. Timed driver tracking is off.
- Edit: start seeded at version0; replace one handler operation ID and corresponding manual registry tree outside clocks. PairSequence even targets version1, odd targets version0, across primers into measured rows. Each pair therefore changes one ID. Preserve actual generator invalidation observations, not an assumption of optimal incremental behavior.

Per case:2paired primer iterations (4rows), then5paired repetitions ×3iterations (30rows). Total36primer rows +270measured rows =306rows. No-op/edit also have12unmeasured seeded-state artifacts (3sizes×2states×2paths), reported separately from rows. PairSequence0,1 are primers,2..16 are measured. Generated runs first iff `(caseIndex + pairSequence) % 2 == 0`; both paths consume the same target version. No force-GC between pairs or filtering. Record all ticks, process CPU, process-wide allocated bytes and GC deltas around the declared scope; disclose instrumentation/global background allocation noise and zero CPU timer quantization without floors.

Summarize each case/path over all15measured iterations and all5repetition means (3iterations per repetition). Wall-time CV uses sample standard deviation divided by mean of those5means; report all5means and raw15-value min/max. Raw p50/p95 use the fixed nearest-rank estimator `sorted[ceil(p*n)-1]` over all15values (so p95 equals the largest of15). No interpolation/floor/filtering. CV>15% marks unstable performance inference. It is not grounds to drop samples, repeat favorable pairs or claim a timing-budget pass.

## CLI processes

Fixed base order: new-portable, new-small-api, validate-portable, validate-small-api, export-api, export-both, export-graphql, export-off. Each round rotates this list left by `round % 8`, then reverses odd rounds. Eighteen rounds total:0..2 are primers,3..17 measured. Exactly144fresh launches =24primer +120measured;15measured rows per scenario. Every new/export output is a new directory. Fixture build/restore/lock/source and generator benchmark preparation are outside CLI clocks.

Clock starts immediately before process launch and ends after process exit and stdout/stderr drain; post-return artifact validation/log persistence is excluded. Store raw start/end/elapsed, order and exit/output data. Per-process CPU is null if not reliably observed, never inferred from controller CPU. Processes are cache-primed fresh launches, not cold disk. No fake CLI baseline or application throughput claim.

Validate each result: exact9/14source files and observed17/32inputs, pure selected plans, deterministic artifacts, selected OpenAPI/SDL file sets, actual registry metadata and no business/host/key work. Enabled GraphQL export must disclose provider/schema work and awaited disposal; disabled module work stays zero. Timed operations start no network server and need no credentials. Preserve stdout/stderr/timeouts/failures and every primer row. Generated consumer build/locks/emitted registry/runtime graph are checked outside timing.

CLI summaries use all15measured wall values per scenario, sample CV, raw min/max and the same nearest-rank p50/p95 estimator. CV>15% flags unstable inference. No arbitrary numerical budget or superiority PASS is defined for these shared-host observations. Canonical phase order is build/preflight preparation, generator matrix, then the CLI18round series; compilation/verification work never overlaps a measured CLI interval.

## Acceptance and reporting

Required: all declared cases/rows/order/versions/semantic and emit/output checks complete, zero failures/timeouts/skips, exact source/SDK/lock provenance, monotonic/nonnegative metrics and no retries/filtered rows. Failure stops dependent measurement but retains partial raw; fixes require a complete new protocol attempt with failures preserved. Do not automatically rerun unchanged CI rejected before steps or change billing.

Report `status=completed|failed`, `correctness_status=passed|failed`, `performance_status=observed` with variability flags and `qualification_status=not_qualified`. Correctness/completeness thresholds are100%; full #20 Benchmark Planned/#3 Blocked/M0 remain unchanged. Neither affinity nor available memory proves reserved resources. Dedicated/reference hardware, production/IDE/provider/AOT/distribution behavior and numerical acceptance budgets are outside this phase.
