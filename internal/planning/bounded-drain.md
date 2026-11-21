# Bounded manual outbox delivery and progress evidence

Date2026-11-21. Tracking #18 with #7/#8 regressions. [Requirement](../requirements/2026-11-21-bounded-drain.md), [ADR0046](../adr/ADR-0046-bounded-outbox-drain.md), [predeclared protocol](../validation/bounded-drain.md), [guide](../../public/guides/experimental-audit-trails.md).

## Behavior

Engine d3630bd3448df1d59561d233dde9bfb094213076 adds DrainAsync to the existing relay, with caps16batches/2048acknowledgements/128perbatch. Positive underfilled batches continue. Zero progress, record limit or batch limit returns immutable tenant-bound observations, with NoProgress/RecordLimit/BatchLimit precedence. Zero is not proof of an empty backlog: SKIP LOCKED, active leases and concurrent writers remain possible. No status/history query or extra inspect permission is added.

One newly authorized operation owns the call; existing live scope/caller checks run between batches and before returning. They do not re-resolve identity sources for every batch. Existing configured work timeout remains per batch, with no overall timer or elapsed-time promise. Existing APIs and their single-batch token/fault behavior remain; ordinary RelayAsync creates no drain ledger. No provider/schema/package/lock or fixed17/32 scaffold-count change.

The first failure stops further calls. A success is counted before a subsequent outer scope/cancellation check, and partial failure retains completed/current acknowledgements, batch counts and possible delivery. The original child exception object remains PrimaryFailure and InnerException. Public exception type is insufficient as provenance: a provider can rethrow a prior RelayException from another invocation/tenant. Private per-call ledger plus exact newly emitted terminal-failure identity prevents those old totals being borrowed. A foreign error thrown during this invocation's sink is nested inside this invocation's owned relay error, preserving only current progress. No outer retry/release is added. Failure does not imply rollback, and counts are acknowledgement observations rather than unique business effects.

Durable deferral/quarantine/poison recovery is deliberately a separate scheduling profile: due-time eligibility affects current status and durable storage contracts. This helper bounds manual progress and fails fast, without solving poison starvation.

## Source and preparation

Runtime stays in existing Audit.cs with a private relay core retaining original public signatures. New component testfile/hook adds44 cases to prior120. Sole focused01 passes164outbox/56status, all201current/frozen inputs exact at commit; pre-SDK review strengthens watchdog fixture cleanup before first execution, not an extra/favorable rerun. Original120 names/order/results and old budget test bytes remain unchanged. Component coverage includes limits/underfill/zero,8 prior-tenant/call error provenance cases,2 outer-guard captured errors, success-before-guard accounting, partial/cleanup/replay and per-batch budgets.

The separate consumer adds a generated protected DrainGateway and explicit operation grant. Its service registry changes intentionally from the earlier relay/status-only registry; registration presence is not activation or authority. Original security registry and old operations/provider SQL/schema remain. Source and all failures/preparations are frozen and retained before every SDK attempt.

## Final matrix

| Scope | Windows | WSL | Boundary |
| --- | --- | --- | --- |
| Complete committed components | 1275passed/0failed | 1272passed/0failed | Prior1231/1228 plus44new contracts |
| Existing generated HTTPS security | 651passed/0failed | 651passed/0failed | Original651 cases |
| Actual PostgreSQL outbox/status/budget/drain | 108passed/0failed | 108passed/0failed | Prior84 plus new drain cases; same owned fixture |

Final results/source/registries, exact-revision CI, SHA256SUMS/index checks and SDK evidence exclusions are recorded in delivery artifacts. Public suitable source/raw: [Samples bounded drain evidence](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/security-api/evidence/2026-11-21-bounded-drain). Exclude private credentials/keys/SDK/build/cache/gitobjects/inherited evidence. Retain all raw/worktrees and primary borrowed object storage; WSL source uses explicitLF alternate metadata outside Engine ancestor policy and is not an independent archive clone.

## Tracking and limits

Only #7/#8/#18 body/journal updates; new Engine SHA only in journals. Other20 complete rows/taskbytes including #3Blocked/#20, all native/Projectmetadata/nullhours/milestones/M0/gates and original benchmark remain unchanged. Reviewed plan/dryrun/exacthashapply/readback23 and direct privateProject4beforeafter23x11=253field/identity/null equalities. ThreepublicMITrepos/privateProject4; push3main/delete owned merged branches, retain user4editedEngine/4untrackedSamples hashes.

Local Windows26300, loopback-to-WSL PostgreSQL and scoped functional tests do not certify nativeWindowsDB, fullsupported-host/provider/production or original performance gates. No speedup/GC/scheduler cause or universal Engine maturity claim. #3 remains Blocked/M0. Owned fixture cleanup verifies exact ID/image/name/volume/helper ownership before stop and retains image/data/raw.

First rootfinaldriver passes all6serial lanes at exact d363/87a21 committed LF source, with143component/85security/95provider input maps identical acrosshosts. Compilerfixture/rawregistry/Core-only runtime graph pass; service6d35eb73f43799c83ffad87ad35b6bf49845249c66162bb84b8c4f9dadca1895/security0534d97c0deba2f33744091b828da6a8a4e375d46c44ef2ca938f2088f148489 match actual emitted sources, no Roslyn runtime leak. Allbuilds lockedRelease/warnaserror0warnings/errors.

Exact-revision CI [44876270089](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44876270089) and [44876270126](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44876270126) pass all4Windows2025/Ubuntu24.04 jobs/steps. RetainedCI proof is metadata-only/noartifactdownload; no usage/billing skip. Full supported-host/provider gates remain separate.

Final Samplesmain90751e377b2949d1925807f4cae47179fa577892 publishes1198evidencefiles including SHA256SUMS; all1198 Git-index blobs match reviewed bytes. SHA256SUMSdigest a184617f723e89825436de7c436dbd337316c09470baf8eca608504accd30f74. Bounded content/selection review finds no private fixture credential/JWT/PEM/binary material in the exported set. Actual postarchive SDK items are security19Compile/0Content/2None and provider8/0/2, zero evidence items; security's extra None is the preserved user launchSettings. Fresh bounded-drain cleanup receipt8b618dae87e1ea28be600a6d1c8fae9165f2210b5f9810283752f688d33bee1f verifies exact owned resources/listener55053 stopped with data/image/volume retained. Owned merged branches deleted after detaching retained worktrees. Reviewed body-only7/8/18 plan9c9f48e3a393ed65cb6e884c0927b91aa94e1d69ed5934660f0f07648c29069a and23/253readbacks pass; all protected rows/metadata/user hashes remain. Final Docspush follows without selfhashloop.
