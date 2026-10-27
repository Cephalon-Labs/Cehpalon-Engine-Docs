# Qualification checklist หลัง W0 selection

สถานะ 2026-10-27: **Not run / M0** รายการต่อไปนี้เป็นงานคงเหลือที่ต้องมีหลักฐาน ไม่ใช่ผลตรวจผ่าน

| ชุดตรวจ | เงื่อนไขออกจาก pending | Owner issue |
| --- | --- | --- |
| SDK/platform | ดาวน์โหลด SDK ที่เลือกและตรวจ bytes กับ published hash, pin SDK, build/run bounded smoke บน supported Linux/Windows, บันทึก runtime/OS/TFM จริง | #3 |
| Packages | Exact restore graph/lock hashes, target/runtime compatibility, transitive licenses/SBOM, current advisories และ bounded smoke ต่อ driver/transport | #3, #9, #12, #14 |
| Infrastructure artifacts | Lock image manifest/platform digests, base OS, Java/Erlang compatibility, limits, health/start/stop และ data persistence ของ PostgreSQL/RabbitMQ/Keycloak/Qdrant | #3 และ provider tasks |
| GraphQL opt-in | HTTP-only maps/cost/depth/size, no IDE/subscription activation, disabled registration/eager initialization ทำงานเป็นศูนย์ | #6, #9, #11 |
| Business contracts | Freeze schema/migrations/RLS/runtime role, trusted tenant membership, order state machine, event envelope, retry/idempotency and ordering scopes | #7, #8, #12, #14, #15 |
| Optional cache | Pin client ที่ qualify กับ Valkey จริง และ tenant-key/invalidation/failure conformance ก่อนเปิด profile; ค่าเริ่มต้นยังปิด | #13 |
| AI artifacts | ดาวน์โหลด exact GGUF และตรวจ byte hash, runner binary/container digests, tokenizer/template/Modelfile/model manifest และ embedding settings | #3, #16, #17 |
| AI provider contracts | Generation/tool/schema mapping, exact dimensions/instructions, local-only egress, bounded loops, compute cancellation และ same-weight two-runner conformance | #16, #17 |
| Fixtures/gold | สร้าง generator ที่ deterministic, review corpus/gold/state ledger, freeze source/output hashes; fixture-only ไม่ใช่ real-provider proof | #11, #15, #17 |
| Fair baselines | Policy/tenant/durability/schema/telemetry parity, same artifacts/resources/request schedule และ approved preflight ตาม protocol แต่ละ lane | #21 และ sample tasks |
| Real execution | Raw positive/negative/fault/benchmark results ตรง Engine revision, invalid attempts retained, per-provider/version/host maturity และ cleanup evidence | implementation/sample tasks |
| Tracking operations | Pull validation มี conflict/identity/drift checks; reviewed writes, resumability, migration mappings และ metadata edit conflict coverage ยังต้องทำเพิ่ม | #23 |

ตัดสิน Fail, Invalid, Blocked และ Not run ตามสาเหตุจริง ไม่สร้างผล pass จากการไม่มีเครื่อง/credentials หรือจาก CI ที่ยังไม่เริ่ม ค่าของ Actual person-hours ยังเป็น null จนมีการบันทึกเวลาคนจริง
