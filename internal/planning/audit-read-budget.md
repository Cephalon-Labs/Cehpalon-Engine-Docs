# Optional cooperative audit read budget

Date2026-11-21; #18 with #7/#8 regressions. [Requirement](../requirements/2026-11-21-audit-read-budget.md), [ADR0051](../adr/ADR-0051-optional-audit-read-budget.md), [predeclared protocol](../validation/audit-read-budget.md), [consumer guide](../../public/guides/experimental-audit-trails.md).

## Behavior

Three change-audit readers gain project-selected ActivateWithBudget while retaining existing constructor/Activate/null behavior. Disabled or invalid configuration performs no provider-factory work. Per-call system timers and linked cancellation span source work, integrity validation, current-policy projection and successful completion guards. Original-caller cancellation precedes observed private expiry at primary classification; unrelated OCE and non-OCE failures retain their declared identities. Empty/null results receive configured completion vetoes. All checked tenant/resource/cursor/authority checks remain.

Uncooperative provider work is awaited and remains caller-owned; no hard deadline, rollback, continuous authority refresh or atomic network-delivery claim. Reader disposal owns only timer/link resources, not provider lifecycle or undisclosed callback work. Indexed storage still provides only exact lookup/resource history; legacy history is a separate port. One additive local typed generated history gateway intentionally changes the service registry fingerprint; the original five declarations and security0534 are preserved.

## Validation

Exact Engine `5184517a92a087abe4e0091d256142b6c35a2b39` and consumer source `1234ec9ab152bd7c1f03ec8da5c306d2b16abbe7` passed all six serial committed-source final lanes. Frozen actual source/runner/locks/templates/settings/declaration, old case prefixes and new48+24 cases, current/cross-host source maps and generated registry semantics pass independent review. Every preparation/SDK/runtime attempt is retained. Original timed benchmark not run or changed.

## Delivery boundary

Only #7/#8/#18 bodies and new full Engine SHA journals; reviewed plan/dry/exact apply/readback23/directProject253 and strict other20row/taskbyte/allmetadata/nullhour preservation. #3 remains Blocked, #20 entirely unchanged, M0/gates/original criteria retained. Three public MIT repositories/private Project4. Merge/push mains and delete only owned merged refs, preserve eight user files and all source/raw worktrees/objectstore. Cleanup exact owned fixture/helpers/native listener, retain data/image/volume. Final remote/user-file audit follows Docs push without a Docs self-hash loop.

## Retained preparation and development attempts

Engine Program and Samples README encoding preparation errors were caught before SDK and restored from exact HEAD bytes with only the declared ASCII hook/append. Failed preparation snapshots remain. Consumer dev01 stopped at compile with two CS1061 fixture calls to nonexistent TimeSpan.AddTicks; no provider or restart tests ran. Declaration02 froze only the same-value one-tick-over-limit expression correction before dev02. Complete dev02 passed244/0 and both final hosts passed244; failed01/frozen107inputs/declaration01 and corrected107inputs/bothdeclarations remain separately archived. No product API, timeout range, SQL, workload, concurrency, Pooling=false or benchmark gate changed.

| Scope | Windows | WSL | Source inputs per host |
| --- | --- | --- | --- |
| Complete Engine components | 1523 passed | 1520 passed | 147 |
| Generated HTTPS security | 651 passed | 651 passed | 85 |
| Actual PostgreSQL outbox/read budgets | 244 passed | 244 passed | 106 |

All four exact-revision Windows2025/Ubuntu24.04 Engine hosted jobs passed. Metadata/steps evidence is separate from local PostgreSQL consumer execution; no hosted PostgreSQL profile claim.

[Public suitable source/raw archive](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/security-api/evidence/2026-11-21-audit-read-budget) contains 1327 files. SHA256SUMS digest `6584e53c17ac92183f8f56bfde294aa178012a8b313c60dbbe7aa47941e49733`. All staged blobs equal reviewed bytes. Explicit selection excludes credentials, private fixture state, keys, binaries, SDK/cache/build and Git objects; bounded comparisons and actual SDK evidence-item exclusions pass, without universal secret detection claim.

Reviewed body-only7/8/18 plan `32b937ae5e3315b2c6a5150b9c0a90fa16d596c711acfd8ef75f58ced817af3c` passed dry/exact apply/readback23/directProject253 and strict other20row/taskbyte/allmetadata/nullhour preservation. Every new Engine SHA is journaled on the three scoped issues; Samples SHAs are technical provenance only. All three mains pushed; owned merged refs detached/deleted, eight user files/source/raw retained. Exact fixture/helpers/native listener stopped with data/image/volume retained; final remote/user-file audit follows Docs push without self-hash loop.
