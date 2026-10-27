# 2026-10-27 — W0 providers, workloads and proof contracts

Timezone: Asia/Bangkok. Scope: user-authorized W0 study/selection/ADRs/GitHub–Docs synchronization, with three lane agents and primary as sole remote writer.

## Accepted W0 engineering choices

- Read [decision package](../planning/w0-decisions.md) and [ADR-0001](../adr/ADR-0001-w0-profile-and-proof-boundaries.md), then lane ADR-0002/0003/0004 and workload protocols.
- Small API: Kestrel/Minimal API + bounded BCL fixture; no external DB/cache/broker/AI/IdP. Hot Chocolate 16.7.1 is opt-in candidate. Dataset 10k, 1,000 req/s, 5 paired repetitions; p95/p99 budgets 20/50 ms.
- Business: PostgreSQL 18.6/Npgsql 10.0.3 async ADO.NET, RabbitMQ 4.4.0/Client 7.2.2, Keycloak 26.8.1; cache off. Optional Valkey 9.1.3 needs a qualified client pin. Order/reservation 100 tenants, 100k stock + 100k initial orders, 100 req/s, 5 pairs; HTTP p95/p99 budgets 100/250 ms. Durable outbox/inbox and at-least-once+dedup, not global exactly-once.
- AI: Ollama 0.40.11 + official pinned Qwen3-4B Q4_K_M and Qwen3-Embedding-0.6B Q8_0 + Qdrant 1.20.0; llama.cpp 0.7.0 is second inference adapter. Keycloak 26.8.1 identity is required in real-provider tiers; fixture identity does not prove authn. 10 tenants, 2,000 chunks, 200 gold + 100 negative cases; Hit@5 >= .95, mean Recall@5 >= .90, grounded answers >= .90 and zero tenant leaks/forbidden tool execution in declared suites.
- Startup config plus restart/redeploy is the first portability boundary. Common app budget 2 vCPU/2 GiB; Business splits API/Worker; providers/loadgen are separate; AI model tier 8 vCPU/16 GiB is a proposed experiment resource tier, not measured minimum.

These choices are accepted within the delegated W0 planning scope, not a user signature on production SLOs or runtime qualification. All numerical gates are predeclared engineering budgets. Runtime features remain M0.

## Observed evidence and review

- Official SDK candidate metadata:11.0.100-rc.3.26522.148 and runtime11.0.0-rc.3.26522.148. Preserved source JSON/hash and published expected SDK hashes, not downloaded binary verification.
- Queried pinned publisher metadata for both Qwen files and confirmed revision/expected SHA256/file sizes; preserved source/hash. No weights downloaded or executed.
- Integration review corrected successful-offered-work floors to exclude fast rejection, required per-variant reset/reseed after warmup, clarified scheduled-arrival latency and AI identity provenance.
- Added pull-only conflict-aware tracking tool and 15 offline conflict/recovery tests. Review found preflight/write race and partial-write risks; fixes add cooperating-run lock, atomic per-file replacement, retained recovery copies/journal and snapshot-last commit. Arbitrary external editors still have an optimistic-check window. Full generic bidirectional sync stays open.
- [Engine journal](../evidence/w0/engine-commit-journal.md) records the new Engine documentation commit and related issues only. Keep Docs/Samples commits out of task/card journals.
- No SDK install, package restore/build, actual provider/sample run, benchmark, hosted CI execution or runtime maturity promotion occurred. CI histories were empty at start of this turn.

## Tracking and resume

- Project remains Cephalon-Labs Project 4; 23 Engine issue identities are preserved. Do not use historical Project 3 or rerun bootstrap initialization.
- Closed #2/#4/#21 as Done with Test gate Passed only for W0 architecture/reference study/predeclared test strategy after document/live metadata verification. #3 remains open/In Progress for real platform/artifact/driver qualification; #23 remains open/In Progress for full reviewed bidirectional sync/migration work. Runtime implementation/sample tasks remain open. W0 milestone still has these two open tasks and is not closed.
- Final observed totals: 23 Engine issues, 4 closed (including bootstrap #1), 19 open; six milestones. Live tracking pull/check passed, the offline tracking regression suite passed 15/15, and W0 document/provenance/tracking verification passed. Detailed evidence is in `internal/evidence/w0/validation.json` and `tracking-tool-tests.json`.
- Current live state is captured in `internal/evidence/tracking/github-observed.json`; task mirrors are generated from live bodies/native Type/Labels/Priority/milestone/status/hour fields. Refresh before acting.
- Next work: qualify SDK and exact package/image/model artifact locks, select actual supported OS/hardware, create deterministic fixtures/gold and baseline parity, then implement/test profiles from their protocols. Retain all failed/invalid attempts and do not lower gates after seeing results.
