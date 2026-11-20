# Experimental configurable audit history and trails

Status: bounded local contracts and generated HTTPS consumer proof. Existing operation history and explicit domain-change history are independently selectable. No real durable database/outbox/CDC, retention/tamper-evidence or production audit profile is certified by this guide.

## Choose the project format

| Mode | Recorded state | Value-factory work |
| --- | --- | --- |
| Disabled | No trail recorder/history provider activation | None |
| MetadataOnly | Who, tenant, operation/action, entity, receipt, observed/reported time and versions | None |
| ChangedFields | Allowed changed fields, with typed before/after values or redacted markers | One trusted state factory when fields are enabled |
| BeforeAfterSnapshots | Before/after values for allowed fields, including unchanged fields | One trusted state factory when fields are enabled |

Default policy mode is MetadataOnly. Whole feature activation remains optional. Empty or unmatched operation/action/resource-kind rules deny recording; unknown history rules return metadata only. MetadataOnly and an empty matching field allowlist do not invoke the trusted state factory. Applications can bind project configuration to these immutable settings, select separate policies for different operations and supply their own append/history providers. Validate intended recording rules against the application operation catalog before accepting mutations. To change an immutable policy, create/select a recorder or reader using the new policy; no automatic configuration watcher or hot-reload lifecycle is installed.

```csharp
var policy = new TenantChangeAuditPolicy(
    TenantChangeAuditMode.ChangedFields,
    [new TenantChangeAuditRule("document.update", "write", "document",
        [new("title"), new("classification"),
         new("sensitiveNote", redact: true)])]);
var recorder = TenantChangeAuditRecorder.Activate(policy, () => trustedStore);
// Inside the checked tenant operation, using an application/provider change receipt:
await recorder!.RecordAsync(context, providerReportedReceipt,
    () => new TenantChangeStates(beforeState, afterState), cancellationToken);
```

Leave the module unselected or select Disabled to skip provider factories and constructors. Select exact fields deliberately: unknown fields are omitted, and both sides of a redacted field become fixed markers before the sink sees the record. Original typed values determine WasChanged before redaction, so a changed secret remains visible as a redacted change. Current read policy is applied again to stored history. Tightening rules can hide older values; selecting a richer mode cannot recreate state that was never captured or restore redacted values.

## Integrate with actual changes

The application/provider reports an explicit TenantChangeReceipt after its chosen mutation/commit handling; the framework does not infer committed database state from request or response DTOs. Receipt principal/issuer, scheme, tenant, operation/action, entity kind/ID and authorization-resource version must match an active TenantOperationContext. BeforeEntityVersion and AfterEntityVersion are separate domain versions: the authorization-resource version might represent an ACL rather than a data row. Create uses a correctly authorized reserved entity scope. A receipt constructor does not prove a commit.

Build immutable TenantChangeState values from actual before/after entity snapshots. Supported scalar representations distinguish Missing from Null and include Text, Boolean and Decimal. Text/fields/states/records have finite limits; complex application types need explicit bounded scalar projection. No reflection/object-graph capture or automatic JSON serialization is installed. Exclude credentials/session identifiers from capture rules or explicitly redact sensitive fields. Text preserves well-formed source characters, including controls; providers and UIs must use structured escaped encoding.

Stable receipt IDs support application/provider idempotency. They are not a fabricated link to the automatic operation InvocationId or caller correlation. ReportedAtUtc is provider supplied; RecordedAtUtc is observed by the recorder.

## Read history and handle failure

TenantChangeAuditHistoryReader requires the distinct audit-trail/tenant/read checked scope. Ordinary operation-metadata history permission does not grant field history. The facade validates page size/tenant ownership, rechecks active context after asynchronous reads/projection and applies current project redaction. Implement retention, storage encryption, integrity verification and pagination in the selected provider.

Required append has an independent bounded cancellation budget; the provider must cooperate. After a reported mutation, expiry/cancellation/append failure can mean data already changed and the trail may or may not have persisted. TenantChangeAuditWriteException exposes MayHaveCommitted. There is no automatic retry, rollback or exactly-once guarantee. Unhandled recorder failures become operation faults. The sample explicitly maps them to audit_trail.write_failed_may_have_committed and an operation rejection; callers must not infer unchanged data or blindly repeat the mutation. Atomic database/outbox integration belongs to the application/provider transaction. Browser cookie authentication also needs host-owned CSRF/cookie protections; this trail API does not configure browser security.

Automatic TenantAuditServices still records authorization and terminal processing metadata separately. A terminal event reflects the processing outcome computed before required persistence, not atomic network delivery. Session observation restrictions survive checked identity copies/tenant/read-set contexts. Use WithValidity/IntersectValidity when wrapping those snapshots so you retain their original restrictions; reconstructing a public DTO neither authenticates nor preserves private constraints. This is an in-process trusted-host boundary, not a C# sandbox or continuous distributed session revocation.

See the [generated security consumer](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/security-api), [decision](../../internal/adr/ADR-0039-configurable-audit-trails.md) and [validation report](../../internal/planning/observation-audit-trails.md). Original benchmark gates and #3 Blocked remain unchanged.
