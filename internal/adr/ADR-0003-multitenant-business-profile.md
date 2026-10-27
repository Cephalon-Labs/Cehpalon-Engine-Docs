# ADR-0003 — ชุดเริ่มต้นสำหรับ Multitenant business Sample

- วันที่: 2026-10-27 (Asia/Bangkok)
- สถานะ: **Accepted for W0 planning; implementation qualification pending**
- ระดับที่สังเกตได้: **M0** ทุก provider/profile ในเอกสารนี้
- งานที่เกี่ยวข้อง: Engine #2, #3, #7, #8, #12, #13, #14, #15, #21
- คู่เอกสาร: [workload และเกณฑ์ตรวจรับ](../validation/business-workload.md)

Qualification update: [SDK/driver/artifact results](../planning/w0-qualification-and-sync.md) include actual images/OS/Java/Erlang, real PostgreSQL and RabbitMQ client smoke and owned-fixture cleanup. They do not establish RLS/tenant/outbox/inbox/HA/business workflow or this workload's acceptance gates.

## บริบทและคำตัดสิน

เลือกธุรกิจตัวอย่าง **คำสั่งซื้อและการจองสินค้าแยกตาม tenant** เพื่อพิสูจน์ API → SQL transaction/outbox → broker → Worker/inbox → สถานะคำสั่งซื้อ และใช้ handlers/contracts เดิมใน profile ที่ประกาศรองรับ ผู้ใช้เลือก lane นี้พร้อม Small API และ AI/Retrieval จึงเลือก infrastructure ที่ใช้ร่วมกันได้โดยไม่บังคับให้ทุก lane ต้องเปิดทั้งหมด

ใช้ **PostgreSQL + Npgsql แบบ async ADO.NET, RabbitMQ, Keycloak** เป็นชุดแรก เลือก cache เป็น **ปิดโดยค่าเริ่มต้น** และเตรียม Valkey เป็น profile เพิ่มเมื่อถึงงาน cache การเลือกนี้เป็นคำตัดสินด้านแผนตามที่ผู้ใช้มอบหมาย ยังไม่ใช่ผล restore/build/E2E หรือการรับรองจากผู้ขาย

| ส่วน | Candidate ที่เลือกจากแหล่งทางการ ณ วันที่ตรวจ | เหตุผลและข้อจำกัด |
| --- | --- | --- |
| SQL | PostgreSQL **18.6** | สาย 18 ยังอยู่ในช่วง support ตามตารางทางการถึง 2030-11-14; ใช้ transaction, constraints และ row-level security เป็นขอบเขตพิสูจน์แรก ไม่เลือก 19 RC เป็นฐานข้อมูลเริ่มต้น [S1] |
| Driver | **Npgsql 10.0.3**, ใช้ async ADO.NET โดยตรง | NuGet แสดง assets สำหรับ net8.0/net9.0/net10.0; ใช้เป็น candidate สำหรับ net11.0 ต้อง restore/build/run กับ RC3 จริงก่อนอ้าง compatibility ไม่อนุมานจาก computed TFM [S2–S3] |
| Broker | RabbitMQ **4.4.0**, AMQP 0-9-1 | มี release 2026-10-20 และ community support ตามตารางถึง 2027-07-31; ใช้ publisher confirms, manual consumer acknowledgements และ durable quorum queues การรับรอง HA ต้องมี profile สาม broker แยกจาก single-node proof [S4–S6] |
| Broker client | **RabbitMQ.Client 7.2.2** | NuGet แสดง net8.0 และ netstandard2.0; .NET 11 RC3 restore/runtime/TLS/recovery ยังต้อง qualify [S7] |
| Identity | **Keycloak 26.8.1** | Release 2026-10-13; ใช้ OIDC discovery/JWKS และ JWT access tokens ผ่านมาตรฐาน ไม่ใส่ Java/server SDK ใน Core [S8–S9] |
| Cache เพิ่มเติม | **Valkey 9.1.3** เป็น optional candidate; **ไม่เปิดในฐานแรก** | Official releases ระบุ 2026-10-26; version นี้ไม่ใช่ 9.2 RC ใช้ cache catalog/query เท่านั้น ไม่ใช้ตัดสิน stock, tenant หรือ authorization [S10] |

ไม่เพิ่ม ORM เป็น dependency บังคับใน slice แรก เพื่อไม่ผูกกำหนดส่งกับการออก provider major ใหม่ของ EF Core งาน EF Core adapter ต้องมี qualification แยกตาม major ของ EF/provider และ contract ที่ประกาศ ไม่ถือว่า ADO.NET proof รับรอง ORM proof

## โครงสร้างและ semantics ที่เลือก

- หนึ่ง PostgreSQL database สำหรับ business data แบบ shared tables ที่ทุก tenant-owned primary/unique/foreign key มี tenant scope; ใส่ explicit application filter และ RLS เป็น defense in depth
- Role ที่ runtime ใช้ไม่เป็น superuser, ไม่เป็นเจ้าของ table และไม่มี BYPASSRLS; migration role แยกจาก runtime ใช้ tenant session context ภายใน transaction และต้อง reset ได้เมื่อคืน pooled connection การมี RLS ไม่ทดแทน trusted tenant resolution [S11]
- User tenant มาจาก validated identity และ membership policy ที่ตรวจแล้ว ไม่เชื่อ tenant header/body เอง หนึ่ง Keycloak realm ใช้ test tenants หลายรายเพื่อพิสูจน์ application isolation ไม่อ้างว่า realm เท่ากับ tenant
- API `PlaceOrder` commit order + outbox ใน transaction เดียว แล้วตอบ accepted พร้อม order ID/idempotency key; Worker commit inbox marker + stock reservation + order transition + derived outbox ใน transaction เดียว
- Event contract มี immutable tenant ID, event ID, aggregate ID, aggregate version, schema version และ trace context ไม่ส่ง bearer token/secret ไปใน event Worker ใช้ service identity และตรวจ envelope/tenant scope ของตนเอง
- Delivery เป็น **at-least-once + duplicate-safe business effects**; unique inbox และ idempotency constraints เป็นส่วนหนึ่งของ proof ไม่ใช้คำว่า exactly-once ทั้งระบบ Publisher confirm ไม่ใช่หลักฐานว่า consumer transaction สำเร็จ [S5]
- Ordering รับรองเฉพาะ state transition/version ของ order แต่ละรายการ ไม่รับรอง global FIFO ข้าม queues, workers หรือการ redelivery; stale/out-of-order events ต้องถูกตรวจและทำให้ลู่เข้าสู่สถานะที่ถูกต้องตามสัญญาที่จะกำหนด
- Profile เริ่มต้นแยก API และ Worker เป็น processes โดยใช้ contracts เดียวกัน Profile unified process ต้องใช้ handlers และ conformance suite เดิม พร้อม event dispatcher ที่รักษาขอบเขต durability ที่ระบุ ไม่แปลง durable event เป็น fire-and-forget เงียบ ๆ
- API-only config ต้องไม่มี Worker, broker connection หรือ cache activation ถ้าไม่มีโมดูลอื่นต้องใช้สิ่งนั้น Profile business เปิดเฉพาะ dependencies ที่ระบุไว้ใน immutable composition plan

## Resource profiles และการทำซ้ำ

Reference target เป็น Linux x64 ตามมาตรฐานกลางที่ primary จะสรุป สำหรับ workload นี้กำหนด app budget รวม **2 dedicated vCPU / 2 GiB** แบ่ง API 1 vCPU/1 GiB และ Worker 1 vCPU/1 GiB Infrastructure และ load generator อยู่คนละ resource budget ไม่รันแข่งกับ app ภายใน limit เดียวกัน

- `business-single-broker`: PostgreSQL 2 vCPU/4 GiB, RabbitMQ 1 node 2 vCPU/2 GiB, Keycloak 2 vCPU/2 GiB; durable queue replica เดียว พิสูจน์ restart/replay แต่ไม่ใช่ broker-node failover
- `business-ha-broker`: quorum queue สามสมาชิกบนสาม broker คนละ failure boundary เพื่อพิสูจน์สูญเสียหนึ่ง node/leader; กำหนด Erlang/image/resource/network/storage pins ก่อนรัน มี gate แยกจาก baseline
- Load generator แยกอย่างน้อย 2 vCPU/2 GiB พร้อม time synchronization และเครื่องมือที่บันทึก offered/completed/dropped requests ได้
- ใช้ development containers/Compose ภายในเครื่องหรือ CI ที่มีอยู่ ไม่ provision cloud, paid service, credentials หรือ commercial support ใน W0

ตัวเลข resource เป็น **เงื่อนไขทดสอบที่เลือก** ไม่ใช่ minimum requirements ของผู้ขายหรือผลวัด capacity หากเครื่องไม่ครบให้ gate เป็น Not run/Blocked ตามสาเหตุ ไม่อ้างผลบน resource อื่นว่าเทียบเท่ากัน

## ทางเลือกที่พิจารณา

| ทางเลือก | คำตัดสินสำหรับ slice แรก |
| --- | --- |
| SQL Server | เก็บเป็น second-provider conformance ในอนาคต เพื่อพิสูจน์ portability; ไม่เพิ่ม provider สองตัวก่อนเส้นทาง transaction/outbox แรกชัดเจน |
| SQLite หรือ in-memory SQL substitute | ใช้ fixture/component tests ได้ตามข้อจำกัด แต่ไม่ใช้แทน PostgreSQL จริงใน durable/concurrency/RLS proof |
| PostgreSQL outbox polling โดยไม่มี broker | เป็น topology เพิ่มได้เมื่อรักษาสัญญา แต่ไม่ทำให้ผ่านงาน RabbitMQ delivery/recovery/scale-out |
| Kafka | เลื่อนไปเมื่อมี replay/log-stream workload ที่ระบุชัด; lane แรกต้องพิสูจน์ command/event queue และ recovery ให้ครบก่อนเพิ่มอีก abstraction |
| Managed identity/broker/database | ไม่เลือกเป็น first proof เพราะต้องมีบัญชี/สิทธิ์/infra ภายนอกและอาจมีค่าใช้จ่าย; self-hosted proof ก็ไม่รับรอง managed service |
| เปิด cache ตั้งแต่ต้น | ปิดเพื่อให้ correctness ของ stock/order ไม่พึ่ง invalidation; เพิ่ม Valkey หลังวัด baseline และมี tenant-key/conformance tests |

## License และ maintenance boundary

PostgreSQL และ Npgsql ใช้ PostgreSQL license; RabbitMQ server/core plugins ใช้ MPL-2.0 และ client เปิดให้เลือก Apache-2.0 หรือ MPL-2.0; เลือก Apache-2.0 สำหรับ client dependency inventory; Keycloak ใช้ Apache-2.0; Valkey COPYING ระบุ BSD-3-Clause [S2,S7,S12–S15] นี่เป็น inventory จาก upstream ไม่ใช่การเปลี่ยน license ของ Engine/Docs/Samples ซึ่งคง MIT และไม่ใช่การรับรองว่าทุก transitive artifact ใช้ license เดียวกัน ต้องสร้าง SBOM/license notices จาก artifacts จริงก่อน distribution

ก่อน qualification ต้องตรวจ current advisories, exact package/image digests, Erlang/Java/base-image versions และ licenses ของ dependencies ทั้งหมด ล็อก artifacts ที่ตรวจแล้วโดยไม่ใช้ floating `latest` PostgreSQL/RabbitMQ มี support dates ที่แหล่งทางการแสดง; ไม่แต่ง support window ให้ Npgsql/Keycloak/Valkey ที่ไม่ได้รับรองในแหล่งที่อ่าน และไม่อ้าง commercial LTS โดยไม่มีสัญญา

## งานที่ยังขวางการรับรอง implementation

1. Qualify SDK .NET 11 RC3 และ restore graph ของ Npgsql/RabbitMQ.Client กับจริง; TFM metadata ยังไม่ใช่ runtime proof
2. ล็อก container digests และ Erlang/Java/base-image compatibility; ยังไม่ได้ดึงหรือติดตั้ง artifacts ใน W0 รอบนี้
3. กำหนด schemas/migrations, membership policy, event state machine และ signed/trusted envelope boundary ใน implementation ADR/contract
4. เลือกและ pin .NET cache client ก่อนเปิด optional Valkey; การเลือก server ไม่ได้พิสูจน์ protocol/feature compatibility ของ client
5. รัน correctness/security/recovery และ benchmark ตาม [protocol](../validation/business-workload.md) จาก Engine revision ที่ระบุ ไม่มีผลรันใน ADR นี้

## แหล่งทางการที่ตรวจ 2026-10-27

- S1: [PostgreSQL versioning/support](https://www.postgresql.org/support/versioning/)
- S2: [Npgsql 10.0.3 package metadata](https://www.nuget.org/packages/Npgsql/10.0.3)
- S3: [Npgsql 10 release notes](https://www.npgsql.org/doc/release-notes/10.0.html)
- S4: [RabbitMQ release/support information](https://www.rabbitmq.com/release-information)
- S5: [Publisher confirms and consumer acknowledgements](https://www.rabbitmq.com/docs/confirms)
- S6: [Quorum queues](https://www.rabbitmq.com/docs/quorum-queues)
- S7: [RabbitMQ.Client 7.2.2 metadata](https://www.nuget.org/packages/RabbitMQ.Client/7.2.2)
- S8: [Keycloak 26.8.1 release](https://www.keycloak.org/2026/10/keycloak-2681-released)
- S9: [Keycloak OIDC endpoints](https://www.keycloak.org/securing-apps/oidc-layers)
- S10: [Valkey releases](https://valkey.io/download/releases/)
- S11: [PostgreSQL 18 row security](https://www.postgresql.org/docs/18/ddl-rowsecurity.html)
- S12: [PostgreSQL license](https://www.postgresql.org/about/licence/)
- S13: [RabbitMQ 4.4.0 license](https://raw.githubusercontent.com/rabbitmq/rabbitmq-server/v4.4.0/LICENSE)
- S14: [Keycloak license](https://github.com/keycloak/keycloak#license)
- S15: [Valkey 9.1.3 COPYING](https://github.com/valkey-io/valkey/blob/9.1.3/COPYING)
