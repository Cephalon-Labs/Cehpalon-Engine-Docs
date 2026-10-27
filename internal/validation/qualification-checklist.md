# Qualification checklist หลัง W0 selection

สถานะ 2026-10-27: **bounded component checks ผ่านตามขอบเขต; Engine runtime features ยัง M0** ดู [รายงานปัจจุบัน](../planning/w0-qualification-and-sync.md) และ [ผลตรวจรวม](../evidence/w0/qualification/final-validation.json) ตารางด้านล่างคงเงื่อนไข qualification เต็มไว้ ผลที่ตรวจได้ยังไม่ทดแทน Engine/provider/sample conformance

| ผลตรวจปัจจุบัน | ขอบเขต / สิ่งที่คงเหลือ |
| --- | --- |
| SDK actual SHA512, private pin, locked63-package restore/build; component smoke14/14 ต่อOS | WSL Ubuntu22.04.5 อยู่ในรายการที่ตรวจ; local Windows26H2 ไม่อยู่ จึงยังขาด listed-supported Windows proof / #3 Blocked |
| Hosted Engine/Docs matrices | GitHubปฏิเสธทั้ง4jobsก่อนstepแรกจาก account payments หรือ spending limit ไม่มีCIpassและไม่ใช่code-testfailure |
| Package graph/TFMs/raw hashes/license inventory | Nitro32.0.2 ใช้ ChilliCream License1.0 ไม่ใช่MIT-onlygraph; distribution/SBOM/notices reviewอยู่#22 |
| Immutable imagesครบ5ตัว พร้อมactualOS/Java/Erlang/start/probe/ownedcleanup | ยังไม่รับรองpersistence/restart/HA/TLS/Engineintegration/deploymentlimits |
| HTTPS/JWT/GraphQL/PG/Rabbit componentchecks | ไม่ใช่ Engine disabled-entrypoint/composition/tenancy/businesscontracts/OIDCbrowser proof |
| ModelGGUF/runnerarchive actualbytes/hash และrunner versions/dependencies | ไม่มีmodelimport/inference/tokenizer/template/embedding dimensions/runtime conformanceหรือqualityrun |
| Two-way sync59/59 Windows และ59/59 WSL, independentrepair4/4, realGitbytepreservation, liveGitHubroundtrip/staleplan/restoration | #23 Doneตามlocal+liveacceptance; hostedCIยังBlocked มีoptimisticAPI/recoverablefiletransactionlimitsระบุในusage |

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
| Tracking operations | Reviewed plan/dryrun/apply/readback/checkpoint/resume/identity mappings และ metadata conflict guards ส่งมอบแล้ว; hosted CIยังBlocked ไม่มีforceoverwriteเมื่อเจอthirdstate | #23 Done |

ตัดสิน Fail, Invalid, Blocked และ Not run ตามสาเหตุจริง ไม่สร้างผล pass จากการไม่มีเครื่อง/credentials หรือจาก CI ที่ยังไม่เริ่ม ค่าของ Actual person-hours ยังเป็น null จนมีการบันทึกเวลาคนจริง
