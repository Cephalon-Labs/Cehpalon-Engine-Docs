# Portable CLI/scaffold correctness protocol

Declared 2026-10-29 before this slice's validation. Scope: ADR0012 and existing #20 only. #3 remains Blocked, full task gates and dependencies remain unchanged, maturity M0.

Use the existing pinned SDK `11.0.100-rc.3.26522.148`, official isolated NuGet source and locked Engine dependencies. Record exact Engine commit plus observed source hashes; retain uncommitted integration attempts distinctly from final clean committed proof. Run Windows then Linux sequentially on this shared machine; these are portable local observations, not listed-supported Windows or hosted CI qualification.

Required correctness matrix:

- CLI argument/command/profile/name failures must return a nonzero documented code with structured diagnostics, without emitting secret input or creating a target.
- Existing files and empty/nonempty directories must survive unchanged. Reject observed symlink/reparse ancestors, invalid names and known Engine/Docs/Samples checkout content destinations. Inject partial-write and publication-collision failures; preserve outsider content and clean up only owned staging. State race limits explicitly.
- Same source/name/profile must produce identical fixed file bytes across two output directories. No generated timestamp, output-directory identity or random staging identifier may leak into published files.
- Launch the actual CLI executable into a fresh Samples ignored directory containing spaces and Unicode. Generate a new consumer, restore/build it in Release with the pinned SDK and warnings as errors, retaining commands, logs, emitted registry and runtime dependency list. Inspect actual generated operation registration and reject compiler/analyzer dependencies at runtime.
- Execute app-on/optional-off: the generated handler must dispatch successfully, activated module factories must match the immutable plan and all owned resources/handlers must dispose. All-off: zero factories/handler construction/dispatch. Invalid config: reject before activation. `validate` uses Composition without activation and fails unsupported selections.
- Valid names that overlap framework/compiler/Engine names (`Program`, `Console`, `Path`, `JsonSerializer`, `File`, `System`, `OperationContext`, `ModuleRole`) must generate consumers that compile and dispatch. A fixed consumer namespace independent of the requested assembly name prevents namespace shadowing; retain original compiler repros and verify the complete set after correction.
- Run existing Core/Composition/generator/identity/tenant/HTTP/GraphQL component contracts to detect integration regressions. Runtime algorithms and original transport/cancellation/performance protocols are unchanged.

Every required check must pass. Any failed attempt stays retained; changes justify a complete bounded matrix rerun, never favorable case replacement. No wall-clock speed threshold, statistical comparison, startup or throughput claim is made here. Full #20 timing benchmark remains Planned. Keep original gates, person-hour estimates, dependencies and #3 body/editable metadata unchanged unless a separately reviewed tracking plan explicitly states otherwise.
