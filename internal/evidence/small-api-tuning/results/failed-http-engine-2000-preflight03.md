# Failed HTTP Engine diagnostic at 2,000 req/s: forensic audit

Read-only inspection of retained canonical03 evidence. No code changes, builds, timed retry, commits or remote writes.

**The failure is retained and is not an Engine capacity result.** The collector observed 4,000 offered requests: 3,963 correct and 37 `offered.dropped`. All 37 were dropped before send (`sentTicks=0`, status/body bytes=0), with 128 sent-but-not-completed requests reconstructed at every drop. The driver exited `-6` through its deliberate preflight guard; neither the 60-second warmup nor the 180-second measurement was entered.

| Observation | Adjacent baseline | Failed Engine |
| --- | ---: | ---: |
| Correct / offered |4,000 / 4,000|3,963 / 4,000|
| Collector drops |0|37|
| First observed completion |2.205244 ms|51.688269 ms|
| Largest gap between completions |5.089794 ms|29.299844 ms|
| Client CPU across snapshot span |2655.932 ms|2809.041 ms|
| Client GC delta Gen0/1/2 |0/0/0|1/0/0|
| ThreadPool workers before→after |3→4|4→4|
| Pending pool work at boundaries |0→0|0→0|
| Successful read-only preparation requests |130|130|
| Connections in pre-phase TLS snapshot |128|4|
| Planned mutation state |PASS|PASS|

Drop clusters are indexes 129–161 (33 requests; scheduled 64.5–80.5 ms) and 178–181 (four requests; 89–90.5 ms). The first Engine completion appears at 51.688269 ms, followed by a 29.299844 ms completion gap. The offered scheduler continues producing the declared 0.5 ms schedule; the backlog is observed in request completion, which includes client read/validation as well as network/server time. All dropped operations are reads (35 get, two list), so the planned mutation state can pass while the offered-work gate fails.

Both variants have byte-identical complete offered manifests and identical first 4,000 logical inputs. Independent replay of the 200 planned writes matches the failed Engine run's retained 10,000-record final snapshot and state hash, with 4,093 factories/disposals balanced. Raw persistence starts after request completion; gzip did not overlap this preflight. Preparation proves successful read-only requests, rather than a fixed number of simultaneous physical connections. Four Engine connections versus 128 baseline connections is observed. New TLS events during the failed phase were not retained: the current source writes that later snapshot into warmup/load results, which are absent on preflight failure.

Possible causes include a client/collector scheduling or GC/JIT transient, server-side delay, new TLS connections, or shared-host contention. The single Gen0 delta and boundary-only pool counts do not establish when a pause occurred. There are no server phase event traces or in-phase failed-run TLS events to identify a root cause. This single two-second failed preflight cannot establish an Engine 2,000 req/s limit or replace the unchanged 1,000 req/s acceptance series. No retry, filtering, threshold or rate adjustment was used in this audit. The shared reference environment and issue #3 remain Blocked regardless of other numeric passes.

Machine-readable evidence includes all 37 exact indexes, raw timing clusters, input hashes, pool/GC/CPU counters, comparison metrics and explicit hypotheses.
