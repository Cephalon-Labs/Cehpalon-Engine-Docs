# 2026-11-23 PostgreSQL tenant scope and connection reuse

The user asked to continue the roadmap. #18 now has concurrent audit
collector measurements and a trace/log proposal. In the Business lane,
the original PostgreSQL probe was updated to follow the Samples GA SDK
pin, then executed against the pinned PostgreSQL 18.6 Linux image with
Npgsql 10.0.3. The default SQL and pool proof plus a restricted runtime
login proved same-backend scope clearing after commit and rollback. The
false-flag rollback and missing-password refusal were verified in
separate owned fixture runs. Both runtime cases saw the tenant's own row
for the shared order ID and zero unscoped rows. Every final container and
volume was removed and its loopback port closed.
[Verification](../validation/postgresql-runtime-pool.md)

#7 remains Blocked and #12 remains Backlog. Continue with a scoped
application-facing PostgreSQL transaction and migration contract that
uses checked tenant context. Keep work on #14 and #15 tied to the
provider and identity dependencies. #8 still needs real IdP lifecycle
and #11 still needs the dedicated Linux reference and separate load
driver. #20 benchmark qualification remains open.
