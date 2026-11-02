# Disabled scheduler perf preflight and namespace boundary

2026-11-02, Engine #20, [ADR0027](../adr/ADR-0027-owned-scheduler-conformance.md). Engine remains `55c630fc5d4c47258a1a2b0da4a16ce8bc42b9f7`; #3 remains Blocked. This wave implements and executes only the B1 disabled-FD permission/read-layout stage. The full synthetic actor collector (B2) is not implemented or launched: kernel payload TID mapping is unresolved before filters can safely be armed.

## Observed preflight

Samples `tools/preflight_scheduler_perf.py` is a Linux x86_64-only one-shot probe, with portable injected-backend tests. It pins the ADR0026 planner/bundle, validates all eight live format bytes/IDs, checks the entire declared online topology and freezes its source before the real call. Root reviewed the execution declaration/source/command hashes before invocation; the independent reviewer found no B1 execution blocker.

Exactly one `perf_event_open` succeeded for sched_switch/config268 on CPU0, pid=-1/group=-1, CLOEXEC. The 128-byte attribute packet requests disabled, sample_id_all/use_clockid CLOCK_MONOTONIC, TID/TIME/CPU/RAW1158 and ungrouped read_format23 (enabled/running/ID/LOST); all undeclared flags/sidebands remain zero. No filter, mmap, enable, actor, workload or recording occurred. This accepts one particular disabled attribute combination, not every CPU/event or a live timestamp channel.

The single read returned exactly40bytes: value0, enabled0, running0, perf_event_id3, lost0. The perf identifier is a unique event-FD identifier, distinct from tracepointconfig268 and returned descriptor3 even where integers happen to coincide. Close acknowledged and immediate F_GETFD reported EBADF. Source/planner/bundle/live8formats, topology, interpreter image, boot/time/namespace identities passed same-invocation postchecks. The process exited0 within its fixed30second native timeout; no retry/fallback/open-again was used. `active_capture_ready=false` remains explicit.

Zero counters on a never-enabled FD do not prove lossless active delivery. No ring existed. No initial/final scheduler state, actor cleanup, filter delivery, monotonic sample brackets, migration, delayed free or overflow negative gate was tested. Source byte snapshots and file checks are observed freezes, not immutable executing-globals/binary attestation.

## Source and namespace findings

Nineteen primary-source files from the matching Microsoft WSL kernel tag and28 read-only command observations are retained with bytes/hashes/status. Tag/version correspondence does not attest the installed complete kernel binary. Compiler probes found no gcc/cc/clang/make in ordinary/root PATH; Python ctypes uses the reviewed existing syscall ABI without installation or a native build.

The matching kernel uses global/initial-PID-namespace task IDs in scheduler payload fields (`p->pid`), while perf TID headers use the namespace captured on event creation. Proc NSpid and `/proc/PID/sched` can also be namespace-relative; the latter uses `task_pid_nr_ns`, so it is not a global-ID oracle. Separate WSL probes observed boot/namespace changes; none is fused into B1's identity or a future actor lease.

Read-only `NS_GET_PARENT` on the caller's active PID namespace returned EPERM; matching source limits visibility above that namespace even for this root call. `NS_GET_PID_IN_PIDNS` can translate a caller-visible TID into an already-open destination namespace, but own-namespace self-translation702→702 proves no global mapping. No initial PID namespace FD was obtained, no namespace was entered/created and no alternate proc mount, comm bootstrap or unrestricted recording was attempted.

The matching loss implementation exposes per-event `lost_samples` in checked terminal `PERF_FORMAT_LOST` reads even when the final LOST record cannot be emitted; RESET does not reset that counter. This is an implementation design finding, not a successfully exercised overflow gate. A later collector still needs fresh FDs, stable terminal drain/counters, strict raw-ring bounds and actual memory-ordering validation.

Primary interfaces: [perf_event_open](https://man7.org/linux/man-pages/man2/perf_event_open.2.html), [kernel perf security](https://docs.kernel.org/admin-guide/perf-security.html), and retained exact-source provenance. Original upstream SPDX notices remain in source evidence; repository MIT does not replace them.

## Required next work and limits

First establish a reviewed same-execution mapping from leased ordinary-user actor TIDs to initial-namespace payload IDs, using an available proven namespace reference or another separately declared bounded mechanism. Do not infer that mapping from EPERM, matching header numbers, proc displays or an old boot. Then freeze the complete [B2 protocol](scheduler-conformance-protocol.md), collector/actor bytes and resource/deadline bounds before any actor/filter/enable: allCPU/eight-event disabled FDs, all filter ACKs before release, static owned leases, overflow negative then positive delivery, armed exit/free, migration, clocks, counters/drain, cleanup and perturbation. Static actors do not qualify dynamic Roslyn ThreadPool coverage.

No Engine optimization is justified by this preflight. The original benchmark remains Observed/unqualified with original workloads/thresholds/primers/flags/GC/concurrency. No unchanged-source benchmark was rerun. #20 stays In Progress/P2/M0 with its original dependencies, estimates, Planned Test/Benchmark gates and null hours. Existing hosted Engine runs remain payment/spending rejected before any steps; no billing or rerun action. No supported-Windows, provider, reference, production or release qualification follows.

Verification, retention and reviewed #20-body-only tracking readback are recorded in [delivery evidence](../evidence/scheduler-conformance/delivery.json). The initial Windows offline fixture failure and all tested source versions are retained, not replaced by later passes.

The implementation's98fixtures pass on Windows/WSL, and an independent reviewer completed72additional mocked guards per platform. The reviewer inspected final source before B1, then hit a usage limit after authoring the artifact audit. Root completed that audit with two recorded preparation corrections: upstream bitfield whitespace parsing and reference to frozen pre-execution ADR bytes after the outcome was appended. The initial audit exception/source remain retained. Corrected audit179checks passed over actual bytes plus all19source snapshots/28commands. This is an agent-authored audit executed/completed by root, not a separate final agent signoff or another perf run.
