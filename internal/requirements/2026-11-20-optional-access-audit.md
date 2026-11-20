# User refinement: optional authentication, authorization and audit/history

Date: 2026-11-20. Source: user message in the active program conversation.

> ต่อเลย ยาวๆไป ให้ engine รองรับ authorize/authentication ด้วยนะทั้ง ABAC, RBAC และรองรับ audit/history logs ด้วย ถ้าคนนำ framework เราไปใช้และต้องการใช้ feature นี้

Accepted scope: consumers can opt in to established host authentication, role policy, attribute policy or their conjunction, and structured operation audit/history. Retain host-agnostic Core and existing tenant authority checks across supported entrypoints. Selecting a public profile does not automatically activate security or audit. Disabling required security while selecting a protected endpoint must reject composition, never make the endpoint public.

Map to existing REQ-05 / Engine #7/#8 for tenant/authentication/authorization and REQ-10 / #18 for audit/history. No duplicate issue or change to #3, #20, dependencies, original acceptance/benchmark gates or unknown actual person-hours. This portable/local implementation slice does not close blocked provider/SDK acceptance.

Implementation decision: [ADR0033](../adr/ADR-0033-optional-access-and-audit.md). Validation: [predeclared protocol](../validation/optional-access-audit.md). Authentication uses ASP.NET Core's established JWT handler and an explicit-scheme bridge; other protocols remain pluggable through IIdentitySource. No home-grown password/token issuer is added. Operation history records verified identifiers/outcomes, not arbitrary payload snapshots. Durable storage, field-level version history, transactions/outbox, key/session lifecycle, retention and production deployment require application/provider-specific work and scoped evidence.
