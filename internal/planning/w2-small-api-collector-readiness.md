# Small API collector readiness and complete canonical04

2026-10-28–29 (Asia/Bangkok). **Implementation, validation and the complete original benchmark finished. Original numerical startup/idle/main/CV gates pass in the declared observational profile. All12diagnostics actually ran. Reference qualification, #3 and the full #9/#11 gates remain Blocked/M0.**

Canonical04 ran **2026-10-28T14:02:15.698233+00:00–2026-10-28T17:35:39.413941+00:00**, all120fresh startup launches,20idle processes/1200RSS samples,20main runs and12diagnostic runs. Main3,600,000 plus diagnostic1,872,000 actual measured requests = **5,472,000 correct, zero errors/drops/timeouts/lost acknowledged writes**. These counts exclude preparation, warmup, planned-but-unexecuted manifest entries and the separately declared probes. Collection exit0 alone is not the proof; read the [independent raw audit](../evidence/small-api-collector/results/raw-audit/audit-final.md).

## Change and frozen provenance

[ADR0011](../adr/ADR-0011-small-api-collector-connection-readiness.md) froze the experiment before timing. Samples compiled source is `a3bd8b5c5747440c81124774ac10b6451d88ff82`; Engine remains `6804271d429106864e01e4ec546a41dff771f84b`. Only collector, tooling and documentation changed. Portable Engine/business handlers, codecs, typed operations, original payloads/schedules/rates/caps/deadlines/budgets remain unchanged. SDK/runtime remain11.0.100-rc.3.26522.148 /11.0.0-rc.3.26522.148; no new package, R2R or runtime knob.

The collector now separates control and load pools. Two verified control reads precede128read-only HTTP/1.1 load responses held unread simultaneously. Require128distinct first-use TLS connection identities, then release one barrier and validate every nonempty body. One30s deadline covers preparation; failed holds cancel/join/dispose before a structured nonzero failure. Phase TLS/client history and all observed rows survive managed preflight/phase rejection. The controller requires complete readiness, clocks, raw-file presence and exact failure stage/counts/no-later-phase evidence; exit1 is the only recognized managed preflight rejection. TLS1.3/custom-root/hostname verification and the original128outstanding/1s scheduled request deadline remain.

The128live-response claim applies at the barrier. Later cumulative TLS histories do not count currently live sockets. Handshake timestamps are after TLS negotiation, not TCP starts. GC/thread-pool counters are phase-boundary aggregates; they do not localize a GC cause. Abrupt process/host loss can still lose the in-memory phase and invalidates it.

The [independent host/fairness audit](../evidence/small-api-collector/results/canonical04-host-fairness-review.md) deduplicates physical driver connections by output directory plus connectionId: **6874actualTLS1.3/HTTP1.1/AES256GCM connections**, comprising6790LOAD and84CONTROL. Preparation-only129×52=6708 does not count134newLOAD connections during entered phases or32newCONTROL handshakes inside completion-metrics requests. Thus allocation/CPU brackets include matching nonzero control instrumentation; measured request latency and client-after snapshots stop before those post-join control requests. The172controller first-response handshakes are a separate scope. This evidence does not turn cumulative identities into later live-socket counts.

Fresh native app/cwd is `/home/tom/.local/share/cehpalon-benchmark-deployment/collector-20261028/app-final-02`;67files/23,281,577bytes match the clean Linux02 artifact, assembly SHA256 `742451b86f81c439938d93aad19a0f568133fe9ff2910bae4458f6633cdcfdd4`. Native SDK4178regularfiles/549,400,671bytes plus1668symlinks were independently rechecked before timing. All15build inputs/host match Git blobs, three actual generated catalog registrations compile, and runtime graphs exclude Roslyn/CodeGeneration. The raw audit verifies all109frozen source hashes and actual loaded-runtime paths. Startup trace was off; key import/full10kreadiness hash/first verified response remain inside the existing clock.

## Validation, including retained negatives

- Offline collector proof10/10, shared metadata guards29/29 on Windows/Linux, canonical failure-classifier checks16/16 and five independent actual TLS fault fixtures pass. Fault fixtures cover ConnectionClose, empty/invalid body, a stalled30s header deadline, and128valid holds followed by4000HTTP503 offered failures. All started requests joined; failure rows/TLS/client/stage reports remain; warmup/measurement were skipped. These are robustness fixtures, not production capacity tests.
- **Windows01 failed one case:** baseline HTTP409 entered the delayed handler0.3382ms after abort. ACK0.5528ms/no mutation/cleanup do not satisfy the required in-flight condition. Linux01 passed. Root initially ran both hosts concurrently; interference is plausible, not established. Both complete01 attempts remain retained.
- Before another validation, ADR0011 froze exactly one entire sequential02 matrix, Windows then Linux, unchanged source/50ms abort/100ms ACK gate and no competing owned work. Both passed4000cases each, including400cancellations,120same-process host cycles and20kAPI-only exercise/host. Maximum ACK Windows1.2032ms/Linux1.330781ms raw; maximum shutdown6.5286/1.6362ms. No favorable individual-case replacement. [Detailed precanonical audit](../evidence/small-api-collector/preflight/sequential02-precanonical-audit.md).
- Connection diagnostic01 completed12/12fresh-server probes13:58:05–14:00:44UTC:48000actualoffers, allcorrect, zeroerrors/drops,130verified reads and128distinct held load TLS connections each. Full360kplanned manifests were generated per invocation (4,320,000entries total) to preserve canonical preconditioning, but only the4000prefix actually executed. No warmup/measured phase ran. [Probe summary](../evidence/small-api-collector/connection-probes/summary.json).

## Startup and idle

| Transport | Baseline p95 ms | Engine p95 ms | Original numeric gate |
| --- | ---: | ---: | --- |
|http|401.814949|417.954793|PASS|
|graphql|844.554428|863.721846|PASS|

Thirty observations per variant/transport, all retained. Both absolute1000ms and Engine-extra150ms bounds pass. These are fresh processes under observed OS caches, not machine-cold boots.

| Transport | Pair | Order | Baseline median MiB | Engine median MiB | Original numeric gate |
| --- | ---: | --- | ---: | ---: | --- |
|http|1|BE|144.012|147.004|PASS|
|http|2|EB|144.012|145.211|PASS|
|http|3|BE|141.277|147.902|PASS|
|http|4|EB|141.867|146.727|PASS|
|http|5|BE|143.082|139.844|PASS|
|graphql|1|BE|160.754|163.906|PASS|
|graphql|2|EB|161.719|157.789|PASS|
|graphql|3|BE|166.723|161.551|PASS|
|graphql|4|EB|164.910|163.852|PASS|
|graphql|5|BE|163.422|164.926|PASS|

All20processes have60RSS samples after the unchanged60s warmup/120s settle. All absolute256MiB and Engine-minus-baseline16MiB gates pass. Same-binary/package/scaffolding RSS compares activation/dispatch paths, not a stripped minimum Engine-free distribution.

## Main1000/s — all observations retained

| Lane | All five p95 observations ms | Population CV | Original numeric gate |
| --- | --- | ---: | --- |
|http/baseline|0.310688, 0.307513, 0.319817, 0.284578, 0.315258|3.975222%|PASS|
|http/engine|0.312662, 0.293807, 0.318286, 0.319622, 0.320555|3.186566%|PASS|
|graphql/baseline|0.379032, 0.389071, 0.394672, 0.388500, 0.393212|1.405936%|PASS|
|graphql/engine|0.393223, 0.416120, 0.358363, 0.390057, 0.397033|4.769352%|PASS|

All four CVs are below the unchanged10% rule. No latency floor, outlier filtering, best-run selection or lower offered rate. All10matched pairs meet p95≤20ms/p99≤50ms, relative p95≤baseline+max(1ms,15%), allocation≤baseline+1KiB/request, correctness and drain gates.

| Transport | Pair/order | Baseline p95 ms | Engine p95 ms | p99 B/E ms | Approx allocated B/E bytes/offer | Numeric gate |
| --- | --- | ---: | ---: | ---: | ---: | --- |
|http|1/BE|0.310688|0.312662|0.444001/0.446033|21184.148/21063.869|PASS|
|http|2/EB|0.307513|0.293807|0.439670/0.460936|21183.654/21063.660|PASS|
|http|3/BE|0.319817|0.318286|0.450164/0.452631|21184.425/21063.700|PASS|
|http|4/EB|0.284578|0.319622|0.440939/0.454539|21183.612/21063.607|PASS|
|http|5/BE|0.315258|0.320555|0.446937/0.459275|21183.557/21063.772|PASS|
|graphql|1/BE|0.379032|0.393223|0.524989/0.549099|18071.253/18334.475|PASS|
|graphql|2/EB|0.389071|0.416120|0.538087/0.578903|18548.264/18334.895|PASS|
|graphql|3/BE|0.394672|0.358363|0.535012/0.527894|18549.046/18068.171|PASS|
|graphql|4/EB|0.388500|0.390057|0.539081/0.536304|18548.557/18111.301|PASS|
|graphql|5/BE|0.393212|0.397033|0.539704/0.551996|18548.221/18333.882|PASS|

## Comparison with complete canonical03

| Lane | Mean run-p95 03 ms | Mean run-p95 04 ms | CV03 | CV04 |
| --- | ---: | ---: | ---: | ---: |
|http/baseline|0.324863|0.307571|2.342875%|3.975222%|
|http/engine|0.327445|0.312986|1.907502%|3.186566%|
|graphql/baseline|0.415460|0.388897|5.301286%|1.405936%|
|graphql/engine|0.402594|0.390959|3.261601%|4.769352%|

Mean run-p95 values are lower in04, but HTTP baseline/Engine and GraphQL Engine CVs are higher. In particular Engine GraphQL CV increases3.261601%→4.769352%, while remaining valid. Startup observations are also lower. **Do not claim all-metric improvement or an isolated Engine-code speedup:** Engine did not change, collector pool topology/preparation changed, and the shared host is nonreserved.

Canonical03's HTTP Engine2000/s preflight37drops/4000 remains failed, with no warmup/measured interval. Its initial4TLS connections versus baseline128 did not prove equal readiness; failed-phase TLS events were missing. Successful04 does not reconstruct those missing events, establish a single cause or an intrinsic capacity ceiling.

## Separate diagnostics100/500/2000

| Transport | Rate/s | Order | p95 B/E ms | p99 B/E ms | Actual outcome |
| --- | ---: | --- | ---: | ---: | --- |
|http|100|BE|3.931054/3.145660|4.148639/3.367485|Both timed, correct|
|http|500|EB|1.687883/2.668612|1.885272/2.851303|Both timed, correct|
|http|2000|BE|0.289883/0.279239|0.416364/0.414712|Both timed, correct|
|graphql|100|BE|3.252152/4.089722|4.721004/4.327828|Both timed, correct|
|graphql|500|EB|2.797778/3.046788|3.036599/3.317584|Both timed, correct|
|graphql|2000|BE|0.320494/0.348780|0.501047/0.487655|Both timed, correct|

All12actualtimed runs have correct state, no errors/drops, valid offered work and successful shutdown. Each uses60s warmup/180s measure. These rates have no acceptance latency/allocation budget and never replace1000/s. In particular HTTP Engine2000/s completed360000measured correct offers in04; this is a bounded fixture observation, not universal sustained-capacity or production qualification.

## Audit, retention and remaining gates

Independent raw audit streams188gzip files/8,596,800phase observations/6,672,000planned manifest entries. It regenerates136complete state snapshots (84driver+52finalserver), checks52physical readiness barriers,136phase TLS/client accounting records,32metrics-before-persistence brackets,172identities/runtime mappings/shutdowns,86pair orders and1200RSS samples. Unexpected discrepancies0. All raw source/row/manifest checks retain all observations.

Full raw bytes and both01/02validation matrices, probes and fault/offline proofs are retained in private Samples `small-api-benchmark/evidence/2026-10-28-collector/`; the execution-retention manifest records2640files/1,335,210,272bytes, maximum27,494,953bytes and1169excluded compiled-artifact files. Private fixtures/keys/dumps are excluded; native originals and agent worktrees remain. The immutable raw link and hash are in [raw-evidence-link.json](../evidence/small-api-collector/results/raw-evidence-link.json). Later final audit files are retained in Docs alongside the raw audit.

After timing, a Windows UNC audit reader failed with transport semaphore/invalid-argument errors. Read-only audits switched to native WSL paths; no measurement was repeated or rewritten. The task-owned Windows sleep guard released successfully and no persistent power plan changed. Final host/runtime and probe/functional closure audits are retained alongside the raw audit.

The [independent closure audit](../evidence/small-api-collector/results/closure-audit/closure-audit04.md) separately streams all48000probe rows/4.32Mplanned entries, replays all12full10kfinal states, verifies130prep/128heldLOAD/129scopedTLS per probe and no newTLS during those2s preflights, and rechecks30frozen build inputs/42conformanceJSONhashes. It preserves Windows01, canonical03 and an initial audit-only expected-label typo corrected from frozen Domain.cs; no workload rerun or source change followed that audit correction. Raw data, successful and failed audit attempts remain retained.

Proof limits: full response bodies are not all retained; runtime business validation and state assertions complement offline raw checks. API-exercise totals derive from deterministic loops/completed checks, not20kretained response rows. TLS history is not later socket liveness; aggregate GC/pool snapshots are not event-level causes. Source/artifact hashes are provenance consistency, not independent reproducible-build attestation. The public10kfixture does not replace protected20ktenant/IdP/provider tests. Unchanged Engine347/protected40tests were not rerun in this wave.

Shared WSL affinity does not establish dedicated2vCPU/2GiB or native OS deployment. Current Windows26H2 is observational and does not clear listed-supported-Windows #3. Existing Engine6804 CI runs40622737320/40622737252 still show four rejected jobs/zero steps due the retained payments/spending block: Blocked, not code failure or CI pass; no rerun or billing change. All three repositories remain private MIT. Existing #9/#11 stay OPEN/Blocked/M0 with null actual person-hours; only their bounded evidence bodies are synchronized through reviewed plan/dry-run/exact-hash apply/readback. #3 body/editable fields must remain unchanged.
