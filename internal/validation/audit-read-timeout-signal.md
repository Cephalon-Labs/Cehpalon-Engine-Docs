# Opt-in audit timeout wire signal

Declared 2026-11-23 under #18 and #7/#8 authority regressions. This
continues the optional reader deadline in ADR-0051 and the protected
transport adapters in ADR-0052 and ADR-0053.

The four-argument ActivateWithReadTimeout overload selects a typed
TenantChangeAuditReadTimeoutException for the reader's own configured
deadline. The existing signatures still throw the exact prior plain
TimeoutException for reader expiry. Caller cancellation takes priority;
unrelated cancellation and non-cancellation failures, including a plain
provider TimeoutException, retain their original behavior. The reader still
awaits and joins provider work. No hard I/O or HTTP response deadline is added.

The Samples host offers an init-only ReportReadTimeout option. It is false
by default and only applies with a positive selected ReadTimeout. Map the
typed failure inside each checked audit handler while preserving cancellation
and normal cleanup. HTTP returns 504 and GraphQL returns a field error.
Both use the fixed audit.read_timeout code and fixed public message. Default
timeout and ordinary provider failures still use the generic internal error.
Export HTTP 504 only for selected HTTP routes under the effective option.
GraphQL field shape and the old default wire contract remain intact.

Verify all three Engine readers, exact default exception compatibility, and
the HTTP/GraphQL redaction mappings. Run the existing offline and real-provider
wire suites. In an untimed WSL fixture with PostgreSQL 18.7 and Npgsql 10.0.3,
verify the 504 schema opt-in and 20 real HTTPS controls over both operations
and protocols. Each cell covers typed expiry, legacy expiry, unrelated
provider TimeoutException after real SQL, caller abort and a cross-tenant
request. Observe the exact tagged PostgreSQL Lock wait before timeout/abort,
retain the lock until the backend is quiescent, prove no failed result is
published, then verify a fresh successful read. Cross-tenant denial must
perform zero handler or SQL work. Record checks and preserve prior data.
No timed benchmark, threshold, maturity, or #3 status change.
