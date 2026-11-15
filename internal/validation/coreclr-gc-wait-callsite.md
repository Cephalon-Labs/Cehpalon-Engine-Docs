# CoreCLR GC wait callsite fixture

Engine #20 and ADR0031. Use the pinned WSL x86-64 release runtime and its build-ID and debuglink-CRC matched symbols. Verify the executable file offsets and instruction bytes for the call and the first instruction after the virtual `IGCHeap::WaitUntilGCComplete(false)` call inside `Thread::RareDisablePreemptiveGC`. Runtime source, loaded image and disassembly must agree.

Use two initially disabled perf uprobe descriptors bound to the single named TID of an ordinary owned fixture. Do not attach to Roslyn. Open before releasing the worker. The fixed sequence is an ordinary native sleep control, with no induced GC, followed by overlapping worker transitions and 12 explicit full blocking compacting collections on the caller. Retain output on any failure. Require exact worker PID/TID labels, zero terminal losses, raw sample totals equal descriptor counts, ordering and cleanup. The control must emit zero site samples and the GC arm must produce at least one ordered pair on that worker to pass.

A call and return identify a runtime path taken in this one fixture. The callee can return immediately, and breakpoints and the fixture perturb the target. These receipts do not establish physical blocking, guest scheduler time, throughput or the earlier Roslyn callsite. Keep original benchmark gates and #3 Blocked.
