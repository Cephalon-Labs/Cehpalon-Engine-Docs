# Tooling trace investigation — variance remains unresolved

User authorized process-scoped JIT/GC/scheduler/IO diagnosis with agents, evidence-based improvement and one complete original benchmark series, keeping #3 Blocked. [ADR0018](../adr/ADR-0018-tooling-trace-guided-investigation.md) declared the fixed lanes, conformance and final unchanged-source series before collection. Engine remains `55c630fc5d4c47258a1a2b0da4a16ce8bc42b9f7`. This wave improves diagnostic tooling; no Engine optimization is justified by the observed traces. Timing and qualification are separate from capture integrity and semantic correctness.

## Completed diagnostic scope

Windows EventPipe runtime02, Linux EventPipe runtime01 and separate Linux native01 each completed one full diagnostic generator matrix and24CLI processes, totaling75targets. Each generator preserves270measurements+36primers,12seeds/3cache preflights/18runtime postflights and2,956stage markers. CLI uses all eight original scenarios in three rotated/reversed rounds. These are perturbed diagnostic executions, never benchmark acceptance or startup timings; reverse-port suspension and collector coordination are excluded from no claimed startup metric.

Private collector tools are pinned: dotnet-trace10.0.750501, TraceEvent4.0.0 and Diagnostics client0.2.750501, using SDK11.0.100-rc.3.26522.148. Standalone analyzer dependencies do not alter Engine policy. Runtime provider0x11C14FCCBD/Verbose5 and sampled-thread-time profile do not request forced collection or heap dumps. ForcedGC occurs only in the separate synthetic conformance fixture.

Independent [Windows audit](../evidence/tooling-traces/audit-win01.json) and [Linux audit](../evidence/tooling-traces/audit-linux01.json) replayed25targets/host, exact306generator semantic/order identities,2,956spans, all24CLI outputs, pinned binaries/sources,675,007/913,546raw events, target PID/marker clocks and normal joined cleanup. Reported EventPipe/ETLX loss and payload errors are zero. Seven targets per host retain incomplete interpretation; aggregate EE pairing errors39/135 and JIT errors1/0 remain visible. An integrity pass does not establish complete causal attribution. All50runtime OS observers saw exit, but counters are sampled lifetime observations.

## What the traces establish

[All runtime rows/stages and48CLI findings](../evidence/tooling-traces/runtime-findings.md) retain every value. Generator traces have40,916/41,532paired JIT intervals and87/77paired GC-related envelopes (Windows/Linux). Main measured RunGenerators sums are631.438/449.090ms versus7,189.789/6,226.028ms PE Emit; these traced totals include manual and generated emit, with generation only in the generated half. They do not measure full SDK builds or developer productivity.

Some slow size32 manual and generated rows overlap10–34ms verified narrow all-suspended GC windows. Other slow size1 rows have no paired GC/same-caller JIT, so GC/JIT cannot explain every slow row. Managed caller stacks include Roslyn Emit and WaitForWorkers/task waits; sampled residency is not CPU hotspot attribution. Background JIT elapsed overlap does not prove caller stall. Linux additionally has13measured rows intersecting ambiguous EE episode windows; paired-GC zero is not absence proof.

All12GraphQL-enabled exports contain3,744HotChocolate JIT intervals per trace and schema/executor stacks. All36other CLI traces show no observed HotChocolate JIT/stacks. This agrees with actual guarded offline schema construction and disposal. Expected selected GraphQL work is not evidence of disabled-module activation. Canonical artifact/counter checks independently preserve disabled-work zero and no serving/key/business/authority work.

[Native verdict](../evidence/tooling-traces/native-verdict.json):25targets,64,254native events and10,672proc samples, with no sampled PID/birth mismatch or unparsed/incomplete syscall records. Kernel event-loss count is unavailable. Forty-eight thread-read races and nine terminal-unavailable observer statuses remain. Of306main rows,270have wholly interior main-TID counter intervals;40rows contain135safely attributable selected syscalls. The slowest871.262ms compiler body has862.431ms interior coverage but6.403ms main-TID CPU,0reported queuewait and99voluntary switches. This cannot distinguish GC/futex/other-TID work, ptrace or shared-host effects; it does not prove absence of IO/waits.

Generator journal writes306pwrite64/240,915bytes/204.917ms summed syscall wall occur outside compiler metric bodies. Publication fsync/rename calls match intended durability; evidence gives no basis to weaken them. Linux proc IO accounting is unavailable. Syscall wall/bytes are not physical-disk latency, and separate native/EventPipe runs cannot be fused as exact causal overlaps. Windows current token cannot supply kernel scheduler/context-switch/file traces: process CPU/IO and initial owned-thread CPU are the declared fallback. Later-created Windows threads are outside that cached-thread dimension.

## Collector improvements and retained failures

Synthetic Windows04/Linux01 conformance passed five known aligned markers, positive JIT/GC/stacks, known file semantics, loss/error checks and owned cleanup. Native synthetic conformance verifies exact4,096-byte file read/write with FD lifetime, PID/birth, clocks and raw replay. Fifteen native positive/negative fixture checks and five child-environment/missing-binary checks pass.

Retain Windows conformance01 pipe-name mismatch and excessive repeated global Toolhelp scans;02 default-port resume acknowledgment that did not release its custom reverse port;03 successful capture with unregistered CLR templates; and full Windows runtime01 stopped at first export due a relative collector-DLL path. Fixes use a bare private pipe, one initial owned-thread snapshot, explicit QPC clocks, same-port session/startup resume, subscribed CLR templates with raw event metadata, absolute executable inputs and child-only diagnostic environment isolation. Missing tools are rejected before any owned child starts. The entire Windows lane was repeated as02; no partial lane is stitched into the final result.

Initial observer cost remains disclosed: the Windows03 snapshot used109.375ms CPU before managed startup; steady reads averaged0.069ms and actual cadence reached16.07ms despite10ms requested. Native ptrace/polling materially perturb execution. These are collector observations, not causes of previous untraced Engine variance.

Launch runner source and later on-disk snapshots are separately pinned for Linux runtime01, where an unused native-conformance branch was integrated after Python loaded its launch source. Independent AST comparison proves six runtime-related functions equal across approved variants; no immutable executing-byte attestation is claimed. Final native lane freezes input executable/orchestrator hashes before/after. All raw attempts, exact source snapshots and deterministic compressed evidence are retained; ETLX/build/private/clone material is excluded. Per-row PE hashes cannot reconstruct omitted PE bytes.

## Product decision and unchanged final benchmark

No safe avoidable Engine work is isolated. Keep codegen semantic identity, selected schema generation/disposal, trusted tenant paths, Roslyn concurrency, tiering/GC behavior and atomic durable publication unchanged. Do not add primers, force GC, filter outliers or relax thresholds. A reserved reference environment and deeper supported scheduling/wait tracing would be needed for stronger causal attribution.

The one predeclared final untraced Windows→Linux series runs at unchanged Engine55 after all diagnosis agents become idle. Its original harness/protocol/locks/clocks/order/versions/primers/statistics remain byte-identical:270generator measurements+36primers and144CLI launches/host, with100%correctness/completeness and descriptive15%CV. Any favorable or worse values are retained as an unchanged-source observation, not an implementation speedup. Full results follow below.

Both full untraced matrices completed on55, sequential Windows then Linux, each270measured+36primer generator rows/12seeds/3preflight/18postflight and144CLIlaunches(24primers+120measured). All actual emit/runtime/registry/output/counter checks passed. Primary source/raw/stat/blob/output replay passed30,009checks with zero failures; [independent replay](../evidence/tooling-traces/final-benchmark-review01.json) passed32,801checks/zero failures. All306source/registry pairs and four export artifact sets/bytes/counters equal every preceding full series. These checks do not rerun or relabel older tenant/HTTPS regression suites.

All four series, every sample and statistic are in [final comparison](../evidence/tooling-traces/final-comparison.json). Sequence is baseline29df → Candidate01(1b9) → Candidate02(55) → final unchanged55.

| Host | Generator groups with CV>15% | CLI scenarios with CV>15% |
|---|---:|---:|
| windows | 4 → 6 → 7 → 9 | 1 → 0 → 1 → 0 |
| linux | 3 → 5 → 4 → 3 | 0 → 0 → 0 → 0 |

Final generator mean milliseconds (CV%); all18groups/host are shown. SampleSD over five three-iteration repetition means; original15raw samples and nearest-rank p50/p95 remain in raw data.

| N / state | Windows generated | Windows manual | Linux generated | Linux manual |
|---|---:|---:|---:|---:|
| 1 / fresh | 16.954 (8.70%) | 16.325 (16.21%) | 23.439 (27.98%) | 19.413 (20.53%) |
| 1 / noop | 25.466 (24.92%) | 12.424 (32.48%) | 18.903 (12.51%) | 9.848 (14.81%) |
| 1 / edit | 39.078 (5.27%) | 36.233 (3.71%) | 15.893 (3.10%) | 15.015 (4.19%) |
| 3 / fresh | 42.848 (3.02%) | 37.387 (1.63%) | 15.146 (3.95%) | 14.014 (5.40%) |
| 3 / noop | 38.748 (5.46%) | 18.275 (18.20%) | 11.772 (4.08%) | 6.954 (7.25%) |
| 3 / edit | 25.952 (21.40%) | 23.971 (21.45%) | 12.643 (7.14%) | 11.162 (12.04%) |
| 32 / fresh | 47.412 (18.59%) | 30.831 (15.24%) | 33.495 (4.86%) | 26.815 (6.65%) |
| 32 / noop | 25.441 (4.79%) | 20.180 (15.88%) | 17.041 (9.69%) | 12.299 (12.64%) |
| 32 / edit | 34.116 (11.29%) | 22.667 (11.52%) | 21.785 (15.37%) | 14.442 (12.60%) |

Final CLI mean milliseconds (CV%); each scenario has all15measured launches plus three retained primers.

| Scenario | Windows | Linux |
|---|---:|---:|
| new-portable | 115.787 (4.13%) | 414.484 (4.60%) |
| new-small-api | 120.100 (1.81%) | 592.826 (3.00%) |
| validate-portable | 106.061 (2.81%) | 175.190 (2.90%) |
| validate-small-api | 105.977 (2.50%) | 173.368 (3.66%) |
| export-api | 349.144 (12.30%) | 231.808 (2.80%) |
| export-both | 670.608 (7.14%) | 737.772 (2.50%) |
| export-graphql | 678.946 (7.18%) | 705.529 (2.64%) |
| export-off | 319.986 (11.37%) | 212.203 (3.45%) |

Variance remains unresolved: final Windows generator unstable count worsens7→9 while Linux4→3; CLI flags are0on both hosts. Windows export-off319.986ms/CV11.367% versus earlier unchanged55at346.836ms/CV16.639% demonstrates differing observations without a new Engine patch. Never present this as fixed variance or a code speedup. No filtered values, selected pairs, changed threshold/primers/runtimeflags, favorable extra retry or causal cross-OS claim. Performance remains Observed/qualification not_qualified on shared Windows/WSL; source/output on9p differs from native SDK storage, and resources are not reserved.

## Tracking, CI and remaining boundaries

Full #20 remains In Progress/P2/M0, original W5/#2/#11 dependencies, Test+Benchmark Planned, estimates40–80(midpoint60), actual/remaining null. #3 body/editable metadata remains identical Blocked. No supported-Windows/provider/reference/production/IDE/distribution/AOT/public-release promotion, authority bypass or billing action. Engine55 is unchanged, so current component40993252408/platform40993252420 remain the earlier payment/spending rejection before steps; they are neither a new pass nor a code-test failure and were not forced to rerun. Docs/Samples SHAs are technical provenance only; task/card journal remains Engine-only.

Raw evidence and deterministic retention: [Samples tooling-traces](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/tooling-traces/evidence/2026-10-30). Original nettrace/native/proc data, every failed attempt, all analysis sources and full final untraced outputs are retained with original/stored hashes. Derived ETLX/build/private/clone material is excluded. [Delivery metadata](../evidence/tooling-traces/delivery.json) records audits, retention totals and final tracking readback. No independent repeated timing series is added after these results.

Fresh-build binary hashes differ between the earlier55 and final55attempts; independent audit lists each before/after value and verifies final bytes against its own manifest. Source/harness/parameters are unchanged, but binary identity is not assumed and no PE-level reason for the difference is established. This strengthens the limit on causal timing comparisons.
