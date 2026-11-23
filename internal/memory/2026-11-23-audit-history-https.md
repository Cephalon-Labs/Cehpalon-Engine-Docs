# 2026-11-23 Audit history over HTTPS and PostgreSQL

Use the [frozen protocol](../validation/audit-history-https-allocation.md) and
[raw evidence](../evidence/audit-history-https/2026-11-23). Engine before was
887c529c5975e37bd53082896b56d7eff448dbbc and after was
4dedaeec12a6ae1e0d0d9313d79aa5d62113e7fa. Engine source was not changed in
this measurement delivery. Both Release binaries used SDK 11.0.100, the same
consumer source, Npgsql 10.0.3 and PostgreSQL 18.7 on WSL x64. The fixture used
the retained image digest, a fresh owned volume, loopback and fixed server
limits of one CPU, 512 MiB and 128 PIDs. Both revisions read the same newly
seeded schema with Pooling=false and the default planner.

The four AB/BA pairs used eight server processes and a separate client.
The independent verifier confirmed 3,200 measured responses, 640 warmups,
144 access and control requests, and 32 measured batches. Every measured
response corresponded to one completed protected PostgreSQL query. Canonical
response digests matched across revisions and transports for each tenant and
page size. A and B had distinct digests with the same receipt IDs and resource
ID. All 96 rejected controls recorded zero protected handler, query and result
work. Allowed paths checked scope, exact receipt order, continuation, field
order, redaction and unknown field omission. All measured connections reused
their verified TLS connection after warmup.

| Transport and page | Server allocated bytes/request, median before → after | Paired allocation | Paired p50 | Paired p95 | Paired p99 |
| --- | ---: | ---: | ---: | ---: | ---: |
| HTTP, 25 | 666,231 → 637,345 | −4.34% | −0.88% | +3.10% | +5.69% |
| GraphQL, 25 | 627,585 → 598,288 | −4.72% | +3.06% | +4.86% | +6.05% |
| HTTP, 200 | 4,662,504 → 4,416,870 | −5.12% | −8.89% | −2.20% | −2.62% |
| GraphQL, 200 | 4,247,738 → 4,015,688 | −5.42% | −2.67% | +3.31% | −3.16% |

Percentages are medians of the four within-pair changes. They can differ from
the ratio of the independently aggregated before and after medians. All four
cells allocated fewer managed bytes. End-to-end latency moved in both
directions, so this supports no overall latency improvement claim. Allocation
includes managed server process background work and the snapshot protocol.
It excludes Python client and PostgreSQL allocations. Pressure from this
one sequential client does not establish throughput, production qualification
or a result against the original benchmark gates. The optional reader
readTimeout and concurrency limits were left unset in both lanes.

Preflight 01 stopped in seed at the missing base schema. Preflight 02 seeded
but stopped before TLS due to the Python context manager mismatch. Preflight 03
passed both revisions, all 36 controls and eight page checks. Its verified
binaries were reused for the first and only timed matrix. Failed attempts,
source snapshots, builds and local stderr were retained in their own folders.
The public export includes numeric timings, counters, digests, hashes, the
seed receipt and a verifier. Credentials, raw response bodies and servers'
stderr stay local. The exact owned fixture stopped and its loopback listener
closed. Its volume remains for audit. [Samples harness](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/commit/34a1b3b3c4215ec9b222a03d0b2f0fa30361086e)

A Windows Release build with locked restore passed with no warnings or errors.
The no-argument entrypoint still exits successfully with its setup guide.
The provider measurement evidence is from WSL. [Samples CI](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/actions/runs/45125221539)

GitHub and Docs synced append-only updates to #7, #8 and #18. Readback matched
all 23 issues with all Project values preserved. #3 stays Blocked. The original
benchmark criteria and #20 mirror remain intact.
