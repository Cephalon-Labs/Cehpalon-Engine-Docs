# Core dispatch completion correlation

Engine issue #18. Engine `5e92ac1c7fa1e150e7e97de6d68e94b31ffba053`
adds an opt-in observer on a selected Core dispatcher. It captures detached
W3C trace and span IDs at the validated registered dispatch boundary,
before histogram publication. After handler cleanup, the host receives an
outcome, a duration and the optional IDs. The host supplies the callback
and controls where to send the fixed event. Existing histogram dimensions
are preserved. [Implementation](https://github.com/Cephalon-Labs/Cehpalon-Engine/commit/5e92ac1c7fa1e150e7e97de6d68e94b31ffba053) · [Contract and acceptance plan](../planning/observability-trace-correlation.md)

## Core and protected HTTPS

A locked .NET 11.0.100 Release build of the exact Engine commit passed 42
Core checks on Windows and WSL, including seven new completion checks.
They cover entry-time capture before instrument publication, absent and
hierarchical ambient IDs, cleanup and outcome boundaries, observer
exceptions and same-flow recursion across asynchronous work. The initial
WSL preparation stopped because Linux Git could not resolve a Windows
worktree's metadata path. A Linux-created clone at the same revision
passed the build and tests. [Core reports](../evidence/dispatch-correlation/2026-11-23/core/)

The Samples proof scaffolds the protected Small API from the exact Engine
CLI and builds an instrumented copy. The copy opts in at the outer gateway
and independently reads the native ASP.NET request Activity. The callback
uses an in-memory structured projection. Published reports contain counts,
bounded outcomes and comparison flags.

| Scenario | Completion records | Core histogram observations |
| --- | ---: | ---: |
| Owner, per transport | 1 success | 2 |
| Authenticated tenant denial, per transport | 1 failure | 1 |
| Anonymous, per transport | 0 | 0 |
| Owner with observer disabled, per transport | 0 | 2 |
| Four parallel fields in one GraphQL request | 4 successes | 8 |

The fixture also verifies absent and malformed trace headers against native
host interpretation. Four independent HTTPS requests held their handlers
before releasing the barrier, with distinct request traces. The GraphQL
alias case held four handlers under one request trace. Checked event fields
excluded private fixture sentinels and both hosts disposed owned handlers
and closed their loopback ports. This evidence applies to the selected
outer gateway, its fixture sink and generated protected HTTPS.

Windows and WSL each passed all 17 wire cases with 16 completion records,
34 histogram observations, two verified shutdowns and zero unscoped
signals. The results matched case for case and both hosts resolved the
same consumer dependency graph. Each platform's original package lock
bytes and manifest are retained. [Samples harness](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/902b18bb3f348fb68744a4ec2cbf93595ce20a5b/tooling-small-api/dispatch-correlation) · [Wire receipts and build manifests](../evidence/dispatch-correlation/2026-11-23/https/)

The exact Engine revision also passed the hosted checks on Windows Server
2025 and Ubuntu 24.04, with 1,553 and 1,550 contracts respectively. Both
default platform smoke jobs had 12 passes and two real-provider
cases that did not run. [Hosted result summary](../evidence/dispatch-correlation/2026-11-23/engine-hosted.json)

## Component observation cost

The fixed paired experiment dispatched 10 million synchronous operations
per host, including warmup. It compared the two constructors on the same
Engine revision. All owned handler cleanup, result and completion counts
matched. The loop also checked entry-time IDs and durations in the
enabled callback.

| Host | Ambient context | Paired enabled minus disabled median (range), ns per dispatch | Current-thread allocation delta, bytes per dispatch |
| --- | --- | ---: | ---: |
| Windows 11 build 26300 | Absent | 61.92 (57.75 to 66.99) | 72 |
| Windows 11 build 26300 | W3C | 90.08 (88.85 to 92.03) | 160 |
| WSL Ubuntu 22.04.5 | Absent | 74.31 (71.39 to 75.96) | 72 |
| WSL Ubuntu 22.04.5 | W3C | 109.21 (107.07 to 118.75) | 160 |

Measured baseline allocation was 24 bytes per dispatch in every timed
arm with the observer disabled. Current-thread allocation was constant
within each enabled ambient state during measurement. The timing includes callback checks,
synchronous dispatch and handler lifetime. The protocol excludes logging,
export, network and provider costs. These are component measurements on
one shared workstation. A prior-revision regression comparison and
production benchmark qualification remain open.
[Protocol, raw trials and replay](../evidence/dispatch-correlation/2026-11-23/component/)

#18 stays In Progress at M0. The remaining observability scope includes
supported-path shutdown and recovery, exporter effects and workload
measurement under the original gates.
