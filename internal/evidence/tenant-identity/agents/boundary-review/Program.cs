using System.Text.Json;
using Cehpalon.Engine.Core;
using Cehpalon.Engine.Identity;
using Cehpalon.Engine.Tenancy;

var results=new List<object>();
foreach(var name in new[]{"monotonic duration despite UTC rollback within validity","expired lease resurrection after UTC rollback"})
{
    var fixture=new Fixture(); var blocked=false;
    fixture.Action=(ctx)=>
    {
        if(name.StartsWith("monotonic",StringComparison.Ordinal)) fixture.Clock.Advance(TimeSpan.FromSeconds(31),TimeSpan.FromSeconds(20));
        else
        {
            fixture.Clock.Advance(TimeSpan.FromSeconds(31),TimeSpan.FromSeconds(31));
            try { ctx.DemandAccess(Fixture.Tenant,"document","shared","document.read"); }
            catch(TenantAccessDeniedException) { }
            fixture.Clock.Advance(TimeSpan.FromSeconds(1),TimeSpan.FromSeconds(-26));
        }
        try { ctx.DemandAccess(Fixture.Tenant,"document","shared","document.read"); }
        catch(TenantAccessDeniedException) { blocked=true; throw; }
    };
    var result=await fixture.Dispatcher.DispatchAsync<string,int>("document.read","shared",new OperationContext("independent-review"));
    results.Add(new {name,expected_rejection_observed=blocked,returned_success=result.IsSuccess,factory_calls=fixture.FactoryCalls,dispose_calls=fixture.Disposed});
}
var json=JsonSerializer.Serialize(new {observed_at_utc=DateTimeOffset.UtcNow,scope="Independent fake-clock lease repro; not provider/identity/production or benchmark proof",results},new JsonSerializerOptions {WriteIndented=true});
Console.WriteLine(json);
if(args.Length>0) await File.WriteAllTextAsync(args[0],json+"\n");

sealed class Clock:TimeProvider
{
    private DateTimeOffset now=Fixture.Now; private long ticks;
    public override DateTimeOffset GetUtcNow()=>now;
    public override long GetTimestamp()=>ticks;
    public override long TimestampFrequency=>TimeSpan.TicksPerSecond;
    public void Advance(TimeSpan elapsed,TimeSpan utc){ticks+=elapsed.Ticks;now+=utc;}
}
sealed class Fixture:IIdentitySource,ITenantMembershipSource,IResourceScopeSource,ITenantAccessPolicy
{
    public static readonly DateTimeOffset Now=new(2026,10,27,14,0,0,TimeSpan.Zero);
    public static readonly TenantId Tenant=new("A");
    public static readonly PrincipalId Principal=new("urn:review:issuer","subject");
    public Clock Clock=new(); public Action<TenantOperationContext>? Action; public int FactoryCalls,Disposed;
    public TenantOperationDispatcher Dispatcher {get;}
    public Fixture()
    {
        var registry=new TenantOperationRegistryBuilder().Register<string,int>("document.read","document.read","document",request=>request,request=>new(Tenant,request),()=>{FactoryCalls++;return new Handler(this);}).Build();
        Dispatcher=new(registry,new TenantSecurityServices(this,new IdentityTrustPolicy([Principal.Issuer],["fixture"]),this,this,TimeSpan.FromSeconds(30),this,Clock));
    }
    public ValueTask<IdentitySnapshot?> ResolveAsync(CancellationToken token)=>ValueTask.FromResult<IdentitySnapshot?>(new(Principal,"fixture",Now.AddHours(-1),Now.AddHours(1)));
    public ValueTask<TenantMembershipSnapshot?> ResolveAsync(IdentitySnapshot id,TenantId tenant,CancellationToken token)=>ValueTask.FromResult<TenantMembershipSnapshot?>(new(new(Principal.Issuer,Principal.Subject),new(tenant.Value),true,Now.AddHours(-1),Now.AddHours(1),"m1"));
    public ValueTask<ResourceScopeSnapshot?> ResolveAsync(TenantId tenant,string kind,string id,CancellationToken token)=>ValueTask.FromResult<ResourceScopeSnapshot?>(new(new(tenant.Value),kind,id,"r1"));
    public ValueTask<bool> IsAllowedAsync(TenantAccessRequest request,CancellationToken token)=>ValueTask.FromResult(true);
    private sealed class Handler(Fixture fixture):ITenantOperationHandler<string,int>,IDisposable
    {
        public ValueTask<OperationResult<int>> HandleAsync(string request,TenantOperationContext context,CancellationToken token)
        {fixture.Action?.Invoke(context);return ValueTask.FromResult(OperationResult<int>.Success(1));}
        public void Dispose()=>fixture.Disposed++;
    }
}
