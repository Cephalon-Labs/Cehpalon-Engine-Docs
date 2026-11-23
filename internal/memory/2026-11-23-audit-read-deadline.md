# 2026-11-23 Optional audit read deadline overhead

The user requested clearer naming and the cost of enabling the audit read
timeout. The three Engine readers now name their optional helper readDeadline,
and the internal type is TenantChangeAuditReadDeadline. API names including
ActivateWithBudget and readTimeout, public error text, cancellation priority
and lifetime stay intact. A source comparison verified that only the internal
names and XML summaries changed. [Engine revision](https://github.com/Cephalon-Labs/Cehpalon-Engine/commit/f4be820b481cb871230cee6b0b006d6c4df0f36e)

The [declared protocol](../validation/audit-read-deadline-overhead.md) used
one Release binary and the same PostgreSQL 18.7 schema for both arms on WSL.
Only readTimeout changed from null to 2 seconds. Npgsql 10.0.3 used
Pooling=false. The four alternating pairs returned 3,200 measured responses,
640 warmups and 144 controls. All 96 rejected controls recorded zero protected
queries, handlers and results. The same receipt and resource IDs returned
each tenant's own fields, and all response digests matched the corresponding
tenant and page across HTTP, GraphQL and timeout settings.

| HTTPS workload | Paired allocation overhead | Paired allocation bytes/request | Paired p50 | Paired p95 | Paired p99 |
| --- | ---: | ---: | ---: | ---: | ---: |
| HTTP, 25 rows | +0.099% | +629 | +0.37% | +0.76% | −3.40% |
| GraphQL, 25 rows | +0.103% | +617 | +0.55% | +1.65% | +8.66% |
| HTTP, 200 rows | +0.255% | +11,278 | +0.58% | −5.34% | −3.48% |
| GraphQL, 200 rows | +0.00017% | +7 | −1.58% | −1.04% | −1.80% |

Each value is a median of within-pair differences. Allocation is managed
process-wide and includes server background work plus the snapshot protocol.
HTTP 25 had one negative allocation pair and GraphQL 25 increased in all four
pairs. The 200-row allocation deltas varied by several kilobytes and latency
moved in both directions. These observations do not isolate the timer's byte
cost or establish a consistent latency effect. The timing runs contain no
induced SQL lock and do not change any canonical benchmark gate.

The untimed preflight also passed 8 real PostgreSQL lock controls and 36
admission and validation controls. Server work and the exact owned SQL backend
finished at roughly 2.22 seconds for HTTP and 2.20 seconds for GraphQL when
the private 2-second deadline fired. The caller was still active, the adapter
returned its generic wire error and no page was published. Explicit caller
abort cancelled outstanding work with either configuration. With null, the
same SQL lock held past 2.25 seconds and the read finished successfully on
release. Every case observed the tagged PostgreSQL Lock waiter before the
signal and proved backend quiescence and successful reuse. The 250 Engine
Audit Trail checks, including direct TimeoutException and caller cancellation
classification, passed in the local WSL build.

The fixture was the existing owned PostgreSQL container, started only after
identity verification. Each phase seeded a new schema and preserved previous
data. It was stopped afterward with loopback port closure and volume retention
verified. Raw timing, paired comparisons, preflight controls, input hashes,
test report and verifier are in the [evidence directory](../evidence/audit-read-deadline/2026-11-23).
[Samples harness](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/commit/3f701be13495b3028bc123accf09a45fa6945eea)

The locked Windows sample build passed without warnings or errors. Its
no-argument setup entrypoint returned successfully. Hosted Engine artifacts
confirmed 1,526 Windows and 1,523 Ubuntu contract checks, including 250 audit
trail checks on each, from the exact Engine commit. Both SDK and driver
smokes passed. [Contract CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/45127001716)
[Platform smoke CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/45127001690)

GitHub and Docs synced append-only updates to #7, #8 and #18. Readback matched
all 23 issues while preserving every Project value, #3 Blocked, the complete
#20 mirror and the original benchmark criteria. Existing user edits were
preserved.
