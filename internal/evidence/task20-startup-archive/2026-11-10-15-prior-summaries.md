### 2026-11-10 Scoped scheduler entry/exit fixture (ADR0031)

Engine remains `55c630fc5d4c47258a1a2b0da4a16ce8bc42b9f7`. Both named boundary hooks attached to an owned leader and one newborn worker. Negative:184 attempts/1 row/183 capacity losses; positive:182/182, zero loss. Generation-local accounting gives25 switch and64 no-switch pairs,9 with CPU change, plus explicit seeded/newborn prefixes and open tails. Both cases close32nativeFDs. Tests144each Windows/WSL pass. Native entry-preempt-true coverage remains unobserved; physical timing, GC cause and speedup are uncertified. Next freeze CLR ThreadPool boundary/overhead controls before Roslyn. #3 remains Blocked; metadata/gates/hours/originalbenchmark unchanged. [Report](https://github.com/Cephalon-Labs/Cehpalon-Engine-Docs/blob/main/internal/planning/scheduler-boundary-fixture.md).


### 2026-11-15 CLR ThreadPool boundary hooks

On pinned WSL 6.18.58.1, the real managed worker joined native boundaries in all six instrumented cases. All 942 rows reconcile. The four paired incremental observer deltas were +16,984 to +204,360 ns (median +193,382 ns) on the fixed pipe fixture. [Results and limits](https://github.com/Cephalon-Labs/Cehpalon-Engine-Docs/blob/main/internal/planning/clr-threadpool-boundary.md).

Roslyn captured 175,352 scheduler boundary rows on WSL 6.18.58.1. [Same-execution Emit, TPL and GC findings](https://github.com/Cephalon-Labs/Cehpalon-Engine-Docs/blob/main/internal/planning/roslyn-emit-boundaries.md).
