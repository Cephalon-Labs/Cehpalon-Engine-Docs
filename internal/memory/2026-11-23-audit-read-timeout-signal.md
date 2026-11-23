# 2026-11-23 Opt-in audit read timeout signal

A caller can distinguish a configured Engine audit reader deadline from a
provider failure when the application selects that behavior. The four-argument
ActivateWithReadTimeout overload opts into TenantChangeAuditReadTimeoutException.
The default overloads still emit exactly plain TimeoutException for that
deadline. Provider TimeoutException stays the same exception, and an available
caller abort takes precedence. The reader still awaits the provider.
[Validation protocol](../validation/audit-read-timeout-signal.md)

Samples exposes ReportReadTimeout as an init-only option. With a selected
positive ReadTimeout, it maps the typed expiry for checked receipt lookup and
resource history to HTTP 504 or a GraphQL field error with code
audit.read_timeout and the fixed message "The audit read deadline expired."
The option defaults to false. Unexpected provider errors remain redacted as
internal.error. The selected HTTP OpenAPI export includes 504 only when the
option is effective. GraphQL uses its existing errors envelope.

Audit Trail passed 253, HTTP 53 and GraphQL 49 in the exact WSL build. The
existing audit offline and wire suites each passed eight cases. The new real
PostgreSQL 18.7 HTTPS fixture passed the schema check and 20 combinations
across both readers and transports. Twelve cases observed the exact tagged
SQL backend waiting on a PostgreSQL lock and proved it quiescent before
unlock. Four cross-tenant cases did zero source queries or handler work.
Four provider-failure cases used a controlled plain TimeoutException after
actual SQL and retained the generic response. Every case proved successful
reuse and zero failed-result publication.

The dedicated fixture reused the existing owned WSL container after identity
verification, seeded a new schema and retained existing data. It stopped
after the tests and its loopback port closed. This was untimed functional
verification. No canonical benchmark or provider/production gate changed.
Captured reports contain synthetic status, counters and hashes. Raw machine
logs and absolute build paths are retained locally. The published input hash
list uses relative paths.

[Engine commit](https://github.com/Cephalon-Labs/Cehpalon-Engine/commit/0836fe3eafdfb647bd8c3ddaeb983768beba2ea0)
[Samples commit](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/commit/6b6cac0d1b524c7b90132f9672f0f16b14f5e7b9)
[Reports and verifier](../evidence/audit-read-timeout-signal/2026-11-23)

The Windows sample build passed with locked restore and zero warnings or
errors. Its no-argument setup path passed. Hosted Engine artifacts report
1,531 Windows and 1,528 Ubuntu checks at the exact commit, including the
253/53/49 audit and transport suites. Both platform smoke jobs passed.
[Contract CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/45149695719)
[Platform smoke CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/45149695720)

GitHub and Docs appended updates to #7, #8, #9 and #18. All 23 mirrors matched
after readback and every Project value was preserved. #3 remains Blocked.
#20 and original benchmark criteria are intact, as are the user's local edits.
