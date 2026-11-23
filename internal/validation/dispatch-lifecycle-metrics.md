# Dispatch and lifecycle histogram validation

This #18 slice adds bounded `System.Diagnostics.Metrics` histograms to Core
dispatch and Composition lifecycle attempts. Phase and outcome are the only
measurement dimensions. A dispatcher invocation is the unit of the Core
instrument. Composition records one completed activation, rollback or disposal
attempt for each resource it operates on.

First publication can invoke a listener inline. A single caller attempts
publication without holding an application lock. Concurrent and reentrant work
may proceed without observations during publication. If a listener throws, Engine
disposes the failed meter on a best-effort basis and skips that histogram for the
rest of the process. A throwing measurement callback also leaves the application
result intact. Listeners execute synchronously and can delay the caller. They
must return without waiting on the lifecycle attempt they observe.

## Test matrix

- Start fresh processes for first publication, throwing publication and cleanup
  callbacks, and concurrent/reentrant attempts. Verify the original operation
  and lease return and exception contracts. Core checks include cleanup
  cancellation as a fault, preserving the original exception and token.
- Run the complete locked Release verification on Windows and WSL with .NET
  SDK 11.0.100/runtime 11.0.0, including the actual compiler fixture. Read back
  hosted Windows Server 2025 and Ubuntu 24.04 jobs for the exact Engine commit.
- Run the existing generated Small API verifier first. Build a copy of its
  generated app with a separate probe entry point and verify its original
  source lock and Engine inputs before and after. Run normal, throwing
  publication and throwing measurement observers in separate processes.
  Verify all-off publishes nothing and paired transport owner/denial counts
  are exact. A first-publication failure must preserve owned shutdown and
  allow a second successful application lifetime in the same process.
- Compare the clean predecessor with the clean candidate without a listener
  and with an inline listener under the [component observation protocol](../evidence/dispatch-lifecycle-metrics/2026-11-23/PROTOCOL.md).
  Retain every warm batch, first-use observations and failed preparations.

## Current proof boundary

The protected fixture authenticates real HTTPS requests using ephemeral JWT
and TLS material and uses an in-process store. A single owner request traverses
two Core dispatchers, a tenant denial traverses one, and an anonymous denial
traverses zero. Metric totals describe these invocations across the process.
The observation measures single-threaded component loops with a minimal
listener. Exporters, external providers, contention, supported-host qualification
and the canonical Small API workload keep their own acceptance criteria.

[Engine change](https://github.com/Cephalon-Labs/Cehpalon-Engine/commit/c18757f7ef4df2c78c73e902aa39d05424e6bcff) · [Core contract](https://github.com/Cephalon-Labs/Cehpalon-Engine/blob/main/src/Cehpalon.Engine.Core/README.md) · [Composition contract](https://github.com/Cephalon-Labs/Cehpalon-Engine/blob/main/src/Cehpalon.Engine.Composition/README.md)


## Results on c18757f

The exact locked component suites passed 1,546 checks on Windows and 1,543 on
WSL. Core contributed 35 and Composition 83 on each host. The corresponding
hosted contract jobs passed with the same counts on Windows Server 2025 and
Ubuntu 24.04. The two hosted platform smoke jobs passed 12 checks each and
reported the two real provider checks as Not run.

The original generated Small API passed 155 verification checks and its
39-case HTTPS self-test on both local hosts. The separate metrics entry point
passed 24 wire controls per host. Healthy and throwing measurement observers
each saw 12 records, including 3 activations, 3 disposals, 4 successful Core
invocations and 2 business failures. The throwing publication observer saw
each first publication once and no measurements. After it detached, a second
host on the same process could still serve and shut down. The probe rechecked
all 32 Engine source inputs before and after building and running. The initial
Windows probe alone failed during build because the generated project uses an
explicit compile list. Adding the probe to that list fixed the proof setup.

The component cost comparison completed all six rounds per host and retained
all 18 process reports per host. The table reports the median of paired warm
batch deltas in nanoseconds per dispatch or per one-module cycle.

| Workload | Windows, listener off minus predecessor | WSL, listener off minus predecessor | Windows, enabled minus off | WSL, enabled minus off |
| --- | ---: | ---: | ---: | ---: |
| Core dispatch | +1.73 | +0.87 | +27.53 | +32.84 |
| Activate and dispose one module | +36.66 | +22.35 | +39.82 | +166.43 |

Every recorded warm allocation delta was 0 bytes per call or cycle on the
measurement thread. All four listener-off latency ranges crossed zero.
The Windows enabled lifecycle range also crossed zero. An initial preparation
failed before timing when the SDK globbed assembly metadata from another arm.
The attempt was retained and every arm was rebuilt with an explicit compile
item before the complete measurements. Cold rows include first-use JIT.

The earlier synchronous audit-read counter experiment is filed with this handoff.
It observed +4.34 ns/read on Windows and +3.53 ns/read on WSL on paired
medians, with no additional allocation in measured batches.

[Raw data and protocols](../evidence/dispatch-lifecycle-metrics/2026-11-23) · [Hosted contracts](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/45201013780) · [Hosted platform smoke](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/45201014020)

[Sample probe source](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/tooling-small-api/dispatch-lifecycle-metrics)
