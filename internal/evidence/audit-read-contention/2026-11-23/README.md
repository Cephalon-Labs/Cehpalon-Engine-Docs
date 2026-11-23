# Reproduce the concurrent collector observation

Read [the declared protocol](PROTOCOL.md). Use a clean Engine checkout at
`6fe7254404cf6b148370bd95befe8331e8932354` and verified x64 .NET SDK
11.0.100 with runtime 11.0.0 on both hosts. Commands run from this directory
with separate new artifact and output directories. The original WSL SDK,
Engine, project and artifacts were all on the Windows-mounted D: drive.

Windows PowerShell setup and conformance:

```powershell
$engine = 'D:/path/to/clean/Engine'
$dotnet = 'D:/path/to/verified/win-x64/dotnet.exe'
$artifacts = 'D:/path/to/new/windows-artifacts'
& $dotnet restore AuditReadContention.csproj --configfile "$engine/Tests/PlatformQualification/NuGet.Config" --locked-mode --artifacts-path $artifacts "-p:ProbeEngineRoot=$engine"
& $dotnet build AuditReadContention.csproj --no-restore -c Release --artifacts-path $artifacts "-p:ProbeEngineRoot=$engine"
$env:DOTNET_TieredCompilation = '0'
& $dotnet "$artifacts/bin/AuditReadContention/release/AuditReadContention.dll" conformance "$artifacts/conformance.jsonl"
```

WSL Bash setup and conformance:

```bash
engine=/mnt/d/path/to/clean/Engine
dotnet=/mnt/d/path/to/verified/linux-x64/dotnet
artifacts=/mnt/d/path/to/new/wsl-artifacts
"$dotnet" restore AuditReadContention.csproj --configfile "$engine/Tests/PlatformQualification/NuGet.Config" --locked-mode --artifacts-path "$artifacts" "-p:ProbeEngineRoot=$engine"
"$dotnet" build AuditReadContention.csproj --no-restore -c Release --artifacts-path "$artifacts" "-p:ProbeEngineRoot=$engine"
export DOTNET_TieredCompilation=0
"$dotnet" "$artifacts/bin/AuditReadContention/release/AuditReadContention.dll" conformance "$artifacts/conformance.jsonl"
```

Check each step's exit status before continuing. After replaying both
conformance records with `analyze.py`, capture the configurations and
SHA-256 hashes shown in [the original manifest](pre-measurement.json).
Run the Windows then the WSL executable once each, substituting
`measure` and a new output filename for the conformance mode and file.
Run the Windows observation to completion before starting the WSL
observation. Retain failure records if any stage fails. To independently
replay the committed series from either host:

```text
python analyze.py windows-conformance.jsonl wsl-conformance.jsonl --output conformance-replay.json
python analyze.py windows.jsonl wsl.jsonl --output measurement-replay.json
```

The measured replay should reproduce [summary.json](summary.json).
