# Retained agent attempts

These are historical observations from the isolated agent worktree, not the
integrated Engine acceptance result.

- `restore-attempt01.txt` / `build-attempt01.txt`: initial restore inherited two
  machine package sources and produced NU1507; the analyzer also reported RS2008
  because diagnostic release tracking was absent. Scoped NuGet.Config now clears
  to official nuget.org; unshipped diagnostic release files now enable tracking.
- `build-attempt02.txt`: the new test harness had CS1525 from a missing space
  between C# null-forgiving `!` and equality `==`. Corrected the test expression;
  this was not a generator/Engine runtime failure. Final driver build has zero
  warnings/errors and all38 tests pass.
- First package-inventory collector attempt raised
  `ValueError: Cache/lock content hash mismatch: microsoft.codeanalysis.analyzers`.
  The collector incorrectly compared `.nupkg.sha512` (raw signed archive hash)
  with NuGet lock contentHash. Corrected collector checks actual raw archive
  against `.nupkg.sha512`, and separately compares `.nupkg.metadata.contentHash`
  with every lock graph. All13 package records now pass those distinct checks.
  This correction does not replace either hash or alter any package bytes.
- Initial compiler fixture emitted generator output under its source directory
  because `IntermediateOutputPath` was not initialized at that evaluation point.
  Moved the retained generated output to ignored `.local/codegen/generated-attempt01`
  and changed the output property to `$(BaseIntermediateOutputPath)generated`,
  inside excluded `obj/`. A subsequent actual SDK build/run passes; no generated
  `.cs` remains in the fixture's source glob.
- The first advisory CLI query implicitly restored using the machine cache;
  final locked restore explicitly uses the private cache and the retained final
  advisory query uses `--no-restore`. No global runtime/settings were changed.

Final data files are `win-driver.json`, `win-compiler-consumer.json`,
`package-inventory.json`, `package-advisory.json` and `provenance.json`.
Their scope does not include listed-supported Windows, hosted CI, real transports,
tenant/security conformance, benchmarks, AOT or production qualification.
