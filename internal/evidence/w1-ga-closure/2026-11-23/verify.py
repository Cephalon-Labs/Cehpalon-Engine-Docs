"""Independently replay every row of the unchanged W1 component guardrail output."""
import json
import math
from pathlib import Path
from statistics import median
import sys


def require(condition, caption):
    if not condition:
        raise ValueError(caption)


def near(a, b):
    return math.isclose(a, b, rel_tol=1e-12, abs_tol=1e-9)


report = json.loads(Path(sys.argv[1]).read_bytes())
env = report["environment"]
require(env["os"].startswith("Ubuntu 22.04"), "Unexpected WSL distribution")
require(env["framework"] == ".NET 11.0.0" and env["architecture"] == "X64", "Unexpected runtime or architecture")
frequency = env["stopwatchFrequency"]
require(frequency > 0 and env["affinity"] and env["logicalProcessors"] > 0, "Missing clock or affinity")


def verify(row, count, checksum):
    require(row["Iterations"] == count and row["Checksum"] == checksum, "Iteration count or checksum differs")
    ticks, allocated = row["ElapsedTicks"], row["AllocatedBytes"]
    require(ticks > 0 and allocated >= 0, "Invalid elapsed ticks or allocation")
    ns_op = ticks * 1_000_000_000 / frequency / count
    b_op = allocated / count
    require(near(row["NanosecondsPerOperation"], ns_op) and near(row["BytesPerOperation"], b_op),
            "Raw conversion differs")
    return ns_op, b_op


dispatch = report["dispatch"]
require((dispatch["iterations"], dispatch["warmup"], dispatch["repetitions"]) == (100_000, 10_000, 5),
        "Dispatch workload differs")
require(len(dispatch["runs"]) == 5, "Dispatch repetitions differ")
overheads, extra_allocations = [], []
for index, row in enumerate(dispatch["runs"]):
    require(row["repetition"] == index and row["order"] == ("direct,dispatcher" if index % 2 == 0 else "dispatcher,direct"),
            "Paired order differs")
    baseline_ns, baseline_b = verify(row["direct"], 100_000, 4_999_950_000)
    dispatch_ns, dispatch_b = verify(row["dispatcher"], 100_000, 4_999_950_000)
    overheads.append(dispatch_ns - baseline_ns)
    extra_allocations.append(dispatch_b - baseline_b)
require(near(dispatch["medianExtraNanoseconds"], median(overheads)) and
        near(dispatch["medianExtraBytes"], median(extra_allocations)), "Dispatch medians differ")
require(dispatch["created"] == dispatch["disposed"] == 1_000_000, "Wrong ownership totals")


def composition(name, iterations, warmup, count):
    group = report[name]
    require((group["iterations"], group["warmup"], group["repetitions"]) == (iterations, warmup, 5),
            f"{name} workload differs")
    require(len(group["runs"]) == 5, f"{name} repetitions differ")
    if name == "largeComposition":
        require(group["nodes"] == 128, "Wrong large graph size")
    stats = [verify(row, iterations, iterations * count) for row in group["runs"]]
    return tuple(median(values) for values in zip(*stats, strict=True))


small = composition("smallComposition", 1_000, 100, 2)
large = composition("largeComposition", 100, 10, 128)
median_time, median_allocations = median(overheads), median(extra_allocations)
gates = [True, True, median_time <= 20_000, median_allocations <= 1_024,
         small[0] <= 2_000_000, small[1] <= 128 * 1024, large[0] <= 10_000_000, large[1] <= 2 * 1024 * 1024]
require([case["passed"] for case in report["checks"]] == gates and report["passed"] == all(gates),
        "Guardrail count or decision differs")
print(json.dumps({
    "guardrails": {"passed": sum(gates), "total": len(gates)},
    "dispatch": {"median_extra_ns": median_time, "median_extra_bytes": median_allocations,
                 "extra_ns_per_op": overheads, "extra_bytes_per_op": extra_allocations},
    "small_composition": {"median_ns": small[0], "median_bytes": small[1]},
    "large_composition": {"median_ns": large[0], "median_bytes": large[1]},
    "rows_validated": 20
}, indent=2))
raise SystemExit(int(not report["passed"]))

