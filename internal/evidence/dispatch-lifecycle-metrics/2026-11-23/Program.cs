using System.Diagnostics;
using System.Diagnostics.Metrics;
using System.Runtime.InteropServices;
using System.Text.Json;
using Cehpalon.Engine.Composition;
using Cehpalon.Engine.Core;

if (args.Length != 1 || args[0] is not ("base" or "off" or "on"))
    throw new ArgumentException("Pass base, off, or on.");
var mode = args[0];
if (Environment.GetEnvironmentVariable("DOTNET_TieredCompilation") != "0")
    throw new InvalidOperationException("DOTNET_TieredCompilation must be 0.");

var dispatchSamples = 0;
var lifecycleSamples = 0;
var invalid = false;
using var listener = new MeterListener();
if (mode == "on")
{
    listener.InstrumentPublished = (instrument, current) =>
    {
        if (instrument.Meter.Name == "Cehpalon.Engine.Core" && instrument.Name == "cehpalon.operation.dispatch.duration" ||
            instrument.Meter.Name == "Cehpalon.Engine.Composition" && instrument.Name == "cehpalon.module.lifecycle.duration")
            current.EnableMeasurementEvents(instrument);
    };
    listener.SetMeasurementEventCallback<double>((instrument, elapsed, tags, _) =>
    {
        invalid |= !double.IsFinite(elapsed) || elapsed < 0 || instrument.Unit != "s";
        if (instrument.Name == "cehpalon.operation.dispatch.duration")
        {
            invalid |= tags.Length != 1 || tags[0].Key != "outcome" || !Equals(tags[0].Value, "success");
            dispatchSamples++;
        }
        else
        {
            invalid |= tags.Length != 2 || tags[0].Key != "phase" || tags[0].Value is not ("activation" or "disposal") ||
                tags[1].Key != "outcome" || !Equals(tags[1].Value, "success");
            lifecycleSamples++;
        }
    });
    listener.Start();
}

var dispatch = new OperationDispatcher(new OperationRegistryBuilder()
    .Register<int, int>("benchmark.fast", static () => new Handler()).Build());
var context = new OperationContext("observation");
var configuration = """
    {"Cehpalon":{"SchemaVersion":1,"Architecture":"Modular","Topology":"SingleProcess","Pattern":"RequestReply",
    "Modules":{"api":{"Enabled":true}}}}
    """;
var plan = CompositionCompiler.Compile(configuration, [new("api", ModuleRole.EntryPoint)]).Plan
    ?? throw new InvalidOperationException("Expected valid single-module plan.");
ModuleRegistration[] registrations = [new("api", static _ => ValueTask.FromResult<IAsyncDisposable>(new Resource()))];
const int dispatchWarmup = 100_000, dispatchReads = 500_000;
const int lifecycleWarmup = 10_000, lifecycleRuns = 50_000;
var firstDispatch = Observe("cold", "dispatch", 1, Dispatch);
var firstLifecycle = Observe("cold", "lifecycle", 1, Lifecycle);
_ = Observe("warmup", "dispatch", dispatchWarmup, Dispatch);
_ = Observe("warmup", "lifecycle", lifecycleWarmup, Lifecycle);
var measured = new[] { Observe("warm", "dispatch", dispatchReads, Dispatch), Observe("warm", "lifecycle", lifecycleRuns, Lifecycle) };
var expectedDispatch = mode == "on" ? 1 + dispatchWarmup + dispatchReads : 0;
var expectedLifecycle = mode == "on" ? 2 * (1 + lifecycleWarmup + lifecycleRuns) : 0;
if (invalid || dispatchSamples != expectedDispatch || lifecycleSamples != expectedLifecycle)
    throw new InvalidOperationException($"Unexpected samples: dispatch {dispatchSamples}, lifecycle {lifecycleSamples}, invalid {invalid}.");
Console.WriteLine(JsonSerializer.Serialize(new
{
    mode, os = RuntimeInformation.OSDescription, runtime = RuntimeInformation.FrameworkDescription,
    architecture = RuntimeInformation.ProcessArchitecture.ToString(), frequency = Stopwatch.Frequency,
    dispatchSamples, lifecycleSamples, firstDispatch, firstLifecycle, measured
}));

void Dispatch()
{
    var pending = dispatch.DispatchAsync<int, int>("benchmark.fast", 42, context);
    if (!pending.IsCompletedSuccessfully || pending.Result.Value != 42)
        throw new InvalidOperationException("Dispatch did not complete synchronously.");
}
void Lifecycle()
{
    var pending = PlanActivator.ActivateAsync(plan, registrations);
    if (!pending.IsCompletedSuccessfully) throw new InvalidOperationException("Activation did not complete synchronously.");
    var cleanup = pending.Result.DisposeAsync();
    if (!cleanup.IsCompletedSuccessfully) throw new InvalidOperationException("Disposal did not complete synchronously.");
    cleanup.GetAwaiter().GetResult();
}
static object Observe(string stage, string workload, int iterations, Action action)
{
    var before = GC.GetAllocatedBytesForCurrentThread();
    var ticks = Stopwatch.GetTimestamp();
    for (var index = 0; index < iterations; ++index) action();
    var elapsed = Stopwatch.GetTimestamp() - ticks;
    var allocated = GC.GetAllocatedBytesForCurrentThread() - before;
    return new { stage, workload, iterations, ticks = elapsed, allocated };
}

sealed class Handler : IOperationHandler<int, int>, IDisposable
{
    public ValueTask<OperationResult<int>> HandleAsync(int request, OperationContext context, CancellationToken cancellationToken) =>
        ValueTask.FromResult(OperationResult<int>.Success(request));
    public void Dispose() { }
}

sealed class Resource : IAsyncDisposable
{
    public ValueTask DisposeAsync() => ValueTask.CompletedTask;
}

