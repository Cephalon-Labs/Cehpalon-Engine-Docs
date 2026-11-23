import itertools, json, sys
from pathlib import Path

root = Path(sys.argv[1])
rows = [json.loads(line) for line in (root/'timeout-wire.jsonl').read_text().splitlines()]
schema, *cases = rows
assert schema == dict(kind='wire_timeout_schema', selected_paths=2, legacy_and_null_have_no_504=True,
                      graphql_only_has_no_http_contract=True)
transports = ('http', 'graphql')
operations = ('receipt', 'resource')
scenarios = ('typed-timeout', 'legacy-timeout', 'provider-timeout', 'caller-abort', 'cross-tenant')
assert len(cases) == 20
assert {(r['transport'], r['operation'], r['scenario']) for r in cases} == set(itertools.product(transports, operations, scenarios))
expected = {
    'typed-timeout': ('audit.read_timeout', 504),
    'legacy-timeout': ('internal.error', 500),
    'provider-timeout': ('internal.error', 500),
    'caller-abort': (None, None),
    'cross-tenant': ('access.denied', 403),
}
for row in cases:
    scenario = row['scenario']
    code, http = expected[scenario]
    assert row['kind'] == 'wire_timeout_control'
    assert row['code'] == code and row['status'] == (200 if http and row['transport'] == 'graphql' else http)
    assert row['source_queries'] == (0 if scenario == 'cross-tenant' else 1)
    locked = scenario in ('typed-timeout', 'legacy-timeout', 'caller-abort')
    assert row['lock_observed'] == row['quiescent_under_lock'] == locked
    assert row['no_failed_result_published'] and row['successful_reuse']
for file, expected_count in [('AuditTrail.json',253),('Http.json',53),('GraphQL.json',49),('offline/report.json',8),('wire/report.json',8)]:
    report = json.loads((root/file).read_bytes())
    assert report['passed']==expected_count and report['failed']==0
print('Verified schema, 20 wire controls, 12 lock joins, 4 denials before SQL, and all existing targeted suites.')
