$ErrorActionPreference = 'Stop'
$src = 'D:/Cephalon/Cehpalon-Engine/.local/continuation-delivery-20261123/bench'
$sdk = 'D:/Cephalon/.tools/dotnet11-ga/win-x64/dotnet.exe'
$roots = [ordered]@{
    base = 'D:/Cephalon/.worktrees/audit-read-statistics-engine'
    candidate = 'D:/Cephalon/.worktrees/continuation-metrics'
}
$env:DOTNET_CLI_TELEMETRY_OPTOUT = '1'
$env:DOTNET_NOLOGO = '1'
foreach ($arm in $roots.Keys) {
    $engine = $roots[$arm]
    Set-Location $engine
    $artifacts = "$src/artifacts-win02-$arm"
    $properties = @("-p:EngineSource=$engine", '--artifacts-path', $artifacts)
    if (!(Test-Path -LiteralPath "$src/packages.lock.json")) {
        & $sdk restore "$src/HistogramCost.csproj" --configfile "$engine/NuGet.Config" @properties *> "$src/win02-$arm-restore-initial.log"
        if ($LASTEXITCODE -ne 0) { throw 'Initial benchmark lock generation failed' }
    }
    & $sdk restore "$src/HistogramCost.csproj" --locked-mode --configfile "$engine/NuGet.Config" @properties *> "$src/win02-$arm-restore.log"
    if ($LASTEXITCODE -ne 0) { throw "Locked benchmark restore failed for $arm" }
    & $sdk build "$src/HistogramCost.csproj" -c Release --no-restore -warnaserror @properties *> "$src/win02-$arm-build.log"
    if ($LASTEXITCODE -ne 0) { throw "Benchmark build failed for $arm" }
}

