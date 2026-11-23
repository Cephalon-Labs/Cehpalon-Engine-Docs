using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text.Json;
using Cehpalon.Engine.Core;

if (args.Length != 3 || args[0] is not ("conformance" or "measure") ||
    args[2].Length != 40 || !args[2].All(char.IsAsciiHexDigit))
    throw new ArgumentException("Expected conformance|measure, a new JSONL path and an Engine SHA.");
if (Environment.Version != new Version(11, 0, 0) ||
    Environment.GetEnvironmentVariable("DOTNET_TieredCompilation") != "0")
    throw new InvalidOperationException("Use .NET 11.0.0 with DOTNET_TieredCompilation=0.");

using var output = new StreamWriter(new FileStream(args[1], FileMode.CreateNew)) { AutoFlush = true };
void Write(object row) => output.WriteLine(JsonSerializer.Serialize(row));

bool measuring = args[0] == "measure";
int warmup = measuring ? 50_000 : 4;
int dispatches = measuring ? 200_000 : 8;
int pairs = measuring ? 12 : 2;
Write(new
{
    type = "start", mode = args[0], engine = args[2], frequency = Stopwatch.Frequency, warmup, dispatches, pairs,
    os = RuntimeInformation.OSDescription, architecture = RuntimeInformation.ProcessArchitecture.ToString(),
    runtime = RuntimeInformation.FrameworkDescription, availableProcessors = Environment.ProcessorCount
});

var harness = new Harness();
try
{
    foreach (bool ambient in new[] { false, true })
    {
        using Activity? activity = ambient ? new Activity("component-observation").SetIdFormat(ActivityIdFormat.W3C).Start() : null;
        if (Activity.Current != activity)
            throw new InvalidOperationException("Unexpected ambient activity.");
        harness.SetExpected(activity);

        foreach (bool enabled in new[] { false, true, true, false })
            RunBlock(0, enabled, warmup);

        for (int pair = 1; pair <= pairs; pair++)
        {
            bool enabledFirst = pair % 2 == 0;
            RunBlock(pair, enabledFirst, dispatches);
            RunBlock(pair, !enabledFirst, dispatches);
        }

        void RunBlock(int pair, bool enabled, int count)
        {
            var sample = harness.Run(enabled, count);
            if (Activity.Current != activity)
                throw new InvalidOperationException("Dispatch replaced the ambient activity.");
            Write(new { type = pair == 0 ? "warmup" : "sample", pair, ambient, enabled, count,
                sample.Ticks, sample.Bytes, sample.FactoryCalls, sample.Disposals, sample.Completions });
        }
    }
    Write(new { type = "completed" });
}
catch (Exception error)
{
    Write(new { type = "invalid", error = error.ToString() });
    throw;
}

sealed class Harness
{
    private static readonly OperationResult<int> Result = OperationResult<int>.Success(1);
    private readonly OperationContext context = new("component-observation");
    private readonly OperationDispatcher disabled;
    private readonly OperationDispatcher enabled;
    private int factories;
    private int disposals;
    private int completions;
    private int invalid;
    private ActivityTraceId? traceId;
    private ActivitySpanId? spanId;

    public Harness()
    {
        var registry = new OperationRegistryBuilder().Register<int, int>("probe.operation", () =>
        {
            factories++;
            return new Handler(this);
        }).Build();
        disabled = new OperationDispatcher(registry);
        enabled = new OperationDispatcher(registry, completion =>
        {
            completions++;
            if (completion.TraceId != traceId || completion.SpanId != spanId ||
                completion.Outcome != OperationDispatchOutcome.Success || completion.Duration < TimeSpan.Zero || factories != disposals)
                invalid++;
        });
    }

    public void SetExpected(Activity? activity)
    {
        traceId = activity?.TraceId;
        spanId = activity?.SpanId;
    }

    public Sample Run(bool collect, int count)
    {
        int previousFactories = factories;
        int previousDisposals = disposals;
        int previousCompletions = completions;
        var dispatcher = collect ? enabled : disabled;
        long allocated = GC.GetAllocatedBytesForCurrentThread();
        long start = Stopwatch.GetTimestamp();
        for (int i = 0; i < count; i++)
        {
            var result = dispatcher.DispatchAsync<int, int>("probe.operation", 1, context);
            if (!result.IsCompletedSuccessfully || !ReferenceEquals(Result, result.Result))
                throw new InvalidOperationException("Unexpected dispatch result.");
        }
        long ticks = Stopwatch.GetTimestamp() - start;
        long bytes = GC.GetAllocatedBytesForCurrentThread() - allocated;
        var sample = new Sample(ticks, bytes, factories - previousFactories,
            disposals - previousDisposals, completions - previousCompletions);
        if (ticks <= 0 || bytes < 0 || invalid != 0 ||
            sample.FactoryCalls != count || sample.Disposals != count ||
            sample.Completions != (collect ? count : 0))
            throw new InvalidOperationException("A block failed its dispatch counts or receipt assertions.");
        return sample;
    }

    public readonly record struct Sample(long Ticks, long Bytes, int FactoryCalls, int Disposals, int Completions);

    private sealed class Handler(Harness owner) : IOperationHandler<int, int>, IDisposable
    {
        public ValueTask<OperationResult<int>> HandleAsync(int request, OperationContext context,
            CancellationToken cancellationToken) => ValueTask.FromResult(Result);

        public void Dispose() => owner.disposals++;
    }
}
