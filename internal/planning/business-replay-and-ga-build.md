# Business replay verification and Small API GA build plan

Declared 2026-11-24 for the requested bounded recovery path and
benchmark build preparation.

## Business recovery

Use a paired synthetic tenant fixture and the same order ID and SKU for
the tenant A operation and the tenant B control where supported by the
scope. Use separate application lifetimes for transactional order
submission, outbox publishing and consumption. Pin the PostgreSQL and
RabbitMQ providers from the prior durable recovery proof.

1. Commit order and outbox in one transaction. Verify the pending order
   and canonical event in PostgreSQL before publisher work.
2. Hold the first publisher after RabbitMQ confirms a mandatory
   persistent message and before the outbox row is marked sent.
   Check the outstanding outbox and broker state before replaying the
   publisher. Verify that the replay publishes the same event.
3. Run an actual Worker with manual broker acknowledgement. Commit the
   inbox marker and order and stock effects in the same PostgreSQL
   transaction. Stop the first Worker after the commit while its delivery
   remains unacknowledged. Read the committed state independently.
4. Restart and use fresh clients for replay. Reconcile the original
   redelivery and the separately published copy when the broker exposes
   those distinct states. Require exactly one committed inbox/outcome,
   one order transition and one stock decrement. Check the unrelated
   tenant's seeded state and broker completion. Verify owned cleanup.

Record the actual restart method and the narrow fixture identity and
provider lease. The original Business workload has separate scale,
identity, poison-message, ordering, HA, latency and resource gates.
[Business contract](../validation/business-workload.md) · [Prior provider recovery](../validation/durable-recovery.md)

## Small API preparation

Use .NET SDK 11.0.100 and the current exact GA Engine pin. Require locked
Release restore/build and an actual generated registry. Keep the
synthetic corpus, schedule, request mix, baseline definition, thresholds,
pairing, cancellation and analysis criteria at their declared values.
Compare the active workload and protocol inputs against the frozen
baseline. Preserve all archived RC3 evidence. Revalidate any affected
correctness matrix or record its exact pending scope. The build work
does not activate reference timing or alter its environment gate.
[Original thresholds](../validation/small-api-workload.md) · [Prior readiness check](../validation/original-benchmark-readiness-2026-11-24.md) · [Frozen baseline](../evidence/business-replay-ga/2026-11-24/frozen-benchmark-baseline.json)
