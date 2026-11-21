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

### Validate and prepare before mutation

For declared audited operations, prefer validation against the actual frozen tenant registry before loading the sink:

```csharp
var recorder = TenantChangeAuditRecorder.ActivateValidated(
    policy, tenantRegistry, ["document.update"], () => trustedStore);
// Inside the checked handler, before application data effects:
var prepared = recorder?.Prepare(context, cancellationToken);
var change = await applicationMutation(cancellationToken); // application/provider code
if (prepared is not null)
    await prepared.CompleteAsync(change.Receipt,
        () => new TenantChangeStates(change.Before, change.After), cancellationToken);
```

`DescribeOperations()` exposes immutable operation/action/resource-kind metadata without invoking handlers, request freezers or target selectors. Enabled validated activation checks every configured rule and every explicitly required operation before invoking the sink factory. Disabled skips catalog/required-enumeration/provider work. Required audited operations are declared by the host; action names do not imply auditing.

Use the **same registry instance** for activation and dispatch. Identical rebuilt registries, including two snapshots from the same builder, do not share the private binding. Keep request identity/security services fresh. Preparation performs live-context/origin/rule/cancellation checks without storage or payload work. Before-effect denial/cancellation does not assert a commit happened. It can run inside an already-created handler; the guarantee is no application mutation when that check fails.

Completion captures the original context and recorder and consumes the preparation before receipt validation, callbacks or I/O. Null/misbound receipts, cancellation, failed first attempts, concurrent losers and replay all consume/fail with possible-commit semantics; at most one facade append attempt occurs per preparation. This is not backend exactly-once or an automatic retry. New configurations do not retarget or instantly revoke old preparations bound to their immutable owner.

Callers **must await completion after effects**. Preparation neither reserves storage nor forces/automates completion: abandoning it can leave changed data without a trail and requires application reconciliation. Context must remain active. The original direct `Activate`/`RecordAsync` API remains available and can still discover a rule error after effects; upgrading the library alone does not migrate application flow. Atomic transaction/outbox behavior remains provider/application responsibility.

The application/provider reports an explicit TenantChangeReceipt after its chosen mutation/commit handling; the framework does not infer committed database state from request or response DTOs. Receipt principal/issuer, scheme, tenant, operation/action, entity kind/ID and authorization-resource version must match an active TenantOperationContext. BeforeEntityVersion and AfterEntityVersion are separate domain versions: the authorization-resource version might represent an ACL rather than a data row. Create uses a correctly authorized reserved entity scope. A receipt constructor does not prove a commit.

Build immutable TenantChangeState values from actual before/after entity snapshots. Supported scalar representations distinguish Missing from Null and include Text, Boolean and Decimal. Text/fields/states/records have finite limits; complex application types need explicit bounded scalar projection. No reflection/object-graph capture or automatic JSON serialization is installed. Exclude credentials/session identifiers from capture rules or explicitly redact sensitive fields. Text preserves well-formed source characters, including controls; providers and UIs must use structured escaped encoding.

Stable receipt IDs support application/provider idempotency. They are not a fabricated link to the automatic operation InvocationId or caller correlation. ReportedAtUtc is provider supplied; RecordedAtUtc is observed by the recorder.

### Await mutation and recording together

For a new integration, `ExecuteAsync<TResult>` keeps the mutation callback and required trail completion in one awaited flow. Use it **inside the active checked handler**, with the same validated recorder/registry. Disabled auditing must still run ordinary business behavior:

```csharp
if (recorder is null)
{
    var change = await applicationMutation(cancellationToken);
    return change.Result;
}
return await recorder.ExecuteAsync(context, async token =>
{
    var change = await applicationMutation(token);
    return new TenantChangeAuditMutation<MyResponse>(
        change.Receipt, change.Result,
        () => new TenantChangeStates(change.Before, change.After));
}, cancellationToken);
```

Here `applicationMutation`, its returned change and `MyResponse` belong to the consuming application. It must report the actual chosen provider operation; constructing a receipt is not proof of a commit. The envelope is immutable, while arbitrary response object graphs remain application-owned. Metadata-only and empty-field policies skip its lazy state factory. The disabled branch constructs neither the envelope nor audit state; application-owned snapshot work should also be selected explicitly.

Null callback, failed preparation and pre-invocation cancellation occur before the callback. Once invocation starts, all failures conservatively report `MayHaveCommitted`, including a callback that changes data then throws or cancels without returning a receipt. That case has no fabricated trail and needs application reconciliation. The helper invokes its callback once and does not automatically retry either the mutation or append. Separate calls can each change data; there is no cross-call idempotency.

After a receipt returns, the helper awaits checked completion using the private write deadline and then checks caller cancellation before returning the result. Thus caller cancellation alone does not suppress required persistence after a returned receipt; it can withhold a result after the append succeeded. Invalid/expired scope, invalid receipt, provider failure or private timeout can still prevent/fail recording. Direct `CompleteAsync(receipt, values, callerToken)` retains its earlier caller-token checks. Timeouts are cooperative: a provider or mutation that ignores cancellation can remain pending. The helper cannot force a consumer to await it or make database changes and trails atomic. No transaction/outbox, hard deadline or guaranteed delivery is implied. See [ADR0041](../../internal/adr/ADR-0041-audit-execution.md).

### Select a provider transaction and outbox

Projects can select the experimental transaction/outbox integration instead of direct required append. Its success means the business change **and pending outbox record committed together in the selected provider transaction**. It does not mean the final history sink has received that record. Existing direct APIs keep their earlier behavior.

```csharp
// Only invoke this activation when the project's outbox capability is selected.
var executor = TenantChangeAuditOutboxExecutor<IDocumentMutationSession>
    .ActivateValidated(policy, tenantRegistry, ["document.update"],
        () => projectTransactionProvider);
// Inside the active checked document handler:
if (executor is null)
    return await ordinaryApplicationMutation(cancellationToken);
return await executor.ExecuteAsync(context, async (session, token) =>
{
    var change = await session.UpdateAsync(request, token);
    return new TenantChangeAuditMutation<MyResponse>(change.Receipt, change.Result,
        () => new TenantChangeStates(change.Before, change.After));
}, cancellationToken);
```

`IDocumentMutationSession`, its method and response are application-owned ports. Implement `ITenantChangeAuditTransactionProvider<TSession>` so that every mutation through Session and every `StageAsync` use the **same actual transaction**, with immutable tenant binding and no use after completion/disposal. Commit/rollback lifecycle is separate from Session. An application that performs effects outside that transaction cannot obtain rollback protection for those effects. Provider acquisition must not mutate business data and must clean partial initialization itself if it fails.

Validated activation checks the actual catalog before the provider factory; Disabled skips it. Metadata/field modes and lazy redaction use the same checked projection as direct audit recording. Only the frozen, redacted record enters outbox storage. Do not persist raw state graphs or callbacks. Do not auto-commit inside the mutation callback or retain its session for later work.

`TenantChangeAuditTransactionException` exposes `Outcome`, `PrimaryFailure`, `RollbackFailure`, `DisposalFailure` and `MayHaveCommitted`. `RolledBack` requires provider rollback acknowledgement before any commit attempt. Failed rollback is `RollbackUnknown`; an error after commit invocation is `CommitUnknown`, with no automatic retry or rollback claim. Successful commit remains `Committed` even if later cancellation, scope expiry or disposal withholds the response. Inspect the outcome before reconciliation; repeating a request may repeat business work. Commit/rollback budgets are cooperative and do not forcibly terminate providers or arbitrary mutation callbacks.

### Drain under fresh service authority

Select relay independently and call it explicitly; the Engine installs no worker, timer or network endpoint:

```csharp
var relay = TenantChangeAuditOutboxRelay.Activate(projectRelayEnabled,
    () => projectOutboxSource, () => projectIdempotentHistorySink);
// Inside a NEW configured service operation checked for audit-outbox/tenant/relay:
if (relay is not null)
    await relay.RelayAsync(relayContext, maximum: 64, cancellationToken);
```

Dispatch a fresh trusted service identity through normal tenant checks for each bounded relay call. The original writer may have logged out or its request scope may have ended; that context must not be reused. Writer and history-reader permissions do not grant relay permission. Disabling new capture does not erase already queued records; the project chooses whether to keep draining them. All-off selection invokes neither executor nor relay providers.

The source claims at most128 immutable unique records for one tenant, with an opaque lease GUID and expiry. Relay validates the complete batch before the first sink call, checks live scope and local UTC/monotonic validity, and acknowledges only after `AppendOnceAsync` accepts the record. The provider must enforce exact tenant/lease/receipt/expiry compare-and-set for acknowledgement and fence-specific release. Stale cleanup must not clear another worker's claim. A lease cannot be renewed by this facade.

The sink must deduplicate `(tenant, receiptId)`: identical payload replay succeeds; conflicting payload fails. Sink success followed by acknowledgement loss/expiry can therefore replay. Earlier records in a batch may already be delivered/acknowledged when a later record fails. `TenantChangeAuditOutboxRelayException` exposes acknowledged count, possible delivery, primary and release failures. There is no automatic drop/dead-letter, business retry, atomic batch delivery or backend exactly-once guarantee. Replay preserves the original frozen payload/capture mode; current read policy may hide more, while queued-data changes require explicit provider retention/migration.

The owned PostgreSQL/Npgsql consumer demonstrates the tested same-database transaction/fence/dedup behavior. Portable interfaces alone do not prove a provider's atomicity, durability or isolation, and the fixture is not a production or native Windows database qualification. See [ADR0042](../../internal/adr/ADR-0042-audit-transaction-outbox.md) and the [conformance protocol](../../internal/validation/audit-outbox.md).

### Select a cooperative relay budget

The original `Activate` entrypoint retains its signature and behavior. A project can instead select a nullable work budget through the distinct `ActivateWithBudget` entrypoint:

```csharp
var relay = TenantChangeAuditOutboxRelay.ActivateWithBudget(
    projectRelayEnabled,
    relayTimeout: projectRelayTimeout, // TimeSpan?; null keeps legacy behavior
    sourceFactory: () => projectOutboxSource,
    sinkFactory: () => projectIdempotentHistorySink,
    leaseDuration: TimeSpan.FromSeconds(15));
```

Configured budgets must be positive and at most one minute. Disabled selection skips validation and provider factories. The system timer starts before claim and remains active through final success validation; the optional `timeProvider` still controls lease UTC/monotonic checks. Claim, sink and acknowledgement receive linked caller/private cancellation. Release keeps its own five-second cleanup token, including after caller cancellation or work-budget expiry. The facade awaits uncooperative I/O and cleanup, so elapsed wall time can exceed the selected budget.

With a configured budget, observed caller cancellation retains the original caller token and takes precedence over a simultaneously observed private expiry. Private expiry reports a generic `TimeoutException`; unrelated provider failures remain distinct. Inner diagnostics are for trusted host code and must not be serialized to public responses. Null budget keeps the original token/error behavior.

A late known claim is released before failure is returned; a late null claim also fails rather than reporting zero. Pre-lease claim failure provides no handle for Engine cleanup: the trusted source owns partial-acquisition recovery/expiry. Once a sink call is attempted, delivery may have happened even if acknowledgement count is zero. A budget expiring during cleanup can withhold success after every acknowledgement. Inspect `TenantChangeAuditOutboxRelayException` counts and separate primary/release failures, then reconcile or explicitly retry with fresh authority and the same idempotent receipt payload. Timeout is not rollback, a renewed lease or automatic retry. See [ADR0045](../../internal/adr/ADR-0045-cooperative-outbox-relay-budget.md).

### Deliver several batches with explicit work limits

`DrainAsync` is a manual sequential helper on the same optional relay. Call it inside one newly authorized `audit-outbox/tenant/relay` operation:

```csharp
var progress = relay is null ? null : await relay.DrainAsync(
    relayContext, maximumBatches: 8, maximumRecords: 500,
    maximumPerBatch: 64, cancellationToken: cancellationToken);
```

Defaults are16batches,2048acknowledgements and128perbatch; those are also the experimental upper caps. Each batch requests at most the remaining record allowance. A positive short batch continues, while zero acknowledgements returns `NoProgress`; reaching a record or batch cap returns `RecordLimit` or `BatchLimit`. `CompletedBatches` counts successful relay invocations, including a final zero-progress one. Counts describe acknowledgements, not unique business effects. NoProgress does not establish an empty backlog: other workers can hold claims or locks, and concurrent writers may add records. No status/history query or permission is added.

Existing `ActivateWithBudget` timeouts remain **per batch**. The helper adds no overall timer, elapsed-time guarantee, parallel workers, failed-batch retry, delay, quarantine or background loop. Each batch owns its existing fenced release. The original checked scope is revalidated between batches and at completion; this does not resolve identity/membership sources anew for each batch. Use a fresh dispatcher operation for a later manual call.

Projects can separately opt into a total cooperative budget spanning multiple batches:

```csharp
var progress = relay is null ? null : await relay.DrainWithBudgetAsync(
    relayContext, drainTimeout: TimeSpan.FromSeconds(10),
    maximumBatches: 8, maximumRecords: 500, maximumPerBatch: 64,
    cancellationToken: cancellationToken);
```

Null retains the original DrainAsync behavior. A configured total must be positive and at most one minute. It starts after initial admission and stays active through all batches and their cleanup; per-batch budgets remain independent. Cancellation is cooperative: the Engine awaits uncooperative I/O and independent fenced release rather than abandoning work. A total-budget timeout therefore sets no hard completion deadline. Caller cancellation preserves the original caller token. Relevant cancellation signals are classified when the primary failure is selected, before cleanup; a later signal does not replace an already selected provider error, per-batch timeout or total timeout. Release-only failures remain separate. Acknowledgements remain visible even when expiry during cleanup withholds success. Existing progress and authority limits apply. See [ADR0047](../../internal/adr/ADR-0047-total-outbox-drain-budget.md).

The first failure stops subsequent calls. `TenantChangeAuditOutboxDrainException` retains the exact child `PrimaryFailure`/inner reference, started/completed batch counts, acknowledgements from completed and interrupted batches, aggregate acknowledgements and possible delivery. A provider rethrowing an older RelayException cannot contribute another invocation's partial totals: current partial observations require a private owned terminal marker. Earlier delivery/acknowledgement can remain committed, including when cancellation/scope failure withholds a final result. Do not interpret failure or zero known acknowledgements as rollback/no delivery. Raw inner diagnostics remain trusted-host-only. See [ADR0046](../../internal/adr/ADR-0046-bounded-outbox-drain.md).

### Inspect outbox status without reading payloads

Projects may independently select `TenantChangeAuditOutboxStatusReader`. Disabled activation skips its provider factory; the Engine installs no polling loop, metrics listener or endpoint:

```csharp
var inspector = TenantChangeAuditOutboxStatusReader.Activate(
    projectOutboxStatusEnabled, () => projectStatusSource);
// Inside a NEW configured operation checked for audit-outbox/tenant/inspect:
var status = inspector is null
    ? null
    : await inspector.ReadAsync(inspectContext, cancellationToken);
```

Implement `ITenantChangeAuditOutboxStatusSource` for the chosen provider. The immutable result exposes only its tenant, provider observation UTC, five counts and nullable oldest pending enqueue UTC. `Pending = Available + Claimed`; Claimed means active unexpired claims, while Available includes unclaimed and expired-claim pending records. `ExpiredClaims` is a subset of Available. `Delivered` counts retained outbox rows marked delivered, and need not equal a separately retained history table. Oldest is null exactly when no records are pending. Count relationships are validated without overflowing `long`.

Grant inspect separately from relay, domain writes and field-history reads. Every call requires a live checked context and verifies returned tenant ownership after I/O. Public DTO construction is not authority. Provider timestamps describe that observation; the facade does not compare them to a client clock to invent freshness or grant access. Counts may change immediately after the statement and are not a global health verdict or a recovery command. Reading must not claim, acknowledge, release or alter records.

Default read budget is5seconds, configurable to a positive value up to1minute. Caller cancellation retains its token; observed private-budget expiry without caller cancellation reports `TimeoutException`, including a provider that completes late after ignoring cancellation. The facade still awaits an uncooperative source, so this is not a hard deadline. Timeout Message is generic; inner provider cancellation details remain for trusted diagnostics and must not be serialized directly to public responses. Other provider failures remain distinct. Existing adapters retain unexpected-error redaction. No caching or automatic retries are installed.

The PostgreSQL example calculates all counts and oldest pending database enqueue time in one tenant-filtered statement with one clock observation. It adds enqueue metadata only when creating new owned fixture schemas; no automatic migration of existing outboxes is installed. See [ADR0043](../../internal/adr/ADR-0043-outbox-operational-status.md).

## Read history and handle failure

Projects can select the experimental PostgreSQL indexed storage sample through its optional Composition Support module. It implements the existing sink, receipt-lookup and resource-history ports; no Engine API change is required. A validated immutable plan precedes module factory, credential access and initialization. Disabled selection has no module-owned factory/connection/DDL/query work. Existing mutation/read gateways retain fresh tenant grants and current-policy projection.

This profile stores resource metadata and the established escaped TEXT payload atomically in a new versioned table, with an exact tenant/resource/receipt index. Conditional append accepts only identical metadata and payload for a repeated key; conflicting replay faults without overwriting the visible record. Duplicate UPSERTs can still create MVCC/index/vacuum work. Resource reads filter in SQL, validate selected physical metadata against decoded receipt and keep typed receipt-key continuation semantics. NUL-bearing field values remain supported without SQL JSON conversion. Selective reads do not continuously inspect unrelated rows or prove tamper-free storage, chronological snapshots or speedup.

CreateNew and OpenExisting are explicit, separate initialization modes. Opening verifies the expected version/table/columns/collations/PK/index and rejects unsupported schema behavior; it never repairs or migrates. This is point-in-time validation under trusted database administration. The module lease owns provider lifetime and rejects retained new work after disposal. Existing and indexed histories are distinct: there is no automatic backfill, dualwrite, cutover or replay of previously acknowledged receipts. Outbox Delivered does not identify which history store received the record. Plan migration before changing a real deployment's sink.

See [ADR0050](../../internal/adr/ADR-0050-optional-indexed-audit-storage.md) and [profile evidence](../../internal/planning/indexed-audit-storage.md). The initial evidence covers correctness and actual index/query plans; index existence and a diagnostic plan do not establish production performance. Legacy streaming storage remains available.

Projects can independently select bounded history for one exact resource kind/id:

```csharp
var resourceHistory = TenantChangeAuditResourceHistoryReader.Activate(
    currentProjectReadPolicy, () => projectResourceHistorySource);
var query = new TenantChangeAuditResourceQuery("document", "shared", limit: 50);
// Inside an operation freshly checked for audit-trail/tenant/read:
var page = resourceHistory is null ? null : await resourceHistory.ReadAsync(
    historyContext, query, cancellationToken);
// A later fresh request can reuse page.NextCursor with the same filters.
```

Implement `ITenantChangeAuditResourceHistorySource`. Limit1..200; kind/id equality is ordinal. The immutable typed continuation binds tenant, filters and last receipt. The reader validates input binding before provider work, every returned identity and strictly advancing canonical Guid-N receipt order before projection, and continuation consistency with the last returned row. Page size can change. Empty pages still receive completion guards; nonempty underfilled pages may have continuation. Disabled activation skips the source factory. Captured immutable read policy and current-policy selection work like exact receipt lookup.

Receipt-key order defines pagination; chronological order and stable snapshots need a separate provider contract. New keys before a bookmark can be missed, later keys can appear, and deletion/retention can remove rows or the bookmark. Public cursors are selection data with binding checks, without cryptographic authenticity. They do not grant tenant, resource read/write or field-history authority, and no new endpoint is installed. The legacy pagination and exact receipt APIs remain.

The sample's compatible PostgreSQL profile streams existing tenant/receipt-ordered TEXT and decodes with its established codec before exact managed resource filtering. This preserves valid escaped-NUL field values that JSON/JSONB processing cannot generally handle. It retains at most limit+1 matching records plus the current decoded row; page size does not bound total scan/decoding/elapsed time or all driver buffering. Caller cancellation is cooperative and reader disposal may drain remaining data. Malformed scanned payloads fail closed, including unrelated resources. Storage indexing and scan performance need separate evidence. See [ADR0049](../../internal/adr/ADR-0049-exact-resource-history-query.md).

Projects can independently select exact history lookup by a known receipt:

```csharp
var lookup = TenantChangeAuditLookupReader.Activate(
    currentProjectReadPolicy, () => projectLookupSource);
// Inside an operation freshly checked for audit-trail/tenant/read:
var record = lookup is null ? null : await lookup.FindAsync(
    historyContext, receiptId, cancellationToken);
```

Implement `ITenantChangeAuditLookupSource` over the selected history store. Disabled activation skips its factory. An activated reader requires a nonempty receipt and live checked history scope, passes the original caller token and validates both returned tenant and receipt before projecting the record through its configured immutable read policy. Caller/scope checks also run after a null result and before return. Configure a new reader when changing that policy; the reader does not reload project configuration automatically. Existing pagination APIs remain unchanged.

A null result describes absence from that selected history store at the read. It can include pending outbox publication or retention and does not prove never committed, globally absent or unhealthy delivery. Receipt IDs can repeat across tenants. Relay, inspect and ordinary operation-history permission do not grant field-history access. A DTO or receipt ID is not authority. The Engine installs no lookup endpoint or background work; route service requests through fresh protected dispatch and retain unexpected-error redaction. Provider failures remain original trusted-host diagnostics, and uncooperative reads are awaited. See [ADR0048](../../internal/adr/ADR-0048-exact-audit-receipt-lookup.md).

TenantChangeAuditHistoryReader requires the distinct audit-trail/tenant/read checked scope. Ordinary operation-metadata history permission does not grant field history. The facade validates page size/tenant ownership, rechecks active context after asynchronous reads/projection and applies current project redaction. Implement retention, storage encryption, integrity verification and pagination in the selected provider.

Required append has an independent bounded cancellation budget; the provider must cooperate. After a reported mutation, expiry/cancellation/append failure can mean data already changed and the trail may or may not have persisted. TenantChangeAuditWriteException exposes MayHaveCommitted. There is no automatic retry, rollback or exactly-once guarantee. Unhandled recorder failures become operation faults. The sample explicitly maps them to audit_trail.write_failed_may_have_committed and an operation rejection; callers must not infer unchanged data or blindly repeat the mutation. Atomic database/outbox integration belongs to the application/provider transaction. Browser cookie authentication also needs host-owned CSRF/cookie protections; this trail API does not configure browser security.

Automatic TenantAuditServices still records authorization and terminal processing metadata separately. A terminal event reflects the processing outcome computed before required persistence, not atomic network delivery. Session observation restrictions survive checked identity copies/tenant/read-set contexts. Use WithValidity/IntersectValidity when wrapping those snapshots so you retain their original restrictions; reconstructing a public DTO neither authenticates nor preserves private constraints. This is an in-process trusted-host boundary, not a C# sandbox or continuous distributed session revocation.

See the [generated security consumer](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/security-api), [decision](../../internal/adr/ADR-0039-configurable-audit-trails.md) and [validation report](../../internal/planning/observation-audit-trails.md). Original benchmark gates and #3 Blocked remain unchanged.


Projects can select a separate cooperative budget for change-audit history, exact receipt lookup and resource-history reads:

```csharp
var resourceHistory = TenantChangeAuditResourceHistoryReader.ActivateWithBudget(
    currentProjectReadPolicy, TimeSpan.FromSeconds(5), () => projectResourceHistorySource);
// The history and receipt-lookup readers offer the same ActivateWithBudget shape.
// Call from a fresh checked audit-trail/tenant/read operation context.
var page = resourceHistory is null ? null : await resourceHistory.ReadAsync(
    historyContext, query, cancellationToken);
```

A non-null budget is positive and at most one minute. Disabled policies skip the source factory; null keeps the original constructor/Activate behavior, provider token and legacy checks. Configure a new reader to change its policy or budget. Each configured read owns an independent system timer and linked token spanning provider work, validation, projection and completion checks. Original-caller cancellation takes precedence over an observed private expiry; otherwise expiry is a TimeoutException. Unrelated cancellation and non-cancellation provider faults retain the declared trusted-host diagnostics. Existing checked-scope, tenant, cursor and current-policy validation still applies to null/empty results.

The reader awaits providers that ignore cancellation and does not dispose their lifetime. This is cooperative cancellation, without a hard elapsed bound, rollback or atomic response-delivery deadline. Providers own any additional asynchronous work and callbacks; callbacks must not block/throw or wait for reader completion. The local PostgreSQL sample exercises the legacy history/lookup/resource and indexed lookup/resource ports through generated protected dispatch; indexed storage does not offer tenant-wide history. See [ADR0051](../../internal/adr/ADR-0051-optional-audit-read-budget.md) and the [read-budget report](../../internal/planning/audit-read-budget.md). Runtime maturity and original benchmark gates remain unchanged.


The Samples `audit-outbox` receipt transport host can expose exact indexed lookup through HTTPS POST `/audit/receipts/lookup` and GraphQL `trailReceipt`. Select either transport or neither. It uses an explicit primitive wire DTO bridge to the existing generated lookup gateway, then the checked reader and immutable project read policy. Successful absence remains a nullable record from the selected history store. The wire receipt includes resource kind and captured/current modes; identifiers and tenant values never grant access.

Supply trusted TLS/authentication configuration, an explicit JWT scheme/issuer trust and fresh project membership/resource/RBAC-ABAC providers. The host reads identity from the current validated ASP.NET ticket. Local fixture-service authorities are not a serving authentication path. Compile the Composition plan before owned callbacks; disabled selection opens no owned source or listener. A selected source is a newly constructed PostgresIndexedAuditStorage opened with read-only OpenExisting, with test seeding/provisioning separate. Startup catalog SQL is distinct from request lookup SQL.

Admission closes before shutdown, and admitted server work joins before storage disposal, including stop failures and uncooperative post-SQL completion. A canceled HttpClient task does not prove server/provider completion. Read budgets are cooperative and end at reader completion, excluding DTO serialization and network delivery. Existing error redaction/status semantics remain. This is a bounded indexed PostgreSQL sample, with local signed-token fixtures; resource-history transports, legacy lookup transports, external IdP/session/production and performance qualification remain separate. See [ADR0052](../../internal/adr/ADR-0052-protected-audit-receipt-transports.md) and the [receipt transport report](../../internal/planning/audit-receipt-transports.md).


The existing sample host also supports resource history: set `ResourceHistoryEnabled = true` on its options to expose POST `/audit/resources/history` and GraphQL `trailResourceHistory`. `ReceiptLookupEnabled` defaults true and can independently be disabled; resource history defaults false. Its four positional options and activation call remain compatible. Receipt-only, resource-only and combined modes share one indexed source and shutdown owner. Both reads off, or both transports off, performs no owned activation/listener work.

Send tenant, exact resource kind/id, limit1..200 and optional continuation. The primitive continuation contains tenant/kind/id and last receipt Guid. Input bounds and Ordinal binding are validated before querying; actual authority still comes from the validated request ticket and fresh project checks. Grant `trail.resource-history` separately from lookup, entity access and ordinary history. Responses contain projected primitive entries and nullable next cursor using the same record mapper as lookup.

Reuse a returned cursor with the same tenant/filters and optionally a different limit. A caller-created compatible missing bookmark is valid selection metadata. Pagination follows Guid-N receipt-key order, without chronological, snapshot or cryptographic authenticity guarantees; inserts/deletions can change later pages. The indexed source can return empty or underfilled terminal pages, and uses limit+1 lookahead. No response-byte or elapsed bound follows from the entry limit. Current read policy, selected physical identity checks and cooperative budget remain; budget ends before wire mapping/flush. Mixed receipt/resource requests fully join before the single storage owner disposes. See [ADR0053](../../internal/adr/ADR-0053-protected-audit-resource-history-transports.md) and the [resource transport report](../../internal/planning/audit-resource-history-transports.md).

## Optional shared audit-read admission

The experimental indexed audit transport host can share one total/per-tenant capacity budget across receipt lookup and resource history, HTTP and GraphQL:

```csharp
var options = new AuditReceiptTransportOptions {
    ResourceHistoryEnabled = true,
    ConcurrencyLimits = new AuditReadConcurrencyLimits(
        MaximumConcurrentReads: 16, MaximumConcurrentReadsPerTenant: 4)
};
```

These example limits are project choices, not measured deployment capacity. Null keeps the original unlimited dispatch path. Selected limits must be positive and the tenant limit cannot exceed the total. Disabled profiles ignore unused limits and activate no owned budget/source/listener. Each host owns its own budget.

Established JWT identity and fresh membership/resource/RBAC-ABAC checks run before admission. Capacity uses the authorized tenant, shared across operations and transports; same resource/receipt IDs remain tenant-isolated. Rejections use `operation.capacity_exceeded` (HTTP503 or a GraphQL error) before business handler/provider work. No waiting queue, fairness, rate or distributed capacity guarantee.

Capacity covers protected dispatch and owned-handler completion. Authentication, DTO mapping, serialization and wire delivery are outside that interval. Caller abort or cooperative timeout cannot release a slot while the handler is still completing. Shutdown closes both admissions, stops the app and fully joins work before disposing the source, even when stop fails. Optional `ConcurrencySnapshot` contains aggregate counts only; no tenant-tagged metric or listener is created.

[Decision and limitations](../../internal/adr/ADR-0054-audit-read-concurrency-admission.md) · [Validation](../../internal/planning/audit-read-admission.md). Local indexed PostgreSQL/token fixtures remain M0 and do not establish throughput, native Windows DB, external IdP or production capacity.
