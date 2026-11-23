# 2026-11-24 Small API W0 machine placement

- Samples main `7b577315` and Engine `5e92ac1` passed a locked
  Linux x64 Release build and the 52 tests. A local transfer bundle
  holds the identical deployment, its manifest, and both remote helpers.
- Existing authorized native Linux machines can use a private LAN.
  The proposed cloud pair is Hetzner CCX23 app/controller and CCX13
  driver on Spread placement with a direct private network. App
  process limits remain two exclusive CPUs and exactly 2 GiB.
- No authorized project pair, provider allocation or real machine
  preflight was observed. The WSL reference resource gate still
  rejects the local environment. No timed benchmark was started.

A local Terraform 1.17.2 and hcloud 1.70.0 mock plan passed five
tests for the proposed Singapore pair, its private subnet and
restricted public admin ingress. The driver remains private-only.
There are separate local Terraform and Linux deployment bundles.
No provider allocation or benchmark run followed.

[Allocation and execution plan](../planning/small-api-w0-machine-allocation.md)
