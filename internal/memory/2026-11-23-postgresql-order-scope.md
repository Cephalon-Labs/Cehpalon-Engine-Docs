# 2026-11-23 scoped PostgreSQL order operations

The user asked to continue after the initial PostgreSQL RLS and pool
proof. The optional Business sample now binds one typed order read and
one conditional update to an Engine-checked tenant resource and a restricted
PostgreSQL role. It has an explicit initial migration. Exact Samples
1bb96af and Engine 6fe7254 passed a real disposable PostgreSQL 18.6
fixture on WSL. Exercises included six zero-provider-work controls,
same-order-ID isolation, a stale revision on an eligible order, commit,
post-update cancellation rollback and same-backend scope clearing.
Migration rollback and repeat refusal passed. Local evidence and the
package/image pins are in the validation report.
[Application PostgreSQL proof](../validation/postgresql-application-scope.md)

#18 also delivered the Core completion observer with protected HTTPS
correlation. #7, #12 and #18 retain their status and maturity scopes.
Next, declare and prove overlapping transaction behavior and its
provider contract before widening to business migrations or eventing.
The full identity profile still needs an actual IdP and #11 still needs
the dedicated Linux reference and separate load generator.
[Completion observer evidence](../validation/dispatch-correlation.md)
