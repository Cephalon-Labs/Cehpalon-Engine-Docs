# .NET12 research track — W0

วันที่ตรวจ: 2026-10-27. Related issue #3. สถานะ: research only; ไม่มี .NET12 API เป็น supported Engine contract

Official ASP.NET Core milestones ที่ตรวจมี `.NET 12 Planning` และ `12.0-preview1` การมี milestone/issue ไม่รับรองว่า API หรือ release behavior เสร็จแล้ว ใช้เป็นแหล่งติดตามแยกจาก SDK11 RC3 ที่ pin และทดลองจริงในรอบนี้

| หัวข้อติดตาม | การตัดสินใจของ Engine ตอนนี้ | Gate ก่อนนำไปใช้ |
| --- | --- | --- |
| Runtime/SDK/OS/ISA/AOT/trimming | Core contracts ไม่ผูก experimental runtime APIs | Official release/support/breaking-change review และ provider/host conformance บน artifact ที่ล็อก |
| ASP.NET hosting/transports/streaming | Protocol capabilities และ host adapters แยกจาก business handlers | API/error/cancellation/streaming parity และ disabled-module activation tests |
| Configuration/source generation/tooling | Versioned schema และ immutable startup plan เป็นสัญญาของเรา | Schema migration, generated code builds, diagnostics และ compatibility ของ source/runtime |
| Data/driver/identity/telemetry dependencies | ไม่อนุมานว่า provider major รองรับ TFM ใหม่จาก platform release | Exact package graph/selected assets/license/advisory review และ real-provider smoke/E2E ตามขอบเขต |

ทบทวน watchlist เมื่อเริ่ม implementation ที่เกี่ยวข้องหรือมี official release/change ที่กระทบ ADR ไม่ตั้ง recurring automation และไม่เปลี่ยน SDK ตาม floating latest อัตโนมัติ การอัปเกรดต้องมี ADR change note, migration/deprecation scope และเก็บหลักฐานเดิม

แหล่งทางการที่ตรวจ: [ASP.NET Core milestones](https://github.com/dotnet/aspnetcore/milestones?state=open), [.NET release policies](https://github.com/dotnet/core/blob/main/release-policies.md), [.NET11 supported OS](https://github.com/dotnet/core/blob/main/release-notes/11.0/supported-os.md)
