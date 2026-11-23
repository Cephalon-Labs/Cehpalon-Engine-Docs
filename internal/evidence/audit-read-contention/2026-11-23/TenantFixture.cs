using Cehpalon.Engine.Core;
using Cehpalon.Engine.Identity;
using Cehpalon.Engine.Tenancy;

sealed class TenantFixture : IIdentitySource, ITenantMembershipSource, IResourceScopeSource, ITenantAccessPolicy
{
    public static TenantId Tenant { get; } = new("A");
    private static readonly DateTimeOffset Stamp = DateTimeOffset.UnixEpoch.AddDays(500);
    private static readonly PrincipalId Principal = new("issuer", "alice");

    public ValueTask<IdentitySnapshot?> ResolveAsync(CancellationToken token) =>
        ValueTask.FromResult<IdentitySnapshot?>(new(Principal, "Bearer", Stamp.AddMinutes(-1), Stamp.AddMinutes(10)));

    public ValueTask<TenantMembershipSnapshot?> ResolveAsync(IdentitySnapshot identity, TenantId tenant, CancellationToken token) =>
        ValueTask.FromResult<TenantMembershipSnapshot?>(new(identity.Principal, tenant, true, Stamp.AddMinutes(-1), Stamp.AddMinutes(10), "member"));

    public ValueTask<ResourceScopeSnapshot?> ResolveAsync(TenantId tenant, string kind, string id, CancellationToken token) =>
        ValueTask.FromResult<ResourceScopeSnapshot?>(new(tenant, kind, id, "acl"));

    public ValueTask<bool> IsAllowedAsync(TenantAccessRequest request, CancellationToken token) => ValueTask.FromResult(true);

    public async Task Run(Action<TenantOperationContext> work)
    {
        var registry = new TenantOperationRegistryBuilder().Register<string, bool>(
            "trail.lookup", "read", "audit-trail", resource => resource, resource => new(Tenant, resource),
            () => new Handler(work)).Build();
        var services = new TenantSecurityServices(this, new(["issuer"], ["Bearer"]), this, this,
            TimeSpan.FromMinutes(1), this, new FixedUtcClock());
        var result = await new TenantOperationDispatcher(registry, services)
            .DispatchAsync<string, bool>("trail.lookup", "tenant", new("audit-read-contention-probe"));
        if (!result.IsSuccess)
            throw new InvalidOperationException("Trusted tenant fixture denied or failed the experiment.");
    }

    private sealed class Handler(Action<TenantOperationContext> work) : ITenantOperationHandler<string, bool>
    {
        public ValueTask<OperationResult<bool>> HandleAsync(string request, TenantOperationContext context, CancellationToken token)
        {
            work(context);
            return ValueTask.FromResult(OperationResult<bool>.Success(true));
        }
    }

    private sealed class FixedUtcClock : TimeProvider
    {
        public override DateTimeOffset GetUtcNow() => Stamp;
    }
}
