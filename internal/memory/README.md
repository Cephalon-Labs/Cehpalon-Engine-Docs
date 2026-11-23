# Program memory

อ่านไฟล์นี้ก่อนเริ่มงาน แล้วอ่าน handoff ที่เกี่ยวข้องและตรวจ GitHub/Git/CI ปัจจุบัน วันที่ในชื่อไฟล์อย่างเดียวไม่รับประกันลำดับเวลา

Latest handoff: [2026-11-23 Opt-in audit read timeout signal](2026-11-23-audit-read-timeout-signal.md).

Prior delivery: [2026-11-23 Public read timeout API](2026-11-23-audit-read-timeout-api.md).

Prior delivery: [2026-11-23 Optional audit read deadline overhead](2026-11-23-audit-read-deadline.md).

Prior delivery: [2026-11-23 Audit history over HTTPS and PostgreSQL](2026-11-23-audit-history-https.md).

Prior delivery: [2026-11-23 Audit history read allocation](2026-11-23-audit-history-read-cost.md).

Prior delivery: [2026-11-23 Visual Studio profiles for web sample self-tests](2026-11-23-sample-debug-profiles.md).

Prior delivery: [2026-11-23 GraphQL field errors during F5](2026-11-23-graphql-field-errors.md).

Prior startup delivery: [2026-11-23 all sample and Tooling startup](2026-11-23-all-sample-startup.md).

Prior startup delivery: [2026-11-23 Small API empty-argument startup](2026-11-23-small-api-no-args.md).

Prior build delivery: [2026-11-23 Samples Visual Studio Build/restore](2026-11-23-small-api-visual-studio-restore.md).

Prior runtime delivery: [2026-11-22 offline audit-read contracts](2026-11-22-audit-contract-export.md).

Prior delivery: [2026-11-22 optional shared audit-read admission](2026-11-22-audit-read-admission.md).

Prior delivery: [2026-11-22 protected audit resource history transports](2026-11-22-audit-resource-history-transports.md).

Prior delivery: [2026-11-21 optional protected audit receipt transports](2026-11-21-audit-receipt-transports.md).

Prior delivery: [2026-11-21 optional cooperative audit read budget](2026-11-21-audit-read-budget.md).

Prior delivery: [2026-11-21 optional indexed audit storage profile](2026-11-21-indexed-audit-storage.md).

Prior delivery: [2026-11-21 exact resource history query](2026-11-21-resource-history-query.md).

Prior delivery: [2026-11-21 optional exact audit receipt lookup](2026-11-21-audit-receipt-lookup.md).

Prior delivery: [2026-11-21 optional total cooperative drain budget](2026-11-21-total-drain-budget.md).

Prior delivery: [2026-11-21 bounded manual outbox delivery](2026-11-21-bounded-drain.md).

Prior delivery: [2026-11-21 optional cooperative outbox relay budget](2026-11-21-relay-budget.md).

Prior delivery: [2026-11-21 .NET11 GA correction and current build evidence](2026-11-21-dotnet11-ga.md).

Prior delivery: [2026-11-21 protected outbox status and Project4 readback](2026-11-21-outbox-status.md).

Prior delivery: [2026-11-21 optional provider transaction and audit outbox](2026-11-21-audit-outbox.md).

Prior delivery: [2026-11-21 awaited audit execution](2026-11-21-audit-execution.md).

Prior delivery: [2026-11-20 audit preflight and prepared recording](2026-11-20-audit-preparation.md).

Prior delivery: [2026-11-20 configurable audit trails and observation lifetime](2026-11-20-observation-audit-trails.md).

Prior delivery: [2026-11-20 optional session-status boundary](2026-11-20-session-status.md).

Prior delivery: [2026-11-20 optional local key-ring lifecycle](2026-11-20-local-keyring.md).

Prior delivery: [2026-11-20 nested signed JWE](2026-11-20-jwe.md).

Prior delivery: [2026-11-20 authentication profiles, switching and tenant read sets](2026-11-20-auth-profiles-tenant-readsets.md).

Prior delivery: [2026-11-20 optional authentication, RBAC/ABAC and audit/history](2026-11-20-optional-access-audit.md).

Prior delivery: [2026-11-20 controlled timer publication probes](2026-11-20-timer-publication.md).

Prior delivery: [2026-11-20 Windows warmup drop tracing](2026-11-20-windows-warmup-drops.md).

Prior delivery: [2026-11-20 HTTPS listener overhead](2026-11-20-https-metrics-overhead.md).

Prior delivery: [2026-11-20 live HTTPS budget metrics](2026-11-20-live-budget-metrics.md).

Prior delivery: [2026-11-19 opt-in budget metrics](2026-11-19-budget-metrics.md).

Prior delivery: [2026-11-19 concurrent budget observation](2026-11-19-budget-contention.md).

Prior delivery: [2026-11-19 snapshot observer cost](2026-11-19-snapshot-observer-cost.md).

Prior delivery: [2026-11-19 aggregate budget snapshots](2026-11-19-budget-snapshots.md).

Prior delivery: [2026-11-18 operation budget drain](2026-11-18-operation-budget-drain.md).

Prior delivery: [2026-11-18 tenant concurrency budget](2026-11-18-tenant-concurrency-budget.md).

Prior delivery: [2026-11-17 generated Small API capacity](2026-11-17-small-api-capacity.md).

Prior delivery: [2026-11-17 public repositories and operation overload](2026-11-17-public-repositories-operation-capacity.md).

Latest product slice: [2026-11-16 operation concurrency budget](2026-11-16-operation-concurrency-budget.md), with portable admission and tenant contracts plus local Windows/WSL evidence.

Latest investigation: [2026-11-16 Roslyn GC event identity](2026-11-16-roslyn-gc-event-object.md), with four awaited-worker waits bound to the same object and exact GC emitter. Prior investigation: [2026-11-16 CoreCLR GC event-object fixture](2026-11-16-coreclr-gc-event-object.md), with the same exact object on wait and setter sites for two newborns. Prior investigation: [2026-11-15 Roslyn recorded wake order](2026-11-15-roslyn-gc-wake-order.md), with restart-bracket timing and all comparison links overlapping other suspension envelopes. Prior investigation: [2026-11-15 Roslyn GC wait callsite](2026-11-15-roslyn-gc-callsite.md), with six exact awaited-worker callsites enclosing a switch and linked GC inner interval. Prior investigation: [2026-11-15 CoreCLR newborn GC wait fixture](2026-11-15-coreclr-gc-wait-newborn.md), with two later-born worker lifetimes and same-image process isolation. Prior investigation: [2026-11-15 CoreCLR GC wait callsite fixture](2026-11-15-coreclr-gc-wait-callsite.md), with exact instruction probes and positive/negative control on one owned worker. Prior investigation: [2026-11-15 Roslyn GC and worker intervals](2026-11-15-roslyn-gc-task-intervals.md), with 15 GC inner spans between worker scheduler receipts. Prior investigation: [2026-11-15 Roslyn without precise allocation reads](2026-11-15-roslyn-without-allocation-probes.md), with zero residual reason-0 starts and all 306 outputs matched. Prior investigation: [2026-11-15 Roslyn precise allocation reads](2026-11-15-roslyn-allocation-probes.md), with both traces reconciled against the diagnostic driver probe windows. Prior investigation: [2026-11-15 Roslyn without stack sampling](2026-11-15-roslyn-without-stack-sampling.md), with residual reason-0 sequences and same-execution GC/scheduler co-occurrence. Prior investigation: [2026-11-15 Roslyn GC episode replay](2026-11-15-roslyn-gc-episodes.md), separating stack-sampling suspension from source-linked blocking GC. Prior investigation: [2026-11-15 Roslyn Emit boundary joins](2026-11-15-roslyn-emit-boundaries.md), with same-execution TPL, GC and native scheduler co-occurrence. Prior investigation: [2026-11-15 CLR ThreadPool boundary hooks](2026-11-15-clr-threadpool-boundary.md), with real managed worker binding and paired incremental observer overhead. Prior investigation: [2026-11-10 scoped scheduler entry/exit fixture](2026-11-10-scheduler-boundary-fixture.md), with actual two-hook attachment, owned newborn and no-switch pairs; CLR ThreadPool perturbation and Roslyn/GC causal qualification remain open. Prior investigation: [2026-11-10 owned callback clock brackets](2026-11-10-scheduler-clock-brackets.md), with a complete fixed native negative/positive pair and perpoint reference brackets; physical switch timing and historical Roslyn qualification remain open. Prior investigation: [2026-11-10 raw scheduler-state and clock contract](2026-11-10-scheduler-state-contract.md), with explicit source-based state labels and unchanged legacy results; physical scheduler duration and GC cause remain uncertified. Prior investigation: [2026-11-07 same-execution Roslyn scheduler correlation](2026-11-07-roslyn-scheduler-correlation.md), with complete admitted lifetimes and identity-bound TPL waits; state-mask/timestamp and GC causal attribution remain unresolved. Prior investigation: [2026-11-06 CLR ThreadPool scheduler fixture](2026-11-06-clr-threadpool-scheduler-fixture.md), with actual callback binding and a complete paired collector-overhead series. Roslyn correlation remains pending. Prior investigation: [2026-11-06 multiworker scheduler fixture](2026-11-06-dynamic-scheduler-multiworker.md), with nested admission, overlapping worker lifetimes and readmission after free. CLR ThreadPool evidence remains pending. Prior investigation: [2026-11-06 active dynamic scheduler fixture](2026-11-06-dynamic-scheduler-active-fixture.md), with named owner acknowledgement, loss rejection and one complete synthetic worker lifecycle. Roslyn evidence remains pending. Prior investigation: [2026-11-05 dynamic scheduler native preflight](2026-11-05-dynamic-scheduler-native-preflight.md), with held-owner pidfd seed and two unattached verifier passes. Active lifecycle evidence remains pending. Prior investigation: [2026-11-05 dynamic scheduler admission](2026-11-05-dynamic-scheduler-admission.md), with offline layout/replay and one unattached verifier load completed; actual owned birth, remote wake and Roslyn remain unqualified. Prior investigation: [2026-11-03 static scheduler conformance](2026-11-03-static-scheduler.md), with fixed loss-negative and fresh positive static cases completed; owned new-wake and dynamic Roslyn coverage remain unqualified. Prior investigation: [2026-11-02 owned task PID mapping](2026-11-02-scheduler-pid-mapping.md), with one actual local738-to-global1056 owned syscall sample; full scheduler/dynamic coverage remains unqualified. Prior investigation: [2026-11-02 disabled scheduler perf preflight](2026-11-02-scheduler-conformance.md), with one successful disabled open/read/close and unresolved initial-namespace actor mapping; no active capture readiness. Prior investigation: [2026-11-02 scheduler readiness](2026-11-02-scheduler-readiness.md), with ordinary-user denial, one-shot root format visibility and a reviewed disabled-open/payload-filter specification; active capture readiness remains false. Prior investigation: [2026-11-01 awaited worker contexts](2026-11-01-roslyn-worker-context.md), with strict point scopes, nonexclusive managed-frame labels and explicit unknown/no-sample coverage; no progress/CPU/GC/scheduler cause established. Prior investigation: [2026-11-01 literal Roslyn task ordering](2026-11-01-roslyn-task-ordering.md), with complete raw-reference binding and literal event categories, no workload launch or causal/duration claim. Prior investigation: [2026-11-01 Roslyn task lineage](2026-11-01-roslyn-task-lineage.md), with one complete same-execution TPL generator lane, audited task-header/method-point observations and no causal or performance claim. Prior investigation: [2026-11-01 synthetic task conformance](2026-11-01-task-conformance.md), with positive task-to-thread linkage in an isolated seven-case target, retained failed pair and no Roslyn/scheduler/GC causal claim. Prior investigation: [worker trace feasibility and exact-source correction](2026-10-31-worker-feasibility.md), with task-event candidates and scheduler access not established. Prior investigation: [2026-10-31 Emit worker GC/scheduler evidence](2026-10-31-emit-workers.md), with two legacy GC boundary disputes, cumulative-credit limits, passing offline audits and no justified Engine patch. Prior investigation: [2026-10-30 same-process tooling waits](2026-10-30-tooling-waits.md), with observed caller wait context in Emit and no justified Engine patch. Prior investigation: [2026-10-30 tooling JIT/GC/scheduler/IO traces](2026-10-30-tooling-traces.md), with complete diagnostic lanes and original untraced benchmark; no justified Engine patch and variance unresolved. Prior investigation: [2026-10-30 tooling variance](2026-10-30-tooling-variance.md), with correctness passed and variance unresolved. Prior [tooling observations](2026-10-30-tooling-benchmark.md) follow [offline transport contract export](2026-10-29-tooling-contract-export.md), [Small API CLI profile](2026-10-29-small-api-cli.md) and [portable CLI/scaffolding](2026-10-29-portable-cli.md). At that earlier RC snapshot, new-revision CI was payment/spending blocked before steps; current GA CI passes at its exact revision, as recorded in the latest handoff. #3 remains Blocked. Prior [collector readiness and canonical04](2026-10-29-collector-readiness.md) completes the [collector investigation](2026-10-28-collector-readiness.md) and succeeds [startup/variance tuning](2026-10-28-small-api-tuning.md), the [complete Small API observation handoff](2026-10-28-small-api-benchmark.md), the [protected adapter handoff](2026-10-28-transports-small-api.md), the [portable tenant/identity handoff](2026-10-28-tenant-identity.md) and [W1 Core/Composition/codegen handoff](2026-10-27-w1-core-composition-codegen.md); refresh current tracking and CI before work.

- [2026-10-27 new baseline and user decisions](2026-10-27-program-bootstrap.md)
- [Program plan](../planning/2026-10-27-program-plan.md)
- [Shared skill](../../skills/cehpalon-engine/SKILL.md)

บันทึกแต่ละครั้งให้มี: คำขอ/คำตัดสิน, ข้อเท็จจริงที่ตรวจแล้ว, หลักฐาน, สิ่งที่เปลี่ยน, สิ่งที่ยังไม่พิสูจน์, blockers และงานถัดไป แยก proposed/accepted/observed ชัดเจน ไม่เก็บ secrets หรือ private access tokens

Memory ช่วยเริ่มต่อ ไม่ใช่หลักฐานว่าระบบปัจจุบันผ่านการทดสอบ ต้องตรวจ revision/provider/version/host ที่เกี่ยวข้องเสมอ
