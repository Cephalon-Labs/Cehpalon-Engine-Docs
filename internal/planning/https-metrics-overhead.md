# HTTPS budget metrics overhead observation

The declared #18 comparison completed all 24 WSL arms and 120,000 measured reads. Windows did not complete either attempted series: both stopped at a rejected warmup. These results measure a separate diagnostic workload and leave the canonical benchmark criteria and #3 blocker unchanged. Engine product source remains `5f8f252e901e85c50d7fc6f4b760e457965ce3bb`; only Samples harness/analysis and Docs change in this delivery.

The baseline creates the same business budget without a meter, listener or sampler. The observed policy creates the caller-owned meter/listener before warmup and collects after requested 10 ms asynchronous delays. Both run the unchanged actual generated Core gateways, Composition host and fresh tenant checks. Server and client are separate processes of one augmented generated consumer executable; no new runtime package is added. The original and augmented projects, locks, emitted registry and source/binary hashes are retained. The augmented registry matches the original generated registry byte-for-byte.

The workload mixes HTTP/GraphQL and Alice/Bob equally, reading the complete unchanged item 1 through authenticated HTTPS and sending an opposite tenant header. Four cross-tenant probes precede warmup. Each arm prepares 32 distinct TLS1.3/HTTP1.1 connections at an unread-response barrier, warms 1,500 reads at 500/s, then measures 5,000 at 500/s. Six alternating pairs run for each budget mode: total 64, then total 64/per-tenant 32. [Frozen protocol and preparation corrections](../validation/https-metrics-overhead.md).

## Complete WSL series

All 24 arms passed validation: zero failed/dropped measured or warmup offers, no new TLS connections, complete response validation and exact owned cleanup. Each arm ends with 6,532 factories, constructors, reads and disposals, zero writes/forbidden factories, one host disposal and a closed empty budget. All 96 cross-tenant probes deny before business work. This is 120,000 measured reads plus 36,000 warmup and 768 preparation reads. Baselines create no observation objects. Listener arms reconcile all 13,877 indexed samples/callback totals, including 10,106 samples starting inside server measurement brackets, and emit no callback after disposal.

The following table uses the six arm means per mode. Response p95 is the mean of six arm p95 values, not a pooled percentile. CPU and allocation are whole-server-process bracket differences divided by measured successful reads; they include background work and matching control gaps.

| Budget | Metric | Baseline mean | Listener mean | Difference of means |
| --- | --- | ---: | ---: | ---: |
| Host | CPU ms/read | 1.091214 | 1.160995 | +6.395% |
| Host | Managed bytes/read | 38673.348267 | 38724.245067 | +0.132% |
| Host | Response p95 ms | 1.122494 | 1.067636 | -4.887% |
| Host | Response p99 ms | 1.470058 | 1.430612 | -2.683% |
| Host | Scheduled-to-completion p95 ms | 4.496343 | 4.367083 | -2.875% |
| Host | Completed reads/s | 499.952873 | 499.944731 | -0.002% |
| Tenant | CPU ms/read | 1.083677 | 1.074488 | -0.848% |
| Tenant | Managed bytes/read | 38674.518133 | 38705.803733 | +0.081% |
| Tenant | Response p95 ms | 1.086172 | 1.070718 | -1.423% |
| Tenant | Response p99 ms | 1.416096 | 1.421608 | +0.389% |
| Tenant | Scheduled-to-completion p95 ms | 4.378740 | 4.413682 | +0.798% |
| Tenant | Completed reads/s | 499.983060 | 499.999663 | +0.003% |

Every paired difference is retained. To expose the spread, the next table reports signed listener-minus-baseline differences, with latency/CPU converted to microseconds. No pair or outlier was removed.

| Budget | Metric | Mean delta | Median delta | Minimum delta | Maximum delta |
| --- | --- | ---: | ---: | ---: | ---: |
| Host | CPU us/read | +69.780 | +81.436 | -95.959 | +181.017 |
| Host | Managed bytes/read | +50.897 | +51.766 | +16.144 | +91.915 |
| Host | Response p95 us | -54.857 | -69.507 | -275.224 | +129.676 |
| Tenant | CPU us/read | -9.189 | -39.479 | -101.617 | +149.769 |
| Tenant | Managed bytes/read | +31.286 | +29.333 | +7.544 | +64.602 |
| Tenant | Response p95 us | -15.455 | -72.174 | -105.886 | +260.354 |

Process allocation increased in all six pairs per mode: mean +50.897 bytes/read for host-only and +31.286 for tenant mode. These are observed process differences for this collection policy, not exact allocation attributed to an individual request or a universal meter cost. Host-only mean CPU increased 6.395%, while tenant mean CPU decreased 0.848%; signed CPU and response-latency ranges cross zero. Negative latency deltas do not establish a speedup. Six shared-host pairs do not establish a stable universal timing overhead or significance.

The 10 ms requested delay produced mean recorded intervals of 12.075–12.100 ms across listener arms. First collection costs span 661.644–889.313 us; per-arm collection medians span 3.307–4.358 us. All first samples and observed current-thread collection allocations (0 or 24 bytes) remain retained. These collection timings include RecordObservableInstruments and synchronous callback validation; they exclude storing the preallocated sample row and persistence. Row stores and timer scheduling remain part of the observed server process policy; callback wall time cannot be equated with the complete process CPU delta. Timer scheduling and other background work are included in server resource counters.

The original analysis output is retained. A presentation-only correction removes CV for signed paired differences, which lack a ratio-scale origin. All input hashes, per-arm values, paired deltas and means/medians/ranges are identical. Baseline/listener arm sample CV remains in the final analysis. No benchmark was rerun for this correction.

## Windows incomplete attempts

Attempt 01 completed three arms, then rejected host-only pair 2 baseline warmup (`passed=false`, 32 connections). The controller stopped its waiting client before warmup rows were persisted. Available host/controller output is preserved; missing rows prevent identifying the exact failed requests or cause. This is an invalid/incomplete full series.

The demonstrated collector defect was corrected without changing load or capacities: ABORT the waiting client, await its complete partial report and then stop the host. A controlled abort test preserves all 128 warmup rows, reconciles 160 handler disposals and closes the empty budget. The separately declared attempt 02 completed two arms, then rejected host-only pair 2 listener warmup. It retains all 1,500 offers: 1,495 passed and five were dropped at indexes 1190–1194. There were 32 pending client tasks at each drop, the preceding same-lane task completed later, and no new TLS connection was made. Maximum send-to-validated-response time was 62.2305 ms; maximum send lag was 16.0449 ms. The host reconciles 1,527 completed reads and disposals (32 preparation + 1,495 warmup), with zero writes and closed empty admission.

This establishes occupied client lanes at those observations. It does not isolate server capacity, physical server work, GC pauses or scheduler cause. No further unchanged-source timing rerun was made. Both partial audits retain every entered arm, including the failed and unpaired arms; their one complete pair each is descriptive only. The two Windows attempts are not pooled, substituted for WSL or presented as completed performance qualification.

## Validation and limits

Fresh actual generated consumer verification passed 160 checks per host, including all 39 original self-tests, cross-tenant and disabled-module proofs. Final harness conformance passed four arms per host, and all 17 adversarial evidence mutations were rejected per host. Earlier preparations/conformance are also retained. The collector's intentional ABORT path is separately tested. Archives losslessly round-trip every retained raw digest and reproduce the full WSL and both Windows partial analyses exactly. The unchanged tracking-tool regression passed 60 tests.

The SDK is `11.0.100-rc.3.26522.148`. WSL is Ubuntu 22.04.5 LTS x64, observes 20 processors and Server GC/Interactive mode; its SDK/runtime are in Linux-home storage while app/cwd/output use the mounted Windows filesystem. Local Windows is build 26300. Resources are shared and are not the dedicated canonical reference profile. No affinity, priority, GC setting, trust store, provider or host configuration was changed. The ten-second brackets are not the canonical sustained workload. Startup/keys/meter creation/TLS preparation/warmup and shutdown are outside the bracket; all initial samples are still retained. BEGIN/END control gaps and process background work remain included, so these counters do not attribute a precise per-request CPU or GC cost.

Engine source did not change, so its existing exact-revision hosted component/SDK-driver CI remains the recorded prior evidence; this new harness was tested locally on Windows/WSL. Real PostgreSQL/RabbitMQ checks are still unrun. #3 remains Blocked; #18/#20 remain In Progress/M0 with existing Test/Benchmark gates, dependencies and null actual hours. No production, provider, release or canonical performance acceptance follows.

[Immutable Samples evidence, frozen sources and SHA-256 index](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/109313ca8749fe24de52959d5d5ffdc922fcef9d/tooling-small-api/evidence/2026-11-20-https-metrics-overhead) retain all preparations, conformance, both incomplete Windows attempts and the complete WSL series. Raw host/client/controller JSON uses deterministic lossless gzip with separate stored/raw hashes; all retained data and three analyses round-trip exactly.
