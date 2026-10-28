# Small API workload and test protocol — W0 version 1

- วันที่: 2026-10-27 (Asia/Bangkok)
- Decision: [ADR-0002](../adr/ADR-0002-small-api-profile.md)
- สถานะเดิมเมื่อ freeze W0: **Predeclared engineering design; not executed**. Continuation2026-10-28: [complete nonqualifying observations](../planning/w2-small-api-conformance-benchmark.md) now exist, with startup FAIL and GraphQL stability INVALID; reference/full gates remain Blocked. The budgets below are unchanged.
- Maturity: M0; task #11 และ adapter/core/config tasks ต้องแนบ evidence ของ revision ที่รันจริง

## 1. Reference environment และ preflight

Performance reference เริ่มจาก Linux x64, app มี 2 dedicated vCPU/2 GiB RAM, load generator อยู่คนละเครื่อง/CPU allocation และไม่มี database/cache/broker/IdP/AI process เป็น dependency ของ lane นี้ Parent W0 platform ADR เป็นแหล่งกำหนด host reference ร่วม; ถ้ารายละเอียดขัดกันให้ resolve ก่อน freeze run manifest

ล็อก exact OS/kernel/container digest, CPU model/governor/affinity, memory limit, SDK/runtime, package lock, build Release, server GC/tiering settings, TLS cipher, driver commit/version และ network topology ใน manifest ห้ามเปลี่ยนระหว่าง baseline และ Engine ใช้ Kestrel HTTPS TLS 1.3 + keep-alive ทั้งคู่ ไม่มี debugger/profiler ใน timed runs ส่วน instrumentation overhead ต้องเหมือนกัน

Baseline คือ ASP.NET Core Minimal API โดยตรงบน runtime เดียวกัน ใช้ business handler, fixture store, JSON settings, error/validation/cancellation behavior และ probes ชุดเดียวกัน Engine เพิ่มเฉพาะ portable dispatch/composition/adapter path ที่จะวัด ห้ามตัด validation/policy ออกเพื่อทำ baseline หรือ Engine เร็วขึ้น GraphQL baseline ใช้ Hot Chocolate version เดียวกันและ handlers เดียวกันโดยตรง แยกจาก REST result series

Preflight ต้องพิสูจน์ driver ไม่มี drops, payload/status validation ถูกต้อง, clock/timestamps ใช้ monotonic duration และ app/driver ไม่ถูก throttle โดยข้อจำกัดที่ไม่ได้ประกาศ ถ้าสภาพแวดล้อมไม่พร้อมให้บันทึก blocked/invalid แทนการเรียกผลว่า pass

## 2. Deterministic fixtures

- Dataset ID: `cehpalon-small-api-v1`; seed bytes: UTF-8 `cehpalon-small-api-v1:20261027`
- สร้าง records `id=1..10000`; `label` เริ่มเป็น `item-` ตามด้วยเลข id แบบ decimal 5 หลัก; `revision=0`; `amountMinorUnits=id*17` เก็บเป็น integer
- Payload ปกติเป็น JSON UTF-8 ไม่เกิน 1 KiB ต่อ command; `label` ยาวไม่เกิน 64 Unicode scalar values; ListItems page size คงที่ 20 และ sort ด้วย id ascending
- Generator ใช้ `SHA256(seed || UTF8(":" + decimal(requestIndex)))` และอ่าน 8 bytes แรกเป็น unsigned big-endian เพื่อเลือก read id แบบ modulo 10000 ห้ามใช้ Random implementation ที่อาจเปลี่ยนตาม runtime
- Hash UTF-8 serialized dataset และ ordered request manifest ก่อนรัน ระบุ serialization ordering/line endings ชัดเจน ให้ baseline และ Engine รับ bytes ชุดเดียวกัน
- Store จำกัด 10,000 keys ตลอดรัน ไม่มี unbounded insert command; logical writer lanes มีหมายเลข `0..31` สำหรับ write ordinal `j` ภายใน lane เลือก `id=1+lane+32*(j mod 312)` และ expected revision `floor(j/312)`; label ใหม่เป็น `lane-{lane}-write-{j}` จึงไม่ทับ writer อื่นและไม่เพิ่ม keys แต่ละ writer ส่ง update ของตนแบบลำดับเดียว จึงไม่มี conflict ที่เกิดจาก driver design โดยไม่ตั้งใจ
- Reset dataset ก่อนแต่ละ process/run Warmup state ถูกทิ้งและ reseed ก่อน measured interval โดย barrier ที่อยู่นอกช่วงเวลา การตรวจผลหลังรันคำนวณ revision/label ที่คาดจาก acknowledged request manifest; เก็บ request IDs ที่ failed/unknown outcome ไว้เสมอ

## 3. Operations และ traffic mix

| Operation | สัดส่วนของ block 100 requests | ผลที่ตรวจ |
| --- | --- | --- |
| GetItem | 80 | id/label/revision/amount ตรง snapshot ที่ contract อนุญาต ไม่คืน item ผิด |
| ListItems | 15 | 20 IDs เรียงลำดับ ไม่ซ้ำ และ pagination boundary ถูกต้อง |
| SetLabel | 5 | expected revision → atomic +1; response และ final-state invariant ตรงกัน |

กำหนดตำแหน่งแต่ละ operation ใน block คงที่และ serialize writer sequences ไว้ใน manifest ก่อนรัน ใช้ logical request schedule เดียวกันกับ REST และ GraphQL เปรียบเทียบ business result ไม่เทียบ HTTP/GraphQL wire envelope ว่าต้องเหมือนกัน ข้อมูล concurrent read เปรียบเทียบกับ valid version history/linearization ของ record ไม่เทียบกับ final state อย่างผิดเงื่อนไข

หลักของ parity ใช้ ordered functional corpus แยกจาก load test: 1,000 cases ประกอบด้วย valid get/list/update, not-found, validation, revision conflict และ cancelled requests กำหนด expected business outcomes ไว้ใน fixture ก่อน adapter mapping

## 4. Correctness และ negative gates

| Gate | เกณฑ์ผ่านที่ประกาศ |
| --- | --- |
| Functional corpus | expected business outcomes ทั้ง 1,000 cases ตรงกัน ไม่มี unaccounted skip |
| State/concurrency | 10,000 keys เท่าเดิม; acknowledged updates ไม่หาย; revision conflicts ที่จงใจสร้างคืน error ที่ระบุ; duplicate request ไม่ตีความเป็น idempotent เว้นแต่ contract ประกาศไว้ |
| REST/GraphQL parity | ordered corpus ผ่านทั้งสอง adapters; handler source/contract เดียวกัน; unsupported exposure ถูกปฏิเสธก่อน start |
| Invalid input | malformed JSON, wrong types, null required values, label เกินขนาด, invalid id/page และ 16 KiB+1 body ถูกปฏิเสธตาม contract ก่อน business mutation |
| Cancellation | 100 deterministic requests ต่อ profile ใช้ cancellable fixture delay 5 s, client cancel หลัง 50 ms; handler สังเกต cancellation ภายใน 100 ms และไม่มี state mutation หลัง cancel acknowledgement |
| Startup failure | dependency cycle, unknown module, incompatible profile และ explicit false dependency contradiction ล้มก่อน module-owned side effects |
| Cleanup | shutdown เสร็จภายใน 5 s, ไม่เหลือ listening socket/owned background task/resource lease; repeat start/stop 30 รอบ |
| Security boundary | isolated synthetic dataset เท่านั้น; ไม่คืน stack traces/secrets; request body limit ใช้จริง; TLS client ตรวจ trust/hostname ด้วย test CA ที่ติดตั้งเฉพาะ test context ไม่มี certificate-validation bypass |

Small API profile นี้ไม่มี external authentication/tenancy จึงไม่เป็นหลักฐานว่า identity/tenant boundary ผ่าน เมื่อเปิด capability เหล่านี้ภายหลังต้องเพิ่ม full negative contract tests; ห้ามใช้ public benchmark profile กับข้อมูลจริงหรือเรียกว่า production-secure SaaS

## 5. Zero activation gates

รัน functional phase สำหรับ API-only, API+GraphQL และ invalid/disabled API profile ใช้ probes ที่นับ module-owned factories, constructors, DI activation, GraphQL schema/executor initialization, endpoints, background tasks, network connection attempts และ provider lifecycle

- API-only: GraphQL/Worker/database/cache/broker/AI/retrieval probe counts เป็น **0** ตลอด startup + 10,000 requests + shutdown; `/graphql` ไม่เปิดและไม่มี schema/IDE/WebSocket endpoint
- API+GraphQL: เปิดเฉพาะ API และ GraphQL HTTP ที่เลือก; Worker/database/cache/broker/AI/retrieval ยังเป็น 0; ทดสอบ GraphQL cost/depth/size rejection และไม่มี IDE/subscription activation
- API ถูกปิดและไม่มี entrypoint อื่น: ไม่สร้าง WebApplication/Kestrel/listener; invalid config ต้อง fail ก่อน activation callback แรก
- ใน disabled probe ใช้ factory ที่ throw เมื่อถูกเรียก เพื่อให้การเปิดผิดล้มอย่างเห็นได้ชัด แยก shared dependencies ที่โมดูลอื่นต้องใช้ ไม่รวมเข้ากับโมดูลปิดอย่างผิดความหมาย
- Endpoint 404 อย่างเดียวไม่พอรับรอง zero activation และการมี package ใน publish output ไม่เท่ากับมี constructor/connection work

## 6. Performance protocol และ budgets

1. แต่ละ matched pair เป็น baseline/Engine บนเครื่องและ manifest เดียวกัน สลับลำดับแบบกำหนดก่อนเริ่ม: BE, EB, BE, EB, BE รวม 5 pairs ต่อ profile
2. แต่ละ process warmup 60 s ที่ offered rate เดียวกับ measurement แล้ว reseed ที่ barrier; measure 180 s ด้วย fixed open-loop 1,000 requests/s, request timeout 1 s, max 128 outstanding requests เมื่อ cap เต็มให้บันทึก dropped offered request เป็น failure ไม่ซ่อนโดยลดอัตรา
3. Sweep 100/500/2,000 requests/s เป็น diagnostic series แยก ไม่ใช้เลือก rate ที่ให้ผลดีที่สุดมาแทน acceptance series 1,000 requests/s
4. เก็บ per-request scheduled/sent/completed timestamps, operation, status/business code, bytes, error/cancel, queue wait และ raw histogram; latency ใช้ completion minus scheduled time เพื่อไม่ซ่อน coordinated omission
5. Startup วัด process start → readiness และ successful verified request แรก 30 fresh process launches ต่อ variant แยกจาก load series ไม่นับ build/download เป็น startup และไม่เรียก OS-cache-warm launches ว่า machine-cold boot
6. Idle RSS วัดหลัง startup + warmup แล้ว idle 120 s; เก็บค่า 1 Hz ช่วง 60 s ถัดมา; allocations/CPU/GC วัด matched path โดย instrumentation เท่ากันและรายงาน overhead limitations

| Metric | Gate สำหรับ initial reference profile |
| --- | --- |
| Correct responses | 100% contract-valid expected business outcomes ตาม positive steady manifest; unplanned 4xx/429/5xx, timeout, dropped offered requests และ lost acknowledged updates เป็น 0; explicit rejection ไม่ถือเป็น successful work |
| Warm latency ที่ 1,000 req/s | p95 ≤20 ms และ p99 ≤50 ms ต่อ measured run |
| Engine overhead | Engine p95 ≤ baseline p95 + max(1 ms, 15% baseline p95) ภายในแต่ละ matched pair; allocations/request ≤ baseline +1 KiB |
| Successful offered work | ≥99.9% of scheduled requests ต้องสำเร็จตาม expected business outcome ภายใน measured interval หรือ drain ≤1 s; rejected/error responses ไม่ช่วยให้ผ่าน floor และ gate correctness ยังห้าม unplanned rejection/lost/timeouts/drops |
| Fresh-process startup | p95 ≤1,000 ms และ Engine p95 ≤ baseline p95 +150 ms |
| Idle RSS | ≤256 MiB และ Engine median idle RSS ≤ baseline +16 MiB |
| Stability | per-run p95 coefficient of variation ≤10% ภายใน variant; ถ้าเกินให้ผล performance ชุดนี้ invalid และรักษา raw data ทั้งหมด |

Budgets นี้เป็นการเลือกของทีมสำหรับ sample บน reference environment ไม่ใช่ข้อรับรอง .NET/Hot Chocolate หรือขีดจำกัดของ Engine ทุก workload ต้องผ่านทุก valid measured pair ไม่เลือกเฉพาะ aggregate ที่ดี Run ที่ baseline ไม่สามารถรับ 1,000 requests/s ตาม protocol ให้ระบุ infrastructure/workload invalid และทบทวน protocol แบบ version ใหม่ก่อนรันทั้งชุด ไม่ลด rate ย้อนหลังให้ผลเดิมผ่าน

## 7. Evidence และ stopping rules

- เก็บ predeclared manifest/protocol hash, exact Engine revision, package/dependency locks, fixture/request hashes, all raw runs และ environment capture ตัว commit ที่ใช้ reproducibility ของ Samples อยู่ใน evidence manifest ไม่ใส่ใน task/card Engine commit journal
- แยก correctness fail, security fail, performance fail, invalid environment และ CI blocked ให้ชัด เก็บ preparation failures และ outliers โดยไม่ตัดออก
- ถ้า source/config/dependency เปลี่ยนหลังวัด ต้องระบุ invalidate scope และรัน affected matrix ใหม่ตาม protocol ทั้งชุด ห้าม selective rerun เพื่อเลือกผลผ่าน
- ไม่รันจริงใน W0 document selection นี้ ยังไม่มี elapsed runtime, measured RSS, throughput, latency, security assurance หรือ maturity promotion

Later execution2026-10-28: [attempt03 tuning report](../planning/w2-small-api-tuning.md) supersedes prior current-result status, without changing this protocol. Numeric startup/idle/main/CV gates pass; diagnostic12attempts include11timed/one failed preflight. Reference/#3 stay Blocked. Preserve earlier failed/invalid runs rather than overwriting history.
