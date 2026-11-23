# 2026-11-23 Public read timeout API

Following the internal readDeadline rename, Engine now exposes
ActivateWithReadTimeout on tenant-wide history, exact receipt lookup and exact
resource history. The old ActivateWithBudget signatures forward to the same
implementation. There is no obsolete warning or default timeout change.
Null keeps the original caller token and guard order. Disabled policies skip
the source factory. Configured timeouts remain cooperative with the same
bounds, cancellation classification and provider ownership.
[Naming decision](../adr/ADR-0051-optional-audit-read-budget.md)

The protected Samples transport host uses the new name at both receipt lookup
and resource history. Existing Samples contract suites passed eight offline
checks and eight real HTTPS/PostgreSQL wire checks. Its untimed preflight
passed 36 admission and validation controls, eight page checks, and eight
actual PostgreSQL Lock cases. The configured timeout and the caller
cancellation paths joined the exact backend before reuse. All 24 rejected
requests performed zero handler, query or result work.

A second lane started from the prior executable compiled against
ActivateWithBudget. A detached copy swapped only Cehpalon.Engine.Tenancy.dll.
The old consumer DLL and all other files matched the retained inputs by hash.
It was not recompiled and passed the same eight wire checks, 36 controls,
eight page checks and eight lock cases. This exercises both API names under
the actual receipt and resource transport host.

The Engine Audit Trail suite passed 250/250. Its existing cases now exercise
the new name by default and compare the old name for disabled factories,
bounds, original null-mode tokens and faults, and configured linked-token
reads. WSL used SDK 11.0.100, Npgsql 10.0.3 and PostgreSQL 18.7. Both live
lanes used fresh schemas on the existing owned fixture. The container stopped,
its port closed and its volume was retained. No timing matrix or original
benchmark change was part of this naming proof.

[Engine commit](https://github.com/Cephalon-Labs/Cehpalon-Engine/commit/5f49b3b25ae13c9e57321d6436c429b5cb712775)
[Samples commit](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/commit/113271fca815e246d82b9d7c0fe962477569ba6b)
[Reports and checksums](../evidence/audit-read-timeout-api/2026-11-23)

The Windows sample build passed with locked restore and zero warnings or
errors. Its no-argument setup path also passed. Hosted Engine artifacts report
1,526 Windows and 1,523 Ubuntu contract checks, including all 250 Audit Trail
checks on both at the exact commit. Both platform smoke jobs passed.
[Contract CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/45138408682)
[Platform smoke CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/45138408986)

Body-only sync updated #7, #8 and #18. Readback matched all 23 mirrors with
all Project values preserved. #3 remains Blocked, #20 is byte-identical, and
the original benchmark criteria remain in force. Existing user files were
preserved.
