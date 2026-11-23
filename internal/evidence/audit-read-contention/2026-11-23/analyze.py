import argparse
import json
from pathlib import Path
from statistics import median

ENGINE = "6fe7254404cf6b148370bd95befe8331e8932354"
MODES = "OPS"
PERMUTATIONS = ("OPS", "OSP", "POS", "PSO", "SOP", "SPO")
SIZES = (1, 2, 4)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def snapshot(count):
    return dict(Succeeded=count, DeadlineExceeded=0, CallerCancelled=0, Faulted=0)


def distribution(values):
    return {"min": min(values), "median": median(values), "max": max(values)}


def analyze(path):
    with path.open(encoding="utf-8") as stream:
        rows = iter(json.loads(line) for line in stream)
        start = next(rows)
        require(start["type"] == "start" and start["engine"] == ENGINE, "Wrong Engine baseline")
        require(start["architecture"] == "X64" and start["runtime"] == ".NET 11.0.0", "Wrong runtime")
        require(start["tieredCompilation"] is False and start["processorCount"] >= 1, "Invalid process settings")
        require(start["frequency"] > 0 and start["workersByLane"] == list(SIZES), "Invalid clock or lane list")
        conformance = start["mode"] == "conformance"
        repetitions, warmup, batch = (6, 2, 4) if conformance else (12, 100_000, 250_000)
        require(start["mode"] in {"measure", "conformance"}, "Wrong invocation mode")
        require((start["repetitions"], start["warmupReads"], start["batchReads"]) ==
                (repetitions, warmup, batch), "Wrong matrix")
        blocks = [("warmup", 0, 0, mode, warmup) for mode in "OPSSPO"]
        blocks += [
            ("sample", index + 1, slot + 1, mode, batch)
            for index in range(repetitions)
            for slot, mode in enumerate(PERMUTATIONS[index % len(PERMUTATIONS)])
        ]
        results = [
            analyze_lane(rows, blocks, size, repetitions, start["frequency"])
            for size in SIZES
        ]
        require(next(rows) == {"type": "completed"} and next(rows, None) is None, "Incomplete run or extra records")
        return {
            "file": path.name,
            "host": start,
            "totalReads": sum(result["totalReads"] for result in results),
            "lanes": results,
        }


def analyze_lane(rows, blocks, size, repetitions, frequency):
    expected_reads = 0
    expected_personal = 0
    expected_shared = 0
    previous_end = None
    threads = None
    rounds = [{} for _ in range(repetitions)]
    start_skew = {mode: [] for mode in MODES}
    overlap = {mode: [] for mode in MODES}
    allocated = {mode: [] for mode in MODES}
    for kind, trial, slot, mode, reads in blocks:
        row = next(rows)
        stage = f"{size} workers, {kind} {trial}/{slot} ({mode})"
        require((row["type"], row["workers"], row["Round"], row["Slot"], row["mode"], row["Reads"]) ==
                (kind, size, trial, slot, mode, reads), f"Unexpected record at {stage}")
        expected_reads += reads
        expected_personal += reads if mode == "P" else 0
        expected_shared += reads * size if mode == "S" else 0
        require(row["shared"] == snapshot(expected_shared), f"Shared outcomes differ at {stage}")
        receipts = row["receipts"]
        require([worker["Worker"] for worker in receipts] == list(range(size)), f"Wrong worker indices at {stage}")
        observed_threads = tuple(worker["Thread"] for worker in receipts)
        if threads is None:
            threads = observed_threads
        require(len(set(threads)) == size and threads == observed_threads, f"Worker changed or was reused at {stage}")
        begins = [worker["Begin"] for worker in receipts]
        ends = [worker["End"] for worker in receipts]
        bytes_allocated = 0
        for worker in receipts:
            require(worker["Begin"] < worker["End"] and worker["Bytes"] >= 0, f"Invalid interval or allocation at {stage}")
            require(worker["Calls"] == expected_reads and worker["Personal"] == snapshot(expected_personal),
                    f"Source calls or personal outcomes differ at {stage}")
            bytes_allocated += worker["Bytes"]
        require(previous_end is None or min(begins) >= previous_end, f"Trials actually overlapped at {stage}")
        previous_end = max(ends)
        if kind == "sample":
            ns_per_tick = 1e9 / frequency
            rounds[trial - 1][mode] = (max(ends) - min(begins)) * ns_per_tick / (reads * size)
            start_skew[mode].append((max(begins) - min(begins)) * ns_per_tick / 1e6)
            overlap[mode].append((min(ends) - max(begins)) * ns_per_tick / 1e6)
            allocated[mode].append(bytes_allocated / (reads * size))
    require(next(rows) == {
        "type": "checked", "workers": size, "readsPerWorker": expected_reads,
        "expectedPersonal": expected_personal, "expectedShared": expected_shared,
    }, f"Final quiescent check differs for {size} workers")
    contrasts = {}
    for first, second in ("PO", "SO", "SP"):
        deltas = [row[first] - row[second] for row in rounds]
        first_before_second = [
            PERMUTATIONS[i % len(PERMUTATIONS)].index(first) < PERMUTATIONS[i % len(PERMUTATIONS)].index(second)
            for i in range(repetitions)
        ]
        contrasts[f"{first}-{second}"] = {
            **distribution(deltas),
            "firstEarlier": distribution([delta for delta, earlier in zip(deltas, first_before_second) if earlier]),
            "firstLater": distribution([delta for delta, earlier in zip(deltas, first_before_second) if not earlier]),
        }
    return {
        "workers": size,
        "totalReads": expected_reads * size,
        "personalSuccesses": expected_personal * size,
        "sharedSuccesses": expected_shared,
        "nsPerRead": {mode: distribution([row[mode] for row in rounds]) for mode in MODES},
        "pairedNsPerRead": contrasts,
        "startSkewMs": {mode: distribution(start_skew[mode]) for mode in MODES},
        "allWorkerOverlapMs": {mode: distribution(overlap[mode]) for mode in MODES},
        "nonoverlapBlocks": {mode: sum(value <= 0 for value in overlap[mode]) for mode in MODES},
        "allocatedBytesPerRead": {mode: distribution(allocated[mode]) for mode in MODES},
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", type=Path, nargs="+")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    results = [analyze(path) for path in args.runs]
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(results, stream, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
