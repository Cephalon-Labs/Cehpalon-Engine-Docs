# User request — 2026-10-27

Preserved source request. Later clarifications are recorded separately in program memory.

- ศึกการพัฒนา Software (kernel, engine, framework, logic, design pattern, architecture, server, operating system, standard) ต่างๆ และวิเคราะห์ข้อดีข้อเสีย และ feature/function ต่างๆเพื่อนำมาอ้างอิง
- ศึกษา .net11,12 และออกแบบ framework/engine ของเราให้ได้ดีที่สุด ครอบคลุม ครบถ้วน รองรับทุก business, logic, pattern, architecture และครอบคุมทุกด้าน
- ทำ standard สำหรับโลกอนาคตในการพัฒนา software ทุกประเภท ใน farmwork/engine ของเรา
- วางโครงสรัางเพื่อให้รองรับการสังงานโดย AI หลายเจ้า เช่น Cluade, Gimini, Gwen, DeppSeek และอื่นๆ
- จำทุกอย่างไว้จะได้ไม่ต้องเริ่มใหม่ทุกครั้งที่ทำงาน
- Username สำหรับ GitHub ที่ใช้คือ "Cephalon-Neza"
- ศึกษา วิเคาระห์ และวางแผน
- วางแผนัฒนา engine ของเราโดยใช้ Github Project (ชื่อ Project: Cehpalon-Engine)
- topology, pattern, transport, architecture ได้พวกนี้ ให้ developer เลือกใช้จาก farmework/engine เอานะครับ โดยใช้จากค่า config (appsettings) เพราะบาง project อาจจะทำแค่ api อย่างเดียว หรือบาง proect อาจจะมี api,graphql จะได้ไม่ทำงานเกินความจำเป็น โดย engine เราจะให้ developer ที่นำไปใช้เขียน code ชุดเดียว เวลาเปลี่ยน topology, pattern, transport, architecture จะได้ไม่ต้องแก้โค้ด และเขียนโค้ดชุดเดียวทำงานได้หลาย transport แล้วแต่จะกำหนดใน config
 - GitHub project, Milestone, Task/Card sync กับ repo: https://github.com/Cephalon-Labs/Cehpalon-Engine ส่วน https://github.com/Cephalon-Labs/Cehpalon-Engine-Docs ไว้เก็บเอกสารต่างๆ ที่เป็น .md (รวมถึง task/card .md)
 - Task/Card ต้องระบุ Labels, Type, Priority 
 - ใน Task/Card ให้ให้มี  commit id ของ https://github.com/Cephalon-Labs/Cehpalon-Engine ทุกครั้งที่มีการ commit เพื่อจะได้ trace ได้ภายหลัง ส่วน repo อื่นไม่ต้องอ้างอิง commit id เพราจะ trace แค่ farmework/engine เท่านั้น

เป้าหมาย framework
- Host-agnostic
- รองรับ Multitenancy ทุกอย่าง
- Observability
- AI และ Agentics
- Retrieval
- Identity
- รองรับ Eventing ทุกอย่าง
- Data/Document รองรับ Database ทุกประเภท
- รองรับการทำ Driven ทุกประเภท
- Cache รองรับ Cache ทุกประเภท
- Transports รองรับ การทำ API, GraphQL, Grpc, JsonRpc, SSE
- รองรับการทำ Worker 
- รองรับการทำงานหรือ deploy ทุกรูปแบบ Server/Serless, Edge, Cloud native, Traefik, Kubernetes, Docker อื่นๆในอนาคต
- Core system ที่เข็งแรงปลอดภายและ performance ดี
- มี performance, security และ standard ขั้นสูง
- CLI & scaffolding
- Codegen
- รองรับการนำไปใช้กับ project ทุกขาดตั้งแต่เล็ก-ใหญ่มาก และทำงานได้่แบบบ single, multi, scaling, autoscaling หรืออื่นๆ
- framework/engine ของเราต้องแข็งแกร่งและยืดหยุ่น ปลอดภัย และรวดเร็ว
- developer สามารถเลือกได้ว่าจะใช้อะไรบ้างใน framework/engine ของเรา ซึ่่งเราจะเตรียมพร้อมไว้ให้ทุกอย่าง
- ทำให้เป็น framework/engine ในอนาคต อีก 30-50 ยังใช้งานได้ดี
- ทำให้เหนือกว่า framework/engine ทุกภาษาที่มีในท้องตลาดในทุกๆด้าน
- ทำให้ไม่มีขึดจำกัดในการพัฒนา
- ทำให้ผุ้นำ framework/engine ไปใช้กับ project ต่างๆ เขียนโค้ดน้อยลง เพื่อให้ focus ที่ bussiness logic ของ project เขาอย่างเดียว และเลือกใช้ feature ใน framework/engine ของเรา
- เตรียมการเพื่อ publish framework/engine ของเราไปยัง nuget
- เขียนโค้ดชุดเดียวได้ transport หลายแบบ เมื่อปรับเปลี่ยนโครงสร้างไม่ต้องแก้โค้ดใหม่
- Event รองรับการทำ scaling
- อะไรที่สำคัญและเป็นกฎเก็บลงใน SKILL.md เพื่อให้ ai agent ได้ใช้ร่วมกัน

แบ่ง folder หลักออกเป็น 3 ส่วน ดังนี้ แต่ละส่วน ใช้ คนละ git repository กัน

1. Cehpalon-Engine/ สำหรับการพัฒนา framework/engine (https://github.com/Cephalon-Labs/Cehpalon-Engine)
 - src/
 - Tests/ (อาจจะแยกเป็นหลาย project เพื่อให้ทำงานได้เร็วขึ้น เมื่อ framework/engine เราใหญ่ขึ้น)
 - Benchmarks/ (อาจจะแยกเป็นหลาย project เพื่อให้ทำงานได้เร็วขึ้น เมื่อ framework/engine เราใหญ่ขึ้น)
 - อื่นๆ ที่จำเป็น

2. Cehpalon-Engine-Docs/ (https://github.com/Cephalon-Labs/Cehpalon-Engine-Docs) สำหรับจัดการเอกสารของ framework/engine และ Sync กับ GitHub project/tasks/milestone ให้แบ่ง folder ให้ชัดเจนเพื่อนำไปเป็นเอกสาร
 - Sync กับ GitHub project
 - Sync กับ GitHub milestone
 - Sync กับ task/card ใน GitHub project โดยระบุ attribute ให้่ครบถ้วน รวมถึง man-hour และ sub task หรือ feature
 - สถานะของ Task/Card ไหนต้องมี test และเข้าสูสถานะ test และทำการทดสอบว่าผ่านหรือไม่ผ่าน ถ้าไม่ผ่านก็แก้ไข code แล้ว test จนผ่าน
 - สถานะของ Task/Card ไหนต้องมี benchmark และเข้าสูสถานะ benchmark ละทำการทดสอบว่าผ่านหรือไม่ผ่าน ถ้าไม่ผ่านก็แก้ไข code แล้ว test จน benchmark ผ่าน
 - แต่ละ Task/Card ให้เก็บเป็นไฟล์ .md เป็นแต่ละไฟล์ เพื่อจะได้ลงรายละเอียดและอัปเดทสถานะได้ (กำหนดชื่อไฟล์เป็นชื่อเดียวกับ Task/Card id)
 - แต่ละ Task/Card แยกให้ชัดเจินว่าเป็น feature, bug หรืออื่นๆ และให้มี reference ถึง Feature/Function หลักหรือเอกสารที่เกี่ยวข้อง
 - ถ้า task/card ไหนที่ close ไปแล้ว แล้วมีการแก้ไขหรือเปลี่ยนรูปแบบ ให้ทำการนำมาแก้ไข card นั้น เพื่อจะได้มีต้องสร้าง card ใหม่เพืยงเพิ่ม note เข้าไปว่าจากเดิมเป็นอย่างไรและทำไมต้องเลี่ยนแปลง
 - กำหนด สถานะ M0-M4 ของแต่ละ feature ตามการทำงานได้จริงและผ่านการทดสอบจริง
 - การคุยกันทุกครั้งให้เก็บเข้าไว้ใน memory .md เพื่อจะได้ไม่คุยกันเรื่องเดิมซ้ำและจะได้วิเคราะห์แนวทางได้
 - การเก็บเอกสารแยก Folder กันชัดเจน folder ไหนเป็นข้อมูลภายใน framework/engine ตัวไหนจะทำเป็นเอกสารเพื่อเปยแพร่  เพื่อนำไปทำเป็นเอกสารการใช้งาน framework/engine ของเรา และในอนาคตจะใช้โปรแกรมเพื่อ generate จาก .md เป็น website (ในอนาคตจะใช้ Astro ในการทำ) เพื่อทำเป็นเอกสารสำหรับนักพัฒนาที่ต้องการใช้งาน framework/engine ของเราในการทำ bootstrap ของโปรเจคของเขา
 - โดยทั้ง code และ docs ใน  Cehpalon-Engine/ และ Cehpalon-Engine-Docs/ จะต้องสอดคล้องกัน ถ้าแก้ไขฝั่งใดฝั่งหนึ่งจะต้องอัปเดทให้ตรงกันเสมอ
 - ใน task/card รวมถึง ให้อ้างอิง commit id จาก https://github.com/Cephalon-Labs/Cehpalon-Engine ทุกครั้งที่ commit ของ repo นี้ ส่วน repo อื่นไม่ต้องอ้างอิง เพราะเราต้องการ track แค่ตัว framework/engine อย่างเดียว

3. Cehpalon-Engine-Samples/ (https://github.com/Cephalon-Labs/Cehpalon-Engine-Samples) เป็น project สำหรับทดสอบ Cehpalon-Engine/ การทำงานจริง(End-to-End) อาจะจะมีหลายๆ project ย่อยในนี้ เพื่อให้การทดสอบจริงคลอบคลุมทุกอย่าง

spawn agent มาช่วยได้เลย ไม่ว่าจะเป็น
 - Architecture
 - Software Engineer
 - Developer
 - QA
 - PM
 - Research
 - DevOps
 - Security
 - Marketing
 - Network Engineer
 - หรือ role อื่นๆ เพื่อให้งานออกออกมามีประสิทธิภาสูงสุด

-- มีคำถามหรือข้อเสนอแนะอะไรไหม