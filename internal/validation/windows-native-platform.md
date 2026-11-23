# GA native-provider qualification on Windows

The Windows native job uses the existing PlatformQualification harness and
requires all 14 results to pass with zero skipped cases. It checks the
observed Windows Server 2025 caption before provisioning. The opt-in workflow
runs only the native job. Push, pull request and normal manual dispatch continue
to run the original Windows and Linux no-server smoke jobs.

The fixture verifies Microsoft SDK 11.0.100 with SHA-512, and PostgreSQL 18.6-5,
RabbitMQ 4.4.0 and Erlang/OTP 29.1.2 vendor ZIPs with SHA-256 and byte lengths.
It builds against the locked driver graph. It runs private native processes
without installing services and observes their loopback addresses and owners.
EPMD binds both IPv4 and IPv6 loopback. The driver connections use IPv4.
A successful run records versions and all 14 result names and verifies owned
cleanup. The test state and raw process logs remain private.

## Windows rehearsal

Attempt 05 passed all 14 on Windows build 26300 with .NET 11.0.0,
PostgreSQL 18.6, RabbitMQ 4.4.0 and OTP 29.1.2. The four selected TCP ports
had no remaining listeners and cleanup reported zero failures. The same
script bytes were selected for the hosted run. Build 26300 is local
observational evidence and is outside the project's checked support matrix.

Preparation evidence includes PostgreSQL inheriting redirected pipe handles,
an EPMD IPv6 loopback guard rejection, a RabbitMQ startup timeout, and a
Python executable selection failure after both native providers were ready.
The corrected attempt reused the same verified archive bytes. It set an
explicit 75-second broker startup allowance and checked the real Python
executable before starting fixtures. Failed attempts remain retained.

The native Windows packages ship the same selected provider versions as the
original Linux containers. They are different distribution artifacts.
This smoke exercises real transaction, cancellation, queue confirm and
single-node redelivery paths. Business isolation, TLS deployment and high
availability have separate gates.

## Hosted Windows Server 2025

The opt-in job ran a clean checkout of
`a6fb5ace85b3fa01fb13f121e6efcbb91f600c16` on Windows Server 2025 Datacenter
x64 build 26100. It used runner image `win25-vs2026` version
`20261116.315.1`, .NET 11.0.0 and Python 3.13.17. The job verified all four
archive digests and observed PostgreSQL 18.6, RabbitMQ 4.4.0 and OTP 29.1.2.
It passed 14 checks, with zero failed and zero Not run. The result includes
the PostgreSQL transaction/query/cancellation control and the RabbitMQ
publisher-confirm/manual-ack control. Cleanup verified zero remaining
listeners across the four owned ports and recorded no failures.

The adjacent push workflow used the regular Windows/Ubuntu no-server
matrix. Both smoke jobs passed and the opt-in job skipped as designed.

[Native job and artifact](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/45205225398) · [Default smoke](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/45205225296) · [Retained summaries](../evidence/windows-native-platform/2026-11-23)

## Linux companion smoke

The matching GA smoke also passed 14/14 with zero skipped on WSL Ubuntu
22.04.5 LTS x64. The test built the archived harness from clean Engine
`c18757f7ef4df2c78c73e902aa39d05424e6bcff`. Its seven build and fixture
input blobs are identical to those at `a6fb5ace`. The WSL client used
PostgreSQL 18.6 and RabbitMQ 4.4.0 / OTP 29.1.2 from their pinned Linux/amd64
OCI manifests and config digests. The exact owned containers, anonymous
volumes, network and temporary build/state directory were gone after cleanup.
The two local fixture ports were closed.

The hosted Windows result and the Linux companion complete the bounded
SDK and provider compatibility checks selected for #3. The existing
Small API Linux reference workload has a separate resource and benchmark
requirement under #11. The verified client smoke does not extend to a new
host deployment, provider release, topology or business acceptance gate.
