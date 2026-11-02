# Proposed owned scheduler collector conformance

2026-11-02. Status: proposed next experiment, NOT executed or capture-qualified by ADR0026. It requires a separately frozen declaration before any workload/perf FD open. Engine, original benchmark, GC/compiler flags and #3 Blocked stay unchanged.

## Identity and data scope

Run the synthetic workload as the ordinary WSL user. Only a bounded collector may use the existing one-shot root path. No installation, mount, ACL/capability/sysctl/global tracefs filter/clock changes. Freeze collector/fixture source and binary hashes. Select an output directory with no overwrite; ownership and cleanup are scoped to the launched process/FDs.

Create a fixed, small actor-thread set before arming. Each actor reports native PID/TID, UID, process/thread starttime and PID/time namespace identifiers, then waits at a ready barrier. Independently check proc ownership/starttimes and expected image. Determine the tracepoint payload PID namespace from exact source and controlled actor observations; reconcile NSpid and collector/target namespace mappings before constructing S. A process-local/container PID must not silently become a kernel payload TID filter. These pre-arm leases are not captured-birth proof; initial scheduler states remain unknown. Unexpected/reused/dead/unleased IDs invalidate the affected scope. This static fixture does not qualify a dynamic Roslyn ThreadPool; a separate dynamic-thread ownership/coverage design is required before a real generator lane.

The collector observes per-event/per-CPU tracepoint FDs, filtered by event payload TIDs. switch uses prev_pid OR next_pid; wake/waking/new/migrate/exit/free use pid; fork uses parent_pid OR child_pid. Never treat common_pid as the wake target or process-only attachment as complete remote-wakeup coverage. Even filtered samples retain unowned switch/fork counterparty PID/comm and wake-emitter header metadata; disclose/retain this bounded scope. Do not collect an unrestricted host trace. Generic perf-record sideband/synthetic mmap/comm data may exceed sample filters; use explicitly reviewed attributes, no callchains/kcore or unrequested task/mmap/comm metadata.

## Arm and stop sequence

1. Snapshot exact eight ABI formats/IDs, all online CPU topology, namespaces and resource limits. Abort on unsupported layouts/topology changes.
2. Open every required CPU/event FD initially disabled, tracepoint type/config fixed, inherit off, close-on-exec on, forward non-overwrite buffers, sample TID/TIME/CPU/RAW plus sample_id_all. Request CLOCK_MONOTONIC per session; never rewrite global trace_clock.
3. Apply all payload filters and retain success/failure acknowledgments. If no private-filter readback API exists, record that limitation and validate positive/negative delivery independently. Any failure closes all owned FDs before releasing actors.
4. Validate target leases and recorded attributes, then enable all FDs. Record enable brackets per FD; release the ordinary-user ready barrier only after the last successful enable. Prefix states are unassigned.
5. Exercise known synthetic park/wake, CPU-running/yield and controlled migration phases without original Engine workload or tuning. Require at least two permitted CPUs for migration qualification; otherwise mark that gate unsupported. Cross-CPU record order/ties remain uncertain until validated.
6. Predeclare sacrificial actors from the already-leased static set that exit while collection is still armed, so exit/free delivery can actually be checked. Remaining actors and controller hold their final barrier. Observe RCU-delayed free for a fixed bounded post-join window; missing free by the deadline remains unknown/failure, not a favorable-rerun reason. Guard identity reuse and exclude post-end events from ownership. Only then disable every FD for the remaining controlled scope, drain buffers and record stable head/tail/counter snapshots. No partially drained terminal tail is a zero-loss pass. Retain raw bytes and every decoder rejection. Stop/join only owned children; check no owned process/FD remains.

## Fixed gates required before a positive lane

- Permission: successful owned perf_event_open and exact attributes/filter acknowledgments; root file readability alone is insufficient.
- Delivery/filter scope: all declared owned actors have switch/wakeup and lifecycle evidence appropriate to observed windows. Separate controlled nonmember activity proves filters do not use emitter ID by mistake. No automatic child ownership expansion. A separately declared negative membership case may create a known nonmember child from a leased parent to validate parent-side fork filtering; mark that child scope unowned/rejected and do not fold it into the positive static-actor proof.
- State: decode raw prev_state/preemption flags using exact source, require complete known switch-out/wakeup/switch-in chains, propagate migration and initial/final unknowns. A missing wakeup is not zero runnable delay.
- Clocks: validate session clock attributes, compare native monotonic marker brackets, preserve uncertainty/steps/ties and per-CPU ordering. Do not merge different executions or infer time from record index.
- Loss: retain LOST/overrun/throttle/decoder accounting per buffer/event and terminal drain. LOST can be emitted only after space returns, so absence of a final LOST record is insufficient. Where supported, investigate independent read-format lost counters; unavailable accounting stays unknown. Predeclare a separate intentional-overflow negative conformance case before any positive lane.
- Perturbation/resources: record collector CPU/cadence/buffer size and target phase counts. No latency/CV/speedup/qualification from a synthetic single lane.

Only after these gates pass should a separately declared complete diagnostic lane be considered. This proposal changes no Engine task gate, runtime maturity, original benchmark threshold or provider/supported-Windows/reference/production/release status.
