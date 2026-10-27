# มาตรฐานการส่งมอบ หลักฐาน และระดับความพร้อม

วันที่: 2026-10-27
สถานะ: **Proposed — ข้อเสนอมาตรฐานวิศวกรรมสำหรับโครงการใหม่**

เอกสารนี้กำหนดแนวทางที่เสนอให้ใช้กับ Cehpalon-Engine, Cehpalon-Engine-Docs และ Cehpalon-Engine-Samples การมีแผน เอกสาร หรือ task ไม่ถือเป็นหลักฐานว่าพัฒนา ทดสอบ หรือใช้งานจริงสำเร็จแล้ว ค่าเริ่มต้นของ feature ที่ยังไม่มีหลักฐานคือ M0

## 1. หน่วยที่ใช้ประเมินความพร้อม

ประเมินเป็นราย **feature × provider × version × host/deployment profile** พร้อม revision และวันที่ของหลักฐาน ตัวอย่างเช่น ผลของ PostgreSQL บน Linux ไม่ใช้ยืนยัน SQL Server หรือ Kubernetes และผลของ API ไม่ใช้ยืนยัน Worker

แยกสถานะงานออกจากระดับความพร้อม: task ที่เป็นงานวิจัยอาจ Done ได้ตาม acceptance criteria ขณะที่ feature ยังเป็น M0 การปิด task หรือ milestone ไม่ยกระดับ maturity โดยอัตโนมัติ

| ระดับ | ความหมาย | หลักฐานขั้นต่ำที่เสนอ |
| --- | --- | --- |
| M0 | Planned / Experimental | มีข้อกำหนด แผน หรือโค้ดทดลอง แต่ยังไม่ครบเกณฑ์รับรองระดับถัดไป; ระบุสิ่งที่ทราบ สิ่งที่ยังไม่พิสูจน์ และเงื่อนไขเลื่อนระดับ |
| M1 | Component verified | สัญญาการทำงานและขอบเขตชัดเจน; unit/contract tests ผ่าน รวมกรณีผิดพลาด การยกเลิก และขอบเขตความเชื่อถือที่เกี่ยวข้อง; ผูกผลกับ Engine revision และ dependency versions |
| M2 | Integrated | ใช้ provider จริงสำหรับขอบเขตที่อ้างรองรับ; Samples ผ่าน end-to-end รวม configuration, lifecycle, failure และ cleanup; พิสูจน์ identity/tenant isolation เมื่อเกี่ยวข้อง; มีหลักฐาน CI บน revision ที่อ้าง |
| M3 | Operationally verified | ผ่าน M2 พร้อมหลักฐาน performance, security, observability และ recovery ตาม host/deployment profile; ผ่าน install/start/stop, upgrade/rollback และ fault scenarios ที่ประกาศไว้; มีคู่มือปฏิบัติการและข้อจำกัด |
| M4 | Production proven | ผ่าน M3 และมีหลักฐานใช้งานจริงตามช่วงเวลา ภาระงาน SLO และเกณฑ์เหตุขัดข้องที่กำหนดล่วงหน้า; มีผู้รับผิดชอบดูแล compatibility, vulnerability response และ maintenance |

ทุกระดับต้องมีหลักฐานตรวจซ้ำได้ เกณฑ์ที่ไม่เกี่ยวข้องต้องระบุเหตุผล `Not required` ห้ามเว้นเงียบ ๆ การเปลี่ยน dependency, provider, contract หรือ runtime behavior ต้องประเมินว่าหลักฐานส่วนใดยังใช้ได้ ไม่สืบทอดระดับเดิมโดยไม่มีเหตุผล เมื่อหลักฐานเดิมไม่ครอบคลุมให้ระบุ `Revalidation required` และงดอ้างระดับนั้นสำหรับขอบเขตที่เปลี่ยน

## 2. บทบาทของ repository และแหล่งข้อมูลหลัก

- **Engine:** source, Tests, Benchmarks, GitHub issues และ milestones ของงาน Engine
- **Docs:** ข้อกำหนด ADR มาตรฐาน หลักฐาน สรุปการตัดสินใจ และ Markdown mirror ของ task
- **Samples:** consumer และ end-to-end scenarios ที่ใช้ยืนยันการนำ Engine ไปใช้จริงตามขอบเขตที่ประกาศ
- **GitHub Project `Cehpalon-Engine`:** มุมมองติดตามงานที่เชื่อมกับ Engine issues

ใช้ GitHub issue number เป็นรหัส task คงที่ และเก็บ mirror ที่ `tasks/<issue-number>.md` เช่น `tasks/6.md` โดยไม่เติมเลขศูนย์ด้านหน้า เก็บ Project item ID เป็นข้อมูลเชื่อมเสริม ไม่ใช้แทน issue number

GitHub เป็นแหล่งสถานะ issue/milestone/Project ส่วน Docs เป็นแหล่งรายละเอียดข้อกำหนด การตัดสินใจ และหลักฐาน ก่อน sync ให้ดึงสถานะล่าสุดและตรวจความขัดแย้ง ห้ามเขียนทับข้อมูลใหม่ด้วย snapshot เก่า หาก conflict ต้องแสดง field ที่ขัดกันและให้ผู้รับผิดชอบตัดสิน ไม่สร้าง issue ซ้ำเพียงเพื่อให้ sync ผ่าน

## 3. ข้อมูลขั้นต่ำของ Task/Card

ใช้ native **Issue Type** สำหรับประเภทงาน และ custom field **Priority** ใน Project ทั้งสองอย่างแยกจาก Labels หากระบบหรือสิทธิ์ไม่รองรับ ต้องบันทึกข้อจำกัดให้ชัดเจน การเขียนคำว่า Type/Priority ใน body เพียงอย่างเดียวไม่ถือว่าตั้งค่า native/custom field สำเร็จ

| ข้อมูล | ความหมายและกติกา |
| --- | --- |
| Issue number / URL | รหัสและลิงก์ของ Engine issue; ยังไม่สร้างให้เป็น `null` และระบุว่าเป็นร่าง |
| Title / Issue Type | ชื่อที่สื่อผลลัพธ์; ประเภท Feature, Bug หรือ Task ตามชนิดที่ตั้งค่าในองค์กร |
| Labels | ใช้จัดหมวด area/provider/transport หรือบริบทอื่น โดยไม่ใช้แทน Issue Type หรือ Priority |
| Priority | ค่าเสนอ P0–P3: P0 งานขัดขวางร้ายแรงที่ต้องจัดการก่อน, P1 งานสำคัญของ milestone, P2 งานปกติที่จัดลำดับแล้ว, P3 งานเลื่อนออกได้; แยก priority ออกจาก security severity |
| Status / Blocked reason | ขั้นตอนงานและเหตุที่ขวาง พร้อมผู้รับผิดชอบหรือเงื่อนไขปลด blocker |
| Milestone / Owner | เป้าหมายการส่งมอบและผู้รับผิดชอบ; ถ้ายังไม่กำหนดให้เป็น `null` |
| Parent / Sub-issues / Dependencies | ความสัมพันธ์ของงานและสิ่งที่ต้องพร้อมก่อนเริ่มหรือปิดงาน |
| Feature / Requirement / ADR references | ลิงก์ไปยังความสามารถหลัก ข้อกำหนด และการตัดสินใจที่งานนี้ทำให้เกิดขึ้น |
| Scope / Acceptance criteria | สิ่งที่ส่งมอบ เงื่อนไขรับงานที่ตรวจได้ และขอบเขตที่ยังไม่ครอบคลุม |
| Estimated hours | ประมาณชั่วโมงคน พร้อม assumptions และช่วงความไม่แน่นอน; ยังประเมินไม่ได้ใช้ `null` |
| Actual hours | เวลาที่บันทึกจริงพร้อมที่มา; ไม่ทราบใช้ `null` ไม่ใช้ 0 แทนข้อมูลที่ขาด และไม่แปลงเวลา AI/CI เป็นชั่วโมงคนโดยอัตโนมัติ |
| Remaining estimate | ประมาณงานคงเหลือ แยกจาก estimate เริ่มต้นและ actual; ไม่ทราบใช้ `null` |
| Test required / Result / Evidence | ระบุความจำเป็น ผล และลิงก์หลักฐาน; `Not required` ต้องมีเหตุผล |
| Benchmark required / Result / Evidence | ระบุความจำเป็น เกณฑ์ ผล และลิงก์หลักฐาน; `Not required` ต้องมีเหตุผล |
| Maturity before / Target / Observed | แยกระดับเดิม เป้าหมาย และระดับที่หลักฐานรองรับจริง พร้อม provider/version/profile |
| Engine commit journal | full commit SHA ของ Engine พร้อมเหตุผล ผลต่อพฤติกรรม และ issue ที่เกี่ยวข้อง |
| Change notes | ประวัติข้อกำหนดหรือรูปแบบที่เปลี่ยน: เดิมเป็นอย่างไร เปลี่ยนเป็นอะไร เหตุผล และหลักฐานที่ต้องทดสอบใหม่ |

ทุก Engine commit ต้องถูก trace ใน Engine issue ที่เกี่ยวข้องและ mirror ของ task หลังทราบ full SHA ให้บันทึกทันที ไม่เติม SHA ที่คาดเดาไว้ก่อน commit การอ้าง commit เพื่อ tracking ใน task/card และ commit journal ใช้ **Engine SHAs เท่านั้น** ไม่บันทึก Docs/Samples SHAs ใน journal ดังกล่าว ส่วนข้อมูลล็อก source/dependency ที่จำเป็นต่อการทำซ้ำให้เก็บใน evidence manifest แยกต่างหาก

งานที่ปิดแล้วแต่มีการเปลี่ยน behavior/design ของงานเดิม ให้ reopen และปรับ card เดิมพร้อม change notes โดยคงประวัติก่อนหน้า ไม่สร้าง card ซ้ำเพื่อปกปิดการเปลี่ยนหรือผลทดสอบที่ไม่ผ่าน

## 4. Workflow ของ Project

สถานะที่เสนอ: **Backlog, Ready, In Progress, Review, Test, Benchmark, Blocked, Done**

| สถานะ | เงื่อนไขการใช้ |
| --- | --- |
| Backlog | รับความต้องการไว้แล้ว แต่ scope/ลำดับ/dependencies ยังไม่พร้อม |
| Ready | scope, acceptance criteria, priority, owner และแผนตรวจรับชัดเจน; dependencies ที่ต้องใช้เริ่มงานพร้อม |
| In Progress | กำลังทำงานตาม scope พร้อมอัปเดตข้อค้นพบและสิ่งที่ยังไม่พิสูจน์ |
| Review | มีผลลัพธ์ที่ตรวจได้ พร้อมการตรวจ code/design/docs ตามลักษณะงาน |
| Test | รันและทบทวนการทดสอบตาม matrix ที่กำหนด; ผลไม่ผ่านต้องแก้และทดสอบผลกระทบที่เกี่ยวข้องใหม่ |
| Benchmark | งานต้องวัด performance และกำลังตรวจตาม protocol/threshold ที่ประกาศก่อนเห็นผล |
| Blocked | ไม่สามารถเดินหน้าขั้นที่จำเป็นได้; บันทึกเหตุ เงื่อนไขปลด blocker และสถานะที่จะกลับไป |
| Done | acceptance criteria ผ่านครบ หลักฐานตรง revision งาน review เสร็จ และ code/docs/samples/task mirror สอดคล้องกันในส่วนที่เกี่ยวข้อง |

เส้นทางทั่วไปคือ `Backlog → Ready → In Progress → Review → Test → Benchmark → Done` ข้าม Test หรือ Benchmark ได้เฉพาะเมื่อบันทึก `Not required` พร้อมเหตุผลที่เหมาะกับงาน งานแก้ไขย้อนกลับไปขั้นที่จำเป็นได้ โดยไม่ลบประวัติผลเดิม

CI ที่เริ่มไม่ได้จากสิทธิ์ โครงสร้างพื้นฐาน หรือข้อจำกัดค่าใช้จ่ายเป็น **Blocked** ไม่ใช่ test pass และไม่ใช่หลักฐาน code failure การผ่าน local tests ต้องบันทึกว่าเป็น local proof และไม่ใช้แทน hosted CI ที่ยังไม่รัน

## 5. กติกาการทดสอบ

1. ระบุสิ่งที่จะพิสูจน์และ matrix ก่อนลงมือ: feature/provider/version/OS/host/profile รวม positive, negative, cancellation และ failure scenarios ที่เกี่ยวข้อง
2. แยก unit, contract, integration, end-to-end, security และ operational checks ตามสิ่งที่แต่ละชุดพิสูจน์ได้ ไม่สรุปครอบคลุมเกินหลักฐาน
3. ผลต้องระบุ Engine revision, dependency locks, environment, คำสั่งหรือขั้นตอนทำซ้ำ, จำนวนที่รัน/ผ่าน/ไม่ผ่าน/ข้าม และเหตุผลที่ข้าม
4. ทดสอบบน revision ที่ส่งมอบจริง หากแก้ source หลังผลเดิม ให้ทดสอบสิ่งที่ได้รับผลกระทบและอัปเดตหลักฐาน ห้ามนำผลของ source เก่ามารับรอง source ใหม่โดยไม่อธิบาย
5. เก็บผลที่ไม่ผ่านและการแก้ไขไว้ แก้และทดสอบซ้ำจนผ่านเกณฑ์ หรือระบุ blocker/ข้อจำกัดอย่างตรงไปตรงมา การเปลี่ยนเกณฑ์ต้องมีเหตุผลที่ตรวจได้และไม่ย้อนหลังทำให้ผลเดิมกลายเป็นผ่าน
6. พิสูจน์ด้าน lifecycle: module ที่ปิดต้องไม่มี factory/constructor/provider connection/endpoint/background work ของ module นั้นตามขอบเขตที่ออกแบบไว้
7. งาน tenant/identity ต้องมีกรณีข้าม tenant, สิทธิ์ไม่พอ, credential/context ไม่ถูกต้อง และ resource cleanup ตามความเกี่ยวข้อง
8. ข้อมูลทดสอบต้องไม่ปะปนกับ production และ raw evidence ต้องไม่มี secrets; ระบุสิ่งที่ redacted และรักษาข้อมูลที่จำเป็นต่อการตรวจผล

ไม่จำเป็นต้องสร้างชุดทดสอบใหม่สำหรับการแก้เอกสารหรือการเปลี่ยนที่ไม่กระทบ behavior เพียงเพื่อเพิ่มจำนวน tests ให้เลือกวิธีตรวจที่พิสูจน์ความเสี่ยงจริง เช่น ตรวจลิงก์ schema หรือความสอดคล้องของเอกสาร

## 6. กติกา Benchmark และการอ้าง Performance

- กำหนด protocol ก่อนรัน: baseline, metric, workload, topology, provider, dataset, hardware, OS/runtime, build configuration, concurrency, warmup, sample size, repetition และ threshold
- ระบุว่าเป็น cold/warm, latency/throughput/allocation หรือ resource usage และระบุชั้นที่วัด เช่น compiler, host, handler หรือ end-to-end ห้ามนำผลชั้นหนึ่งไปอ้างอีกชั้นหนึ่ง
- เก็บ raw results, source/manifest/hash และวิธีวิเคราะห์เพื่อทำซ้ำ รวมรอบ invalid และ preparation failures โดยไม่แทนที่ข้อมูลเดิมด้วยรอบใหม่
- ห้ามเลือกเฉพาะรอบดี ตัด outliers เปลี่ยน threshold หรือเลือก rerun หลังเห็นผลเพื่อทำให้ผ่าน หาก protocol ไม่สมบูรณ์ให้ระบุ invalid พร้อมเหตุผล ประกาศ protocol ใหม่และเก็บหลักฐานเดิม
- ความถูกต้อง การแยก tenant และข้อกำหนดความปลอดภัยต้องยังผ่านเมื่อวัด performance ผลเร็วขึ้นจากการตัดการตรวจที่จำเป็นไม่ถือว่าผ่าน
- การเปรียบเทียบต้องใช้ขอบเขตและเงื่อนไขเทียบกันได้ พร้อมข้อจำกัด ห้ามอ้างว่าเหนือกว่าทุก framework/ภาษา หรือรองรับภาระงานทุกแบบจาก benchmark เฉพาะกรณี
- เมื่อมี failure หรือความไม่แน่นอน ให้รายงานตามข้อมูลจริงก่อนตัดสินผ่าน/ไม่ผ่าน ไม่สร้างตัวเลขแทนค่าที่ไม่ได้วัด

## 7. Sample lanes ที่ต้องวางแผนและรับรองแยกกัน

ผู้ใช้กำหนดให้มี **ทั้งสาม lane** ในแผน แต่ละ lane ต้องมี task, acceptance criteria และหลักฐานของตนเอง ความสำเร็จของ lane หนึ่งไม่ใช้แทนอีก lane

| Lane | เป้าหมายการพิสูจน์ | ขอบเขตสำคัญ |
| --- | --- | --- |
| Small API | project ขนาดเล็กใช้ API และเฉพาะ module ที่จำเป็น | setup/bootstrapping, request/response/error/cancellation, observability และ zero activation ของ GraphQL/Worker ที่ปิด |
| Multitenant API + Worker + SQL | ธุรกิจเดียวทำงานผ่าน API/Worker กับ SQL provider ที่เลือกและประกาศไว้ | tenant/identity isolation, transaction boundary, idempotency/retry, worker lifecycle, failure/recovery และการ scale ตาม profile ที่อ้างรองรับ |
| AI + Retrieval | เรียก AI provider และ retrieval flow ภายใต้สัญญา Engine | provider capability/streaming/cancellation, retrieval authorization, tenant/document isolation, timeout/rate-limit/cost controls และความแตกต่างระหว่าง mock proof กับ provider จริง |

การใช้ business handlers/contracts ร่วมกันต้องพิสูจน์ใน profile และ transport ที่ประกาศรองรับจริง หาก semantics ต่างกันจนต้องมี adapter/contract เฉพาะ ให้เปิดเผยข้อจำกัดและทดสอบตามนั้น ไม่อ้างว่าการเปลี่ยน config ทำให้ behavior ที่ต่างกันกลายเป็นเทียบเท่าโดยอัตโนมัติ

## 8. เกณฑ์จบงานและรายงาน

ก่อน Done ให้ตรวจว่า requirements, implementation, tests, benchmarks, Samples และเอกสารใช้งานสอดคล้องกันตามขอบเขตงาน พร้อม Engine SHAs และหลักฐานที่ตรวจย้อนกลับได้ ระบุสิ่งที่ยังไม่ได้พิสูจน์และงานติดตามอย่างชัดเจน

รายงานต้องแยก **ข้อเท็จจริงจากแหล่งข้อมูล / การตัดสินใจที่รับแล้ว / ข้อเสนอ / สิ่งที่ยังไม่ยืนยัน** ไม่ใช้จำนวน commits/tests/cards เป็นตัวแทนคุณภาพหรือความพร้อมใช้งานจริง

การเปลี่ยนมาตรฐานนี้ให้บันทึกเหตุผลและผลกระทบต่อ task/หลักฐานเดิมก่อนนำไปใช้ การอนุมัติแผนไม่ทำให้ feature ผ่าน gate และไม่ใช่การอนุมัติ publish NuGet หรือ public release โดยอัตโนมัติ
