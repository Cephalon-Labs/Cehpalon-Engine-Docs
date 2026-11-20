# Observation lifetime and configurable audit trails

The user continued substantial engine work, then clarified that audit means audit history/audit trails. Asked about before/after values, the user explicitly required support for the alternative formats, with each consuming project choosing what to enable or disable. This is an accepted requirement, not merely operational diagnostic logging.

Root selected two compatible bounded slices: preserve the original trusted session observation lifetime through protected tenant admission/execution boundaries (#8/#7), and add explicitly reported domain-change trail/history with per-project Disabled, MetadataOnly, ChangedFields and BeforeAfterSnapshots modes (#18). Field allowlists/redaction, tenant isolation and pluggable persistence/history are required. Existing automatic operation outcome history remains available independently.

Before/after state must come from explicit trusted application/provider change handling, never be inferred as committed database state from generic requests/results. Domain entity versions and authorization-resource versions are separate. No automatic CDC, database transaction/outbox, real IdP/store/distributed revocation or production qualification is claimed by local contracts/HTTPS fixtures. Keep #3 Blocked, #20 complete row, original benchmarks/metadata/M0/unknown hours unchanged.
