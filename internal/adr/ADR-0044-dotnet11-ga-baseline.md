# ADR-0044: Select verified .NET11 GA for current builds

Status: Accepted correction/continuation. Date2026-11-21. Tracking #3; regression validation does not requalify #20 benchmarks.

## Current fact and decision

The user correctly points to [Microsoft's .NET11 download page](https://dotnet.microsoft.com/en-us/download/dotnet/11.0). It lists SDK11.0.100 and runtime/ASP.NET Core11.0.0, released2026-11-10. The repository still selected11.0.100-rc.3.26522.148. Product release status and the project's older pin must be stated separately; calling the current product RC was stale.

Pin current global.json to11.0.100 with rollForward disable and allowPrerelease false. Migrate current JwtBearer package, strict CLI source validation and emitted Small API template to11.0.0. Refresh only affected locked graphs; retain unrelated Roslyn4.14.0, Npgsql10.0.3, RabbitMQ.Client7.2.2, HotChocolate16.7.1 and compatible IdentityModel8.19.2. [Official JwtBearer GA package](https://www.nuget.org/packages/Microsoft.AspNetCore.Authentication.JwtBearer/11.0.0) declares its IdentityModel OpenIdConnect floor>=8.19.2. Actual lock differences must be reviewed, not assumed.

Install official SHA512-verified Windows/Linux SDK archives privately under D:/Cephalon/.tools/dotnet11-ga, alongside existing dotnet11 RC folders. No global installation, PATH replacement, RC deletion, workload upgrade or Hosting Bundle. Retain official release metadata, selection/installer sources, hashes, failed preparation and actual SDK/runtime probes.

## Evidence boundary

Historical versioned requirements/ADRs/raw and exact-source profile locks remain unchanged. Current generic build/scaffold labels and active Small API/security/outbox consumers move to GA. Root Samples SDK selection means historical collector build commands need their original RC source checkout/private SDK; current GA cannot reuse old CoreCLR offsets, GC/setter/scheduler attribution, compiler timings or benchmark qualification. Original thresholds/workloads remain. New functional GA tests establish only their exact source/package/host/profile.

Microsoft's [OS table](https://github.com/dotnet/core/blob/main/release-notes/11.0/supported-os.md) currently carries an older2026/09/28/GoLive heading despite the GA download page. It lists Server2025 and Ubuntu22.04, but does not list local Windows26H2/build26300. Retain that source/date discrepancy. GA availability alone does not establish this program's local supported-host/provider qualification. #3 remains Blocked; hosted Server2025 no-server smoke and actual local provider proof are separate.

## Validation and tracking

[Protocol](../validation/dotnet11-ga.md). Freeze before graph restore, explicitly record unlocked GA lock refresh then locked Release/warnings-as-errors runs. Verify strict CLI rejection of RC pins/prerelease opt-in and actual generated GA consumers. Run complete components, platform/driver smoke, HTTPS/auth profiles, PostgreSQL transaction/status and current Small API functional validation serially on Windows/WSL. No broad dependency upgrade or framework redesign. #3 title/body changes reflect GA, while native/project metadata remain; #20 and other card rows stay unchanged. Reviewed plan/apply/readback plus independent Project4 fields. Main push/owned branch cleanup and raw retention continue.
