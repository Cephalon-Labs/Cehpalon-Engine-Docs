# W0 — Artifact identity และ Linux runner qualification

วันที่ตรวจ: 2026-10-27 (Asia/Bangkok); ขอบเขต Engine #3 และ ADR-0003/0004

สถานะ: **ตรวจ actual model/archive bytes และ registry manifest/config identities แล้ว; bounded Linux runner version/dependency smoke ผ่านตามเงื่อนไขด้านล่าง** ไม่มี modelserver, inference, model-quality benchmark, provider container หรือ SDK ถูกเริ่มโดย agent นี้ Runtime feature maturity ยัง M0 การตรวจนี้ไม่ใช่ security audit หรือการรับรอง production

## Model files ที่ตรวจจาก bytes จริง

ใช้ publisher metadata จาก revision ที่ ADR pin และตรวจขนาดก่อนดาวน์โหลด หลังเขียนไฟล์/flush/fsync แล้วเปิดไฟล์จาก disk อีกครั้งเพื่อคำนวณ SHA256 ไม่ใช้ hash ของ network stream เพียงอย่างเดียว

| Artifact ใน `D:\Cephalon\.tools\models` | Actual bytes | Actual on-disk SHA256 | ผล |
| --- | --- | --- | --- |
| `Qwen3-4B-Q4_K_M.gguf` | 2497280256 | `7485fe6f11af29433bc51cab58009521f205840f5b4ae3a32fa7f92e8534fdf5` | ตรง expected publisher size/hash |
| `Qwen3-Embedding-0.6B-Q8_0.gguf` | 639150592 | `06507c7b42688469c4e7298b0a1e16deff06caf291cf0a5b278c308249c3e439` | ตรง expected publisher size/hash |

ข้อมูล revision/license/source-metadata hash และ attempt timestamps อยู่ใน [model-artifacts.json](model-artifacts.json) และ `sources/*.publisher.json` Model weights อยู่ภายนอก Git ไม่ execute model repository scripts หรือดาวน์โหลด arbitrary code จาก model card การ match expected hash เป็น artifact identity proof ไม่ใช่ semantic quality, parser safety หรือ inference compatibility proof

## Inference binary archives และ exact release mapping

| Runner | Actual archive | Actual size/SHA256 |
| --- | --- | --- |
| Ollama 0.40.11 | `D:\Cephalon\.tools\binaries\ollama\v0.40.11\ollama-linux-amd64.tar.zst` | 1508659610 bytes; `7bedab90dd122661be78798e9f0edf37fccf0cccf2699d2c58ea1a3afdc04b6d` |
| llama.cpp release alias 0.7.0 | `D:\Cephalon\.tools\binaries\llama-cpp\v0.7.0\llama-b11669-bin-ubuntu-x64.tar.gz` | 17851611 bytes; `cf07c1c112d709bd67e522017471de57ed0ec8bea031d732c5422351c07f65ac` |

ทั้งสอง archive ตรง GitHub release asset SHA256 ที่ประกาศและ actual bytes ที่เปิดตรวจจาก disk ไม่อ้างว่า checksum จาก GitHub API เป็นการตรวจ detached signature ของ binary

Release `v0.7.0` ของ llama.cpp ไม่ได้มี CPU archive โดยตรง มี asset `nightly-tag.txt` ที่ชี้ไป `b11669` ตรวจ checksum ของ marker และตรวจ release/ref ของ nightly พบ commit เดียวกันกับ versioned release: `620d2225cc436ab0b001e3200e590e3b286ef9ab` จึงเลือก plain Ubuntu x64 archive ของ nightly นี้ ไม่เลือก CUDA/OpenVINO/Vulkan asset และไม่เปลี่ยน commit ไปใช้ latest

Actual `llama-server --version` แสดง **`0.7.0-dev (build 11669, commit 620d2225c)`**, build GNU 11.4.0/Linux x86_64 จึงต้องใช้ release-alias + build + full source commit + archive hash + actual version string ร่วมกัน ไม่เปลี่ยนคำว่า dev ให้เป็น stable runtime proof ดู [inference-binaries.json](inference-binaries.json) และ preserved nightly metadata/marker/ref

## Safe extraction และ WSL dependency smoke

ตรวจ archive member names, types และ link targets ก่อนแตกไฟล์: ปฏิเสธ absolute/parent-traversal paths, devices/FIFOs และ link ที่ออกนอก root จากนั้นใช้ target ที่ resolve แล้วอยู่ภายใน owned `.tools` directory เท่านั้น ไม่เขียนทับ runtime directory ที่ไม่มี matching completion marker

- Ollama: แตก CPU subset ที่ `D:\Cephalon\.tools\binaries\ollama\v0.40.11\runtime` โดยเว้น CUDA/Vulkan directories; เก็บ LICENSE/NOTICE และ CPU libraries ที่ archive มี
- llama.cpp: แตกที่ `D:\Cephalon\.tools\binaries\llama-cpp\v0.7.0\runtime` โดยเว้น `rpc-server` และ `libggml-rpc.so` ไม่ execute RPC/mmproj/multimodal/GPU paths
- ELF ของ executable ทั้งสองเป็น ELF64 little-endian machine62/x86_64; llama wrapper note ระบุ `x86-64-baseline`, build-id `59b4ac7ac48aceca05f0429ef18c9687b035f163`; Ollama build-id `f97d113deb5dfc6082de38b6d1252d8c5cf1508c` แต่ไม่ได้อ่านได้ว่า backend ที่ dispatch จริงใช้ ISA ใด จึงไม่รับรอง AVX2 จากชื่อไฟล์เพียงอย่างเดียว
- Environment ที่รัน smoke จริง: **WSL Ubuntu 22.04.5**, Linux kernel `6.18.54.1-microsoft-standard-WSL2`, glibc **2.35-0ubuntu3.13** ไม่ใช่ native Linux deployment certification หรือ benchmark resource profile
- Ollama `--version` ผ่านและระบุ client0.40.11 มี warning เพราะตั้ง `OLLAMA_HOST=http://127.0.0.1:65534` ไปยัง endpoint ที่ไม่มี server โดยตั้งใจ ไม่เริ่ม modelserver
- llama initial `--version` ล้มเหลว exit127: `libgomp.so.1` ไม่อยู่ใน host; `ldd` ยืนยัน dependency ขาด ผลแรกยังอยู่ใน [llama-cpp.runtime-inspection.json](llama-cpp.runtime-inspection.json)

แก้ dependency แบบ app-local โดย **ไม่ติดตั้ง package ลง WSL/global**:

1. ดาวน์โหลด fresh Ubuntu `jammy-updates/InRelease` จาก archive ทางการ ตรวจ `gpgv` ด้วย existing `/usr/share/keyrings/ubuntu-archive-keyring.gpg` สำเร็จ เก็บ signature output/keyring hash และ release date 2026-10-26T18:33:41Z แหล่งนี้ไม่มี Valid-Until ที่อ่านพบ; tool จึงกำหนด freshness window ไว้ใน source ก่อนใช้ครั้งต่อไป
2. ตรวจ `Packages.xz` actual bytes/hash กับ signed Release SHA256 จากนั้นเลือก entry `libgomp1` ของ amd64 ใน index และตรวจ actual `.deb` กับ SHA256 ของ entry
3. Package `libgomp1 12.3.0-1ubuntu1~22.04.3`, 126570 bytes, actual `.deb` SHA256 `870c27299185a5dd4accad3b15bf82a7409fd7073cccaa8025875307da4d0ce2`
4. อ่าน data archive ด้วย `dpkg-deb --fsys-tarfile` ไม่รัน maintainer scripts แล้วคัดเฉพาะ regular library bytes เป็น `runtime/lib/libgomp.so.1`: 298776 bytes, SHA256 `d46f9225c1883039e8a6853e6d96ca1af11d034ce186a090952e4a7c8a7c2fdc`
5. Scope `LD_LIBRARY_PATH=/mnt/d/Cephalon/.tools/binaries/llama-cpp/v0.7.0/runtime/lib` เฉพาะ child process แล้ว `ldd` ไม่มี missing libraries; `--version` และ `--help` exit0 ดู [llama-cpp-local-dependency.json](llama-cpp-local-dependency.json)

Package นี้เป็น source gcc-12 runtime การตรวจ loader ไม่รับรอง transitive redistribution/license compliance ทั้งชุด ต้องทำ SBOM/notices รวม GCC runtime licensing ก่อนแจก artifact การที่ app-local smoke ผ่านไม่แปลว่าติดตั้ง package dependencies ทั้งหมดของ Ubuntu แล้ว

Exact executable hashes, archive member lists และ stdout/stderr อยู่ใน [archive-inspection.json](archive-inspection.json), [runtime-binary-inspection.json](runtime-binary-inspection.json), [Ollama inspection](ollama.runtime-inspection.json) และ dependency report แยก ไม่ใช้ `runtime-binary-inspection.json` ที่เก็บ initial missing-dependency outcome มาอ้างว่ารอบ app-local ที่ตามมาล้มเหลวด้วย

## Container registry locks สำหรับ primary

[container-manifests.json](container-manifests.json) เป็น canonical incremental lock: `images[]` มี `registry`, `repository`, `tag`, **`index_digest`**, **`linux_amd64_digest`**, **`config_digest`**, `pull_reference`, `platform` และ status

ตรวจจาก response bytes จริงของ index → linux/amd64 manifest → config blob และเทียบ SHA256 ทุกขั้นกับ registry digest headers/descriptors เก็บ raw/source hash แยกใน `sources/` ไม่มีการ pull image layers หรือเปลี่ยน Docker/Podman state โดย agent นี้ ไม่มี bearer token หรือ signed download redirect URLs ถูกเก็บใน evidence

| Selected source tag | Linux/amd64 platform digest |
| --- | --- |
| `library/postgres:18.6` | `sha256:9770878138a2e83abcb10856d30cc3f24dae0d317bb956db6ab9159de6c3c80d` |
| `library/rabbitmq:4.4.0` (bare/lean) | `sha256:184d4ae2a5d7fd4cbe1ad7165d1fb6c1377735ed2744c6be478deed5e8f0ba88` |
| `quay.io/keycloak/keycloak:26.8.1` | `sha256:3e1ac632e743660017b1e6bb4c3ffc800fd02c82cdd0db858cd03456a98a8dfc` |
| `qdrant/qdrant:v1.20.0` | `sha256:2d1b0bfd0a961275481ea09400fc98008216ae54e1b52ed7d24520d63050c644` |
| `valkey/valkey:9.1.3` (optional/cache off) | `sha256:b94f4063db6015ab2fd39a764c241a107aa176c5e7801742af81f4f8f3cb532a` |

ข้อค้นพบที่ต้องรักษา:

- **`qdrant/qdrant:1.20.0` ได้404**; tag ทางการที่ตรวจสำเร็จคือ **`v1.20.0`** เก็บ failed selector ใน [failed-selector-attempts.json](failed-selector-attempts.json) ไม่ถือว่า bare-tag lookup ผ่าน
- `rabbitmq:4.4.0-management` เป็น audit alternative ที่ตรวจครั้งแรก แต่ primary เลือก bare4.4.0 ไม่ใช้ digest ของ management สลับเป็น bare เก็บ first observation/raw source แยกใน `initial-registry-observation/`
- Published config แสดง PostgreSQL `PG_VERSION=18.6-1.pgdg13+2`; RabbitMQ labels อ้าง Ubuntu26.04 และ `RABBITMQ_VERSION=4.4.0`; Keycloak config label version26.8.1 และ RHEL9 CPE; Valkey env9.1.3 ข้อมูลนี้เป็น publisher config metadata ไม่ใช่การอ่าน `/etc/os-release` หรือ Java/Erlang binaries ที่ติดตั้งจริง
- **Primary เป็นผู้ pull/inspect/start provider fixtures และบันทึก actual OS/Java/Erlang/runtime versions** การที่ index/config hash ตรงไม่ใช่ layer extraction, provider startup หรือ Engine integration proof

## License, maintenance และ advisory boundary

ตรวจ versioned Ollama MIT และ llama.cpp MIT sources; extracted Ollama archive มี third-party LICENSE/NOTICE หลายส่วน จึงไม่สรุปว่า archive ทุก byte มี license เดียวกับโครงการ Model publisher metadata ระบุ Apache-2.0 ตาม ADR การเตรียม redistribution ต้องมี inventory จาก binary/image/weight artifacts จริง

ตรวจ official PostgreSQL support policy, RabbitMQ release information, Keycloak26.8.1 release/security fixes, Valkey release list และ inference repositories' published advisory endpoints ณ วันที่นี้ เป็น **bounded inventory** ไม่ใช่ vulnerability scan หรือข้อสรุปไม่มีช่องโหว่

- Official llama.cpp advisory query pageแรกคืน13รายการ; Ollamaคืน0รายการสำหรับ endpoint/query ที่ใช้ จำนวน0ไม่รับรองว่าไม่มีช่องโหว่หรือไม่มี disclosure ที่อื่น เก็บ raw API source/hash
- Official llama.cpp [security PR29360](https://github.com/ggml-org/llama.cpp/pull/29360) เรื่อง malformed mmproj out-of-bounds ยัง `open`, `merged_at=null` ณ query นี้ ไม่อ้างว่า v0.7.0 มี fix ดังกล่าว และไม่อ้างพิสูจน์ vulnerability exploitation ใน build นี้ งานรอบนี้ใช้ text-only pinned GGUF ไม่โหลด mmproj และไม่เปิด RPC/multimodal surface; ยังต้องตรวจ advisories/dependency inventory ของ deployment ที่จะใช้จริง
- Keycloak26.8.1 release pageแสดง security fixes หลายรายการ การใช้ releaseนี้ไม่ทดแทนการตรวจ realm/client/token/proxy configuration และ current advisories ก่อน deployment

## Tool verification และหลักฐานที่ต้องทำต่อ

รัน `python tools/qualify_artifacts.py selftest`: offline safety checks **6/6** ผ่าน เรื่อง valid-cache reuse, mismatch preservation, failed checksum ไม่ promote destination และ prior source/JSON retention ดู [tool-validation.json](tool-validation.json) รวมผล assertion attemptแรก5/6ที่นับ history ของไฟล์อื่นผิดไว้ใน `retained-observations/`; แก้ test selector ไม่ใช่ลบข้อมูลที่ tool เก็บ และ rerun ด้วย isolated test root ใหม่

คำสั่งที่ทำซ้ำได้: `models`, `registries`, `binaries`, `inspect`, `dependency`, `selftest` ผ่าน script เดียว source/toolไม่มี credential arguments รุ่น/tagที่เลือกอยู่ใน source และไม่มี floating latest การรัน `inspect` แบบไม่มี app-local LD_LIBRARY_PATH จะยังบันทึก stock-host missing-dependency outcome แยกจาก `dependency` ที่ scope environmentให้ library นี้

งานคงเหลือของ primary: actual image/layer/runtime inventory, provider/HTTP smoke, .NET11 RC3 adapter/driver qualification, scoped model import/loading และ conformance การ pass `--version` ไม่รับรอง provider startup, prompt/tokenizer/tool mapping, 1024-dimensional embeddings, cancellation หรือ workload/SLO/benchmark gate

## Primary sources ที่ใช้ตรวจ

- [Pinned Qwen generation artifact](https://huggingface.co/Qwen/Qwen3-4B-GGUF/blob/bc640142c66e1fdd12af0bd68f40445458f3869b/Qwen3-4B-Q4_K_M.gguf) และ [embedding artifact](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B-GGUF/blob/370f27d7550e0def9b39c1f16d3fbaa13aa67728/Qwen3-Embedding-0.6B-Q8_0.gguf)
- [Ollama0.40.11 release](https://github.com/ollama/ollama/releases/tag/v0.40.11), [versioned license](https://github.com/ollama/ollama/blob/v0.40.11/LICENSE)
- [llama.cpp0.7.0 release](https://github.com/ggml-org/llama.cpp/releases/tag/v0.7.0), [official b11669 assets](https://github.com/ggml-org/llama.cpp/releases/tag/b11669), [versioned license](https://raw.githubusercontent.com/ggml-org/llama.cpp/v0.7.0/LICENSE)
- [Ubuntu signed jammy-updates InRelease](https://archive.ubuntu.com/ubuntu/dists/jammy-updates/InRelease), [Ubuntu amd64 package index](https://archive.ubuntu.com/ubuntu/dists/jammy-updates/main/binary-amd64/Packages.xz)
- [PostgreSQL maintenance policy](https://www.postgresql.org/support/versioning/), [RabbitMQ release/support](https://www.rabbitmq.com/release-information), [Keycloak26.8.1 fixes](https://www.keycloak.org/2026/10/keycloak-2681-released), [Valkey release list](https://valkey.io/download/releases/)
- [Ollama published advisories](https://github.com/ollama/ollama/security/advisories), [llama.cpp published advisories](https://github.com/ggml-org/llama.cpp/security/advisories), [llama.cpp PR29360](https://github.com/ggml-org/llama.cpp/pull/29360)
