# ADR-0004 — Local AI, Agent และ Retrieval profile สำหรับ Samples

- วันที่ตัดสินใจ/ตรวจแหล่งข้อมูล: 2026-10-27 (Asia/Bangkok)
- สถานะ: **Accepted for W0 planning; implementation qualification pending**
- ขอบเขต: Engine #2, #3, #16, #17, #21; runtime maturity **M0**
- ผู้ตัดสินใจรอบนี้: ทีม agent ตามคำสั่งผู้ใช้ให้ศึกษาและเลือก provider โดย primary เป็นผู้รวมผลและเขียน remote

Qualification update: [actual artifact byte/runner/dependency checks](../planning/w0-qualification-and-sync.md) are now available. Image selector for Qdrant is `v1.20.0`; llama's selected release resolves to a same-commit nightly with actual version string `0.7.0-dev/build11669`. No modelserver, inference/embedding quality, tool-loop or model cancellation conformance ran. Initial expected-checksum observations below remain historical metadata evidence.

## บริบทและผลที่ต้องการ

ต้องมี sample ที่นำ business operation เดิมผ่าน retrieval → model → bounded tool loop → schema-validated answer ได้ โดยสลับ provider ผ่าน contract ที่ประกาศรองรับ การทดสอบต้องแยกความถูกต้องของ orchestration ออกจากคุณภาพของ model จริง และทำซ้ำได้โดยไม่จำเป็นต้อง provision cloud หรือซื้อบริการ

## คำตัดสิน

เลือก **Ollama + official Qwen GGUF artifacts + Qdrant** เป็น local reference profile โดย .NET host ติดต่อผ่าน HTTP adapter ที่แยกจาก Core ใช้ model/embedding/vector contracts คนละสัญญา ไม่ผูก business handlers กับ SDK ของผู้ให้บริการ และไม่ใช้ mutable model tag เป็น production/evidence pin

| บทบาท | สิ่งที่เลือกสำหรับ qualification | เหตุผลและขอบเขต |
| --- | --- | --- |
| Deterministic model/embedding fixture | Scripted adapter ของ Samples + exact in-memory cosine oracle | ใช้พิสูจน์ schema, tenant/policy, tool state machine, cancellation และ zero activation โดยไม่ใช้ model จริง; ไม่ใช่หลักฐาน inference/semantic quality |
| Local generation provider | **Ollama 0.40.11**, official release 2026-10-24, native chat HTTP adapter | เลือก self-hosted API ที่แยก tool/schema controls ได้; ต้องทดสอบ local-only settings, timeout/cancellation และ request/response mapping ของรุ่นนี้จริงก่อนรับรอง |
| Generation weights | **Qwen/Qwen3-4B-GGUF**, file **Qwen3-4B-Q4_K_M.gguf** | ขนาด artifact ประมาณ 2.50 GB ตาม publisher metadata; Apache-2.0; ใช้ non-thinking profile และ context สั้นตาม workload ไม่อนุมานจากขนาดไฟล์ว่า RAM เพียงพอ |
| Embedding weights | **Qwen/Qwen3-Embedding-0.6B-GGUF**, file **Qwen3-Embedding-0.6B-Q8_0.gguf** | Apache-2.0 และ model card ระบุ multilingual support; เลือก output **1024 dimensions**, cosine, fixed query instruction และไม่มี reranker ใน baseline |
| Vector store | **Qdrant 1.20.0**, official release 2026-10-22, HTTP adapter | รองรับ payload filtering และ vector search; ใช้ shared collection พร้อม indexed tenant field ซึ่ง Engine ต้องเติมจาก trusted identity ทุก query/write/delete ไม่ถือว่า payload filter เป็น authentication |
| Identity สำหรับ real-provider tiers | **Keycloak 26.8.1** ตาม [ADR-0003](ADR-0003-multitenant-business-profile.md) | ใช้ JWT/OIDC validation และ server-side tenant-membership policy ก่อนเรียก retrieval/model/tools; exact issuer/audience/key/scopes อยู่ใน frozen manifest ไม่ใช้ caller tenant field เป็น authority |
| Provider portability รอบแรก | **llama.cpp 0.7.0** server, release 2026-10-15, โหลด GGUF ไฟล์เดิม | สลับ inference adapter และคง business/tool contracts กับ artifact เดิม เพื่อแยกผลของ provider mapping ออกจากผลของการเปลี่ยน weights; tool templates/JSON/cancellation ต้อง qualify แยก |

Ollama เป็น MIT; Qdrant และ model artifacts ที่เลือกเป็น Apache-2.0 ตามแหล่งทางการ ต้องเก็บ notices/license ของแต่ละส่วนตามจริง การที่ Engine ใช้ MIT ไม่ได้เปลี่ยน license ของ dependencies หรือ weights ที่แจกพร้อม Sample [S1–S5]

## Artifact identity ที่ตรวจจาก publisher metadata

ข้อมูลต่อไปนี้ได้จาก metadata API ของ repository เจ้าของ model และหน้าไฟล์ revision ที่ระบุเมื่อ 2026-10-27 **ยังไม่ได้ดาวน์โหลด weights หรือคำนวณ hash ของไฟล์บนเครื่อง** ค่า SHA256 จึงเป็น publisher-declared expected checksum ที่ต้องตรวจ bytes อีกครั้งระหว่าง qualification [S6–S7]

| Artifact | Repository revision | File bytes | Expected file SHA256 |
| --- | --- | --- | --- |
| `Qwen3-4B-Q4_K_M.gguf` | `bc640142c66e1fdd12af0bd68f40445458f3869b` | 2497280256 | `7485fe6f11af29433bc51cab58009521f205840f5b4ae3a32fa7f92e8534fdf5` |
| `Qwen3-Embedding-0.6B-Q8_0.gguf` | `370f27d7550e0def9b39c1f16d3fbaa13aa67728` | 639150592 | `06507c7b42688469c4e7298b0a1e16deff06caf291cf0a5b278c308249c3e439` |

ก่อนทดสอบจริง ให้บันทึก runtime binary/container digest, CPU build/ISA, artifact hashes, tokenizer/chat template/Modelfile hashes และ Ollama model manifest digest จาก `/api/tags` หรือกลไกที่รุ่นนั้นรองรับ [S8] ถ้า import weights เข้า Ollama ให้เทียบ model blob กับ GGUF ที่ตรวจแล้วและบันทึก manifest ของผล import ด้วย ห้ามใช้ชื่อ `qwen3:4b`, `latest` หรือ tag image เพียงอย่างเดียวเป็น immutable evidence

Metadata API ที่ตรวจ: `https://huggingface.co/api/models/Qwen/Qwen3-4B-GGUF?blobs=true` และ `https://huggingface.co/api/models/Qwen/Qwen3-Embedding-0.6B-GGUF?blobs=true` ตัว hash ของ model ไม่ใช่ Engine commit และต้องไม่ใส่ใน task/card Engine commit journal

## ขอบเขตความสามารถและการเปิดโมดูล

- แยก `Chat`, `Embeddings`, `VectorSearch`, `ToolExecution` และ `AgentLoop`; model เสนอ tool call ได้ แต่ trusted dispatcher ตรวจ identity, tenant, capability, arguments และ budget ก่อนเรียก tool ทุกครั้ง
- Tools รอบแรกมีเพียง `LookupPolicy` และ `GetSyntheticOrder` แบบอ่านข้อมูล fixture ห้าม network egress, shell, filesystem, billing หรือธุรกรรมภายนอก ข้อมูลในเอกสารเป็น untrusted input และไม่มีสิทธิ์เปลี่ยน tool policy
- Request ไม่ส่ง tenant ID เพื่อเลือกสิทธิ์เอง; query/write/delete สร้าง tenant constraint จาก validated principal นโยบาย RAG ต้องตรวจสิทธิ์ก่อนส่ง context เข้า model และตรวจ citations ก่อนตอบ
- Tier F ใช้ scripted `FixtureIdentityHandler` ที่เลือกจาก trusted test composition เท่านั้น เพื่อป้อน immutable test principal/membership; ไม่เป็นหลักฐาน OIDC authentication และห้ามเปิดใน real-provider profile Tier R/M ใช้ Keycloak 26.8.1 กับ JWT validation ของ platform ตรวจ signature, fixed issuer/audience, lifetime, scopes และ membership; missing/mismatched identity ต้อง deny ก่อน provider call Negative authn/tenant cases ของ R/M ต้องผ่าน real adapter ไม่ใช้ fixture pass แทน
- ใช้ non-thinking template ของ Qwen และบันทึกวิธีปิดที่ provider รุ่นนั้นรองรับจริง การตั้ง `think:false` หรือ template ที่คล้ายกันต้องมี conformance test ไม่อนุมานว่าการส่ง soft instruction ปิด hidden token budget ได้ [S9]
- Embedding 1024 มิติและ query instruction เป็นส่วนหนึ่งของ index version; เปลี่ยน weights/dimension/normalization/chunking ต้องสร้าง index version ใหม่และ re-embed ไม่ผสม vector space ใน collection เดิม
- AI/Retrieval ปิดอยู่ต้องไม่มี model load, client factory, connection, index warmup หรือ background indexing ของโมดูลนั้น เลือก real profile ไม่ได้ถ้า binary/model manifest/digest หรือ capability ที่จำเป็นขาด

## ตัวเลือกที่พิจารณาและผลกระทบ

| ทางเลือก | เหตุผลที่ยังไม่เป็น reference แรก |
| --- | --- |
| ใช้ llama.cpp โดยตรงตั้งแต่เริ่ม | ได้การควบคุม artifact และ runner มาก เหมาะเป็น provider สอง; รอบแรกเลือก Ollama เพื่อแยก lifecycle/import/API mapping ให้เห็นชัด ไม่อ้างว่าตัวใดเร็วกว่าจนมีผลทดสอบ |
| PostgreSQL + pgvector | ลดจำนวนบริการเมื่อใช้ SQL เดียวกับ business lane แต่ผูก lifecycle และ failure domain เข้ากับฐานธุรกิจ; เป็น vector-provider qualification ถัดไป ต้องใช้ corpus/embedding/gold เดิมและทดสอบ tenant semantics ใหม่ |
| Managed model/embedding APIs | ช่วยทดสอบ provider ที่ต่างจริงและลดภาระเครื่อง แต่มีค่าใช้จ่าย credentials และข้อมูลส่งภายนอก; เป็น opt-in lane หลังได้รับสิทธิ์เฉพาะ ไม่ถูกสร้างหรือเรียกใน W0 และไม่ใช้แทน local deterministic gate |
| Mock-only AI | เร็วและ deterministic แต่ไม่พิสูจน์ actual provider, model quality, tokenization, prompt/tool formatting หรือ inference resource footprint จึงใช้เป็น tier แรกเท่านั้น |

การเลือก model family เก่าที่ pin ได้และมี license ชัดเจนเป็น deliberate reference ไม่ใช่ข้ออ้างว่าเป็น model ล่าสุดหรือดีที่สุด งานปรับ model ใหม่ใช้ corpus/gold/protocol เดิมและ ADR change note

## Qualification และข้อที่ยังเปิดอยู่

1. เลือก binary/container assets สำหรับ Linux x64 พร้อม publisher checksum/signature และยืนยัน bytes; release tag อย่างเดียวไม่ใช่ artifact digest
2. ตรวจ Ollama local-only mode, model import, JSON/tool chat templates, embedding instruction/dimension/normalization และ `truncate:false` จริง; document อาจใหม่กว่า release จึงต้องตรวจ versioned behavior [S10–S11]
3. ทดสอบ .NET 11 RC3 HTTP adapter build/run และ OS/CPU capability; การใช้ HTTP ลด dependency coupling แต่ไม่ใช่หลักฐาน compatibility ของ host หรือ runner
4. สร้างและ review corpus/gold ก่อน first run แล้ว freeze hashes; ยังไม่มี dataset artifact หรือผลตาม [workload protocol](../validation/ai-retrieval-workload.md)
5. พิสูจน์ cancellation จน provider ไม่ค้างงานหลัง client ยกเลิก ถ้า runner รองรับเพียงตัด response ต้องเปิดเผยและไม่รับรอง full compute cancellation
6. Record measured peak RAM, CPU, latency และ token counts บน hardware ที่ระบุ; budgets ใน workload เป็น acceptance targets ที่เลือกสำหรับ sample ไม่ใช่ vendor performance promises

## แหล่งทางการ

- S1: [Ollama 0.40.11 release](https://github.com/ollama/ollama/releases/tag/v0.40.11), [MIT license](https://github.com/ollama/ollama/blob/main/LICENSE)
- S2: [Qdrant 1.20.0 release](https://github.com/qdrant/qdrant/releases/tag/v1.20.0), [license](https://github.com/qdrant/qdrant/blob/master/LICENSE)
- S3: [Qwen3-4B GGUF publisher card](https://huggingface.co/Qwen/Qwen3-4B-GGUF)
- S4: [Qwen3-Embedding GGUF publisher card](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B-GGUF), [base model dimensions/languages](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B)
- S5: [llama.cpp 0.7.0 release](https://github.com/ggml-org/llama.cpp/releases/tag/v0.7.0), [versioned server reference](https://raw.githubusercontent.com/ggml-org/llama.cpp/v0.7.0/tools/server/README.md)
- S6: [Pinned generation file metadata](https://huggingface.co/Qwen/Qwen3-4B-GGUF/blob/bc640142c66e1fdd12af0bd68f40445458f3869b/Qwen3-4B-Q4_K_M.gguf)
- S7: [Pinned embedding file metadata](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B-GGUF/blob/370f27d7550e0def9b39c1f16d3fbaa13aa67728/Qwen3-Embedding-0.6B-Q8_0.gguf)
- S8: [Ollama model-list digest](https://docs.ollama.com/api/tags)
- S9: [Qwen thinking/non-thinking controls](https://huggingface.co/Qwen/Qwen3-4B)
- S10: [Ollama chat API](https://docs.ollama.com/api/chat), [embedding API](https://docs.ollama.com/api/embed), [FAQ/context/runtime configuration](https://docs.ollama.com/faq)
- S11: [Qdrant multitenancy/filtering](https://qdrant.tech/documentation/manage-data/multitenancy/)
