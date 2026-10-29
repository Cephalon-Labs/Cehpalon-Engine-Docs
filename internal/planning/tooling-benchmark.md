# Bounded tooling observations — 2026-10-30

Existing #20 now has a complete fixed observational matrix for the actual generator and source-checkout CLI. Both local hosts passed every declared correctness/completeness check at exact clean Engine `29df762cf28d12bd0d587b3c9d99925bcb99b14f`. Runtime libraries and generated templates are unchanged; this delivery adds the measurement driver, orchestration and evidence. #20 remains In Progress/P2/M0 with full Test/Benchmark Planned, original W5/#2/#11 dependencies and null actual/remaining hours. #3 remains Blocked.

[ADR0015](../adr/ADR-0015-tooling-observational-benchmark.md) and the [protocol](../validation/tooling-benchmark-protocol.md) were committed before canonical timing. Source/SDK/package locks, commands, timestamps, compiler/CLI journals and artifacts are retained. [Delivery JSON](../evidence/tooling-benchmark/delivery.json), [independent replay](../evidence/tooling-benchmark/independent-review.json), [223 exact Engine source blobs](../evidence/tooling-benchmark/source-blobs.json) and [Samples raw](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/tooling-benchmark/evidence/2026-10-30) provide provenance.

## Correctness and measurement boundaries

Sequential Windows then Linux: component contracts 505/502 (zero failures), including tenant/identity/disabled adapters and actual SDK compiler fixture. Three Windows-only alias cases explain the count difference. Each host then completed270 generator measurements +36 primers,12 unmeasured retained-state seeds,3 cache preflights and18 postflight runtime proofs. Independent manual registration AST and actual lazy factory/dispatch/disposal match. Every timed emit succeeds. Each CLI series completed144 fresh launches (24 primers+120 measured), checking exact9/14scaffold files,17/32source inputs, actual selected plans, emitted3operation registry, consumer lock/runtime graph and four selected offline exports. Disabled work stays zero; enabled GraphQL schema/provider work and awaited disposal are positive and disclosed.

Independent review replayed10,811 checks with zero failures, including schedules/order/versions, raw journal equality, summary math, stdout/artifact/log/source/binary/assembly hashes and environment limits. All223 recorded Engine file hashes match committed Git blobs. Current templates/runtime are unchanged, so this phase did not repeat the historical full HTTPS/TLS/portable collision consumer or W0 API load matrices; their prior bounded evidence is historical, not new performance proof.

Generator clocks cover DriverRun+PEEmit versus PEEmit of an independently authored prepared typed registry. Parsing/references/manual authoring/edit preparation are outside both clocks. Fresh means new compiler graphs in a primed process; no-op retains exact inputs/driver, edit changes one operation ID per pair. Cache tracking is separate from timed drivers. CLI clocks include fresh process launch through exit and drained captured pipes, excluding output checking/log persistence. Preparation/primers/checks prime filesystem caches. CLI child CPU is unavailable/null; generator process CPU/global allocation/GC counters include matching instrumentation and background noise. Two Windows measured CPU rows are zero due to timer quantization and remain zero. Per-row PE bytes are not retained; their hashes alone do not independently reconstruct emitted code.

## CLI observations

All durations are milliseconds; p95 is nearest rank over 15values (the maximum of15), without interpolation/filtering. CV uses sample standard deviation of15launch values. Each row is an absolute cost; there is no competitive CLI baseline or causal OS comparison.

| Scenario | Windows mean | Windows p95 | Windows CV % | WSL mean | WSL p95 | WSL CV % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| new-portable | 105.7294 | 121.7119 | 5.0727 | 443.9781 | 502.2356 | 4.9043 |
| new-small-api | 110.7939 | 120.7145 | 3.4173 | 653.3848 | 738.9883 | 6.4039 |
| validate-portable | 96.6780 | 102.6029 | 3.2084 | 194.8282 | 222.7010 | 7.8606 |
| validate-small-api | 98.4252 | 107.6454 | 4.2004 | 192.4232 | 213.5165 | 5.8589 |
| export-api | 321.4199 | 377.2125 | 12.6716 | 319.7873 | 357.8123 | 7.0692 |
| export-both | 695.6594 | 750.2466 | 7.6560 | 814.6421 | 913.8412 | 5.5654 |
| export-graphql | 672.7492 | 758.3681 | 7.1788 | 788.7772 | 913.4044 | 5.2022 |
| export-off | 320.0426 | 400.7848 | 15.2210 | 289.6548 | 321.4656 | 5.6951 |

## Generator observations

Mean and CV use five repetition means of three iterations. Raw15-value min/max/p50/p95 and all CPU/allocated-byte/GC deltas remain in the JSON. Generated/manual path distributions are shown independently; no subtraction of unrelated p95 values or selected-pair effect is claimed.

### Windows generator/emit observations

| Operations | State | Generator mean ms | Generator CV % | Manual mean ms | Manual CV % |
| --- | --- | ---: | ---: | ---: | ---: |
| 1 | fresh | 17.9356 | 12.6971 | 16.7782 | 20.0299 |
| 1 | noop | 31.1386 | 10.8753 | 13.6502 | 4.4239 |
| 1 | edit | 39.8237 | 3.3092 | 36.2708 | 5.0041 |
| 3 | fresh | 45.1052 | 2.3591 | 39.3029 | 1.9910 |
| 3 | noop | 38.3845 | 5.9285 | 17.5984 | 4.9882 |
| 3 | edit | 32.9296 | 21.2722 | 30.2867 | 22.2369 |
| 32 | fresh | 57.5717 | 10.7576 | 40.4013 | 15.6763 |
| 32 | noop | 27.0454 | 9.3469 | 20.2703 | 13.9586 |
| 32 | edit | 37.9832 | 13.6891 | 25.4854 | 7.9143 |

### Linux generator/emit observations

| Operations | State | Generator mean ms | Generator CV % | Manual mean ms | Manual CV % |
| --- | --- | ---: | ---: | ---: | ---: |
| 1 | fresh | 21.9101 | 24.3947 | 18.4017 | 17.4477 |
| 1 | noop | 19.6104 | 9.6206 | 8.2586 | 14.3931 |
| 1 | edit | 14.7536 | 4.2547 | 13.9434 | 6.6397 |
| 3 | fresh | 17.1796 | 2.4763 | 16.6313 | 8.0303 |
| 3 | noop | 14.6255 | 7.9457 | 8.5164 | 7.3077 |
| 3 | edit | 15.9006 | 4.8091 | 13.6563 | 5.1912 |
| 32 | fresh | 35.0324 | 9.2281 | 25.1604 | 17.9606 |
| 32 | noop | 18.5198 | 5.1779 | 14.0812 | 10.1914 |
| 32 | edit | 23.9806 | 9.8847 | 14.5516 | 12.9573 |

CV>15% flags descriptive instability: Windows generator 4 groups and CLI export-off15.220958%; Linux generator 3 groups and CLI 0 groups. The outer manifest `unstable_observation` flag covers CLI only. Raw generator `measurementStatus` and group CVs are separate; delivery JSON also exposes the combined flag. Both hosts therefore have unstable observations. Correctness passed; performance is **Observed**, qualification **not_qualified**. No numerical performance PASS, threshold relaxation, outlier removal or rerun selection occurred.

## Host, failures, CI and next work

Windows SDK/source/output are on NTFS. WSL SDK/runtime is native ext4, source/output mounted through9p. The same shared physical host, caches, storage and runtime paths do not establish reserved/reference resources or OS/Engine speedups. These observations cannot clear #3 or full #20 qualification.

Retained generator smoke01 used earlier source and is preliminary. CLI Preparation01 failed before timing because an overly broad `tooling` substring rejected its own valid fixture assembly. Exact dependency-family checks and a fixed valid BenchmarkSample name corrected this. Preparation02 rebuilt/verified fixtures and exports with zero measurements, then both final canonical matrices ran unchanged. Preparation attempts retain manifests/logs but did not snapshot their old scripts; final canonical attempts snapshot source/lock/README. A preparatory SDK build flag misuse was rejected before runtime and corrected to locked restore then build. No failed preparation or measured row was hidden.

New exact-revision [component CI40925539477](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/40925539477) and [platform CI40925539491](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/40925539491) have4 jobs / 0 steps with explicit payments/spending-limit annotations. They are infrastructure Blocked before execution, neither a current CI pass nor code-test failure. [Raw CI](../evidence/tooling-benchmark/ci) is retained; no forced unchanged rerun or billing action occurred.

Public raw retention excludes build binaries/intermediates, clone objects and private material; code/project suffixes add.txt while preserving exact bytes. Original attempts/worktrees remain. Sources/build parents are trusted; hashes are observations, not immutable attestation or filesystem isolation. Provider, production, supported-Windows, package/global-tool distribution, AOT/trimming, IDE and full profile qualification remain separate. Next choose a separately declared ready slice or reference qualification; do not optimize by selecting favorable reruns or mark #20 complete from these observations.
