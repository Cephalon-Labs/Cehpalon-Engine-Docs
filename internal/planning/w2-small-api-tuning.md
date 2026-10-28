# Small API startup and GraphQL variance tuning — complete attempt03

2026-10-28. User authorized analysis/improvement with agents, a complete rerun under the original criteria and GitHub/Docs synchronization, keeping #3 Blocked.

**Startup and main1000req/s numerical gates now pass in the declared local profile. Engine GraphQL CV falls from12.3681% to3.2616% under the unchanged10% rule.** All original phases were attempted. Diagnostics have **12/12 accounted attempts,11 actual timed runs and one failed HTTP Engine2000req/s capacity preflight**; its warmup/measured interval did not run. Reference qualification and full #9/#11 gates remain Blocked/M0; #3 stays unchanged Blocked.

## What changed and why

[ADR0010](../adr/ADR-0010-small-api-startup-variance-investigation.md) froze diagnosis/selection before canonical timing. Source Engine `6804271d429106864e01e4ec546a41dff771f84b` is unchanged. Samples `fb77069ec2af583b29814f941643a318222b420e` contains the consumer/collector/deployment improvements; these technical revisions are not task/card Engine journal entries. SDK/runtime remain `11.0.100-rc.3.26522.148` / `11.0.0-rc.3.26522.148`, HotChocolate16.7.1, the same locks and generated typed Core/Composition/adapters. No new package, ReadyToRun compilation or runtime tuning knob.

1. **Use Linux-native storage for both variants.** A predeclared2×2 diagnostic ran64 fresh processes,4 repetitions per lane/layout with rotating ABCD/BCDA/CDAB/DABC order, identical traced app/runtime bytes and fixed control-file storage. Moving SDK/shared runtime alone reduces descriptive median startup680–782ms; app+cwd placement alone85–173ms; all-native763–902ms across lanes. SDK regular files4178/549,400,671bytes plus1668link targets were verified. The app factor includes working/content root, so it is not a pure DLL-only measurement. Stage marks do not isolate individual runtime instructions. Canonical tracing is off, and key import/full10k readiness hash/first business response remain counted.
2. **Correct packaging and readiness publication.** Web SDK default items copied2135evidence files into an artifact:2202files/380MB. Excluding `evidence/**` produces67files/about23MB with the same dependency/runtime graph; all repository evidence remains. This packaging correction's independent startup effect was not isolated. Readiness now serializes, flushes and disposes a fresh sibling `.writing` before no-overwrite rename; selected transient stat/read absence errors retry within the original continuously counted clock/60s deadline. All other errors still fail.
3. **Remove in-window recorder work.** Each offered observation publishes once into an indexed array; identical8-field raw rows persist after all requests join. Request schedules, payloads, mix, cap, deadline, validators and recorded timestamps are unchanged. Measured server end-metrics now occur after joined requests and **before** persistence, correcting the previous flush-inclusive bracket. Client CPU/approximate allocation/GC/thread-pool and post-handshake TLS timestamps aid interpretation. Managed failures retain partial rows before failing; abrupt process/host termination can lose an in-memory phase and invalidates the attempt. This is reduced instrumentation interference, not a proven single cause of the old GraphQL variance.

The original [W0 budgets](../validation/small-api-workload.md) and [runbook](../validation/small-api-measurement-runbook.md) remain unchanged. The baseline is native direct dispatch with shared binary/packages/validators/store/scaffolding, including unused pure ModuleRegistration metadata; it bypasses Core dispatch/Composition activation. This is an activation/path comparison, not an Engine-free minimum distribution or stripped-package footprint. The same synthetic public10k fixture is separate from the protected20k tenant consumer.

## Prior evidence and diagnosis retained

The [previous complete attempt02](w2-small-api-conformance-benchmark.md) remains immutable: startup absoluteFAIL and Engine GraphQL CV12.3681% INVALID. Its high run stays in every comparison. Offline analysis shows that increase after send throughout all12time windows and all operations; pacing queue alone was not demonstrated as the cause. Server aggregate GC/CPU and untimestamped prior TLS counts cannot establish a single root cause.

Startup diagnostic01 stopped after40/64 because DrvFs readiness read returned ENODATA61. All raw data remains invalid as a complete experiment; none was adopted into diagnostic02. After the publication repair, diagnostic02 ran all64, then canonical03 ran all120 starts with tracing disabled. Failed offline probe01 was a CRLF comparison inference, retained and corrected without changing raw evidence/timing gates. No outlier deletion, selective acceptance rerun, latency floor or threshold/rate relaxation.

## Exact validation and host boundary

Clean committed source on both hosts passed **4000cases/host**, including400cancelled writes (max acknowledgement Windows1.6179ms, Linux1.5247ms recorded/1.524738ms raw, unchanged100ms limit),120same-process start/stop cycles and20,000API-only exercise requests/host. Dataset, ordered manifest and expected model hashes match. Conformance now records Stopwatch frequency explicitly. [Integrated preflight](../evidence/small-api-tuning/preflight/integrated-validation.json) verifies all13 build inputs against Git blobs and equality across hosts; four short collector lanes pass correctness/state/actualTLS and metrics-before-persistence checks. The short trial is not acceptance. Agents independently reviewed source, packaging, lifetime and the measurement method. Prior Engine347/347 and protected tenant consumer40/40 at unchanged Engine source remain separate evidence and were not rerun this continuation.

Canonical03 ran **08:54:16–12:24:25 UTC** on shared WSL Ubuntu22.04.5 x64/glibc2.35, hosted by observational Windows11Pro26H2/build26300.9711. App CPUs0,2, driver4,6, controller8,10;20shared logical CPUs/about31GiB, no reserved2vCPU or enforced2GiB app cap. Native storage does not repair these reference failures or establish native OS deployment proof. Windows remains outside the checked support table. **Reference preflight and #3 remain Blocked regardless numerical passes.**

Both variants load the same privately pre-generated48h leaf/49h CA with TLS1.3, custom trust and hostname validation, without bypass. Private files stay in separate0700/0600 Linux-home fixture storage and never enter evidence. The final app's67 hashes match the Linux conformance artifact and canonical DLL; no compiler-only runtime library or evidence content. Actual invocation/app hash and post-first-response runtime mappings verify the deployed native runtime. Mapping inspection is outside counted startup/load. The temporary Windows idle-sleep guard released; no persistent power plan changed.

## Fresh-process startup — original numerical budgets pass

120starts,30/variant/transport, alternating BE/EB by index; nearest-rank p95, no discarded samples. Before process creation through the fully verified first business response; builds/downloads/RSA generation outside the clock, all existing initialization/key load/hash/first request inside. Fresh process is not machine-cold boot.

| Transport | Old p95 B/E ms | New p95 B/E ms | New absolute≤1000ms / extra≤150ms |
| --- | --- | --- | --- |
| http | 1200.400 / 1235.691 | 432.789 / 438.697 | PASS / PASS |
| graphql | 1731.741 / 1830.724 | 894.146 / 902.391 | PASS / PASS |

Engine HTTP p95 becomes438.697ms from1235.691ms, GraphQL902.391ms from1830.724ms. The controlled layout diagnosis supports a deployment effect. This is not a claim that Engine runtime code became intrinsically faster; Engine code is unchanged and the overall consumer/harness/profile changed.

## Idle — all10 paired numerical observations pass

20processes,5pairs/transport in BE/EB/BE/EB/BE order. Each warms60s at1000/s, rests120s, samples60RSS values at1Hz;1200scheduled samples retained. Each maximum≤256MiB, and Engine median≤matched baseline+16MiB. Absolute and relative gates both hold. This does not prove an enforced2GiB cap.

| Transport | Pair/order | Baseline median MiB | Engine median MiB | Extra MiB | Numeric gates |
| --- | --- | --- | --- | --- | --- |
| http | 1/BE | 144.465 | 146.883 | 2.418 | PASS |
| http | 2/EB | 141.672 | 147.531 | 5.859 | PASS |
| http | 3/BE | 142.871 | 145.848 | 2.977 | PASS |
| http | 4/EB | 143.137 | 146.812 | 3.676 | PASS |
| http | 5/BE | 140.590 | 147.832 | 7.242 | PASS |
| graphql | 1/BE | 165.723 | 163.102 | -2.621 | PASS |
| graphql | 2/EB | 164.000 | 163.305 | -0.695 | PASS |
| graphql | 3/BE | 158.680 | 162.492 | 3.812 | PASS |
| graphql | 4/EB | 157.844 | 160.766 | 2.922 | PASS |
| graphql | 5/BE | 164.223 | 161.766 | -2.457 | PASS |

## Main1000req/s — all20 runs,3.6million measured requests correct

Five pairs per transport, each60s warmup/reset/180s measure,128outstanding cap,1s scheduled deadline, at most1s drain. All3,600,000correct, zero unplanned errors/drops/timeouts/lost acknowledged writes,100% within drain. Wire/logical manifest and paired final-state hashes match. All per-run p95/p99≤20/50ms, Engine p95≤baseline+max(1ms,15%) and allocation≤baseline+1024bytes/offer. Allocation metrics include application/runtime/control/background work; they are not isolated handler allocation tracers. The changed metrics bracket means old/new allocation observations cannot be attributed solely to Engine code.

| Transport | Pair/order | p95 B/E ms | p99 B/E ms | Allocation B/E bytes/offer | Individual pair gates |
| --- | --- | --- | --- | --- | --- |
| http | 1/BE | 0.317944 / 0.339708 | 0.445939 / 0.481793 | 21183.6 / 21064.8 | PASS |
| http | 2/EB | 0.317028 / 0.323019 | 0.444416 / 0.450158 | 21183.9 / 21064.4 | PASS |
| http | 3/BE | 0.323696 / 0.326007 | 0.446945 / 0.457246 | 21183.9 / 21063.8 | PASS |
| http | 4/EB | 0.337936 / 0.325377 | 0.485323 / 0.457422 | 21185.7 / 21063.9 | PASS |
| http | 5/BE | 0.327713 / 0.323115 | 0.458321 / 0.450287 | 21184.1 / 21063.6 | PASS |
| graphql | 1/BE | 0.419134 / 0.418070 | 0.603910 / 0.598365 | 18550.3 / 18336.8 | PASS |
| graphql | 2/EB | 0.406816 / 0.409634 | 0.561783 / 0.567388 | 18548.4 / 18333.9 | PASS |
| graphql | 3/BE | 0.400989 / 0.408854 | 0.549586 / 0.583626 | 18055.8 / 18334.9 | PASS |
| graphql | 4/EB | 0.456316 / 0.395948 | 0.648300 / 0.550011 | 18548.6 / 18335.1 | PASS |
| graphql | 5/BE | 0.394045 / 0.380465 | 0.539938 / 0.563016 | 18548.1 / 18089.6 | PASS |

Population coefficient of variation uses **all five** values in each variant/transport:

| Transport / variant | Old all-five p95 ms | New all-five p95 ms | Old CV% | New CV% | New≤10% |
| --- | --- | --- | --- | --- | --- |
| http / baseline | 0.272353, 0.274878, 0.307386, 0.287051, 0.303843 | 0.317944, 0.317028, 0.323696, 0.337936, 0.327713 | 4.9854 | 2.3429 | PASS |
| http / engine | 0.292068, 0.280111, 0.293098, 0.276969, 0.292157 | 0.339708, 0.323019, 0.326007, 0.325377, 0.323115 | 2.4023 | 1.9075 | PASS |
| graphql / baseline | 0.367981, 0.356796, 0.345033, 0.365457, 0.349637 | 0.419134, 0.406816, 0.400989, 0.456316, 0.394045 | 2.4726 | 5.3013 | PASS |
| graphql / engine | 0.364532, 0.343007, 0.480505, 0.382131, 0.369469 | 0.418070, 0.409634, 0.408854, 0.395948, 0.380465 | 12.3681 | 3.2616 | PASS |

All four new CVs are≤10%, so the main series is numerically valid under the original rule. **This observation improves stability, not every latency metric.** Means of the five observed p95s are shown explicitly:

| Transport / variant | Old mean of five p95 ms | New mean of five p95 ms |
| --- | --- | --- |
| http / baseline | 0.289102 | 0.324863 |
| http / engine | 0.286881 | 0.327445 |
| graphql / baseline | 0.356981 | 0.415460 |
| graphql / engine | 0.387929 | 0.402594 |

Old/new mean p95 values are higher in the new observation. Different deployment, collector instrumentation and shared-host conditions prevent attributing this to an isolated code regression or speedup. Individual baseline/Engine comparisons within attempt03 use one common declared profile. Read-history validation checks allowed record/revision/label tuples against issued revisions and deterministic locked final state; it does not establish distributed linearizability.

## Diagnostics —12 attempted,11 timed, one capacity preflight failure

Fixed100BE/500EB/2000BE per transport. These rates have no acceptance latency/allocation gate and never replace the1000rate series. Eleven measured runs total **1,512,000correct requests**, zero measured errors/drops/timeouts. With main, actual measured total is **5,112,000**, not the5,472,000from the previous all-timed attempt. One planned warmup/measured interval did not execute and has no fabricated timed percentile.

| Transport | Rate/s | Variant | Order | Timed phase | Correct/offered | Timed p95/p99 ms |
| --- | --- | --- | --- | --- | --- | --- |
| http | 100 | baseline | BE | 180s | 18000/18000 | 4.882850/6.063348 |
| http | 100 | engine | BE | 180s | 18000/18000 | 5.251269/5.889864 |
| http | 500 | engine | EB | 180s | 90000/90000 | 1.694007/1.867624 |
| http | 500 | baseline | EB | 180s | 90000/90000 | 2.480375/2.682809 |
| http | 2000 | baseline | BE | 180s | 360000/360000 | 0.271956/0.400607 |
| http | 2000 | engine | BE | **NOT RUN** | **preflight3963/4000;37drops** | No timed percentile |
| graphql | 100 | baseline | BE | 180s | 18000/18000 | 6.142002/6.436828 |
| graphql | 100 | engine | BE | 180s | 18000/18000 | 5.186860/7.200278 |
| graphql | 500 | engine | EB | 180s | 90000/90000 | 3.069187/3.369427 |
| graphql | 500 | baseline | EB | 180s | 90000/90000 | 3.155065/3.527213 |
| graphql | 2000 | baseline | BE | 180s | 360000/360000 | 0.367296/0.526786 |
| graphql | 2000 | engine | BE | 180s | 360000/360000 | 0.321583/0.506237 |

Failed Engine HTTP2000 preflight:4000offers,3963correct,37offered drops, valid resulting state, no request timeout/HTTP/business-error flags; driver exit-6. The host still shut down gracefully with balanced owned handlers/closed listener/zero disabled probes. No warmup or180s measurement entered. The protocol retains this count-consistent failure and proceeds to remaining diagnostics; it is not silently retried or scored as a1000rate failure. **It is also not a successful2000rate qualification.**

Forensic raw observations locate the37drops at indexes129–161 and178–181, scheduled64.5–90.5ms of the2s preflight. All have sentTicks0; no SetLabel dropped. The preparation snapshot has4TLS connections versus128in the adjacent baseline after the same130read-only preparations. Actual physical connection availability was therefore different despite identical preparation policy. TLS events during the failed phase were not emitted into a later warm/load result; retained initial snapshots cannot prove the event cause. The first Engine completion occurs51.688ms after schedule origin versus2.205ms baseline; recorded in-flight count is128at each drop. One Gen0 collection is visible only as a phase aggregate, without event timing. These observations are detailed in the final forensic audit. This does not demonstrate an intrinsic Engine capacity ceiling or a single TLS/GC cause; no new timed retry was selected to replace the failure.

Low-rate scheduled latency includes pacing/queue delay; compare sent-to-completed telemetry too. Do not rank100/500/2000rates as intrinsic server speed. Future capacity work should predeclare and verify connection-readiness parity and retain per-phase TLS events on failures before a complete qualifying rerun; these are follow-up proposals, not retroactive changes to this experiment.

## Evidence, audits and tracking

- [Structured complete summary](../evidence/small-api-tuning/results/summary.json), [main results/CVs](../evidence/small-api-tuning/results/load-summary.json), [all diagnostic observations](../evidence/small-api-tuning/results/diagnostic-observations.json), [host/source audit](../evidence/small-api-tuning/results/tuning-final-host-review.md) [final raw audit](../evidence/small-api-tuning/results/raw-audit/audit-final.md), [functional audit](../evidence/small-api-tuning/results/functional-evidence-audit03.md) and [failed-preflight forensic audit](../evidence/small-api-tuning/results/failed-http-engine-2000-preflight03.md), with exact scripts retained.
- Full byte-preserved actual/failed outputs, declarations, manifests, dataset/state, timestamps, metric boundaries, TLS,120starts/1200RSSsamples, short preflight and both conformance hosts: [Samples execution evidence](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/bad8e36c04418bd5b71da2367a52a673b40da213/small-api-benchmark/evidence/2026-10-28-tuning). [Hash link](../evidence/small-api-tuning/results/raw-evidence-link.json); `.gitattributes -text` preserves raw bytes. Private fixtures, binary artifacts and dumps are excluded; original native files/worktrees remain. Raw response contents are not all retained; offline audits verify raw flags/status/timing/state/source, not replay every absent body. API-only exercise totals derive from source loops/completed checks rather than individually retained requests.
- [Hosted CI refresh](../evidence/small-api-tuning/results/hosted-ci-readback.json): Engine6804's existing40622737320/40622737252, four jobs, **zero steps** due payment/spending rejection. Blocked, not pass/code failure; no billing changes or unchanged rerun.
- Existing #9/#11 remain OPEN/Blocked/M0, Test/Benchmark gates Blocked. Numerical startup/CV/main gates improved, but supported Windows #3, dedicated reference qualification and remaining provider/production scope are not met. Preserve Type/Labels/Priority/dependencies/estimates/null person-hours and Engine-only journal; compare #3 editable/body unchanged through reviewed plan/dryrun/exact-hash apply/readback of23mirrors. No issue creation, publication or maturity promotion.

Remaining: explain/remedy the diagnostic collector-capacity failure in a separately frozen experiment, establish reserved reference resources and listed-supported Windows evidence, then complete qualifying gates. Preserve all negative history and continue from the current handoff; do not selectively rerun the previous high p95 or failed2000attempt to replace it.

Independent raw audit streams186gzip files,8,116,800phase observations and6,672,000frozen manifest rows; all106frozen source hashes and13inputs per host match. It checks134phase-accounting files,31measured metrics-before-persistence brackets,172owned host identities/runtime/lifetimes,1200RSS samples and83state checks (82driver-report snapshots plus the failed preflight's final server state). The37nonempty error strings are exactly offered.dropped in the known failure, not37business/HTTP errors; the reused scanner's legacy semantic_error_flags name counts all nonempty raw errors. No unexpected discrepancies or discarded observations. Host audit confirms4180actualTLS1.3connections across31timed main/diagnostic results; no owned benchmark processes or dump candidates/unexpected files remain in app-directory metadata. No dump/key content was read or copied.

Final [tracking readback](../evidence/small-api-tuning/results/tracking-readback.json) confirms exactly two reviewed body updates (#9/#11),23mirrors synchronized and #3 editable fields/body unchanged. Full statuses remain Blocked/M0; raw evidence is pushed in private Samples at the immutable result link above.
