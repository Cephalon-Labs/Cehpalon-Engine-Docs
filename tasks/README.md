# Engine task mirrors

Each Engine issue has a Markdown file named exactly `<issue-number>.md`. The GitHub issue number is the stable tracking key; Project item IDs and node IDs are connection metadata and must be refreshed after migrations.

Task details include Type, Labels, Priority, Milestone, Status, Owner, dependencies/subtasks, feature references, estimates/actuals, acceptance criteria, test and benchmark gates, scoped maturity, Engine commit journal, and change history.

GitHub owns live issue/milestone/Project state. Markdown preserves reviewable details and evidence. Synchronization must detect conflicting edits before overwriting either side. A last-synced snapshot is not a claim of perpetual synchronization.

See the [three-system tracking runbook](../internal/standards/hermes-tracking.md) for the separate Hermes Engine reference board, document links, and approved update paths.
