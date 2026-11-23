# 2026-11-23 .NET 11 GA platform and real driver compatibility

Issue #3 is closed and Project 4 reports Done and Test gate Passed.
Observed Windows Server 2025 x64 and WSL Ubuntu 22.04.5 x64 both passed all
14 platform checks with .NET 11.0.0 and real PostgreSQL 18.6 and RabbitMQ
4.4.0 / OTP 29.1.2. Native Windows artifacts and Linux OCI images were
verified against separate pins, and both fixture owners confirmed cleanup.

Engine `a6fb5ace` adds explicit GitHub workflow dispatch for the native
Windows lane. The regular Windows and Linux no-server matrix still runs for
push and pull request. The Windows observation used the exact clean commit.
The Linux harness ran from `c18757f` with all seven relevant inputs matching
`a6fb5ace` byte-for-byte. Local build 26300 supplied preparation/rehearsal
evidence. Hosted build 26100 supplied the supported Windows proof.

Keep W1 component, W0 dedicated Small API reference and downstream business
or AI provider qualification tied to their separate criteria. Project
maturity remains M0. [Validation and retained evidence](../validation/windows-native-platform.md)
