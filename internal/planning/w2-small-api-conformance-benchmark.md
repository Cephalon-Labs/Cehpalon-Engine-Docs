# Small API conformance and complete comparative observations

2026-10-28. Engine issues [#9](https://github.com/Cephalon-Labs/Cehpalon-Engine/issues/9) / [#11](https://github.com/Cephalon-Labs/Cehpalon-Engine/issues/11). **Functional corpus passed on both observational hosts. All planned measurement phases completed; benchmark acceptance did not pass.** Fresh-process startup exceeds1s; Engine GraphQL p95 CV is12.3681%, so the main performance series is invalid under the unchanged10% rule. Reference-environment preflight remains Blocked. #3 stays unchanged OPEN/Blocked; #9/#11 remain OPEN/Blocked, M0, with full Test and Benchmark gates Blocked.

## Scope and immutable inputs

This user-authorized continuation implements the remaining public W0 fixture, independent expected corpus, cancellation/lifecycle/disabled checks, fresh-process startup, idle RSS, five paired1000req/s runs per transport, and the separate100/500/2000diagnostics. It uses the project's actual code generator, Core, Composition and HTTP/GraphQL adapters. Agents supplied the host, corpus, driver/review and final independent audits; the primary is the sole remote writer.

- Engine pin: `6804271d429106864e01e4ec546a41dff771f84b`, unchanged this continuation.
- Samples measurement source: `d9f401a5c0de2687ba20b511f62715c7bdd69e23`. Runtime build used clean `9d915f90b66d90e44c7a54f8a5d6b4415df799e5` source; subsequent changes affect Python orchestration only. [Build provenance](../evidence/small-api-benchmark/results/build-provenance.json) binds all runtime inputs and artifact hashes to the frozen measurement source. These are technical evidence revisions, not task/card Engine commit entries.
- SDK `11.0.100-rc.3.26522.148`, runtime `11.0.0-rc.3.26522.148`, locked Release, HotChocolate16.7.1; real emitted typed operation registrations and no compiler-only runtime dependency. See exact [manifest](../evidence/small-api-benchmark/results/manifest.json), build manifests and lock files.
- [ADR0009](../adr/ADR-0009-small-api-conformance-and-measurement.md), [execution runbook](../validation/small-api-measurement-runbook.md) and original [W0 protocol](../validation/small-api-workload.md) were frozen before timing. All original numerical budgets, five-pair order, rates/caps and failures are retained.

## Comparison and environment boundary

Public synthetic10,000-record fixture,80/15/5 GetItem/ListItems/SetLabel mix, deterministic SHA256 seed and32serialized writer lanes. Both variants use the same owned business handlers, validators, bounded store, errors, runtime/packages, TLS fixture and instrumentation. Native baseline uses independent native Minimal API / HotChocolate direct-handler bindings without Core dispatch, generated registry or Composition activation. Engine uses those actual paths. Baseline also constructs unused pure ModuleRegistration metadata in shared startup scaffolding, without compiling/activating the plan. This is a native/direct-dispatch comparison with shared fixture scaffolding, not an Engine-free minimum host. Both variants live in the **same executable/package graph**, so RSS measures activation/path difference, not separately stripped distribution footprint. The fixed server-owned fixture principal is not authentication/tenant authority.

Timing ran2026-10-28 **03:52:20–07:29:26 UTC**. Shared WSL Ubuntu22.04.5 x64/glibc2.35 on Windows11Pro26H2/build26300.9711;20logical CPUs/about31GiB. App affinity0,2; driver4,6; orchestrator8,10 use disjoint guest physical-core groups. Affinity does not reserve dedicated CPUs. User cgroups are unbounded/non-writable: no demonstrated dedicated2vCPU/2GiB app reference, and app/driver share a machine. WSL is not native deployment proof; this Windows host is outside the checked support table. **All numbers are nonqualifying observations**, including numerical passes. No benchmark or functional result clears #3.

TLS1.3/custom CA/hostname verification applies to both variants, with actual client protocol/cipher telemetry. A shared pre-generated48h leaf/49h CA sits in task-owned Linux-home0700/0600 storage outside timing; no private PFX enters evidence or system trust. Fresh-process startup includes runtime/config/key loading and first business response, but excludes RSA generation and build/download. It is not machine-cold boot. A1s wall/monotonic discontinuity guard would invalidate/abort the attempt. The task-owned Windows idle-sleep guard was released; no persistent power plan changed.

## Functional, cancellation and lifecycle

Final Windows02 and Linux02 each pass baseline/Engine × HTTP/GraphQL, **1000 ordered cases/lane =4000/host, zero failures/skips**. The independently frozen categories per lane are500success,100conflict,100not-found,200validation and100cancelledwrites. Identical dataset/corpus/final expected-state hashes apply across hosts/lanes. The100cancelledwrites are included in1000, not extra cases.

Each host also passes **400 timed cancellations**, absolute monotonic50ms client abort with the handler entered,5s synthetic handler delay, server acknowledgement≤100ms after actual abort (maximum Windows16.0981ms; Linux20.2075ms), joined owned cleanup and no mutation after acknowledgement. **120 same-process start/stop cycles/host**, each shutdown≤5s with listener closed and owned handlers balanced, are distinct from fresh-process startup timing. **20,000 API-only requests/host** (10,000/variant) retain zero disabled GraphQL registration/DI/factory/executor/schema-ready observations through shutdown, with enabled positive controls. Schema-ready is an executor-readiness observation, not an independent schema constructor hook. Pure all-off compiler checks here do not replace the prior protected consumer's actual no-host/listener proof. Traps for unimplemented providers do not qualify providers.

The final conformance raw files, declarations, timestamps and lifecycle/probe records are in the [Samples evidence](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/64b45dc0b46230d559a7d992e88d8efb9c51e3ea/small-api-benchmark/evidence/2026-10-28) under `benchmark-conformance-win-02` and `benchmark-linux-integration-02/conformance`. Earlier01matrices remain retained too.

The previous protected20,000-record tenant fixture remains separate: Engine347/347 and protected consumer40/40 per observational host were already delivered at the same unchanged Engine source. This continuation does not claim they were rerun or promote the public benchmark to tenant/real IdP proof.

## Fresh-process startup — absolute budget failed

All **120 launches** retained:30/variant/transport, alternating BE/EB by launch index. Nearest-rank p95; no discarded starts. Startup spans before process creation through the first verified business response. All owned shutdowns passed.

| Transport | Baseline p95 ms | Engine p95 ms | Engine extra ms | Absolute ≤1000 ms | Extra ≤150 ms |
| --- | --- | --- | --- | --- | --- |
| http | 1200.400 | 1235.691 | 35.291 | FAIL | PASS |
| graphql | 1731.741 | 1830.724 | 98.983 | FAIL | PASS |

Engine's extra startup is within150ms in both transports, but **both variants fail absolute1s**. Relative passes cannot erase that failure.

## Idle RSS — all numerical observations passed

**20 processes,10 matched pairs**, BE/EB/BE/EB/BE per transport. Each warmed60s at1000/s, idled120s, then supplied60samples at1Hz. All1200samples satisfy their original slots; no resampling/filtering. Maximum≤256MiB and Engine median≤matched baseline+16MiB hold in all pairs. Warmups total1.2million correct offered requests, no errors/drops.

| Transport | Pair/order | Baseline median MiB | Engine median MiB | Extra MiB | Numeric budget |
| --- | --- | --- | --- | --- | --- |
| http | 1/BE | 137.703 | 141.758 | 4.055 | PASS |
| http | 2/EB | 137.227 | 134.312 | -2.914 | PASS |
| http | 3/BE | 138.273 | 142.191 | 3.918 | PASS |
| http | 4/EB | 138.723 | 138.695 | -0.027 | PASS |
| http | 5/BE | 135.309 | 143.785 | 8.477 | PASS |
| graphql | 1/BE | 147.805 | 151.656 | 3.852 | PASS |
| graphql | 2/EB | 156.766 | 162.645 | 5.879 | PASS |
| graphql | 3/BE | 159.172 | 150.895 | -8.277 | PASS |
| graphql | 4/EB | 155.980 | 156.566 | 0.586 | PASS |
| graphql | 5/BE | 154.812 | 158.160 | 3.348 | PASS |

## Main1000req/s series — individually within budgets, overall invalid

**20 measured runs /10pairs /3,600,000offers**, each separate60s warmup then reset and180s fixed open-loop1000/s,128outstanding cap,1s scheduled deadline, at most1s drain, no retries/rate reduction. All3.6million correct; zero unplanned errors, drops, timeouts or lost acknowledged updates,100% within drain. Paired wire/logical manifests and final-state hashes match; logical schedule matches across transports. p95/p99 include scheduled queue delay. All individual pairs satisfy20/50ms latency, Engine p95 overhead≤max(1ms,15%) and allocation overhead≤1024bytes/request.

| Transport | Pair/order | p95 B/E ms | p99 B/E ms | Allocation B/E bytes/offer | Individual pair budgets |
| --- | --- | --- | --- | --- | --- |
| http | 1/BE | 0.272353 / 0.292068 | 0.442989 / 0.452175 | 21183.6 / 21063.9 | PASS |
| http | 2/EB | 0.274878 / 0.280111 | 0.445388 / 0.447328 | 21183.9 / 21063.8 | PASS |
| http | 3/BE | 0.307386 / 0.293098 | 0.440491 / 0.497182 | 21186.3 / 21065.2 | PASS |
| http | 4/EB | 0.287051 / 0.276969 | 0.464035 / 0.442771 | 21183.7 / 21063.6 | PASS |
| http | 5/BE | 0.303843 / 0.292157 | 0.466659 / 0.472031 | 21184.0 / 21063.6 | PASS |
| graphql | 1/BE | 0.367981 / 0.364532 | 0.544635 / 0.560191 | 18549.6 / 18334.2 | PASS |
| graphql | 2/EB | 0.356796 / 0.343007 | 0.501556 / 0.498536 | 18548.6 / 17605.7 | PASS |
| graphql | 3/BE | 0.345033 / 0.480505 | 0.498226 / 0.708594 | 18094.6 / 17636.4 | PASS |
| graphql | 4/EB | 0.365457 / 0.382131 | 0.522177 / 0.571866 | 18548.6 / 18334.3 | PASS |
| graphql | 5/BE | 0.349637 / 0.369469 | 0.528279 / 0.574751 | 18253.6 / 17819.5 | PASS |

Population standard deviation divided by mean across **all five** per-run p95 values:

| Transport | Variant | All five p95 observations ms | Population CV | ≤10% |
| --- | --- | --- | --- | --- |
| http | baseline | 0.272353, 0.274878, 0.307386, 0.287051, 0.303843 | 4.9854% | PASS |
| http | engine | 0.292068, 0.280111, 0.293098, 0.276969, 0.292157 | 2.4023% | PASS |
| graphql | baseline | 0.367981, 0.356796, 0.345033, 0.365457, 0.349637 | 2.4726% | PASS |
| graphql | engine | 0.364532, 0.343007, 0.480505, 0.382131, 0.369469 | 12.3681% | **FAIL — series invalid** |

The Engine GraphQL third observation remains included. Its12.3681%CV exceeds10%; under the original protocol **the performance series is invalid**, despite low absolute latency and every individual pair passing. No outlier filtering/selective rerun/threshold relaxation. HTTP observations alone do not turn the combined acceptance into a pass. Cheap CPU/GC/allocation snapshots remain in raw load results; allocation deltas include matching metrics/background/runtime work and are not per-handler allocation tracers. Read-history validation checks permitted id/amount/revision/label tuples against issued revisions and final locked state, not general distributed linearizability.

## Separate diagnostic sweeps — all12 attempted and measured

100BE/500EB/2000BE per transport, each variant60s warmup+180s measure. **12/12 actual timed runs;1,872,000measured offers correct, zero errors/drops/timeouts**, all planned attempts accounted for. These have no acceptance latency/allocation gate and never replace the1000req/s series.

| Transport | Rate/s | Order | Variant | Measured correct/offered | Scheduled p95/p99 ms | Sent p95 ms | Allocation B/offer |
| --- | --- | --- | --- | --- | --- | --- | --- |
| http | 100 | BE | baseline | 18000/18000 | 3.978772/4.219961 | 0.540704 | 21178.7 |
| http | 100 | BE | engine | 18000/18000 | 3.719634/3.857503 | 0.513314 | 21058.2 |
| http | 500 | EB | engine | 90000/90000 | 2.950526/3.228329 | 0.395301 | 21060.3 |
| http | 500 | EB | baseline | 90000/90000 | 1.683389/1.907038 | 0.367363 | 21179.3 |
| http | 2000 | BE | baseline | 360000/360000 | 0.252136/0.537271 | 0.248810 | 21191.0 |
| http | 2000 | BE | engine | 360000/360000 | 0.262329/0.548949 | 0.258877 | 21071.0 |
| graphql | 100 | BE | baseline | 18000/18000 | 4.012200/4.309423 | 0.661616 | 18553.7 |
| graphql | 100 | BE | engine | 18000/18000 | 4.178131/4.421041 | 0.774465 | 18339.9 |
| graphql | 500 | EB | engine | 90000/90000 | 1.793952/3.063195 | 0.505663 | 18334.6 |
| graphql | 500 | EB | baseline | 90000/90000 | 1.776113/2.010869 | 0.465508 | 18549.1 |
| graphql | 2000 | BE | baseline | 360000/360000 | 0.315147/0.574853 | 0.311770 | 18548.2 |
| graphql | 2000 | BE | engine | 360000/360000 | 0.328678/0.624136 | 0.324880 | 17791.1 |

At low rates the driver pacing/queue delay is visible: e.g HTTP100 baseline scheduled p95≈3.979ms versus actual-send p95≈0.541ms. A smaller high-rate scheduled percentile does not establish a faster intrinsic server. Keep both timestamps and avoid ranking rates as server speed/capacity promises.

## Retained failed preparation and attempt01

Attempt01 is preserved **invalid/stopped**, including all startup observations and its first baseline warmup with45offered drops during cold client connection establishment. None of those startup samples was substituted into attempt02. The collector was repaired before02: one get/list plus128parallel read-only connection preparations, retained2s fixed-rate capacity preflight, state validation, then reset into unchanged warmup/measurement. Both variants receive the same sequence. All structured preparation rows remain retained; no hidden retry or skipped failure.

Native HTTP16KiB backing-buffer/no extra trim-copy and GraphQL4KiB streaming strategies were aligned with Engine before02, followed by full conformance reruns. Other retained setup failures include nonexportable Windows certificate re-export and ineffective Windows-mounted chmod; final private fixtures use verified Linux-home modes. Historical raw results/build attempts are not rewritten as passes.

## Evidence, tracking and next work

- Full raw request/manifest gzip files, environment, clocks,120startup/1200RSSsamples, state/metrics/TLS, all attempts/preflights/build/conformance outputs: [Samples raw evidence](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/64b45dc0b46230d559a7d992e88d8efb9c51e3ea/small-api-benchmark/evidence/2026-10-28), byte-preserved under `.gitattributes -text`; [retention hash link](../evidence/small-api-benchmark/results/raw-evidence-link.json). Private keys and build output directories are excluded; source/package/assembly hashes are retained.
- [Structured results](../evidence/small-api-benchmark/results/summary.json), [all main observations](../evidence/small-api-benchmark/results/load-observations.json), [diagnostics](../evidence/small-api-benchmark/results/diagnostic-observations.json) and final independent audits in the evidence directory. Final host audit verifies106frozen input hashes,172ready/shutdown records and4233actual TLS1.3 connections; no owned benchmark processes remain. Functional audit independently replays the expected model. The20,000API exercise count per host derives from source loops and completed checks, not individual request rows. Corpus raw files retain expected/actual status and hashes but not complete response bodies/final record snapshots. Load raw rows retain validation/status/timestamps/bytes, not complete response bodies, so offline replay cannot independently reconstruct every response payload; the semantic validator, corpus and deterministic final state provide the declared checks.
- [Hosted CI readback](../evidence/small-api-benchmark/results/hosted-ci-readback.json): existing Engine6804 runs40622737320/40622737252, four jobs total, **zero steps**; payment/spending rejection. This is Blocked, not a test pass or a code failure. No billing change or unchanged job rerun.
- Existing #9/#11 mirrors and Project4 stay OPEN/Blocked/M0. Benchmark gate changes Planned→Blocked because observations completed with startupFAIL/CVINVALID and nonqualifying reference preflight. Full Test gate stays Blocked on #3. #11's measurement criterion records completion with these explicit boundaries; no full-acceptance closure. Native Type/Labels/Priority, estimates, null actuals, dependencies and Engine-only journal are preserved. #3 body and editable fields are compared unchanged before/after synchronization.

Remaining qualification: listed-supported Windows proof for #3 and actual dedicated reference hardware/resource limits; investigate startup initialization and variability using a separately predeclared experiment, then run a complete qualifying protocol on frozen source. Do not selectively rerun the high GraphQL value or relax budgets. Native deployment, external authentication/tenant/provider/durability/recovery and production gates remain separate. No blanket framework superiority, production capacity or maturity promotion is claimed.

Final [tracking readback](../evidence/small-api-benchmark/results/tracking-readback.json) confirms the four reviewed operations only,23mirrors synchronized and #3 editable fields/body unchanged. Raw evidence is committed in private Samples at the immutable link above.

Independent [raw audit](../evidence/small-api-benchmark/results/raw-audit/audit-final.md) streams all188gzip files:8,596,800phase observations including preparation/warmup,6,672,000frozen manifest rows,84full state snapshots,172host ready/shutdown records and1200RSSsamples. Recomputed percentiles, CV, manifests, final state, offered conservation, pair orders and numerical budgets agree.5,472,000of those observations are the measured main+diagnostic requests. No unexpected findings; the initial strict Python-orchestrator provenance difference is retained and adjudicated separately from unchanged compiled inputs. Exact audit scripts and initial scan remain alongside the final result.
