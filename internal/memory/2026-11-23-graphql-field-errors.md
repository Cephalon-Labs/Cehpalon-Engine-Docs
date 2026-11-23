# 2026-11-23 GraphQL field errors during F5

The user reported `HotChocolate.GraphQLException: Access denied.` at
`GraphQLOperationCatalog.TypedField.Resolve` while troubleshooting F5. Small API
and Security API self-tests deliberately send denied requests. The reported
stack points to the translation of a denied operation result into a GraphQL
field error. In a controlled loopback reproduction, Hot Chocolate handled the
exception and returned the expected client response, while the CLR delivered
three first-chance notifications for `GraphQLException`.

The adapter now reports field errors directly through Hot Chocolate and
returns null for the failed field. Authentication before dispatch, policy
decisions, cancellation, and sanitization of host faults keep their existing
contracts. Expected denials still return HTTP 200 with `access.denied` in the
GraphQL envelope. An allowed sibling field still returns data. The startup
profiles in Samples use the adapter through project references.

The new regression checks the status, code, message, aliased error path, null
denied field, and allowed sibling data. On the prior adapter it failed on the
three first-chance notifications. On the new adapter it observed zero, and all
48 GraphQL contracts passed. Both Debug executables launched with empty
arguments against the new adapter. Small API passed 40/40 and Security API
passed 651/651. These runs instrumented CLR exceptions and did not drive the
Visual Studio F5 UI. The original benchmark was not rerun, and #3 remains
Blocked under the same acceptance criteria.

Local evidence remains in `.local/graphql-field-errors` in the isolated Engine
and Samples worktrees. A verifier draft initially assumed optional GraphQL
source locations were present in the baseline response. The final regression
checks the baseline's actual error path. An isolated Samples checkout also hit
Windows path limits in historical evidence. The successful runs explicitly
built the project files against the isolated Engine checkout from an existing
clean Samples worktree.

The Engine commit is on `main`. Both hosted workflows passed on Windows and
Ubuntu at that revision. [Engine commit](https://github.com/Cephalon-Labs/Cehpalon-Engine/commit/887c529c5975e37bd53082896b56d7eff448dbbc),
[contract CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/45117043695),
[platform smoke CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/45117043711).

GitHub and Docs synchronized two append-only updates to #9 and #11. All 23
issue mirrors matched on readback. Issue and Project metadata stayed intact.
