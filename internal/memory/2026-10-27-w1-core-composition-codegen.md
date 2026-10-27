# W1 continuation — portable Core/Composition/code generation

คำขอผู้ใช้: ทำ W1 ส่วนที่เดินต่อได้โดยไม่รอ Windows qualification ให้ agent ช่วยพัฒนา Core/Composition ทดสอบและซิงก์ GitHub/Docs และใช้ code generation ส่วน #3 ต้องคง Blocked จนมี supported-Windows proof

## ข้อสรุปและ revision ที่ตรวจแล้ว

- Current workspace คือ `D:\Cephalon\{Cehpalon-Engine,Cehpalon-Engine-Docs,Cehpalon-Engine-Samples}`; private/MIT, Git author/committer Cephalon-Neza, Project4/original23issues ไม่ใช้ historical implementations/Project3
- [ADR-0005](../adr/ADR-0005-w1-portable-core-composition.md) แยก portable development ออกจาก full platform acceptance โดยไม่ลบ #5→#3 / #6→#5; [ADR-0006](../adr/ADR-0006-incremental-operation-code-generation.md) ระบุ early operation-generator subset ของ #20 โดยไม่ย้าย W5 milestone หรืออ้างว่าส่ง CLI/scaffolding แล้ว
- Engine `fee491cecaba04232207a1a2884057498e81213e`: Core/Composition BCL-only, typed lazy owned dispatch, strict schema1 immutable graph/lifecycle และ Roslyn incremental typed registration generator มี exact-clean-commit Release proofs บนทั้งสอง host: Core32 + Composition80 + Codegen42 =154/154 รวม actual compiler fixture ไม่มี Roslyn ใน consumer runtime
- Samples portable-core pin Engine SHA ข้างต้น ใช้ business handler เดียวกับ generated registry และ JSON3profiles ผ่าน5/5ต่อhost เป็น in-process module recorders ไม่ใช่ API/GraphQL/Worker/provider/tenant/identity/E2E ของสาม real sample lanes
- SDK11.0.100-rc.3.26522.148/runtime11.0.0-rc.3.26522.148 ไม่เปลี่ยน globalSDK Windows11Pro26H2/build26300.9711 ยัง observational/unlisted; WSLUbuntu22.04.5/glibc2.35 เป็น listed distribution แต่ไม่ใช่ native deployment certification

## Gates และสถานะ

- #3 ยัง OPEN/Blocked/Test gateBlocked โดย body/fields เดิมไม่ถูกเปลี่ยนจาก W0
- #5/#6 ส่งมอบ portable subset แล้วแต่ full acceptance **Blocked** ตาม platform/dependency gate; local component Test/Benchmark gates Passed แบบ scoped ไม่ใช่ hostedCI pass
- #20 InProgress, full task Test/Benchmark Planned เพราะ CLI/scaffolding/transport schemas/E2E และ generator-speed benchmark ยังไม่ครบ แม้ early registry generator ผ่าน
- #7/#8 ยังไม่ได้ implement; OperationContext เป็น correlation metadata ไม่ใช่ tenant authority Umbrella maturityทุกfeatureยังM0 actual/remaining person-hoursnull ไม่มีการแปลงเวลาagent/CIเป็นเวลาคน
- CI exact Engine revision: W1 run40509385311 และ platform run40509385312 ถูกปฏิเสธทั้ง4jobsก่อนstepsจาก reportedrecentaccountpaymentsหรือspendinglimit ไม่มีbillingchange ไม่ใช่ codefailure หรือ CIpass ไม่rerunซ้ำจนexternalstateเปลี่ยน

## ขอบเขตสัญญาและ lessons

- Core factories ต้องคืน handler ใหม่ที่ dispatcher เป็นเจ้าของและ dispose ไม่ใช่ shared/pooled/DI-scope-owned instance; error/cancel/cleanup failure semantics ชัดเจน ไม่กลบ primary failure
- Composition อ่าน plain trusted appsettings JSON ไม่ใช่ effective IConfiguration stack; ไม่มี env/CLI provider merge/live reload รองรับเฉพาะ Modular/SingleProcess/RequestReply, max256modules/1MiBJSON/depth32 Support deps implicitได้แต่ entrypointsต้อง explicit; falseห้ามactivation
- Descriptors/registration metadata ต้อง pure ไม่มี resource side effects ใน static fields/captured constructors ก่อน validation Factoryต้องคืน resources ที่เป็นเจ้าของต่าง instance และ cleanup partial allocationที่ยังไม่ส่งมอบเอง Rollbackไม่ใช่ externalbusiness transaction
- Peerแก้ literal/escaped surrogate JSON exception และ cancellationระหว่างfactoryพร้อมregressions Core/Composition independent8/8ผ่าน
- ห้าม deduplicate sourcegen candidates ด้วย display name: file-local/normal symbolsอาจเหมือนกันจน silentlydropdiagnostic ตามsourceorder ใช้ semanticISymbolidentity ตรวจerrorsทุกcandidate นับattributesทั้งpartialsymbol และreservednamespace/type Peerexact5reprosหลังแก้ผ่าน5/5 ไม่มีgeneratedtrees
- NuGet.Config isolateofficialnuget.org แก้ ambientCME+CPMsource warningโดยไม่แก้machineconfig Roslyn4.14.0 compiler-onlyexactpin/new13-packagegraphมีrawhash/contenthash/license inventory ไม่ใช่ distribution/security approval

## Benchmark และหลักฐาน

Protocolประกาศก่อนวัดใน [w1-component-protocol](../validation/w1-component-protocol.md) Acceptedattempt02 ผ่าน8/8guardrailsบนsharedWSL: 5pairedCore runs,5small/largecompiler runs เก็บrawทั้งหมด Coremedianextra96.28ns/op,extraalloc0B/opแต่ทั้งสองvariantsยังalloc56B/op ไม่ใช่allocation-freeหรือframeworkranking

Attempt01 แม้8guardrailsผ่านถูกเก็บInvalidเพราะprimaryเริ่มpackagecollectorซ้อนก่อนmeasurementจบ จึงรันใหม่ทั้งprotocolหลังcollectorจบด้วยsource/workload/thresholdเดิม ไม่เลือกrerunเฉพาะรอบดี ไม่มี generator-speed/real-provider/workload benchmark

[Delivery report](../planning/w1-core-composition-codegen.md) · [delivery manifest](../evidence/w1/delivery-manifest.json) · [final validation](../evidence/w1/final-validation.json)

## วิธีต่อ

1. Refresh live heads/Project4/CI และ latest handoff ไม่ใช้ historicalmemoryเป็นpassปัจจุบัน รักษา#3BlockedจนมีsupportedWindowsproof
2. ใช้ canonical reviewedtwo-way sync: pull → editexistingmirror → plan → review/dryrun → applyexacthash → readback Engine-onlySHAjournals ไม่เพิ่มDocs/SamplesSHAs ไม่สร้างduplicatecards
3. ก่อนปิด#5/#6 ต้องเคลียร์dependency/platform/fullacceptance gates ไม่ใช้recorderprofilesแทนrealhosts ก่อนขยาย#20ให้ทำCLI/schema/realconsumerและbenchmarkprotocolของตนเอง
4. ไม่มี NuGet/publicrelease/billing/secret provisioning ในรอบนี้ source/artifact failuresและagentworktreesเก็บไว้ให้ตรวจย้อนกลับ อย่าลบraw/normalizer LF/CRLF ของevidence/taskmirrors
