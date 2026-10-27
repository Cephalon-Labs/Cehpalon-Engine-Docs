# Tracking and W0 verification tools

Run from this Docs checkout with Python 3 and authenticated `gh` access. These tools are project maintenance helpers, not Engine runtime APIs or sample implementations.

- `python tools/sync_tracking.py pull`: read existing Engine issues, milestones and Project 4 into editable task mirrors and an observed-state snapshot. `pull_tracking.py` remains the pull-only entry point. Unknown local edits or identity changes stop an unreviewed pull.
- `python tools/sync_tracking.py plan --output .local/reviewed-plan.json`: perform field-level three-way merge and create an exact bounded change plan. Review before execution.
- `python tools/sync_tracking.py apply --plan .local/reviewed-plan.json`: dry run. Remote changes require explicit `--execute --approve <exact-plan-hash>`; see [full usage](../internal/standards/tracking-sync-usage.md).
- `python tools/pull_tracking.py --check`: read live state and fail on drift without updating mirrors/snapshot. A temporary cooperating-run lock is used.
- `python -m unittest discover -s tools -p test_pull_tracking.py -v`: offline conflict/recovery tests; no GitHub calls.
- `validate_w0.py` and its report preserve the earlier W0 selection snapshot. They intentionally refer to earlier tool hashes/pending task states and are not the qualification-phase validator.

Pull stages and fsyncs files, retains before/new copies under ignored `.local/tracking-transactions/`, uses atomic replacement per file and commits the tracking snapshot last. A partial/failed batch retains a recovery journal and blocks the next pull. Cooperating runs use an exclusive lock. Arbitrary editors are not fully serialized, and the batch is recoverable rather than filesystem-atomic.

If a lock/recovery marker remains, inspect its recorded owner and retained before/new/current hashes; preserve local edits and reconcile the affected files/snapshot deliberately. Record the recovery decision before clearing reviewed markers. Do not automatically remove a live owner's lock or overwrite changed files merely to make the next pull pass. Retained recovery history requires intentional cleanup after review.

Reviewed two-way updates now cover native issue metadata, body/state/milestone assignment and supported Project fields, including guarded identity mapping and resumable checkpoints. They create/delete no issues or items. The existing #23 live qualification exercises both directions, stale Project-only rejection and restoration. It does not imply atomic server transactions or automatic synchronization without an explicitly reviewed plan.

Milestone counters use GraphQL issue connections checked against fetched native issue states. REST-reported counters are retained separately with a consistency flag; a disagreement between GraphQL and fetched issues stops synchronization. This handles the observed W0 REST counter mismatch without changing issue state or hiding the reported source value.

`bootstrap-github.py`, `validate-bootstrap.py` and the bootstrap snapshot/report are frozen initial-baseline artifacts. Do not use them as current-state synchronization or validation after W0 changes; they intentionally describe earlier assumptions and IDs.
