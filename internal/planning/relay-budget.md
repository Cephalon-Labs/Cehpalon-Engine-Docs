# Optional cooperative outbox relay budget delivery

Date2026-11-21. Tracking #18 with #7/#8 regressions. [Requirement](../requirements/2026-11-21-relay-budget.md), [ADR0045](../adr/ADR-0045-cooperative-outbox-relay-budget.md), [frozen protocol and retained corrections](../validation/relay-budget.md), [consumer guide](../../public/guides/experimental-audit-trails.md).

## Behavior and source

Engine3eb2b0eb957304bae24a1ef749160b8dd159772f adds distinct `TenantChangeAuditOutboxRelay.ActivateWithBudget` and retains the original `Activate` signature. Null preserves legacy tokens/faults; Disabled skips all validation/factories. An enabled optional positive<=1minute system timer covers claim through final success validation. Claim/sink/ack receive linked cancellation; cleanup retains its independent5second token. Existing lease UTC/monotonic checks and configured fresh relay authority remain distinct from the I/O timer.

Configured observed caller cancellation takes precedence and retains its original token; private expiry becomes generic TimeoutException with trusted-host diagnostics. Other provider faults remain original. Assign a known late lease before rejecting so fenced release still runs; late null also rejects. Pre-handle failures cannot provide an Engine cleanup fence, so provider partial-acquisition recovery remains the source's responsibility. Once sink invocation starts, delivery may have happened; acknowledgement count and independent release faults remain available through the relay exception. A budget expiring during cleanup can withhold success after all acknowledgements. No abandoned work, hard-deadline promise, automatic retry, renewal, deadletter, dropped record, new listener or background worker.

Only existing Audit.cs changes runtime;44new component contracts use a dedicated testfile plus one Program hook. SDK11.0.100/runtime11.0.0, packages/locks/provider SQLschema and fixed17/32 scaffold input counts remain unchanged. Actual provider consumer continues to use the generated protected service/tenant gateway and Core/Composition integration. This is a project-selected optional helper, not a newly implemented scaffold/provider profile.

## Retained attempts

Focused01 passes113outbox=76prior+37new and56status. Focused02 adds7 test-only edge controls and passes120/56. Focused03 strengthens an existing uncooperative sink case using a held-after-expiry gate and finally join, then passes120/56; productAudit.cs bytes identical acrossall3. Current200inputs match final03 frozen copies; old freezes remain intact. Independent review finds no runtime blocker.

Consumer source-freeze second invocation rejects an occupied old01 directory with FileExistsError/WinError183 before SDK; no overwrite. Preserve the original fixed-path freezer/hash and exact rejection. Corrected helper requires explicit fresh output. Development01 passes80/81main (old34+23status and23/24new), then stops before restart: synchronous dispatcher cancellation escaped the fixture's capture. Independent review also separates actual relay error capture from the outer watchdog. Corrected source changes only those test controls; development02 passes81main+3restart=84, with original60 unchanged. All94 executing inputs/frozen copies and both generated registry hashes independently match. Wrapper/late-result cases are labeled; actual claim/ack tests execute unchanged provider SQL under controlled table/row locks, observe exact tagged backend Lock wait before expiry, then join/reconcile/quiesce before reuse/replay. No favorable performance selection or product/policy weakening.

## Final results

| Scope | Windows | WSL | Limits |
| --- | --- | --- | --- |
| Clean committed complete components | 1231passed/0failed | 1228passed/0failed | Includes original outbox76+new44 and status56 |
| Generated HTTPS security consumer | 651passed/0failed | 651passed/0failed | Original651 cases, local synthetic trust/fresh tenant fixtures |
| Actual PostgreSQL transaction/outbox/status/budget consumer | 84passed/0failed | 84passed/0failed | Prior60+new24; existing schema/driver/owned fixture |

Cross-host source and emitted registry inventories, compiler/runtime dependency checks, exact-revision CI and public SHA/index checks are recorded with final evidence. The root WSL consumer is a realGit repository borrowing exact committed objects from the retained primary store via read-only Linux-path alternates, outside Engine ancestor package policy; it is not an independent archival clone. No source/SDK/restore flags or original performance protocol change.

## Delivery boundaries

Public suitable source/raw archive: [Samples relay budget evidence](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/security-api/evidence/2026-11-21-relay-budget). Retain all failed/partial/focused/development/final source, settings and raw, including direct runners and watchdog corrections. Exclude private credentials/keys/tokens, compiled outputs/caches/SDK binaries, inherited evidence and machine-private data. Publish SHA256SUMS and verify every Git-index blob; ensure public evidence is excluded from actual SDK items.

Only #7/#8/#18 bodies and Engine-only journals update. Keep all native/Project metadata, null hours, maturity and gates unchanged, plus #3/#20 complete rows/taskbytes and other20 rows/milestones. Reviewed plan/dryrun/exacthashapply/readback23 and independent Project4 before/after23cardsx11fields=253 compare identities/titles/fields/nulls. All three repos remain publicMIT/privateProject4. Push3main, delete owned merged branches and retain worktrees/raw and the user's original file hashes.

Local Windows build26300 and Windows-loopback-to-WSL PostgreSQL remain observational. The helper's cooperation, callback/fence checks and tested driver behavior do not prove forced cancellation, physical causality, power-loss/nativeWindows/all-provider durability, production or original benchmark qualification. #3 remains Blocked/M0; #20 original protocol/gates unchanged. Owned fixture cleanup stops exact owned resources only and retains data/image/volume.

Exact Engine CI [44871739876](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44871739876) and [44871740016](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44871740016) pass all4Windows2025/Ubuntu24.04 jobs/steps. Retained CI proof is latest-attempt metadata only, without artifact/log download; no usage/billing step skipped. Hosted no-server platform smoke is separate from actual local PostgreSQL and full supported-host/provider gates.

Final Samplesmain20a354cc846e2666f4771943a618ed0d69e5728a contains1615publicarchivefiles including SHA256SUMS; all1615 Git-index blobs match the reviewed bytes. SHA256SUMS digest9bc67f8d24ee9ba865fa15f14c13d258eb3f2a910fa124b2373086d913af7b09. Content/allowlist review finds no private fixture secret/JWT/privatePEM/binary material in the selected archive. Post-archive SDK items are security19Compile/0Content/2None and provider6/0/2, zero evidence items. Only security's extra None is the preserved user launchSettings; provider includes the new test source. Owned fixture/listener/helpers stop with image/data/volume/raw retained. Owned merged branches are removed after detaching source worktrees. UserfourEngineedited/fourSamplesuntracked hashes remain unchanged. Reviewed body-only plan60b7608db836c5b43784d98537341d2c210cf94c8de19d2a7482c5e4baba355f and independent23/253readbacks pass; public evidence/delivery records include the exact limits.
