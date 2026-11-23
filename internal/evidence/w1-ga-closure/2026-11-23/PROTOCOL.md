# Final W1 component guardrail evidence

This repetition covers the existing [W1 component protocol](w1-component-protocol.md) for #5 and #6 from clean Engine revision 6fe7254404cf6b148370bd95befe8331e8932354. The copied protocol equals the original predeclared SHA-256. The only historical change to the original benchmark entry point adds an opt-in dispatch budget branch. This run omits that flag. Runtime is private .NET 11 GA, SDK 11.0.100, workload settings from the protocol, no enabled metric listener, and the listed shared WSL Ubuntu environment.

One complete timed run follows locked Release build after the previous slot is released. The original GC, CPU affinity and threshold policy applies. The runner saves exact source and binary hashes, OS/runtime/SDK and affinity, logical/physical CPU, memory, and raw results. The Python verifier independently replays all 20 measured rows and the eight guardrail outcomes.

    wsl -d Ubuntu -- bash /mnt/d/Cephalon/Cehpalon-Engine/.local/continuation-delivery-20261123/w1-ga/run.sh

Any preparation failure or benchmark failure is retained. The benchmark addresses the bounded Core dispatch and Composition compile contracts, with no generator speed, cold startup, dedicated-reference W0, transport, provider, or production inference.

