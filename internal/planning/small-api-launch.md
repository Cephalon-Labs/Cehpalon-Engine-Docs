# Small API empty-argument launch recovery

Date: 2026-11-23. Scope: checked-in protected Small API consumer, Engine #11.

## Problem and behavior

Program.cs previously used `args.Single(...)` for `--output=`, so a normal
Visual Studio profile without command-line arguments failed at line11 with
`Sequence contains no matching element`. The original failure was reproduced
with the retained clean-Engine binary before editing.

With no arguments, the consumer now creates a timestamp/GUID report name under
Samples `.local/small-api-runs`, prints the full path, runs its existing forty
checks and exits. It locates the source checkout from the working or binary
directory using the Samples solution/project markers; copied binaries outside
that layout fall back to the working directory. This is path discovery, not
source attestation or authority. Default reports live outside project content
globs in a normal checkout.

Explicit `--output=<new-report.json>` remains supported. Empty, unknown or
duplicate arguments and existing file/directory destinations return exit2 with
an actionable message before fixture construction. `--help`/`-h` return usage.
Final writes still use CreateNew; previous reports are preserved. The executable
remains a finite test fixture, not a persistent serving profile. User-owned
launchSettings.json and other untracked files are untouched.

## Validation

Local SDK11.0.100 / runtime .NET11.0.0, clean Engine baseline
`5184517a92a087abe4e0091d256142b6c35a2b39`: build passed with zero warnings/errors.
Twenty-six launch checks passed. Empty-argument runs from the Samples root and
the project directory each passed40/40 and wrote distinct ignored reports;
explicit-output execution passed40/40, for120 consumer checks total. Five bad
argument/destination cases returned2 without fixture completion, help returned0,
and earlier/sentinel report bytes were unchanged. No additional native F5 GUI
session was used; tests execute the actual binary with empty arguments.

A separate local run also inherited the existing user profile's Development and
ASPNETCORE_URLS values, used the project working directory and empty arguments,
and passed40/40 with a new automatic report. This is an additional environment
check, separate from the 26-check/120-case verifier and from native GUI proof.

[Samples source/evidence](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/commit/8bf3f69c2fedf8598333dd4bdc49a5f128d285c3)
is technical provenance only. [Public results](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/blob/main/build-restore/evidence/2026-11-23-launch/summary.json)
and three consumer reports preserve raw bytes under the existing evidence
attribute. Raw original failure, build and subprocess logs remain local.
Hosted [run45109256919](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/actions/runs/45109256919)
passed all steps. Downloaded artifacts confirm launch26 and consumer120 passed;
the existing Build/restore62 matrix, consumer706 and full validation solution
build also passed. The existing Build/restore matrix is unchanged; its workflow
also invokes the new launch checks. No usage/billing skip occurred.

## Constraints

Engine source, tenant/identity/module semantics and the original benchmark are
unchanged. #3 stays Blocked, #20 and all Project metadata/gates/hours remain
unchanged. No provider, supported-host, performance, serving or production
qualification is inferred. Ten existing user files are preserved by hashes.

Reviewed body-only #11 sync used plan
`50113ed606cec130e53eee17bbe6ce96cb7330cbbb8ef93774e73452415d607f`, dry run,
exact-hash apply and full readback. All23 mirrors match; other22 mirror bytes,
all issue metadata and all253 Project values are unchanged. Engine main remains
at the baseline; no new Engine commit journal entry was added.
