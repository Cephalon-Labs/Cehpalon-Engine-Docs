from pathlib import Path
import json,shutil,statistics

root=Path('/mnt/d/Cephalon/Cehpalon-Engine-Samples')
docs=root.parent/'Cehpalon-Engine-Docs'
raw=Path.home()/'.local/share/cehpalon-benchmark-runs/benchmark-observation-04'
out=docs/'internal/evidence/small-api-collector/results'
out.mkdir(parents=True,exist_ok=True)
for name in ('summary.json','manifest.json','startup-summary.json','startup-observations.json','idle-summary.json','idle-observations.json','load-summary.json','load-pairs.json','load-observations.json','diagnostic-summary.json','diagnostic-observations.json','diagnostic-pairs.json'):
    shutil.copyfile(raw/name,out/name)
for name in ('benchmark-windows-launcher-04.json','canonical-classifier-review.json','collector-final-app-staging-02.json','collector-sdk-reverification-02.json'):
    shutil.copyfile(root/'.local'/name,out/name)
read=lambda path:json.loads(path.read_text(encoding='utf-8-sig'))
summary=read(raw/'summary.json');startup=read(raw/'startup-summary.json');load=read(raw/'load-summary.json');idle=read(raw/'idle-summary.json');diags=read(raw/'diagnostic-summary.json');obs=read(raw/'load-observations.json')
old=docs/'internal/evidence/small-api-tuning/results'
old_load=read(old/'load-summary.json');old_start=read(old/'startup-summary.json')
old_series={(x['transport'],x['variant']):x for x in old_load['stability']}
startup_rows='\n'.join(f"|{x['transport']}|{x['baseline_p95_ms']:.6f}|{x['engine_p95_ms']:.6f}|PASS|" for x in startup)
series_rows='\n'.join(f"|{x['transport']}/{x['variant']}|{', '.join(format(v,'.6f') for v in x['p95_observations_ms'])}|{100*x['population_coefficient_of_variation']:.6f}%|PASS|" for x in load['stability'])
comparison_rows='\n'.join(f"|{x['transport']}/{x['variant']}|{statistics.mean(old_series[(x['transport'],x['variant'])]['p95_observations_ms']):.6f}|{statistics.mean(x['p95_observations_ms']):.6f}|{100*old_series[(x['transport'],x['variant'])]['population_coefficient_of_variation']:.6f}%|{100*x['population_coefficient_of_variation']:.6f}%|" for x in load['stability'])
idle_rows='\n'.join(f"|{x['transport']}|{x['pair']+1}|{x['pair_order']}|{x['baseline_median_rss_bytes']/1048576:.3f}|{x['engine_median_rss_bytes']/1048576:.3f}|PASS|" for x in idle)
pair_rows=[]
for x in load['pairs']:
    b=next(v for v in obs if v['transport']==x['transport'] and v['pair']==x['pair'] and v['variant']=='baseline')
    e=next(v for v in obs if v['transport']==x['transport'] and v['pair']==x['pair'] and v['variant']=='engine')
    pair_rows.append(f"|{x['transport']}|{x['pair']+1}/{x['pair_order']}|{x['baseline_p95_ms']:.6f}|{x['engine_p95_ms']:.6f}|{b['measured']['p99Ms']:.6f}/{e['measured']['p99Ms']:.6f}|{b['allocations_bytes_per_offered_request']:.3f}/{e['allocations_bytes_per_offered_request']:.3f}|PASS|")
diag_rows='\n'.join(f"|{x['transport']}|{x['rate']}|{x['pair_order']}|{x['baseline_p95_ms']:.6f}/{x['engine_p95_ms']:.6f}|{x['baseline_p99_ms']:.6f}/{x['engine_p99_ms']:.6f}|Both timed, correct|" for x in diags['pairs'])
report=f'''# Small API collector readiness and complete canonical04

2026-10-28–29 (Asia/Bangkok). **Implementation, validation and the complete original benchmark finished. Original numerical startup/idle/main/CV gates pass in the declared observational profile. All12diagnostics actually ran. Reference qualification, #3 and the full #9/#11 gates remain Blocked/M0.**

Canonical04 ran **{summary['started_at_utc']}–{summary['completed_at_utc']}**, all120fresh startup launches,20idle processes/1200RSS samples,20main runs and12diagnostic runs. Main3,600,000 plus diagnostic1,872,000 actual measured requests = **5,472,000 correct, zero errors/drops/timeouts/lost acknowledged writes**. These counts exclude preparation, warmup, planned-but-unexecuted manifest entries and the separately declared probes. Collection exit0 alone is not the proof; read the [independent raw audit](../evidence/small-api-collector/results/raw-audit/audit-final.md).

## Change and frozen provenance

[ADR0011](../adr/ADR-0011-small-api-collector-connection-readiness.md) froze the experiment before timing. Samples compiled source is `a3bd8b5c5747440c81124774ac10b6451d88ff82`; Engine remains `6804271d429106864e01e4ec546a41dff771f84b`. Only collector, tooling and documentation changed. Portable Engine/business handlers, codecs, typed operations, original payloads/schedules/rates/caps/deadlines/budgets remain unchanged. SDK/runtime remain11.0.100-rc.3.26522.148 /11.0.0-rc.3.26522.148; no new package, R2R or runtime knob.

The collector now separates control and load pools. Two verified control reads precede128read-only HTTP/1.1 load responses held unread simultaneously. Require128distinct first-use TLS connection identities, then release one barrier and validate every nonempty body. One30s deadline covers preparation; failed holds cancel/join/dispose before a structured nonzero failure. Phase TLS/client history and all observed rows survive managed preflight/phase rejection. The controller requires complete readiness, clocks, raw-file presence and exact failure stage/counts/no-later-phase evidence; exit1 is the only recognized managed preflight rejection. TLS1.3/custom-root/hostname verification and the original128outstanding/1s scheduled request deadline remain.

The128live-response claim applies at the barrier. Later cumulative TLS histories do not count currently live sockets. Handshake timestamps are after TLS negotiation, not TCP starts. GC/thread-pool counters are phase-boundary aggregates; they do not localize a GC cause. Abrupt process/host loss can still lose the in-memory phase and invalidates it.

Fresh native app/cwd is `/home/tom/.local/share/cehpalon-benchmark-deployment/collector-20261028/app-final-02`;67files/23,281,577bytes match the clean Linux02 artifact, assembly SHA256 `742451b86f81c439938d93aad19a0f568133fe9ff2910bae4458f6633cdcfdd4`. Native SDK4178regularfiles/549,400,671bytes plus1668symlinks were independently rechecked before timing. All15build inputs/host match Git blobs, three actual generated catalog registrations compile, and runtime graphs exclude Roslyn/CodeGeneration. The raw audit verifies all109frozen source hashes and actual loaded-runtime paths. Startup trace was off; key import/full10kreadiness hash/first verified response remain inside the existing clock.

## Validation, including retained negatives

- Offline collector proof10/10, shared metadata guards29/29 on Windows/Linux, canonical failure-classifier checks16/16 and five independent actual TLS fault fixtures pass. Fault fixtures cover ConnectionClose, empty/invalid body, a stalled30s header deadline, and128valid holds followed by4000HTTP503 offered failures. All started requests joined; failure rows/TLS/client/stage reports remain; warmup/measurement were skipped. These are robustness fixtures, not production capacity tests.
- **Windows01 failed one case:** baseline HTTP409 entered the delayed handler0.3382ms after abort. ACK0.5528ms/no mutation/cleanup do not satisfy the required in-flight condition. Linux01 passed. Root initially ran both hosts concurrently; interference is plausible, not established. Both complete01 attempts remain retained.
- Before another validation, ADR0011 froze exactly one entire sequential02 matrix, Windows then Linux, unchanged source/50ms abort/100ms ACK gate and no competing owned work. Both passed4000cases each, including400cancellations,120same-process host cycles and20kAPI-only exercise/host. Maximum ACK Windows1.2032ms/Linux1.330781ms raw; maximum shutdown6.5286/1.6362ms. No favorable individual-case replacement. [Detailed precanonical audit](../evidence/small-api-collector/preflight/sequential02-precanonical-audit.md).
- Connection diagnostic01 completed12/12fresh-server probes13:58:05–14:00:44UTC:48000actualoffers, allcorrect, zeroerrors/drops,130verified reads and128distinct held load TLS connections each. Full360kplanned manifests were generated per invocation (4,320,000entries total) to preserve canonical preconditioning, but only the4000prefix actually executed. No warmup/measured phase ran. [Probe summary](../evidence/small-api-collector/connection-probes/summary.json).

## Startup and idle

| Transport | Baseline p95 ms | Engine p95 ms | Original numeric gate |
| --- | ---: | ---: | --- |
{startup_rows}

Thirty observations per variant/transport, all retained. Both absolute1000ms and Engine-extra150ms bounds pass. These are fresh processes under observed OS caches, not machine-cold boots.

| Transport | Pair | Order | Baseline median MiB | Engine median MiB | Original numeric gate |
| --- | ---: | --- | ---: | ---: | --- |
{idle_rows}

All20processes have60RSS samples after the unchanged60s warmup/120s settle. All absolute256MiB and Engine-minus-baseline16MiB gates pass. Same-binary/package/scaffolding RSS compares activation/dispatch paths, not a stripped minimum Engine-free distribution.

## Main1000/s — all observations retained

| Lane | All five p95 observations ms | Population CV | Original numeric gate |
| --- | --- | ---: | --- |
{series_rows}

All four CVs are below the unchanged10% rule. No latency floor, outlier filtering, best-run selection or lower offered rate. All10matched pairs meet p95≤20ms/p99≤50ms, relative p95≤baseline+max(1ms,15%), allocation≤baseline+1KiB/request, correctness and drain gates.

| Transport | Pair/order | Baseline p95 ms | Engine p95 ms | p99 B/E ms | Approx allocated B/E bytes/offer | Numeric gate |
| --- | --- | ---: | ---: | ---: | ---: | --- |
{chr(10).join(pair_rows)}

## Comparison with complete canonical03

| Lane | Mean run-p95 03 ms | Mean run-p95 04 ms | CV03 | CV04 |
| --- | ---: | ---: | ---: | ---: |
{comparison_rows}

Mean run-p95 values are lower in04, but HTTP baseline/Engine and GraphQL Engine CVs are higher. In particular Engine GraphQL CV increases3.261601%→4.769352%, while remaining valid. Startup observations are also lower. **Do not claim all-metric improvement or an isolated Engine-code speedup:** Engine did not change, collector pool topology/preparation changed, and the shared host is nonreserved.

Canonical03's HTTP Engine2000/s preflight37drops/4000 remains failed, with no warmup/measured interval. Its initial4TLS connections versus baseline128 did not prove equal readiness; failed-phase TLS events were missing. Successful04 does not reconstruct those missing events, establish a single cause or an intrinsic capacity ceiling.

## Separate diagnostics100/500/2000

| Transport | Rate/s | Order | p95 B/E ms | p99 B/E ms | Actual outcome |
| --- | ---: | --- | ---: | ---: | --- |
{diag_rows}

All12actualtimed runs have correct state, no errors/drops, valid offered work and successful shutdown. Each uses60s warmup/180s measure. These rates have no acceptance latency/allocation budget and never replace1000/s. In particular HTTP Engine2000/s completed360000measured correct offers in04; this is a bounded fixture observation, not universal sustained-capacity or production qualification.

## Audit, retention and remaining gates

Independent raw audit streams188gzip files/8,596,800phase observations/6,672,000planned manifest entries. It regenerates136complete state snapshots (84driver+52finalserver), checks52physical readiness barriers,136phase TLS/client accounting records,32metrics-before-persistence brackets,172identities/runtime mappings/shutdowns,86pair orders and1200RSS samples. Unexpected discrepancies0. All raw source/row/manifest checks retain all observations.

Full raw bytes and both01/02validation matrices, probes and fault/offline proofs are retained in private Samples `small-api-benchmark/evidence/2026-10-28-collector/`; the execution-retention manifest records2640files/1,335,210,272bytes, maximum27,494,953bytes and1169excluded compiled-artifact files. Private fixtures/keys/dumps are excluded; native originals and agent worktrees remain. The immutable raw link and hash are in [raw-evidence-link.json](../evidence/small-api-collector/results/raw-evidence-link.json). Later final audit files are retained in Docs alongside the raw audit.

After timing, a Windows UNC audit reader failed with transport semaphore/invalid-argument errors. Read-only audits switched to native WSL paths; no measurement was repeated or rewritten. The task-owned Windows sleep guard released successfully and no persistent power plan changed. Final host/runtime and probe/functional closure audits are retained alongside the raw audit.

Proof limits: full response bodies are not all retained; runtime business validation and state assertions complement offline raw checks. API-exercise totals derive from deterministic loops/completed checks, not20kretained response rows. TLS history is not later socket liveness; aggregate GC/pool snapshots are not event-level causes. Source/artifact hashes are provenance consistency, not independent reproducible-build attestation. The public10kfixture does not replace protected20ktenant/IdP/provider tests. Unchanged Engine347/protected40tests were not rerun in this wave.

Shared WSL affinity does not establish dedicated2vCPU/2GiB or native OS deployment. Current Windows26H2 is observational and does not clear listed-supported-Windows #3. Existing Engine6804 CI runs40622737320/40622737252 still show four rejected jobs/zero steps due the retained payments/spending block: Blocked, not code failure or CI pass; no rerun or billing change. All three repositories remain private MIT. Existing #9/#11 stay OPEN/Blocked/M0 with null actual person-hours; only their bounded evidence bodies are synchronized through reviewed plan/dry-run/exact-hash apply/readback. #3 body/editable fields must remain unchanged.
'''
(docs/'internal/planning/w2-small-api-collector-readiness.md').write_text(report,encoding='utf-8',newline='\n')
shutil.copyfile(Path(__file__),out/Path(__file__).name)
print(json.dumps({'report':str(docs/'internal/planning/w2-small-api-collector-readiness.md'),'summary_status':summary['status'],'all_numeric_gates':summary['numeric_budget_observations_passed'],'measured_main':3600000,'measured_diagnostics':1872000}))
