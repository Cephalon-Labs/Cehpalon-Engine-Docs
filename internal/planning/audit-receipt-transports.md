# Optional protected audit receipt lookup transports

Date2026-11-21; #18 with #7/#8 regressions. [Requirement](../requirements/2026-11-21-audit-receipt-transports.md), [ADR0052](../adr/ADR-0052-protected-audit-receipt-transports.md), [frozen protocol](../validation/audit-receipt-transports.md), [consumer guide](../../public/guides/experimental-audit-trails.md).

## Selected behavior

A dedicated Samples indexed receipt host selects HTTPS HTTP POST /audit/receipts/lookup and/or GraphQL trailReceipt. Immutable Composition precedes owned security/source/configuration/credential callbacks; disabled selection skips owned work and invalid security dependencies reject before callbacks. Host-owned storage is constructed then OpenExisting-validated; provisioning is separate. Request lookup SQL counters are distinguished from startup inventory work.

A request-owned typed transport bridge maps primitive wire data to the existing LookupRequest/LookupResult generated Core signature, invoking fresh validated JWT identity plus project membership/resource/RBAC-ABAC checks. Existing reader/budget and captured current-policy projection run before one shared wire mapper. Resource kind/provenance and nullable absence remain explicit. No fixture-service authority, new operation declaration, Engine API, legacy host edit, new endpoint in existing hosts or package change.

Shutdown closes admission atomically and fully joins admitted request/dispatch work before storage disposal, even on stop failure; client abort is not server completion. Reader budgets exclude serialization/network flush. Local signed-token and indexed PostgreSQL proof do not establish external IdP, native Windows DB, all-provider, production or performance qualification. Existing Engine1523Windows/1520WSL and four hosted jobs at unchanged5184517 are reused baseline, not new host execution. M0/original benchmark gates remain.

## Verification

Unchanged Engine `5184517a92a087abe4e0091d256142b6c35a2b39` and consumer source `fd6afaad591aeac7eabf6a2cebebd2e1e4fb1118` passed all four serial committed-source consumer lanes. Independent source/raw review verifies original244/651 prefixes, new28 actual wire cases, frozen source/scripts/locks/settings/declarations, current/cross-host source maps and unchanged generated registries. Actual SQL/token/server-completion/shutdown controls pass; retained failed preparations and attempts remain explicit. Original timed benchmark not run or changed.

## Delivery

Body-only7/8/18 with no Engine commit/journal addition, reviewed plan/dry/exact apply/readback23/directProject253 and strict other20row/taskbyte/allmetadata/nullhour checks. #3 Blocked/#20 entire row/original criteria retained. Public suitable evidence/SHA256SUMS/index-byte/SDK evidence exclusions, main3 pushed with Engine unchanged, only owned merged refs removed while raw/worktrees/objects/eight user files retained. Exact owned fixture/helpers/native listener cleanup retains data/image/volume; final remote/user-file audit follows Docs push without self-hash loop.

## Retained preparation and development

Host source-only review narrowed the post-provider hook to a cancellation token without a raw pre-policy record; both87a3429/ac7b3cb snapshots remain. Before SDK, the scheduled-worker fixture was corrected to cancel and unconditionally join its aggregate in finally. First consumer dev01 stopped at compile with five nullable-flow diagnostics; no provider/restart tests ran. Declaration02 froze only five null-forgiving annotations at already activated/asserted source sites. Corrected dev02 passed272/0, with all109 inputs/bothdeclarations retained. No emitted runtime logic, host contract, SQL, workload, concurrency, Pooling=false or gate changed in that compile correction. All final consumer lanes use the committed corrected source.

| Scope | Windows | WSL | Source inputs per host |
| --- | --- | --- | --- |
| Existing generated HTTPS security | 651 passed | 651 passed | 85 |
| PostgreSQL outbox and receipt transports | 272 passed | 272 passed | 108 |

Engine1523Windows/1520WSL components and four hosted Windows2025/Ubuntu24.04 jobs at unchanged5184517 are reused baseline. New receipt-host hosted execution, native Windows PostgreSQL, external IdP and performance/production qualification are not claimed. Client abort alone is not server completion; positive joined server/backend controls and held work are separate from reader budget and wire flush.

[Public suitable source/raw archive](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/security-api/evidence/2026-11-21-receipt-transport) contains 922 files. SHA256SUMS digest `0972775fd73b20c4d2f86ab886ebd768ae09e9a9cfc1f1825046f616b159b9e2`. All staged blobs equal reviewed bytes. Explicit selection excludes credentials/private fixture state/keys/binaries/SDK/cache/build/Git objects and inherited evidence. Bounded comparisons and actual SDK evidence-item exclusions pass; no universal secret-detection claim.

Reviewed body-only7/8/18 plan `ca2f7453edf46491ffd9b18cbfb41db3412500db40aad56a7148c292fd186a1a` passed dry/exact apply/readback23/directProject253 and strict other20row/taskbyte/allmetadata/nullhour checks. Engine unchanged with no new journal entry. Three mains synchronized; only owned merged refs removed with source/raw/worktrees/objectstore/eight user files retained. Exact fixture/helpers/native listener stopped with data/image/volume retained; final remote/user-file audit follows Docs push without self-hash loop.
