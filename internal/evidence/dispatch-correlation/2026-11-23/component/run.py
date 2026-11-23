"""Build and run one host's locked Engine completion component observation."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
PROJECT = HERE / "DispatchCorrelationCost.csproj"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--engine", type=Path, required=True)
    parser.add_argument("--dotnet", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--conformance-only", action="store_true")
    args = parser.parse_args()
    engine, dotnet, out = (path.resolve(strict=True) for path in (args.engine, args.dotnet, args.out.parent))
    out /= args.out.name
    env = dict(os.environ, DOTNET_TieredCompilation="0", DOTNET_CLI_TELEMETRY_OPTOUT="1", DOTNET_NOLOGO="1")
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=engine, text=True).strip()
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=engine):
        raise ValueError("Engine checkout is dirty.")
    sdk = subprocess.check_output([str(dotnet), "--version"], cwd=engine, env=env, text=True).strip()
    if sdk != "11.0.100":
        raise ValueError(f"Expected SDK 11.0.100, received {sdk}.")
    out.mkdir(exist_ok=False)

    manifest = {
        "status": "preparing",
        "engine": revision,
        "sdk": sdk,
        "build": "locked Release",
        "source": {path.name: digest(path) for path in (PROJECT, HERE / "Program.cs", HERE / "packages.lock.json",
                                                        HERE / "PROTOCOL.md", HERE / "run.py", HERE / "analyze.py")},
    }

    def write():
        (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8", newline="\n")

    def run(stage, *command):
        with (out / f"{stage}.log").open("xb") as log:
            subprocess.run([str(dotnet), *map(str, command)], cwd=engine, env=env, stdout=log,
                           stderr=subprocess.STDOUT, check=True, timeout=180)

    write()
    try:
        target = out / "artifacts"
        build_options = ("--artifacts-path", target, f"-p:ProbeEngineRoot={engine}")
        run("restore", "restore", PROJECT, "--locked-mode", "--configfile",
            engine / "Tests/PlatformQualification/NuGet.Config", *build_options)
        run("build", "build", PROJECT, "--no-restore", "-c", "Release", *build_options, "-warnaserror")
        directory = target / "bin/DispatchCorrelationCost/release"
        assembly = directory / "DispatchCorrelationCost.dll"
        run("conformance", assembly, "conformance", out / "conformance.jsonl", revision)
        manifest["artifacts"] = {path.name: digest(path) for path in sorted(directory.iterdir())
                                 if path.suffix in {".dll", ".json"}}
        manifest["conformance_sha256"] = digest(out / "conformance.jsonl")
        manifest["status"] = "ready"
        write()
        (out / "pre-measurement.json").write_bytes((out / "manifest.json").read_bytes())
        if not args.conformance_only:
            run("measure", assembly, "measure", out / "measure.jsonl", revision)
            manifest["measurement_sha256"] = digest(out / "measure.jsonl")
        if subprocess.check_output(["git", "status", "--porcelain"], cwd=engine):
            raise ValueError("Engine checkout changed.")
        manifest["status"] = "passed"
    except Exception as error:
        manifest.update(status="invalid", failure=str(error))
        raise
    finally:
        write()


if __name__ == "__main__":
    main()
