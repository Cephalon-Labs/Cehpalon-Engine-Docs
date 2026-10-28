# Small API collector connection readiness continuation

2026-10-28. Status: protocol frozen; implementation and validation in progress, no new measurement result yet. Existing #9/#11 remain Blocked/M0 and #3 remains Blocked.

[ADR0011](../adr/ADR-0011-small-api-collector-connection-readiness.md) freezes the connection barrier, failure telemetry, 12-probe diagnostic matrix and complete fresh canonical rerun before timing. [Canonical03](w2-small-api-tuning.md) remains immutable historical evidence, including its 37 dropped offers in the HTTP Engine 2000/s preflight. This work cannot retroactively complete that missing timed interval or establish a single root cause.

Current verified Engine remains `6804271d429106864e01e4ec546a41dff771f84b`; Samples before this wave is `bad8e36c04418bd5b71da2367a52a673b40da213`. Exact compiled source/build inputs and staged artifact hashes will be retained before canonical timing. SDK/runtime and package locks remain unchanged. Shared WSL is observational: affinity does not provide reserved CPUs or the required memory/reference isolation.

The bounded implementation scope is collector connection preparation, structured managed-failure evidence and phase TLS/client snapshots. No portable Engine, business handler, identity authority, host startup boundary, codec, request schedule or numerical budget change is planned. Delegated work uses separate worktrees; the primary agent integrates and is the sole remote writer. All failed trials and raw artifacts remain retained.

Final delivery will record clean Windows/Linux conformance, all diagnostic probes, the complete canonical attempt or its actual stopping reason, independent raw/source audits, and an exact reviewed update/readback of existing GitHub #9/#11. Verify #3 body/editable fields unchanged. Unknown actual person-hours stay null; no release, billing or supported-platform qualification is inferred.
