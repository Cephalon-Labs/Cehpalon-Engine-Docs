# 2026-11-23 Visual Studio profiles for web sample self-tests

The user's Small API screenshot showed exit code 0 and an IDE connection
dialog. Its local `Project` launch profile enabled browser launch at fixed
HTTP and HTTPS URLs. Small API instead opens fixtures on ephemeral loopback
ports, writes its conformance report, and exits. The Security API local profile
had the same mismatch.

Samples now tracks `SmallApi.Consumer` and `SecurityApi.Consumer` launch
profiles with browser launch disabled. Neither profile supplies a static URL
or command-line arguments. The original local profile bytes were saved under
Samples `.local/f5-debug-profiles-before` before replacement. The other eight
pre-existing user files retained their original bytes.

The original running Visual Studio solution accepted F5 with the corrected
Small API profile, produced a fresh 40/40 report, and returned to Ready
without the connection dialog. This checks the IDE behavior in the user's
checkout. The isolated verifier also ran both named profiles with empty
arguments and checked the profile shape, exit code and report. All 71 verifier
checks passed, including Small API 40/40 and Security API 651/651. The Security
API profile was exercised through the CLI.

The change is confined to Samples launch and verification configuration.
GitHub and Docs received one append-only update to #11. Readback matched all
23 mirrors and preserved Project metadata. Issue #3 remains Blocked and the
original benchmark criteria still apply.

[Samples commit](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/commit/a1ef28f6af7dbeeee802c121f2f901a6e54d35d8)
[Samples CI](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/actions/runs/45118050111)
