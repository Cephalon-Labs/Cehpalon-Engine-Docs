# Reproduce the audit lookup statistics observation

Use a clean Engine checkout at
`f77c42b187483086e99a5ec5ade6bcd80b9ad738`. The original runs used the
existing detached worktree at `D:/Cephalon/.worktrees/audit-read-statistics-engine`.
The SDK archives had already been verified for the program's .NET 11 GA
baseline. The harness uses the frozen scratch project lock and the committed
Engine project locks. Preserve established evidence by using new artifact and
evidence paths for any later attempt.

Run these Windows PowerShell commands from the Engine checkout after
substituting new artifact and output paths.

```powershell
$probe = (Resolve-Path '.local/continuation-20261123/collector').Path
$engine = 'D:/Cephalon/.worktrees/audit-read-statistics-engine'
$dotnet = 'D:/Cephalon/.tools/dotnet11-ga/win-x64/dotnet.exe'
$artifacts = "$probe/artifacts-win"
& $dotnet restore "$probe/CollectorProbe.csproj" --configfile "$engine/Tests/PlatformQualification/NuGet.Config" --locked-mode --artifacts-path $artifacts "-p:ProbeEngineRoot=$engine"
& $dotnet build "$probe/CollectorProbe.csproj" --no-restore -c Release --artifacts-path $artifacts "-p:ProbeEngineRoot=$engine"
$env:DOTNET_TieredCompilation = '0'
& $dotnet "$artifacts/bin/CollectorProbe/release/CollectorProbe.dll" conformance "$probe/windows-conformance-new.jsonl"
& $dotnet "$artifacts/bin/CollectorProbe/release/CollectorProbe.dll" measure "$probe/windows-new.jsonl"
```

Run the same sequence from a WSL Ubuntu shell after the Windows candidate
exits. The original WSL SDK, source, binaries and evidence all lived on the
Windows-mounted `D:` filesystem at `/mnt/d`.

```bash
probe=/mnt/d/Cephalon/Cehpalon-Engine/.local/continuation-20261123/collector
engine=/mnt/d/Cephalon/.worktrees/audit-read-statistics-engine
dotnet=/mnt/d/Cephalon/.tools/dotnet11-ga/linux-x64/dotnet
artifacts="$probe/artifacts-linux"
"$dotnet" restore "$probe/CollectorProbe.csproj" --configfile "$engine/Tests/PlatformQualification/NuGet.Config" --locked-mode --artifacts-path "$artifacts" "-p:ProbeEngineRoot=$engine"
"$dotnet" build "$probe/CollectorProbe.csproj" --no-restore -c Release --artifacts-path "$artifacts" "-p:ProbeEngineRoot=$engine"
DOTNET_TieredCompilation=0 "$dotnet" "$artifacts/bin/CollectorProbe/release/CollectorProbe.dll" conformance "$probe/wsl-conformance-new.jsonl"
DOTNET_TieredCompilation=0 "$dotnet" "$artifacts/bin/CollectorProbe/release/CollectorProbe.dll" measure "$probe/wsl-new.jsonl"
python3 "$probe/analyze.py" "$probe/windows-new.jsonl" "$probe/wsl-new.jsonl"
```

`pre-measurement.sha256` binds the original protocol, source, projects,
conformance outputs and exact executed .NET assemblies and runtime manifests
to the selected runs. The checked report preserves all paired observations in
`windows.jsonl` and `wsl.jsonl`. The process logs are empty because successful
execution directed its records to the dedicated JSONL file.
