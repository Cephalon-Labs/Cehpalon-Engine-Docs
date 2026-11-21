# Optional exact audit receipt lookup

Date2026-11-21. Tracking #18 with #7/#8 regressions. [Requirement](../requirements/2026-11-21-audit-receipt-lookup.md), [ADR0048](../adr/ADR-0048-exact-audit-receipt-lookup.md), [predeclared protocol](../validation/audit-receipt-lookup.md), [guide](../../public/guides/experimental-audit-trails.md).

## Behavior

A separate optional lookup port/facade reads a known nonempty receipt ID inside a checked audit-trail/tenant/read scope. It passes the original caller token and preserves provider error references. Null and positive results receive post-await and final guards. Returned tenant and receipt must both match before current configured policy projection. Disabled activation skips the factory. Existing history pagination, outbox/relay budgets, source interfaces, SQL/schema/packages/locks remain unchanged.

The immutable reader captures its selected policy; projects construct/configure another reader for a changed read policy. No receipt ID, DTO, cursor or metadata flag grants authority. Provider absence does not establish global existence, delivery health, never-committed data or durable snapshot freshness. A record can be pending outbox publication or retained away. No new timer, retry, endpoint, background work, pagination guarantee or retention control is installed.

The additive PostgreSQL adapter reads existing sink rows with parameterized tenant/receipt and a validated owned schema. A new generated typed/lazy LookupGateway has an explicit sample operation grant and fresh history scope. Its additional service registration is intentional; registration itself is not activation or authority. Security registration and old provider/store/SQL/test bodies remain intact.

## Validation

First focused attempt passes103trail (prior48+55new),212outbox and56status. All203 frozen/current/committed inputs match; original48 names/order/results and complete outbox/status results remain intact. Consumer development01 is retained as151/153main: prior129main and22/24lookup pass, restart3 not run. Two new checks expected exceptions while protected dispatch intentionally returns access.denied. Independent review confirms the fixture expectation mismatch.

Corrected development02 passes156 (153main+3restart; prior132+24new). Exact changes from the100 frozen01 inputs are LookupChecks assertions/evidence plus verifier observation-count12to15; Engine/host/provider/SQL/schema/packages and all24/full156 behavioral criteria remain. The corrected controls establish exact denial codes, zero unauthorized queries, withheld reader results and observed invalidity latch before fixture clock restore. All100 executing/frozen/committed02 inputs match with LF/no normalization exception. Retain failed01, successful02 and three declaration snapshots:01/02 precede their respective SDK runs;03 is explicitly after dev02 launch and corrects earlier prose that omitted the second already-reviewed/frozen verifier input change.

Exact Engine `505d7f0e08057a0a24debe092e9956fd534790d4` and consumer source `617e89e9e4713313e683cd50f08ae77d49b891fe` passed all six serial final lanes. Every actual executing input is frozen and retained; committed bytes and cross-host source/registry maps match. All original cases and locked packages remain. Independent source/raw review passes; no original benchmark was run.

## Tracking and limits

Only #7/#8/#18 bodies and full Engine SHA journals update using reviewed plan/dry/exact apply/readback23. Private Project4 gets direct before/after253 field/identity/null comparisons. Other20 entire rows/task bytes, all metadata, estimates/null actual hours, milestones/M0/gates, #3 Blocked and #20 original benchmark remain unchanged. Three public MIT repositories, private Project4; root sole remote writer, preserved four Engine dirty/four Samples untracked user files.

Windows26300 and Windows loopback-to-WSL PostgreSQL are local observations; WSL uses direct loopback. No native Windows DB, full supported-host/provider, actual IdP, snapshot, retention, performance or production qualification. Exact owned fixture/helpers/listener cleanup retains image/data/volume/raw. Final remote-head/main-only/user-file audit follows the Docs push without a Docs self-hash loop.

| Scope | Windows | WSL | Source inputs per host |
| --- | --- | --- | --- |
| Complete components | 1378 passed | 1375 passed | 145 |
| Generated HTTPS security | 651 passed | 651 passed | 85 |
| Actual PostgreSQL outbox/history | 156 passed | 156 passed | 99 |

Exact-revision CI passed all four Windows2025/Ubuntu24.04 jobs. Proof is metadata/steps only; local provider evidence above is separate. No billing/usage step was skipped.

[Public suitable raw/source archive](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/security-api/evidence/2026-11-21-audit-lookup) contains 1243 files, all Git-index blobs equal reviewed bytes. SHA256SUMS digest `063c048a74197dfccc8532f14ad77d1a1e7e70cc8c4741b058416cf23bdce3b8`. Explicit selection excludes private credentials/keys/binaries/SDK/cache/build/Git objects and inherited evidence. Bounded content comparisons and actual postarchive SDK evidence-item exclusions pass; no universal secret detection claim.

Reviewed body-only7/8/18 plan `97295fa0009f1316e906a60717a049e22b02b87f5494f58a2e7d4fe24086682c` passes dry/exact apply/readback23, direct Project4 253-field comparison and strict other20 complete row/task byte plus metadata/nullhours preservation. Main branches are pushed in three repos and owned merged feature refs detached/deleted; source/raw retained. Exact fixture/helpers/listener stopped while data/image/volume retained. Final remote-head/user-file audit follows Docs push without a self-hash loop.
