# ADR-0002 — Small API: minimal host และ optional GraphQL

- วันที่: 2026-10-27 (Asia/Bangkok)
- สถานะ: **Accepted for W0 planning; implementation qualification pending**
- Maturity ที่สังเกตได้: **M0** ไม่มี restore/build/runtime/benchmark proof ใน ADR นี้
- งานที่เกี่ยวข้อง: Engine #2, #3, #5, #6, #9, #11 และ #21
- Protocol: [Small API workload](../validation/small-api-workload.md)

## บริบทและเป้าหมาย

Sample นี้ต้องพิสูจน์ว่าผู้ใช้ขนาดเล็กเริ่มจาก API อย่างเดียวได้ โดยไม่มีฐานข้อมูล, broker, Worker, GraphQL หรือ AI ที่ไม่ได้เลือกทำงาน และเปิด transport เพิ่มให้ business operation เดิมผ่าน config ได้ภายหลัง ขอบเขตนี้เป็น public synthetic catalog สำหรับทดสอบ Engine ไม่ใช่ SaaS ที่มีข้อมูลจริงหรือ durability requirement

## การตัดสินใจ

| ส่วน | เลือกใน W0 | ขอบเขตและเหตุผล |
| --- | --- | --- |
| Platform candidate | SDK `11.0.100-rc.3.26522.148`; .NET/ASP.NET Core runtime `11.0.0-rc.3.26522.148` | หน้า download ทางการระบุ exact versions นี้ [S1]; ต้องตรวจ distribution/checksum และ build จริงใน #3 ก่อนถือว่า qualified |
| Host/server | ASP.NET Core `WebApplication` + Kestrel, Linux x64 เป็น performance reference | ใช้ server ของ platform โดยตรง ไม่มี reverse proxy/service mesh ใน first proof; Windows x64 เป็น functional compatibility target แยก |
| Transport เริ่มต้น | HTTP JSON ผ่าน Minimal API adapter; TLS 1.3 และ keep-alive ใน reference protocol | Business contracts ไม่รับ HttpContext; API adapter เป็นผู้ map wire/result/cancellation |
| State provider | Bounded in-memory fixture store ของ Sample ใช้ BCL collection และ atomic update ที่ระบุไว้ | ไม่ใช้ EF InMemory, SQLite หรือ external database และไม่เรียก fixture นี้ว่า durable database/cache provider |
| Optional transport | Hot Chocolate HTTP GraphQL candidate `HotChocolate.AspNetCore` **16.7.1** | NuGet metadata แสดง net11.0 dependency group [S4]; ยังไม่ใช่หลักฐานว่า restore/build/runtime บน RC3 ผ่าน ต้องล็อก transitive dependencies และทดสอบ |
| Telemetry | Built-in Activity/Meter และ process/resource capture เฉพาะที่ protocol ระบุ | Exporter network ปิดใน minimal baseline; ไม่เพิ่ม collector process ให้ sample จำเป็นต้องพึ่ง |
| Identity/tenancy | ไม่มี external IdP ใน profile นี้; synthetic public catalog ภายใน isolated test network | ไม่อ้าง authn/tenant proof จาก sample นี้ งาน identity และ tenant isolation ต้องผ่าน Business/AI profiles และ adapter conformance ที่เกี่ยวข้อง |

SDK candidate อ่านจากแหล่งทางการ ณ 2026-10-27; ไม่ติดตั้ง SDK หรือแก้ global runtime ในรอบตัดสินใจนี้ Microsoft ประกาศ RC3 เมื่อ 2026-10-25 พร้อม security fixes และแนะนำ RC2 users อัปเดต [S2] การใช้ go-live release ไม่ทำให้ Engine หรือ third-party adapters ได้รับการรับรองโดยอัตโนมัติ

## Profiles และ activation boundary

- `small-api`: API เปิด, GraphQL/Worker/database/cache/broker/AI/retrieval ปิด เป็น default ของ lane
- `small-api-graphql`: API + GraphQL HTTP เปิด ใช้ `GetItem`, `ListItems`, `SetLabel` handlers/contracts เดิม ไม่มี WebSocket/subscription/IDE activation
- การสลับ profile เกิดตอน startup และ restart/redeploy; live reconfiguration ไม่อยู่ในสัญญาแรก
- Config ที่ปิด GraphQL ต้องข้าม GraphQL registration, schema build, request executor creation, hosted services และ endpoint mapping ทั้งหมด ตรวจด้วย activation probes ไม่ใช้เพียง HTTP 404 เป็นหลักฐาน
- เอกสาร migration ของ Hot Chocolate v16 ระบุ eager schema/executor initialization ตอน startup [S5] จึงห้ามเรียก registration แล้วหวังว่าการไม่ map endpoint จะเพียงพอ
- ใน opt-in profile ใช้เฉพาะ HTTP endpoint behavior ที่ต้องการ ปิด schema download/IDE/multipart/batching/WebSocket และกำหนด cost/depth/request limits ชัดเจน ตรวจ API ที่มีจริงใน package version ที่ล็อกก่อนลงมือ เอกสาร endpoints มีตัวเลือกแยก HTTP, WebSocket, schema และ IDE [S6]
- Meta-package HotChocolate.AspNetCore มี Nitro และ transport packages เป็น dependencies [S4] ต้องตรวจ license/transitive graph และประเมิน minimal package composition ก่อน release ไม่เปิด Nitro cloud/telemetry เพียงเพราะ dependency ถูกติดตั้ง
- คำว่า zero activation ครอบคลุมงานของโมดูลที่ปิด ไม่รับรองว่า byte ของ dependency หายจาก publish output หรือ assembly ไม่ถูกโหลดจนกว่าจะมีการวัดแยก

ชื่อ profile ข้างต้นเป็น design identifiers; ยังไม่ใช่ executable appsettings schema ที่เผยแพร่แล้ว

## Business fixture ที่ใช้ร่วมกัน

เลือก catalog 10,000 records: GetItem, ListItems และ SetLabel เป็น operations ที่มี input/output/error/cancellation contract เดียว REST กับ GraphQL ต้อง map business outcome ให้ตรงกัน แต่ HTTP status กับ GraphQL error envelope ไม่จำเป็นต้องเหมือนกันแบบ byte-for-byte

In-memory store ต้องมี bounded key set และ compare-and-swap/lock ที่ทำให้ revision update เป็น atomic การมี ConcurrentDictionary ไม่ได้ทำให้ read-modify-write ทั้งชุด atomic โดยอัตโนมัติ ประกาศ state reset และไม่มี data retention หลัง restart อย่างชัดเจน

## ทางเลือกที่พิจารณา

| ทางเลือก | ข้อดี | เหตุผลที่ไม่เลือกเป็น default นี้ |
| --- | --- | --- |
| MVC/controllers | เหมาะกับ richer conventions และ filter/model binding | Small API proof เริ่มจาก minimal transport adapter ได้; ไม่ห้าม controller adapter ภายหลัง |
| SQLite file database | มี persistent relational behavior ในเครื่อง | เพิ่ม SQL semantics/migrations/locking ที่ไม่จำเป็นต่อ zero-activation proof; ให้ data/provider proof อยู่ใน lane ที่ต้องใช้ |
| EF Core InMemory | Bootstrap ตัวอย่าง data access ได้ง่าย | ไม่ต้องใช้ ORM และไม่ควรสับสนกับ real relational provider conformance |
| GraphQL เปิดทุกครั้ง | เริ่ม API+GraphQL ได้ทันที | ไม่ตรง requirement ที่ API-only ต้องไม่เปิด GraphQL ที่ไม่ได้เลือก |
| Dapr/Orleans/sidecar | มี distributed capabilities สำหรับ workload ที่เหมาะ | เพิ่ม lifecycle/process/dependency ใน minimal profile; ศึกษาใน distributed profile แยก |
| เขียน GraphQL executor เอง | ควบคุม dependency graph ได้ | ขอบเขต protocol implementation ใหญ่โดยไม่มี requirement รองรับ; ใช้ mature provider หลัง qualification |

## เกณฑ์รับและผลกระทบ

ต้องผ่าน protocol ที่ลิงก์ไว้ ทั้ง correctness, disabled-module activation, cancellation, input limits, REST/GraphQL parity และ baseline-relative resource/latency gates ก่อนยก maturity ของ profile ที่ทดสอบจริง ตัวเลขใน protocol เป็น engineering budgets ที่ประกาศล่วงหน้า ไม่ใช่ measured capacity

ข้อแลกเปลี่ยน: profile นี้ใช้ข้อมูล synthetic และไม่มี distributed durability/authentication/tenant guarantee จึงแสดง minimal host overhead ได้ชัด แต่ใช้แทน Business/AI E2E proof ไม่ได้ ต้องรัน security/isolation checks ของ contracts ที่เพิ่มภายหลังใหม่

## สิ่งที่ต้อง qualified ก่อน implementation claim

1. ตรวจ SDK checksum, OS support, exact runtime และ reproducible build บน Linux/Windows ที่เลือก
2. Restore/build/license/transitive-dependency qualification ของ Hot Chocolate 16.7.1 บน exact RC3; package metadata เป็นเพียง evidence ของ declared target
3. ตรวจ HTTP-only mapping, eager initialization suppression และ security defaults กับ source/version ที่ล็อก ไม่อ้างเอกสาร current ว่า behavior ของ pinned package ตรงกันทุกบรรทัด
4. Freeze fixture generator, driver version, OS/container digest, CPU allocation และ TLS settings ก่อน benchmark ชุดแรก

## แหล่งข้อมูล

ตรวจอ่าน 2026-10-27 ข้อเสนอและ budgets ใน ADR นี้เป็นการตัดสินใจของโครงการ ไม่ใช่ performance claims ของแหล่งข้อมูล

- S1: [Microsoft .NET 11 downloads](https://dotnet.microsoft.com/en-us/download/dotnet/11.0) — exact RC3 SDK/runtime candidate
- S2: [Microsoft October 2026 OOB update](https://devblogs.microsoft.com/dotnet/dotnet-october-2026-oob-security-updates/) — RC3 security release
- S3: [Kestrel overview](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/servers/kestrel?view=aspnetcore-10.0&preserve-view=true), [Generic Host](https://learn.microsoft.com/en-us/dotnet/core/extensions/generic-host), [Minimal APIs](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/minimal-apis?view=aspnetcore-10.0) — architecture background; exact net11 behavior still requires qualification
- S4: [HotChocolate.AspNetCore 16.7.1](https://www.nuget.org/packages/HotChocolate.AspNetCore/16.7.1) — package metadata and transitive dependency groups
- S5: [Hot Chocolate v16 migration](https://chillicream.com/docs/hotchocolate/migrating/migrate-from-15-to-16) — eager initialization change
- S6: [Hot Chocolate endpoints](https://chillicream.com/docs/hotchocolate/server/endpoints) — separate HTTP/IDE/schema/WebSocket mappings
