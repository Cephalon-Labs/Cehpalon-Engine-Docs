# Dispatch completion observation cost

Run after functional proof for the exact clean Engine revision named in the
pre-measurement manifest. This is a descriptive #18 component observation.
The process uses x64 .NET 11.0.0 with tiered compilation disabled. Use
.NET SDK 11.0.100 to build locked Release separately on Windows and WSL
Ubuntu. Run Windows then WSL serially on the same workstation. Keep every
completed or invalid attempt and record any preparation correction.

In each process, use two dispatchers sharing one registry, operation,
context and factory. Disabled uses the original constructor. Enabled
registers a synchronous completion callback that validates the outcome,
elapsed duration, IDs and cleanup count. Every operation constructs and
disposes a simple synchronous handler, checks the immediate result and
increments the same factory and disposal counts. A callback increments
one additional receipt count. There is no metric listener, structured log
sink, network or provider. Run first without an ambient Activity, then
with a single active native W3C Activity for the whole block series.
Activity creation, result serialization and validation outside the loop
are outside the clock. The observed loop includes synchronous handler
creation and cleanup, result checking and enabled callback validation.

For each ambient state, warm up in off/on/on/off order at 50,000 dispatches
per arm. Run 12 matched pairs at 200,000 dispatches per arm. Odd pairs
start with off, even pairs with on. The separate conformance invocation
uses four warmup and eight trial dispatches per arm and two pairs. Assert
one complete factory and disposal per dispatch, exact callback count,
correct nullable native IDs, success outcome, nonnegative callback
duration and unchanged ambient Activity. An incorrect block invalidates
the attempt. Record Stopwatch ticks, frequency, current-thread allocated
bytes, and counts. Capture protocol, source, build, runtime manifests and
successful conformance receipt hashes before collecting timed results.

Report per-state medians and full ranges of per-arm ns/dispatch and
bytes/dispatch and matched on-minus-off deltas. Retain all pairs and
report timing deltas split by ordering. Treat both ambient states as
separate sequences. No numerical acceptance threshold applies to this
component observation. The results include the sample callback work,
exclude logging/export, and provide no network latency, shutdown,
production cost, scale or broader qualification claim.
