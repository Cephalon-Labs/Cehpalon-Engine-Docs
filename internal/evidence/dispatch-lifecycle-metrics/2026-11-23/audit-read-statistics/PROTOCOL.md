# Audit lookup statistics overhead observation

Declared 2026-11-23 for Engine issue #18 at Engine commit
`f77c42b187483086e99a5ec5ade6bcd80b9ad738`. Build once per OS in Release
with SDK 11.0.100, pinned dependencies, and isolated outputs. Use runtime
11.0.0 with tiered compilation disabled in the process environment. Run the
Windows and WSL Ubuntu observations serially, once per OS.

The same five-argument `ActivateWithReadTimeout` factory activates two
exact receipt lookup readers. Both use the same deterministic synchronous
in-memory source, matching checked tenant context from a real Engine tenant
dispatch, metadata-only policy, receipt lookup, null timeout, and caller
token. The only intended variable is a null statistics argument versus one
caller-owned collector. The empty successful lookup excludes policy
projection and reflects one positive reader outcome on one thread. Fixed
fixture UTC removes UTC wall-clock drift. The scope still uses its ordinary
monotonic timestamp limit. No external provider or endpoint is opened.

Each process warms both modes in four 100,000-read blocks ordered off,
on, on, off. Then it alternates the order of 12 pairs with 250,000 reads
per mode per pair. Odd pairs run off then on. Every read verifies immediate
successful completion and a null result. Each block checks exact total
provider calls, success counts and zero other outcomes. The process records
each measured block as one JSON line with raw Stopwatch ticks, clock
frequency, thread-allocated bytes and validated cumulative counts. The
per-read figures include the synchronous fixture and correctness checks.
Startup, authority setup, counter sampling and JSON output are outside the
clock. A conformance run checks all four warmup positions with four reads
per block and has no measurement samples. Retain raw output and any
incomplete or failed attempt.

For each OS, convert ticks to nanoseconds and divide by batch size.
Calculate medians and full ranges per mode and for all paired on-minus-off
deltas, including paired delta ranges split by order. Report allocation
bytes per read and any spread. Treat the results as descriptive paired
batch observations on the available hosts, with no outlier exclusions and
no performance acceptance threshold. This does not measure request
percentiles, asynchronous provider paths, network/database behavior,
counter contention, exporters or CPU placement. Original qualification
gates remain in force.
