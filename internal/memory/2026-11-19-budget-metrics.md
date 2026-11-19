# Opt-in operation budget metrics handoff

The continuation delivers budget CreateMetrics APIs in `f6293afccc5fc84799b70efa094a6fd94057a62a` and host-selected meter names in `b87c75856313f3c90a38a20a0c59a2ca088a7e96`. Caller-owned Meter instances expose aggregate observable integer gauges with empty Engine measurement tags. The caller chooses when to collect and disposes the meter. Gauge callbacks sample independently during concurrent activity. GetSnapshot remains the coherent aggregate API.

Final component checks passed 521 Windows and 518 WSL. Actual generated Small API verification passed 159 each. Listener lifecycle tests covered held cleanup, closure, drain, custom names, meter disposal and successful business dispatch after collector callback failure. Periodic collection retained 80 collections and 640 callbacks per host, including the first 24-byte collection and all actual cadence measurements. Earlier default-only preparation passed before custom naming was added. See the [report](../planning/budget-metrics.md) and [protocol](../validation/budget-metrics.md).

#18 and #20 remain In Progress. Keep #3 Blocked for outstanding qualification and the original benchmark criteria. If GitHub usage or billing blocks a step, record that exact step and proceed with local work. Preserve primary-checkout telemetry changes and untracked Samples paths.
