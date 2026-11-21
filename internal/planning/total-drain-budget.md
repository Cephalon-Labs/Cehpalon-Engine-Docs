# Optional total cooperative outbox drain budget

Date2026-11-21. Tracking #18 with #7/#8 regressions. [Requirement](../requirements/2026-11-21-total-drain-budget.md), [ADR0047](../adr/ADR-0047-total-outbox-drain-budget.md), [predeclared protocol](../validation/total-drain-budget.md), [guide](../../public/guides/experimental-audit-trails.md).

## Behavior and proof boundary

DrainWithBudgetAsync selects an optional positive total up to one minute across the existing bounded manual drain. Null and original DrainAsync retain the legacy work tokens/errors and create no new total cancellation sources. The total starts after initial admission and survives every batch, independent child release and final guard. Per-batch work policies remain independent. Work that ignores cancellation remains awaited; no hard completion deadline, retry, renewal, scheduling or background task is installed.

Classify primary cancellation at selection before cleanup using original caller, then total, then per-batch observed signals. Preserve the selected primary if a different signal arrives during cleanup; release-only errors remain separate. Exact child errors and invocation-owned counts remain: a forwarded older/different-tenant RelayException cannot inject progress. Expiry during cleanup can withhold a child's return while preserving its actual acknowledgement count as interrupted progress. CompletedBatches advances only on a returned child success. No count implies rollback, unique delivery or empty global backlog.

One fresh authorized operation still owns the sequence; live scope checks are not repeated provider identity resolution. The generated consumer uses existing typed/lazy DrainGateway and exact configured grant. Portable relay scope and provider fences remain required. No provider SQL/schema, package/lock, scaffold17/32 inputs or authority change.

## Validation

First focused attempt passes212outbox (prior164+48new) and56status, all202 frozen/current/committed inputs exact. First consumer development attempt passes132 (prior108+24new); all97 executing/frozen/committed inputs match with LF/no normalization exception. Pre-SDK review corrections include positively observable signal ordering, external watchdog/finally joins and distinct legacy/new-null public API routes. No SDK failure, selective repeat or favorable rerun occurred. Original provider test bodies/SQL/locks and service/security registries remain unchanged. All preparation notes and declaration revisions are retained.

Exact Engine `7499db9759bc9e8017760fb4be34d35dd564393f` and consumer source `894801d140a758a0765942338a4af44efdad4648` passed the full serial matrix below. All original cases remain. Actual committed-source inventories and generated registry hashes match across hosts; no original performance benchmark was run. Retained attempts and source proofs are linked below.

## Tracking and limits

Only #7/#8/#18 body/Engine SHA journal changes are planned through reviewed plan/dry/apply/readback23 plus private Project4 direct253field comparison. Other20 complete rows/task bytes, all metadata/null hours/milestones/M0/gates, #3 Blocked and #20 original benchmark remain. Three public MIT repositories, private Project4; root is sole remote writer. Preserve four Engine dirty and four Samples untracked user files.

Local Windows26300 and a Windows loopback client to the retained WSL PostgreSQL fixture establish their scoped observations only. They do not establish native Windows database, full supported-host/provider, production acceptance, GC/scheduler cause or performance qualification. Fixture cleanup verifies owned container/image/name/volume/helpers and native listener state, retaining image/data/source/raw.

| Scope | Windows | WSL | Source inputs per host |
| --- | --- | --- | --- |
| Complete components | 1323 passed | 1320 passed | 144 |
| Generated HTTPS security | 651 passed | 651 passed | 85 |
| Actual PostgreSQL outbox | 132 passed | 132 passed | 96 |

Exact-revision push CI passed four Windows2025/Ubuntu24.04 jobs. Retained proof is metadata/steps only; provider proofs above are separate local executions. No billing/usage step was skipped.

[Public suitable raw/source archive](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/security-api/evidence/2026-11-21-total-drain-budget) contains 1008 files, all Git-index blobs equal reviewed bytes. SHA256SUMS digest `9342b413c80561011baf4432fb3d0a573237716e238d29e00a21a1c18a8a0649`. Explicit selection excludes private credentials, keys, binaries, SDK/cache/build/Git objects and inherited evidence. Bounded secret comparisons and actual postarchive SDK evidence-item exclusions pass; this is not a universal secret detector.

Reviewed body-only7/8/18 plan `dfad32cd10a5ad7bc2435dfb793c423472ebf40818d98c02066e5d040011a05a` passes dry/exact apply/readback23, direct Project4 253-field comparison and strict preservation of other20 complete rows/task bytes/all metadata/nullhours/#3/#20. Main branches are pushed in all three repositories, owned merged feature branches detached/deleted, raw worktrees retained. Exact owned fixture/helpers/listener stopped; image/data/volume retained. Final exact remote-head and user-file audit follows the Docs push without a Docs self-hash loop.
