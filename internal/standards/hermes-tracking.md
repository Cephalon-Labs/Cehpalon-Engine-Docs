# Engine tracking across GitHub, Docs and Hermes

| Record | Source of truth | Projection |
|---|---|---|
| Engine issues, item status, fields, owners and milestones | `Cephalon-Labs/Cehpalon-Engine` and [Project 4](https://github.com/orgs/Cephalon-Labs/projects/4) | Reviewed Docs task mirrors and milestone snapshot; Hermes reference tasks by issue number or milestone number. |
| Native sub-issues | GitHub parent/child relation | Follow the parent issue link for the current hierarchy. Body checklists remain checklists in Docs. The current bridge does not import native hierarchy or create native sub-issues; Hermes dependency links are not a substitute. |
| Plans, requirements, ADRs, evidence, and other documents | This repository | Link the versioned paths from relevant GitHub issues and from Hermes references. The Hermes document index points to the program plan and navigation entry points; documents are not copied into task bodies. |
| Company approvals, execution subtasks, logs and local evidence | Hermes `cephalon-company` | Link the relevant canonical issue/document in the work package. Only reviewed, authorized tracking changes are sent back through GitHub/Docs. Never promote a GitHub item based solely on Hermes status. |

`cephalon-engine-mirror` contains the same read-only reference records in Hermes Kanban and its task list. All generated cards are left **blocked and unassigned** to keep them out of the dispatch queue; that status is not the GitHub issue/Project status. Do not put local execution tasks or manual edits there. Keep G0/G1/G2 and deferred product #4 on `cephalon-company`.

## Refresh and verify

1. With authorized Project access, use `python tools/sync_tracking.py pull --check` to assess drift and `python tools/sync_tracking.py pull` to update Docs under the [reviewed GitHub/Docs workflow](tracking-sync-usage.md). To propose upstream changes, use its plan, dry run, exact-hash approval and readback sequence. Do not bypass conflict detection or the repository's publication review. For new/deleted items, native sub-issue links, milestone edits and identity migrations, follow the approved owner workflow; this bridge never writes GitHub.
2. Once the snapshot and its mirrors are committed together in the reviewed Docs revision, run from that checkout:

   ```sh
   python tools/hermes_tracking.py --kanban-home "$HOME/.hermes"          # plan only
   python tools/hermes_tracking.py --kanban-home "$HOME/.hermes" --apply  # dedicated mirror only
   python tools/hermes_tracking.py --kanban-home "$HOME/.hermes"          # expect create=0, edit=0
   ```

   Pass the actual shared Kanban root if it differs from `$HOME/.hermes`, not a profile directory. Add `--hermes /app/venv/bin/hermes` if the CLI is not on `PATH`. The bridge pins the mirror database and does not inherit worker Kanban routing overrides. The plan opens SQLite in read-only mode rather than running `kanban list`, which can recompute readiness. Links use the committed Docs revision; use a published checkout for shared links. The card header records the GitHub snapshot timestamp. A GitHub REST issue read is not live Project verification.
3. Re-run the read-only plan to verify the target; apply also checks readback. An unexpected, archived, missing-source or assigned card stops the bridge; no deletions or title-based matching. Use one controller and do not edit the reference board from the UI or another process during apply. The lock at `<kanban-home>/.cephalon-engine-mirror.lock` coordinates only this tool, not other Hermes writers. Each CLI write is checked before proceeding; the sequence is not atomic and completed writes are not rolled back. After any ambiguous CLI failure, read back the exact mirror board before retrying, and verify the PID and operator state before removing a stale lock.

No scheduler or GitHub writer is enabled by this bridge. A durable cross-system job requires an approved identity with Project access, an owner, conflict handling, freshness monitoring, and a reviewed workflow for native hierarchy and writes.
