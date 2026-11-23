# F5 and empty-argument entrypoints

Date: 2026-11-23. Scope: Engine #11/#20, source-only consumer/developer experience.

## Layer decision

Argument interpretation belongs to executable entrypoints. Core/Composition and
business/tenant contracts must not choose report paths, IDE behavior, credential
files or provider defaults. They are unchanged. Engine Tooling does own generated
entrypoints, so it required a bounded fix: empty CLI arguments now show help with
exit 0/no publication; generated Small API empty arguments select its existing
finite fixture self-test, with a new report under the binary's .local directory.
Explicit serving still requires caller-provided trust. Generated portable's
default config path already worked and is unchanged.

## Checked-in projects

| Startup project | Empty-argument behavior |
| --- | --- |
| Portable Core | Existing five fixture checks; fresh ignored report |
| Tenant/Identity | Existing ten checks; fresh ignored report |
| Small API | Existing forty HTTPS/tenant/disabled-module checks; fresh report |
| Security API | Existing 651 local fixture checks; fresh report |
| Audit/Outbox | Setup guide only; no connection read/open or PostgreSQL pass |
| Public benchmark | One finite HTTP correctness smoke; no benchmark execution |

The four report consumers share a Samples-only linked source helper. It rejects
empty/duplicate/unknown output options and existing destinations before fixtures,
supports help, and retains CreateNew publication. Reports use timestamp/GUID names
outside project content globs in a normal checkout. No user launch profile was
modified. Existing nonempty benchmark modes and all acceptance criteria remain.

Seven separate diagnostic entrypoints were also reviewed. Conformance, syscall
wait, TPL, TraceAnalysis and metrics RuntimeTrace show usage without a controller.
The two Linux-only actors reject Windows with an explicit message/exit 2. The GC
actor's new Windows guard precedes its large GC workload/libc protocol; ThreadPool's
existing platform guard is retained. Valid controlled protocols are unchanged,
and no trace collection, runtime resume, syscall fixture or scheduler hook was
started by these Windows checks. Historical diagnostic evidence is not promoted.

## Local validation

SDK 11.0.100 with exact clean Engine
`ff66a46220740ab7ccf1002dce15d2af5b8ee668`:

- Engine Tooling contracts: 156 passed, 0 failed; source changes are only Tooling,
  its embedded Small API template, documentation and the related test.
- Build/restore: 62 checks and existing consumer suites 5/10/40/651 passed.
- Six consumer startup checks: 69 passed. All four default runs executed their
  complete suites. Audit results are setup guidance only; benchmark results are
  finite correctness smokes, including explicit baseline HTTP/GraphQL variants.
- The prior Small API launch regression: 26 checks /120 conformance cases passed.
- Actual generated portable consumer: 70 verifier checks passed.
- Actual generated Small API: 155 verifier checks passed; both explicit and
  empty-argument self-tests passed 39/39. Exact fourteen emitted files, locked
  package graph, lazy typed registrations, disabled factories and cross-tenant
  checks remain covered. Compiler/CLI dependencies stayed out of runtime graphs.
- Diagnostic02: all 7 builds/guidance/platform-rejection checks passed. Diagnostic01
  retained an early-return signature compilation error in RuntimeTrace after four
  helpers; the return was corrected to preserve its existing void/Task entrypoint.
  Both source and failed logs remain local. No capture was attempted.

Current tooling consumer locks still referred to an old RC SDK. They now pin the
tested GA SDK and this clean Engine commit for developer proofs. Historical
benchmark inputs, locks, captures and raw outcomes remain archived unchanged;
this does not reclassify old observations or constitute a new timed benchmark.
Source inventories now include the shared build target/helper wherever compiled.

Validation built and launched the actual executables with empty arguments; it did
not automate a native Visual Studio F5 session. Select an executable sample as
the startup project; library projects are not startup applications.

## Delivery

Engine [ff66a46](https://github.com/Cephalon-Labs/Cehpalon-Engine/commit/ff66a46220740ab7ccf1002dce15d2af5b8ee668),
Samples [75d2e9e](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/commit/75d2e9e88ff63c1462ff8b8e2330a4d9f76528df)
(Samples SHA is technical provenance, not an Engine journal entry).
[Public exact-byte reports and summary](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/build-restore/evidence/2026-11-23-all-startup)
retain executed suites and failed diagnostic boundary. Private raw attempts,
generated projects and worktrees remain local. Hosted CI and tracking readback
are recorded below after completion.

Engine hosted workflows [portable contracts](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/45113226082)
and [platform probes](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/45113226215)
passed at this exact commit. Their names/results do not clear #3 or full #20
qualification. Samples [run 45113299235](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/actions/runs/45113299235)
passed the broader entrypoint/SDK-consumer matrix. Downloaded artifacts confirm
build 62, consumer startup 69, Small API 26, diagnostic 7, generated portable 70 and
generated Small API 155. The generated explicit/default reports both pass 39/39.
All workflow steps and upload passed. No usage/billing step was skipped.

The #20 native body was already 65386 characters before this delivery. Its exact
two older diagnostic summary sections were moved to [the raw archive](../evidence/task20-startup-archive/2026-11-10-15-prior-summaries.md)
with a checksum manifest solely to stay within GitHub's body limit while adding
the Engine journal. All original benchmark/metadata text before that boundary
remains exact bytes; no historical numbers or limits were rewritten.

Reviewed plan `622482c3c1e31c3195630cf06633359fe370094b6ed04aaed149321d9b22dfa7`
applied exactly two body-only updates, #11/#20, after dry run. Full live readback
matched 23 mirrors. All 253 Project values, all issue metadata and the other 21
mirror bytes were unchanged. The new full Engine SHA is linked in both task
journal continuations. The old #20 prefix and archived suffix were independently
compared as bytes; #3's entire mirror stayed identical. Ten user file hashes matched.

Ten existing user file hashes are preserved. #3 remains wholly Blocked. #20 keeps
its status/priority/dependencies/M0/test/benchmark gates and null actual hours;
only its authorized startup continuation/Engine journal is updated. No provider,
supported-host, original performance or production qualification is inferred.
