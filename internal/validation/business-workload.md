# Business workload v1 — คำสั่งซื้อและจองสินค้าแยก tenant

- วันที่ประกาศแผน: 2026-10-27
- คำตัดสิน: [ADR-0003](../adr/ADR-0003-multitenant-business-profile.md)
- สถานะ: **Predeclared design protocol; Not run; runtime M0**
- งานที่เกี่ยวข้อง: Engine #7, #8, #12, #14, #15, #21

ตัวเลขทั้งหมดเป็น engineering budgets สำหรับ first proof ไม่ใช่ผลวัดหรือ SLO ที่ตกลงกับผู้ใช้ production ห้ามเปลี่ยน threshold หลังเห็นผลเพื่อทำให้ผ่าน หากต้องเปลี่ยน protocol ให้สร้าง version ใหม่พร้อมเหตุผลและเก็บผลเก่าครบ

## Fixture และพฤติกรรมธุรกิจ

ใช้ fixture manifest version `business-v1`, seed **20261027**, UTF-8 และเวลา UTC คงที่สำหรับ correctness fixture IDs สร้างจาก `(seed, tenant, entity kind, sequence)` ตามอัลกอริทึมที่บันทึกใน fixture generator; ไม่ใช้ GUID/time/random จากเครื่องโดยไม่ล็อก Capture generator revision, row counts และ SHA-256 ของ dataset ก่อนเริ่มวัด

| ข้อมูล | ขนาดเริ่มต้น |
| --- | --- |
| Tenants | 100 ราย `T0001`–`T0100`; การกระจาย workload รอบเท่ากัน |
| Test users | 10 รายต่อ tenant, 1,000 identities; role/membership fixtures คงที่ |
| Catalog/stock | 1,000 SKUs ต่อ tenant รวม 100,000 rows; SKU identifiers ซ้ำข้าม tenant ตั้งใจให้จับ scope bug ได้ |
| Order history | 1,000 orders ต่อ tenant รวม 100,000 orders; 3 lines/order รวม 300,000 lines |
| Initial available stock | 10,000 หน่วยต่อ `(tenant, SKU)` สำหรับ steady load; oversell fixture ใช้ stock 10 แยกจากชุดนี้ |
| Payload | Create order มี 3 SKU, จำนวน 1–3 ต่อ SKU, body ไม่เกิน 4 KiB; event envelope ไม่เกิน 8 KiB; list page 20 rows |

`PlaceOrder` บันทึก Pending order + outbox atomically แล้ว Worker จอง stock และเปลี่ยนเป็น Reserved หรือ Rejected พร้อม inbox marker/derived event ใน transaction เดียว `RequestCancel` ต้องรักษา state machine และชดเชย reservation เพียงครั้งเดียวตาม aggregate version สถานะ Pending/Reserved/Rejected/CancelRequested/Cancelled และ allowed transitions ต้อง freeze เป็น contract ก่อนรัน

## Request/event mix

- 40% `PlaceOrder`, 10% `RequestCancel`, 40% `GetOrder`, 10% `ListOrders`; generator ใช้ deterministic schedule และเลือก cancellation เฉพาะ orders ที่มีสิทธิ์และสถานะที่กำหนด
- Every accepted create มี `OrderPlaced` outbox event; completed reservation และ cancellation มี state-change event ที่คาดได้จาก ledger ไม่ใช้จำนวน queue deliveries เป็นจำนวน business effects
- 5% ของ write requests ใน **conformance variant** replay idempotency key เดิมทั้ง body เดิมและ body ต่างกัน; replay body เดิมต้องคืนผลเดิม ส่วน body ต่างกันต้อง conflict โดยไม่เกิด effect เพิ่ม Variant นี้แยกจาก steady performance mix
- โหลด steady เป็น open-loop **100 requests/second**, max in-flight 100, timeout 2 วินาที; บันทึก offered/completed/dropped ทุก request เพื่อไม่ซ่อน overload ด้วย closed-loop pacing
- การขยายที่ **250 requests/second** เป็น stress characterization ภายใต้ resource เดิม: ต้อง bounded queues/timeouts/resource use และคง correctness แต่ไม่ใช่เงื่อนไขว่า throughput/latency steady gate ต้องผ่านที่ 250

## Reference profile และ baseline

ใช้ `business-single-broker` ใน ADR: app รวม 2 dedicated vCPU/2 GiB แบ่ง API/Worker เท่ากัน, infrastructure/load generator แยก limit สำหรับ benchmark ใช้ persistent storage/fsync และ TLS ตาม config เดียวกันทั้งสองฝั่ง ระบุ CPU model, scheduler quotas, OS/kernel, memory, disk class, network, .NET SDK/runtime, exact packages, images/digests และ all process limits

Baseline เป็น plain ASP.NET Core + Npgsql/RabbitMQ.Client ทำธุรกิจ/schema/auth/tenant/RLS/outbox/inbox/retry/telemetry แบบเดียวกัน โดยไม่ผ่าน Engine ใช้ SQL migrations, dataset, request schedule และ wire contracts เดียวกัน ห้ามเทียบ Engine ที่มี security/durability ครบกับ baseline ที่ข้ามสิ่งเหล่านี้ ถ้ายังไม่มี baseline parity ให้รายงาน **comparison blocked** และห้ามคำนวณ overhead pass

ก่อน **แต่ละ variant/run** ของ baseline และ Engine ต้อง reset DB/queues/inbox/outbox/caches ด้วย fixture เดิมและตรวจ hashes; restart app/provider ตามแผนเดียวกัน Warmup 120 วินาที แล้วหยุด offered load, drain งาน warmup และทำ reseed barrier นอกช่วงวัดเพื่อให้ dataset, request ordinals, stock, idempotency keys และ ledger เริ่มเหมือนกันทั้งสองฝั่ง คง process/JIT/connection warm state ที่สัญญาอนุญาตและบันทึกไว้ จากนั้นวัด 600 วินาทีต่อ run ทำ **5 paired repetitions** เรียงแบบ balanced deterministic order จาก seed; เก็บทุกรอบ ไม่เริ่มรอบใหม่เพียงเพราะ latency รอบก่อนสูง

## Correctness และ isolation gates

| Gate | เกณฑ์ผ่าน |
| --- | --- |
| Transaction boundary | ทุก accepted order มี durable order+outbox; fault ก่อน commit ไม่เหลืออย่างใดอย่างหนึ่ง หลัง commit แต่ response ขาดต้องตามคืนด้วย idempotency key ได้ |
| Inbox/business idempotency | Replay message เดิม 10 ครั้งและ delivery ขนาน 10 consumers: reservation/order transition/inbox effect เกิดตาม ledger เพียงหนึ่งครั้งต่อ logical event ไม่มี stock หักซ้ำ |
| Concurrent stock | 100 concurrent attempts สำหรับ SKU stock 10 และ quantity 1: มี 10 successful reservations เท่านั้น, stock ไม่ติดลบ, ที่เหลือ reject ตาม contract |
| Tenant boundary | ใช้ tenant A identity เรียก IDs/SKU/idempotency keys ของ B ผ่าน get/list/create/cancel/event paths ต้องไม่อ่านหรือแก้ B; zero cross-tenant rows/effects ใน independent SQL audit |
| RLS/pooling | ทดสอบ runtime role ไม่มี BYPASSRLS/table ownership; stale tenant context หลัง connection reuse และ missing context ต้องไม่ข้าม tenant; raw SQL aggregate/query paths อยู่ใน matrix |
| Worker trust | Envelope tenant/aggregate/schema mismatch, caller-supplied principal, unknown event type และ unauthorized producer ต้อง reject/quarantine โดยไม่มี business effects |
| Identity | Wrong issuer/audience/signature, expired/not-yet-valid token, missing scope/membership และ altered tenant header/body ต้อง deny; logs/events ไม่บันทึก bearer/refresh tokens หรือ secrets |
| Ordering | ส่ง version `n+1` ก่อน `n`, replay stale versions และใช้หลาย workers: state machine ตรวจพบและลู่เข้าสู่ valid state โดยไม่ double-effect ไม่อ้าง global FIFO |
| Cancellation | ก่อน SQL commit ต้อง rollback/cleanup; หลัง commit client cancellation ไม่ทำให้ durable work หาย; cancelled tasks/connections กลับสู่ resource budget |
| Config activation | API-only ไม่มี worker loop/broker/cache connection; disabled provider ไม่มี constructor/factory/I/O ของตนเอง เว้น shared dependency ที่มี module อื่นต้องใช้อย่างชัดเจน |

Correctness/security gates ต้องผ่าน **ทุกกรณีที่ประกาศ** ไม่ใช้ error-rate percentile กลบ tenant leak หรือ lost order Independent reconciliation ต้องตรวจครบทุก order/event ใน fixture/run ledger และบันทึก counts/hash ไม่สุ่มดูบางรายการ

## Steady performance gates สำหรับ resource ที่ประกาศ

| Metric | Budget ที่เลือก |
| --- | --- |
| Offered/successful/rejected/dropped | 100 req/s ตลอด measurement; successful expected business outcomes ≥99.9% ของ offered ภายใน interval + drain budget; unplanned 4xx/429/5xx, dropped และ timeouts เป็น 0 ใน positive non-fault variant; explicit rejection ไม่ช่วยให้ผ่าน successful-work floor; expected domain outcomes ต้องระบุใน manifest ล่วงหน้า |
| HTTP latency | p95 ≤100 ms, p99 ≤250 ms ต่อ run; แยก endpoint พร้อม overall ไม่ใช้ weighted mean แทน tail percentile |
| End-to-end business completion | จาก accepted DB commit ถึง durable terminal reservation state: p95 ≤2 s และ p99 ≤5 s |
| Engine overhead | เทียบ paired baseline: p95 ratio ≤1.15, p99 ratio ≤1.20, completed throughput ratio ≥0.90; ทุก paired repetition ต้องผ่าน พร้อมรายงาน absolute SLO ทั้งสองฝั่ง |
| Memory/resources | รวม API/Worker RSS peak ≤2 GiB และไม่มี OOM/crash; CPU quota ไม่เกิน 2 vCPU; ตรวจ handle/thread/connection/outstanding work หลัง drain ว่าไม่โตไม่จำกัด |
| Drain | หลังหยุด offered requests 30 s ต้องไม่มี due outbox/in-flight orders ที่ไร้ terminal reason; ตรวจ ledger ครบ ไม่ใช้ queue depth อย่างเดียว |

Request latency = terminal completion minus **scheduled arrival** จาก monotonic clock ของ driver โดยเก็บ actual send, queue wait, success/rejected/error/drop แยก; timeout ต้องรวม elapsed/censoring ตามจริง ไม่ใช้เฉพาะ actual-send latency Event completion ใช้ correlated timestamps ที่เทียบ clock domain ได้ หรือรายงาน clock uncertainty แยก เก็บ traces, SQL metrics, broker backlog, GC และ RSS เป็นหลักฐาน การเปิด telemetry ต้องเหมือนกันทั้งสองฝั่ง

## Failure/recovery suite ที่แยกจาก steady measurement

ทุก scenario ทำกับ dataset reset ของตนเองและเก็บ before/after ledger ชัดเจน ไม่รวม intentionally rejected/fault requests เข้า steady error-rate แล้วเลือกตัดออกภายหลัง

1. **Broker unavailable 30 s:** SQL/outbox ที่รับสำเร็จต้องคงอยู่; restore broker แล้วหยุด offered load และ drain ให้ครบภายใน 60 s ไม่มี lost business effect วัด retry budget/backlog และไม่วน retry ถี่โดยไม่มีการจำกัด
2. **Worker process kill 30 s:** kill หลัง publish ก่อน inbox commit และหลัง business commit ก่อน ack เป็นคนละ case; restart แล้ว dedup ถูกต้องและ drain ภายใน 60 s พิสูจน์ด้วยฐานข้อมูลและ event IDs
3. **Database unavailable 10 s:** affected API calls fail ภายใน 2 s โดยไม่ตอบ accepted หากยังไม่ commit; recovery ภายใน 30 s หลัง database healthy และไม่มี connection retry ไม่จำกัด
4. **Poison message:** ใช้ schema/event ที่ consumer ประมวลผลไม่ได้; สูงสุด 3 delivery attempts (initial + 2 retries) พร้อม backoff 1/2 s และ deterministic jitter ที่ล็อกไว้ แล้ว quarantine/DLQ ภายใน 30 s จาก delivery แรก โดย good messages ยังเดินต่อ ไม่ requeue วนไม่สิ้นสุด
5. **Identity discovery/key rotation faults:** ทดสอบ valid cached-key policy, unknown kid, expired metadata และ issuer endpoint failure ตาม configured trust policy; ห้าม fail-open หรือดึง discovery URL จาก untrusted request
6. **Single-node broker restart:** committed outbox และ broker durability/replay ต้อง reconcile ครบ; ไม่ใช้ผลนี้อ้าง node-loss HA
7. **HA profile เพิ่มเติม:** ใช้ quorum สาม broker ตาม ADR แล้วสูญเสียหนึ่ง node/leader; เมื่อ majority ยังอยู่ต้อง recover delivery ภายใน 30 s และไม่มี lost/duplicate business effects ภายใน 60 s หลังหยุด load การสูญเสีย majority ต้อง bounded fail/stall ตามสัญญา ไม่อ้างว่ายัง available
8. **Scale-out variant:** เพิ่ม Worker 1→3 processes โดยบันทึก CPU/RAM รวมที่เพิ่มจริง รายงาน throughput/lag และ ordering/dedup/tenant correctness; เกณฑ์แรกคือ correctness และ bounded recovery ไม่รับประกัน linear autoscale จาก run เดียว

## Invalid runs, evidence และการตัดสิน

- Freeze protocol revision, baseline parity, fixture hashes และ hardware manifest ก่อน measurement หากเปลี่ยน software/config/provider/data/resource/threshold ระหว่าง run ให้ invalid พร้อมเหตุผล
- Preflight ตรวจ load-generator drops, clock uncertainty, insufficient disk, denied resource quotas และ background load; ถ้าพบหลังเริ่มวัดให้เก็บ raw และทำเครื่องหมาย invalid ไม่ลบผล
- ต้องแสดงรายการ attempts ทั้งหมด รวม preparation failures, failed gates และ invalid runs ห้ามตัด outliers หรือเก็บเฉพาะ best run; rerun จาก environment fault ต้องระบุ cause/fix และรันคู่ baseline/Engine ใหม่ตาม protocol ที่ประกาศ ไม่เลือก rerun เฉพาะฝั่งที่เสียเปรียบ
- Performance gate ที่ไม่ผ่านโดยไม่มี environment invalidity คือ Fail ไม่ใช่เหตุให้เลื่อน threshold Benchmark ผ่านไม่แทน correctness/security/operational proof
- เก็บ source/Engine SHA, dependency locks, image digests, fixture/manifest hashes, commands, raw request/events/traces/SQL/broker metrics, counts/results และ cleanup state ให้ redact secrets โดยบันทึกขอบเขต ไม่ลดข้อมูลที่จำเป็นต่อ reconciliation
- CI เริ่มไม่ได้เพราะ permission/infra/spending คือ Blocked ไม่ใช่ pass; local pass ไม่ใช่ hosted CI pass และไม่ทำให้ M0 ขยับเอง

ยังไม่มี generator, harness, containers, sample implementation หรือผล run จาก protocol นี้ หลัง implement และรันจริงให้ผูก evidence กับ Engine SHA และ provider/version/profile ที่ตรวจเท่านั้น
