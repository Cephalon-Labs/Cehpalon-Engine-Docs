# W1 — tenant/identity contracts บน Core

ส่งมอบส่วน portable ของ #7/#8 ตามคำขอผู้ใช้ โดยคง #3 Blocked และไม่ลบ dependency/full acceptance gates เดิม [ADR-0007](../adr/ADR-0007-tenant-identity-operation-boundary.md) และ [protocol](../validation/tenant-identity-component-protocol.md) ถูกบันทึกก่อนวัด performance

Engine revision: `90d136dea3a76545e2994f64e2b3f6e096d83285` · SDK11.0.100-rc.3.26522.148/runtime11.0.0-rc.3.26522.148 · private MIT repos/Project4 เดิม ไม่มี billing, secret provisioning หรือ public/NuGet release

## สิ่งที่พัฒนา

- Identity.Contracts เป็น BCL-only ไม่มี Core/provider/ASP.NET/token-library dependency เก็บ principal แบบ exact issuer/subject, time-bounded snapshot และ immutable issuer/scheme trust allowlist การสร้าง DTO ไม่ใช่ authentication
- Tenancy ตรวจ fresh identity, membership ที่ผูก principal/tenant, resource scope ที่ผูก tenant/kind/ID และ policy แบบ default deny ก่อนสร้าง business handler ค่า metadata หรือ admin/role ที่ caller ส่งมาไม่เป็น authority
- Snapshot/selector ที่ระบบลงทะเบียนต้อง copy mutable request อย่างถูกต้อง Action/resource-kind มาจาก server binding ไม่ใช่ metadata ภายหลัง async lookups จะใช้ frozen request เดิม
- Checked context ถูก mint ภายใน ผูก operation/action/resource/principal และส่งผ่าน private Core bridge ตรวจ UTC validity พร้อม monotonic elapsed cap เมื่อพบ invalidity แล้วจะไม่กลับมาใช้ได้อีก และ revoke หลัง cleanup
- Consumer ใช้ generated Core gateway กับ tenant-aware handler ชุดเดียว ทดสอบ resource ID `shared` ที่มีจริงแยกใน tenant A/B และ data port ที่ตรวจ scope/version ก่อนอ่าน

Core primitive และ generator เดิมไม่ได้เพิ่ม authentication อัตโนมัติ ทุก protected entrypoint ต้อง route ผ่าน tenant boundary นี้ Trusted handlers/providers ยังรับผิดชอบไม่ข้าม checked ports; context เป็น capability ไม่ใช่ sandbox หรือ atomic database authorization/read

## ผลตรวจบน exact committed source

| ชุดตรวจ | Windows26H2 observational | WSL Ubuntu22.04.5 |
| --- | --- | --- |
| Identity contracts | 34/34 | 34/34 |
| Tenancy contracts | 70/70 | 70/70 |
| Core/Composition/Codegen เดิม | 154/154 | 154/154 |
| รวม component checks | 258/258 | 258/258 |
| Actual SDK compiler fixture | Passed | Passed |
| Pinned generated tenant consumer | 10/10 | 10/10 |

Locked restore/Release build โดย warnings-as-errors ผ่านทั้งสอง host ไม่มี skipped checks นับเป็น pass Windows26H2/build26300.9711 ยังไม่อยู่ใน support table ที่ตรวจ จึงไม่ใช้แทน supported-Windows proof WSL เป็น listed distribution แต่ไม่ใช่ deployment certification

Cross-tenant pre-dispatch denials มี business factory/constructor/read/write เป็นศูนย์ แม้ stateless gateway และ authority lookups ยังทำงานอยู่ กรณี expiry/cancel หลัง factory ตรวจ ownership/cleanup ของ instance ที่สร้างไปแล้ว ไม่อ้างว่าตอนนั้นไม่เคยสร้าง handler

หลักฐาน: [Windows](../evidence/tenant-identity/exact-win/manifest.json), [Linux](../evidence/tenant-identity/exact-linux/manifest.json), [consumer Windows](../evidence/tenant-identity/consumer-win/manifest.json), [consumer Linux](../evidence/tenant-identity/consumer-linux/manifest.json), [independent review](../evidence/tenant-identity/agents/boundary-review/review-final.json)

## Independent review และสิ่งที่แก้

Peer ตรวจ exact final DLL ผ่าน11/11 โดยเก็บ repro/ผลก่อนและหลังครบ พบว่า UTC rollback เคยขยายอายุ lease และทำให้ context กลับมาใช้ได้หลัง expiry แก้ด้วย monotonic cap และ latched revocation อีกกรณี cleanup-only TenantAccessDenied เคยถูกแปลงเป็น denial ปกติ แก้ให้เป็น infrastructure fault ที่เก็บ original exception ไม่ซ่อน cleanup failure

ทดสอบเพิ่ม nested/overlapping tenants, same-ID resources, input mutation ระหว่าง await, metadata ปลอม, fresh next-call revocation/fault, resource ย้าย tenant ที่ checked provider port และการเก็บ context ไว้ใช้หลังจบ operation ทั้งหมดเป็น component/in-memory proof ไม่ใช่หลักฐาน real IdP/provider

## Readiness และงานคงเหลือ

รอบนี้ไม่ปิด #7/#8 เต็มขอบเขต: real protocol authentication/token/session/key lifecycle, database/RLS/connection reuse, jobs/events/cache/retrieval และ real transport/sample paths ยังต้องพัฒนาและตรวจแยกกัน Full task Test/Benchmark gates จึงยัง Planned และ umbrella maturity M0; actual person-hours null

#3 คง OPEN/Blocked โดยไม่แก้ body/fields เดิม CI ของ revision นี้ถูกปฏิเสธก่อนขั้นตอนแรกจาก reported account payments หรือ spending limit ดู [raw CI](../evidence/tenant-identity/hosted-ci.json) ไม่ใช่ code-test failure หรือ CI pass การเชื่อมต่อ GitHub ชั่วคราวล้มเหลวระหว่าง dry run ถูก retry แบบ read-only ก่อนใช้ plan เดิม ไม่มี force overwrite

[Component benchmark](../evidence/tenant-identity/benchmark-attempt01/result.json) ผ่าน5/5guardrails เป็นเพียง synchronous fixture regression guard ตาม protocol ไม่วัด JWT crypto/network/provider/production performance เก็บ raw5paired runs และ environment/source/assembly hashesครบ ไม่มี qualification/collector workload รันซ้อนระหว่างวัด Median authorized1.160us/544B ต่อop และ denied0.371us/160B ต่อop เป็น shared-host fixture observation ไม่ใช่ production SLO หรือ constant-time claim

[Developer guide](../../public/guides/experimental-tenant-identity.md) · [Pinned consumer](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/tenant-identity) · [Final integrity validation](../evidence/tenant-identity/final-validation.json)
