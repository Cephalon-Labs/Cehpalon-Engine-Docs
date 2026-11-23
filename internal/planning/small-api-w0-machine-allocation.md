# Small API W0 machine allocation

Reviewed on 2026-11-24. The original workload, numeric gates, fixtures,
phase ordering and transport checks are governed by the W0 protocol.
[W0 workload](../validation/small-api-workload.md) ·
[Two-host runner proof](../validation/small-api-two-host-preflight.md)

## Candidate layouts

| Route | App machine | Driver machine | Evidence required |
| --- | --- | --- | --- |
| Existing project Linux machines | Native x64/glibc with two exclusive app CPUs and at least one disjoint controller CPU | Separate authorized Linux x64/glibc machine over the private LAN | Admin allocation, direct route, distinct live machine and boot IDs, and observed capacity |
| Hetzner Cloud Singapore | CCX23 with 4 dedicated vCPUs and 16 GB VM RAM | CCX13 with 2 dedicated vCPUs and 8 GB VM RAM | Both VMs in the same Spread placement group, on the same project private network. Record the provider allocation and verify active Linux limits. |
| DigitalOcean Singapore | Regular CPU-Optimized 4 vCPU / 8 GiB | Regular CPU-Optimized 2 vCPU / 4 GiB | Confirm SKU availability, dedicated allocation, and physical-host separation through the provider if required for this attempt. The region listing does not establish physical placement. |

The minimum controller headroom comes from the runner requiring a
nonempty controller CPU set that is disjoint from the app CPUs. A
four-vCPU VM is the proposed host size. Inside the app host the app
leaf owns exactly two CPUs and has the original **2 GiB** hard cap
(2,147,483,648 bytes). Driver sizing is a proposed starting point.
Successful collector preflight establishes the observed driver
capacity for the declared profile.

Hetzner's published Singapore compute rates for CCX23 and CCX13 are
US$0.2051/h and US$0.1017/h respectively, about US$1.84 combined for a
six-hour allocation. The return from the provider must confirm stock,
account limits, the current bill and Spread membership. Rates exclude
tax and IPv4. Two Regular CPU-Optimized Droplets at published rates
would be about US$1.13 for six hours, before taxes or extras and
subject to the selected region and plans.
[Hetzner plan specs](https://www.hetzner.com/cloud/general-purpose/) ·
[Hetzner Singapore rates](https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/#singapore-sin) ·
[Hetzner Spread placement](https://docs.hetzner.com/cloud/placement-groups/faq/) ·
[DigitalOcean rates](https://www.digitalocean.com/pricing/droplets) ·
[DigitalOcean regional availability](https://docs.digitalocean.com/platform/regional-availability/)

## Allocation readback

1. Verify project ownership and authorization for both targets. For
   rented instances, record the plan, region, allocation or placement
   receipt, private network, and the spending limit associated with
   the attempt. For owned machines, record the admin-assigned
   exclusive resources and the separate driver machine.
2. Confirm Linux x64/glibc, a complete initial-namespace cgroup v2
   hierarchy, and the CPU and memory interfaces the runner reads.
   On the app machine, the administrator prepares a task-owned
   isolated leaf with exactly two effective exclusive CPUs and
   `memory.max=2147483648` bytes. Check that no ancestor reduces
   that allocation and that controller affinity is disjoint. A
   controller with delegated permission moves only its owned child
   into that app leaf. Provisioning the cgroup is separate from
   running the benchmark.
3. Confirm the driver has independent allocation and storage, the
   private IPv4 app bind and driver peer addresses, and direct TCP
   routing on their private network. Verify the app's controller
   source and the driver's source as seen by the listener. Use a
   separately pinned SSH host key and a provisioned driver account.
   Keep private keys and the working configuration untracked.
4. On both hosts verify the exact .NET SDK 11.0.100 and .NET and
   ASP.NET Core runtime 11.0.0. Pin and keep the app build receipt
   with the deployment. Copy the identical deployment and the
   two verified remote helper sources to the driver. Maintain
   the clean Engine and Samples checkouts on the app host.
   Retain the deployment hashes and data path for both roles.
   Ubuntu 24.04 x64 is a candidate. Verify the actual guest kernel
   exposes the required cgroup interfaces.
   [Linux cpuset interfaces](https://docs.kernel.org/admin-guide/cgroup-v2.html#cpuset) ·
   [Ubuntu .NET support](https://learn.microsoft.com/en-us/dotnet/core/install/linux-ubuntu-decision)

## Execution boundary

Run the existing Samples two-host invocation from the app host with
the real private configuration and a fresh output area. First use
`--preflight-only` and require all four HTTP/GraphQL baseline and
Engine lanes, `reference_preflight_passed: true`, and no timed phases.
Verify the held TLS connections, all 2,000 offered requests per lane,
expected state and owned cleanup.

After successful resource admission and standalone collector preflight,
execute the same pinned invocation with a fresh output path and the
full original phase sequence. Remove only the preflight-only switch.
The runner performs the reference admission again before entering any
timed phase. Keep the private outputs and record any invalid attempts
without leaving the original budgets.

Budget **3 h 28 min** for the full scheduled windows, before resource
and collector checks, startup launches, evidence transfer, and final
analysis. The original sequence has 20 idle windows of 240 seconds,
20 main load windows of 240 seconds, and 12 diagnostic windows of up
to 240 seconds. A failed diagnostic may stop at its declared preflight.
A six-hour allocation is a setup and collection estimate. Native SSD
storage with around 40 GiB free per host is a conservative staging
allowance for raw retained jobs, the deployment and the runtime. Preserve raw
evidence and reconcile cloud cleanup only for resources owned by this
attempt.
[Exact runner invocation](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/blob/7b577315bc86b00d457148f52b3c0fdf578e274a/small-api-benchmark/README.md#two-host-reference-execution) ·
[Timing protocol](../validation/small-api-workload.md#6-performance-protocol-และ-budgets)

## Staged build

The local Linux x64 locked Release build from Samples `7b577315`
and Engine `5e92ac1` passed all 52 unit tests before packaging.
The bundle contains the 67-file deployment, both driver helper sources,
and the build manifest. Each archive entry was independently rehashed.
Both machines can use the same Linux x64 deployment. The SDK archive
also matched the official SHA-512 for 11.0.100.
[Deployment checksums](../evidence/small-api-w0-placement/2026-11-24/staging-receipt.json) ·
[SDK integrity](../evidence/small-api-w0-placement/2026-11-24/sdk-integrity.json)

## Validated Hetzner configuration

A local Terraform 1.17.2 plan package with locked Hetzner Cloud
provider 1.70.0 passed schema validation and five provider-mocked plan
tests. The plan checks the CCX23 and CCX13 pairing in one Singapore
Spread group, fixed private IPv4 addresses on one subnet, and a single
public SSH rule on the app for an approved admin IPv4 /32. The
driver has neither public IPv4 nor public IPv6. Its .NET runtime and
deployment can be staged from the app over the private network.
The negative tests cover a broad admin CIDR, non-IPv4 administration,
a missing SSH key, and an unscoped attempt name.

Mock planning leaves provider capacity, account authorization, guest
configuration, host W0 admission and collector readiness for the
real allocation. No credentialed provider plan ran. The deploy
archive SHA-256 still matches the staged package.
[Mock plan receipt](../evidence/small-api-w0-placement/2026-11-24/hetzner-mock-plan.json) ·
[Hetzner firewall semantics](https://docs.hetzner.com/cloud/firewalls/faq/) ·
[Terraform provider mocks](https://developer.hashicorp.com/terraform/language/tests/mocking)

## Current readiness

No authorized app and driver pair was verified. The scoped checks
found no project-bound machine inventory, alias or overrides. Engine,
Docs and Samples each reported zero self-hosted GitHub runners and
the organization-level query returned HTTP 403. The local WSL view
still has CPUs 0–19 available, no cgroup CPU quota or memory cap and
an incomplete enclosing cgroup view. No provider allocation, real
two-host preflight, or timed reference benchmark was started.

[Readiness inventory](../evidence/small-api-w0-placement/2026-11-24/project-readiness.json) ·
[Local runner resource gate](../evidence/small-api-w0-placement/2026-11-24/wsl-resource-gate.json)
