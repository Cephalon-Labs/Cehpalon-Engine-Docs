# Sequential02 precanonical audit

**The complete sequential02 conformance matrix passes within its declared scope. The Windows01 negative outcome remains retained separately.**

| Host | Corpus executions | Included cancellations | Maximum recorded ACK | Maximum raw ACK | Repeat host cycles | Maximum shutdown | API-only exercise |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| windows |4,000|400|1.2032 ms|1.2032 ms|120|6.5286 ms|20,000 requests|
| linux |4,000|400|1.3307 ms|1.330781 ms|120|1.6362 ms|20,000 requests|

Both hosts used source `a3bd8b5c5747440c81124774ac10b6451d88ff82`. All **15 input hashes per host** match the frozen Git blobs. Actual DLL hashes match the manifests; the emitted registry contains exactly the three catalog operations, and actual runtime dependency graphs contain no Roslyn/CodeGeneration library. Recorded execution times confirm Windows02 completed before Linux02 began.

Every lane contains indexes0–999 exactly once and the same frozen dataset/corpus. Independent expected-model replay matches the declared final hash. All cancellation records meet handler-before-abort, no early abort, raw and recorded acknowledgement under100ms, joined ownership and no-mutation assertions. Actual clock frequencies come from headers, not inference. Lifecycle rows balance factory/disposal and meet5seconds. API-only probes are zero; enabled GraphQL has positive lifecycle controls.

Fresh native app-final-02: all **67 files /23,281,577 bytes** were independently hashed against the clean Linux02 artifact tree and staging manifest. Its assembly hash is `742451b86f81c439938d93aad19a0f568133fe9ff2910bae4458f6633cdcfdd4`. All **4,178 native SDK files /549,400,671 bytes** and **1,668 symlink targets** were independently checked against bound staging manifests, with only the predeclared separator/normpath representation translation. No SDK was executed by the audit.

Retained prior outcome: Windows01 baseline-http409 entered the delayed handler0.3382ms after client abort. It failed the in-flight criterion despite ACK0.5528ms and successful cleanup. Linux01 passed. Both full01 results remain; neither was replaced by a favorable individual case. Root predeclared the entire sequential02 repeat with unchanged criteria. Parallel interference remains a possibility, not an established cause.

Limits:

- The400 cancellations per host are included in4,000 executions. Positive response bodies/final live store hashes were checked by the running harness; raw case rows retain assertion/code/status rather than every response body.
- The20,000 API exercise count per host derives from deterministic loops and completed checks, rather than20,000 separately retained response rows.
- The120 lifecycle cycles are same-process host restarts; fresh-process startup measurement is separate. Invalid/all-off/cycle evidence here is pure compiler preflight.
- Public fixture and staging identity do not establish tenant/IdP/provider, production, reserved resources, native deployment or listed-supported Windows proof. Actual runtime module mapping remains for the later process observation. #3 stays Blocked.
- No audit build, test, request, timing, source change, commit or remote write was performed.

Machine-readable report and reproducible scripts are alongside this file. Audit activity stops before the frozen12-probe timing matrix.
