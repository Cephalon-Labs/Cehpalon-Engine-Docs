# 2026-11-23 Core/Composition acceptance and GA contract exports

Engine `6fe7254` makes offline OpenAPI and export manifest JSON use LF
on every host. Windows and WSL each passed 160 export checks and 25
protected HTTPS/runtime differential checks. All eight published files
were byte-identical across hosts and against the previous WSL baseline.
Samples pins this exact GA revision for the offline verifier. #20 remains
In Progress while its wider profile and benchmark criteria remain open.

The unchanged W1 component protocol passed 8/8 on exact `6fe7254`.
The required Windows Server 2025 and Ubuntu 24.04 contract CI jobs passed.
With the supported-platform #3 dependency closed, the #5 Core and #6
Composition component requirements are complete. Project maturity level
continues to represent the existing feature scopes.

#7 and #8 still need real identity/provider and lifecycle proof for their
full acceptance. #9 and #11 also require the original reference transport
run. The current WSL host has shared CPU and RAM. No existing runner has
demonstrated both the dedicated Linux x64 2 vCPU/2 GiB application tier and
a separately allocated load driver. The original reference conditions
continue to apply.

[W1 and closure evidence](../validation/w1-ga-closure.md) · [GA contract exports](../validation/tooling-contracts-ga.md) · [Platform qualification](2026-11-23-platform-real-providers-ga.md)
