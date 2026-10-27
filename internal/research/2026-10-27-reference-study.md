# การศึกษาอ้างอิงและข้อเสนอสถาปัตยกรรมเบื้องต้น

วันที่ตรวจแหล่งข้อมูล: **2026-10-27**

สถานะ: **อ่านเอกสารทางการเบื้องต้นและคัดหัวข้อศึกษาต่อ** ยังไม่มีการติดตั้ง ทดสอบ integration, benchmark หรือพิสูจน์ความพร้อมใช้งานจริงจากการศึกษานี้ เอกสารนี้เป็นข้อเสนอสำหรับโครงการใหม่ ไม่ใช่รายงานสถานะ implementation เดิม

การเลือกเวอร์ชัน .NET 11/12, SDK, dependency และ support policy ให้ยึดผลตรวจสอบแพลตฟอร์มและการตัดสินใจที่ผู้รับผิดชอบโครงการบันทึกแยกต่างหาก เอกสารนี้ไม่ประกาศว่า packages ที่อ้างอิงรองรับ .NET รุ่นใดแล้ว

## ข้อกำหนดจากผู้ใช้และขอบเขตข้อเสนอ

ข้อกำหนดจากผู้ใช้:

- แยก Engine, Docs และ Samples เป็นสาม repositories
- นักพัฒนาเขียน business logic ครั้งเดียว และเลือกโมดูล, topology, pattern, transport และ architecture ผ่าน config เท่าที่ชุดความสามารถรองรับ
- API-only ต้องไม่เริ่ม GraphQL, Worker หรือ provider ที่ไม่ได้เลือก
- รองรับงานตัวอย่างทั้งสามสาย: API ขนาดเล็ก; business application หลาย tenant ที่มี API + Worker + SQL; AI/Agent + Retrieval
- ออกแบบให้เพิ่ม provider และ deployment targets ได้ พร้อมหลักฐานด้านคุณภาพ ความปลอดภัยและ performance

ข้อเสนอในเอกสารนี้ต้องแยกจากขอบเขตที่อนุมัติให้ implementation แล้ว คำว่า “รองรับทุกอย่าง”, “เหนือกว่าทุก framework” และ “ใช้งานได้อีก 30–50 ปี” เป็นทิศทางระยะยาว ซึ่งควรแปลงเป็นรายการความสามารถ เกณฑ์เปรียบเทียบ และนโยบายวิวัฒนาการที่ตรวจสอบได้

## แนวทางแกนกลางและขอบเขตโมดูล

เสนอ **แกนเล็ก + โมดูลเลือกใช้ + ตารางความสามารถที่พิสูจน์แล้ว** โดยให้ config เลือกเฉพาะชุดที่เข้ากันได้:

| ส่วน | หน้าที่ | ขอบเขตที่เสนอ |
|---|---|---|
| Core | operation contracts, dispatch, result/error model, cancellation, capability descriptors และ composition plan | ไม่พึ่งเว็บ, host, database หรือ SDK ของ provider |
| Application | business handlers, validation และ policies | ไม่รับ `HttpContext`, GraphQL context หรือ broker delivery object โดยตรง |
| Adapters | API, GraphQL, gRPC, JSON-RPC, SSE, Worker, data, cache, identity, event broker และ AI provider | แยก package และ conformance suite; รายงาน capability และข้อจำกัดชัดเจน |
| Composition | schema, dependencies, profiles, exposures และ activation bindings | อ่าน config → ตรวจทั้งหมด → สร้างแผน immutable → เปิดเฉพาะสิ่งที่เลือก |
| Hosting / Operations | startup, shutdown, health, telemetry, deployment integration | แยกจาก business logic; ผูกกับ platform ผ่าน adapters |

Generic Host ของ .NET จัดการ DI, logging, configuration และ lifetime และจะเริ่ม hosted services ที่ลงทะเบียนไว้ จึงควรพิสูจน์การไม่ลงทะเบียน/ไม่เริ่ม Worker ที่ปิดอยู่ รวมถึงไม่มี constructor, connection, endpoint และ background work ของโมดูลที่ปิด [S1]

หาก config เลือกความสามารถที่ใช้ร่วมกันไม่ได้ เสนอให้ล้มเหลวพร้อมเหตุผลก่อนเริ่ม side effects โดยแสดงว่าโมดูลใดเปิด/ปิดและเพราะเหตุใด ห้ามแอบเปลี่ยนไปใช้ provider หรือ guarantee ที่อ่อนลง

## ตารางอ้างอิงจาก ecosystem

คุณสมบัติในคอลัมน์แรกอ้างจากเอกสารที่อ่าน ส่วนประโยชน์ ข้อแลกเปลี่ยน และสิ่งที่เสนอให้ Engine รับหรือหลีกเลี่ยงเป็นการวิเคราะห์ของโครงการ ตารางนี้ไม่มีผล benchmark และไม่ใช่การประเมิน ecosystem แบบครบถ้วน

| กลุ่มอ้างอิง / feature-function | ประโยชน์ที่นำมาศึกษา | ข้อแลกเปลี่ยน / ขอบเขต | ข้อเสนอสำหรับ Engine |
|---|---|---|---|
| .NET built-ins / Aspire / Orleans: Generic Host; AppHost และ dashboard; virtual actors/grains, placement, state และ lifecycle [S1–S3] | ตัวอย่างแยก host, การประกอบทรัพยากร และ programming model สำหรับ state แบบกระจาย | แต่ละส่วนแก้คนละปัญหา; การบังคับทุก handler ให้เป็น grain เพิ่มข้อกำหนดต่อ programming model | ใช้ built-ins เป็นฐาน; ทดลอง Aspire ใน Samples/DevOps; พิจารณา Orleans adapter เฉพาะ workload ที่เหมาะ ไม่ฝังใน Core |
| Dapr: HTTP/gRPC building blocks สำหรับ invocation, pub/sub, state, workflow และ components [S4] | ตัวอย่าง API กลางที่แยก provider implementations | มี runtime/sidecar เพิ่มในเส้นทางทำงาน; API กลางไม่ได้ทำให้ guarantees ของ providers เท่ากัน; บาง API ในเอกสารมีสถานะ alpha | ศึกษา capability descriptors และ conformance; ให้ Dapr เป็น adapter ทางเลือก; พิสูจน์ failure behavior ราย provider |
| Spring Boot: starters และ conditional auto-configuration ตาม class, bean, property และ app type [S5] | ลด bootstrap code และเปิดฟังก์ชันตามบริบท; ผู้ใช้ override defaults ได้ | เอกสารเตือนเรื่องลำดับประเมิน conditions และ bean ที่เริ่มเร็วเกินไป | รับแนวคิด defaults ที่ override ได้; แสดงเหตุผลการเปิด/ปิด; ตรวจ composition plan ก่อน activation |
| Quarkus: build-time DI, unused-bean removal และ build profile/property conditions [S6] | ตัวอย่าง dependency reachability และการลดสิ่งที่ไม่ใช้ | Dynamic lookup อาจทำให้ตัด bean ที่ยังใช้จริง; build-time choices มีขอบเขตต่างจาก runtime choices | แยก build-time / startup / runtime config; ทดลอง generated graph และตรวจว่าการตัดโมดูลไม่ทำให้ lookup เสีย |
| NestJS: feature modules, imports/exports และ provider encapsulation [S7] | ขอบเขตโมดูลชัด; exported providers เป็น public interface | ยังต้องตรวจ dependency graph และ lifetime; module boundary ไม่ใช่ process isolation | ใช้ explicit exports และตรวจ dependency cycles; หลีกเลี่ยง global registration ที่ทำให้โมดูลเห็นกันทั้งหมด |
| FastAPI / Go: type-based validation, OpenAPI/JSON Schema และ codegen; interfaces เล็กที่แทนพฤติกรรมเฉพาะ [S8–S9] | ลดข้อมูลซ้ำระหว่าง contracts, validation, docs และ client; รักษา abstraction ให้เล็ก | Schema generation ต้องมี wire semantics; interface เล็กไม่ได้รับประกัน portability; Effective Go เป็นเอกสารเก่าที่ไม่ครอบคลุม ecosystem รุ่นใหม่ทั้งหมด | ทดลองสร้าง transport schemas จาก operation contracts พร้อม escape hatch; แยก ports ตาม capability แทน universal interface ขนาดใหญ่ |

ลำดับศึกษาต่อที่เสนอ: **.NET composition และ Spring/Quarkus activation rules → NestJS module boundaries → FastAPI schema/codegen → Dapr/Orleans สำหรับ distributed profiles** ก่อนเลือกใช้ต้องกำหนด version, workload, host และ acceptance tests

## ขอบเขตของ portability

“เขียน business logic ครั้งเดียว” ควรเป็นสัญญาที่มีขอบเขต: ใช้ handler และ policy ร่วมกันผ่าน adapters ที่ผ่าน conformance แต่ไม่รับประกันว่าเปลี่ยน config แล้วทุก topology, protocol และ database จะมี semantics เหมือนกัน

| สิ่งที่เปลี่ยน | สิ่งที่ตั้งเป้าใช้ร่วมกัน | สิ่งที่ยังต้องออกแบบหรือพิสูจน์ |
|---|---|---|
| API ↔ gRPC ↔ GraphQL | business operation, validation และ policy | schema, serialization, error mapping, pagination, deadlines และ streaming |
| Single process ↔ Distributed | handler ที่ไม่พึ่ง process-local state | network failure, cancellation propagation, retries, idempotency, consistency และ compatibility |
| SQL ↔ Document / Key-value | application ports ภายใน capability ที่ประกาศ | query semantics, transactions, indexes, concurrency และ migration |
| Server ↔ Serverless / Edge | logic ที่ไม่พึ่ง host-specific facilities | lifetime, cold start, memory, filesystem, streaming และ background-work constraints |
| AI provider ↔ AI provider | task contract และผลลัพธ์ที่ตรวจ schema ได้ | tool behavior, structured outputs, context/token limits, model capability, cancellation และค่าใช้จ่าย |

gRPC กับ HTTP/JSON มีจุดเด่นและข้อจำกัดต่างกัน จึงควรมี protocol mapping ที่ตรวจสอบได้ [S10] EF Core providers ต้องตรวจ compatibility รายตัว และ migrations หลาย provider ต้องดูแลเป็นหลายชุด [S11–S12]

สำหรับ eventing เสนอให้แยก delivery guarantee, ordering scope, retry policy, deduplication และ transaction boundary เป็น capabilities ห้ามอนุมาน exactly-once ทั้งระบบจาก happy path หรือ guarantee ของ broker เพียงส่วนเดียว Outbox และ consumer ที่จัดการข้อความซ้ำได้เป็นหัวข้อพิสูจน์สำคัญเมื่อ database commit และ event publication อยู่คนละระบบ [S13]

## Kernel, operating system และ servers

ข้อเสนอขอบเขตการศึกษา: ศึกษาว่า OS scheduling, process/container isolation, memory/GC, filesystem, sockets, TLS, I/O, service lifetime และ resource limits ส่งผลต่อ Engine อย่างไร แล้วกำหนด host capability contracts และ tests ที่เกี่ยวข้อง

“Kernel” ใน Engine ควรนิยามเป็น application core ที่มีหน้าที่จำกัด การสร้าง operating system kernel, HTTP server, cryptography stack, container scheduler หรือ database engine ของเราเองเป็นงานคนละระดับ เสนอให้ยังอยู่นอก implementation ระยะแรก เว้นแต่มี requirement และหลักฐานว่าฐานที่มีอยู่แก้ไม่ได้ การเลือก Kestrel/reverse proxy/container/Kubernetes ควรอยู่ใน deployment profiles และ integration tests ตามเป้าหมายที่เลือกจริง

รายการ OS/server ข้างต้นเป็นขอบเขตศึกษาต่อ ยังไม่มีการตรวจ implementation หรือทำ benchmark ระบบปฏิบัติการและ server ในการศึกษาครั้งนี้

## สามสาย Samples และหลักฐานที่ต้องวางแผน

| สายตัวอย่างที่ผู้ใช้เลือก | เส้นทางพิสูจน์ที่เสนอ | หลักฐานสำคัญ |
|---|---|---|
| Small API | operation หนึ่งชุดผ่าน API-only | bootstrap code, startup/idle overhead, error/validation/cancellation; GraphQL/Worker/providers ที่ปิดทำงานเป็นศูนย์ |
| Multitenant business API + Worker + SQL | tenant-scoped command/query → SQL → event/outbox → Worker | tenant isolation, authorization, transaction boundary, duplicate/crash recovery, queue backlog และ observability |
| AI / Agent + Retrieval | query → retrieval → model/tool loop → validated response | tenant-aware retrieval, tool authorization, secret isolation, prompt/tool boundaries, cancellation, quotas และ provider failure; ใช้ fixtures เป็นฐานและแยกจากผล provider จริง |

เสนอให้สร้างโครงทั้งสามสายตั้งแต่เริ่ม และส่งมอบเป็น slice ที่ทดสอบได้ โดยมี Core/composition ร่วมกัน แต่แต่ละสายมี acceptance criteria และ maturity ของตนเอง การมี folder หรือ descriptor ยังไม่ถือว่าทำงานได้

## ลำดับ proof slices ที่เสนอ

1. **Config และ zero activation:** API-only, API+GraphQL และ Worker-only; disabled modules ไม่มี factory/constructor, connection, endpoint หรือ background work
2. **Business portability:** operation เดียวผ่านสอง transports ให้ business result, tenant authorization, validation และ cancellation ตรงตาม contract
3. **Distribution:** local และ remote adapters พร้อม timeout, retry, duplicate, crash และ mixed-version checks
4. **Durable eventing:** database/outbox commit, consumer deduplication, poison messages, ordering scope และ recovery หลัง restart
5. **Provider conformance:** เลือก SQL, cache, broker, identity และ AI/retrieval providers ที่จะพิสูจน์จริง; เพิ่มชนิดใหม่เมื่อผ่านชุดทดสอบ ไม่อนุมานจาก interface
6. **Performance:** ประกาศ workload, dataset, machine/runtime, warmup, repetitions และเกณฑ์ก่อนวัด; เก็บ raw results ทุกครั้ง และวัด startup, idle memory, allocations, throughput, p95/p99 เทียบ baseline ของ stack เดียวกัน

## มาตรฐานที่ช่วยให้พัฒนาต่อได้ระยะยาว

เสนอใช้ versioned contracts/config schemas, compatibility policy, migration tooling, replaceable adapters และ deprecation windows เพื่อรองรับการเปลี่ยนเทคโนโลยีตามเวลา ไม่รับรองอายุใช้งาน 30–50 ปีจากการออกแบบครั้งเดียว

ตัวชี้วัดที่ควรตกลงแทนคำว่า “เหนือกว่าทุก framework”: ปริมาณโค้ดที่ผู้ใช้ต้องเขียน, เวลาเพิ่ม operation/transport, overhead ของโมดูลที่ปิด, tenant-isolation correctness, failure recovery และ performance/cost ภายใต้ workload ที่กำหนด การเปรียบเทียบข้ามภาษาและ runtime ต้องมีวิธีทดลองที่เป็นธรรมและเปิดเผยขอบเขตผล

## คำถามที่ยังมีผลต่อรายละเอียดแผน

- งาน business ตัวอย่างและปริมาณโหลดเป้าหมายของแต่ละสายคืออะไร รวมถึงขนาดข้อมูล จำนวน tenants และ concurrency?
- การเปลี่ยน topology/architecture ยอมรับ deploy ใหม่ได้หรือจำเป็นต้องเปลี่ยนขณะรัน? ข้อเสนอเริ่มจาก config ตอน startup และ deploy ใหม่; live changes ต้องเพิ่ม state migration และ rollback design
- SQL/cache/broker/identity/model/vector providers และ host/OS ใดเป็นชุดแรกที่จะรับรอง? การเลือกต้องสอดคล้องกับ compatibility ของ .NET ที่อนุมัติ

## แหล่งข้อมูลที่ตรวจ

ตรวจอ่านเมื่อ **2026-10-27** เอกสารออนไลน์อาจเปลี่ยนภายหลัง ลิงก์เหล่านี้เป็นแหล่งอ้างอิงของคุณสมบัติ ไม่ใช่หลักฐานว่าตัว Engine ทำได้แล้ว

- **S1:** [.NET Generic Host](https://learn.microsoft.com/en-us/dotnet/core/extensions/generic-host)
- **S2:** [Aspire FAQ](https://aspire.dev/get-started/faq/)
- **S3:** [Microsoft Orleans overview](https://learn.microsoft.com/en-us/dotnet/orleans/overview)
- **S4:** [Dapr building blocks](https://docs.dapr.io/concepts/building-blocks-concept/)
- **S5:** [Spring Boot — Creating Your Own Auto-configuration](https://docs.spring.io/spring-boot/reference/features/developing-auto-configuration.html)
- **S6:** [Quarkus — Contexts and Dependency Injection](https://quarkus.io/guides/cdi-reference/)
- **S7:** [NestJS modules](https://docs.nestjs.com/modules)
- **S8:** [FastAPI features](https://fastapi.tiangolo.com/features/)
- **S9:** [Effective Go — Interfaces](https://go.dev/doc/effective_go#interfaces_and_types); เอกสารระบุว่าเขียนตั้งแต่ปี 2009 และไม่ได้ปรับปรุงครอบคลุม ecosystem ปัจจุบัน จึงใช้อ้างเฉพาะแนวคิด interface พื้นฐาน
- **S10:** [Compare gRPC services with HTTP APIs](https://learn.microsoft.com/en-us/aspnet/core/grpc/comparison?view=aspnetcore-10.0)
- **S11:** [EF Core database providers](https://learn.microsoft.com/en-us/ef/core/providers/)
- **S12:** [EF Core migrations with multiple providers](https://learn.microsoft.com/en-us/ef/core/managing-schemas/migrations/providers)
- **S13:** [AWS Prescriptive Guidance — Transactional outbox pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html)
