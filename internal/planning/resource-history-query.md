# Optional exact resource audit history

Date2026-11-21. Tracking #18 with #7/#8 regressions. [Requirement](../requirements/2026-11-21-resource-history-query.md), [ADR0049](../adr/ADR-0049-exact-resource-history-query.md), [predeclared protocol](../validation/resource-history-query.md), [guide](../../public/guides/experimental-audit-trails.md).

## Behavior

An optional source/reader selects one exact resource kind/id under existing checked tenant history permission. Immutable query/page/typed continuation DTOs carry bounded selection data; cursors are untrusted positions, not authority. Validate cursor binding before provider work and all page identities, strict canonical Guid-N order after input position, count/progress/next-last binding before policy projection. Caller/live scope checks apply before I/O, after await and before return, including empty pages. Disabled activation skips its factory; source failures/tokens stay original. No timer/retry/background/endpoint or old API change.

Receipt-key order is explicit. It does not establish chronology, commit order, a stable snapshot, permanent completeness or delivery health. Inserts before a bookmark may be missed, later positions can appear and deletion can remove rows/bookmarks. Page size can change; nonempty underfilled continuation is legal. Captured immutable policy requires reader reconfiguration for changed read policy. Resource selection does not grant entity read/write authority or broader history access.

## Provider refinement before SDK

Initial unexecuted JSONB filter source/declarations are retained. Existing well-formed audit Text includes NUL, stored escaped in TEXT; PostgreSQL JSONB and JSON processing can reject it. Refinement03 selects streaming existing TEXT through the established codec, exact managed Ordinal resource filtering and physical tenant/UUID keyset/order. Validate physical versus decoded keys, including malformed unrelated scanned payload. Matching and unrelated-before-target NUL fixtures round-trip through old AppendOnce/lookup and the new query. No regex extraction, old SQL/schema/index/package migration or wire-profile narrowing.

Retain at most limit+1 matching records plus current decoded bounded record. Total rows scanned, decoding, connection occupancy, elapsed time and all-layer buffering are unbounded by page count/unmeasured; disposal/drain is cooperative. Future indexed metadata profiles need separate storage/migration/performance evidence. New fifth lazy generated Core gateway uses an explicit sample grant/fresh tenant boundary; existing mutation fixtures retain Composition. No new Composition query module/transport endpoint claim.

## Validation

First focused attempt passes200trail (prior103+97new),212outbox and56status. All204 actual executing/frozen/committed inputs match with LF. Prior103 names/order/results and complete old outbox/status results remain unchanged. First consumer development attempt passes188/0 (185main+3restart; prior156+32new), all103 executing/frozen/committed inputs exact and102 verifier inputs its subset. All six changed files and generated service registry bytes match actual builds, security registry remains unchanged, and22 structured observations pass. No SDK failure or alternate run occurred.

All three declarations01(initial),02(error shape),03(TEXT/NUL provider refinement) precede the first SDK attempt and are retained with hashes, including twelve copied declaration files in the consumer freeze. The rejected JSONB adapter is preserved as unexecuted preparation, without treating it as a failed or passed workload. Provider/host code, old SQL/schema/lookup tests and packages outside the explicit additive query scope stay intact. Independent pre-SDK and development source/raw reviews pass.

Bookkeeping provenance: the first final driver writes to retained `rh-finrh-driver01` because a broad path-prefix replacement also changed the directory's spelling. Its executing source, frozen runner and all seventeen successful phase receipts remain untouched; export/monitoring point to the actual directory and no SDK repeat occurred. The future preparation helper is corrected. Tracking plan creation wrote a valid three-operation JSON before its cp1252 console summary failed on U+2264; retain that plan/error and use UTF8 for guarded dry/apply/check. Neither correction changes runtime inputs, benchmark criteria or issue-body bytes. Exact notes are retained in the evidence.

Exact Engine `d0d49c7eb47ae8fedc23743dfe76b359b677d796` and consumer source `6bfc43d407d94dac1d3c2dec7a2920f7e376d6e6` passed all six serial final lanes. Actual executing source/runner/locks/templates/settings are frozen and retained; committed bytes and cross-host source/registry maps match. Prior cases and packages remain. Independent source/raw review passes; no original benchmark was run.

## Tracking and limits

Reviewed only7/8/18 body/Engine SHA journals plan/dry/exact apply/readback23, direct private Project4before/after253field/identity/null checks and strict other20whole row/task byte/all metadata/milestone/nullhour preservation. #3 Blocked/#20 original benchmark/M0/gates unchanged. Three public MIT repos/private Project4. Main3 push, detach/delete only owned merged refs, retain source/raw/borrowed object store and four Engine/four Samples user files.

Windows26300 and Windows loopback-to-WSL PostgreSQL are local observations; WSL direct. No native Windows DB, real IdP, full supported-host/provider, snapshot, production or performance qualification. Exact owned fixture/helpers/native listener cleanup retains image/data/volume/raw. Final remote-head/user-file audit follows Docs push without a self-hash loop.

| Scope | Windows | WSL | Source inputs per host |
| --- | --- | --- | --- |
| Complete components | 1475 passed | 1472 passed | 146 |
| Generated HTTPS security | 651 passed | 651 passed | 85 |
| Actual PostgreSQL outbox/history | 188 passed | 188 passed | 102 |

Exact-revision CI passed all four Windows2025/Ubuntu24.04 jobs. Proof is metadata/steps only, separate from local provider evidence; no usage/billing skip.

[Public suitable raw/source archive](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/security-api/evidence/2026-11-21-resource-history) contains 1068 files, all index blobs equal reviewed bytes. SHA256SUMS digest `2234cea8a4c6194c99d4f1a9d085bcf48bd6af573c43edc907616b9ea220641f`. Private credentials/keys/binaries/SDK/cache/build/Git objects/inherited evidence excluded by explicit selection; bounded content comparisons and actual SDK evidence-item exclusions pass, without universal secret detection claim.

Reviewed body-only7/8/18 plan `ded39ee70a5af88854177f84591c490671264af707a02e378f2fb06b1342d87f` passes dry/exact apply/readback23/directProject253 and strict other20row/taskbyte/allmetadata/nullhour preservation. Main3 pushed, owned merged refs detached/deleted and raw retained. Exact fixture/helpers/listener stopped with data/image/volume retained; final remote-head/user-file audit follows Docs push without self-hash loop.
