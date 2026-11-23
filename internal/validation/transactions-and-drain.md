# PostgreSQL transaction overlap and protected HTTPS drain

## PostgreSQL order transactions

The optional application sample runs its existing migration and tenant
controls first. A separate test phase opens up to two application
connections and one unpooled observer. The application uses checked
Engine tenant contexts and the restricted Npgsql role. The observer
examines the participants' own PostgreSQL state and blocker IDs. Each
order operation uses one READ COMMITTED transaction.

| Case | Evidence |
| --- | --- |
| Distinct tenants, same order ID | Both UPDATEs entered their post-write gates on distinct backends. PostgreSQL observed both transactions open. Tenant B committed while A remained held, then A committed. Each row advanced one revision. B's returned backend had no tenant scope or visible rows. |
| Same tenant, same order and expected revision | PostgreSQL observed an active UPDATE waiting on a lock held by the first backend. After release, one update committed and the other conditional update affected zero rows. The final revision was one. The original still-eligible wrong-revision case independently exercises the revision predicate. |
| Cancel a blocked UPDATE | PostgreSQL reported the expected blocker before cancellation. Npgsql returned the caller token and PostgreSQL SQLSTATE `57014`. The waiter acknowledged rollback. The pool returned that same backend without tenant scope or visible rows while the holder still had its lease. |

Each run closed its owned fixture and retained the container, volume and
loopback cleanup outcomes in the receipt. The proof covers PostgreSQL
18.6, Npgsql 10.0.3 and selected conditional writes. Concurrent behavior
for other queries, lock patterns and providers has its own scope. The
test holds ordering gates and observes actual database state. Performance
and commit acknowledgement fault qualification have separate gates.
The exact Samples commit was `4ba83d1de32f59a9eca42afb00a754a3fab2a9c1`.
Engine `6fe7254404cf6b148370bd95befe8331e8932354` ran with .NET
SDK 11.0.100 and runtime 11.0.0 on WSL Ubuntu 22.04.5.
[Local provider receipt](../evidence/transactions-and-drain/2026-11-24/postgres/wsl.json) · [Protocol](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/blob/4ba83d1de32f59a9eca42afb00a754a3fab2a9c1/multitenant-business/postgres/OVERLAP-PROTOCOL.md) · [Previous application controls](postgresql-application-scope.md)

## Protected HTTPS drain and fresh activation

The generated Small API was built from Engine
`5e92ac1c7fa1e150e7e97de6d68e94b31ffba053` with locked dependencies.
The Samples proof adds fixture-only controls for the outer dispatcher
observer, a cleanup gate and access to the actual admission budget.

The total-budget case holds an admitted GraphQL mutation and lets cleanup
succeed. The tenant-budget case holds an admitted HTTP mutation and faults
after running the underlying cleanup. Admission closes with one operation
active and capacity two. While the listener remains online, the proof
checks the authorized overload response and generic message on HTTP and
GraphQL, the authenticated cross-tenant denial and anonymous 401. These
calls invoke no business factory or write. Canceling one independent
drain wait leaves the admitted work and shared drain in place.

The admitted operation reaches actual owned cleanup before the gate
releases. The generated host shutdown stays pending, the permit remains
active and no completion is recorded for that operation while cleanup is
held. Releasing it produces one outer completion with matching native
ASP.NET request Activity and the expected success or fault. The HTTP
fault response represents the synthetic cleanup failure after one
in-memory write. It uses the generic 500 envelope and excludes the
private fixture sentinel. The old listener closes. A fresh host in the same
process receives successful owner requests through both transports with
an open, empty budget and initial in-memory catalog state. Its listener
also closes after disposal.

The first Windows attempt found a parser error in the probe. HTTP
problem details and GraphQL use different message fields. The corrected
full matrix retained the exact public message checks and the first
failed attempt was kept locally. The final ordinary trace-mode Windows
regression also passed 17 wire cases, with 16 completions and 34
histogram observations.
[Earlier correlation proof](dispatch-correlation.md) · [Existing admission contract](operation-budget-drain.md)

This is a controlled graceful restart of the generated HTTPS fixture.
The probe closes the budget explicitly before normal host disposal.
The restart recreates the in-memory store in the same process. Persistent
data recovery, exporter behavior and original workload qualification
have separate gates.

Windows 11 build 26300 and WSL Ubuntu 22.04.5 each passed 18 wire cases
with 14 completion records, 20 histogram observations and zero unscoped
signals. Their case receipts matched. The exact Samples fixture was
`ba1525611521ad0d3624821059604f2a557a126a`.
[Wire receipts and build manifests](../evidence/transactions-and-drain/2026-11-24/https/) · [Fixture protocol](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/ba1525611521ad0d3624821059604f2a557a126a/tooling-small-api/dispatch-correlation)

## Hosted CI and delivery

Samples PR 3 passed the protected HTTPS proof on Windows Server 2025 and
Ubuntu 24.04 and the disposable PostgreSQL order proof on Ubuntu 24.04.
The successful hosted HTTPS receipts matched both local case matrices.
The hosted PostgreSQL receipt confirms all three concurrency cases and
owned cleanup. The checked-out PR tree matched the branch head and
merged Samples main. The Engine revisions remained pinned to each
proof's declared source.

On the first hosted attempt, Windows HTTPS and Ubuntu PostgreSQL ran
successfully. Ubuntu HTTPS stopped at argument parsing because the runner
resolved multiple dotnet executables. The workflow selected one executable
from PATH on the next full matrix, with the existing SDK version and
proof assertions. [Passing workflow](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/actions/runs/45237963550) · [First hosted run](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/actions/runs/45237547376) · [Revision and job receipts](../evidence/transactions-and-drain/2026-11-24/hosted.json)

#7 remains Blocked, #12 remains Backlog and #18 remains In Progress at
M0. Their broad acceptance criteria and benchmark gates remain open.
