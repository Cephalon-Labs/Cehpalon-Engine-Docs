# Final benchmark host/source provenance review

Read-only audit after all measurements completed. No builds, workload reruns, source edits or remote mutations.

Verified106 frozen Engine/Samples source hashes against the recorded commits. Build manifest's12 C# project/lock/config/verifier inputs remain identical between compiled Samples9d915f90b66d90e44c7a54f8a5d6b4415df799e5 and observed Samplesd9f401a5c0de2687ba20b511f62715c7bdd69e23; only tools/benchmark_small_api.py changed after build, as separately disclosed. Actual retained DLL/deps hashes match build and attempt02 manifests; no Roslyn/CodeGeneration runtime libraries.

Native HTTP/HotChocolate fields dispatch directly to the same owned handler/store/validator source. Engine selects generated Core registration/dispatcher, Composition compilation/activation and Engine adapters. Both paths share one executable/package graph and portable result/context/interface/binding representations; common startup also constructs unused pure ModuleRegistration metadata on the native branch. Therefore this is a direct native-dispatch comparison with shared fixture scaffolding, not an Engine-free minimal distribution or stripped-package/RSS comparison.

All172 server-ready reports use the same public CA hash. All172 shutdown/final-state reports show graceful exit0, closed listener, balanced handler factories/disposals and zero forbidden-module probes. API-only has zero GraphQL registration/services/diagnostic/executor/schema-ready probes; GraphQL has actual positive executor-created/schema-ready observations. The schema-ready counter observes executor.Schema, not an independent constructor hook. Post-run Linux/proc inspection found no owned SmallApi.Benchmark dotnet children.

All32 timed load/diagnostic result files contain actual TLS1.3 observations:4233 connections, HTTP1.1, TLS_AES_256_GCM_SHA384. Source enforces TLS1.3, custom-root chain trust and normal hostname validation without validation bypass. Private fixture remains outside tracked evidence.

No remaining concrete source/provenance/lifetime issue found in this audit. The public synthetic fixed-principal fixture does not establish protected identity/tenant/provider behavior; those separate tests cannot be inferred from this benchmark.

Canonical result boundaries must stay visible: nonqualified shared WSL/no reserved2CPU/no2GiBcap; startup p95 fails absolute1000ms for both variants/transports; GraphQL Engine p95 CV12.368092% exceeds10% and invalidates the canonical performance series. Favorable per-pair latency/RSS observations and diagnostic rates do not override these results. No outlier deletion, best-rerun selection or budget changes. #3 remains Blocked.

Machine-readable audit: benchmark-host-final-audit.json alongside this file.
