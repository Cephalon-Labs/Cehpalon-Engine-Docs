# Audit receipt collector contention on Windows and WSL

Engine issue #18. Observed on exact clean Engine
`6fe7254404cf6b148370bd95befe8331e8932354` with SDK 11.0.100 and runtime
11.0.0. Windows 11 build 26300 and WSL Ubuntu 22.04.5 were tested serially
on the same workstation. Both processes reported 20 available logical
processors. See the [protocol, frozen inputs, raw trials and replay](../evidence/audit-read-contention/2026-11-23/).

The real Engine audit receipt reader used a synchronous empty source
inside a checked tenant dispatch. Each worker owned its fixture and receipt
reader. Within each worker count, 12 matched rounds compared the collector
disabled, one collector per worker, and one shared collector. Numbers below
are aggregate elapsed time divided by completed reads, in ns/read. Each
contrast pairs modes within a round.

| Host | Workers | Disabled median | One per worker median | Shared median | Shared minus disabled median (range) | Shared minus one per worker median (range) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Windows | 1 | 85.69 | 89.73 | 89.66 | 3.95 (0.92 to 38.50) | 0.05 (−13.68 to 34.65) |
| Windows | 2 | 43.19 | 45.28 | 61.80 | 18.45 (16.42 to 20.32) | 16.19 (14.05 to 18.09) |
| Windows | 4 | 24.37 | 23.01 | 38.06 | 14.73 (12.54 to 16.17) | 14.09 (9.70 to 20.68) |
| WSL | 1 | 100.55 | 102.92 | 102.88 | 2.46 (1.10 to 12.22) | −0.04 (−0.34 to 9.87) |
| WSL | 2 | 49.61 | 51.24 | 68.44 | 18.82 (8.26 to 19.73) | 16.48 (14.40 to 17.84) |
| WSL | 4 | 30.82 | 29.79 | 35.31 | 8.23 (−0.72 to 15.80) | 7.78 (−2.70 to 15.77) |

Each host completed 108 measured blocks and 18 warmup blocks, totaling
67,200,000 reads including warmup. All provider and outcome counts matched.
Shared collectors recorded 22,400,000 successes per host and personal
collectors recorded the same aggregate total. All other outcomes were zero.
Every measured loop recorded zero current-thread allocated bytes. All
multi-worker measured intervals overlapped. Maximum start skew was 0.071 ms
on Windows and 0.142 ms on WSL.

The two-worker shared penalty appeared in every matched round on both
hosts, including both relative orders. The WSL four-worker comparisons
spread more widely and each shared contrast had a negative observation.
The full [summary](../evidence/audit-read-contention/2026-11-23/summary.json)
retains all observations, order splits and skew. The shared-versus-personal
difference includes collector layout and scheduling. Worker intervals show
overlap in elapsed time. They provide no CPU residency measurements. The
clock covers the read loop and worker skew, and the fixture excludes
networking, external providers, exporters and request latency. The result is
a component observation on shared hosts. #18 remains In Progress at M0
and the original benchmark gates still apply.
