# ADR-0030 Admit owned threads at kernel birth

- Status: accepted for offline validation and one unattached verifier probe. Native collection is proposed.
- Date: 2026-11-05
- Deciders: Cehpalon program, #20 evidence lane

ADR0029's static actor lease covers known TIDs. A userspace process-list poll can observe a new TID after its first wake, switch, or exit. A TID from that poll alone also carries no execution-scoped birth identity.

Select kernel-side admission at `task_newtask` for a bounded synthetic target. The matching WSL source initializes the thread PID and birth fields before that hook, then reaches `wake_up_new_task` in `kernel_clone`. Enroll only a `CLONE_THREAD` child of an already enrolled active parent, in the same thread group and PID namespace. Read the native/global TID and the owning namespace's local TID at birth, while the task PID pointer is still available. Bind those IDs to a fresh generation. The kernel task pointer and birth marker stay private to the collector; records carry generation numbers and owned numeric identities. [WSL fork source](https://github.com/microsoft/WSL2-Linux-Kernel/blob/linux-msft-wsl-6.18.54.1/kernel/fork.c#L2258-L2642), [task tracepoint ABI](https://github.com/microsoft/WSL2-Linux-Kernel/blob/linux-msft-wsl-6.18.54.1/include/trace/events/task.h)

## Options and consequences

- Adding userspace filters on discovery reuses the static implementation and leaves an unbounded admission gap before the filter takes effect.
- Attaching by task or cgroup simplifies emitter scoping. A complete scheduler lane also needs switches involving an owned incoming task and wakeups emitted remotely for an owned target. Emitter scoping alone cannot establish that coverage.
- Numeric-only kernel enrollment can precede first wake. It leaves a weaker generation and namespace contract at late lifecycle hooks and PID reuse.
- BTF-backed admission permits birth-bound ownership and namespace mapping. It depends on an exact kernel layout, source-reviewed attachment ABI, verifier support, explicit loss accounting and tightly limited transient inspection of task arguments. This is the selected route for synthetic conformance.

## Proposed native scope

Hold one ordinary actor before admission. Evaluate pidfd-keyed task storage for the initial owner binding, using the typed current-task helper. Direct storage access from arbitrary legacy raw tracepoint argument slots requires separate verifier support. Keep the admission gate closed until the seed matches the independently held lease. Preserve the exact boot, layout, namespace and collector provenance. Start with a no-exec, fixed-capacity fixture. Latch an owned `sched_prepare_exec` before identity mutation and inspect only its task argument. Validate lifecycle with an enrolled generation and a minimal kernel-side key through final free. Cache identity at birth and avoid detached PID or group-leader reads at free. Abort on ambiguous reuse or loss.

Wake selection uses the target argument, with separate evidence for emitter and target CPU. Native proof must account for raw hook arguments that omit normalized fields and require an independently validated target-CPU reading. The switch hook checks both sides in kernel. Exclude other processes and their identities from output. A fixed-size ring and terminal attempt/publication/failure counters must reconcile with the complete drain. Allow only finite tests, with no pinning or host setting changes. Cover external emitter, fork exclusion, deliberate loss, rapid exit, late free, lifecycle timeout, and cleanup before accepting dynamic readiness.

The offline replay contract checks a narrow sanitized projection of births, first wakes, switch-ins, remote waking/wakeup observations and exit/free. It takes publication order as input. The producer must establish how ring reservation, sequence and hook order correspond across CPUs, and verify negative controls, source identity and counter provenance independently. Remote waking and wakeup observations can refer to different generations. The fixture rejects live numeric-ID collisions, which is intentionally conservative for PID reuse before free. Roslyn requires a separate protocol for same-execution CLR/TPL/GC and scheduler joins, source/build provenance, clock, perturbation and explicit unknown intervals.

## Frozen verifier probe

Run once as root on Ubuntu WSL x86_64, kernel release `6.18.54.1-microsoft-standard-WSL2`, with the exact observed raw vmlinux BTF SHA recorded by the probe. Verify the fixed nine-instruction program and input source hash before invocation. Load a legacy raw tracepoint program with one typed current-task helper call and one four-byte probe-read of the pinned task PID layout. Zero return value, no context reads, map, attachment, actor or event output. Limit verifier log to 64 KiB and close a successful FD immediately. Retain the invocation, bytecode, verifier result and cleanup outcome. A successful load qualifies verifier acceptance of these instructions only. Any refusal is retained as the result of this attempt.

The single load was accepted and the FD closed. The verifier processed nine instructions. See the [delivery record](../evidence/dynamic-scheduler/delivery.json).

The follow-on [native preflight](../validation/dynamic-scheduler-native-preflight.md) accepted the task-storage and scalar target verifier programs and confirmed actual held-owner userspace seeding through pidfds. A named hook and synthetic lifecycle remain separate acceptance gates.
