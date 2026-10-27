# ADR-0001 — W0 profiles, configuration semantics and proof boundaries

วันที่: 2026-10-27 (Asia/Bangkok)

สถานะ: **Accepted for W0 planning — implementation qualification pending**

ผู้ใช้มอบหมายให้ศึกษาและเลือก provider/workload/เกณฑ์ทดสอบสำหรับ Samples ทั้งสามแนวพร้อม ADR ข้อเลือกในชุด ADR นี้เป็นการตัดสินใจทางวิศวกรรมภายในขอบเขตดังกล่าว ไม่ใช่การรับรองว่าผู้ใช้ลงนามรับทุกค่า SLO หรือว่าระบบทำงานผ่านแล้ว Runtime maturity ยังคง M0

เกี่ยวข้องกับ Engine issues #2, #3, #4, #6, #11, #15, #17, #21 และ #23

## Context

ต้องรักษา business handlers/contracts ชุดเดียวภายใน supported capability profile โดยไม่เปิดบริการที่ไม่ใช้ ทั้งสาม Samples ต้องสะท้อนโครงการคนละขนาดและคนละ failure model ไม่สร้าง Core แยกกัน เป้าหมาย portability ไม่ทำให้ transaction/query/streaming/network/AI semantics เหมือนกันโดยอัตโนมัติ

## Decision

1. เลือก config ตอน startup และ restart/redeploy เมื่อต้องเปลี่ยน deployment profile การเปลี่ยน topology ขณะรันและ state migration เป็นขอบเขตภายหลัง
2. Core/Application ไม่รับ host/protocol/provider SDK objects โดยตรง Transports, state, identity, eventing และ AI เป็น adapters ที่ระบุ capabilities และ dependencies ชัดเจน
3. สร้าง immutable composition plan หลัง validate schema/graph/compatibility และก่อน callbacks/constructors/connections/background work Explicit disabled ห้าม activation ของโมดูลนั้น; shared dependency ที่โมดูลอื่นใช้ต้องจำแนกต่างหาก
4. ใช้ tenant-aware operation context ที่ immutable และ trusted provenance; caller-provided tenant header, event field หรือ retrieved text ไม่ใช่ authority โดยตัวเอง
5. แยก synchronous request/reply, server streaming, at-least-once event delivery และ durable workflow เป็นสัญญาคนละแบบ การเปลี่ยนไป remote ต้องรองรับ deadline, duplicate, serialization และ failure ตาม contract
6. เก็บ business workflow ของ Samples แยกจาก Engine Core ใช้ pinned Engine revision/package เมื่อเริ่มรันจริง

## Selected lane decisions

| Lane | Decision | Workload/proof protocol |
| --- | --- | --- |
| Small API | [ADR-0002](ADR-0002-small-api-profile.md) | [small-api-workload](../validation/small-api-workload.md) |
| Multitenant business | [ADR-0003](ADR-0003-multitenant-business-profile.md) | [business-workload](../validation/business-workload.md) |
| AI / Agent / Retrieval | [ADR-0004](ADR-0004-ai-retrieval-profile.md) | [ai-retrieval-workload](../validation/ai-retrieval-workload.md) |

## Platform and version qualification

Implementation candidate คือ .NET SDK `11.0.100-rc.3.26522.148` และ .NET/ASP.NET Core runtime `11.0.0-rc.3.26522.148` ตาม official release metadata ที่ตรวจวันที่นี้ เก็บ [selected metadata](../evidence/w0/dotnet-11-candidate.json) และ source JSON พร้อม source hash แล้ว การมี published binary hash ยังไม่ใช่การตรวจ hash ของ binary ที่ดาวน์โหลดจริง

ยังไม่ได้ติดตั้ง SDK/restore/build/ทดสอบ drivers หรือเรียก provider จริง ไม่มี `global.json` ที่สร้างความรู้สึกว่าผ่าน qualification แล้ว .NET 12 แยก research track ไม่ใช้ API proposals เป็น supported public contract

Provider version ใน ADR เป็น candidate ที่มีแหล่งอ้างอิง ก่อนการทดลองต้องมี lock manifest: exact package versions, package lock/content hashes, OS/runtime, image manifest digest (รวม platform digest), model revision/file hashes, configuration, fixture hashes, Engine revision และ tool versions ห้ามใช้ mutable `latest` หรือชื่อ model tag เป็น reproducibility lock

หลักฐาน .NET: [official download](https://dotnet.microsoft.com/en-us/download/dotnet/11.0), [release metadata](https://builds.dotnet.microsoft.com/dotnet/release-metadata/11.0/releases.json)

## Common experiment conditions

- Reference application tier: Linux x64/glibc, dedicated 2 vCPU และ memory limit 2 GiB; OS/container image ต้องเลือก supported version และ lock digest ก่อนรัน Linux เป็น reference performance tier ส่วน Windows x64 เป็น functional portability tier ก่อน ยังไม่อ้างผล performance ข้าม OS
- Provider tier กับ load generator อยู่คนละ resource allocation กับ application ห้ามเอา app 2 GiB ไปอ้างว่ารวม SQL/broker/identity/vector/model server แล้ว แต่ละ lane ต้องระบุ provider limits และ topology เพิ่มเติม AI model tier แยกตาม ADR-0004
- บันทึก physical CPU, affinity/quota, VM/container limits, host load, CPU governor/power, memory/swap, network/storage, TLS และ tooling ก่อนเริ่ม ปิดความสามารถที่ไม่เกี่ยวข้องด้วย config ที่ตรวจแล้ว
- ใช้ versioned fixture generator/dataset, fixed seed, clock policy และ canonical fixture hashes โหลด fixtures และ reset state แบบเดียวกันระหว่าง baseline/Engine ทุกครั้ง ห้ามผล test หนึ่งเปลี่ยนข้อมูลโดยไม่ reset แล้วเทียบกับอีกผล
- Baseline ใช้ SDK/provider/TLS/schema/fixture/semantics เดียวกันโดยไม่มี Engine abstraction ที่วัด และต้องผ่าน correctness ก่อน เปรียบเทียบด้วย randomized/declared paired order ตาม lane protocol
- ใช้ run count, warmup, workload mix, offered load และ thresholds ตาม lane protocol อัตรางานแบบ fixed offered load ต้องเก็บ scheduled start, actual send, completion, rejected/dropped/timeout แยกกัน ห้ามซ่อน coordinated omission หรือใช้เฉพาะคำขอสำเร็จคำนวณ latency
- ทุกค่าตัวเลขเป็น **engineering acceptance budget ที่ประกาศก่อนวัด** ไม่ใช่ค่าที่วัดได้หรือ performance guarantee หาก preflight/baseline ทำตามเงื่อนไขไม่ได้ ให้ผล Invalid/Blocked และเก็บข้อมูล ห้ามลดโหลดหรือลดเกณฑ์ย้อนหลังเพื่อให้ผ่าน
- แยก warm steady state, cold start, recovery และ fault-injection ไม่รวมเป็นค่าเฉลี่ยเดียว Timing ของ fault windows ต้องไม่นับเป็น steady-state SLO โดยเงียบ ๆ ต้องมี recovery metrics ของตนเอง

## Cross-lane non-negotiable gates

- Tenant/authorization bypass, unauthorized tool effect, cross-tenant retrieval leak และ invariant violation ต้องเป็นศูนย์ในชุดกรณีทดสอบที่ประกาศไว้ การได้ศูนย์ในชุดนี้ไม่ใช่ข้อพิสูจน์ว่าปลอดภัยจากทุกกรณี
- API-only ต้องไม่มี disabled GraphQL/Worker/SQL/broker/AI registrations ที่ทำ constructor/factory/connection/endpoint/background work นับและเก็บ activation evidence แยก shared dependencies
- Cancellation ต้องตรวจผลข้างเคียงและ eventual cleanup ตาม contract ไม่ใช้ HTTP disconnected อย่างเดียวแทนหลักฐานงานหยุด
- Duplicate delivery ต้องไม่เพิ่ม business effects ซ้ำใน idempotency boundary ที่ประกาศ การยืนยัน durable response ต้องผูกกับ transaction/durable state จริง ไม่ใช้ process memory หรือ cache แทน
- Runtime conformance, isolation/security cases, recovery และ performance เป็น gate แยกกัน การผ่านอย่างหนึ่งไม่ทดแทนอีกอย่าง

## Alternatives and consequences

การเปิด database/cache/broker/AI ให้ทุก sample ช่วยลดจำนวน profile แต่ทำให้ Small API ไม่สะท้อน minimum footprint จึงเลือก opt-in composition ส่วนการบังคับ universal database/event/model interface เดียวทำให้ capability ต่างกันถูกซ่อน จึงเลือก explicit capability contracts และ reject unsupported combinations

การเริ่มจาก local/self-hosted providers ลดการพึ่งบัญชีและค่าใช้บริการในการพิสูจน์ครั้งแรก แต่เพิ่มภาระ version/license/resource/operations qualification Cloud และ managed providers เพิ่มได้เมื่อมีความต้องการและได้รับอนุญาตสำหรับการ provision; ยังไม่อ้างว่า local proof ครอบคลุม cloud

## Completion and revalidation

W0 decision package ผ่านได้เมื่อ ADR/source/workload/gates สอดคล้องกัน, task references ตรวจได้ และเอกสารกับ GitHub ตรงกัน การเลือกนี้ไม่ปิด platform qualification #3 หรือ implementation/E2E tasks โดยอัตโนมัติ

ทบทวน ADR เมื่อเปลี่ยน contracts/provider major/version resource tier/workload/เกณฑ์รับรอง บันทึก before/after/reason และ revalidation scope การเปลี่ยน threshold หลังเห็นผลต้องเป็น protocol รุ่นใหม่ โดยคงผลเก่าและเหตุผลไว้
