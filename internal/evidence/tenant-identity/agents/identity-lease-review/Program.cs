using System.Text.Json;
using Cehpalon.Engine.Core;
using Cehpalon.Engine.Identity;
using Cehpalon.Engine.Tenancy;

var start=new DateTimeOffset(2026,10,27,12,0,0,TimeSpan.Zero);
var clock=new Clock(start); var principal=new PrincipalId("fixture:issuer","alice");var tenant=new TenantId("tenant-a");
var identity=new IdentitySnapshot(principal,"fixture",start.AddSeconds(-1),start.AddHours(1));
var events=new List<string>();
var registry=new TenantOperationRegistryBuilder().Register<string,int>("doc.read","doc.read","document",r=>r,r=>new(tenant,r),()=>new Handler(clock,start,tenant,events)).Build();
var services=new TenantSecurityServices(new Source(identity),new IdentityTrustPolicy(["fixture:issuer"],["fixture"]),new Member(principal,tenant,start),new Resource(tenant),TimeSpan.FromSeconds(30),new Policy(),clock);
var result=await new TenantOperationDispatcher(registry,services).DispatchAsync<string,int>("doc.read","document-a",new("review"));
Console.WriteLine(JsonSerializer.Serialize(new{scope="Independent in-process still-active lease clock rollback repro; no realprovider or identityproof",result=result.Value,resurrected=result.Value==1,events},new JsonSerializerOptions{WriteIndented=true}));

sealed class Clock(DateTimeOffset now):TimeProvider { public DateTimeOffset Now=now; public override DateTimeOffset GetUtcNow()=>Now; }
sealed class Source(IdentitySnapshot snapshot):IIdentitySource { public ValueTask<IdentitySnapshot?> ResolveAsync(CancellationToken ct)=>ValueTask.FromResult<IdentitySnapshot?>(snapshot); }
sealed class Member(PrincipalId principal,TenantId tenant,DateTimeOffset start):ITenantMembershipSource { public ValueTask<TenantMembershipSnapshot?> ResolveAsync(IdentitySnapshot identity,TenantId requested,CancellationToken ct)=>ValueTask.FromResult<TenantMembershipSnapshot?>(new(principal,tenant,true,start.AddSeconds(-1),start.AddHours(1),"v1")); }
sealed class Resource(TenantId tenant):IResourceScopeSource { public ValueTask<ResourceScopeSnapshot?> ResolveAsync(TenantId requested,string kind,string id,CancellationToken ct)=>ValueTask.FromResult<ResourceScopeSnapshot?>(new(tenant,kind,id,"v1")); }
sealed class Policy:ITenantAccessPolicy { public ValueTask<bool> IsAllowedAsync(TenantAccessRequest request,CancellationToken ct)=>ValueTask.FromResult(true); }
sealed class Handler(Clock clock,DateTimeOffset start,TenantId tenant,List<string> events):ITenantOperationHandler<string,int>
{
 public ValueTask<OperationResult<int>> HandleAsync(string request,TenantOperationContext context,CancellationToken ct)
 {
   clock.Now=start.AddSeconds(31);
   try { context.DemandAccess(tenant,"document",request,"doc.read");events.Add("Unexpectedly accepted after expiry"); }
   catch(TenantAccessDeniedException) { events.Add("Denied after expiry"); }
   clock.Now=start.AddSeconds(1);
   try { context.DemandAccess(tenant,"document",request,"doc.read");events.Add("Accepted after clock rollback");return ValueTask.FromResult(OperationResult<int>.Success(1)); }
   catch(TenantAccessDeniedException) { events.Add("Remained denied after clock rollback");return ValueTask.FromResult(OperationResult<int>.Success(0)); }
 }
}
