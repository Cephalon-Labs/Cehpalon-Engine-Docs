# Small API GA conformance and reference readiness

Follow-up on 2026-11-24: [Two-host TLS preflight](small-api-two-host-preflight.md) records the subsequent harness and lab results.

## Executed conformance

Both runs used Samples `a8ad452677c48d87a125460c552ee01c3e044046` and
Engine `5e92ac1c7fa1e150e7e97de6d68e94b31ffba053`, with .NET SDK
11.0.100 and .NET/ASP.NET Core runtime 11.0.0. The locked Release
verifier ran the complete conformance mode once per host. WSL Ubuntu
22.04.5 used native ext4 for the source, SDK and execution. Windows 11
ran after the WSL process exited.

Each cell gives passed ordered cases, cancellation cases included in the
ordered corpus, and same-process start/stop cycles.

| Variant and transport | WSL Ubuntu | Windows 11 |
| --- | ---: | ---: |
| Native baseline HTTP | 1,000 / 100 / 30 | 1,000 / 100 / 30 |
| Native baseline GraphQL | 1,000 / 100 / 30 | 1,000 / 100 / 30 |
| Engine HTTP | 1,000 / 100 / 30 | 1,000 / 100 / 30 |
| Engine GraphQL | 1,000 / 100 / 30 | 1,000 / 100 / 30 |

Both hosts passed all 22 lane checks and five configuration checks.
All 800 cancellations reached the delayed handler before the actual
abort, acknowledged within the declared 100 ms, left state unchanged
and joined handler cleanup. Both HTTP lanes on each host exercised
10,000 additional requests and observed zero disabled GraphQL counters
and a closed GraphQL route. The GraphQL lanes observed positive
registration and executor counters. The five configuration checks are
pure preactivation checks, including the all-off and cycle cases.

Independent readback checked all ordered indices, status and outcome
codes, monotonic cancellation timestamps, lifecycle shutdown/disposal
and activation counters. The dataset, ordered corpus and expected
final-state hashes match the archived RC3 fixture. The generated registry
hash also matches between hosts. The retained archives contain the
synthetic raw results and build manifest, with per-file checksums.
[WSL readback](../evidence/small-api-ga-conformance/2026-11-24/wsl-readback.json) ·
[Windows readback](../evidence/small-api-ga-conformance/2026-11-24/windows-readback.json) ·
[Raw archives and checksums](../evidence/small-api-ga-conformance/2026-11-24/raw-retention-manifest.json)

## Reference readiness

| Requirement | Current evidence |
| --- | --- |
| Requested Linux 2 dedicated vCPU and 1 GiB | No approved target with this allocation was verified. A 1 GiB application limit defines a separate resource profile. |
| Original W0 Linux 2 dedicated vCPU and 2 GiB | WSL exposes 20 logical CPUs and about 31.2 GiB. Its effective CPU set is 0–19, its CPU quota is unlimited and the application memory cap is unset. Dedicated app resources were not verified. |
| Separate driver machine or reserved allocation | No project-mapped target was identified. Repository runner inventories reported zero self-hosted runners across Engine, Docs and Samples. Organization-level inventory access returned HTTP 403. |
| Reference-capable harness | The merged orchestrator launches local processes on fixed CPU affinities and reports an observational verdict. The app binds to loopback. A separate-machine setup would also require compatible private HTTPS binding, certificate identity and first-response verification. |

No timed benchmark or offered-load preflight was started. The original
60-second warmup, 180-second measured interval at 1,000 requests/s,
five alternating pairs per transport, startup, idle, latency, allocation
and stability gates remain authoritative. The successful same-process
lifecycle checks do not furnish fresh-process startup measurements.
[Preflight receipt](../evidence/small-api-ga-conformance/2026-11-24/reference-preflight.json) ·
[Original W0 protocol](small-api-workload.md) ·
[Observational harness](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/blob/a8ad452677c48d87a125460c552ee01c3e044046/tools/benchmark_small_api.py)

Reproduce the executed conformance from a clean Samples checkout and
the exact pinned Engine checkout. Use a new ignored output directory.

```text
python tools/verify_small_api_benchmark.py --dotnet <absolute-GA-dotnet> --engine-root <clean-engine-path> --require-clean --output .local/ga-conformance/<attempt>
```
