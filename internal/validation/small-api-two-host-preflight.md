# Small API two-host TLS preflight

Follow-up on 2026-11-24: [W0 machine allocation and staged deployment](../planning/small-api-w0-machine-allocation.md).

The Samples runner now accepts a private two-host configuration for
Small API. The controller runs on the app machine. It checks the
locked Release deployment, launches the app on a private IPv4 TLS
1.3 listener, and starts the unchanged .NET load client through SSH
on a separate Linux machine. The driver validates the ephemeral
fixture CA and the IP SAN using the standard TLS checks. The socket
accepts only the configured driver peer and the app controller
address. The fixture server key remains on the app machine.

The controller pins the SSH host key and compares the whole staged
deployment. It sends the public CA, owns each driver job through an
SSH lease, checks the returned file hashes and retains partial
evidence on failure. The application and driver use the pinned
.NET and ASP.NET Core 11.0.0 runtimes.

## Executed lab results

The integration used separate controller/app and driver network
namespaces on a single WSL Linux machine. It ran committed Samples
`1d984b0238bd614cb7c78675286ae25192ec9fac` and Engine
`5e92ac1c7fa1e150e7e97de6d68e94b31ffba053` with .NET SDK
11.0.100. The locked deployment contained 67 files.

| Remote lane | Held TLS 1.3 / HTTP 1.1 connections | Correct actual offers |
| --- | ---: | ---: |
| Baseline HTTP | 128 | 2,000 / 2,000 |
| Engine HTTP | 128 | 2,000 / 2,000 |
| Baseline GraphQL | 128 | 2,000 / 2,000 |
| Engine GraphQL | 128 | 2,000 / 2,000 |

Each lane completed 130 read-only preparation requests, followed by
two seconds of collector preflight at the unchanged 1,000 requests/s.
All 8,000 raw observed rows matched the executed prefix of the ordered
manifest. Each lane validated the final synthetic state and retained
the joined driver and app shutdown receipts. The 180,000 planned rows
per lane were frozen preflight inputs. The controller entered no
benchmark startup, idle, warmup, measured load or diagnostic phase.
[Retained observations and raw files](../evidence/small-api-remote-preflight/2026-11-24/two-host-lab-preflight.json)

The trusted endpoint negotiated TLS 1.3. The fixture and client
rejected a wrong CA, wrong IP SAN, TLS 1.2, and an unlisted peer.
The controller stopped before starting a collector when offered an
incorrect SSH host key or insufficient reference environment evidence.
In a separate SSH test the remote client reached an owned held TCP
listener. Closing its controller lease joined the remote process and
returned a structured exit-124 receipt. The fixture containers and
network were removed.
[Plan](../planning/small-api-two-host-preflight.md) ·
[Samples invocation](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/blob/1d984b0238bd614cb7c78675286ae25192ec9fac/small-api-benchmark/README.md#two-host-reference-execution)

The first lab setup failed to read the staged helper under the driver
UID. Once corrected, the host-to-self WSL route presented a rewritten
source address and was rejected by the listener. The passing setup used
two owned network namespaces with direct routing. The allowed-peer
policy remained in effect on the passing attempt.
[Retained attempt notes](../evidence/small-api-remote-preflight/2026-11-24/lab-attempts.json)

The hosted GA locked Release builds passed on Ubuntu 24.04 and
Windows Server 2025 against the exact pull-request test tree.
The Ubuntu job passed all 52 collector, remote transport, resource
and admission unit tests. The original local orchestrator invocation
also completed its loopback preflight with an observational verdict.
[Samples PR #6](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/pull/6) ·
[Hosted GA run](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/actions/runs/45263890953) ·
[Ubuntu build manifest](../evidence/small-api-remote-preflight/2026-11-24/hosted-build-ubuntu-24.04.json) ·
[Windows build manifest](../evidence/small-api-remote-preflight/2026-11-24/hosted-build-windows-2025.json)

The locked local GA conformance rerun passed all 4,000 ordered cases,
including 400 cancellations, and 120 lifecycle cycles on WSL.
The workload, driver, conformance and package-lock bytes agree with
the previous Samples baseline. The timing and scoring methods and
the governing W0 documents match the original bytes.
[W0 and conformance check](../evidence/small-api-remote-preflight/2026-11-24/original-w0-and-local-conformance.json)

## Timing admission

The W0 gate still requires Linux x64, two dedicated application CPUs,
an enforced 2 GiB app cap, and independent driver resources. The two-host
runner checks the complete visible cgroup v2 hierarchy, the actual
app PID and its exclusive CPU partition, controller affinity and
cgroup pressure counters. It compares the driver host identity and
actual driver allocation over SSH. The cgroup checks describe the
visible Linux allocation. Confirm any upstream physical or hypervisor
reservation on the provisioned hosts.

The runner requires four successful real-host TLS and collector
preflights before entering the whole original phase sequence. Original
pair order, startup bracket, durations, offered rate, outstanding cap,
deadlines and thresholds are preserved. The app launch-to-response
clock includes its process launcher. An offline audit checks successful
canonical idle and load evidence before a full reference pass can be
reported.

Reference timing remains blocked. No approved app and independent
driver pair with verified W0 resources was found in the available
inventory. The cross-namespace lab only exercised the transport and
collector path. It ran no full benchmark.
[Current host readiness](../evidence/small-api-remote-preflight/2026-11-24/reference-host-readiness.json) · [Original W0 criteria](small-api-workload.md) ·
[Collector requirements](../adr/ADR-0011-small-api-collector-connection-readiness.md)
