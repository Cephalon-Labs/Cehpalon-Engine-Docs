# 2026-11-23 Audit history read allocation

This Engine continuation applies to #18 and the #7/#8 regression boundary in
[ADR-0049](../adr/ADR-0049-exact-resource-history-query.md). Resource history now
compares receipt GUIDs directly. The public order remains ascending lowercase
Guid-N with ordinal comparison. `Guid.CompareTo(Guid)` compares the canonical
components as unsigned fields, which preserves that order, including values
above signed integer limits. [Microsoft API documentation](https://learn.microsoft.com/en-us/dotnet/api/system.guid.compareto)

Read projection searches the existing immutable field rules using their
ordinal sort and skips rule lookup for metadata-only results. The shared
operation/action/resource lookup keeps the exact case-sensitive match and
projected records preserve field order, allowlisting, redaction and capture
provenance. Tenant and cursor checks, budget and cancellation checkpoints,
provider contracts and wire shapes keep their existing behavior.

The allocation probe used the same prebuilt 200-row pages and policy settings
in two isolated Release builds with SDK 11.0.100 on Windows x64. An actual
checked tenant dispatcher established the scope. The in-memory source and
reader completed synchronously. For each workload the probe verified the
result and performed 32 warmup reads, then five groups of 32 reads. Median
bytes allocated per page on the reading thread were:

| Fixture | Before | After | Reduction |
| --- | ---: | ---: | ---: |
| Metadata only | 53,168 | 13,080 | 75.4% |
| One field | 193,968 | 131,480 | 32.22% |
| 64 field rules | 2,608,422 | 1,149,337 | 55.94% |

These are allocation observations for the in-memory reader. This run did not
measure latency, SQL, wire serialization, throughput or the original benchmark.
The probe source, raw allocation samples, Engine assembly SHA-256 values and
Audit Trail report are in the [evidence directory](../evidence/audit-history-read-cost/2026-11-23).
To reproduce the probe, copy the two `.txt` sources as `Program.cs` and
`Probe.csproj` and build Release with `-p:ProbeEngineRoot=<clean Engine checkout>`.
Use separate probe build directories for the two revisions.

The Audit Trail suite passed 250/250. New cases cover a full canonical page
after a bookmark and case-sensitive field lookup, redaction, omission and
output order with 64 rules. Existing tests cover cross-tenant sources, bound
cursors, cancellation and expiry. Small API passed 40/40 and Security API
passed 651/651 against the candidate assembly in clean Samples source
`a1ef28f`. The first local Audit Trail invocation used the wrong argument
format and exited before running checks. Its local log remains separate from
the successful report.

The Engine commit is [4dedaee](https://github.com/Cephalon-Labs/Cehpalon-Engine/commit/4dedaeec12a6ae1e0d0d9313d79aa5d62113e7fa).
Hosted contract artifacts confirm 1,526 Windows and 1,523 Ubuntu checks from
the exact clean Engine revision. Audit Trail passed 250/250 on each runner.
Both SDK and driver smoke jobs passed. [Contract CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/45121450358)
[Platform smoke CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/45121450504)
GitHub and Docs synchronized append-only updates to #7, #8 and #18. Readback
matched all 23 mirrors and preserved Project metadata. Issue #3 remains
Blocked and the benchmark criteria remain in force.
