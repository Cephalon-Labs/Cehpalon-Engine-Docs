# Checked-in Samples Visual Studio Build/restore

Date: 2026-11-23. Tracking: Engine #11 and #22. Overall M0 and all existing
Project fields, dependencies, hours and benchmark gates remain unchanged.

## Problem and scope

Visual Studio 2026 Enterprise 18.11.4 reproduced NETSDK1004 when the Small API
solution remained open and its entire `obj` directory was removed externally.
Global NuGet restore settings were already enabled. The observed failure is
consistent with stale restore state, without claiming an internal NuGet trace.
The local one-project solution also omitted Engine dependencies needed for a
fresh Visual Studio build. The initial reproduction and single-consumer repair
are retained in [the local repair handoff](../memory/2026-11-23-small-api-visual-studio-restore.md).

The follow-up reviews the thirteen checked-in Samples project entrypoints outside
archived evidence: six Engine consumers and seven separate diagnostic helpers.
The six existing consumer verification scripts already restore before their
`--no-restore` builds and reuse matching artifact/EngineRoot properties. They
retain that explicit sequencing. Engine source and CLI-generated consumers are
unchanged; generated consumers retain their documented `dotnet build` workflow.

## Changes

- Repository NuGet configuration explicitly enables automatic restore.
- `Cehpalon.Samples.slnx` includes the exact reference closure: six consumers and
  ten Engine projects. The Small API solution includes its seven Engine references.
- One Samples-root `Directory.Build.targets` replaces the initial leaf fallback.
  It selects only the six known consumers, runs external locked restore before
  PrepareForBuild if assets are missing, and preserves the selected EngineRoot
  through the child environment. It never forwards a consumer-specific obj path
  as a global property to every referenced project.
- Design-time/IntelliSense, non-VS builds, existing assets and explicit
  `CehpalonRestoreMissingAssets=false` skip recovery. Diagnostic helpers stay
  excluded even with a caller-supplied EngineRoot. Custom intermediate-output
  layouts require explicit restore with matching output properties. This
  fallback is bounded to the tested current consumer/package graphs, not a
  general SDK restore/build reevaluation substitute.
- The new verifier retains moved obj trees, logs, source hashes and every attempt.
  A Windows Actions workflow runs the same real VS MSBuild and consumer checks
  against the pinned clean Engine baseline. Its result is recorded separately.

## Validation and evidence

Final local validation passed 62 checks on SDK 11.0.100 / .NET 11.0.0 using the
clean Engine baseline `5184517a92a087abe4e0091d256142b6c35a2b39`. All six
consumers compiled after moving the entire obj directory, and all warm,
design-time, non-VS and opt-out checks passed. The six explicit CLI
`--no-restore` negative cases returned NETSDK1004 as expected. Normal CLI implicit
restore also passed. The sixteen-project validation solution restored/built with
actual VS MSBuild and warnings treated as errors. The broader build check uses
BuildingInsideVisualStudio=true; it is not additional GUI-click coverage.

| Executed consumer suite | Passed | Failed |
| --- | ---: | ---: |
| Portable Core | 5 | 0 |
| Tenant/Identity | 10 | 0 |
| Protected Small API | 40 | 0 |
| Security API | 651 | 0 |
| Total | 706 | 0 |

Attempt01 passed 61 checks and the same four suites. Attempt02 adds a bounded
consumer selector and explicitly proves trace-tool exclusion; it is the final
source, not a favorable unchanged-source repeat. Both full attempts remain in
the isolated Samples worktree. Native MSBuild/provider/consumer checks run
sequentially. No original benchmark was run or reclassified.

Samples delivery: [a3500fc](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/commit/a3500fcbced95178e1da2fc971e4cc6643b1146d)
(technical provenance only, not an Engine commit journal entry).
[Public summary](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/blob/main/build-restore/evidence/2026-11-23/summary.json)
contains both attempt outcomes, observed source hashes and the solution build
log hash. Four consumer reports retain exact output bytes via the evidence
`-text` Git attribute. Source/project file EOL policy stays unchanged; observed
working-file hashes are not claims of Git blob identity across normalization.

Initial hosted workflow [45075115636](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/actions/runs/45075115636)
failed at Samples checkout because retained evidence paths exceeded Git for
Windows' default path limit. No SDK/test step ran; this was not a billing block.
Workflow-only correction [dd67801](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/commit/dd678011b4f27ad01a03708197df75fe842a103d)
sets `core.longpaths=true` only in the disposable hosted runner before checkout.
It changes no user-machine or runtime/benchmark configuration. Corrected hosted
run [45075418379](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/actions/runs/45075418379)
passed: 62 verifier checks, the same four consumer suites (706 passed / 0 failed),
the sixteen-project solution build, and retained report upload. The downloaded
manifest confirms the pinned SDK and clean Engine baseline. No unchanged failed
workflow was rerun or hidden, and no usage/billing skip occurred.

Initial native GUI coverage remains separate: after removing Small API obj,
right-click Build succeeded; repeated Build reported eight up-to-date projects,
and the resulting consumer passed 40/40 checks. This earlier GUI proof used a
validation solution whose Engine paths pointed to the clean Engine checkout.

## Limits and preservation

Build coverage for PostgreSQL audit/outbox and public benchmark consumers does
not execute a PostgreSQL provider or performance protocol. Existing provider,
IdP, deployment and supported-host qualification are not promoted. #3's whole
Blocked row and #20's whole row remain byte-for-byte unchanged. No measured
person-hours, package release or NuGet publication is inferred.

All four primary Engine user modifications and six existing untracked Samples
files are held outside these commits and checked against their original hashes.
Evidence uses a separate Samples worktree and clean Engine baseline; no primary
dirty Engine compilation is used as validation. Raw attempts and worktrees are
retained. Public evidence contains bounded reports/source hashes, not obj/binary
trees or private fixture material.

## GitHub/Docs synchronization

Reviewed plan `ad51495f66711be3ec9d698253624a2956e3186d71ac3745680c08e97ba2eb67`
contained exactly two body-only issue updates: #11 and #22. Dry run, exact-hash
apply and live `pull --check` completed. All 23 mirrors matched; the other 21
mirror files, all issue metadata headers and all 253 Project values were preserved.
The whole #3 and #20 mirrors and all ten pre-existing user file hashes matched
their pre-work snapshots. No Engine commit was created or added to a journal.
Samples main contains the source/evidence delivery and runner-only correction;
Docs main contains this report, handoff, task bodies and readback snapshot.
