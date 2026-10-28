"""Independent retained-record audit; no workload execution or acceptance relaxation."""
import array, collections, datetime, gzip, hashlib, json, math, statistics, subprocess, time
from pathlib import Path

ROOT=Path('/home/tom/.local/share/cehpalon-benchmark-runs/benchmark-observation-03')
OUT=Path(__file__).resolve().parent/'raw-audit-03'
OUT.mkdir(exist_ok=False)
SEED='cehpalon-small-api-v1:20261027'
issues=[]; counts=collections.Counter(); phases=[]; manifests=[]; tls=set(); expected_cache={}; state_cache={}; accounting_reports=[]; owned_identities=[]
def check(ok,message):
    if not ok: issues.append(message)
def read(path): return json.loads(path.read_text(encoding='utf-8'))
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def pct(values,p): return sorted(values)[max(0,math.ceil(len(values)*p)-1)] if values else 0
def close(a,b): return isinstance(a,(int,float)) and isinstance(b,(int,float)) and math.isclose(a,b,rel_tol=1e-11,abs_tol=1e-9)
def expected(i,transport):
    key=(i,transport)
    if key in expected_cache: return expected_cache[key]
    number=int.from_bytes(hashlib.sha256(f'{SEED}:{i}'.encode()).digest()[:8],'big')
    op='get' if i%100<80 else 'list' if i%100<95 else 'set'
    id=1+number%10000;page=number%500;lane=ordinal=-1;rev=0;label=None
    if op=='set':
        w=(i//100)*5+(i%100-95);lane=w%32;ordinal=w//32;id=1+lane+32*(ordinal%312);rev=ordinal//312;label=f'lane-{lane}-write-{ordinal}'
        inp={'id':id,'expectedRevision':rev,'label':label}
    else: inp={'id':id} if op=='get' else {'page':page}
    field={'get':'catalogItem','list':'catalogPage','set':'setLabel'}[op]
    typ={'get':'GetItemInput!','list':'ListItemsInput!','set':'SetLabelInput!'}[op]
    selection='items { id label revision amountMinorUnits }' if op=='list' else 'id label revision amountMinorUnits'
    payload=inp if transport=='http' else {'query':f'{"mutation" if op=="set" else "query"}($input:{typ}){{{field}(input:$input){{{selection}}}}}','variables':{'input':inp}}
    payload_hash=hashlib.sha256(json.dumps(payload,separators=(',',':')).encode()).hexdigest()
    prefix=f'{i}:{op}:{id}:{page}:{lane}:{ordinal}:{rev}:{label or ""}:'
    value=(op,id,page,lane,ordinal,rev,label,payload_hash,prefix)
    expected_cache[key]=value;return value

def audit_manifest(driver,report,n):
    wh=hashlib.sha256();lh=hashlib.sha256();seen=0
    p=driver/'offered-manifest.jsonl.gz'
    with gzip.open(p,'rt',encoding='utf-8') as f:
        for i,line in enumerate(f):
            r=json.loads(line);e=expected(i,report['transport'])
            actual=tuple(r.get(k) for k in ['operation','id','page','lane','ordinal','expectedRevision','label','payloadSha256'])
            check(r.get('index')==i and actual==e[:8],f'{p.relative_to(ROOT)}: manifest mismatch index{i}')
            wh.update((e[8]+e[7]+'\n').encode());lh.update((e[8]+'\n').encode());seen+=1
    check(seen==n,f'{p.relative_to(ROOT)}: row count {seen}!={n}')
    check(wh.hexdigest()==report['manifestHash'],f'{p.relative_to(ROOT)}: wire hash mismatch')
    check(lh.hexdigest()==report['logicalManifestHash'],f'{p.relative_to(ROOT)}: logical hash mismatch')
    counts['manifest_rows']+=seen;counts['gzip_files']+=1
    manifests.append({'path':str(p.relative_to(ROOT)),'rows':seen,'wire_hash':wh.hexdigest(),'logical_hash':lh.hexdigest(),'gzip_sha256':digest(p)})

def audit_phase(driver,name,rate,n,seconds,reported):
    p=driver/(name+'-requests.jsonl.gz');seen=bytearray(n);lat=[];sentlat=[];starts=[];ends=[];errors=collections.Counter();ops=collections.Counter();start=None;correct=within=rows=0;maxqueue=0;maxdone=0;timeouts=0
    with gzip.open(p,'rt',encoding='utf-8') as f:
        header=json.loads(next(f));freq=header['frequency']
        check(header.get('schema')==1 and len(header.get('columns',[]))==8,f'{p}: unknown header')
        for line in f:
            r=json.loads(line);rows+=1
            if len(r)!=8: issues.append(f'{p}: malformed row');continue
            i,op,sched,sent,done,status,size,error=r
            if not isinstance(i,int) or i<0 or i>=n or seen[i]: issues.append(f'{p}: duplicate/out-of-range index{i}');continue
            seen[i]=1
            expected_op='get' if i%100<80 else 'list' if i%100<95 else 'set'
            check(op==expected_op,f'{p}: wrong operation index{i}');ops[op]+=1
            origin=sched-(i*freq//rate)
            if start is None: start=origin
            check(origin==start,f'{p}: offered schedule changed index{i}')
            check(done>=sched and (sent==0 or sched<=sent<=done),f'{p}: inconsistent timestamps index{i}')
            if not error:
                correct+=1;check(status==200 and size>0 and sent>0,f'{p}: successful row has invalid status/body/sent index{i}')
                if done<=start+(seconds+1)*freq: within+=1
            else: errors[error]+=1
            latency=(done-sched)*1000/freq;lat.append(latency);maxdone=max(maxdone,done)
            if latency>1000+1e-6: timeouts+=1
            if sent:
                sentlat.append((done-sent)*1000/freq);maxqueue=max(maxqueue,sent-sched)
                if done>sent: starts.append(sent);ends.append(done)
    check(rows==n and all(seen),f'{p}: missing offered records')
    dropped=errors['offered.dropped'];summary={'offered':rows,'correct':correct,'errors':sum(errors.values()),'dropped':dropped,'successfulWithinDrain':within,'p95Ms':pct(lat,.95),'p99Ms':pct(lat,.99),'sentP95Ms':pct(sentlat,.95),'maximumQueueMs':maxqueue*1000/freq,'elapsedMs':(maxdone-start)*1000/freq,'errorKinds':dict(errors)}
    for k,v in summary.items():
        check((close(v,reported.get(k)) if isinstance(v,float) else v==reported.get(k)),f'{p.relative_to(ROOT)}: report {k} mismatch audited={v} reported={reported.get(k)}')
    starts.sort();ends.sort();j=active=peak=0
    for s in starts:
        while j<len(ends) and ends[j]<=s:active-=1;j+=1
        active+=1;peak=max(peak,active)
    check(peak<=128,f'{p}: reconstructable network concurrency exceeds128')
    check(ops=={'get':n*80//100,'list':n*15//100,'set':n*5//100},f'{p}: traffic mix mismatch')
    accounting=read(driver/(name+'-evidence-accounting.json'))
    check(accounting['phase']==name and accounting['offeredCount']==n and accounting['observedCount']==n,f'{p}: accounting count mismatch')
    check(accounting['phaseStartedTicks']==start and accounting['requestsCompletedTicks']>=maxdone,f'{p}: phase accounting timestamp mismatch')
    cb,ca=accounting['clientBefore'],accounting['clientAfter']
    check(cb['observedTicks']<=start<=maxdone<=accounting['requestsCompletedTicks']<=ca['observedTicks']<=accounting['persistenceStartedTicks']<=accounting['persistenceCompletedTicks'],f'{p}: client/persistence order mismatch')
    for key in ['cpuMilliseconds','gc0','gc1','gc2','threadPoolCompletedWorkItems']:
        check(ca[key]>=cb[key],f'{p}: cumulative client telemetry decreased '+key)
    if name=='measured':
        check(ca['observedTicks']<=accounting['completionMetricsStartedTicks']<=accounting['completionMetricsCompletedTicks']<=accounting['persistenceStartedTicks'],f'{p}: completion server metrics not before persistence')
    else:check(accounting['completionMetricsStartedTicks'] is None and accounting['completionMetricsCompletedTicks'] is None,f'{p}: unexpected server metric control in non-measured phase')
    check(accounting['phaseFailure'] is None,f'{p}: managed phase failure recorded')
    accounting_reports.append({'path':str(p.relative_to(ROOT)),'phase_start':start,'requests_completed':accounting['requestsCompletedTicks'],'client_before':cb,'client_after':ca,'server_metric_control_before_persist':name=='measured','persistence_duration_ms':(accounting['persistenceCompletedTicks']-accounting['persistenceStartedTicks'])*1000/freq})
    counts['phase_rows']+=rows;counts['gzip_files']+=1;counts['semantic_error_flags']+=sum(errors.values());counts['timeout_budget_exceeding_rows']+=timeouts
    result={'path':str(p.relative_to(ROOT)),'rate':rate,'seconds':seconds,'summary':summary,'maximum_reconstructable_network_overlap':peak,'over_1s_scheduled_latency_rows':timeouts,'gzip_sha256':digest(p)};phases.append(result)
    return result

def expected_state(n):
    if n in state_cache:return state_cache[n]
    records=[{'id':i,'label':f'item-{i:05}','revision':0,'amountMinorUnits':i*17} for i in range(1,10001)]
    for w in range(n*5//100):
        lane=w%32;ordinal=w//32;id=1+lane+32*(ordinal%312)
        records[id-1]={'id':id,'label':f'lane-{lane}-write-{ordinal}','revision':ordinal//312+1,'amountMinorUnits':id*17}
    h=hashlib.sha256(json.dumps(records,separators=(',',':')).encode()).hexdigest();state_cache[n]=(records,h);return records,h

def audit_state(state,n,name):
    records,h=expected_state(n)
    check(state.get('records')==records,f'{name}: independently regenerated final state mismatch')
    check(state.get('stateHash')==h,f'{name}: final state hash mismatch')
    check(state.get('factories')==state.get('disposals'),f'{name}: handler ownership imbalance')
    check(state.get('factories')==n and state.get('reads')==n*95//100 and state.get('writes')==n*5//100,f'{name}: business counters not conserved')
    counts['complete_state_snapshots']+=1

def audit_shutdown(directory,transport):
    r=read(directory/'shutdown.json');state=read(directory/'final-state.json');p=state['probes']
    ready=read(directory/'ready.json');invocation=read(directory/'invocation.json');variant=directory.name.split('-',1)[1]
    check(ready['variant']==variant and state['variant']==variant and ready['transport']==transport and state['transport']==transport,f'{directory}: variant/transport identity mismatch')
    check('--variant='+variant in invocation['command'] and '--transport='+transport in invocation['command'],f'{directory}: invocation identity mismatch')
    mappings=read(directory/'loaded-runtime.json')
    check(mappings['process_id']==ready['processId'] and mappings['inspection_after_first_response'] is True,f'{directory}: runtime mapping identity mismatch')
    check(len(mappings['paths'])==4 and all(x.startswith(root_manifest['deployment']['dotnet'].rsplit('/',1)[0]+'/') for x in mappings['paths']),f'{directory}: runtime not resolved from declared native SDK')
    owned_identities.append({'directory':str(directory.relative_to(ROOT)),'pid':ready['processId'],'variant':variant,'transport':transport,'invocation_utc':invocation['observed_at_utc']})
    check(r['passed'] and r['graceful'] and r['exit_code']==0 and r['listener_closed'] and r['elapsed_ms']<=5000,f'{directory}: shutdown failure')
    check(state['factories']==state['disposals'],f'{directory}: final lifetime imbalance')
    check(p.get('forbiddenFactories')==0,f'{directory}: forbidden factory work')
    gkeys=['graphQLFactories','graphQLServices','graphQLDiagnosticConstructors','graphQLExecutorInitializations','graphQLSchemasReady']
    if transport=='http':check(all(p.get(k)==0 for k in gkeys),f'{directory}: disabled GraphQL activation')
    else:check(all(isinstance(p.get(k),int) and p[k]>0 for k in gkeys),f'{directory}: enabled GraphQL diagnostics missing')
    first=read(directory/'first-response.json');body=first['body'] if transport=='http' else first['body']['data']['catalogItem']
    check(body=={'id':1,'label':'item-00001','revision':0,'amountMinorUnits':17},f'{directory}: first verified payload mismatch')
    check(first.get('tls_protocol')=='TLSv1.3' and first.get('tls_cipher'),f'{directory}: TLS evidence absent')
    tls.add(tuple(first['tls_cipher']));counts['server_shutdowns']+=1

def audit_driver(report_path,warm_only=False):
    report=read(report_path);driver=report_path.parent;rate=report['rate'];n=rate*(60 if warm_only else 180)
    check(report['warmSeconds']==60 and (warm_only or report.get('seconds')==180),f'{driver}: duration changed')
    audit_manifest(driver,report,n)
    pre=read(driver/'collector-preflight.json');audit_phase(driver,'preflight',rate,rate*2,2,pre['preflight']);check(pre['state']['passed'],f'{driver}: failed collector preflight')
    prep=read(driver/'collector-preparation.json');check(len(prep['requests'])==130 and all(not x['error'] and x['status']==200 for x in prep['requests']),f'{driver}: collector preparation failure')
    audit_phase(driver,'warmup',rate,rate*60,60,report['warmup'])
    if warm_only:audit_state(report['finalState'],rate*60,str(driver))
    else:
        audit_state(report['initialState'],0,str(driver)+' initial');audit_state(report['finalState'],n,str(driver)+' final')
        audit_phase(driver,'measured',rate,n,180,report['measured'])
    for connection in report['tlsConnections']:
        check(connection['protocol']=='Tls13' and connection['httpVersion']=='1.1' and connection['connectedTicks']>0 and connection['stopwatchFrequency']==1000000000,f'{driver}: unexpected TLS/HTTP/clock metadata')
        tls.add((connection['cipher'],'TLSv1.3',256))
    audit_shutdown(driver.parent,report['transport'])
    return report

started=time.time();root_manifest=read(ROOT/'manifest.json');check(root_manifest['reference_environment_qualified'] is False,'Reference environment unexpectedly qualified')
main_reports=sorted((ROOT/'load').rglob('load-result.json'));idle_reports=sorted((ROOT/'idle').rglob('warmup-result.json'));diagnostic_reports=sorted((ROOT/'diagnostics').rglob('load-result.json'))
check((len(main_reports),len(idle_reports),len(diagnostic_reports))==(20,20,11),'Planned main/idle/timed-diagnostic counts mismatch')
audited_main={};audited_diag={}
for i,p in enumerate(main_reports+idle_reports+diagnostic_reports):
    print('AUDIT',i+1,'/',51,str(p.relative_to(ROOT)),flush=True)
    r=audit_driver(p,p.name=='warmup-result.json')
    if p in main_reports:audited_main[p.parent.parent]=r;check(r['rate']==1000,f'{p}: main rate changed')
    if p in diagnostic_reports:audited_diag[p.parent.parent]=r;check(r['rate'] in [100,500,2000],f'{p}: unexpected diagnostic rate')

failed_driver=ROOT/'diagnostics/http/2000-engine/driver'
stdout=[json.loads(x) for x in (failed_driver/'stdout.txt').read_text().splitlines() if x.startswith('{')]
frozen=[x for x in stdout if x.get('stage')=='manifest-frozen'];check(len(frozen)==1,'Failed diagnostic must retain exactly one frozen invocation')
pseudo={**frozen[0],'transport':'http'};audit_manifest(failed_driver,pseudo,360000)
pre=read(failed_driver/'collector-preflight.json');failed_phase=audit_phase(failed_driver,'preflight',2000,4000,2,pre['preflight'])
check(failed_phase['summary']['correct']==3963 and failed_phase['summary']['errors']==37 and failed_phase['summary']['dropped']==37 and failed_phase['summary']['errorKinds']=={'offered.dropped':37},'Expected diagnostic preflight failure was not retained exactly')
check(pre['state']['passed'] is True,'Failed read-capacity preflight unexpectedly changed planned write state')
check(not any((failed_driver/x).exists() for x in ['load-result.json','warmup-result.json','warmup-requests.jsonl.gz','measured-requests.jsonl.gz']),'Failed preflight incorrectly entered timed phases')
prep=read(failed_driver/'collector-preparation.json');check(len(prep['requests'])==130 and all(x['status']==200 and not x['error'] for x in prep['requests']),'Failed diagnostic had an unaccounted preparation fault')
failed_observation=read(failed_driver.parent/'observation.json');check(failed_observation['timed_measurement_executed'] is False and failed_observation['diagnostic_status']=='collector-preflight-failed' and failed_observation['driver_exit_code']!=0,'Failed preflight classification/exit was not retained')
failed_state=read(failed_driver.parent/'final-state.json');records,h=expected_state(4000);check(failed_state['records']==records and failed_state['stateHash']==h,'Failed diagnostic final200write state mismatch')
check(failed_state['factories']==failed_state['disposals']==4093 and failed_state['reads']==3893 and failed_state['writes']==200,'Failed diagnostic preparation+admitted-work conservation mismatch')
counts['complete_state_snapshots']+=1;audit_shutdown(failed_driver.parent,'http')
check(len(list((ROOT/'diagnostics').rglob('invocation.json')))==24,'Diagnostic must retain12 server+12 driver attempts, no retry')

startup=read(ROOT/'startup-observations.json');check(len(startup)==120,'Startup count !=120');startup_results=[]
for transport in ['http','graphql']:
    arrays={v:[] for v in ['baseline','engine']}
    for row in startup:
        if row['transport']!=transport:continue
        d=ROOT/'startup'/transport/(f"{row['index']:02}-"+row['variant']);audit_shutdown(d,transport)
        computed=(row['ready_and_verified_monotonic_ns']-row['started_monotonic_ns'])/1e6
        check(close(computed,row['startup_milliseconds']),f'{d}: startup timestamp mismatch');arrays[row['variant']].append(computed)
    check(all(len(v)==30 for v in arrays.values()),f'{transport}: startup launches missing')
    b,e=pct(arrays['baseline'],.95),pct(arrays['engine'],.95);passed=b<=1000 and e<=1000 and e<=b+150
    saved=next(x for x in read(ROOT/'startup-summary.json') if x['transport']==transport)
    check(close(b,saved['baseline_p95_ms']) and close(e,saved['engine_p95_ms']) and passed==saved['budget_observation_passed'],f'{transport}: startup summary mismatch')
    startup_results.append({'transport':transport,'baseline_p95_ms':b,'engine_p95_ms':e,'absolute_budget_passed':b<=1000 and e<=1000,'overhead_budget_passed':e<=b+150})

idle_rows=read(ROOT/'idle-observations.json');check(len(idle_rows)==20,'Idle count !=20');idle_results=[]
for row in idle_rows:
    d=ROOT/'idle'/row['transport']/(f"{row['pair']:02}-"+row['variant']);samples=read(d/'rss-samples.json');check(len(samples)==60,f'{d}: sample count !=60')
    values=[s['rss_bytes'] for s in samples]
    for i,s in enumerate(samples):
        target=row['idle_started_monotonic_ns']+(120+i)*1000000000
        check(s['index']==i and s['scheduled_monotonic_ns']==target and target<=s['observed_monotonic_ns']<target+1000000000,f'{d}: missed/malformed RSS slot{i}')
    med=statistics.median(values);check(med==row['median_rss_bytes'] and max(values)==row['maximum_rss_bytes'],f'{d}: RSS summary mismatch')
    check(max(values)<=256*1024*1024,f'{d}: RSS absolute budget exceeded');counts['rss_samples']+=60
for row in read(ROOT/'idle-summary.json'):
    b=next(x for x in idle_rows if x['pair']==row['pair'] and x['transport']==row['transport'] and x['variant']=='baseline')
    e=next(x for x in idle_rows if x['pair']==row['pair'] and x['transport']==row['transport'] and x['variant']=='engine')
    passed=e['median_rss_bytes']<=b['median_rss_bytes']+16*1024*1024 and b['maximum_rss_bytes']<=256*1024*1024 and e['maximum_rss_bytes']<=256*1024*1024
    check(passed==row['budget_observation_passed'],f'{row}: idle pair gate mismatch');idle_results.append({'transport':row['transport'],'pair':row['pair'],'passed':passed})

load_results=[];cv_results=[]
for transport in ['http','graphql']:
    for pair in range(5):
        b=audited_main[ROOT/'load'/transport/f'{pair:02}-baseline'];e=audited_main[ROOT/'load'/transport/f'{pair:02}-engine']
        def allocation(r):return (r['finalMetrics']['totalAllocatedBytes']-r['initialMetrics']['totalAllocatedBytes'])/180000
        bm,em=b['measured'],e['measured'];latency=all(r['measured']['p95Ms']<=20 and r['measured']['p99Ms']<=50 for r in [b,e]);extra=em['p95Ms']<=bm['p95Ms']+max(1,.15*bm['p95Ms']);alloc=allocation(e)<=allocation(b)+1024
        check(b['manifestHash']==e['manifestHash'] and b['logicalManifestHash']==e['logicalManifestHash'] and b['finalState']['stateHash']==e['finalState']['stateHash'],f'{transport} pair{pair}: pair parity mismatch')
        saved=next(x for x in read(ROOT/'load-pairs.json') if x['transport']==transport and x['pair']==pair)
        check(latency and extra and alloc==saved['allocation_overhead_passed'] and extra==saved['p95_overhead_passed'],f'{transport} pair{pair}: numeric gate mismatch')
        load_results.append({'transport':transport,'pair':pair,'latency_absolute_passed':latency,'latency_extra_passed':extra,'allocation_extra_passed':alloc,'baseline_bytes_per_offered':allocation(b),'engine_bytes_per_offered':allocation(e)})
    for variant in ['baseline','engine']:
        values=[audited_main[ROOT/'load'/transport/f'{pair:02}-{variant}']['measured']['p95Ms'] for pair in range(5)]
        cv=statistics.pstdev(values)/statistics.mean(values);saved=next(x for x in read(ROOT/'load-summary.json')['stability'] if x['transport']==transport and x['variant']==variant)
        check(close(cv,saved['population_coefficient_of_variation']) and (cv<=.1)==saved['budget_observation_passed'],f'{transport}/{variant}: CV mismatch')
        cv_results.append({'transport':transport,'variant':variant,'p95_ms_all_five':values,'population_cv':cv,'budget_passed':cv<=.1})

source_verified=0
for key,h in root_manifest['source_sha256'].items():
    repo,relative=key.split('/',1);folder=Path('/mnt/d/Cephalon')/('Cehpalon-Engine-Samples' if repo=='samples' else 'Cehpalon-Engine');revision=root_manifest['samples_revision' if repo=='samples' else 'engine_revision']
    raw=subprocess.check_output(['git','show',revision+':'+relative],cwd=folder)
    check(hashlib.sha256(raw).hexdigest()==h,'Committed source hash mismatch '+key);source_verified+=1
assembly=Path(root_manifest['assembly']);check(digest(assembly)==root_manifest['assembly_sha256'],'Assembly hash mismatch');check(digest(assembly.with_suffix('.deps.json'))==root_manifest['deps_sha256'],'Deps hash mismatch')
build_sources_verified={}
for host in ['linux','win']:
    build_manifest=read(Path('/mnt/d/Cephalon/Cehpalon-Engine-Samples/.local')/('tuning-conformance-'+host+'-01')/'manifest.json')
    check(build_manifest['samples_source_revision']==root_manifest['samples_revision'] and build_manifest['source_state']=='exact clean committed source',f'{host}: build source provenance revision mismatch')
    for key,h in build_manifest['source_sha256'].items():check(root_manifest['source_sha256'].get('samples/'+key)==h,f'{host}: build/orchestration source mismatch '+key)
    if host=='linux':check(build_manifest['assembly_sha256']==root_manifest['assembly_sha256'],'Native staged assembly does not match Linux build')
    build_sources_verified[host]=len(build_manifest['source_sha256'])
progress=[json.loads(x) for x in (ROOT/'progress-events.jsonl').read_text().splitlines()];max_clock=max(abs(x.get('wall_monotonic_offset_deviation_ns',0)) for x in progress);check(max_clock<1000000000,'Clock continuity deviation >=1second')
actual_gz=set(ROOT.rglob('*.gz'));audited_gz={ROOT/x['path'] for x in phases+manifests};check(actual_gz==audited_gz,'Unaccounted gzip evidence files')
check(counts['phase_rows']==8116800 and counts['manifest_rows']==6672000 and counts['gzip_files']==186,'Independent expected raw totals mismatch')
summary={'observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'consistent' if not issues else 'audit-findings','audit_script_sha256':digest(Path(__file__)),'input':str(ROOT),'input_manifest_sha256':digest(ROOT/'manifest.json'),'elapsed_seconds':time.time()-started,'counts':dict(counts),'main_load_runs':20,'idle_runs':20,'startup_launches':120,'diagnostic_attempts':12,'diagnostic_timed_runs':11,'source_files_verified_against_recorded_commits':source_verified,'assembly_and_build_provenance_matched':True,'build_source_inputs_verified_per_host':build_sources_verified,'observed_tls_cipher_tuples':sorted(tls),'maximum_recorded_clock_offset_deviation_ns':max_clock,'startup_numeric_recomputation':startup_results,'idle_pair_recomputation':idle_results,'main_load_pair_recomputation':load_results,'main_load_stability_recomputation':cv_results,'reference_environment_qualified':False,'benchmark_acceptance_passed':False,'findings':issues,'limits':['Raw offered records include status, byte count and driver semantic error classification, not full response payloads; individual business response contents cannot be independently replayed offline.','Preflight retains driver final-state validation outcome but not its complete snapshot; measured/warm-only final snapshots were independently regenerated and compared.','Network overlap from sent/completed records is reconstructable; admission/writer-queue occupancy timestamps are not retained.','Source/assembly/build hashes prove retained provenance consistency, not an independent reproducible rebuild or runtime attestation.','Shared WSL has no demonstrated dedicated2vCPU/2GiB reference; #3 remains Blocked.']}
(OUT/'audit.json').write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8',newline='\n');(OUT/'phase-recomputation.json').write_text(json.dumps(phases,indent=2)+'\n',newline='\n');(OUT/'manifest-recomputation.json').write_text(json.dumps(manifests,indent=2)+'\n',newline='\n')
(OUT/'accounting-recomputation.json').write_text(json.dumps(accounting_reports,indent=2)+'\n',newline='\n')
print(json.dumps({'status':summary['status'],'counts':summary['counts'],'findings':issues[:20],'finding_count':len(issues),'output':str(OUT)}),flush=True)
