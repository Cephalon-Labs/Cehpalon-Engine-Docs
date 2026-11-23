from itertools import permutations
from hashlib import sha256
from pathlib import Path
import argparse
import json
import os
import statistics
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dotnet", required=True, type=Path)
    parser.add_argument("--baseline", required=True, type=Path)
    parser.add_argument("--candidate", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    assemblies = {"base": args.baseline.resolve(), "off": args.candidate.resolve(), "on": args.candidate.resolve()}
    environment = dict(os.environ, DOTNET_TieredCompilation="0", DOTNET_NOLOGO="1")
    inputs = {str(file): sha256(file.read_bytes()).hexdigest()
              for assembly in set(assemblies.values()) for file in assembly.parent.iterdir() if file.is_file()}
    (args.out / "binary-sha256.json").write_text(json.dumps(inputs, indent=2) + "\n", encoding="utf-8")
    samples = []
    for round_number, order in enumerate(permutations(("base", "off", "on")), 1):
        results = {}
        for mode in order:
            stem = args.out / f"{round_number:02}-{mode}"
            try:
                process = subprocess.run([str(args.dotnet.resolve()), str(assemblies[mode]), mode],
                                         env=environment, capture_output=True, timeout=120)
            except subprocess.TimeoutExpired as failure:
                stem.with_suffix(".json").write_bytes(failure.stdout or b"")
                stem.with_suffix(".stderr").write_bytes(failure.stderr or b"")
                raise
            stem.with_suffix(".json").write_bytes(process.stdout)
            stem.with_suffix(".stderr").write_bytes(process.stderr)
            process.check_returncode()
            parsed = json.loads(process.stdout)
            if parsed["mode"] != mode or parsed["runtime"] != ".NET 11.0.0":
                raise ValueError("Probe mode or runtime did not match")
            results[mode] = parsed
        samples.append({"round": round_number, "order": order, "results": results})
    if any(sha256(Path(file).read_bytes()).hexdigest() != digest for file, digest in inputs.items()):
        raise ValueError("An input binary changed during the fixed run")
    summary = {}
    for workload, index in (("dispatch", 0), ("lifecycle", 1)):
        measures = {mode: [] for mode in assemblies}
        for sample in samples:
            for mode, observation in sample["results"].items():
                row = observation["measured"][index]
                if row["workload"] != workload or row["ticks"] <= 0:
                    raise ValueError("Invalid workload result")
                measures[mode].append((row["ticks"] * 1e9 / observation["frequency"] / row["iterations"],
                                       row["allocated"] / row["iterations"]))
        for name, left, right in (("off_minus_base", "off", "base"), ("on_minus_off", "on", "off")):
            differences = [[a - b for a, b in zip(pair[0], pair[1], strict=True)]
                           for pair in zip(measures[left], measures[right], strict=True)]
            summary.setdefault(workload, {})[name] = {
                "nanoseconds": describe([diff[0] for diff in differences]),
                "bytes": describe([diff[1] for diff in differences]),
            }
    (args.out / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")


def describe(values):
    return {"median": statistics.median(values), "min": min(values), "max": max(values)}


if __name__ == "__main__":
    main()

