# Paired overhead of the audit read deadline

Declared 2026-11-23. Compare readTimeout=null with readTimeout=2 seconds on
the same clean Engine build and the exact same Release consumer binary. This
measurement applies to the existing protected audit resource-history reader.
Only the deadline selection changes across the eight server processes.
The internal Engine naming change preserves public APIs, errors and behavior.

Reuse the [prior HTTPS protocol](audit-history-https-allocation.md) for the
seeded 640 rows, WSL x64, SDK 11.0.100, Npgsql 10.0.3, PostgreSQL 18.7, disabled
pooling, TLS trust, same schema across the arms, page sizes 25/200 and AB/BA/AB/BA
order. The null arm is A. Four pairs each run four rotated workloads with 20
warmups and 100 timed requests. The standard 144 controls are repeated with
the same exact isolation and no-query requirements. Managed allocation and
client full-body latency use the prior batch snapshots and nearest-rank
p50/p95/p99. Report signed paired changes and absolute bytes per request.
Retain every attempt, warmup and measurement. Keep concurrency limits unset.

The untimed preflight additionally runs four real SQL lock controls per
transport against the same seeded schema. Observe one active query tagged
for the owned resource reader, waiting on a PostgreSQL relation lock before
any signal. A configured deadline must complete with the existing generic
wire error while the caller remains active, and leave no published result.
Caller cancellation is tested with the deadline off and on. Observe the
server work token and dispatch token cancel, join the server work, verify the
owned PostgreSQL backend is quiescent, then release the lock and prove a
fresh read succeeds. The null arm is also held longer than 2 seconds and must
return successfully after release. That hold is a correctness observation,
not a sampled latency workload. Engine contracts supply the direct exception
classification checks.

Report this as a bounded sequential local comparison. Allocation snapshots
include managed process background and control overhead. The controls and
PostgreSQL allocations are outside the timing matrix. No new acceptance
threshold, provider qualification, production claim, or canonical benchmark
change. Keep #3 Blocked and preserve the other issue and Project values.
