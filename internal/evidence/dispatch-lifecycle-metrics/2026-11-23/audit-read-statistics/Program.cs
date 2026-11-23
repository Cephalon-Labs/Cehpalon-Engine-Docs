using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text.Json;
using Cehpalon.Engine.Core;
using Cehpalon.Engine.Identity;
using Cehpalon.Engine.Tenancy;

if (args.Length != 2 || args[0] is not ("conformance" or "measure"))
    throw new ArgumentException("Usage: CollectorProbe conformance|measure <new-jsonl>");
if (Environment.GetEnvironmentVariable("DOTNET_TieredCompilation") != "0")
    throw new InvalidOperationException("Set DOTNET_TieredCompilation=0 in the child process.");
if (Environment.Version != new Version(11, 0, 0))
    throw new InvalidOperationException("This probe requires runtime 11.0.0.");

using var stream = new FileStream(args[1], FileMode.CreateNew, FileAccess.Write, FileShare.Read);
using var output = new StreamWriter(stream) { AutoFlush = true };
void Write(object row) => output.WriteLine(JsonSerializer.Serialize(row));

var pairCount = args[0] == "measure" ? 12 : 0;
const int WarmupSize = 100_000;
const int BatchSize = 250_000;
Write(new
{
    type = "start", mode = args[0], engine = "f77c42b187483086e99a5ec5ade6bcd80b9ad738",
    os = RuntimeInformation.OSDescription, architecture = RuntimeInformation.ProcessArchitecture.ToString(),
    runtime = RuntimeInformation.FrameworkDescription, frequency = Stopwatch.Frequency, pairs = pairCount,
    batchSize = BatchSize, warmupSize = WarmupSize, tieredCompilation = false
});

var source = new EmptyLookup();
var policy = new TenantChangeAuditPolicy(TenantChangeAuditMode.MetadataOnly,
    [new("document.update", "write", "document", [])]);
var statistics = new TenantChangeAuditReadStatistics();
var without = Activate(null);
var with = Activate(statistics);
TenantChangeAuditLookupReader Activate(TenantChangeAuditReadStatistics? collector) =>
    TenantChangeAuditLookupReader.ActivateWithReadTimeout(
        policy, null, () => source, distinguishTimeout: false, statistics: collector)
        ?? throw new InvalidOperationException("The selected reader did not activate.");

try
{
    await new TenantFixture().Run(context =>
    {
        void Batch(bool collect, int reads)
        {
            var reader = collect ? with : without;
            for (var index = 0; index < reads; index++)
            {
                var pending = reader.FindAsync(context, EmptyLookup.ReceiptId);
                if (!pending.IsCompletedSuccessfully || pending.Result is not null)
                    throw new InvalidOperationException("An exact lookup must complete synchronously with no result.");
            }
        }

        int expectedCalls = 0;
        int expectedSuccesses = 0;
        void Confirm(bool collect, int reads)
        {
            expectedCalls += reads;
            if (collect)
                expectedSuccesses += reads;
            if (source.Calls != expectedCalls || statistics.GetSnapshot() != new TenantChangeAuditReadStatisticsSnapshot(expectedSuccesses, 0, 0, 0))
                throw new InvalidOperationException("Provider call or reader outcome count disagrees.");
        }

        var warmup = pairCount > 0 ? WarmupSize : 4;
        foreach (var collect in new[] { false, true, true, false })
        {
            Batch(collect, warmup);
            Confirm(collect, warmup);
            Write(new { type = "warmup", collect, reads = warmup, providerCalls = source.Calls, successes = expectedSuccesses });
        }

        void Timed(int pair, bool collect)
        {
            var bytesBefore = GC.GetAllocatedBytesForCurrentThread();
            var ticksBefore = Stopwatch.GetTimestamp();
            Batch(collect, BatchSize);
            var ticks = Stopwatch.GetTimestamp() - ticksBefore;
            var bytes = GC.GetAllocatedBytesForCurrentThread() - bytesBefore;
            Confirm(collect, BatchSize);
            if (ticks <= 0 || bytes < 0)
                throw new InvalidOperationException("Invalid elapsed time or thread allocation delta.");
            Write(new { type = "sample", pair, collect, reads = BatchSize, ticks, bytes, providerCalls = source.Calls, successes = expectedSuccesses });
        }

        for (var pair = 1; pair <= pairCount; pair++)
        {
            var collectFirst = pair % 2 == 0;
            Timed(pair, collectFirst);
            Timed(pair, !collectFirst);
        }

        Write(new { type = "checked", providerCalls = source.Calls, statistics = statistics.GetSnapshot() });
    });
    Write(new { type = "completed" });
}
catch (Exception error)
{
    Write(new { type = "invalid", error = error.ToString() });
    throw;
}

sealed class EmptyLookup : ITenantChangeAuditLookupSource
{
    public static Guid ReceiptId { get; } = new("7a00145b-550d-4fb3-9a7d-d0934ffa64e2");
    public int Calls { get; private set; }

    public ValueTask<TenantChangeAuditRecord?> FindAsync(TenantId tenant, Guid receiptId, CancellationToken token)
    {
        if (!tenant.Equals(TenantFixture.Tenant) || receiptId != ReceiptId || token != CancellationToken.None)
            throw new InvalidOperationException("Unexpected source lookup request.");
        Calls++;
        return ValueTask.FromResult<TenantChangeAuditRecord?>(null);
    }
}

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
            .DispatchAsync<string, bool>("trail.lookup", "tenant", new("audit-read-statistics-probe"));
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
