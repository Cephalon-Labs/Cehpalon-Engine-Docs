# แผนเริ่มต้น Cehpalon Engine — 27 ตุลาคม 2026

สถานะ: แผนพัฒนาเริ่มต้น ขอบเขต feature และตัวเลขชั่วโมงยังเป็นข้อเสนอ ไม่มี runtime feature ที่ได้รับการรับรองจากการตั้ง repository รอบนี้

## ข้อกำหนดที่ยืนยันจากผู้ใช้

- ใช้สาม repository แยกกัน: `Cehpalon-Engine`, `Cehpalon-Engine-Docs`, `Cehpalon-Engine-Samples` ภายใต้ `Cephalon-Labs` และใช้บัญชี `Cephalon-Neza`
- ผู้ใช้ยืนยันว่า URL เดิมยังถูกต้อง และ 404 เกิดจากยังไม่ได้สร้าง repos/project/milestone/tasks จึงเริ่มฐานใหม่ ห้ามยกสถานะหรือ task IDs จากงานเก่ามาเป็นสถานะปัจจุบัน
- รองรับ Samples ทั้งสามแนว: API ขนาดเล็ก, ระบบธุรกิจหลายองค์กรที่มี API/Worker/SQL, และ AI/Agent/Retrieval
- Business handlers/contracts เขียนร่วมกัน โดย config เลือก topology, transport, pattern และ architecture profile ที่ Engine รองรับจริง เปิดเฉพาะสิ่งที่ใช้
- Engine issues เป็นศูนย์กลาง task/milestone/Project; Docs มี Markdown ต่อ issue พร้อม Labels, native Type, Priority, ชั่วโมง, dependency, test/benchmark และหลักฐาน
- Card commit journal อ้างเฉพาะ full SHA จาก Engine ทุกครั้งที่ commit เกี่ยวข้อง ห้าม journal Docs/Samples SHA
- แยกเอกสารภายในกับเอกสารนักพัฒนา เตรียม public Markdown ให้แปลงเป็น Astro ในอนาคต
- ใช้ AI หลายเจ้าได้ บันทึกเหตุผล/ข้อสรุปใน memory และเก็บกติกาที่มีผลต่อการทำงานไว้ใน SKILL.md กลาง

ค่า private และ MIT ใช้ตามคำตัดสินเดิมที่บันทึกไว้ ผู้ใช้ยังไม่ได้เปลี่ยนนโยบายนี้ ไม่มีการเผยแพร่ NuGet ในรอบวางแผน

## หลักออกแบบที่เสนอ

1. Core ขนาดเล็ก เน้น BCL-only contracts, operation dispatch, result/error, cancellation และ capability metadata ไม่พึ่งเว็บ/ORM/broker/AI SDK
2. Application handlers ไม่รับ HttpContext, GraphQL context, broker object หรือ provider SDK objects โดยตรง
3. Adapters แยกแพ็กเกจตาม transport/provider/host ใช้ built-ins และมาตรฐานที่เหมาะสมก่อนสร้าง infrastructure ซ้ำ
4. Composition อ่าน trusted effective config → validate schema/dependencies/capabilities → สร้าง immutable plan → activate เฉพาะโมดูลที่เลือก หยุดก่อน side effects ถ้าเลือกชุดที่ใช้ร่วมกันไม่ได้
5. `Enabled:false` เป็นข้อห้ามเปิดโมดูล ไม่ใช่แค่ปิด endpoint ต้องไม่มี constructor/factory/connection/background work ของโมดูลนั้น โดยแยก shared dependencies ที่โมดูลอื่นต้องใช้
6. เริ่มจากเลือก config ตอน startup และ deploy ใหม่ การเปลี่ยน topology ขณะรันเป็นงานวิจัยแยกที่ต้องมี state migration/rollback ไม่ถือว่าได้รับการรองรับโดยอัตโนมัติ
7. แยก business model ออกจาก delivery semantics: synchronous call, streaming, asynchronous events และ durable workflow มีสัญญาต่างกัน
8. Tenant/identity/authorization/telemetry ต้องผ่านทุก entrypoint, storage/cache key, event envelope, background job และ retrieval scope ที่อ้างรองรับ

## ขอบเขตของการเปลี่ยนด้วย config

| การเปลี่ยน | ส่วนที่ตั้งใจให้ใช้ร่วมกัน | เงื่อนไขที่ต้องออกแบบและพิสูจน์ |
| --- | --- | --- |
| API / GraphQL / gRPC / JSON-RPC / SSE | Business operation, validation, policy | Schema/error/streaming/pagination mapping แยกราย protocol; SSE ใช้สำหรับ server streaming ที่เหมาะสม |
| Single process / distributed | Handler ที่ไม่มี process-local assumptions | Serialization, deadlines, retry, idempotency, network failure, consistency |
| SQL / document / key-value | Application ports ตาม capability | Transaction/query/index/migration semantics ของแต่ละ provider ไม่เท่ากัน |
| Server / container / Kubernetes / serverless / edge | Logic ที่ผ่าน capability constraints | Lifetime, cold start, filesystem, memory, CPU, streaming, background limits |
| Modular / CQRS / event-driven / actors / workflow | Contracts ที่เหมาะกับแต่ละ profile | ไม่บังคับว่าทุก pattern ผสมกันได้ ต้อง reject incompatible combination |

TDD/BDD/DDD เป็นวิธีพัฒนาและออกแบบ บางส่วนไม่ใช่ runtime switch ใน appsettings; dependency injection ก็ไม่ทดแทน distributed consistency

## เส้นทาง Samples ที่ต้องส่งมอบ

| Lane | จุดเริ่ม | เกณฑ์พิสูจน์หลัก |
| --- | --- | --- |
| Small API | API-only, single process, dependency ขั้นต่ำ | เขียน business operation เดียว; disabled GraphQL/Worker/AI ไม่มี activation และวัด startup/idle overhead |
| Business | Tenant-aware API + Worker + SQL | ป้องกัน tenant ข้ามกัน, authz ทุกทางเข้า, outbox/inbox, retry/duplicate/crash recovery; เพิ่ม API+GraphQL ด้วย handler เดิม |
| AI | Provider adapters + Agent + Retrieval | เปลี่ยน model provider ผ่าน contract ที่ประกาศ, tenant-scoped retrieval, tool permissions, cancellation, cost/token budgets, audit และ adversarial evaluation |

ทั้งสาม lane อยู่ในแผนเดียวกัน ใช้ Core/Composition ร่วมกันและเดินตาม dependencies เพื่อหลีกเลี่ยงสร้างแกนแยกสามชุด W0 เลือก provider candidates/workload/budgets แล้วใน [decision package](w0-decisions.md) และ ADR-0001–0004 ส่วน SDK/driver/artifact/runtime qualification ยัง pending จึงไม่อ้าง compatibility จากการเลือกเพียงอย่างเดียว

## แผนตาม milestone

| Milestone | ผลลัพธ์และ gate |
| --- | --- |
| W0 — Baseline & Research | Repos/Project/tasks, requirements traceability, comparative study, ADRs, SDK/provider compatibility, quality matrix; W หมายถึง workstream ไม่ใช่สัปดาห์หรือกำหนดส่ง |
| W1 — Core & Composition | Host-agnostic operations + config compiler + tenancy + identity; config เสียต้องล้มก่อน activation และ API-only ไม่เปิดสิ่งที่ปิด |
| W2 — Transports & Small API | REST/GraphQL conformance, small API E2E; gRPC/JSON-RPC/SSE ตามลำดับความสำคัญและหลักฐาน |
| W3 — State & Durable Business | Data/cache capabilities, eventing/Worker/recovery และ business sample; provider จริงพร้อม tenant isolation |
| W4 — AI & Operations | AI/retrieval sample, observability และ deployment profile matrix; วัด cost/security/failure ตามขอบเขต |
| W5 — Tooling & Distribution | CLI/codegen, compatibility docs, local NuGet pack/install/upgrade, package/release readiness และ developer docs |

Issue รายตัวและชั่วโมงเริ่มต้นอยู่ใน `tasks/` และ Project ช่วงชั่วโมงเป็น planning estimate ความเชื่อมั่นต่ำ รวม engineering/test/docs ของ task นั้น ไม่ใช่เวลารัน AI และไม่ใช่กำหนดส่ง Actual hours ต้องบันทึกจากงานจริง; unknown ไม่ใช่ 0

## เป้าหมายระยะยาวที่วัดได้

- ความเร็ว: วัด startup, idle RSS, allocations, throughput, p50/p95/p99, CPU และ error rate เทียบ baseline เดียวกันภายใต้ workload/เครื่องที่ประกาศ
- ความปลอดภัย: negative tests สำหรับ tenant/authn/authz, input, secret/log redaction, event/retrieval/tool boundaries พร้อม provider-specific evidence
- Developer experience: วัด bootstrap steps, business code ที่ต้องเขียน, schema duplication และ effort ในการเปลี่ยน profile
- อายุ 30–50 ปี: versioned contracts, replaceable adapters, compatibility/deprecation windows, migration tooling และรอบอัปเกรด platform อย่างต่อเนื่อง ไม่ใช่การรับประกัน binary เดิมใช้ได้ตลอด
- คำว่าเหนือกว่าทุก framework และรองรับทุกอย่างเป็นวิสัยทัศน์ ต้องแปลงเป็น comparison matrix และ workload-specific evidence ก่อนใช้เป็นข้อความรับรอง

## .NET 11/12 และความสดของข้อมูล

ตรวจแหล่งทางการวันที่ 2026-10-27: Microsoft ประกาศ .NET 11 RC3 เมื่อ 2026-10-25 และแนะนำผู้ใช้ RC2 อัปเดตเพื่อรับ security fixes จึงต้องเลือก/ล็อก SDK RC3 ที่ตรวจ distribution และ provider compatibility แล้วก่อน implementation ไม่คัดเลข SDK จาก memory มาใช้โดยไม่ตรวจ

เครื่องนี้ `dotnet --list-sdks` จาก installation บน PATH แสดงสูงสุด 10.0.402 และไม่มี .NET 11 ใน installation นี้ ยังไม่ได้ตรวจ private SDK ทุกตำแหน่งและยังไม่ได้ติดตั้งหรือย้าย runtime ของเครื่อง

.NET 12 ใช้เป็น research track และติดตาม official planning/API proposals แยกจากสัญญาที่เผยแพร่ API ที่ยังเปลี่ยนได้ต้องอยู่หลัง adapter/experimental surface ไม่มีข้อรับรองว่า .NET 12 stable แล้ว

แหล่งอ้างอิง: [RC3 security update](https://devblogs.microsoft.com/dotnet/dotnet-october-2026-oob-security-updates/), [.NET 11 release notes](https://github.com/dotnet/core/blob/main/release-notes/11.0/README.md), [ASP.NET Core milestones](https://github.com/dotnet/aspnetcore/milestones?state=open), [Generic Host](https://learn.microsoft.com/en-us/dotnet/core/extensions/generic-host), [EF Core providers](https://learn.microsoft.com/en-us/ef/core/providers/)

## มาตรฐานอ้างอิงและข้อจำกัด

ศึกษาและ pin เวอร์ชันที่ integration รองรับก่อนใช้: [OpenAPI](https://spec.openapis.org/oas/latest.html) สำหรับ HTTP contracts, [CloudEvents](https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md) สำหรับ event metadata และ [OpenTelemetry conventions](https://opentelemetry.io/docs/specs/semconv/) สำหรับ telemetry การใช้ envelope/schema ร่วมกันไม่ได้พิสูจน์ delivery guarantee, tenant isolation หรือ compatibility ของ library

การศึกษาครั้งนี้เป็น document review เบื้องต้นตาม [research note](../research/2026-10-27-reference-study.md) ยังไม่ใช่การทดลองทุก framework/kernel/OS และยังไม่มี benchmark/security audit/production proof

## คำตัดสินที่ยังต้องมีระหว่าง refinement

- W0 เลือก provider candidates/workload และ engineering budgets แล้วตาม [decision package](w0-decisions.md); ยังต้อง freeze artifact locks/actual supported OS/hardware และ qualify ก่อนนำผลไปใช้รับรอง ไม่ถือ budgets นี้เป็น production SLO ที่ผู้ใช้ลงนามแล้ว
- นิยาม supported profiles และขอบเขต restart/redeploy; live topology changes แยกงาน
- รายละเอียด API contract, tenant model, security boundaries และ AI tool approval policy ของ sample
- ขอบเขต public API, package naming และ compatibility policy ก่อน NuGet release

เดินงาน W0 ต่อได้จากแผนนี้ โดยต้องบันทึกข้อสรุปเหล่านี้ลง ADR ก่อน task ที่ขึ้นต่อกันเริ่ม implementation
