# Reproduce the Core completion observation

Use exact clean Engine source from the Engine SHA in the per-host
manifest. Prepare separate artifact locations. The original runs used
x64 SDK 11.0.100 and runtime 11.0.0, with all files and tools on the
Windows D: drive and WSL's mount of that drive. The WSL run used a
Linux-created Git clone so Linux Git could verify the source checkout.

From this directory, run Windows PowerShell first:

```powershell
python run.py --engine 'D:/path/to/engine' --dotnet 'D:/path/to/win-x64/dotnet.exe' --out 'D:/path/to/new/windows-run'
```

After the Windows process completes, use the corresponding WSL Bash command:

```bash
python3 run.py --engine /mnt/d/path/to/engine --dotnet /mnt/d/path/to/linux-x64/dotnet --out /mnt/d/path/to/new/wsl-run
```

The parent of each output path must exist. Both paths must be new.
The runner holds full restore, build and process logs in the chosen
output directory. It records protocol, harness, binaries and conformance
hashes before measurement. Use `--conformance-only` for a new preparation
directory without measurement. [Declared protocol](PROTOCOL.md)

Reconcile and replay the raw records:

```text
python analyze.py /path/to/windows-run/measure.jsonl /path/to/wsl-run/measure.jsonl --output /path/to/new/summary.json
```
