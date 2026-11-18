# Tenant concurrency budget handoff

The 2026-11-18 continuation adds a protected total and per-tenant cap in Engine `baaabf1af720b1c8f021b124663323e5b4c959d0`. The immutable limits share one counter and a bounded map of active tenant identities derived from verified resource scopes. Counts release after owned cleanup. Small API exposes an optional per-tenant flag and a dedicated protected HTTPS self-test.

Local contracts passed 517 Windows and 514 WSL checks. The actual Small API passed 150 verification checks on each host. The new case demonstrates that one tenant can be full while a peer uses spare host capacity and both cross-tenant directions still deny. See the [report](../planning/tenant-concurrency-budget.md) and the [validation protocol](../validation/tenant-concurrency-budget.md).

#18 and #20 remain In Progress. #3 remains Blocked because the successful hosted smoke leaves the real PostgreSQL and RabbitMQ checks unrun. Canonical benchmarks remain as recorded. There were no GitHub usage or billing skips in this delivery. When a future GitHub step hits usage or billing, record the exact pending step and continue local work.
