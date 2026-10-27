# W0 — Provider, workload และเกณฑ์ทดสอบที่เลือก

วันที่: 2026-10-27; สถานะ **W0 design selected; runtime qualification pending (M0)**

ผู้ใช้สั่งให้ใช้ agent ศึกษาและเลือกทั้งสาม Samples รอบนี้ primary รวมผลงาน agent ราย lane ตรวจแหล่งทางการและข้อขัดกันของ resource/semantics แล้วบันทึกเป็น ADR การเลือกนี้ทำให้เริ่ม qualification ได้ ไม่ใช่ผลทดสอบ provider จริง

| Sample | Provider ชุดแรก | Workload และเกณฑ์สำคัญที่ประกาศก่อนวัด |
| --- | --- | --- |
| Small API | Kestrel + Minimal API; bounded in-memory fixture; GraphQL opt-in Hot Chocolate 16.7.1 | Catalog 10,000 records, mix 80/15/5, 1,000 req/s, 5 paired repetitions; p95 ≤20 ms/p99 ≤50 ms; disabled modules activation =0 |
| Multitenant business | PostgreSQL 18.6/Npgsql 10.0.3, RabbitMQ 4.4.0/Client 7.2.2, Keycloak 26.8.1; cache ปิด | 100 tenants, 100k stock rows + 100k initial orders, 100 req/s; p95 ≤100 ms/p99 ≤250 ms; tenant leak/lost acknowledged effect/double reservation =0; crash/retry/poison/recovery แยก suite |
| AI/Agent/Retrieval | Ollama 0.40.11 + Qwen3-4B/Qwen3-Embedding GGUF, Qdrant 1.20.0; llama.cpp 0.7.0 เป็น inference adapter ที่สอง | 10 tenants/2,000 chunks, gold ไทย-อังกฤษ 200 cases +100 negative; Hit@5 ≥95%, mean Recall@5 ≥90%, grounded answers ≥90%; unauthorized tools/tenant leaks =0 |

ตัวเลขเป็น **engineering budgets สำหรับ reference workload** ไม่ใช่ measured capacity หรือข้อรับรอง production ทั้งสาม lane มี raw evidence, invalid-run rules, baseline fairness และ provider-specific gates ของตนเอง AI fixture, real retrieval และ real model เป็นหลักฐานคนละระดับ

- [ADR-0001 — ขอบเขตร่วมและ proof rules](../adr/ADR-0001-w0-profile-and-proof-boundaries.md)
- [ADR-0002 — Small API](../adr/ADR-0002-small-api-profile.md) และ [protocol](../validation/small-api-workload.md)
- [ADR-0003 — Business](../adr/ADR-0003-multitenant-business-profile.md) และ [protocol](../validation/business-workload.md)
- [ADR-0004 — AI](../adr/ADR-0004-ai-retrieval-profile.md) และ [protocol](../validation/ai-retrieval-workload.md)
- [Machine-readable candidates](../validation/provider-candidates.json)
- [Qualification checklist](../validation/qualification-checklist.md)

## เหตุผลหลักและสิ่งที่ไม่เปิดโดยปริยาย

Small API ต้องไม่พึ่ง SQL/broker/AI จึงใช้ fixture state ที่ระบุว่าไม่ durable Business ใช้ ADO.NET ก่อนเพื่อลดการผูกกับ EF provider major และให้เห็น transaction/outbox/inbox ชัด Cache ไม่เป็น authority ของ stock หรือ tenant AI เลือก local reference เพื่อไม่ต้องสร้างบัญชีหรือใช้บริการเสียเงิน และให้สลับ inference runner ด้วย weights เดิมเพื่อทดสอบ adapter semantics

การเลือก provider ไม่ได้ทำให้ทุก database/model/broker รองรับแล้ว และไม่ได้ทำให้ APIs ของแต่ละตัวเท่ากัน Config จะเลือกเฉพาะ compatible capability profiles โดยเปลี่ยนตอน startup และ restart/redeploy Live topology changes ยังต้องมี ADR/state migration แยก

## หลักฐานที่มีตอนนี้

- อ่าน release/package/model metadata จาก upstream และเก็บแหล่งอ้างอิงใน ADR พร้อมวันที่ตรวจ
- เก็บ official .NET release metadata และ published expected hashes ของ SDK candidates; SDK candidate `11.0.100-rc.3.26522.148` ยังไม่ได้ติดตั้งหรือทดสอบ build
- ยืนยัน metadata ของ model ที่ publisher revision ตายตัวและ expected SHA256 แล้ว [model metadata evidence](../evidence/w0/model-candidates.json) ยังไม่ดาวน์โหลด weights หรือยืนยัน binary bytes
- ตรวจเอกสาร/ลิงก์/task metadata และทดสอบ conflict handling ของเครื่องมือ pull tracking เท่านั้น ผลอยู่ใน `internal/evidence/w0/` เมื่อ validation จบ
- ยังไม่มี executable sample, dataset generator, runtime conformance, benchmark, hosted CI run หรือ production proof ของ Engine

## สถานะงานและทางเดินต่อ

งาน #2 architecture/requirements, #4 reference decision study และ #21 predeclared test strategy ส่งมอบในขอบเขต W0 document selection ได้ ส่วน #3 ยังต้อง SDK/artifact/driver qualification และ #23 ยังต้องขยาย synchronization เป็น reviewed bidirectional workflow กับ metadata update/migration coverage จึงไม่ปิดสองงานนี้จากการเลือก provider เพียงอย่างเดียว

หลังตรวจเอกสารและ live readback: #2/#4/#21 ปิดเป็น Done/Test Passed สำหรับงานเอกสารรอบนี้แล้ว #3/#23 ยังเปิดอยู่ จึงยังไม่ปิด W0 milestone ผลตรวจอยู่ใน [W0 validation](../evidence/w0/validation.json) และ [offline tracking tests](../evidence/w0/tracking-tool-tests.json) ทั้งสองส่วนไม่ใช่ runtime test/benchmark/CI proof

ก่อนเริ่ม Core/provider implementation ให้ปิด qualification ที่เป็น dependency ของงานนั้น ระบุ image/binary/package locks, actual supported OS, fixture/gold hashes และคำสั่งรันทดสอบ ห้ามนำ metadata checks ในรอบนี้ไปอ้างว่า .NET11/provider/E2E หรือ benchmark ผ่านแล้ว
