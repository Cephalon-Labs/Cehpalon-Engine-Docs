from itertools import product
import json
from pathlib import Path
import sys


def read_rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def key(row):
    return row["transport"], row["operation"], row["scenario"]


def snapshot(succeeded=0, deadline=0, cancelled=0, faulted=0):
    return dict(Succeeded=succeeded, DeadlineExceeded=deadline,
                CallerCancelled=cancelled, Faulted=faulted)


root = Path(sys.argv[1])
disabled_schema, *disabled_cases = read_rows(root / "timeout-wire.jsonl")
enabled_schema, *enabled_rows = read_rows(root / "read-statistics.jsonl")
assert disabled_schema == enabled_schema == dict(
    kind="wire_timeout_schema", selected_paths=2,
    legacy_and_null_have_no_504=True, graphql_only_has_no_http_contract=True)
enabled_cases = [row for row in enabled_rows if row["kind"] == "wire_timeout_control"]
assert enabled_cases == disabled_cases
assert len(enabled_rows) == 41
expected = {
    "typed-timeout": ("audit.read_timeout", 504, snapshot(deadline=1)),
    "legacy-timeout": ("internal.error", 500, snapshot(deadline=1)),
    "provider-timeout": ("internal.error", 500, snapshot(faulted=1)),
    "caller-abort": (None, None, snapshot(cancelled=1)),
    "cross-tenant": ("access.denied", 403, snapshot()),
}
assert len(enabled_cases) == 20
assert {key(row) for row in enabled_cases} == set(
    product(("http", "graphql"), ("receipt", "resource"), expected))
statistics_rows = [row for row in enabled_rows if row["kind"] == "read_statistics_control"]
statistics = {key(row): row for row in statistics_rows}
assert len(statistics_rows) == len(statistics) == 20
for row in enabled_cases:
    scenario = row["scenario"]
    code, http, totals = expected[scenario]
    assert row["code"] == code
    assert row["status"] == (200 if http is not None and row["transport"] == "graphql" else http)
    assert row["source_queries"] == (0 if scenario == "cross-tenant" else 1)
    locked = scenario in ("typed-timeout", "legacy-timeout", "caller-abort")
    assert row["lock_observed"] == row["quiescent_under_lock"] == locked
    assert row["no_failed_result_published"] and row["successful_reuse"]
    assert statistics[key(row)]["failure_snapshot"] == totals
    assert statistics[key(row)]["snapshot_after_reuse"] == {**totals, "Succeeded": 1}

assert enabled_rows[-1] == dict(kind="read_statistics_shared",
    inactive_has_no_collector=True, snapshot=snapshot(succeeded=2))
for file, expected_count in [
    ("AuditTrail.json", 262), ("Http.json", 53), ("GraphQL.json", 49),
    ("offline/report.json", 8), ("wire/report.json", 8),
]:
    report = json.loads((root / file).read_bytes())
    assert report["passed"] == expected_count and report["failed"] == 0
print("Verified 20 matching wire outcomes per mode, 20 counter transitions, and a shared GraphQL collector.")
print("Each mode recorded 12 lock joins and four cross-tenant denials before SQL.")
