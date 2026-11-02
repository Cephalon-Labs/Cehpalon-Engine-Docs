# ADR0027 - Owned synthetic scheduler collector conformance

Date: 2026-11-02 (Asia/Bangkok). Status: accepted bounded implementation; B1 observed, B2 gated on namespace mapping. #3 remains Blocked.

ADR0026 provides exact scheduler formats and a proposed [conformance protocol](../planning/scheduler-conformance-protocol.md), but not active collection readiness. This wave implements a minimal collector and synthetic actor fixture to test those gates. It does not launch Roslyn, change Engine, rerun the original benchmark, change thresholds/primers/GC/compiler concurrency or claim a performance cause.

## Staged declaration

Stage A permits source development, offline fixtures, and a frozen native build only. Root records exact source, command and binary hashes before any actor or perf FD is launched. A separate execution declaration in the ignored evidence directory must fix actor set/phases, CPU topology, resource limits, overflow negative case, positive case, stop/drain deadlines, filters and loss/clock/identity gates before any target/perf_event_open. Source revisions after a failed attempt require retained old bytes and a stated collection correction; no favorable rerun selection.

Only the bounded collector may use the existing one-shot WSL root path. The target runs as ordinary UID1000. No installation, mount, ACL/capability/sysctl or global tracefs configuration writes; no unrestricted host recording or generic perf sideband. Per-CPU/event tracepoint FDs open disabled, with exact payload membership filters acknowledged on all FDs before enable and target release. Forward rings request TID/TIME/CPU/RAW, sample_id_all and per-session CLOCK_MONOTONIC; no task/mmap/comm/callchain sideband. Counterparty/header metadata inherent in filtered events remains disclosed.

The fixture uses precreated static actor identities, independently checked UID/image/starttime/NSpid/PID+time namespaces, with known park/wake, running/yield, controlled migration and armed sacrificial-exit phases. Initial/final states and missing delayed-free observations remain unknown. Negative overflow accounting precedes positive qualification; terminal absence of LOST is insufficient without independent counters/drain validation. Unsupported permission/ABI/resources/loss/namespace/clock/delivery gates remain explicit failures or unknowns. Close only owned FDs/processes; preserve every attempt.

Root is sole integrator/remote writer. Bounded code work uses an isolated features/ worktree; independent review must inspect actual retained bytes. This static proof cannot qualify dynamic Roslyn ThreadPool capture or establish CPU/GC/scheduler causality. Keep active_capture_ready=false for the generator lane, all original gates and #20 metadata/dependencies/estimates/null hours, and #3 entire row unchanged. Sync only #20 body through reviewed plan/readback. No provider, supported-Windows, reference, production or release qualification follows.

## Observed execution outcome

The staged execution declaration narrowed this wave to B1: one initially-disabled sched_switch FD open/read/close, with zero actors/filter/mmap/enable/records. Frozen source and exact argv preceded the single real invocation; accepted attrs/read_format23,40-byte zero-counter read and closure/EBADF were observed.98offline fixtures passed eachWindows/WSL; independent review checks actual retained bytes. No C/native build occurred; the tool uses existing Python ctypes on reviewed Linuxx86_64 ABI.

B2 collector/actor implementation and execution did not proceed: source and read-only observations do not establish initial-PID-namespace payload mapping. Parent EPERM and own-namespace self-translation are not that proof. All active capture/filter/loss/clock/state gates remain untested/false. Original benchmarks/Engine/host configuration/#3 unchanged. [Report and next gate](../planning/scheduler-conformance.md).
