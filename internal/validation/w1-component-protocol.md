# W1 bounded component protocol — declared before measurement

Date: 2026-10-27. Scope: experimental Core/Composition and generated registry consumer; issues #5/#6/#20. This protocol does not replace W0 workload protocols or #3 platform acceptance.

## Correctness

Run Release builds with the private SDK pinned by Engine global.json. Freeze source/lock/generated-file hashes and record OS/runtime/SDK. Run meaningful executable contract suites for Core, Composition and CodeGeneration plus a consumer that compiles the generator as an analyzer. No skipped tests count as passed. Test both local Windows26H2 (observational) and WSL Ubuntu22.04.5; neither substitutes for missing supported-Windows hosted proof.

Required cases: typed success/business error, unknown/type mismatch with zero factories, malformed IDs, pre/in-flight cancellation, exception/cleanup ordering, immutable input snapshots, concurrent dispatch; schema/profile/dependency/cycle/explicit-false and entrypoint-root validation before activation; disabled module-owned factory/constructor/connection/endpoint/background counters zero; preflight/rollback/reverse/concurrent disposal; generated invalid/duplicate/inaccessible/generic declarations; deterministic output and emitted-code compilation. API/GraphQL/Worker module recorders are not real transport hosts.

## Component performance smoke

Declared guardrails are engineering budgets, not measured results or production promises. Measure only on the local WSL host, record physical/logical CPU, available memory, kernel, runtime, build and process affinity; no dedicated CPU/memory-limit claim. No external providers or network workload. Keep all raw repetitions and preparation failures; do not filter outliers or rerun selectively.

| Measurement | Workload | Warmup | Repetitions | Predeclared guardrail |
| --- | --- | --- | --- | --- |
| Core dispatch | Single synchronous success handler, immutable registry/context, one caller; 100,000 operations per run. Direct baseline creates/disposes the same handler and result with the same request/context/cancellation. Dispatcher plumbing and lookup/type guards are the measured additional work. | 10,000 each | 5 paired runs, alternate order | Median dispatch minus direct <=20 microseconds/op; median extra allocation <=1024 bytes/op; all values correct |
| Small composition | Four descriptors (core/api/graphql/worker); API-only JSON; compile a new plan every iteration, no activation side effects; 1,000 compiles/run | 100 | 5 runs | Median <=2 milliseconds/compile and <=128 KiB allocated/compile; expected plan exact |
| Larger graph | 128-node support chain with one explicitly selected entrypoint; new compile each iteration; 100 compiles/run | 10 | 5 runs | Median <=10 milliseconds/compile and <=2 MiB allocated/compile; expected count/order exact |

Use monotonic Stopwatch and `GC.GetAllocatedBytesForCurrentThread` around synchronous measured loops, fixed warmups/iterations, Release without debugger. Do not force GC between paired variants or run parallel workloads. Verify result/disposal counts and plan order outside measurement in addition to checksums inside loops. Report per-run elapsed, allocation and correctness. A guardrail failure is a failure under this protocol, not grounds to tune the threshold after the fact. Cross-OS comparisons, cold startup, percentiles, sustained throughput, resource ceilings, security overhead and framework superiority are out of scope.

Code-generation build time/allocation performance is **Not run** in this slice: compiler-process startup/restore/IDE effects need a separate cold/warm protocol. Determinism/diagnostic/consumer-build tests are correctness evidence, not a codegen speed claim. Thus full #20 benchmark acceptance remains open. Full #5/#6 acceptance also retains platform/dependency and wider-scope gates.
