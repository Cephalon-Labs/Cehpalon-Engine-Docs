# Functional evidence audit: final attempts 02

Read-only audit of Windows `.local/benchmark-conformance-win-02` and Linux `.local/benchmark-linux-integration-02/conformance`. No builds, test reruns, measurements, commits or remote writes.

**Result: no runtime evidence findings within the audited scope.**

| Host | Corpus executions | Included cancellations | Maximum recorded acknowledgement | Maximum reconstructed raw interval | Repeat lifecycle cycles | Maximum shutdown | API-only exercise |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Windows |4,000|400|16.0981 ms|16.0981 ms|120|6.3029 ms|20,000 requests|
| Linux |4,000|400|20.2075 ms|20.207572 ms|120|1.8789 ms|20,000 requests|

Both hosts use the same initial 10,000-record dataset and ordered 1,000-case manifest. All four lanes per host retain indexes 0–999 without duplicates or omissions. Recorded statuses and business codes match the frozen manifest. An independent replay of the expected model produces its declared final-state hash. All cancellation records show handler entry before abort, no early abort, acknowledgement within the unchanged 100 ms limit, completed handler ownership and no mutation after acknowledgement. All 30 repeat cycles per lane report shutdown within five seconds with balanced handler disposal. API-only GraphQL factory, service, diagnostic, executor and schema probes are zero; enabled GraphQL profiles report those lifecycle hooks.

Worst acknowledgement records: Windows baseline-http case 409; Linux baseline-http case 9. The older 1.9923 ms observation is not the final02 maximum.

Proof limits:

- The 400 cancellation cases per host are included in the 4,000 corpus executions; they are not 400 additional cases.
- Actual response-body equality and final store state were checked during execution. Raw case files retain status/code and assertion outcomes, not every response body or final snapshot. This audit independently replays the expected model; it cannot reconstruct absent response bytes.
- The 20,000 API-only requests per host are supported by deterministic source loops and two completed checks, rather than separately retained network records for all requests.
- The 120 lifecycle cycles per host are same-process host restarts. Fresh-process startup measurements belong to the separate benchmark evidence.
- Invalid, all-off and cycle checks here exercise the pure Composition compiler. They do not execute this public BenchmarkHost with an invalid or all-off configuration; protected consumer host tests are separate.
- This public synthetic fixture uses a fixed server-owned public identity. It does not establish tenant, JWT/real IdP, provider, database or production isolation. Unimplemented provider traps are not provider qualification.
- Windows26H2 remains observational and WSL does not clear supported-Windows issue #3. This functional audit establishes no performance or deployment qualification.

The machine-readable JSON includes per-lane counts, source hashes and hashes of every audited evidence JSON file. Stopwatch frequency was inferred from the declared 50 ms/raw scheduled interval; it was not separately persisted. Linux raw ticks have finer precision than the recorded 100 ns TimeSpan fields. The audit uses a 0.00011 ms representation comparison tolerance and separately checks the raw interval against the unchanged 100 ms gate. An invalid first audit inference from rounded abort milliseconds was retained as `functional-evidence-audit-final02-attempt01-invalid-clock-inference.*`; it was an audit calculation defect, not a runtime test failure.
