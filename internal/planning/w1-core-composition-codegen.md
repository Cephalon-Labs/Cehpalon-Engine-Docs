# W1 — Core, Composition และ operation code generation

วันที่ 2026-10-27 · Engine issues #5, #6 และส่วน code generation ของ #20

Snapshot for this revision; [tenant/identity continuation](w1-tenant-identity.md) supersedes current-state tracking/source assertions while preserving these exact historical proofs.

ส่งมอบส่วนพัฒนาอิสระจากการรับรอง Windows แล้ว โดยใช้ agent แยก worktree และให้ primary รวม/เขียนขึ้น GitHub คนเดียว การพัฒนานี้ไม่ปิด #3 และไม่ลบ dependency เดิม: full acceptance ของ W1 ยังรอ platform gate ส่วน CLI/scaffolding/transport-schema ของ #20 ยังเป็นงานคงเหลือ ดู [ADR-0005](../adr/ADR-0005-w1-portable-core-composition.md) และ [ADR-0006](../adr/ADR-0006-incremental-operation-code-generation.md)

Engine revision ที่ตรวจจริง: `fee491cecaba04232207a1a2884057498e81213e` ใช้ SDK `11.0.100-rc.3.26522.148` และ runtime `11.0.0-rc.3.26522.148` ไม่มีการแทน system SDK หรือเผยแพร่ NuGet

## สิ่งที่พัฒนาแล้ว

| ส่วน | พฤติกรรมที่ส่งมอบ | ขอบเขต |
| --- | --- | --- |
| Core | Typed request/reply, success/business error, immutable context/registry, lazy factory, ตรวจ ID/type/cancellation ก่อนสร้าง handler และคืนทรัพยากรแม้เกิด error/cancel | BCL-only; context เป็น correlation metadata ไม่ใช่ tenant/identity authority; factory ต้องคืน handler ใหม่ที่ engine เป็นเจ้าของ |
| Composition | อ่าน startup appsettings JSON แบบ strict, ตรวจ schema/profile/dependency/cycle/explicit false ก่อน callbacks, immutable explained plan และ deterministic activation order | schema1 รองรับเฉพาะ Modular/SingleProcess/RequestReply; 256 modules, JSON1MiB/depth32; ไม่มี effective IConfiguration provider merge หรือ live reload |
| Lifecycle | Preflight registrations ก่อน factory, สร้างเฉพาะ enabled modules, reverse rollback/disposal, ป้องกัน aliased resource และ cleanup ซ้ำแบบ concurrent | คืนเฉพาะ resources ที่ factory ส่งมอบ; factory รับผิดชอบ partial allocation ของตนเอง; ไม่ใช่ transaction rollback ของ external business effects |
| Code generation | Roslyn incremental generator สร้าง lazy typed registrations จาก Operation attribute; diagnostics สำหรับ invalid/duplicate/inaccessible/generic/ambiguous declarations | Roslyn4.14.0 เป็น build-time dependency; ไม่มี assembly scanning หรือ Roslyn ใน Core/consumer runtime; ไม่สร้าง endpoint/business logic/tenant policy |
| Consumer | Business handler ชุดเดียว ใช้ generated registry กับ appsettings3profiles และทดสอบ success/error/cancel/type guards/cleanup | เป็น in-process module recorders ไม่ใช่ HTTP/GraphQL/Worker adapters ของสาม sample lanes |

## ผลทดสอบบน revision ที่ commit แล้ว

| ชุดตรวจ | Windows11 Pro26H2/build26300.9711 | WSL Ubuntu22.04.5 x64/glibc2.35 |
| --- | --- | --- |
| Core contracts | 32/32 | 32/32 |
| Composition contracts | 80/80 | 80/80 |
| Code-generation driver | 42/42 | 42/42 |
| รวม component checks | 154/154 | 154/154 |
| Actual SDK compiler/analyzer fixture | Passed | Passed |
| Pinned Samples consumer | 5/5 | 5/5 |

Windows เครื่องนี้ยังไม่อยู่ใน support table ที่ตรวจ จึงเป็น **observational proof** เท่านั้น WSL ใช้ distribution ที่อยู่ในตารางแต่ไม่ใช่ bare-metal/deployment certification ทั้งสองระบบ restore แบบ locked และ Release build โดย warnings-as-errors ผ่าน ไม่มี skipped checks นับรวมเป็น pass Generated registry bytes ตรงกันระหว่างสอง host ที่ตรวจ; ไม่อ้าง cross-path DLL/PDB reproducibility, IDE หรือ NativeAOT/trimming compatibility

หลักฐาน: [delivery manifest](../evidence/w1/delivery-manifest.json), [Windows exact-source manifest](../evidence/w1/exact-win/manifest.json), [Linux exact-source manifest](../evidence/w1/exact-linux/manifest.json), [consumer Windows](../evidence/w1/consumer-win/manifest.json), [consumer Linux](../evidence/w1/consumer-linux/manifest.json) และ [13-package hash/license inventory](../evidence/w1/package-inventory.json) Package metadata/advisory inventory ไม่ใช่ security audit หรือ distribution approval

## Independent review และการแก้ที่เก็บหลักฐานไว้

แก้ cancellation ที่เกิดระหว่าง handler factory เพื่อหยุดก่อน business work และยัง dispose handler ที่สร้างแล้ว แก้ literal/escaped lone-surrogate JSON ให้คืน sanitized diagnostics แทน exception ที่หลุดออกมา และเพิ่ม regression cases พร้อมเก็บผลที่ยังไม่ผ่านเดิม

Peer พบว่า display name ไม่ใช่ symbol identity: normal/file-local handler ชื่อเหมือนกันทำให้ generator รุ่นแรกตัด operation ทิ้งตามลำดับไฟล์ แก้เป็น semantic symbol identity ตรวจ candidate errors ทุกตัว นับ attributes ครบ partial symbol และตรวจ reserved namespace/type path Peer รัน repro เดิมซ้ำ **5/5** ได้ rejection และไม่มี generated registry หลุดออกมา การตรวจ Core/Composition แบบ adversarial แยกอีก **8/8** ผ่าน ดู [review8cases](../evidence/w1/agents/integrated-review/results.json) และ [codegen review](../evidence/w1/agents/codegen-review/review-after-fix.json)

ผล 31/38-case และ integration150checks รุ่นก่อนแก้ยังอยู่ใน evidence พร้อม source hashes ไม่ใช้รับรอง source ปัจจุบัน

## Component benchmark

รันตาม [protocol ที่ประกาศก่อนวัด](../validation/w1-component-protocol.md) บน shared WSL host, i5-13500/14cores/20threads ไม่ได้กำหนด dedicated2vCPU/memory ceiling ของ workload ทั้งสาม lane เก็บ CPU/memory/affinity/SDK/source/DLL hashes และ raw5repetitionsครบ

ผลที่รับได้คือ [attempt02](../evidence/w1/benchmark-attempt02/result.json): guardrails **8/8** ผ่าน ค่า median ของ paired dispatcher overhead ประมาณ96.28ns/op และ extra allocation0B/op โดยทั้ง direct/dispatcher ยัง allocate56B/op ใน handler/result path นี้ จึงไม่ใช่ allocation-free claim Small4-module compile median16.82us และ128-node compile median1.343ms เป็นเฉพาะ warm component path ไม่ใช่ production latency หรือข้อพิสูจน์ว่าเร็วกว่า framework อื่น

[Attempt01](../evidence/w1/benchmark-attempt01/review.json) เก็บเป็น **Invalid** แม้ guardrails ผ่าน เพราะ primary เริ่ม package collector ซ้อนก่อนจบช่วงวัด แก้โดยรันใหม่ทั้ง protocolหลังงานอื่นเสร็จ ไม่เปลี่ยน source/workload/threshold และไม่เลือกรันเฉพาะ repetition ที่ดี Code-generation speed/CLI/real transport/provider/security workloads ยังไม่รัน

## GitHub, readiness และงานคงเหลือ

- #3 คง **OPEN/Blocked** จนมีผลบน Windows ที่รองรับ โดยไม่แก้ billing/spending settings
- #5/#6 ส่งมอบ portable component slice และผล local tests/benchmark แล้ว แต่ full acceptance ยังคง **Blocked** ตาม dependency/platform gate ไม่ปิดจากผล observational Windows
- #20 เป็น **In Progress** สำหรับ early operation-registration generator; full CLI/scaffolding/transport schemas/E2E และ benchmark ยังไม่ครบ ค่า full task test/benchmark gate จึงยัง Planned แม้ผล subset ข้างต้นผ่าน
- Umbrella features ยังคง **M0** และ actual person-hours เป็น null ไม่มีข้อมูลเวลาคนจริง
- CI ของ exact Engine revision: [W1 run](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/40509385311) และ [platform run](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/40509385312) ถูก GitHub ปฏิเสธทั้ง4jobsก่อน stepแรก โดยแจ้ง recent account payments หรือ spending limit ดู [raw CI evidence](../evidence/w1/hosted-ci.json) นี่เป็น infrastructure blocker ไม่ใช่ code-test failure หรือ CI pass

ไม่มี real HTTP/GraphQL/Worker/provider/tenant/identity/HA/E2E ของสาม sample lanes จากรอบนี้ กรณี disabled modules ตรวจเป็น zero module-owned recorder work ส่วน descriptors/registration metadata ต้องบริสุทธิ์และไม่สร้าง resources ผ่าน static fields หรือการ capture constructor ก่อน compile

[Experimental developer guide](../../public/guides/experimental-core-composition-codegen.md) · [Pinned executable consumer](https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples/tree/main/portable-core) · [Final consistency validation](../evidence/w1/final-validation.json)
