# .NET 11 GA Core and Composition guardrails

The W1 benchmark ran on clean Engine
`6fe7254404cf6b148370bd95befe8331e8932354` with SDK 11.0.100/runtime 11.0.0,
locked Release packages and WSL Ubuntu 22.04.5 x64. The original
[W1 protocol](w1-component-protocol.md) ran once in the fixed order with no
benchmark flag overrides. Source, executable dependencies and protocol
hashes were checked before and after execution.

The independent replay verified all 20 repetition rows, both counts of
1,000,000 constructed and disposed handlers, and 8/8 unchanged guards.

| Guardrail workload | Observed median | Allocation |
| --- | ---: | ---: |
| Core dispatch minus direct handler per operation | +119.00 ns | +0 B |
| Small composition compile | 18.83 µs | 9,096.24 B |
| 128-node composition compile | 1.361 ms | 931,728.8 B |

This evidence measures the component loops on shared WSL resources. The
existing #3 compatibility closure supplied the supported Windows provider
proof for the #5/#6 dependency gates. Configuration recorders cover invalid
plans, disabled factories and cleanup at the component boundary. #9 and #11
carry the separate transport and W0 resource/reference workload criteria.

[Raw and independent replay](../evidence/w1-ga-closure/2026-11-23) · [Exact revision contract CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/45207552894) · [Platform proof](windows-native-platform.md)
