from pathlib import Path
import hashlib, json, statistics, sys
root = Path(sys.argv[1])
result = json.loads((root/'summary.json').read_text())
assert result['status']=='passed' and not result['preflight']
assert result['fixture']['settings']['server_version'].startswith('PostgreSQL 18.7 ')
seen = set()
counts = dict(measured=0, warmups=0, controls=0, denied=0)
digests = {}
batches = {}
for pair, order in enumerate([('before','after'),('after','before'),('before','after'),('after','before')], 1):
    for lane in order:
        fp = root/f'pair-{pair}-{lane}.jsonl'
        lines = [json.loads(line) for line in fp.read_text().splitlines()]
        controls = [r for r in lines if r['kind'] == 'control']
        assert len(controls) == 18
        counts['controls'] += 18
        for c in controls:
            name = c['name']
            positive = name in ('A-owner','B-owner','membership-restored')
            assert (c['queries'], c['handlers'], c['results']) == ((1,1,1) if positive else (0,0,0)), c
            if not positive: counts['denied'] += 1
        actual = [r for r in lines if r['kind'] == 'batch']
        assert len(actual) == 4
        drawn = [('http',25),('graphql',25),('http',200),('graphql',200)]
        i = (pair-1)%4
        assert [(r['transport'],r['limit']) for r in actual] == drawn[i:]+drawn[:i]
        for b in actual:
            group=(b['transport'],b['limit'])
            entries=[r for r in lines if r['kind']=='request' and (r['transport'],r['limit'])==group]
            assert len(entries)==120
            warmups,measured=entries[:20],entries[20:]
            assert all(not r['measured'] for r in warmups) and all(r['measured'] for r in measured)
            assert [r['index'] for r in warmups]==list(range(20))
            assert [r['index'] for r in measured]==list(range(100))
            assert all(r['tenant']==('A' if r['index']%2==0 else 'B') and r['bytes']>0 for r in entries)
            counts['measured'] += len(measured)
            counts['warmups'] += len(warmups)
            for r in entries:
                assert digests.setdefault((r['tenant'],r['limit']),r['digest'])==r['digest']
            connections=[r for r in lines if r['kind']=='connection' and (r['transport'],r['limit'])==group]
            assert len(connections)==1 and connections[0]['tls'] in ('TLSv1.2','TLSv1.3')
            ordered=sorted(r['latency_ns'] for r in measured)
            assert [b[k] for k in ('p50_ns','p95_ns','p99_ns')] == [ordered[49],ordered[94],ordered[98]]
            assert b['samples']==100 and b['source_queries']==100
            assert all(b['after'][k]-b['before'][k]==100 for k in ('queries','handlers','results'))
            assert b['after']['allocated']-b['before']['allocated']==b['allocated_bytes']>0
            assert b['before']['active']==b['after']['active']==0
            batches[(pair,lane,*group)] = b
assert counts == dict(measured=3200,warmups=640,controls=144,denied=96),counts
assert len(batches)==32 and len(digests)==4 and all(digests['A',n]!=digests['B',n] for n in (25,200))
assert {tuple((r['pair'],r['lane'],r['transport'],r['limit'])):r for r in result['batches']}==batches
print(json.dumps(counts))
for cell in result['comparisons']:
    group=(cell['transport'],cell['limit'])
    old=[batches[(pair,'before',*group)] for pair in range(1,5)]
    new=[batches[(pair,'after',*group)] for pair in range(1,5)]
    measures=(('p50_ns','p50_ms',1e6),('p95_ns','p95_ms',1e6),('p99_ns','p99_ms',1e6),('allocated_bytes','bytes_per_request',100))
    values={}
    for raw,key,scale in measures:
        a=[b[raw]/scale for b in old]
        b=[b[raw]/scale for b in new]
        delta=statistics.median((y/x-1)*100 for x,y in zip(a,b))
        assert abs(delta-cell['median_paired_percent'][key])<1e-6
        values[key]=dict(before=round(statistics.median(a),3),after=round(statistics.median(b),3),paired_percent=round(delta,2))
    print(json.dumps(dict(transport=group[0], limit=group[1], **values)))
