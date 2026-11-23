"""Check the frozen canonical04 observation tables against the original gates."""
import argparse
from hashlib import sha256
import json
import math
from pathlib import Path
from statistics import mean, pstdev

TRANSPORTS = ("http", "graphql")
VARIANTS = ("baseline", "engine")
ORDER = ("BE", "EB", "BE", "EB", "BE")
MIB = 1024 * 1024


def require(condition, description):
    if not condition:
        raise ValueError(description)


def percentile95(values):
    return sorted(values)[math.ceil(0.95 * len(values)) - 1]


def shutdown_ok(row):
    end = row["shutdown"]
    return (end["exit_code"] == 0 and end["error"] is None and
            all(end[key] is True for key in
                ("graceful", "listener_closed", "owned_handlers_balanced", "disabled_probes_zero", "passed")))


def valid_work(row, volume):
    work = row["measured"]
    return (work["offered"] == work["correct"] == volume and
            work["errors"] == work["dropped"] == 0 and not work["errorKinds"] and
            work["successfulWithinDrain"] >= math.ceil(0.999 * volume))


def ordered_pairs(rows):
    expected = [
        (transport, pair, order, variant)
        for transport in TRANSPORTS
        for pair, order in enumerate(ORDER)
        for variant in (VARIANTS if order == "BE" else VARIANTS[::-1])
    ]
    actual = [(row["transport"], row["pair"], row["pair_order"], row["variant"]) for row in rows]
    require(actual == expected, "Invalid matched pair membership or order")
    return [(rows[index], rows[index + 1]) if rows[index]["variant"] == "baseline" else
            (rows[index + 1], rows[index]) for index in range(0, len(rows), 2)]


def replay(folder):
    inputs = {}

    def load(name):
        data = (folder / name).read_bytes()
        inputs[name] = sha256(data).hexdigest()
        return json.loads(data)

    startup = load("startup-observations.json")
    idle = load("idle-observations.json")
    load_runs = load("load-observations.json")
    diagnostic = load("diagnostic-observations.json")
    original = load("summary.json")
    p95_summary = load("startup-summary.json")
    load_summary = load("load-summary.json")

    require(len(startup) == 120, "Unexpected startup matrix size")
    starts = {}
    for transport in TRANSPORTS:
        values = {}
        for variant in VARIANTS:
            selected = [row for row in startup if (row["transport"], row["variant"]) == (transport, variant)]
            require([row["index"] for row in selected] == list(range(30)), "Incomplete startup sequence")
            require(all(row["verified_first_business_response"] is True and shutdown_ok(row) and math.isclose(
                row["startup_milliseconds"],
                (row["ready_and_verified_monotonic_ns"] - row["started_monotonic_ns"]) / 1e6,
                rel_tol=0, abs_tol=0.000001) for row in selected), "Invalid startup observation")
            values[variant] = percentile95([row["startup_milliseconds"] for row in selected])
        logged, = (row for row in p95_summary if row["transport"] == transport)
        require(values["engine"] <= min(1000, values["baseline"] + 150)
                and values["baseline"] <= 1000, "Startup gate failed")
        require(values["engine"] == logged["engine_p95_ms"] and values["baseline"] == logged["baseline_p95_ms"],
                "Startup replay differs from original summary")
        starts[transport] = values

    idle_pairs = ordered_pairs(idle)
    require(all(row["rss_sample_count"] == 60 and row["maximum_rss_bytes"] <= 256 * MIB and
                0 < row["minimum_rss_bytes"] <= row["median_rss_bytes"] <= row["maximum_rss_bytes"] and
                row["warmup_valid"] is True and row["sampling_schedule_valid"] is True and shutdown_ok(row)
                for row in idle), "Idle RSS, receipt or sampling gate failed")
    require(all(left["warmup_manifest_hash"] == right["warmup_manifest_hash"] and
                right["median_rss_bytes"] <= left["median_rss_bytes"] + 16 * MIB
                for left, right in idle_pairs), "Idle pairing gate failed")

    load_pairs = ordered_pairs(load_runs)
    require(len({row["logical_manifest_hash"] for row in load_runs}) == 1
            and all(row["logical_manifest_hash"] for row in load_runs), "Logical corpus differs")
    require(all(valid_work(row, 180_000) and row["driver_valid"] is True and shutdown_ok(row) and
                0 < row["measured"]["p95Ms"] <= 20 and 0 < row["measured"]["p99Ms"] <= 50 and
                row["allocations_bytes_per_offered_request"] >= 0 for row in load_runs), "Load run gate failed")
    for baseline, engine in load_pairs:
        require(all(baseline[key] and baseline[key] == engine[key] for key in
                    ("manifest_hash", "logical_manifest_hash", "final_state_hash")), "Load pair hash mismatch")
        base_p95 = baseline["measured"]["p95Ms"]
        require(engine["measured"]["p95Ms"] <= base_p95 + max(1, 0.15 * base_p95)
                and engine["allocations_bytes_per_offered_request"] <=
                baseline["allocations_bytes_per_offered_request"] + 1024, "Relative overhead gate failed")

    stability = {}
    for recorded in load_summary["stability"]:
        t, v = recorded["transport"], recorded["variant"]
        values = [row["measured"]["p95Ms"] for row in load_runs if (row["transport"], row["variant"]) == (t, v)]
        variation = pstdev(values) / mean(values)
        require(len(values) == 5 and values == recorded["p95_observations_ms"] and variation <= 0.10 and
                math.isclose(variation, recorded["population_coefficient_of_variation"]), "Stability gate failed")
        stability[f"{t}/{v}"] = variation
    require(set(stability) == {f"{t}/{v}" for t in TRANSPORTS for v in VARIANTS}, "Incomplete stability groups")

    require(len(diagnostic) == 12 and len({(row["transport"], row["rate"], row["variant"])
                                         for row in diagnostic}) == 12, "Invalid diagnostic matrix count")
    require({(row["transport"], row["rate"], row["variant"]) for row in diagnostic} ==
            {(t, rate, v) for t in TRANSPORTS for rate in (100, 500, 2000) for v in VARIANTS},
            "Invalid diagnostic matrix membership")
    require(all(row["timed_measurement_executed"] is True and row["diagnostic_status"] == "completed" and
                row["contract_and_offered_work_observation_valid"] is True and
                valid_work(row, row["rate"] * 180) and shutdown_ok(row) for row in diagnostic),
            "Diagnostic work did not reconcile")
    require(original["reference_gate_passed"] is False and original["numeric_budget_observations_passed"] is True,
            "Original reference or numeric classification differs")

    return {
        "scope": "Offline recheck of retained observation tables. The separate historical audit owns per-request replay.",
        "reference_gate_passed_in_original_run": False,
        "numeric_threshold_recheck": "passed",
        "startup_observations": len(startup),
        "nearest_rank_startup_p95_ms": starts,
        "idle_observations": len(idle),
        "idle_rss_samples_reported": sum(row["rss_sample_count"] for row in idle),
        "load_runs": len(load_runs),
        "load_correct_measured": sum(row["measured"]["correct"] for row in load_runs),
        "main_p95_population_cv": stability,
        "timed_diagnostics": len(diagnostic),
        "diagnostic_correct_measured": sum(row["measured"]["correct"] for row in diagnostic),
        "inputs_sha256": inputs,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("results", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    result = replay(args.results)
    with args.output.open("x", encoding="utf-8", newline="\n") as out:
        json.dump(result, out, indent=2)
        out.write("\n")
    print("Frozen canonical04 observation thresholds reconciled.")


if __name__ == "__main__":
    main()
