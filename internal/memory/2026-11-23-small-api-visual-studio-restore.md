# 2026-11-23 Small API Visual Studio restore recovery

User requested one-click Visual Studio Build after externally removing `small-api/obj`.
This is local build troubleshooting, not a new runtime feature or benchmark result.

Observed reproduction: Visual Studio 2026 Enterprise 18.11.4, solution open,
remove the consumer's entire obj directory, Build SmallApi.Consumer: NETSDK1004.
Global NuGet consent and automatic restore were already true. The original local
consumer solution contained only the consumer; referenced Engine projects also
need to belong to the solution for Visual Studio to build them.

Samples changes: explicit repository NuGet automatic-restore settings;
small-api/Directory.Build.targets recovers missing assets with external locked
restore before PrepareForBuild, only for real Visual Studio builds; local
SmallApi.Consumer.slnx includes all seven referenced Engine projects; README
documents solution builds and the executable's required fresh output argument.
The target is scoped to this sample/dependency set, not a general replacement for
the SDK's separate restore/build evaluation or arbitrary custom output layouts.

Validation used SDK 11.0.100, runtime .NET 11.0.0 and clean Engine checkout
5184517a92a087abe4e0091d256142b6c35a2b39. A validation solution substituted only
Engine paths to the clean checkout and the consumer's absolute path. Never
compiled primary Engine's four preserved user modifications. Native Visual Studio
right-click Build after removing obj: 1 succeeded, 0 failed, 7 up-to-date.
Native repeated Build: 0 failed, 8 up-to-date. Actual native-built consumer:
40/40 protected HTTPS/tenant/disabled-module conformance checks.
Direct MSBuild cold recovery passed; design-time, non-VS and existing-assets
guards passed, with existing assets bytes/write time unchanged.

Retained local evidence: Samples .local/vs-restore-770ce90bdd7042829cfd1bbcca30ecfd.
Initial guard attempt forwarded a project-specific extensions path globally and
failed; removed that forwarding before final proof. A native two-instance attempt
hit a Web SDK cache file lock; stopped only the owned original instance and
repeated with one instance. Both failures and moved obj trees remain locally.
Owned validation instances stopped; final restore points assets to primary
Engine without compiling it. Package lock and four primary user file hashes
unchanged. No remote publication or tracking edits in this local repair.
#3 remains Blocked and #20/original benchmark criteria are unchanged; no benchmark
was run and no maturity or supported-platform qualification is inferred.

## Authorized follow-up delivery

The user subsequently authorized checking other locations and committing/pushing
Build/restore fixes to main, synchronizing GitHub/Docs and preserving user edits.
The [delivery report](../planning/build-restore.md) supersedes the single-sample
implementation: one root target selects six consumers; the leaf target was moved
into ignored audit storage. A sixteen-project solution includes the complete
reference closure. Actual VS MSBuild final02 passes 62 checks and consumer suites
5/10/40/651, plus the full validation solution build. Attempt01 passes 61 and is
retained separately. Generated CLI consumers and Engine source remain unchanged.
Public exact-byte consumer reports are in Samples build-restore/evidence/2026-11-23.
The initial native GUI proof above is historical and was not rerun for every
consumer. Broader checks use VS MSBuild with BuildingInsideVisualStudio=true.

Final Samples main: dd678011b4f27ad01a03708197df75fe842a103d; original source/evidence
commit a3500fcbced95178e1da2fc971e4cc6643b1146d (technical provenance only).
Hosted run45075115636 failed checkout on long evidence paths before tests.
Runner-only Git core.longpaths correction enabled run45075418379: all steps pass,
downloaded report62 plus706/0 consumer checks and full solution build confirmed.
No billing skip. Engine main remains 5184517a92a087abe4e0091d256142b6c35a2b39.
Body-only11/22 plan ad51495f66711be3ec9d698253624a2956e3186d71ac3745680c08e97ba2eb67
dry-run/applied/readback23; all253Project values/allissue metadata and other21
mirrors unchanged. #3wholeBlocked/#20whole/original gates unchanged. Ten user-file
hashes preserved; Samples user untracked .github/Properties remain unstaged.
Authored pre-merge stashes, raw moved obj trees and isolated worktree are retained.
