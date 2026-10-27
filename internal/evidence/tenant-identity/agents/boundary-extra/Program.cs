using System.Collections.Concurrent;
using System.Reflection;
using System.Text.Json;
using Cehpalon.Engine.Core;
using Cehpalon.Engine.Identity;
using Cehpalon.Engine.Tenancy;

var results=new List<object>(); var failures=0;
async Task Check(string name,Func<Task> body)
{
    try { await body();results.Add(new{name,passed=true}); }
    catch(Exception error) { failures++;results.Add(new{name,passed=false,error=error.ToString()}); }
}
void Assert(bool value,string message="assertion failed") {if(!value)throw new InvalidOperationException(message);}
void Denied(Action action) {try{action();}catch(TenantAccessDeniedException){return;}throw new InvalidOperationException("Expected scope rejection");}
await Check("public DTO construction exposes no grant or raw Core bridge",()=>
{
    Assert(typeof(TenantOperationContext).IsSealed && typeof(TenantOperationContext).GetConstructors().Length==0);
    Assert(typeof(TenantAccessRequest).GetConstructors().Length==0);
    Assert(typeof(TenantOperationDispatcher).GetProperties().All(p=>p.PropertyType!=typeof(OperationDispatcher) && p.PropertyType!=typeof(OperationRegistry)));
    Assert(typeof(TenantOperationContext).GetProperties().All(p=>p.SetMethod is null || !p.SetMethod.IsPublic));
    return Task.CompletedTask;
});
await Check("nested A then B revokes inner while restoring independent outer context",async()=>
{
    var auth=new Authority("alice","A","B");var business=new Business();var dispatcher=new TenantOperationDispatcher(business.Registry(),auth.Services());
    TenantOperationContext? inner=null;
    business.Body=async (request,context,token)=>
    {
        if(context.Tenant.Value=="A")
        {
            var reply=await dispatcher.DispatchAsync<Request,int>("document.read",new("B","shared"),new("nested"),token);
            Assert(reply.IsSuccess && reply.Value==22);
            Denied(()=>inner!.DemandAccess(new("B"),"document","shared","document.read"));
            context.DemandAccess(new("A"),"document","shared","document.read");
        }
        else { inner=context;Denied(()=>context.DemandAccess(new("A"),"document","shared","document.read")); }
        return business.Read(request,context);
    };
    var result=await dispatcher.DispatchAsync<Request,int>("document.read",new("A","shared"),new("outer"));
    Assert(result.IsSuccess && result.Value==11 && business.Created==2 && business.Disposed==2 && business.Reads==2);
});
await Check("one registry with two trusted identity sources overlaps without context crossover",async()=>
{
    var business=new Business();var registry=business.Registry();var a=new Authority("alice","A");var b=new Authority("bob","B");
    var da=new TenantOperationDispatcher(registry,a.Services());var db=new TenantOperationDispatcher(registry,b.Services());
    var ready=new TaskCompletionSource(TaskCreationOptions.RunContinuationsAsynchronously);var arrivals=0;var observed=new ConcurrentBag<string>();
    business.Body=async(request,context,token)=>
    {
        if(Interlocked.Increment(ref arrivals)==2)ready.SetResult();await ready.Task.WaitAsync(token);
        observed.Add(context.Tenant.Value+":"+context.Identity.Principal.Subject);
        Denied(()=>context.DemandAccess(new(context.Tenant.Value=="A"?"B":"A"),"document","shared","document.read"));
        return business.Read(request,context);
    };
    var replies=await Task.WhenAll(da.DispatchAsync<Request,int>("document.read",new("A","shared"),new("a")).AsTask(),db.DispatchAsync<Request,int>("document.read",new("B","shared"),new("b")).AsTask());
    Assert(replies.All(r=>r.IsSuccess) && observed.Order().SequenceEqual(new[]{"A:alice","B:bob"}) && business.Created==business.Disposed && business.Reads==2);
});
await Check("deep freeze survives real asynchronous authority wait and original nested mutation",async()=>
{
    var auth=new Authority("alice","A","B");var business=new Business();var started=new TaskCompletionSource(TaskCreationOptions.RunContinuationsAsynchronously);var release=new TaskCompletionSource(TaskCreationOptions.RunContinuationsAsynchronously);
    auth.IdentityHook=async()=>{started.SetResult();await release.Task;};
    business.Body=(request,context,_)=>{Assert(request.Tenant=="A" && request.Resource=="shared" && request.Tags.SequenceEqual(new[]{"A"}));return ValueTask.FromResult(business.Read(request,context));};
    var dispatcher=new TenantOperationDispatcher(business.Registry(),auth.Services());var original=new Request("A","shared");
    var pending=dispatcher.DispatchAsync<Request,int>("document.read",original,new("freeze")).AsTask();await started.Task;
    original.Tenant="B";original.Resource="not-authorized";original.Tags[0]="B";release.SetResult();
    var result=await pending;Assert(result.IsSuccess && result.Value==11 && auth.LastResourceLookup=="A:shared" && business.Reads==1);
});
await Check("provider-port guard rejects authoritative resource moved after policy lookup",async()=>
{
    var auth=new Authority("alice","A");var business=new Business();auth.PolicyHook=()=>business.ActualOwner="B";
    var dispatcher=new TenantOperationDispatcher(business.Registry(),auth.Services());
    var result=await dispatcher.DispatchAsync<Request,int>("document.read",new("A","shared"),new("move"));
    Assert(!result.IsSuccess && result.Error.Code=="access.denied" && business.Created==1 && business.Reads==0 && business.Disposed==1);
});
await Check("public identity-shaped metadata cannot authenticate anonymous source",async()=>
{
    var auth=new Authority("alice","A"){Anonymous=true};var business=new Business();var dispatcher=new TenantOperationDispatcher(business.Registry(),auth.Services());
    var counterfeit=new IdentitySnapshot(new("urn:review","admin"),"fixture",Authority.Now.AddMinutes(-1),Authority.Now.AddHours(1));
    var metadata=new Dictionary<string,string>{{"identity",JsonSerializer.Serialize(counterfeit)},{"tenant","A"},{"role","admin"},{"action","document.read"}};
    var result=await dispatcher.DispatchAsync<Request,int>("document.read",new("A","shared"),new("forged",metadata));
    Assert(!result.IsSuccess && result.Error.Code=="access.denied" && business.Created==0 && auth.MemberCalls==0 && auth.ResourceCalls==0);
});
await Check("source failure on a second invocation never reuses prior authorized grant",async()=>
{
    var auth=new Authority("alice","A");var business=new Business();var dispatcher=new TenantOperationDispatcher(business.Registry(),auth.Services());
    Assert((await dispatcher.DispatchAsync<Request,int>("document.read",new("A","shared"),new("first"))).IsSuccess);
    var old=business.LastContext!;auth.ResourceFailure=true;
    try{await dispatcher.DispatchAsync<Request,int>("document.read",new("A","shared"),new("second"));throw new Exception("Expected source failure");}catch(IOException){}
    Assert(business.Created==1 && business.Reads==1 && auth.IdentityCalls==2 && auth.MemberCalls==2);
    Denied(()=>old.DemandAccess(new("A"),"document","shared","document.read"));
});
await Check("execution and cleanup faults revoke retained context and preserve both failures",async()=>
{
    var auth=new Authority("alice","A");var business=new Business{CleanupFailure=true};business.Body=(_,_,_)=>throw new IOException("handler fixture");
    var dispatcher=new TenantOperationDispatcher(business.Registry(),auth.Services());
    try {await dispatcher.DispatchAsync<Request,int>("document.read",new("A","shared"),new("fault"));throw new Exception("Expected aggregate");}
    catch(AggregateException error){Assert(error.InnerExceptions.Count==2 && error.InnerExceptions[0] is IOException && error.InnerExceptions[1] is InvalidOperationException);}
    Assert(business.Created==1 && business.Disposed==1);Denied(()=>business.LastContext!.DemandAccess(new("A"),"document","shared","document.read"));
});
await Check("cleanup-only denial remains lifecycle failure after an authorized data read",async()=>
{
    var auth=new Authority("alice","A");var business=new Business{CleanupDenial=true};var dispatcher=new TenantOperationDispatcher(business.Registry(),auth.Services());
    try {await dispatcher.DispatchAsync<Request,int>("document.read",new("A","shared"),new("cleanup-denial"));throw new Exception("Expected lifecycle failure, not semantic denial result");}
    catch(InvalidOperationException error){Assert(error.InnerException is TenantAccessDeniedException);}
    Assert(business.Created==1 && business.Reads==1 && business.Disposed==1);
    Denied(()=>business.LastContext!.DemandAccess(new("A"),"document","shared","document.read"));
});
var report=new{observed_at_utc=DateTimeOffset.UtcNow,scope="Independent in-process adversarial boundary checks with copied peer DLLs; not real provider/identity/host/deployment/benchmark proof",passed=results.Count-failures,failed=failures,results};
var json=JsonSerializer.Serialize(report,new JsonSerializerOptions{WriteIndented=true});Console.WriteLine(json);if(args.Length>0)await File.WriteAllTextAsync(args[0],json+"\n");return failures==0?0:1;

sealed class Request(string tenant,string resource)
{
    public string Tenant=tenant,Resource=resource;public List<string> Tags=[tenant];
    public Request Copy()=>new(Tenant,Resource){Tags=Tags.ToList()};
}
sealed class FixedClock:TimeProvider {public override DateTimeOffset GetUtcNow()=>Authority.Now;}
sealed class Authority(string subject,params string[] tenants):IIdentitySource,ITenantMembershipSource,IResourceScopeSource,ITenantAccessPolicy
{
    public static readonly DateTimeOffset Now=new(2026,10,27,14,0,0,TimeSpan.Zero);
    public bool Anonymous,ResourceFailure;public int IdentityCalls,MemberCalls,ResourceCalls;public string? LastResourceLookup;
    public Func<Task>? IdentityHook;public Action? PolicyHook;
    public TenantSecurityServices Services()=>new(this,new IdentityTrustPolicy(["urn:review"],["fixture"]),this,this,TimeSpan.FromSeconds(30),this,new FixedClock());
    public async ValueTask<IdentitySnapshot?> ResolveAsync(CancellationToken token)
    {Interlocked.Increment(ref IdentityCalls);if(IdentityHook is not null)await IdentityHook();return Anonymous?null:new(new("urn:review",subject),"fixture",Now.AddMinutes(-1),Now.AddHours(1));}
    public ValueTask<TenantMembershipSnapshot?> ResolveAsync(IdentitySnapshot identity,TenantId tenant,CancellationToken token)
    {Interlocked.Increment(ref MemberCalls);return ValueTask.FromResult<TenantMembershipSnapshot?>(tenants.Contains(tenant.Value,StringComparer.Ordinal)?new(new(identity.Principal.Issuer,identity.Principal.Subject),new(tenant.Value),true,Now.AddMinutes(-1),Now.AddHours(1),"member-v1"):null);}
    public ValueTask<ResourceScopeSnapshot?> ResolveAsync(TenantId tenant,string kind,string resource,CancellationToken token)
    {Interlocked.Increment(ref ResourceCalls);if(ResourceFailure)throw new IOException("source fixture");LastResourceLookup=tenant.Value+":"+resource;return ValueTask.FromResult<ResourceScopeSnapshot?>(resource=="shared"?new(new(tenant.Value),kind,resource,"resource-v1"):null);}
    public ValueTask<bool> IsAllowedAsync(TenantAccessRequest request,CancellationToken token){PolicyHook?.Invoke();return ValueTask.FromResult(request.Action=="document.read");}
}
sealed class Business
{
    public int Created,Disposed,Reads;public string? ActualOwner;public bool CleanupFailure,CleanupDenial;public TenantOperationContext? LastContext;
    public Func<Request,TenantOperationContext,CancellationToken,ValueTask<int>>? Body;
    public TenantOperationRegistry Registry()=>new TenantOperationRegistryBuilder().Register<Request,int>("document.read","document.read","document",request=>request.Copy(),request=>new(new(request.Tenant),request.Resource),()=>{Interlocked.Increment(ref Created);return new Handler(this);}).Build();
    public int Read(Request request,TenantOperationContext context)
    {context.DemandAccess(new(ActualOwner??request.Tenant),"document",request.Resource,"document.read");Interlocked.Increment(ref Reads);return context.Tenant.Value=="A"?11:22;}
    private sealed class Handler(Business business):ITenantOperationHandler<Request,int>,IDisposable
    {
        public async ValueTask<OperationResult<int>> HandleAsync(Request request,TenantOperationContext context,CancellationToken token)
        {business.LastContext=context;var value=business.Body is null?business.Read(request,context):await business.Body(request,context,token);return OperationResult<int>.Success(value);}
        public void Dispose(){Interlocked.Increment(ref business.Disposed);if(business.CleanupDenial)throw new TenantAccessDeniedException();if(business.CleanupFailure)throw new InvalidOperationException("cleanup fixture");}
    }
}
