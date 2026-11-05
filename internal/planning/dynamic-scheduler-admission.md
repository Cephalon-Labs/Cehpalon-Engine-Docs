# Dynamic scheduler admission for #20

Date 2026-11-05. See [ADR0030](../adr/ADR-0030-dynamic-scheduler-admission.md), [ADR0029's static result](static-scheduler-conformance.md) and the [delivery record](../evidence/dynamic-scheduler/delivery.json).

The dynamic lane addresses a specific gap in the static trace. Existing leases can bind threads that are still alive. They cannot bind a worker that is created, wakes and exits between process-list reads. The proposed collector binds an owned generation at the kernel's birth hook, while global and namespace-local TIDs are both available. Later hooks match the admitted generation on the target side, including a wake emitted on a different CPU.

## Evidence levels

| Step | What it can establish |
| --- | --- |
| BTF inspection and retained raw blob | Exact selected structure offsets and field shapes for the observed kernel layout |
| Offline replay | A finite record contract for the projected synthetic fixture, including unknown generation, missing first wake, overlapping TID reuse, post-free references and terminal loss |
| Unattached verifier probe | Kernel acceptance or refusal of the fixed minimal raw tracepoint program at load time |
| Scoped synthetic execution | Actual same-execution held-owner seed, owned first wake, remote target selection, negative controls, loss, exit/free and cleanup |
| Roslyn lane | A separate, provenance-bound join of actual CLR/TPL, GC and scheduler events with explicit uncertainty |

A successful verifier call supplies no execution, attachment or scheduler-event evidence. The replay validator relies on separately authenticated input and accounts only for its declared projection. It does not pair remote waking and wakeup into a single wait or derive a duration.

## Observed on 2026-11-05

- The retained BTF file was 6,018,902 bytes. Windows and WSL extracted byte-identical layouts, including signed four-byte `task_struct.pid` at offset 1360 and the flexible `pid.numbers[]` tail. The offline layout and replay suites passed 36 tests per host. The raw BTF describes the observed layout. It cannot attest the complete running kernel binary.
- The one frozen WSL root probe loaded successfully. The verifier processed all nine instructions and the program FD closed successfully. The loaded program made no event attachment and executed no hook. Task-storage map support, typed owner lookup, scalar remote-target reads and native delivery remain untested.
- The follow-on native preflight passed the held-owner userspace task-storage test and both separate unattached verifier loads. The nine pidfd receipts include alias lookup, duplicate rejection, an unseeded control and post-reap absence. See [the protocol](../validation/dynamic-scheduler-native-preflight.md) and [the native preflight evidence](../evidence/dynamic-scheduler-native-preflight/delivery.json).

Source review and the offline layout work ran separately from the native operator. The retained source review pins the Microsoft WSL revision and the audit verifies raw source hashes. Matching observed release and BTF do not establish full binary attestation. [Retained source review](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/blob/main/tooling-traces/evidence/2026-11-05-dynamic-scheduler/source-review/dynamic-kernel-review.md)

## Native acceptance required before Roslyn

1. Verify the held ordinary actor's executable, boot, PID namespace, pidfd and live local/global identity in the same execution. Open admission only after the root seed is bound. Keep one authorized owner and a fixed generation budget.
2. Exercise child admission before first wake and first switch. Require at least one short-lived child and one child that creates a later child. Check each child against an independently controlled target marker. Exclude an ordinary process fork and an unrelated actor. Invalidate any exec that can change the enrolled identity.
3. Validate wake target selection and actual target CPU for the exact hook ABI. Show a controlled wake from a different CPU. Attach all needed hooks before actor release. Treat after-exit references as outside active attribution and bind final free to the cached generation within the declared deadline.
4. Freeze record, memory, CPU, time, output and generation limits. Demonstrate rejection of deliberate loss, then independently run the fixed positive case. Require full publication/counter reconciliation, complete drain, no helper or recursion misses, and measured perturbation and cleanup. Preserve every attempt.
5. Define the Roslyn lane separately after the synthetic result. It needs clock binding, exact runtime branch/build/binary correspondence and a complete enough same-execution CLR/TPL, GC and scheduler join to distinguish evidence gaps from attributable waits.

The first active synthetic check should prove that a named, reviewed hook can recognize the same held ordinary owner from a typed current task. Use a closed gate, a fixed seed cookie, an explicit owner marker and a nonmember control. Preserve only a bounded acknowledgement for the owned task. Then bind the validated seed to the kernel birth and target-side scheduler hooks and test the complete lifecycle in a separately frozen run.

No Engine revision or original benchmark configuration changes in this lane. The original benchmarks remain Observed and unqualified. #20 stays In Progress with its existing test and benchmark gates. #3 stays Blocked.
