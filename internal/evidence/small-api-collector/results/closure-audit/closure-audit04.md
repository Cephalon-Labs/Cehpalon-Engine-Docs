# Canonical04 functional, readiness and forensic closure audit

Result: **passed with explicit limits; no evidence inconsistency found.** This is read-only evidence analysis after all canonical04 timings completed. No build, test rerun, requests, runtime execution, benchmark, source change, commit or remote write was performed.

## Frozen source and functional evidence

Samples source is `a3bd8b5c5747440c81124774ac10b6451d88ff82`; Engine remains `6804271d429106864e01e4ec546a41dff771f84b`. Reused the completed sequential02 independent audit, freshly verified all **15 frozen Git inputs per host**, and checked all **42 retained conformance JSON hashes** against that audit. The 3 emitted typed registrations are `catalog.get`, `catalog.list`, `catalog.set`; the actual runtime dependency graph excludes CodeAnalysis/CodeGeneration libraries. The source and native assembly identities in both frozen probe and canonical04 manifests agree with the audited Linux02 native assembly (`742451b86f81c439938d93aad19a0f568133fe9ff2910bae4458f6633cdcfdd4`).

Each sequential02 host has **4,000 ordered corpus cases, including 400 cancellation cases, 120 same-process lifecycle cycles, and 20,000 API-only exercise requests**. Combined totals are 8,000 / 800 / 240 / 40,000. Dataset hash `1f78590b75d2facbe87ddb8072d3870bdb1ae1fb02dd5ef2df052021de40564b`, corpus hash `d36fb51be1a5c62d013e9637d8371e9d9eae3b3059f3237f3fcc25e4eb8dcb9f`, independent final-model hash `a285ae0e130dbf825d8944028f5a3b600df27b914949e2c66dbe5f01dd8a9a0b` remain unchanged.

Maximum cancellation ACK reconstructed from raw ticks: **Windows02 1.2032 ms; Linux02 1.330781 ms** (the Linux stored display truncates to 1.3307 ms). Every passing cancellation establishes handler entry before abort, owned completion and no mutation after ACK. Maximum repeated shutdowns were 6.5286 ms / 1.6362 ms. Windows frequency is 10 MHz; Linux is 1 GHz. API-only GraphQL/forbidden probes remain zero, with positive GraphQL hooks in enabled hosts. Five invalid/all-off configuration checks are pure compiler preflight checks, not public all-off host execution.

Reused native staging proof independently verified **67 application files, 23,281,577 bytes; 4,178 SDK regular files, 549,400,671 bytes; and 1,668 symlink targets** before the timings. The closure audit did not rehash the large SDK tree. These establish source/byte/link identity; actual loaded-module evidence is separately retained by the controller.

**Windows01 remains failed.** Its baseline HTTP case409 entered the delayed handler 0.3382 ms after the abort. ACK0.5528 ms, no late mutation and owned completion do not satisfy in-flight cancellation. The complete Windows01 and Linux01 evidence remain separate from the predeclared complete sequential02 repeat. No causal claim about concurrent activity is established, and no individual case was substituted.

## Frozen readiness probes: actual versus planned

Independently audited the native `collector-readiness-probe-01` tree: HTTP/GraphQL × 3 fresh-process pairs, ordered BE / EB / BE = **12 completed probes**. All have:

- **4,000 actual preflight rows** with 8-field schema, ordered indices, exact 2,000/s scheduled timestamps, status200, positive body bytes, no errors/drops and 80/15/5 get/list/set mix.
- **360,000 planned manifest offers** retained; each actual raw prefix matches its declared manifest. Paired manifests and prefixes are deterministic per wire.
- **130 successful read-only preparation calls**: 2 CONTROL reads plus 128 LOAD responses, held simultaneously with positive HTTP1.1 framing and keepalive, all headers ready before common release, all body reads at/after release, and all bodies validated before preflight.
- **128 distinct fresh LOAD TLS connections at the barrier**, plus 1 CONTROL connection. TLS1.3 and cipher metadata retained. All 12 phases have 129 TLS events before and after and zero newly observed connections during preflight. IDs corroborate the held-response readiness cohort; they are not universal per-request socket tracing.
- Fresh PID, state/metrics accounting, client-before/after and TLS snapshots, raw persistence after request join, independent replay of all 10,000 final records and final hash `8c849f782701cc524da2ebd0b9dcc78b81efef8ad6a14dfd437e1c2abd2ab9cc`.
- Exactly 200 writes, 3,930 reads, **4,130 factories/constructors/disposals**, disabled probes zero where required, graceful shutdown within5s, closed listener and balanced owned handlers.

Totals: **48,000 actual scheduled offers**, **4,320,000 planned offers**, **1,560 preparation reads outside schedules**, **zero warmup/measured phases**. These counts must not be conflated. Preparation occurs outside startup measurement. Probe results have no sustained-capacity or acceptance-budget score.

## Offline and actual-negative proof retention

Verified retained results rather than rerunning them: **10 offline conservation/serialization checks**, **29 shared metadata validator tests**, **16 classifier assertions**, and **5 actual owned TLS negative fixtures**. These are distinct evidence types, not additional benchmark trials.

All five peer cases retain matching raw-file hashes and managed exit1: Connection:close, zero-length body, invalid body, one header stalled through a shared30s deadline, and a fully prepared 128-connection cohort followed by **4,000 HTTP503 responses**. The stalled case exited in30.351927449s with preparation30.014947617s; cleanup joined all130 started preparation rows. The503 case retains all4,000 ordered raw errors plus structured `collector-preflight-failed`, client/GC and129-before/after TLS events; only preflight was entered. No warmup/measured artifacts were created. Peer binary is a separate build of reviewed Driver source; no bit-identity claim with the canonical native binary is made.

## Canonical04 diagnostics versus retained03 failure

Canonical04 diagnostic summaries account for **12/12 timed runs, 1,872,000 measured offers, zero reported contract/capacity errors, drops or shutdown failures**. In particular HTTP Engine2,000/s completed360,000 measured offers; its preflight retained128 held LOAD connections,129 TLS events before/after and zero new IDs. Other agents independently audit the complete canonical04 timed raw corpus; this audit independently checks the readiness raw corpus and diagnostic accounting.

Canonical03 HTTP Engine2,000/s remains **4,000 actual preflight offers, 3,963 correct, 37 `offered.dropped`**, indices129–161 and178–181. It did not enter timed warmup/measurement. Its successful preparation retained only **4 initial TLS events**. Its failed phase **does retain client/CPU/GC timing accounting but has no before/after phase TLS bags**. The missing events cannot be reconstructed by the newer collector. The new readiness proof and subsequent successful diagnostic are an observed association; they do not isolate a single cause for03 drops, establish an Engine capacity ceiling, or erase the failed run.

Main04 CVs reported by the canonical controller are below10%; Engine GraphQL04 is4.76935%, **higher than03's3.2616%**. Therefore there is no all-metric improvement claim. Diagnostic rates have no latency/allocation acceptance gate and cannot replace the1,000/s series.

## Scope and reproducibility

This remains a public fixed-identity synthetic fixture on shared observational infrastructure. It does not prove real tenant authority, IdP/provider integration, production behavior, dedicated reference2CPU/2GiB resources, or supported-Windows qualification. **#3 remains Blocked; Engine is unchanged.** Corpus cancellation400 is included within4000; lifecycle120 is same-process; API exercise20k is established by deterministic source loops and completed assertions, not20k separately saved response bodies.

Reproduce this read-only audit with WSL Python using `audit-closure04.py`. Outputs: `closure-audit04.json` and this Markdown. The JSON retains exact paths, raw hashes, prior evidence, per-run counts and limitations. An initial audit-model spelling error (`Item` versus frozen source's `item-{id:D5}`) and its output are preserved in `audit-script-label-defect-attempt01.py/json`; only the audit expectation was corrected. No workload evidence was changed or rerun.
