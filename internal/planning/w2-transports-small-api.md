# Protected HTTP/GraphQL and Small API continuation

User authorized the #9/#11 work that does not wait on #3, with agents, cross-tenant/disabled-module tests and GitHub/Docs synchronization. Delivered Engine `6804271d429106864e01e4ec546a41dff771f84b`. Full issues remain open/M0; #3 stays OPEN/Blocked pending listed-supported Windows proof. No actual person-hours inferred.

## Delivered behavior

Separate experimental HTTP and opt-in HotChocolate16.7.1 GraphQL adapters share explicit typed operation bindings, pure request validation and a host dispatcher port. HTTP references no GraphQL project/package. Both enforce bounded JSON, protected entrypoints, generic access denial, redacted unexpected faults and request cancellation. GraphQL additionally disables GET/schema download/introspection/IDE/WS/batching/multipart/incremental execution, with depth8/cost1000. DTO fields are explicit reviewed schema contracts; arbitrary host schemas/middleware are outside the proof.

The external Samples consumer pins the exact Engine commit and uses generated Core gateways, fresh tenant dispatch and one catalog handler source for GetItem/ListItems/SetLabel. Actual localhost HTTPS validates a custom fixture CA and hostname; invalid trust/hostname reject. Pinned JwtBearer11 RC3 validates RS256 signature, issuer, audience, lifetime, token type and unambiguous/valid subject representation before the fixture identity source. No caller metadata grants authority. Two10,000-record tenant catalogs use compound keys and scope-checked reads/updates. This synthetic authority is not real IdP/provider certification.

Composition validates before host construction. All-off creates no WebApplication/listener; unsupported worker fails before factories. API-only omits GraphQL registration/mapping; GraphQL-only leaves API off. Through10,000 API-only requests and shutdown, GraphQL registration branch, HotChocolate DI descriptors and forbidden module factories remain zero. These are actual source/registration/service/factory observations, not independent vendor schema/executor constructor probes. Combined sample package presence does not imply activation. Throwing traps for unimplemented modules do not qualify those providers.

## Exact validation

| Suite | Windows26H2 observational | WSLUbuntu22.04.5 |
| --- | --- | --- |
| Core |32/32|32/32|
| Composition |80/80|80/80|
| CodeGeneration |42/42|42/42|
| Identity |34/34|34/34|
| Tenancy |70/70|70/70|
| HTTP |44/44|44/44|
| GraphQL |45/45|45/45|
| Engine total |347/347|347/347|
| Protected Small API consumer |40/40|40/40|

Both exact clean committed-source Engine runs used locked restore and Release warnings-as-errors; actual compiler consumer passed. Small API verifies source/package hashes and emitted generated registrations, with no Roslyn/CodeGeneration runtime libraries. Its40 checks include signed invalid/ambiguous/malformed claims, cross-tenant both directions with zero business work, same-ID isolation, metadata spoofing, revocation/wrong owner/default policy, validation/not-found/pagination/update/conflict, abort/no delayed write, malformed/oversized inputs, exposure and owned listener/handler cleanup. Intentional error codes match while REST/GraphQL wire semantics differ.

- [Exact Windows manifest](../evidence/transports/exact-win/manifest.json)
- [Exact Linux manifest](../evidence/transports/exact-linux/manifest.json)
- [Consumer Windows manifest](../evidence/transports/consumer-win/manifest.json) and [40 checks](../evidence/transports/consumer-win/consumer.json)
- [Consumer Linux manifest](../evidence/transports/consumer-linux/manifest.json) and [40 checks](../evidence/transports/consumer-linux/consumer.json)
- [Peer review and corrected findings](../evidence/transports/transport-peer-review.md)
- [Retained evidence hashes](../evidence/transports/retained-files.json)
- [Final source, identity, tracking and evidence consistency](../evidence/transports/final-validation.json)

The first integrated runner attempt failed because the HTTP executable accepted a different output argument form, after its tests passed; compatibility was corrected and the failed attempt retained. GraphQL escaped-surrogate property-name regressions failed before the narrow structural raw-string audit; failed attempts are retained. Peer findings also corrected unexpected GraphQLException disclosure, linked/post-dispatch cancellation and malformed subject handling. Additional dictionary/JsonElement HTTP surrogate checks confirmed rejection without a runtime change. No failed attempt was deleted or reported as a pass.

## Remaining gates and proof limits

This protected fixture has20,000 records, authentication and tenant policy; it is **not execution or replacement of the original public W0 workload**. The predeclared full1,000-case ordered corpus,100 timed cancellations/profile,30 restart cycles, startup/idle RSS and five isolated performance pairs remain Not run. Startup timings in consumer JSON are diagnostic, collected without the W0 isolation/baseline protocol; they do not pass or fail its budgets. No throughput, production capacity, cloud deployment, durable transaction, real IdP session/key lifecycle, database/RLS, job/cache/retrieval isolation, public package distribution or production readiness claim.

Windows26H2 remains outside the checked support table; WSL evidence does not clear #3 or prove native deployment. Hosted runs40622737320 (components/adapters) and40622737252 (platform) at this Engine commit each have two jobs with zero steps: exact annotations report account payment/spending rejection. See [raw CI observation](../evidence/transports/ci-observed.json). This is Blocked, not CI pass/code failure. No billing change or unchanged-job rerun. #9/#11 retain their original acceptance history, dependencies, native identities and estimates; full tests remain Blocked and full benchmark Planned.

Decisions: [ADR0008](../adr/ADR-0008-protected-http-graphql-adapters.md), [functional protocol](../validation/transport-small-api-functional-protocol.md), unchanged [W0 protocol](../validation/small-api-workload.md), [public guide](../../public/protected-http-graphql.md). Continue full workload/performance and supported-host qualification when their prerequisites are available; do not infer those from this functional delivery.
