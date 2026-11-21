# Optional indexed audit storage profile

Date2026-11-21. Tracking #18 with #7/#8 regressions. [Requirement](../requirements/2026-11-21-indexed-audit-storage.md), [ADR0050](../adr/ADR-0050-optional-indexed-audit-storage.md), [predeclared protocol](../validation/indexed-audit-storage.md), [guide](../../public/guides/experimental-audit-trails.md).

## Behavior and ownership

Provider-only continuation: unchanged Engine sink/lookup/resource-history ports and generated gateways compose an optional PostgreSQL indexed storage module. A real immutable Composition plan is compiled before its module factory, credential access and explicit CreateNew/OpenExisting initialization. Disabled/invalid configuration has zero module-owned work. ActivationLease owns provider lifetime; retained references reject new work after disposal, admitted work remains awaited/joined. No new Engine source/API/template/package or commit journal entry.

New versioned storage atomically derives and writes resource metadata plus bounded NUL-compatible TEXT payload from one record, with C-collated exact identity and a composite tenant/resource/receipt search index. Conditional replay accepts only identical payload/metadata; conflicts never overwrite visible history. Concurrent conflict has one visible winner. Duplicate MVCC/index/vacuum work is possible and unmeasured. Selected queries use actual SQL filters/keyset/limit lookahead and validate physical metadata against decoded receipt before reader policy projection.

Exact coherent pg_catalog checks require the declared ordinary persistent table, five non-null columns/types/C collations, expected PK and valid/ready B-tree key/index behavior without included payload, expressions/predicate/RLS/policies/usertriggers/rules/inheritance/generated behavior. OpenExisting is read-only and fails closed without auto-repair; validation is point-in-time, not continuous integrity attestation. CreateNew uses explicit fresh versioned storage, no legacy ALTER/backfill/dualwrite. Committed/unknown DDL is not claimed rolled back/deleted by client cleanup.

## Migration and evidence limits

Legacy/new histories remain distinct. Pending outbox records can be sent to selected new sink, while already acknowledged legacy records are not silently copied/replayed. Outbox delivered counts do not attest the selected destination. Existing lease fencing/ack uncertainty/current authorization and configured policy remain independent. This profile does not continuously scan unrelated corruption or promise snapshot chronology/tamper evidence.

The fixed4096-row default-planner EXPLAIN/pg_catalog observation is diagnostic. No index coercion, new latency threshold, timed speedup benchmark or production qualification. Storage/index-write costs and planner choices remain profile-specific. Existing Engine1475/1472 and four hosted jobs at unchanged d0d are reused baseline; no new indexed-profile hosted execution is claimed. New consumer local Windows/WSL proofs are separate; Windows client connects to WSL PostgreSQL through an owned loopback proxy.

## Validation

Unchanged Engine `d0d49c7eb47ae8fedc23743dfe76b359b677d796` and consumer source `58641dac065a3204f662d7bbd57c2dc59159bdc1` passed all four serial changed-consumer final lanes. Actual executing source/runner/locks/settings/declarations are frozen and retained; committed bytes and cross-host source/registry maps match. Existing188 provider cases and651 security cases remain;32 new indexed-provider cases pass. Independent source/raw review passes; original benchmark not run.

## Tracking and delivery

Reviewed only7/8/18 bodies/no new Engine journal entry, plan/dry/exact apply/readback23/directprivateProject4beforeafter253field/identity/null checks and strict other20row/taskbytes/allmetadata/milestone/nullhour preservation. #3 Blocked/#20/M0/gates/original benchmarks unchanged. Three public MIT repos/private Project4, main3 synchronization with Engine unchanged, detach/delete only owned merged refs, preserve source/raw/objectstore and fourEngine/fourSamples user files. Exact fixture/helper/native-port cleanup retains data/image/volume/raw; final remote-head audit follows Docs push without self-hash loop.

Pre-SDK catalog refinement03: PostgreSQL18 NOT NULL must be validated and enforced for every declared attribute, with exact local constraint ownership/inheritance shape; attnotnull alone is insufficient. Require the ordinary primary-key constraint to be NO INHERIT and ordinary NOT NULL constraints to have their actual PostgreSQL18 default inheritance semantics. Reject NOT VALID constraints, including on non-key columns, without repair. This source-review refinement precedes every SDK or database probe; retain declaration01 and separately freeze declaration02.

| Scope | Windows | WSL | Source inputs per host |
| --- | --- | --- | --- |
| Generated HTTPS security | 651 passed | 651 passed | 85 |
| Actual PostgreSQL outbox/indexed storage | 220 passed | 220 passed | 105 |

Engine1475Windows/1472WSL component checks and four hosted Windows2025/Ubuntu24.04 jobs at unchanged Engine d0d are reused baseline. New indexed-profile hosted execution is not claimed. Fixed4096-row EXPLAIN is a default-planner structural observation, not a timing benchmark or speedup claim.

[Public suitable raw/source archive](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/security-api/evidence/2026-11-21-indexed-storage) contains 668 files, with all index blobs equal reviewed bytes. SHA256SUMS digest `7ba639309058c08214351e07e16d75d520467392e221b488d89f6a8f93459ecb`. Explicit selection excludes credentials/private fixture state/keys/binaries/SDK/cache/build/Git objects/inherited evidence. Bounded publication comparisons and actual SDK evidence-item exclusions pass; this is not universal secret detection.

Reviewed body-only7/8/18 plan `cad11f413933597ec09a507e47ebc04c2c3197326ee9312c057a46fc56b74109` passes dry/exact apply/readback23/directProject253 and strict other20row/taskbyte/allmetadata/nullhour preservation. No Engine commit or new commit-journal entry. Samples/Docs main pushed; Engine main unchanged. Owned merged refs detached/deleted and raw retained. Exact fixture/helpers/listener stopped with data/image/volume retained; final remote-head/user-file audit follows Docs push without self-hash loop.
