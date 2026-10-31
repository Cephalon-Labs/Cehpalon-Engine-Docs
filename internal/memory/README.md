# Program memory

อ่านไฟล์นี้ก่อนเริ่มงาน แล้วอ่าน handoff ที่เกี่ยวข้องและตรวจ GitHub/Git/CI ปัจจุบัน วันที่ในชื่อไฟล์อย่างเดียวไม่รับประกันลำดับเวลา

Latest investigation: [2026-10-31 Emit worker GC/scheduler evidence](2026-10-31-emit-workers.md), with two legacy GC boundary disputes, cumulative-credit limits, passing offline audits and no justified Engine patch. Prior investigation: [2026-10-30 same-process tooling waits](2026-10-30-tooling-waits.md), with observed caller wait context in Emit and no justified Engine patch. Prior investigation: [2026-10-30 tooling JIT/GC/scheduler/IO traces](2026-10-30-tooling-traces.md), with complete diagnostic lanes and original untraced benchmark; no justified Engine patch and variance unresolved. Prior investigation: [2026-10-30 tooling variance](2026-10-30-tooling-variance.md), with correctness passed and variance unresolved. Prior [tooling observations](2026-10-30-tooling-benchmark.md) follow [offline transport contract export](2026-10-29-tooling-contract-export.md), [Small API CLI profile](2026-10-29-small-api-cli.md) and [portable CLI/scaffolding](2026-10-29-portable-cli.md). Current new-revision CI is payment/spending blocked before steps; historical hosted passes are separate. #3 remains Blocked. Prior [collector readiness and canonical04](2026-10-29-collector-readiness.md) completes the [collector investigation](2026-10-28-collector-readiness.md) and succeeds [startup/variance tuning](2026-10-28-small-api-tuning.md), the [complete Small API observation handoff](2026-10-28-small-api-benchmark.md), the [protected adapter handoff](2026-10-28-transports-small-api.md), the [portable tenant/identity handoff](2026-10-28-tenant-identity.md) and [W1 Core/Composition/codegen handoff](2026-10-27-w1-core-composition-codegen.md); refresh current tracking and CI before work.

- [2026-10-27 new baseline and user decisions](2026-10-27-program-bootstrap.md)
- [Program plan](../planning/2026-10-27-program-plan.md)
- [Shared skill](../../skills/cehpalon-engine/SKILL.md)

บันทึกแต่ละครั้งให้มี: คำขอ/คำตัดสิน, ข้อเท็จจริงที่ตรวจแล้ว, หลักฐาน, สิ่งที่เปลี่ยน, สิ่งที่ยังไม่พิสูจน์, blockers และงานถัดไป แยก proposed/accepted/observed ชัดเจน ไม่เก็บ secrets หรือ private access tokens

Memory ช่วยเริ่มต่อ ไม่ใช่หลักฐานว่าระบบปัจจุบันผ่านการทดสอบ ต้องตรวจ revision/provider/version/host ที่เกี่ยวข้องเสมอ
