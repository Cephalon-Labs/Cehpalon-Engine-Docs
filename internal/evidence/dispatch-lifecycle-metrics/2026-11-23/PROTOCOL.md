# Dispatch and module lifecycle histogram overhead observation

Declared before measurement under #18. Compare Engine f77c42b with the exact
clean histogram candidate on each host using the same Release console harness,
pinned .NET SDK 11.0.100/runtime 11.0.0, tiered compilation disabled and no
debugger. Phase order per host is each of the six lexicographic permutations
of (base, off, on), with one owned process at a time. Base is the published
Engine without the histograms. Both candidate arms use identical binaries,
with no started observer in off and one bounded MeterListener in on. Validate
synchronous activity, results, tags and counts. Never rerun unchanged source
to prefer a result. Report stopped/failing runs and retain all outputs.

Each process records one first-use call per workload and then warms up 100,000
dispatches and 10,000 module activation/disposal cycles. Measure one batch of
500,000 successful dispatches and one batch of 50,000 one-module
activation/disposal cycles using Stopwatch and current-thread allocation
bytes. The cold rows include first-use JIT and are kept as raw observations.
Report median and full range of round-paired warm deltas for candidate
disabled minus baseline, and listener enabled minus candidate disabled.
No outlier exclusions, acceptance criteria changes, or inference to a real
exporter, HTTPS, tenant/provider latency or original W0 / #20 qualification.
No concurrent owned builds or fixture setup during timing.

