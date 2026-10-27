using System.Text.Json;
using System.Security.Cryptography;
using Cehpalon.Engine.Core;
using Cehpalon.Engine.Composition;

var main = "D:/Cephalon/Cehpalon-Engine";
var names = new[] { "src/Cehpalon.Engine.Core/Contracts.cs", "src/Cehpalon.Engine.Core/OperationRegistry.cs", "src/Cehpalon.Engine.Core/OperationResult.cs", "src/Cehpalon.Engine.Composition/Contracts.cs", "src/Cehpalon.Engine.Composition/CompositionCompiler.cs", "src/Cehpalon.Engine.Composition/PlanActivator.cs" };
Dictionary<string,string> Hashes() => names.ToDictionary(x=>x, x=>Convert.ToHexStringLower(SHA256.HashData(File.ReadAllBytes(Path.Combine(main,x)))));
var before=Hashes();
var checks=new List<object>(); var failed=0;
void Assert(bool condition) { if(!condition) throw new InvalidOperationException("Assertion failed"); }
async Task<Exception> Error(Func<Task> action)
{
    try { await action(); } catch(Exception error) { return error; }
    throw new InvalidOperationException("Expected rejection");
}
async Task Check(string name,Func<Task> action)
{
    try { await action(); checks.Add(new{name,passed=true}); }
    catch(Exception error) { failed++; checks.Add(new{name,passed=false,error=error.ToString()}); }
}
var json="{\"Cehpalon\":{\"SchemaVersion\":1,\"Architecture\":\"Modular\",\"Topology\":\"SingleProcess\",\"Pattern\":\"RequestReply\",\"Modules\":{\"api\":{\"Enabled\":true},\"graphql\":{\"Enabled\":false}}}}";
var catalog=new[]{new ModuleDescriptor("core",ModuleRole.Support),new ModuleDescriptor("api",ModuleRole.EntryPoint,["core"]),new ModuleDescriptor("graphql",ModuleRole.EntryPoint,["core"])};
var plan=CompositionCompiler.Compile(json,catalog).Plan!;
await Check("factory-cancellation-plus-async-cleanup-failure-preserves-both-without-business-call",async()=>
{
    using var cancellation=new CancellationTokenSource();
    var handler=new Handler();
    var dispatcher=new OperationDispatcher(new OperationRegistryBuilder().Register<int,int>("review.run",()=>{cancellation.Cancel(); return handler;}).Build());
    var error=await Error(()=>dispatcher.DispatchAsync<int,int>("review.run",1,new OperationContext("review"),cancellation.Token).AsTask());
    Assert(error is AggregateException aggregate && aggregate.InnerExceptions[0] is OperationCanceledException canceled && canceled.CancellationToken==cancellation.Token && aggregate.InnerExceptions[1] is ApplicationException && handler.Calls==0 && handler.Cleanup==1);
});
await Check("missing-last-enabled-registration-rejects-before-all-activation-including-disabled-dangerous-factory",async()=>
{
    var calls=0;
    var error=await Error(()=>PlanActivator.ActivateAsync(plan,new[]{
        new ModuleRegistration("core",_=>{calls++; return ValueTask.FromResult<IAsyncDisposable>(new Resource());}),
        new ModuleRegistration("graphql",_=>{calls++; throw new Exception("Disabled factory invoked");})
    }).AsTask());
    Assert(error is ArgumentException && calls==0);
});
await Check("aliased-module-resource-rejected-with-single-owned-rollback",async()=>
{
    var resource=new Resource();
    var error=await Error(()=>PlanActivator.ActivateAsync(plan,new[]{new ModuleRegistration("core",_=>ValueTask.FromResult<IAsyncDisposable>(resource)),new ModuleRegistration("api",_=>ValueTask.FromResult<IAsyncDisposable>(resource))}).AsTask());
    Assert(error is InvalidOperationException && resource.Cleanup==1);
});
await Check("concurrent-failed-lease-disposal-shares-single-observed-failure",async()=>
{
    var entered=new TaskCompletionSource(TaskCreationOptions.RunContinuationsAsynchronously);
    var release=new TaskCompletionSource(TaskCreationOptions.RunContinuationsAsynchronously);
    var cleanup=0;
    var failure=new ApplicationException("owned cleanup");
    var lease=await PlanActivator.ActivateAsync(CompositionCompiler.Compile(json,catalog).Plan!,new[]{
        new ModuleRegistration("core",_=>ValueTask.FromResult<IAsyncDisposable>(new Resource())),
        new ModuleRegistration("api",_=>ValueTask.FromResult<IAsyncDisposable>(new DelegateResource(async()=>{Interlocked.Increment(ref cleanup); entered.TrySetResult(); await release.Task; throw failure;})))
    });
    var tasks=Enumerable.Range(0,8).Select(_=>Error(()=>lease.DisposeAsync().AsTask())).ToArray();
    await entered.Task.WaitAsync(TimeSpan.FromSeconds(5)); release.SetResult();
    var errors=await Task.WhenAll(tasks).WaitAsync(TimeSpan.FromSeconds(5));
    Assert(cleanup==1 && errors.All(x=>ReferenceEquals(x,errors[0])) && errors[0] is AggregateException aggregate && ReferenceEquals(aggregate.InnerExceptions.Single(),failure));
});
await Check("activation-plan-cannot-be-constructed-through-public-api",()=>
{
    Assert(typeof(ActivationPlan).GetConstructors().Length==0 && typeof(ActivationPlan).GetProperties().All(x=>x.SetMethod is null));
    return Task.CompletedTask;
});
await Check("malformed-escaped-unicode-produces-sanitized-diagnostics",()=>
{
    foreach(var invalid in new[]{json.Replace("Modular","\\uD800"),json.Replace("\"api\"","\"\\uD800\""),json.Replace("Architecture","\\uD800")})
    {
        var result=CompositionCompiler.Compile(invalid,catalog);
        Assert(!result.IsSuccess && result.Diagnostics.All(x=>x.Code=="CFG_JSON" && !x.Message.Contains("D800",StringComparison.OrdinalIgnoreCase)));
    }
    return Task.CompletedTask;
});
await Check("entrypoint-cannot-be-implicitly-activated-through-support-dependency",()=>
{
    var result=CompositionCompiler.Compile(json,new[]{new ModuleDescriptor("core",ModuleRole.Support,["graphql"]),new ModuleDescriptor("api",ModuleRole.EntryPoint,["core"]),new ModuleDescriptor("graphql",ModuleRole.EntryPoint)});
    Assert(!result.IsSuccess && result.Diagnostics.Any(x=>x.Code=="PLAN_FORBIDDEN"));
    return Task.CompletedTask;
});
await Check("infinite-dependency-enumerator-is-bounded-and-rejected",()=>
{
    IEnumerable<string> Infinite() { while(true) yield return "core"; }
    var result=CompositionCompiler.Compile(json,new[]{new ModuleDescriptor("core",ModuleRole.Support),new ModuleDescriptor("api",ModuleRole.EntryPoint,Infinite()),new ModuleDescriptor("graphql",ModuleRole.EntryPoint)});
    Assert(!result.IsSuccess && result.Diagnostics.Any(x=>x.Code=="CAT_DEPENDENCIES"));
    return Task.CompletedTask;
});
var after=Hashes();
var sourceStable=before.All(x=>after[x.Key]==x.Value);
if(!sourceStable) failed++;
var report=new{observedAtUtc=DateTimeOffset.UtcNow,scope="Independent bounded read-only adversarial review of integrated Core/Composition; no benchmark or source edits",sourceBefore=before,sourceAfter=after,sourceStable,passed=checks.Count(x=>true)-(failed-(sourceStable?0:1)),failed,checks};
var output=JsonSerializer.Serialize(report,new JsonSerializerOptions{WriteIndented=true});
File.WriteAllText("D:/Cephalon/.worktrees/w1-core/.local/integrated-review/results.json",output+"\n");
Console.WriteLine(output); return failed==0?0:1;

sealed class Handler:IOperationHandler<int,int>,IAsyncDisposable
{
    public int Calls,Cleanup;
    public ValueTask<OperationResult<int>> HandleAsync(int request,OperationContext context,CancellationToken token) { Calls++; return ValueTask.FromResult(OperationResult<int>.Success(request)); }
    public ValueTask DisposeAsync() { Cleanup++; return ValueTask.FromException(new ApplicationException("cleanup")); }
}
sealed class Resource:IAsyncDisposable
{
    public int Cleanup;
    public ValueTask DisposeAsync() { Cleanup++; return ValueTask.CompletedTask; }
}
sealed class DelegateResource(Func<ValueTask> action):IAsyncDisposable
{
    public ValueTask DisposeAsync()=>action();
}
