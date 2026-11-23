"""Replay every component pair and validate raw receipt accounting."""
import argparse
import json
from pathlib import Path
from statistics import median


def require(valid, message):
    if not valid:
        raise ValueError(message)


def distribution(values):
    return {"min": min(values), "median": median(values), "max": max(values)}


def analyze(file):
    with file.open(encoding="utf-8") as stream:
        rows = iter(json.loads(line) for line in stream)
        start = next(rows)
        require(start["type"] == "start" and start["runtime"] == ".NET 11.0.0" and start["architecture"] == "X64",
                "Unexpected runtime")
        require(start["mode"] in ("conformance", "measure") and start["frequency"] > 0, "Unexpected mode or clock")
        pairs, warm, count = (12, 50_000, 200_000) if start["mode"] == "measure" else (2, 4, 8)
        require((start["pairs"], start["warmup"], start["dispatches"]) == (pairs, warm, count), "Matrix mismatch")
        arms = [("warmup", 0, on, warm) for on in (False, True, True, False)]
        for pair in range(1, pairs + 1):
            first = pair % 2 == 0
            arms.extend(("sample", pair, on, count) for on in (first, not first))
        results = {}
        for ambient in (False, True):
            timings = {on: [] for on in (False, True)}
            bytes_by_mode = {on: [] for on in (False, True)}
            for stage, pair, on, volume in arms:
                row = next(rows)
                require(
                    [row[field] for field in ("type", "pair", "ambient", "enabled", "count")] ==
                    [stage, pair, ambient, on, volume],
                    "Arm order mismatch",
                )
                require(row["Ticks"] > 0 and row["Bytes"] >= 0, "Invalid clock or allocation")
                require((row["FactoryCalls"], row["Disposals"], row["Completions"]) ==
                        (volume, volume, volume if on else 0), "Invalid dispatch counts")
                if stage == "sample":
                    timings[on].append(row["Ticks"] * 1e9 / start["frequency"] / volume)
                    bytes_by_mode[on].append(row["Bytes"] / volume)
            paired = [enabled - disabled for enabled, disabled in zip(timings[True], timings[False])]
            results["w3c" if ambient else "absent"] = {
                "ns": {name: distribution(timings[on]) for on, name in ((False, "off"), (True, "on"))},
                "bytes": {name: distribution(bytes_by_mode[on]) for on, name in ((False, "off"), (True, "on"))},
                "paired_ns_on_minus_off": distribution(paired),
                "paired_bytes_on_minus_off": distribution([enabled - disabled
                                                           for enabled, disabled in zip(bytes_by_mode[True], bytes_by_mode[False])]),
                "order": {"off_first": distribution(paired[::2]), "on_first": distribution(paired[1::2])},
            }
        require(next(rows) == {"type": "completed"} and next(rows, None) is None, "Incomplete or extra output")
        return {"input": file.name, "host": start, "total_dispatches": 2 * (4 * warm + 2 * pairs * count), "lanes": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    results = [analyze(file) for file in args.inputs]
    require(len({row["host"]["engine"] for row in results}) == 1, "Engine revision mismatch")
    with args.output.open("x", encoding="utf-8", newline="\n") as stream:
        json.dump(results, stream, indent=2)
        stream.write("\n")


if __name__ == "__main__":
    main()
