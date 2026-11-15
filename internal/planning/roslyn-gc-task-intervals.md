# Blocking GC within Roslyn task and scheduler intervals

The replay used the retained #20 Roslyn run with stack sampling and precise allocation reads disabled. Both native ledgers matched their detached second reads. The clock and identity checks reproduced the earlier 30 caller waits overlapping linked blocking GC. Of 1,930 bound caller waits, 1,928 also had a bound task lifetime from TPL start and completion records. The caller and task had a positive guaranteed intersection for 1,811 waits. Another 102 shared only a possible outer intersection and 15 had no shared interval. Two caller waits and two task lifetimes lacked a positive guaranteed core. [Protocol](../validation/roslyn-gc-task-intervals.md)

| Observed evidence | Distinct waits |
| --- | ---: |
| Linked blocking-GC inner interval overlaps the caller wait | 30 |
| That GC interval also overlaps the guaranteed caller/task intersection | 27 |
| That intersection has both linked GC overlap and a worker scheduler pair | 18 |
| The entire inner GC interval is between the worker's scheduler entry and return receipts | 15 |
| An individual worker entry or return receipt bracket overlaps the inner GC interval | 0 |

The 64 waits with worker pairs contained 376 distinct pairs, including 261 switch and 115 no-switch pairs. The 15 waits with an inner GC interval between worker receipts had one such switch pair each. Eight additional pair-by-episode links overlapped only the possible outer GC envelope. There were no matched no-switch pairs in either interval. The paired worker and the GC emitter had different thread generations in the 15 inner overlaps.

Every one of the 15 switch pairs showed the same recorded order. Worker entry was after `SuspendEEStart` and before `SuspendEEStop`. The worker lifecycle then recorded switch-out with raw state 8193, waking, wakeup and switch-in in both slot and timestamp order. Waking was after `RestartEEStart` in all 15. Nine worker returns ended before `RestartEEStop`, and six began after it. The pinned WSL source defines 8193 as `TASK_INTERRUPTIBLE | TASK_FREEZABLE`. Another 61 worker pairs had the same raw state without a strict linked-GC overlap. That state cannot identify the worker's wait callsite. [State definitions](https://github.com/microsoft/WSL2-Linux-Kernel/blob/a989171929bed4ea681be8d77333845ce1c1732a/include/linux/sched.h#L106-L122) · [Scheduler callsites](https://github.com/microsoft/WSL2-Linux-Kernel/blob/a989171929bed4ea681be8d77333845ce1c1732a/kernel/sched/core.c#L6817-L6950)

The repeated order supports a GC-associated scheduling sequence within the observed task lifetime. The trace does not tie those worker switch-outs to a particular runtime wait callsite or quantify physical time attributable to GC or to the scheduler. Windows and WSL produced byte-identical wait and worker receipts and passed 15 focused tests each. No workload was rerun. #20 remains In Progress, #3 remains Blocked, and the original benchmark and acceptance gates still apply. [Delivery](../evidence/roslyn-gc-task-intervals/delivery.json)

A later fixture captured `WaitUntilGCComplete` entry and return at two exact CoreCLR instruction sites on one held worker. The retained Roslyn waits still lack callsite evidence. [CoreCLR callsite fixture](coreclr-gc-wait-callsite.md)
