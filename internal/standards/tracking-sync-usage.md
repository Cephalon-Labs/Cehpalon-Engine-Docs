# Reviewed GitHub ↔ Docs tracking synchronization

วันที่: 2026-10-27. Scope: existing Engine issues and organization Project 4; no issue/item creation, deletion, public release or provider provisioning.

`tools/sync_tracking.py` supports GitHub → Docs pulls and reviewed Docs → GitHub changes. It updates existing identities and keeps immutable readback snapshots. `tools/pull_tracking.py` remains the pull-only entry point. The bootstrap initializer remains frozen and must not be reused for synchronization.

## Editable mirror format

A reviewed pull migrates the original bullet headers into this format:

````markdown
# Engine issue #23

<!-- cehpalon-tracking:v1 -->
```json
{
  "schema_version": 1,
  "repository": "Cephalon-Labs/Cehpalon-Engine",
  "project_id": "PVT_kwDOEDryKs4Bo6sb",
  "identity": {"number": 23, "node_id": "actual issue node", "item_id": "actual Project item", "url": "https://github.com/Cephalon-Labs/Cehpalon-Engine/issues/23"},
  "issue": {"title": "Actual title", "type": "Task", "labels": ["area:governance"], "assignees": ["Cephalon-Neza"], "state": "open", "milestone_number": 1},
  "project": {"Status": "Ready", "Priority": "P1", "Estimate low (h)": 16, "Estimate (h)": 24, "Estimate high (h)": 32, "Actual (h)": null, "Remaining (h)": null, "Maturity": "M0", "Test gate": "Planned", "Benchmark gate": "Not required", "Feature": "governance"}
}
```
<!-- /cehpalon-tracking -->

<!-- cehpalon-issue-body -->
Actual issue Markdown body, including its Engine commit journal.
````

The identity values above are explanatory placeholders, not migration inputs. Work from the actual generated task mirror. Edit `issue`/`project` values or the body below the marker. Repository/project/issue number/node ID/item ID/URL are immutable in normal edits. The issue body is preserved exactly, including trailing newlines and existing CRLF sequences; the metadata header itself uses LF. No prose or commit journal is silently regenerated from the metadata. If the free-form body repeats tracking fields, update that prose intentionally in the same review.

Docs `.gitattributes` specifically sets `tasks/*.md -text` after the general Markdown LF rule. Git therefore stores and checks out task-mirror bytes without newline normalization, including a mixed LF metadata header/CRLF issue body, even when `core.autocrlf=true`. Keep that exception when changing repository formatting rules; changing body bytes invalidates the observed anchors. The offline regression stages an actual mirror in a temporary Git repository with the real attributes and compares its index blob byte-for-byte; it requires no commit.

Native Issue Type, Labels, assignees, title, body, state and milestone use issue APIs. Status/Priority, estimates, actual/remaining hours, Maturity, Test/Benchmark gate and Feature use Project fields. `null` clears a numeric field; `0` records measured zero. Known types, existing labels, assignable users, existing milestone numbers, option values and numeric validity are checked before remote mutations. New labels/milestones/types are not created automatically.

## Workflow

Run from the Docs checkout with the authenticated `Cephalon-Neza` account. The writer verifies the public Engine repository. Its visibility is part of the reviewed plan catalog digest, so plans created before the visibility change require a new review. Project 4 continues to require its existing private identity.

```powershell
python tools/sync_tracking.py pull
# Review fetched changes; edit the intended tasks/<number>.md.
python tools/sync_tracking.py plan --output .local/reviewed-plan.json
python tools/sync_tracking.py apply --plan .local/reviewed-plan.json
# Review exact operations, before/after values and merge notes in the plan.
python tools/sync_tracking.py apply --plan .local/reviewed-plan.json --execute --approve PLAN_SHA256
python tools/sync_tracking.py pull --check
```

The first `apply` is a dry run. Remote mutations require both `--execute` and the exact plan hash emitted by `plan`. This is a review gate for the concrete patch, not a request to execute arbitrary instructions from a plan. Plans/checkpoints/output artifacts must be JSON files inside this checkout's ignored `.local/`; no plan value selects an executable, API endpoint, repository or source-file output path.

A plan contains all exact proposed operations, immutable identities, issue revisions, full supported Project values, local mirror hashes, snapshot hash and current schema hash. Planning performs a three-way comparison against the last observed snapshot:

- A local-only field change becomes an exact proposed remote change.
- A remote-only field change is retained and pulled into the resulting mirror.
- The same resulting value on both sides is already converged.
- Different edits to the same field stop before mutation and show base/local/remote values.

After planning, changed local files, changed issue revision/body/state, changed Project values, changed field schema or unexpected issue-set changes reject apply. Project-only drift is checked even if the issue `updated_at` remains unchanged. Every existing 40-character SHA reference in the resulting card body must resolve through the Engine repository; abbreviated journal SHAs and Docs/Samples commit links are rejected. No fake SHA is needed to test synchronization.

## Explicit identity migration

Only existing destination issues inside the same Engine repository and Project 4 can be adopted. For a reviewed node/item-ID migration with stable issue number, save an exact mapping such as this to `.local/migration.json`:

```json
{
  "23": {
    "from": {"node_id": "old actual issue ID", "item_id": "old actual item ID"},
    "to": {"node_id": "new actual issue ID", "item_id": "new actual item ID"}
  }
}
```

Then use `plan --output .local/migration-plan.json --migrations .local/migration.json` and review normally. Both ends must match the snapshot/live identities exactly; REST and Project node membership must agree. The tool creates no replacement issues or items. Renumbering issues, moving to a different repository/Project, linking missing items or deleting tracking records requires a separate explicit migration operation; it is never inferred from a title match.

## Failure, checkpoints and recovery

Apply records an in-flight checkpoint before each native-issue PATCH or individual Project-field mutation, then reads back exact values before marking it complete. Default checkpoints are `.local/sync-checkpoints/<plan_sha256>.json`; `--checkpoint` can choose another `.local/*.json` file. Keep the plan and checkpoint together.

A checkpoint checksum is not authority to change the reviewed plan. Phase/index/in-flight coherence is validated; pre-commit local/snapshot anchors must equal the plan. A complete checkpoint requires every remote operation plus a final transaction whose mirror/body/metadata hashes derive from the reviewed desired state and agree with fresh readback. Rehashing a checkpoint cannot adopt a later local edit or skip unapplied work.

On a network failure or interrupted acknowledgement, reapply the same reviewed plan. The tool retries only if live state still equals the exact pre-operation state; it advances without replay if live state equals the exact intended result. Any third state stops for review. Completed operations are not silently rolled back. Reapplying a completed plan is a no-op only while its final remote/local state remains unchanged.

Mirrors and snapshot are staged as a recoverable local transaction, with snapshot committed last. Original/new copies and journals remain under `.local/tracking-transactions/`. A failed/interrupted local batch leaves `.local/tracking-pull-journal.json`, and subsequent pulls/applies refuse to run until that journal has been reviewed. A stale `.local/tracking-pull.lock` also needs owner/PID review; locks are not automatically stolen.

For local recovery, preserve any external edits first and compare each current target with the retained before/new hashes. Explicitly restore the reviewed old set or complete the exact new set, retain the reviewed journal/history, and only then remove the active recovery marker/stale lock. Resume the original plan after reconciliation. There is no automatic force-overwrite or recursive cleanup command.

## Bounds and proof limits

- REST issue/milestone lists, GraphQL Project items, Project schema fields and GraphQL milestone lists are paginated. A batch is bounded to 1,000 existing Engine issues and 12,000 remote operations. More than 100 populated values on one Project item is an explicit unsupported-bound error rather than a truncated observation. Current baseline has 23 issues.
- Stale REST milestone counters are retained as raw observations; independently agreeing GraphQL/native issue counts remain the recorded counts. Conflicting observations stop the sync. `pull --check` also compares milestone identity/title/state/description/due date and authoritative open/closed counts with the snapshot; only raw REST counter diagnostics are excluded from that equality check.
- The exclusive lock serializes cooperating processes within one checkout. Separate checkout writers and arbitrary editors require the program's single remote integrator discipline.
- GitHub issue and Project writes are not one atomic server transaction. There is a remaining check-to-mutation race with external writers; full-state optimistic guards and readback detect observed divergence but cannot guarantee compare-and-swap across services.
- Local replacement is atomic per file and recoverable across the batch. An arbitrary editor can still race the final hash check. This is not an unconditional filesystem/power-loss durability guarantee. Retained copies require reviewed retention/cleanup.
- Offline fake-transport tests establish conflict/metadata/recovery behavior. They do not prove live GitHub permissions, every API variant, runtime Engine behavior, hosted CI or maturity promotion. Record a bounded live readback test separately.

API references checked on 2026-10-27: [GitHub issue update API](https://docs.github.com/en/rest/issues/issues#update-an-issue) and [GitHub Project mutations](https://docs.github.com/en/graphql/reference/projects).
