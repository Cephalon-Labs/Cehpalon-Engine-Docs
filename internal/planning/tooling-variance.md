# Tooling variance investigation - 2026-10-30

The variance goal is **not achieved**. Correctness passed, but final Candidate02 retains7unstable generator distributions on Windows and4on Linux. Windows export-off CV is16.638835%, higher than the15.220958%baseline; its mean rises320.0426 to346.8358ms. Both complete candidates are retained, including Candidate01's temporarily lower export-off CV. Do not summarize this as a general performance or stability improvement.

The user authorized agents, analysis/improvement, complete repeats under the original criteria, GitHub/Docs synchronization and keeping #3 Blocked. Full #20 stays In Progress/P2/M0/Test+Benchmark Planned, W5/#2/#11 dependencies, estimates40-80(mid60) and null actual/remaining hours. [Delivery JSON](../evidence/tooling-variance/delivery.json), [Candidate01 comparison](../evidence/tooling-variance/candidate01-comparison.json), [Candidate02 comparison](../evidence/tooling-variance/candidate02-comparison.json) and [all Samples raw](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/tooling-benchmark/evidence/2026-10-30-variance) retain every result.

## Changes and evidence

Candidate01 Engine`1b9d538b4311cf574912596a0f547ae5ae788070`: reuse immutable type-display formatting, avoid temporary attribute/interface counting arrays and duplicate accessibility checks, replace grouping with ordered semantic-symbol deduplication and ordinal ID counts. ISymbol identity, diagnostic order/fail-closed behavior and exact emitted source remain intact. Four new contracts cover duplicate groups/partial declarations and ID/inherited-contract change+revert. The generated consumer separates serving from common command routing and selected GraphQL construction from common export while preserving actual observed failure counters and awaited disposal. This reduces source-method surface; it does not establish a JIT/assembly-load cause. [ADR0016](../adr/ADR-0016-tooling-variance-reduction.md) preceded its complete matrix.

Candidate02 Engine`55c630fc5d4c47258a1a2b0da4a16ce8bc42b9f7`: only reuse a static compact camelCase journal JsonSerializerOptions at two call sites. Timed work, rows, write/flush and final pretty report remain unchanged. [ADR0017](../adr/ADR-0017-tooling-recorder-metadata-reuse.md) was declared after retaining Candidate01 and before this source change/repeat. The fixed actual-row diagnostic used one primer then100serializations/path:274,816 to251,200allocated bytes, saving23,616bytes; all200strings identical, zero GC. The runtime may share equivalent-options metadata. This modest saving neither proves repeated full metadata rebuilding nor explains workload variance.

The [original protocol](../validation/tooling-benchmark-protocol.md) remains unchanged. Every host/candidate completes270generator measurements+36primers,12seeds/3cache preflights/18runtime postflights and144fresh CLI launches(24primers+120measured). The orchestrator is byte-identical; only02's declared excluded recorder implementation changed. No clock/work shift, extra warmup, runtime flag, forced GC, filtering, floor, selected pair or unchanged-source favorable rerun. Both candidates completed Windows then Linux with no competing owned build/audit during timing.

Exact-source component contracts509/506 and actual SDK compiler fixture passed at both revisions. Candidate01 also passed actual generated Small API133harness+39HTTPS cases, export160+25runtime differential cases and portable70checks per host. These include both tenant directions, disabled modules, external serving/graceful shutdown, late readiness truthful counters and readonly-parent export failure with awaited GraphQL disposal. These full regressions belong to1b9, not55. Candidate02's generator/runtime/templates are byte-identical to1b9;55 repeats components plus every benchmark actual generated consumer/artifact check.

Independent replay passed28,758checks for01 and30,009for02, zero failures: schedules/order/versions, all row/journal data, sample statistics, stdout/artifact/source/binary hashes and223committed Engine blobs/revision. [Audit01](../evidence/tooling-variance/candidate01-review.json) and [audit02](../evidence/tooling-variance/candidate02-review.json) include replay source hashes. All306fixture source/registry hashes and all four exported artifact sets/bytes/counters equal the baseline per host;02 also equals01. Export still performs no host/key/business/authority work, selected GraphQL construction/disposal is positive and disabled work zero.

## All series and negative outcomes

Baseline is29df762. Means are milliseconds. Generator CV uses five three-iteration means; CLI CV uses all15measured launches. All use sampleSD, fixed nearest-rank raw15p50/p95(p95=max), no filtering. CV>15% is descriptive instability, not a numerical qualification gate. CPU zeros remain zero; CLI child CPU is null. Allocation/CPU/GC and all extrema/percentiles are retained in both comparisons/raw rather than hidden when regressing.

### Windows generator and prepared manual emit

| N | State | Path | Baseline mean | 01 mean | 02 mean | Baseline CV % | 01 CV % | 02 CV % |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | fresh | generator | 17.9356 | 16.4530 | 16.6033 | 12.6971 | 6.5407 | 9.8158 |
| 1 | fresh | manual | 16.7782 | 15.4613 | 14.9906 | 20.0299 | 19.5651 | 8.4370 |
| 1 | noop | manual | 13.6502 | 11.0549 | 10.3552 | 4.4239 | 28.4748 | 31.1484 |
| 1 | noop | generator | 31.1386 | 24.9300 | 24.2112 | 10.8753 | 24.2318 | 26.1697 |
| 1 | edit | generator | 39.8237 | 34.6641 | 35.4354 | 3.3092 | 13.1008 | 5.8841 |
| 1 | edit | manual | 36.2708 | 31.5027 | 32.6782 | 5.0041 | 9.4276 | 6.7473 |
| 3 | fresh | manual | 39.3029 | 38.6673 | 38.0085 | 1.9910 | 2.2688 | 1.0930 |
| 3 | fresh | generator | 45.1052 | 43.7611 | 44.0354 | 2.3591 | 4.6703 | 4.2247 |
| 3 | noop | generator | 38.3845 | 37.7268 | 38.7839 | 5.9285 | 5.0104 | 5.1297 |
| 3 | noop | manual | 17.5984 | 16.4872 | 17.2179 | 4.9882 | 3.5637 | 3.3678 |
| 3 | edit | manual | 30.2867 | 36.1439 | 29.1237 | 22.2369 | 3.5589 | 20.2265 |
| 3 | edit | generator | 32.9296 | 39.9808 | 31.6265 | 21.2722 | 1.8378 | 19.6595 |
| 32 | fresh | generator | 57.5717 | 59.7036 | 56.0036 | 10.7576 | 26.8884 | 22.1253 |
| 32 | fresh | manual | 40.4013 | 41.2353 | 41.0294 | 15.6763 | 29.5378 | 15.7959 |
| 32 | noop | manual | 20.2703 | 19.8694 | 22.5889 | 13.9586 | 17.3802 | 16.1330 |
| 32 | noop | generator | 27.0454 | 26.4194 | 27.2735 | 9.3469 | 6.4733 | 5.4173 |
| 32 | edit | generator | 37.9832 | 33.8183 | 31.8161 | 13.6891 | 7.5310 | 7.2248 |
| 32 | edit | manual | 25.4854 | 22.6938 | 24.2720 | 7.9143 | 3.2348 | 14.1385 |

### Windows CLI

| Scenario | Baseline mean | 01 mean | 02 mean | Baseline CV % | 01 CV % | 02 CV % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| new-portable | 105.7294 | 115.8888 | 112.9091 | 5.0727 | 4.9689 | 3.7692 |
| new-small-api | 110.7939 | 124.1046 | 119.8129 | 3.4173 | 8.0939 | 3.5853 |
| validate-portable | 96.6780 | 104.8748 | 105.2513 | 3.2084 | 3.8238 | 3.5220 |
| validate-small-api | 98.4252 | 104.6421 | 104.5139 | 4.2004 | 3.1259 | 3.0093 |
| export-api | 321.4199 | 334.7396 | 314.9701 | 12.6716 | 13.4119 | 10.4376 |
| export-both | 695.6594 | 663.2735 | 662.2203 | 7.6560 | 8.7896 | 5.0264 |
| export-graphql | 672.7492 | 655.4652 | 681.7665 | 7.1788 | 7.2609 | 5.1440 |
| export-off | 320.0426 | 332.6855 | 346.8358 | 15.2210 | 10.3367 | 16.6388 |

### Linux generator and prepared manual emit

| N | State | Path | Baseline mean | 01 mean | 02 mean | Baseline CV % | 01 CV % | 02 CV % |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | fresh | generator | 21.9101 | 16.9843 | 18.0901 | 24.3947 | 15.0452 | 22.5619 |
| 1 | fresh | manual | 18.4017 | 17.0258 | 15.2104 | 17.4477 | 16.0126 | 11.2130 |
| 1 | noop | manual | 8.2586 | 8.0926 | 8.3067 | 14.3931 | 14.3598 | 15.0054 |
| 1 | noop | generator | 19.6104 | 14.7174 | 14.7750 | 9.6206 | 7.0862 | 8.5195 |
| 1 | edit | generator | 14.7536 | 17.7292 | 16.8277 | 4.2547 | 1.7184 | 9.4772 |
| 1 | edit | manual | 13.9434 | 16.1842 | 15.1428 | 6.6397 | 4.1546 | 5.3738 |
| 3 | fresh | manual | 16.6313 | 19.1311 | 17.4120 | 8.0303 | 11.1083 | 4.0978 |
| 3 | fresh | generator | 17.1796 | 20.8316 | 19.0641 | 2.4763 | 8.2024 | 4.3140 |
| 3 | noop | generator | 14.6255 | 15.8372 | 16.0835 | 7.9457 | 5.9721 | 3.8275 |
| 3 | noop | manual | 8.5164 | 9.9197 | 10.3167 | 7.3077 | 7.0870 | 5.9716 |
| 3 | edit | manual | 13.6563 | 13.9790 | 13.6955 | 5.1912 | 16.7485 | 6.1959 |
| 3 | edit | generator | 15.9006 | 16.1838 | 16.0353 | 4.8091 | 7.6290 | 8.0125 |
| 32 | fresh | generator | 35.0324 | 35.0450 | 40.5581 | 9.2281 | 13.0930 | 16.8582 |
| 32 | fresh | manual | 25.1604 | 21.8992 | 29.5359 | 17.9606 | 21.5834 | 17.5571 |
| 32 | noop | manual | 14.0812 | 12.0888 | 11.2275 | 10.1914 | 18.2414 | 12.4424 |
| 32 | noop | generator | 18.5198 | 16.3440 | 16.1166 | 5.1779 | 7.3642 | 8.0391 |
| 32 | edit | generator | 23.9806 | 21.1398 | 19.4691 | 9.8847 | 9.8365 | 14.5052 |
| 32 | edit | manual | 14.5516 | 15.0489 | 15.9022 | 12.9573 | 11.4026 | 14.0302 |

### Linux CLI

| Scenario | Baseline mean | 01 mean | 02 mean | Baseline CV % | 01 CV % | 02 CV % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| new-portable | 443.9781 | 416.4527 | 429.6633 | 4.9043 | 5.6637 | 7.1649 |
| new-small-api | 653.3848 | 601.2939 | 624.9802 | 6.4039 | 4.1543 | 7.8776 |
| validate-portable | 194.8282 | 178.2417 | 181.7834 | 7.8606 | 5.7264 | 6.7062 |
| validate-small-api | 192.4232 | 177.7494 | 178.2255 | 5.8589 | 6.0062 | 4.4911 |
| export-api | 319.7873 | 236.6622 | 243.1618 | 7.0692 | 8.0331 | 6.8614 |
| export-both | 814.6421 | 745.5822 | 782.3680 | 5.5654 | 4.1772 | 10.0638 |
| export-graphql | 788.7772 | 717.0029 | 750.1114 | 5.2022 | 3.2419 | 8.3577 |
| export-off | 289.6548 | 214.4198 | 232.5337 | 5.6951 | 4.2493 | 10.7289 |

Generator unstable counts: Windows4 ->6 ->7, Linux3 ->5 ->4. Windows CLI unstable counts1 ->0 ->1; Linux0 ->0 ->0. Candidate02 has6/8Windows CLI means worse than baseline; all8Linux CLI means are lower than baseline but all8are worse than Candidate01. Generator means worsen in4/18Windows and12/18Linux distributions against baseline. The manual path also fluctuates, and02changes only excluded recorder code: the results do not isolate a generator-code or recorder/GC cause. Outer manifest variability is CLI-only; raw generator flags and delivery per-workload flags stay separate.

Windows uses NTFS; WSL SDK/runtime is native ext4 with source/output9p. Shared-host timing, storage, process/JIT state and different run times remain uncontrolled; no reserved/reference machine, causal OS comparison or universal speedup is established. Performance remains Observed, qualification not_qualified, and the variance goal remains open.

## CI, tracking and continuation

Current55 [component40993252408](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/40993252408)/[platform40993252420](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/40993252420), and prior1b9 runs40991556310/40991556319 each have4jobs/0steps with explicit payments/spending-limit rejection. Infrastructure Blocked before execution, neither current CI pass nor code-test failure. No billing action or forced unchanged rerun. Raw CI is retained.

Existing #20 receives both full Engine journal SHAs and current bounded results through reviewed plan/dry-run/exact-hash apply/readback. #3 body/editable metadata and all23native/Project metadata remain unchanged. Docs/Samples commit hashes are technical provenance only. Raw retention excludes private fixtures/credentials, build binaries/intermediates and clone checkouts; code suffixes add.txt without changing bytes. Sources/build parents remain trusted, not immutable attestation or filesystem isolation.

Next obtain separately declared non-gating JIT/GC/scheduler/IO traces or a controlled reference environment before further performance hypotheses. Do not increase primers, force collection, tune flags or keep rerunning until CV happens to fall. Provider/platform/#3, complete profile/IDE/distribution/AOT/production qualification remains separate. This investigation preserves negative evidence and does not close #20 or claim the variance problem fixed.
