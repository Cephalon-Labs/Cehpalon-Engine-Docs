# Operation concurrency budget handoff

The user requested a product improvement to engine flexibility, security and performance. The bounded #18 delivery adds an opt-in, in-process limit for business handlers including owned cleanup. Fresh tenant authorization precedes admission. See the [report](../planning/operation-concurrency-budget.md), [ADR](../adr/ADR-0032-operation-concurrency-budget.md) and [test and benchmark protocol](../validation/operation-concurrency-budget.md).

Engine main `2bd9cfcaf4b9328a76b36102c094de6f7fd97e17` passed Windows 512, WSL 509 and actual Windows CLI-generated Small API 39. Keep both fixed-protocol timing sets and the fast-path patch in the linked Samples evidence. The experiment lowered the WSL median and raised the Windows median. It remains at detached `cbfb082473183e658ea6c4f955fd77e8b6029482`. Main uses the first implementation.

#18 remains In Progress at M0 with Test and Benchmark Planned. Hosted checks were rejected before job steps by billing or spending-limit policy. Continue with a scoped real workload or a distinct resilience/telemetry slice when authorized. #3 remains Blocked and #20 remains In Progress.
