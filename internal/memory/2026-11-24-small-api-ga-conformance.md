# 2026-11-24 Small API GA conformance and reference preflight

- Exact Samples `a8ad452677c48d87a125460c552ee01c3e044046` and Engine
  `5e92ac1c7fa1e150e7e97de6d68e94b31ffba053` passed locked Release
  conformance on WSL Ubuntu 22.04.5 and Windows 11 using .NET 11 GA.
- Native baseline and Engine passed both HTTP and GraphQL on each host.
  Each host recorded 4,000 ordered cases, 400 cancellations included in
  those cases, 120 lifecycle cycles and five configuration checks. The
  original dataset, ordered corpus and final-state digests agree with
  the archived RC3 fixture. Raw JSON archives and independent readbacks
  are retained under `internal/evidence/small-api-ga-conformance/`.
- The requested 2-dedicated-vCPU/1-GiB allocation and separate driver
  were not verified. W0 requires a 2-GiB app allocation. The current
  loopback harness reports only observational timing, and WSL showed no
  reserved vCPU or app RAM cap. No timed benchmark was launched.

[Validation and retained evidence](../validation/small-api-ga-conformance.md)
