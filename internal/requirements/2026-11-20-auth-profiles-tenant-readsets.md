# User refinement: configurable authentication and tenant selection/read sets

Date: 2026-11-20. User requested continued implementation, consumer-selected authentication (algorithm/JWT/JWK/JWS and other mechanisms), and behavior when one login switches tenant A to B or needs all tenant data. The user also explicitly authorized spawning agents throughout the task.

Accepted interpretation: configuration selects validated established authentication profiles and trusted key/metadata providers; extension interfaces retain other schemes. Token format, signature format, key representation/source and cryptographic algorithm remain separate controls. Credentials and raw key secrets stay outside public configuration and logs.

Tenant selection is per request, validated afresh against destination membership and policy. It never mutates global tenant state or treats login alone as destination permission. Aggregating tenant data requires a separate explicit read-set grant from a trusted source, normal per-tenant authorization and bounded read-only fanout. All means all tenants in that authorized grant, not every row/tenant in storage. Partial response data is withheld on denial/failure; prior authorized reads may have executed. Large catalogs and consistent distributed snapshots are provider-specific work.

Existing mapping: REQ-05 / #7/#8; audit lineage under REQ-10 / #18. Retain #3 Blocked, #20 full row, M0, original workload/benchmark criteria, dependencies and unknown actual person-hours. [ADR0034](../adr/ADR-0034-authentication-profiles-tenant-readsets.md), [validation](../validation/auth-profiles-tenant-readsets.md).
