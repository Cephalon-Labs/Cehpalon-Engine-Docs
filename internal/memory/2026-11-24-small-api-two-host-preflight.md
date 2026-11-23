# 2026-11-24 Small API two-host TLS preflight

- Samples adds a private IP SAN TLS 1.3 listener, pinned SSH driver,
  exact deployment comparison, owned driver leases and evidence
  readback, plus fail-closed W0 resource checks.
- The two-namespace lab passed baseline and Engine on HTTP and
  GraphQL at Samples `1d984b0238bd614cb7c78675286ae25192ec9fac`.
  Each lane held 128 distinct TLS connections and returned 2,000
  correct raw preflight rows. The driver remained preflight-only.
- Trust, SAN, TLS-version, peer and SSH host-key failures were
  rejected. A closed SSH lease joined the actual remote driver.
- The W0 2-dedicated-vCPU/2-GiB allocation and separate physical or
  independently provisioned driver remain unverified. No reference
  timing or qualification was recorded.

[Plan](../planning/small-api-two-host-preflight.md) ·
[Validation and evidence](../validation/small-api-two-host-preflight.md)
