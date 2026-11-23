# 2026-11-24 PostgreSQL overlap and protected HTTPS drain

The user asked to continue from the scoped PostgreSQL order and dispatch
correlation proofs. The PostgreSQL sample added a two-connection READ
COMMITTED phase, with a separate observer using the fixture runtime role.
WSL verified concurrent commits for distinct tenants, one committed
transition and one zero-row conditional result for the same order, and
cancellation during an actual lock wait. The canceled backend was reused
without tenant scope or visible rows while the holder still owned its
lease. Existing migration and sequential scope controls passed first.

The generated protected HTTPS proof tested total and tenant admission under
held owned cleanup. Windows and WSL passed 18 wire cases each, with 14
completion records, 20 histogram observations and zero unscoped signals.
The receipt distinguishes the held GraphQL success from the HTTP
cleanup fault and confirms fresh in-process host activation through both
transports. The ordinary Windows trace regression matched the prior
receipt byte-for-byte. [Combined validation](../validation/transactions-and-drain.md)

Samples PR 3 adds a focused hosted workflow for those proofs. The initial
Ubuntu HTTPS job stopped before the verifier because PowerShell expanded
multiple dotnet matches into arguments. The fix selects the first
application in PATH and retains the original SDK version guard. The
earlier Windows parser correction kept the same public message
expectations for HTTP and GraphQL. See the validation report for hosted
run conclusions.

#7 remains Blocked, #12 Backlog and #18 In Progress at M0. Continue
incrementally with bounded query semantics and separately scoped migration
or outcome-ambiguity proof for PostgreSQL. For #18, the remaining scope
includes external sink behavior, fault recovery and performance under the
declared reference conditions. The #18 issue body is close to its API
limit. Keep full evidence in Docs and preserve old journal text when a
future tracking update needs space.
