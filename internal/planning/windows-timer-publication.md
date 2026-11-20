# Windows timer and completion publication probes

The new controlled probes separate the managed callback-entry leg from completion publication to observed resumption. All four alternating untraced/traced pairs complete 4,096 trials. The timer leg remains about 15.4–15.5 ms, while the asynchronous publication leg is bounded in microseconds in these probes. No recorded GC suspension overlaps analyzed traced legs. Native timer eligibility, pre-callback dispatch and OS scheduler time are still not separated, and no historical drop cause is reconstructed.

Engine product/HTTPS benchmark source and continuation policy are unchanged at `5f8f252e901e85c50d7fc6f4b760e457965ce3bb`; SDK stays `11.0.100-rc.3.26522.148`. These are synthetic, shared-host diagnostics, not a Windows benchmark rerun, production policy comparison or acceptance. [Frozen protocol](../validation/windows-timer-publication.md).

## Exact trial boundaries

Each fresh process runs 128 trials in four fixed profiles: direct Task.Delay(1), one-shot System.Threading.Timer(1 ms) with asynchronous completion, timer with inline-eligible completion and accepted QueueUserWorkItem with asynchronous completion. Await registration completes while its task is still incomplete, before timer arm/queue. Trial state is separate, callback-body completion is latched, and timer callbacks are joined with DisposeAsync. No GC forcing occurs in probe profiles; a separate positive fixture covers known GC/TPL/markers.

Raw points bracket optional EventPipe marker emission with QPC and native/managed TID. Each accepted completion is bracketed before/after TrySetResult. For publication to the observed resume marker, the conservative lower endpoint uses the publisher's after-point end and resume point begin, clamped to zero when they race; the upper endpoint uses before-publication point begin and resume point end. These are observation bounds, not confidence intervals or exact first-instruction timestamps. The guaranteed post-publication window is retained separately. Callback entry is a managed-code observation after some unobserved entry work, not a native timer-ready timestamp.

Callbacks may start before arm/queue return. An asynchronously scheduled continuation may run on another worker before the publisher records its after-point. Neither is an invalid clock or a negative queue time. Inline classification additionally requires the callback's native TID and a resume bracket contained inside the publication bracket. Same TID alone does not establish inline execution. RunContinuationsAsynchronously is used only in the declared synthetic profiles; no Engine setting is changed. [Task creation contract](https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.taskcreationoptions).

## All comparison results

Every profile has 512 untraced and 512 traced trials. The next table reports the range of the four per-arm medians of lower endpoints and upper endpoints separately, in milliseconds. All means, medians, minima, maxima and nearest-rank p95 endpoints remain in the full analysis; no first call or outlier is removed.

| Profile / interval | Observation | Median lower endpoints range ms | Median upper endpoints range ms | Maximum upper endpoint ms |
| --- | --- | ---: | ---: | ---: |
| Task.Delay(1): request to resume | Untraced | 15.527600–15.540500 | 15.527600–15.540650 | 16.588400 |
| Task.Delay(1): request to resume | Traced | 15.512400–15.538150 | 15.523200–15.548850 | 18.556600 |
| Timer / async: arm/queue to callback | Untraced | 15.502100–15.525750 | 15.505550–15.530550 | 16.588100 |
| Timer / async: publication to resume | Untraced | 0.001700–0.002300 | 0.003600–0.005100 | 0.294200 |
| Timer / async: arm/queue to callback | Traced | 15.358800–15.379850 | 15.394100–15.420100 | 16.507200 |
| Timer / async: publication to resume | Traced | 0.011150–0.011850 | 0.036450–0.038150 | 0.542100 |
| Timer / inline eligible: arm/queue to callback | Untraced | 15.505650–15.525900 | 15.510000–15.530550 | 16.586600 |
| Timer / inline eligible: publication to resume | Untraced | 0.000000–0.000000 | 0.002150–0.002450 | 0.199000 |
| Timer / inline eligible: arm/queue to callback | Traced | 15.309550–15.322750 | 15.348550–15.361750 | 16.367300 |
| Timer / inline eligible: publication to resume | Traced | 0.000000–0.000000 | 0.024850–0.026350 | 0.056900 |
| Accepted work / async: arm/queue to callback | Untraced | 0.000500–0.000600 | 0.001100–0.001300 | 0.302000 |
| Accepted work / async: publication to resume | Untraced | 0.000200–0.000300 | 0.000500–0.000700 | 0.008600 |
| Accepted work / async: arm/queue to callback | Traced | 0.004700–0.006100 | 0.026700–0.030350 | 0.262700 |
| Accepted work / async: publication to resume | Traced | 0.000600–0.002100 | 0.018650–0.020450 | 0.300300 |

The dominant observed timer leg precedes managed callback entry: traced async-timer median lower/upper endpoints are about 15.359–15.380 / 15.394–15.420 ms. After publication, traced median endpoints are about 11.15–11.85 / 36.45–38.15 us; untraced medians are 1.70–2.30 / 3.60–5.10 us. Direct accepted-work callback intervals are much shorter in this quiet synthetic workload. This separates the observed legs; it does not prove how much of the pre-callback time belongs to native timer resolution, managed dispatch or OS scheduling. The pattern is consistent with the documented Windows clock limitation of short Task.Delay calls, an inference rather than a measured timer-ready event. [Delay contract](https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.task.delay).

The inline-eligible control resumes within publication on the callback thread in all 1,024 trials, including all 512 traced trials. Neither asynchronous profile is classified inline. The async timer resumes before the publisher's after-point in 59/512 untraced and 2/512 traced trials; the async queue profile does so in 11/512 and 129/512. Those races are retained with zero conservative lower bounds where appropriate. Trace instrumentation changes endpoint width and race frequency. It is inappropriate to interpret the table as a recommendation to remove asynchronous continuation behavior or as a source-only Engine speedup.

The largest upper publication endpoint is 0.5421 ms in the traced async timer; all slow/first/racing trials remain present. Four paired interval-difference records per profile retain both lower/upper mean differences. Profile order is fixed, so JIT/pool warming and shared-host background work can differ across profiles; this does not establish a universal timing bound or a fully isolated scheduler cost. No new performance threshold or significance claim is applied.

## GC and capture coverage

Four traced comparison processes reconcile 14,856 marker events against exact raw point/receipt profile/trial/kind/native identity and QPC brackets, with reported loss/payload-read errors zero. Each has one recorded complete CLR suspension episode elsewhere in its capture. No inner or envelope GC interval overlaps any of the 512 direct-delay windows, 1,536 callback-leg windows or 893 guaranteed post-publication windows. This is absence of recorded overlap within these validated intervals, not a claim that GC never occurs or a retrospective statement about the five historical drops. Suspension can itself contain GC-thread scheduling, so it is not an exclusive GC-versus-OS partition.

The current token is unelevated and has no SeSystemProfilePrivilege/SeDebugPrivilege. No kernel session, privilege, driver, trust-store, affinity, priority, ThreadPool limit, GC flag or timer-resolution setting was changed. Native timer-ready and CSwitch/ReadyThread coverage remain unavailable. No new HTTPS execution, pacer change or benchmark retry was performed. The earlier four zero-drop warmup traces and both incomplete comparison attempts remain intact.

## Validation, provenance and continuation

The complete Samples delivery is pinned at [1f1251639c04e07566f0449839898db5ca3357ce](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/1f1251639c04e07566f0449839898db5ca3357ce/tooling-small-api/evidence/2026-11-20-timer-publication). The diagnostic feature branch was merged into main and deleted after its exact staged evidence digests were checked.

Preflight includes one fresh traced positive GC/TPL/marker fixture plus untraced and traced eight-trial-per-profile processes (64 probe trials). Every comparison requires validated preflight from its exact prepared-manifest hash, checks source/binaries before targets start and drains collectors while targets are still held alive. The new entrypoint augments a verified diagnostic copy only. Existing generated business/host/gateway bytes and emitted registration match their originals; locked package graph and collector are reused. There are no new runtime packages.

Ten new focused tests pass on Windows/WSL, including ten malformed-trial variants plus early callback/publication races, inline containment, same-TID counterexamples and endpoint bounds. All thirteen previous warmup/GC/clock tests also pass per host. Full normalized analysis replays byte-identically on WSL; this is offline replay of Windows data, not a Linux capture or supported-platform qualification. Public archive round-trips every retained raw digest and reproduces preflight/full analyses exactly.

All six original nettraces remain ignored/local, with hashes and sizes recorded; public evidence contains allowlisted normalized payloads, raw points, receipt ledgers, frozen source/protocol, original/augmented source, registry and binary/dependency hashes. Credentials, raw nettraces and binaries are not published. Large JSON/event/receipt files use lossless gzip with raw/stored SHA-256. Unchanged helper/collector source is also included for replay alongside exact pre-run freezes. No source or timing failure occurred in this slice and no result was selectively rerun.

No production behavior patch is justified. Next evidence would need a separately declared native timer-ready observation or exact completion-publication instrumentation on the actual HTTPS path, plus scoped kernel readiness/loss/cleanup controls before attributing OS scheduling. Keep #3 Blocked, #18/#20 In Progress/M0 and all original benchmark criteria, metadata, dependencies and unknown actual hours unchanged.
