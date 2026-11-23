using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Text.Json;
using Cehpalon.Engine.Tenancy;

if (args.Length != 2 || args[0] is not ("conformance" or "measure"))
    throw new ArgumentException("Usage: AuditReadContention conformance|measure <new-jsonl>");
if (Environment.Version != new Version(11, 0, 0) ||
    Environment.GetEnvironmentVariable("DOTNET_TieredCompilation") != "0")
    throw new InvalidOperationException("Use .NET 11.0.0 with DOTNET_TieredCompilation=0.");

using var stream = new FileStream(args[1], FileMode.CreateNew, FileAccess.Write, FileShare.Read);
using var output = new StreamWriter(stream) { AutoFlush = true };
void Write(object row) => output.WriteLine(JsonSerializer.Serialize(row));

var measuring = args[0] == "measure";
var workersByLane = new[] { 1, 2, 4 };
var orders = new[] { "OPS", "OSP", "POS", "PSO", "SOP", "SPO" };
var repetitions = measuring ? 12 : 6;
var warmupReads = measuring ? 100_000 : 2;
var batchReads = measuring ? 250_000 : 4;
var blocks = new List<Block>();
foreach (var mode in "OPSSPO")
    blocks.Add(new Block(0, 0, mode, warmupReads));
for (var round = 1; round <= repetitions; round++)
{
    var order = orders[(round - 1) % orders.Length];
    for (var slot = 0; slot < order.Length; slot++)
        blocks.Add(new Block(round, slot + 1, order[slot], batchReads));
}

Write(new
{
    type = "start", mode = args[0], engine = "6fe7254404cf6b148370bd95befe8331e8932354",
    os = RuntimeInformation.OSDescription, architecture = RuntimeInformation.ProcessArchitecture.ToString(),
    runtime = RuntimeInformation.FrameworkDescription, frequency = Stopwatch.Frequency,
    processorCount = Environment.ProcessorCount, workersByLane, repetitions, warmupReads, batchReads,
    tieredCompilation = false
});

try
{
    foreach (var workerCount in workersByLane)
        RunLane(workerCount);
    Write(new { type = "completed" });
}
catch (Exception error)
{
    Write(new { type = "invalid", error = error.ToString() });
    throw;
}

void RunLane(int workerCount)
{
    var policy = new TenantChangeAuditPolicy(TenantChangeAuditMode.MetadataOnly,
        [new("document.update", "write", "document", [])]);
    var shared = new TenantChangeAuditReadStatistics();
    var workers = new Thread[workerCount];
    var receipts = new Receipt[workerCount];
    var errors = new Exception?[workerCount];
    using var barrier = new Barrier(workerCount + 1);

    void Meet()
    {
        if (!barrier.SignalAndWait(TimeSpan.FromSeconds(15)))
            throw new TimeoutException("The batch barrier timed out.");
    }

    for (var index = 0; index < workerCount; index++)
    {
        var worker = index;
        var thread = new Thread(() =>
        {
            try
            {
                var source = new EmptyLookup();
                var own = new TenantChangeAuditReadStatistics();
                TenantChangeAuditLookupReader Activate(TenantChangeAuditReadStatistics? collector) =>
                    TenantChangeAuditLookupReader.ActivateWithReadTimeout(
                        policy, null, () => source, distinguishTimeout: false, statistics: collector)
                    ?? throw new InvalidOperationException("The receipt reader did not activate.");
                var off = Activate(null);
                var personal = Activate(own);
                var together = Activate(shared);

                new TenantFixture().Run(context =>
                {
                    foreach (var block in blocks)
                    {
                        var reader = block.Mode switch
                        {
                            'O' => off,
                            'P' => personal,
                            'S' => together,
                            _ => throw new InvalidOperationException("Invalid collector mode.")
                        };
                        Meet();
                        var bytesBefore = GC.GetAllocatedBytesForCurrentThread();
                        var begin = Stopwatch.GetTimestamp();
                        for (var read = 0; read < block.Reads; read++)
                        {
                            var pending = reader.FindAsync(context, EmptyLookup.ReceiptId);
                            if (!pending.IsCompletedSuccessfully || pending.Result is not null)
                                throw new InvalidOperationException("A receipt lookup did not synchronously return null.");
                        }
                        var end = Stopwatch.GetTimestamp();
                        var bytes = GC.GetAllocatedBytesForCurrentThread() - bytesBefore;
                        receipts[worker] = new Receipt(worker, Environment.CurrentManagedThreadId,
                            begin, end, bytes, EmptyLookup.Calls, own.GetSnapshot());
                        Meet();
                    }
                }).GetAwaiter().GetResult();
            }
            catch (Exception error)
            {
                errors[worker] = error;
            }
        }) { IsBackground = true, Name = $"audit-read-contention-{worker + 1}" };
        workers[worker] = thread;
        thread.Start();
    }

    var expectedCalls = 0;
    var expectedPersonal = 0;
    var expectedShared = 0;
    var unsuccessful = false;
    try
    {
        foreach (var block in blocks)
        {
            Meet();
            Meet();
            expectedCalls += block.Reads;
            if (block.Mode == 'P')
                expectedPersonal += block.Reads;
            if (block.Mode == 'S')
                expectedShared += block.Reads * workerCount;

            var snapshot = shared.GetSnapshot();
            Write(new
            {
                type = block.Round == 0 ? "warmup" : "sample",
                workers = workerCount, block.Round, block.Slot, mode = block.Mode.ToString(),
                block.Reads, shared = snapshot, receipts
            });
            if (snapshot != new TenantChangeAuditReadStatisticsSnapshot(expectedShared, 0, 0, 0) ||
                receipts.Any(receipt => receipt.Calls != expectedCalls ||
                    receipt.Personal != new TenantChangeAuditReadStatisticsSnapshot(expectedPersonal, 0, 0, 0) ||
                    receipt.Begin >= receipt.End || receipt.Bytes < 0))
                throw new InvalidOperationException("Provider call, outcome count, tick or allocation mismatch.");
        }
    }
    catch (Exception error)
    {
        unsuccessful = true;
        Write(new { type = "lane-error", workers = workerCount, error = error.ToString() });
    }
    finally
    {
        foreach (var worker in workers)
        {
            if (!worker.Join(TimeSpan.FromSeconds(20)))
                throw new TimeoutException("A batch worker did not terminate.");
        }
    }

    var failures = errors.OfType<Exception>().ToArray();
    if (unsuccessful || failures.Length != 0)
        throw new AggregateException("An audit read lane failed.", failures);
    Write(new { type = "checked", workers = workerCount, readsPerWorker = expectedCalls, expectedPersonal, expectedShared });
}

readonly record struct Block(int Round, int Slot, char Mode, int Reads);

readonly record struct Receipt(int Worker, int Thread, long Begin, long End, long Bytes, int Calls,
    TenantChangeAuditReadStatisticsSnapshot Personal);

sealed class EmptyLookup : ITenantChangeAuditLookupSource
{
    [ThreadStatic]
    private static int calls;

    public static Guid ReceiptId { get; } = new("7a00145b-550d-4fb3-9a7d-d0934ffa64e2");
    public static int Calls => calls;

    public ValueTask<TenantChangeAuditRecord?> FindAsync(TenantId tenant, Guid receiptId, CancellationToken token)
    {
        if (!tenant.Equals(TenantFixture.Tenant) || receiptId != ReceiptId || token != CancellationToken.None)
            throw new InvalidOperationException("Unexpected source lookup request.");
        calls++;
        return ValueTask.FromResult<TenantChangeAuditRecord?>(null);
    }
}
