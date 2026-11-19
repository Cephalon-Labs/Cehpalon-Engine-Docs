# Aggregate publication under concurrent observation

The fixed concurrent protocol compares four independently scheduled fixture tenant producers with a waiting or continuously reading observer. Each lane runs 100,000 successful protected operations. Every operation resolves fresh configured authority and disposes its owned handler. The observer checks capacity and tenant-count consistency. [Protocol and candidate declaration](../validation/budget-contention-observation.md)

The baseline uses the tenant budget's admission lock for each snapshot read. The candidate publishes a 64-bit aggregate after each admission, release and close while holding that lock. Its getter reads the published aggregate atomically. The encoded values hold the active operation count, active tenant count and closure flag. Immutable configured limits remain in their existing fields. Publication on the final release precedes drain completion.

Both designs expose detached aggregate values. A snapshot can become stale immediately after it is read. Host operations still use the normal admission path and fresh tenant authority. The new reader avoids entering the admission lock, while each state change now performs one additional atomic publication.

## Results and tradeoff

Baseline `026cdaef0cd85796caddd25b0a32b42b0777a80c` and published-state candidate `9f9ce74f7ce2b38e992b580443648ba0fe7098af` each completed five pairs on both hosts. All four series validated one million successful operations apiece, with fresh authority and exact factory/disposal counts. All observed snapshots satisfied the aggregate invariants, and every lane ended empty and closed after drain. The candidate also passed 520 Windows and 517 WSL component checks and all 159 actual generated Small API checks on each host.

Each table entry measures wall time in milliseconds for 100,000 offered operations. The paired difference is the median of the five signed observed-minus-control differences.

| Host and revision | Control median | Continuous observer median | Median paired difference |
| --- | ---: | ---: | ---: |
| Windows baseline | 52.72 | 93.86 | 34.92 |
| Windows published state | 62.20 | 73.44 | 11.09 |
| WSL baseline | 60.33 | 97.81 | 29.54 |
| WSL published state | 65.26 | 76.90 | 13.16 |

The candidate's continuous-observer median decreased on both hosts, while the control median increased. Its accepted design moves observer reads off the admission lock and adds one aggregate publication to each state mutation. These shared-host series bound the observed tradeoff. Source changes, runtime phases, CPU competition and scheduling can contribute to the timing differences.

The continuous reader is deliberately unthrottled. The baseline observer completed about 0.42–0.89 million reads per lane. The candidate completed about 38.66–88.98 million, so the observer's work count also changed. All candidate observer loops recorded zero current-thread allocated bytes. Baseline observer loops recorded 0–232 bytes. Waiting control observers recorded 88–472 bytes and are retained in the raw series. Producer lanes stayed around 544 bytes per completed operation. No actor allocations were subtracted.

Both revisions, full pair results, source manifests, executable hashes, consumer results and the analyzer are retained with SHA-256 checksums. The analyzer rejects missing pairs, duplicate actor identities, incomplete cleanup and an open terminal state after drain. Serialization/export work, practical polling frequencies, lock-wait attribution and canonical benchmark qualification remain open. [Retained evidence](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/8143add7e1aa3efba70898fc9ff870d84952641a/tenant-identity/evidence/2026-11-19-budget-contention)

Hosted portable and platform workflows passed for the final Engine revision. Platform smoke recorded 12 passed checks on Windows Server 2025 and Ubuntu 24.04, with PostgreSQL and RabbitMQ fixtures unrun on both. #3 remains Blocked. No GitHub step was skipped for usage or billing in this delivery. [Portable CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44538849076) · [Platform CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44538849091)
