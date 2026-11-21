# .NET 11 GA baseline correction and regression evidence

Date2026-11-21. Tracking #3. [Requirement](../requirements/2026-11-21-dotnet11-ga.md), [ADR0044](../adr/ADR-0044-dotnet11-ga-baseline.md), [predeclared protocol and preparation corrections](../validation/dotnet11-ga.md), [developer guide](../../public/guides/dotnet11-ga-builds.md).

## Verified selection and implementation

Microsoft's [download page](https://dotnet.microsoft.com/en-us/download/dotnet/11.0) and [release metadata](https://builds.dotnet.microsoft.com/dotnet/release-metadata/11.0/releases.json) identify SDK **11.0.100**, .NET/ASP.NET Core **11.0.0**, released **2026-11-10**. The earlier project pin was RC3; it did not describe current product release status. Both official archive SHA512 values match the downloaded Windows/Linux bytes. Actual private host probes report GA. Existing private RC SDKs, system installation, PATH and workloads are retained unchanged.

Engine source b68d8e8705a48ea9a815b72126b05deedf2351b9 pins GA with rollForward disable/allowPrerelease false, selects JwtBearer11.0.0 in central policy and actual Small API output, strengthens exact runtime smoke and adds five negative CLI policy cases. Samples source66db9282a2273c941d50c608bb0d1334167ae6eb advances active Small API's Engine lock and current three consumer graphs. Eight lock-file changes are limited to JWT requested/resolved/content hashes and propagated project-reference ranges; IdentityModel8.19.2, HotChocolate16.7.1, Npgsql10.0.3 and unrelated package versions remain unchanged. Fixed source inventories17/32 and authority/lazy activation semantics are preserved.

## Retained attempts and exact sources

Installer01 verifies both archives and Windows probe, then rejects legitimate internal Linux relative links before Linux extraction. Corrected02 reviews all1830 normalized link targets within the new SDK root and succeeds, without replacing RC or redownloading archives. Failed source/log/metadata remains failed evidence.

Development focused Engine proof freezes194 inputs and36 locks; Tooling156 and no-server platform12pass/2NotRun. Consumer development freezes244 inputs; Windows651/60/40 pass before source commit. Its raw manifest truthfully records the previous Samples HEAD and dirty active source. Independent review verifies all244 executing/frozen inputs match committed66db9282 and clean Engineb68d8e8. A separately run clean committed Windows consumer matrix also passes.

Root final driver01 passes both platform lanes and clean Windows consumers, then fails the first WSL locked restore NU1008/NU1004 before corpus: placing the Samples clone beneath Engine .local inherited Engine central package policy. Preserve its clone/source/raw; no product/lock/criteria change. Corrected02 uses the same committed consumer bytes in a sibling real Git WSL clone, outside the Engine policy. All three WSL lanes are rerun there. Scaffold driver01 correctly aborts before any SDK work after predecessor failure; separate driver02 uses already frozen GA inputs after corrected WSL completion.

## Results

| Scope | Windows | WSL | Boundary |
| --- | --- | --- | --- |
| Clean locked Release components,20 suites | 1187passed/0failed | 1184passed/0failed | Exact Engineb68; three existing Windows path cases explain difference |
| Actual compiler fixture | passed | passed | Two factory/disposal calls; runtime graph only Core and fixture |
| Exact SDK/runtime/package no-server smoke | 12passed/2NotRun | 12passed/2NotRun | PostgreSQL and RabbitMQ not selected in this lane |
| Protected generated HTTP/GraphQL/security consumer | 651passed | 651passed | Fresh tenant, RBAC/ABAC, JWT/JWS/JWE, key/session/audit regression |
| Real PostgreSQL transaction/outbox/status | 60passed | 60passed | Prior34+status23+controlled restart3; retained owned WSL server |
| Active protected Small API | 40passed | 40passed | Exact updated consumer lock, real loopback HTTPS |
| Actual CLI Small API generation/build/runtime/serve | 133outer/39nested passed | 133outer/39nested passed | Separate frozen GA input lock; historical tracked RC lock unchanged |

Component source inventories141 match Windows/WSL exactly. Each build is locked Release/warnings-as-errors with zero warnings/errors. New GA consumers must retain the security registry0534d97c0deba2f33744091b828da6a8a4e375d46c44ef2ca938f2088f148489 and provider relay/status registry3651818cbccf40def05650121327f43b2c94b0b23d23aa0589a812a1e0622dd9; raw manifests record actual digests. No Roslyn/code-generation runtime leakage.

Exact-revision hosted [component CI44867631140](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44867631140) and [platform CI44867631103](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/44867631103) both succeed on windows-2025/ubuntu-24.04. Four jobs and executed steps are retained in [CI readback](../evidence/dotnet11-ga/hosted-ci.json). No usage/billing step skipped. Platform no-server smoke does not establish provider coverage.

## Evidence and limits

Public source/raw archive: [Samples GA evidence](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/security-api/evidence/2026-11-21-dotnet11-ga). Retain failed preparations, source freezes, original harnesses, official metadata/selection/hashes, restore/build/test raw and independent review. SDK archives, private fixture credentials/PFX/PEM/tokens, package caches, compiled outputs, inherited evidence and machine-private data are excluded. SHA256SUMS and Git index comparisons cover published bytes; raw remains under ignored local attempt directories.

Historical dated RC source/evidence/locks/trace collectors and offsets remain byte-identical. Their replay requires original checkout/RC runtime. Current GA is not a new original benchmark run, old measurement relabel, causal GC/scheduler map, speedup or production/provider qualification. Original #20 workload/thresholds/primers/flags/GC/concurrency and entire card remain unchanged.

Local Windows26H2/build26300 is not listed by the checked [Microsoft OS table](https://github.com/dotnet/core/blob/main/release-notes/11.0/supported-os.md), whose2026/09/28/GoLive header predates the GA page. Preserve the discrepancy. Ubuntu22.04/Server2025 are listed. Windows PostgreSQL tests use a private loopback bridge to the owned WSL container, not native Windows PostgreSQL. Keep #3 Blocked/M0, supported-host/full-provider gates and unknown actual hours; .NET12 remains research.

Only #3 native title/body is corrected to GA and new Engine SHA. Reviewed plan/dry-run/exact-hash apply/readback23 plus independent Project4 before/after23cards x11fields=253 verify all fields, identities, titles and null hours. #3 status/priority/estimates/gates remain; other22 rows/task bytes including #20 and all milestones remain unchanged. All three repos remain publicMIT; Project4 remains private. Source/evidence/main push, owned branch cleanup and fixture shutdown are recorded in the final delivery artifacts.

Final publication contains2245 source/raw/proof files including SHA256SUMS; all2245 Git-index blobs equal reviewed working bytes. Samples evidence main22c390bf438300025c7db09c3dce34f457676227 also adds the raw-byte .gitattributes rule for security-api/evidence. Post-archive SDK item evaluation reports security19Compile/0Content/2None and provider5/0/2, with zero evidence items. The primary security project's extra None is the preserved user launchSettings file; executions use clean worktrees. Fixture cleanup verifies exact container/image/name/volume and helper ownership before stop, retains image/data/volume and confirms listener/helpers closed. Owned merged branches are deleted after detaching retained worktrees; primary Engine's four user-edited files and Samples' four untracked files retain their baseline hashes. No original performance protocol or threshold changed.
