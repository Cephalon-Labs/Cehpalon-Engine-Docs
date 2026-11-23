# 2026-11-23 Optional audit read statistics

Projects may pass a caller-owned `TenantChangeAuditReadStatistics` to any of
the three audit readers using the five-argument `ActivateWithReadTimeout`
overload. `GetSnapshot()` independently samples success, reader deadline,
caller cancellation and fault totals. Initial input, permission and caller
cancellation rejections do not count. Empty reads count as successes. Configured
deadlines use the existing caller-first classification. With a null timeout, a
cancellation counts as a caller outcome when its exception carries the
signaled caller token. Provider and other admitted failures count as faults.
The collector counts at the reader boundary, after awaited provider work
and before any wire serialization. It stores no identity or payload data.

The Sample host enables sharing with `CollectReadStatistics = true`. Its
`ReadStatistics` property is null by default and with both transports
disabled. Timeout wire reporting remains independently configurable.

The two collection modes passed 20 matching HTTPS controls each against
PostgreSQL 18.7. The enabled mode passed the counter transitions and mixed
GraphQL sharing. Both modes denied four cross-tenant requests before SQL.
The Windows Samples build and the four hosted Engine jobs passed. This
delivery did not measure the collector's latency or allocation overhead.

Tracking readback matched all 23 task mirrors. Only the bodies of #7, #8
and #18 received entries. #3 remains Blocked and #20 remains In Progress.
All Project fields, original benchmark criteria and pending user file
hashes were verified.

[Validation protocol and results](../validation/audit-read-statistics.md)
[Published evidence](../evidence/audit-read-statistics/2026-11-23)
