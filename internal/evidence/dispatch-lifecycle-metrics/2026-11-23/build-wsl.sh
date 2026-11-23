set -eu
src=/mnt/d/Cephalon/Cehpalon-Engine/.local/continuation-delivery-20261123/bench
sdk=/mnt/d/Cephalon/.tools/dotnet11-ga/linux-x64/dotnet
export DOTNET_CLI_TELEMETRY_OPTOUT=1 DOTNET_NOLOGO=1
for arm in base candidate; do
  if [ "$arm" = base ]; then engine=/mnt/d/Cephalon/.worktrees/audit-read-statistics-engine; else engine=/mnt/d/Cephalon/.worktrees/continuation-metrics; fi
  cd "$engine"
  artifacts="$src/artifacts-wsl02-$arm"
  "$sdk" restore "$src/HistogramCost.csproj" --locked-mode --configfile "$engine/NuGet.Config" "-p:EngineSource=$engine" --artifacts-path "$artifacts" > "$src/wsl02-$arm-restore.log" 2>&1
  "$sdk" build "$src/HistogramCost.csproj" -c Release --no-restore -warnaserror "-p:EngineSource=$engine" --artifacts-path "$artifacts" > "$src/wsl02-$arm-build.log" 2>&1
done

