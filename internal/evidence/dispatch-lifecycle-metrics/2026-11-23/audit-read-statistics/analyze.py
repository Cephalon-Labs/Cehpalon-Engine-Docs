import json
from pathlib import Path
from statistics import median
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def describe(values):
    return {"median": median(values), "min": min(values), "max": max(values)}


def analyze(path):
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    header = rows[0]
    require(
        header["type"] == "start"
        and header["mode"] == "measure"
        and header["engine"] == "f77c42b187483086e99a5ec5ade6bcd80b9ad738"
        and header["runtime"] == ".NET 11.0.0"
        and header["tieredCompilation"] is False
        and header["pairs"] == 12
        and header["batchSize"] == 250_000
        and header["warmupSize"] == 100_000
        and header["frequency"] > 0
        and len(rows) == 31,
        f"Run provenance or size differs from the protocol in {path.name}",
    )
    calls = successes = 0

    def verify(row, expected_type, collect, reads):
        nonlocal calls, successes
        calls += reads
        successes += reads if collect else 0
        require(
            row["type"] == expected_type
            and row["collect"] is collect
            and row["reads"] == reads
            and row["providerCalls"] == calls
            and row["successes"] == successes,
            f"Unexpected {expected_type} observations in {path.name}",
        )

    for row, collect in zip(rows[1:5], (False, True, True, False), strict=True):
        verify(row, "warmup", collect, header["warmupSize"])

    reads = header["batchSize"]
    by_mode = {False: [], True: []}
    allocation = {False: [], True: []}
    deltas = []
    for pair in range(1, header["pairs"] + 1):
        on_first = pair % 2 == 0
        for row, collect in zip(rows[5 + (pair - 1) * 2 : 5 + pair * 2], (on_first, not on_first), strict=True):
            verify(row, "sample", collect, reads)
            require(
                row["pair"] == pair and row["ticks"] > 0 and row["bytes"] >= 0,
                f"Invalid measured pair {pair} in {path.name}",
            )
            by_mode[collect].append(row["ticks"] * 1_000_000_000 / header["frequency"] / reads)
            allocation[collect].append(row["bytes"] / reads)
        deltas.append(by_mode[True][-1] - by_mode[False][-1])

    require(
        rows[-2] == {
            "type": "checked",
            "providerCalls": calls,
            "statistics": {"Succeeded": successes, "DeadlineExceeded": 0, "CallerCancelled": 0, "Faulted": 0},
        } and rows[-1] == {"type": "completed"},
        f"The expected terminal checks failed in {path.name}",
    )
    return {
        "file": path.name,
        "os": header["os"],
        "calls": calls,
        "collectedSuccesses": successes,
        "nanosecondsPerRead": {
            "off": describe(by_mode[False]),
            "on": describe(by_mode[True]),
            "onMinusOff": describe(deltas),
            "offFirstDelta": describe(deltas[::2]),
            "onFirstDelta": describe(deltas[1::2]),
        },
        "allocatedBytesPerRead": {
            "off": describe(allocation[False]),
            "on": describe(allocation[True]),
            "onMinusOff": describe([on - off for on, off in zip(allocation[True], allocation[False], strict=True)]),
        },
    }


if __name__ == "__main__":
    print(json.dumps([analyze(Path(filename)) for filename in sys.argv[1:]], indent=2))
