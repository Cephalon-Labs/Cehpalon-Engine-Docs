# Experimental Small API measurements

The separate [public synthetic fixture](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/small-api-benchmark) compares native direct handlers with generated Core/Composition/HTTP/GraphQL paths. It uses the same binary/packages, shared validators, business handlers and fixture scaffolding; this measures activation/dispatch differences, not a separately stripped distribution.

The2026-10-28 [report](../internal/planning/w2-small-api-conformance-benchmark.md) retains all observations. Both observational hosts pass4000functional cases, including400cancellations,120same-process lifecycle cycles and20,000API-only requests/host. The public fixture is separate from protected tenant tests and supplies no real authentication, tenancy, provider or production guarantee.

All startup/idle/load/diagnostic phases completed. Benchmark acceptance did not pass: startup p95 exceeds1s, Engine GraphQL p95 CV12.3681% exceeds10%, and shared WSL cannot qualify the dedicated2CPU/2GiB reference. Favorable idle and individual latency values cannot override these results. #3 stays Blocked; full #9/#11 profiles remain experimental M0.

Reproduce with pinned Engine source, SDK, locks and the published runbook. Use a fresh output directory and all predeclared phases; retain failed attempts. Do not lower the rate, select outliers, publish a performance/capacity promise or use the synthetic fixture with real data.
