# 2026-11-23 Small API empty-argument startup

User reported Sequence contains no matching element at small-api Program.cs11.
Reproduced original actual binary with empty args before patch; it required
--output via Single. No-args now chooses unique ignored report path, prints it,
runs40 checks and exits. Explicit report supported; invalid/duplicate/existing
destinations return2 before fixtures, help0, CreateNew retains prior output.
Root markers select normal checkout from cwd or binary; copied binaries use cwd.
Source is Samples-only; no Engine or launchSettings/user-file change.

Local actual SDK11.0.100 build0warnings/errors with clean Engine5184517 baseline;
26 launch checks and three40-case runs (120) passed. Raw original failure/build/
attempt01 in isolated Samples .local/small-api-launch, original user hashes in
primary Samples .local/small-api-launch-user-files.json. Public exact-byte
reports in build-restore/evidence/2026-11-23-launch. Source Samples
8bf3f69c2fedf8598333dd4bdc49a5f128d285c3 (technical provenance only).
See [delivery](../planning/small-api-launch.md) for hosted result and tracking.
Keep #3wholeBlocked/#20whole, original benchmark and M0/metadata/nullhours.
An additional local empty-args run from the project directory with the user's
existing Development/ASPNETCORE_URLS environment also passed40; report and log
retained locally, no native GUI claim and no user profile edits.
Hosted run45109256919 passed all steps; downloaded launch26/120 and existing
build62/706 manifests confirm success; solution build also passed. No billing
skip. Body-only11 plan50113ed606cec130e53eee17bbe6ce96cb7330cbbb8ef93774e73452415d607f
dry-run/apply/readback23; other22 task bytes/allmetadata/253Projectvalues unchanged.
All ten original user file hashes unchanged. Samples main8bf3f69, Engine5184517
unchanged; generated CLI profile and other consumers' argument contracts untouched.
