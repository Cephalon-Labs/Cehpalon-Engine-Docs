# Final02functional evidence audit

ObservedUTC: 2026-10-28T13:54:29.677479+00:00. Read-only; no builds,reruns,measurement,commits orremote writes.

Status: passed_with_explicit_boundaries. Findings: 0.

| Host | Corpus executions | Included cancellations | Maximum serverack afterabort | Repeat cycles | Maximum shutdown | API-onlyexercise |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| windows | 4000 | 400 | 1.2032ms | 120 | 6.5286ms |20000|
| linux | 4000 | 400 | 1.3307ms | 120 | 1.6362ms |20000|

Rawtick reconstruction maxima: Windows1.2032ms; Linux1.330781ms. Recorded .NET TimeSpan millisecond fields in thetable arequantized to100ns; bothraw andrecordedintervals satisfy100ms.

Bothhosts have identical initialdataset and orderedcorpus hashes. All1000indexes perlane are accounted for, allrecorded outcomes match thefrozen manifest, all400cancellationrecords perhost satisfy theunchanged100ms acknowledgementlimit andserver-entry/abort ordering withjoined ownership/no mutation flags. Theindependently replayed expected model produces thedeclared finalstate hash. Enabled/disabled actualGraphQL lifecycle probes match eachprofile. All30repeat cycles perlane pass5second shutdown withbalanced ownership.

Proof boundaries:

- The400cancellationcases per host are INCLUDED in4000corpus executions; do not addthem again as4400cases.
- Actual Stopwatch frequency is now retained in each predeclared header. Raw intervals are checked against the unchanged100ms gate. Only representation comparison allows0.00011ms for100ns TimeSpan quantization.
- Responsebody equality andactualfinalstorestate were checked bytheexecutionharness. Raw case rows retain status/code andassertion outcomes, not allresponse bodies oractual final snapshots; thisaudit independently replays the frozen expected model, not absent response bytes.
- The20000API-only requests per host are supported by deterministic10000request loops andtwo completed high-level checks, not20000separately retained response records.
- The120repeat lifecycle cycles per host are same-process host restarts, separate from benchmark fresh-process startup measurements.
- Invalid/all-off/cycle evidence here is pure Composition compiler preflight. It does not itself execute a public BenchmarkHost with anall-off/invalid configuration; protectedconsumer host tests are separate.
- This is apublic synthetic10000record fixture withfixed server-owned public identity; it doesnotprove JWT/realIdP/tenant/provider/database/production isolation.
- Zero forbidden factory andGraphQL lifecycle probes coverthese explicitfixture paths; unimplemented provider traps are notproviderqualification.
- Windows26H2 remains observational andWSL doesnotclearsupported-Windows#3. No qualification orperformance promotion inferred fromthisfunctional audit.
