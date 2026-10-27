# W0 — SDK/driver/artifact qualification และ two-way tracking

วันที่: 2026-10-27 (Asia/Bangkok). Related Engine issues #3 และ #23

## ผลที่ตรวจจริง

| ส่วน | หลักฐานและขอบเขต |
| --- | --- |
| SDK11 RC3 | ดาวน์โหลด Windows/Linux archives, ตรวจ actual SHA512 ตรง official metadata, แตกใน private `.tools` และ pin `global.json`; ไม่แทน global SDK |
| Driver/platform | Locked restore/build พร้อม63 packages; HTTPS/JWT/GraphQL และ PostgreSQL/RabbitMQ fixture smoke14/14 บน Windows26H2 และ WSL Ubuntu22.04.5; zero skipped provider checks ใน owned mode |
| Host support | Ubuntu22.04.5 อยู่ในตารางที่ตรวจ; Windows26H2 ของเครื่องนี้ยังไม่อยู่ในตาราง จึงเป็น observational compatibility ไม่ใช้แทน supported-Windows qualification |
| Artifacts | Model GGUF ทั้งสองและ inference archives ตรวจ actual bytes/hash แล้ว; container registry index/platform/config lockครบ5images และ primary pull/ตรวจ installed config/OS/Java/Erlang/start/probe จริง |
| Inference runners | Ollama version smokeผ่าน; llama.cppต้อง app-local libgomp จาก signed Ubuntu metadata แล้ว version/help/ldd ผ่าน Actual versionstringเป็น0.7.0-dev/build11669 ต้องเก็บร่วมกับ release alias/digest ไม่มี modelserver/inference/quality run |
| Two-way sync | Reviewed plan/dry-run/guarded apply/readback/checkpoint/resume, native issueและProject metadata, explicit identity mapping และ Engine-only SHA validation; create/deleteไม่มี |
| Tool tests | Offline59/59 ผ่านทั้งWindowsและWSL Linux พร้อม real-Git byte-preservation test; independent repair repro4/4 และ live #23 roundtrip/stale-Project rejection/restoration ผ่าน |

SDK/driver smokeไม่ใช่ Engine Core/composition/tenancy/ธุรกิจ/AI/E2E/HA/performance/production proof ทุก Engine runtime feature ยังM0

## Hosted CI blocker และสถานะงาน

GitHubปฏิเสธทั้ง Linux/Windows jobs ของ Engine และ Docs **ก่อนขั้นตอนแรก** โดยแจ้ง recent account payments หรือ spending limit ผลนี้เป็น **Blocked infrastructure** ไม่ใช่ code-test failure และไม่ใช่ CI pass ดู [exact-source CI evidence](../evidence/w0/qualification/hosted-ci-blocker.json)

- #3 ยังเปิดเป็น **Blocked**: local/artifact workเสร็จตามขอบเขตที่รายงาน แต่ supported-Windows/hosted qualificationยังไม่มี เพราะเครื่องlocalเป็น26H2ที่ไม่อยู่ในรายการ และ hosted jobsยังไม่เริ่ม ต้องปลด account CI blockerหรือมี supported hostที่ได้รับอนุญาตก่อนรับรองส่วนนั้น
- #23 ปิดเป็น **Done** หลัง tool/local tests/live API qualification และ guarded final sync/readback ผ่านตาม acceptance criteria สถานะ Doneของงานเครื่องมือไม่ใช่ hosted-CI pass; account CI blockerยังอยู่และรายงานไว้
- W0 milestoneยังเปิดเพราะ #3คงเหลือ ไม่เปลี่ยน billing/spending configuration หรือ public/NuGet publication

## รายงานและวิธีทำซ้ำ

- [Engine harness/pins/license/retained failures](https://github.com/Cephalon-Labs/Cehpalon-Engine/blob/main/Tests/PlatformQualification/README.md) และ [Engine qualification summary](https://github.com/Cephalon-Labs/Cehpalon-Engine/blob/main/Tests/PlatformQualification/evidence/qualification-summary.json)
- [Artifact source/byte/dependency report](../evidence/w0/artifacts/qualification-report.md)
- [Live two-way sync report](../evidence/w0/qualification/live-sync-roundtrip.json) และ [sync usage](../standards/tracking-sync-usage.md)
- [Final validation](../evidence/w0/qualification/final-validation.json) และ [tool test record](../evidence/w0/qualification/tool-tests.json)
- [Engine commit journal](../evidence/w0/qualification/engine-commit-journal.md)

เก็บ raw failures/corrections ไม่ลบหรือเปลี่ยนผลเดิม: Schannel ephemeral-key fixtureแก้เป็น scoped temporary user key/custom root trust; Rabbit ack oracleเพิ่ม close barrier+independent channel; signed NuGet archivehashแยกจากcontentHash; qdrantต้องใช้v-tag; llamaขาดlibgompแก้app-local; sync checkpoint/milestone/EOL guardsแก้พร้อมregression ไม่มีการปรับ performance thresholdเพื่อให้ผ่าน เพราะรอบนี้ไม่รัน benchmark

## License และข้อจำกัดที่ต้องส่งต่อ

GraphQL graph มี `ChilliCream.Nitro.App32.0.2` พร้อม ChilliCream License1.0 แม้ไม่เปิด IDE ไม่เรียกทั้งgraphว่าMIT-onlyหรือdistribution-cleared ต้องทำ release/license reviewใน #22 ก่อนแจกจ่าย ส่วนใบอนุญาต Engine/Docs/SamplesยังMIT

Custom-CA HTTPSไม่ใช่ public PKI/revocation proof; fixture JWTไม่ใช่ real OIDC browser/key rotation; provider linksในfixtureเป็นloopback plaintext; one-node Rabbit quorum smokeไม่ใช่HA/restart/exactly-once; model byteidentity/runnerversionไม่ใช่model quality/tool/cancellation conformance งานเหล่านี้อยู่ใน implementation/provider/sample tasksของตนเอง

เครื่องมือซิงก์ใช้ optimistic guardsเพราะ GitHubไม่มี cross-service transaction/CAS ครอบ issue+Project และ localfilebatchเป็นrecoverabletransaction ข้อจำกัดของexternalwritersระบุในusage; ไม่มีforce-overwriteอัตโนมัติเมื่อเจอthird state

Cleanup เดิมของ owned fixtures สำเร็จและมีหลักฐานใน Samples; final check ยืนยัน ports ยังปิดและ private state ไม่มี password/token ปัจจุบัน แต่ Docker API สำหรับตรวจรายชื่อ container/network ซ้ำคืน Internal Server Error จึงบันทึกสองรายการนี้เป็น Unavailable ไม่อ้าง fresh container absence proof และไม่ restart shared Docker service ผลตรวจใน [final validation](../evidence/w0/qualification/final-validation.json) แยก limitation นี้ไว้
