# Tracking and W0 verification tools

Run from this Docs checkout with Python 3 and authenticated `gh` access. These tools are project maintenance helpers, not Engine runtime APIs or sample implementations.

- `python tools/pull_tracking.py`: read existing Engine issues, milestones and Project 4; refresh task mirrors and an observed-state snapshot. It never creates or mutates remote issues. Unknown local edits or identity changes stop the pull for reconciliation.
- `python tools/pull_tracking.py --check`: read live state and fail on drift without updating mirrors/snapshot. A temporary cooperating-run lock is used.
- `python -m unittest discover -s tools -p test_pull_tracking.py -v`: offline conflict/recovery tests; no GitHub calls.
- `python tools/validate_w0.py`: check ADR/protocol links, preserved metadata provenance, Git identity and live tracking consistency. It writes `internal/evidence/w0/validation.json` only. `--final` additionally checks the expected W0 document-task completion and pending qualification/sync tasks.

Pull stages and fsyncs files, retains before/new copies under ignored `.local/tracking-transactions/`, uses atomic replacement per file and commits the tracking snapshot last. A partial/failed batch retains a recovery journal and blocks the next pull. Cooperating runs use an exclusive lock. Arbitrary editors are not fully serialized, and the batch is recoverable rather than filesystem-atomic.

If a lock/recovery marker remains, inspect its recorded owner and retained before/new/current hashes; preserve local edits and reconcile the affected files/snapshot deliberately. Record the recovery decision before clearing reviewed markers. Do not automatically remove a live owner's lock or overwrite changed files merely to make the next pull pass. Retained recovery history requires intentional cleanup after review.

Full bidirectional writes, reviewed metadata edit plans and migration resolution remain Engine issue #23 scope. The W0 delivery used a bounded change plan for existing issues, then pulled/verified live state; it is not a generic automatic remote writer.

Milestone counters use GraphQL issue connections checked against fetched native issue states. REST-reported counters are retained separately with a consistency flag; a disagreement between GraphQL and fetched issues stops synchronization. This handles the observed W0 REST counter mismatch without changing issue state or hiding the reported source value.

`bootstrap-github.py`, `validate-bootstrap.py` and the bootstrap snapshot/report are frozen initial-baseline artifacts. Do not use them as current-state synchronization or validation after W0 changes; they intentionally describe earlier assumptions and IDs.
