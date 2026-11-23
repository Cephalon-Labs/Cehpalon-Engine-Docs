#!/usr/bin/env bash
set -euo pipefail
stage=/mnt/d/Cephalon/Cehpalon-Engine/.local/continuation-delivery-20261123/w1-ga
engine=/mnt/d/Cephalon/.worktrees/cm-tooling-newlines-linux
dotnet=/mnt/d/Cephalon/.tools/dotnet11-ga/linux-x64/dotnet
revision=6fe7254404cf6b148370bd95befe8331e8932354
project=Benchmarks/W1.Components/W1.Components.csproj
out=$stage/attempt01
mkdir -m 700 "$out"
trap 'code=$?; printf "%s\n" "$code" > "$out/exit-code.txt"; exit "$code"' EXIT
cd "$engine"
[[ "$(git rev-parse HEAD)" == "$revision" && -z "$(git status --porcelain=v1 -uall)" ]]
printf '%s\n' "$revision" > "$out/engine-revision.txt"
git ls-files -z -- global.json NuGet.Config Directory.Packages.props Directory.Build.props Directory.Build.targets \
  Benchmarks/W1.Components src/Cehpalon.Engine.Core src/Cehpalon.Engine.Composition |
  sort -z | xargs -0 sha256sum > "$out/source.sha256"
cmp "$stage/source.sha256" "$out/source.sha256"
sha256sum "$stage/w1-component-protocol.md" > "$out/protocol.sha256"
grep -q '^9e83d9c62557d40e4e04f2644fff8a8edcaf7a4d713e8da15d0a6ffb63f0adf0 ' "$out/protocol.sha256"
vmstat -w > "$out/wsl-vmstat-pre.txt"
lscpu -J > "$out/wsl-cpu.json"
grep -E '^(MemTotal|MemAvailable):' /proc/meminfo > "$out/wsl-memory.txt"
uname -srmo > "$out/wsl-kernel.txt"
taskset -pc $$ > "$out/launcher-affinity.txt"
env | cut -d= -f1 | sort | grep -Ei '^(DOTNET|COMPlus|CORECLR|COR_ENABLE_PROFILING|MSBuildSDKsPath)' > "$out/runtime-environment-keys.txt" || true
if grep -Eqi '^(DOTNET|COMPlus)_(tiered|gc|enableProfiling|DiagnosticPorts)|^(CORECLR_|COR_ENABLE_PROFILING)' "$out/runtime-environment-keys.txt"; then
  printf '%s\n' 'An inherited runtime instrumentation, GC or tiered compilation override is present.' > "$out/preflight-failure.txt"
  exit 1
fi
export DOTNET_NOLOGO=1 DOTNET_CLI_TELEMETRY_OPTOUT=1
export DOTNET_CLI_HOME="$out/dotnet-home" NUGET_PACKAGES="$out/packages"
[[ "$("$dotnet" --version)" == "11.0.100" ]]
"$dotnet" --info > "$out/sdk-info.txt"
"$dotnet" restore "$project" --configfile NuGet.Config --locked-mode --artifacts-path "$out/artifacts" \
  --disable-build-servers > "$out/restore.txt" 2>&1
"$dotnet" build "$project" -c Release --no-restore --artifacts-path "$out/artifacts" \
  --disable-build-servers -warnaserror > "$out/build.txt" 2>&1
assembly="$out/artifacts/bin/W1.Components/release/W1.Components.dll"
(cd "$(dirname "$assembly")" && sha256sum W1.Components.dll Cehpalon.Engine.Core.dll Cehpalon.Engine.Composition.dll \
  W1.Components.deps.json W1.Components.runtimeconfig.json) > "$out/binary.sha256"
printf '%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$out/measurement-started-utc.txt"
code=0
timeout --kill-after=10s 120s "$dotnet" "$assembly" "--output=$out/result.json" > "$out/run.txt" 2>&1 || code=$?
printf '%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" > "$out/measurement-finished-utc.txt"
vmstat -w > "$out/wsl-vmstat-post.txt"
[[ "$(git rev-parse HEAD)" == "$revision" && -z "$(git status --porcelain=v1 -uall)" ]]
sha256sum -c "$out/source.sha256" > "$out/source-readback.txt"
(cd "$(dirname "$assembly")" && sha256sum -c "$out/binary.sha256") > "$out/binary-readback.txt"
exit "$code"

