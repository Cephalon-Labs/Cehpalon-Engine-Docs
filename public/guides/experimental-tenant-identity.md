# Experimental tenant/identity boundary

Status: portable component/fixture proof only. No real IdP, JWT validation, database/RLS, job/event/cache/retrieval transport or production isolation is qualified by these contracts.

Identity snapshots are immutable representations, not credentials. Configure a trusted `IIdentitySource`, exact issuer/scheme trust policy, membership/resource sources and an explicit access policy. Established protocol adapters must authenticate first; caller-created DTOs or Core metadata cannot grant authority. A missing policy denies.

Register a tenant operation with fixed server-owned operation/action/resource-kind, a pure defensive snapshot callback, a target selector over that snapshot and a newly owned handler factory. Resource lookup takes tenant selection plus resource key, then the dispatcher verifies returned actual ownership and exact principal membership. Same resource IDs may exist independently in A and B.

```csharp
var registry = new TenantOperationRegistryBuilder()
    .Register<ReadDocument, DocumentView>(
        "documents.read", "documents.read", "document",
        request => new(request.Tenant, request.DocumentId),
        frozen => new(new TenantId(frozen.Tenant), frozen.DocumentId),
        () => new DocumentReader(checkedStore))
    .Build();
var dispatcher = new TenantOperationDispatcher(registry, trustedServices);
```

`ITenantOperationHandler` receives a checked `TenantOperationContext`; use its `DemandAccess` and server resource/version when accessing a provider. The context is internally minted, checked against UTC validity and a monotonic elapsed cap, permanently revoked after observed invalidity, and revoked after invocation cleanup. An active reference is a data-bound capability that trusted code can pass to helpers; this is not a C# sandbox or atomic provider authorization transaction.

Protected entrypoints must route through the tenant dispatcher. Code generation and plain Core dispatch do not add authorization automatically. The [runnable consumer](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/tenant-identity) uses a generated stateless Core gateway that delegates into this boundary and one tenant-aware business handler for both tenants.

Pre-dispatch denials perform zero business factory/constructor/read/write work. Gateway and authority lookup work may still occur. Expiry/cancellation after creation must release the owned handler; later denial does not undo previous side effects. Unexpected provider/cleanup faults remain faults rather than ordinary denial results. Fresh next-call checks do not promise instantaneous distributed revocation inside an existing operation.

Do not use this generic scope as a signed token or accept a context from request metadata. Real protocol lifecycle, provider transactions/RLS, connection pooling, envelopes and cache/retrieval filtering need their own qualified adapters. See [ADR-0007](../../internal/adr/ADR-0007-tenant-identity-operation-boundary.md).
