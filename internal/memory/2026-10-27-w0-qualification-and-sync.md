# W0 continuation — SDK/driver/artifact และ two-way tracking

คำขอผู้ใช้: ดำเนิน #3 และ #23 ต่อ ให้ agent ช่วยตรวจ SDK/driver/artifact ทำเครื่องมือซิงก์สองทาง ทดสอบ และซิงก์ GitHub/Docs ใช้ scoped downloads/private SDK/owned provider fixtures และ reversible GitHub updates ไม่มี billing/public release/NuGet publication

## Current accepted/observed state

- Repos: `D:\Cephalon\Cehpalon-Engine`, `Cehpalon-Engine-Docs`, `Cehpalon-Engine-Samples`; ทั้งสาม private/MIT, author/committer Cephalon-Neza ใช้ Project4/original23issues ไม่ใช้ historical checkout หรือ Project3
- #23 ปิด Done/Test gatePassed; #3 เปิด Blocked/Test gateBlocked; W0เปิดเพราะ #3 เหลือหนึ่งงาน ทุก Engine runtime featureยังM0 Actual person-hoursไม่มีข้อมูลจึงnull
- Engine `5a6795b34535fdc311b519e8d452ea1c9f715bba` ตรวจ exact committed source ในเครื่องแล้ว14/14ทั้งสองOS ไม่มีprovider checks skipped ในownedmode; [commit journal](../evidence/w0/qualification/engine-commit-journal.md) เก็บเฉพาะEngineSHA
- SDK `11.0.100-rc.3.26522.148`, runtime `11.0.0-rc.3.26522.148`, private `.tools/dotnet11/{win,linux}-x64`; actualarchiveSHA512ตรงofficialmetadata ไม่แทนsystemSDK Exact63-packagegraph/lock/rawsignedarchivehashes retained
- Windows11Pro26H2/build26300.9711 ผ่านแบบobservationalแต่ไม่อยู่ในcheckedsupporttable; WSLUbuntu22.04.5/glibc2.35 อยู่ในตารางแต่ไม่ใช่bare-metal/deploymentproof
- ทั้งสอง hostedCI matrices ถูกGitHubปฏิเสธก่อนstepแรกโดยแจ้งrecentaccountpaymentsหรือspendinglimit: [Engine run](https://github.com/Cephalon-Labs/Cehpalon-Engine/actions/runs/40499602044), [Docs run](https://github.com/Cephalon-Labs/Cehpalon-Engine-Docs/actions/runs/40499738170) ไม่มีbillingchange ไม่มีCIpass ไม่ใช่code-testfailure ไม่rerunซ้ำจนexternalblockerเปลี่ยน
- Providerfixturesครบ5immutableimagesตรวจOS/version/probeจริง; ownedcontainers/network/anonymousvolumesและtemporarycredentialsล้างแล้ว ทุกownedloopbackportปิด DockerDesktopอาจยังทำงาน อย่าปิดsharedengineโดยอนุมาน
- หลัง cleanup สำเร็จ การเรียก Docker API ตรวจรายชื่อ container/network ซ้ำคืน Internal Server Error; final validation บันทึกสองรายการนี้ Unavailable พร้อมยืนยัน ports ปิดและ current private state ไม่มี password/token ไม่ restart shared Docker service ก่อนใช้งาน fixtures รอบใหม่ต้องตรวจ daemon อีกครั้ง
- GGUFสองไฟล์และOllama/llamaarchivesตรวจactualbytes/hashแล้ว filesอยู่`.tools`นอกGit llama0.7.0releasealiasชี้build11669/commit620d2225cc436ab0b001e3200e590e3b286ef9ab actualversionเป็น`0.7.0-dev`; missinglibgompแก้app-localด้วยsignedUbuntuindex ไม่installglobal ไม่มีmodelserver/inference/qualityrun
- GraphQL transitive `ChilliCream.Nitro.App32.0.2` ใช้ ChilliCream License1.0 ไม่ใช่MIT-onlygraph ยังไม่distribution-cleared ส่งต่อ#22

## Tracking workflow ที่ใช้ต่อ

อ่าน [usage](../standards/tracking-sync-usage.md) ก่อนเขียน GitHub: pull → localmetadata/bodyedit → planใต้ignored`.local` → review → dryrun → applyด้วยexactplanhash → readback แล้วบันทึกsnapshotล่าสุด อย่าใช้bootstrapseedหรือoldW0validatorแทนcurrentstate

Tool offline59/59ทั้งWindows/WSLและindependentrepairrepro4/4ผ่าน มีrealGitLF/CRLFbytepreservationtest Liveexisting#23ทดสอบทั้งสองทิศ, staleProject-onlyrejectionแม้issueupdated_atไม่เปลี่ยน, originalbody/Priorityrestoredและcompletedreplay0ops ไม่สร้างduplicateหรือเปลี่ยนactualhoursตามเวลาที่agentทำงาน

รองรับnativeType/title/body/labels/assignees/state/milestoneassignmentและProjectfieldsที่มีอยู่ Identitymappingต้องexplicit ไม่มีcreate/delete/schema provisioning มีcheckpoint/readback/resumabilityแต่ไม่มีcross-serviceatomicCAS เจอthirdstateต้องหยุดreconcile ห้ามforceoverwrite

Agentทำงานในisolated`.worktrees`และส่งpatchให้primaryเป็นsole remote writer แก้checkpointfalsecompletion/localanchor/stalemilestoneและRabbitackoracleจากindependentreviewแล้ว Rawfailedattemptsเก็บไว้ ไม่ลบหรือปรับthresholdให้ผ่าน

## Next work / proof boundaries

1. ปลดaccountCIblockerหรือจัดlisted-supportedWindowshostที่ได้รับอนุญาต แล้วรันpinnedexact-sourcechecksก่อนปิด#3 ไม่แก้billingอัตโนมัติ
2. ดำเนินimplementation/provider/sampletasksตามADR/protocol Componenttestsไม่รับรองEnginecomposition/tenantbusiness/E2E/HA/modelquality/benchmark/production
3. ตรวจliverevisions/Project/milestones/CIและ[finalvalidation](../evidence/w0/qualification/final-validation.json)ก่อนต่อ ไม่ใช้memoryเป็นหลักฐานpassปัจจุบัน

[รายงานรวม](../planning/w0-qualification-and-sync.md) · [candidate locks](../validation/provider-candidates.json) · [checklist](../validation/qualification-checklist.md)
