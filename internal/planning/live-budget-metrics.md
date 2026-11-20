# Owned budget metrics during protected HTTPS traffic

The generated Small API adds `--self-test-live-metrics --output <new-report.json>` and a `FixtureHost.CreateBudgetMetrics(meterName)` method. The host method returns a caller-owned budget meter after a configured budget exists. An all-off profile returns no meter. Normal serving keeps collection under application ownership.

The proof starts a real fixture HTTPS host with API and GraphQL enabled. It runs both total-capacity eight and total eight/per-tenant four. Four async client drivers split 400 reads across the two transports and two fixture subjects. Every successful response is checked for the expected tenant and item. A held Alice write keeps one slot occupied while the reads complete and across shutdown. Both cross-tenant directions are tested through each transport with generic denial before business work.

The sampler requests a 10 ms delay and serializes explicit collection calls with controlled phase observations. Its records include raw start ticks, callback duration, current-thread collection allocation, gauge values and completed business-read counts. The midpoint pauses all four drivers after 200 completed reads until a periodic observation has recorded that state.

After the original traffic, four additional reads pause inside authorized handlers: one per transport for each tenant. The fixture observes five admitted operations and two active tenants in a controlled overlap phase and requires the periodic sampler to see five active operations. Ready, held, midpoint, overlap, closing and stopped phases verify exact aggregate values. Periodic samples check individual bounds, names and monotonic closure. Gauge callbacks can represent different instants during concurrent requests. The sampler checks each gauge separately during that period. When shutdown starts, the write and four reads still own five slots and closed admission is observable. Releasing them permits 404 successful reads, one write, 405 factories and 405 disposals in each mode, with one host disposal. The meter remains available to read the terminal empty/closed state, then disposal stops its callbacks.

The output preserves all observations, including the first collection, and retains partial case data on failure. The analyzer checks the phase sequence, each collection, exact business and cleanup counts, tenant denials and meter disposal. [Frozen protocol](../validation/live-budget-metrics.md)

## Preserved results

The initial source `1021a4e388b8e38f6022a770556a01e523d35cb9` completed both full host verifiers. Every periodic active sample was one: it saw the held write while the short read admissions escaped observation. The separately declared extension `5f8f252e901e85c50d7fc6f4b760e457965ce3bb` retains that workload and adds four paused reads per mode. Its controlled overlap and closing samples show active five and, for the tenant budget, two active tenants; its periodic samples also see five. Both versions and all their raw samples remain in the evidence archive.

Each revision passed 521 local Windows and 518 WSL component checks. Actual generated consumers passed 160 checks on each host, including all 39 original self-test cases, capacity, tenant capacity, drain and normal external serving. The extended metrics proof completes 808 reads, two writes and eight cross-tenant denials per host across both budget modes, with exact cleanup counts. The disabled profile creates no budget meter or host. Disposing the meter stops callbacks. Four altered initial datasets and eight altered extended datasets were rejected by the analyzer.

All collection costs below are descriptive, in microseconds. Each row retains its first collection. The counts include explicit controlled phases and periodic observations; collection allocation is caller-thread allocation only.

| Source / host | Budget | Collections / periodic | First | Median | Maximum | Observed allocation bytes |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Initial / Windows | Host | 23 / 18 | 825.100 | 6.400 | 825.100 | 0, 24 |
| Initial / Windows | Tenant | 10 / 5 | 274.400 | 4.900 | 274.400 | 0 |
| Initial / WSL | Host | 34 / 29 | 753.031 | 7.935 | 753.031 | 0, 24 |
| Initial / WSL | Tenant | 12 / 7 | 289.006 | 6.047 | 289.006 | 0 |
| Extended / Windows | Host | 28 / 22 | 832.600 | 7.050 | 832.600 | 0, 24 |
| Extended / Windows | Tenant | 14 / 8 | 295.200 | 6.000 | 295.200 | 0 |
| Extended / WSL | Host | 35 / 29 | 869.762 | 7.352 | 869.762 | 0, 24 |
| Extended / WSL | Tenant | 14 / 8 | 236.415 | 5.628 | 236.415 | 0 |

The timed interval includes `RecordObservableInstruments` and its callback dictionary updates; it excludes copying a completed row for output. The sampler requests a 10 ms asynchronous delay after each collection and records actual start intervals. It does not promise a 10 ms timer or observe every short request. There is no no-listener traffic baseline, so these values do not quantify total HTTP overhead. The controlled read pause is fixture synchronization rather than natural request duration. Different gauge values during unconstrained traffic may reflect different instants; use `GetSnapshot` for a coherent state.

The pinned SDK is `11.0.100-rc.3.26522.148`. These local Windows and WSL observations do not close #3 or establish canonical benchmark qualification. #18 and #20 stay In Progress, M0, with their existing gates, dependencies and unknown actual hours unchanged.

[Immutable consumer evidence and hashes](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/d9064c83fe1aaaa79a79301551eafb0a6afa8db3/tooling-small-api/evidence/2026-11-20-live-metrics) preserve 170 collections across both revisions and hosts. The source change is limited to generated Small API fixture/command support; Core and tenant admission semantics are unchanged.

[Hosted component CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44666844909) passed 521 checks on windows-2025 and 518 on ubuntu-24.04 at the extended Engine revision. [SDK/driver smoke](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44666844953) passed 12 with two real-provider checks not run on each runner: PostgreSQL transaction/query/cancellation and RabbitMQ confirm/manual-ack had no owned fixture connection. The new 160-check HTTPS consumer proof above is local Windows/WSL evidence. [Retained CI artifacts and hashes](../evidence/live-budget-metrics/2026-11-20-ci/SHA256SUMS.txt).
