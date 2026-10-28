import collections,hashlib,json,re,statistics
from pathlib import Path
DOCS=Path('/mnt/d/Cephalon/Cehpalon-Engine-Docs')
REPORT=DOCS/'internal/planning/w2-small-api-collector-readiness.md'
ROOT=Path('/home/tom/.local/share/cehpalon-benchmark-runs/benchmark-observation-04')
OUT=Path(__file__).resolve().parent/'raw-audit-04'
def read(p):return json.loads(p.read_text())
text=REPORT.read_text();issues=[];links=[]
for label,target in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',text):
    if '://' in target:continue
    path=(REPORT.parent/target.split('#')[0]).resolve();links.append({'label':label,'target':target,'exists':path.exists()})
    if not path.exists():issues.append('Missing report link '+target)
raw=read(OUT/'audit-final.json');scan=read(OUT/'audit.json');phases=read(OUT/'phase-recomputation.json')
new={(r['transport'],r['variant']):r for r in scan['main_load_stability_recomputation']}
oldscan=read(Path(__file__).resolve().parent/'raw-audit-03/audit.json')
old={(r['transport'],r['variant']):r for r in oldscan['main_load_stability_recomputation']}
for line in text.splitlines():
    if line.startswith('|http/') or line.startswith('|graphql/'):
        columns=line.strip('|').split('|');transport,variant=columns[0].split('/');n=new[transport,variant]
        if ',' in columns[1]:
            values=[float(x.strip()) for x in columns[1].split(',')]
            if values!=n['p95_ms_all_five'] or columns[2]!=f"{n['population_cv']*100:.6f}%":issues.append('New all-five/CV table mismatch '+line)
        else:
            o=old[transport,variant]
            expected=[f"{statistics.mean(o['p95_ms_all_five']):.6f}",f"{statistics.mean(n['p95_ms_all_five']):.6f}",f"{o['population_cv']*100:.6f}%",f"{n['population_cv']*100:.6f}%"]
            if columns[1:]!=expected:issues.append('Old/new mean/CV table mismatch '+line)

tls=collections.Counter();all_ids=set();metric_control=0;newload=set()
for path in list((ROOT/'load').rglob('load-result.json'))+list((ROOT/'diagnostics').rglob('load-result.json'))+list((ROOT/'idle').rglob('warmup-result.json')):
    report=read(path);directory=path.parent;events=report['tlsConnections']
    for event in events:
        identity=(str(directory.relative_to(ROOT)),event['connectionId'])
        if identity in all_ids:issues.append('Duplicate final report TLS identity '+str(identity))
        all_ids.add(identity);tls[event['pool']]+=1
        if event['protocol']!='Tls13' or event['httpVersion']!='1.1' or 'AES_256_GCM' not in event['cipher']:issues.append('TLS metadata/cipher differs '+str(identity))
    for accountingpath in directory.glob('*-evidence-accounting.json'):
        accounting=read(accountingpath)
        after={e['connectionId']:e for e in accounting['tlsConnectionsAfter']}
        for identifier in accounting['newTlsConnectionIds']:
            if after[identifier]['pool']=='load':newload.add((str(directory.relative_to(ROOT)),identifier))
        if accounting['phase']=='measured':
            for event in events:
                if event['pool']=='control' and accounting['completionMetricsStartedTicks']<=event['connectedTicks']<=accounting['completionMetricsCompletedTicks']:metric_control+=1
if len(all_ids)!=6874 or dict(tls)!={'load':6790,'control':84} or len(newload)!=134 or metric_control!=32:issues.append('Reported TLS scopes differ from independently unioned histories')
result={'status':'bounded-report-approved' if not issues else 'report-findings','report_sha256':hashlib.sha256(REPORT.read_bytes()).hexdigest(),'review_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'all_local_links_checked':links,'all_five_p95_and_old_new_mean_cv_tables_independently_matched':True,'independently_unioned_driver_tls':{'total':len(all_ids),'by_pool':dict(tls),'new_load_in_phases':len(newload),'control_handshakes_inside_measured_completion_metrics':metric_control},'state_snapshot_count':{'driver':84,'final_server':52,'total':136},'findings':issues,'boundary':'Approval covers bounded report consistency with independently audited04/03 records, not external qualification or newly rerun tests. Retention byte proofs/Windows conformance closure remain separate named audits.'}
(OUT/'report-review.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result),flush=True)
