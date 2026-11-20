# ADR-0039: Project-configurable domain audit history and trails

Status: Accepted for the user's explicit audit-history/trail requirement. Date2026-11-20. Tracking #18, #7/#8 checked-context regressions. Provider/host/production qualification remains open.

## Context and user decision

The user clarified audit means audit history/audit trails, and required consuming projects to choose the format and enable/disable it. Existing automatic operation events capture authorization/outcome metadata, not field-value change history. Add an explicit domain-change trail alongside those events.

## Decision

Provide project-selectable Disabled, MetadataOnly, ChangedFields and BeforeAfterSnapshots modes, exact operation/action/resource-kind rules and per-field allowlist/redaction. Whole feature activation is optional; disabled activation creates no sink/provider work. MetadataOnly and Disabled do not invoke a values factory. Other modes accept only bounded immutable scalar states (Missing distinct from Null, Text, Boolean, Decimal and Redacted), with finite field/value/record limits. No automatic arbitrary object serialization, reflection diff or request/result CDC.

The trusted application/provider explicitly reports a change receipt with stable receipt identity, principal/scheme/tenant/operation/action/entity and authorization-resource version matching an active checked context. Domain before/after versions remain separate: resource-scope version can represent ACL authority rather than entity data version. Create/update/delete describe provider-reported mutations; creation must first authorize an appropriate reserved entity scope. A receipt constructor is not proof of a database commit.

ChangedFields compares original typed values before redaction; otherwise a changed secret could disappear after both sides become the same marker. Snapshot mode includes allowed unchanged fields too. Project into a new immutable record and strip unknown fields/redact both sides before crossing the sink. Current read policy is applied again to older stored records, so tightening rules does not reveal values previously captured. Default metadata behavior never silently captures arbitrary payloads. Explicit capture rules can persist supplied domain values; this is not automatic secret detection. Projects must exclude credentials/session identifiers or mark sensitive fields for redaction. Text is bounded well-formed UTF16 and can retain control characters from source data; storage/rendering/logging must use structured escaped encoding.

Expose pluggable required append and bounded tenant history ports. Trail history requires a distinct audit-trail/tenant/read scope, pre/post checked-context validity and page/tenant validation; ordinary operation-audit metadata permission does not grant field history. Stable receipt identity supports provider idempotency contracts, without automatic retry/exactly-once claims. Link through verified operation/principal/entity/versions and the receipt; caller correlation is not a trusted automatic operation InvocationId.

Required persistence uses a bounded independent cancellation budget with post-await checks, while the provider must cooperate. Post-commit expiry/cancellation/persistence failure may leave changed data or even persisted history; surface explicit may-have-committed failure, never report rollback. Caller cancellation after a reported mutation is wrapped as that required-trail failure rather than plain business cancellation. An unhandled wrapper is an operation fault; applications may explicitly convert it to a rejection carrying possible-commit semantics, as the sample does. Atomic database/outbox/CDC, retention, encryption, tamper evidence, nonrepudiation, migrations and distributed consistency belong to the selected provider/application and need separate qualification.

## Options and consequences

Keep operation metadata only: retain it as the smallest profile, but insufficient for user-selected field history. Generic request/result diff: convenient yet cannot establish committed values or prevent accidental secrets; rejected. Explicit bounded receipts/state projection plus pluggable persistence: chosen, adds application integration and failure semantics with clear provenance. Field history is more sensitive than operation metadata; deny by default outside declared rules and separate history permission. No performance claim without measurement.

## Validation

[Protocol](../validation/configurable-audit-trails.md), [requirement](../requirements/2026-11-20-observation-audit-trails.md). All modes/lazy providers/values, typed CRUD states, omission/redaction/read tightening, identity/entity/version binding, retained contexts/cross-tenant pages and post-mutation failure. Actual generated HTTPS HTTP/GraphQL receipts after controlled fixture mutation, with ordinary tenant/RBAC/ABAC/session checks. Original gates and #3/#20 remain unchanged. Local fixtures do not qualify real durable storage or production audit acceptance.
