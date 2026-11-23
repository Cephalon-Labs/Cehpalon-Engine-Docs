# Concurrent audit receipt collector observation

Declared 2026-11-23 for Engine #18 at Engine commit
`6fe7254404cf6b148370bd95befe8331e8932354`. Build locked Release on each
host with .NET SDK 11.0.100. Run Windows first and WSL Ubuntu second,
once per host, with runtime 11.0.0 and tiered compilation disabled.
Record any failed preparation or incomplete run before a stated correction.
No numerical acceptance threshold applies to this descriptive component study.

Use 1, 2 and 4 dedicated persistent managed threads in ascending blocks.
Each worker owns a real tenant dispatch scope, a deterministic synchronous
empty receipt source and three real Engine receipt readers. The readers use the
same checked tenant, receipt ID, fixture policy and null read timeout. The
source verifies the inputs and counts invocations in thread-local storage.
The dispatch fixture is adapted from the prior serial audit-read probe.
O disables the collector, P attaches a dedicated collector per worker, and S
attaches one collector shared among all workers of that lane. No snapshot
reader, exporter, endpoint or external provider runs in the timed work.
The same worker threads execute every mode in a lane.

Warm all workers in six blocks of 100,000 reads per worker in order OPSSPO.
Measure 12 matched rounds, 250,000 reads per worker and mode. Execute all
six permutations in order OPS, OSP, POS, PSO, SOP, SPO, then repeat the
sequence once. Conformance uses identical worker counts and permutations,
two reads per warmup block, four per trial block, and one permutation cycle.
Each timed read must complete synchronously with a null result. At each
barrier the coordinator validates exact source calls and personal/shared
success totals, with zero cancellation, timeout and fault counts. Report
every worker's begin and end timestamps, allocated bytes, thread ID and count.
Join the workers before leaving each lane.

Each trial's elapsed time is the interval from the earliest worker start to
the latest finish. Divide by the total completed reads to report inverse
batch throughput in ns/read. This includes worker scheduling skew and
excludes barrier coordination outside the recorded intervals. It is a
batch throughput metric. For each host and worker count, report median and
full range by mode, and paired P minus O, S minus O and S minus P deltas.
Also report start skew, all-worker overlap, measured thread allocation and
the observed host CPU availability. A nonoverlapping observation remains in
the record and the analysis. Analyze order and skew as possible sources of
variation, with no removal of extreme observations. Interpret S minus P as
a comparison between collector layouts, which may also reflect memory
placement and scheduling. Worker timestamps establish interval overlap,
without measuring actual simultaneous CPU residency.

Verify raw record order, independent worker identities within lanes,
consistent identities across each lane, read volumes, exact outcome counts,
allocation and monotonic time across trials. Record source and binary
hashes before measurement. This experiment covers in-process synchronous
empty receipt lookups with no simultaneous exporter. Networked/provider
paths, request latency and production performance remain outside its scope.
The original benchmark gates continue to apply.
