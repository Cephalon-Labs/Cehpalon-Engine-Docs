# สถานะและแผนทำงานต่อของ Engine วันที่ 23 พฤศจิกายน 2026

## สถานะที่ตรวจแล้ว

- `main` ของ Engine อยู่ที่ `f77c42b187483086e99a5ec5ade6bcd80b9ad738` และตรงกับ remote. หัวของ Docs คือ `768d624cad981f5d63ff9c5603d69070933abd77` และ Samples คือ `516861095f7950950ea8db8801596fa1ab194d67`. ทั้งสาม repository เป็น public และ Project 4 เป็น private.
- Engine ใช้ .NET 11 GA SDK 11.0.100 และ runtime 11.0.0. CI ตรงกับ Engine SHA นี้ผ่านสี่งานบน Windows Server 2025 และ Ubuntu 24.04. ผล contract checks คือ 1,540 และ 1,537 ตามลำดับ. อ่าน JSON ของ platform smoke แล้วพบ 12 ผ่านและ 2 `Not run` ต่อระบบ โดยทั้งสองรายการต้องใช้ PostgreSQL และ RabbitMQ จริง. [Contract CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/45158542258) · [Platform CI](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/45158542282)
- Project 4 มี 23 รายการ แบ่งเป็น Done 5, In Progress 2 (#18 และ #20), Blocked 7 (#3, #5–#9 และ #11) และ Backlog 9. ค่า maturity ใน Project เป็น M0 ทั้งหมด. [Project 4](https://github.com/orgs/Cephalon-Labs/projects/4)
- Core และ Composition มี contract tests. Protected HTTP และ GraphQL มีหลักฐานระดับตัวอย่างร่วมกับ PostgreSQL 18.7 จริงสำหรับ audit read โดยผ่าน HTTPS 20 กรณีต่อโหมด และปฏิเสธคำขอข้าม tenant สี่กรณีต่อโหมดก่อน SQL. CLI สร้าง portable console และ Small API ที่ build และรันได้. Business lane แบบ API + Worker + SQL และ AI + Retrieval lane ยังต้องส่งมอบหลักฐานครบตามเกณฑ์ของแต่ละ lane. [Audit validation](../validation/audit-read-statistics.md) · [แผนโครงการ](../planning/2026-10-27-program-plan.md)

## งาน #18 ที่เริ่มแล้ว

ทดสอบชุดแก้ histogram ที่มีอยู่ใน working tree จากสำเนาแยก ซึ่งสร้างบน Engine SHA ข้างต้นและตรวจ SHA-256 ให้ตรงกับไฟล์ต้นฉบับทั้งสี่ไฟล์. Locked Release build ด้วย SDK 11.0.100 ผ่าน Core 33 และ Composition 81 เคสบน Windows build 26300 และ WSL Ubuntu 22.04.5. การรัน WSL ครั้งแรกสะดุดที่วิธีส่งสคริปต์ก่อนเริ่มทดสอบ จึงเก็บ error และรันผ่านไฟล์สคริปต์ LF. ผลนี้เป็นหลักฐานเฉพาะชุดแก้ที่ยังไม่ commit.

การทดสอบเพิ่มเติมบน Windows เปิดสี่โปรเซสใหม่เพื่อแยกชุดควบคุมและ listener ที่โยน exception ใน `InstrumentPublished`. ชุดควบคุมของ Core และ Composition เรียก factory และ cleanup ครั้งละหนึ่งครั้งในแต่ละรอบ. เมื่อ listener โยน exception ตอนประกาศ histogram ครั้งแรก ทั้งสองส่วนเจอ `TypeInitializationException` และไม่เรียก factory. การลองซ้ำหลังถอด listener ยังได้ผลเดิม. ก่อนรวมชุดแก้ ให้เพิ่มเคสเริ่มต้นแบบโปรเซสใหม่และตรวจว่า dispatch, activation, rollback และ cleanup ทำงานได้ตามสัญญาเมื่อ listener ล้มเหลว. ให้กำหนดความหมายของการนับต่อ Core dispatch และยืนยันจำนวน observation ต่อ protected HTTP/GraphQL request ซึ่งอาจผ่าน dispatcher มากกว่าหนึ่งครั้ง.

เก็บแพตช์ที่ใช้ทดสอบ รายงานรายเคส และโปรแกรมตรวจ cold publication ไว้ใน `.local/continuation-20261123/` ของ Engine. SHA-256 ของแพตช์คือ `546d121f36ab2a11257b7e7ec5eeeccdfa16f7494bd6fc66e0335085f85cfda1e`. ผลชุดนี้ยังไม่ได้รวมเข้า Engine หรืออัปเดต GitHub Project.

การวัด audit-read collector ที่อยู่บน `main` ใช้ receipt lookup จริงของ Engine กับแหล่งข้อมูลจำลองที่ตอบผลว่างแบบ synchronous และปิด timeout. รันแบบเปิด/ปิดตัวนับ 12 คู่สลับลำดับบน Windows และ WSL โดยวัดครั้งละ 250,000 reads ต่อโหมดต่อคู่. นับรวม warmup แล้วมี 6.4 ล้าน reads และตัวนับรายงาน 3.2 ล้าน successes ตามคาดต่อระบบ. ทุก batch มีผล allocation 0 bytes ต่อ read บน thread ที่ใช้วัด.

| ระบบ | มัธยฐานของผลต่างเปิดลบปิด | ช่วงผลต่างทุกคู่ |
| --- | ---: | ---: |
| Windows build 26300 | +4.34 ns/read | −5.22 ถึง +21.89 ns/read |
| WSL Ubuntu 22.04.5 | +3.53 ns/read | −38.36 ถึง +33.93 ns/read |

ผลวัดเป็นค่าเฉลี่ยภายในแต่ละ batch และมีความผันผวน. ขอบเขตคือ receipt lookup แบบ thread เดียวสำหรับผลว่าง รวม fixture และการตรวจผลในวงรอบ. ตัวเลขนี้ยังใช้สรุป latency ของ HTTPS, PostgreSQL หรือการแชร์ counter หลาย thread ไม่ได้. ต้นฉบับ protocol, harness, input hashes และ JSONL ทุกคู่เก็บที่ `.local/continuation-20261123/collector/` ของ Engine. เกณฑ์ benchmark เดิมยังใช้กับแต่ละงานตามสัญญา.


## ลำดับงานถัดไปที่เสนอ

| ลำดับ | งาน | เกณฑ์ก่อนเดินต่อ |
| --- | --- | --- |
| เริ่มได้ในเครื่อง | [#18](../../tasks/18.md) ปิดช่องว่างหลักฐาน observability | ใช้ผลสังเกตของ collector เป็น baseline สำหรับแผนวัดแบบมีคำขอพร้อมกัน. จัดการปัญหา first publication ในชุด histogram และยืนยัน lifecycle กับ consumer ก่อนรวมชุดแก้. |
| ทำคู่กันเมื่อพร้อม | [#3](../../tasks/3.md) P0 platform proof | ใช้ Windows x64 ที่อยู่ในรายการรองรับและ PostgreSQL/RabbitMQ fixture แยกที่ล็อกเวอร์ชันและ artifact. รัน harness เดิมบน GA ให้ผ่าน 14/14, `Not run = 0` พร้อมข้อมูล OS, runtime, provider และ cleanup แล้วทบทวนเกณฑ์ #3 ทั้งหมดก่อนขยับสถานะ. |
| ต่อจาก platform proof | [#11](../../tasks/11.md) Small API และ [#20](../../tasks/20.md) Tooling | #11 ใช้ Linux x64 reference ที่จัดสรร 2 vCPU/2 GiB เฉพาะและ load generator แยก รันครบตาม protocol เดิม. สำหรับ #20 ตรวจ generated consumers และช่องว่างของเกณฑ์เต็ม พร้อมรักษาหลักฐาน variance เดิมและบันทึกเหตุผลก่อนรัน benchmark ใหม่. |
| ต่อจากงานฐาน | [#12](../../tasks/12.md) → [#14](../../tasks/14.md) → [#15](../../tasks/15.md) | พิสูจน์ provider SQL, tenant isolation และ transaction boundary ก่อนเพิ่ม durable eventing และ Worker. ให้ Business sample ยืนยัน idempotency, retry, recovery และ tenant isolation กับ provider จริง. |
| หลัง Business lane | [#16](../../tasks/16.md) → [#17](../../tasks/17.md) → [#22](../../tasks/22.md) | พิสูจน์ AI/Retrieval กับ provider จริงตามเกณฑ์การแยก tenant/เอกสารและงบทรัพยากร. เตรียม packaging หลัง #11/#15/#17/#20 พร้อมหลักฐาน. |

[ADR-0044 สำหรับ GA](../adr/ADR-0044-dotnet11-ga-baseline.md) · [ADR-0009 สำหรับ Small API reference](../adr/ADR-0009-small-api-conformance-and-measurement.md) · [ตาราง OS ของ Microsoft](https://github.com/dotnet/core/blob/main/release-notes/11.0/supported-os.md)
