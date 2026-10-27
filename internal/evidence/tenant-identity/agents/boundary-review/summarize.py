from pathlib import Path
import datetime,hashlib,json
base=Path(__file__).resolve().parent
peer=Path('D:/Cephalon/.worktrees/w1-tenancy/src/Cehpalon.Engine.Tenancy')
extra=base.parent/'boundary-extra'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
text=(extra/'Program.cs').read_text()
start=text.index('await Check("cleanup-only denial remains lifecycle failure after an authorized data read"')
end=text.index('var report=new',start)
old=text[:start]+text[end:]
old=old.replace('public bool CleanupFailure,CleanupDenial;','public bool CleanupFailure;').replace('if(business.CleanupDenial)throw new TenantAccessDeniedException();','')
p=extra/'Program-eight-cases.cs.txt'
p.write_text(old,encoding='utf-8',newline='\n')
assert sha(p)=='0036828db7c81da52ba639c0ba57e57c62908382b9b5be0bd71ada95569a6670'
result={
 'reviewer':'/root/tenant_boundary_review','observed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'scope':'Independent copied-DLL contract/adversarial QA, Windows observational only; no realIdP/provider/host/benchmark/production qualification',
 'passed':11,'total':11,
 'lease_rejections':{'count':2,'result':'results-final.json','unchanged_repro_sha256':sha(base/'Program.cs'),'retained_before_result':'results-before.json'},
 'additional_adversarial':{'count':9,'result':'../boundary-extra/results-final.json','source_sha256':sha(extra/'Program.cs')},
 'reviewed_source_sha256':{'Contracts.cs':sha(base/'Contracts-final.cs.txt'),'TenantOperationDispatcher.cs':sha(base/'Dispatcher-final.cs.txt')},
 'peer_source_stable_since_copy':{'Contracts.cs':sha(base/'Contracts-final.cs.txt')==sha(peer/'Contracts.cs'),'TenantOperationDispatcher.cs':sha(base/'Dispatcher-final.cs.txt')==sha(peer/'TenantOperationDispatcher.cs')},
 'loaded_dll_sha256':{p.name:sha(p) for p in (base/'final-libs').glob('*.dll')},
 'actual_loaded_dll_matches_peer':sha(base/'final-libs/Cehpalon.Engine.Tenancy.dll')==sha(peer/'bin/Release/net11.0/Cehpalon.Engine.Tenancy.dll'),
 'remaining_material_findings':[],
 'trust_limits':['Deepfreeze callback, sources, policy and business/provider code are trusted; this is not a sandbox','Checked context is an active in-process data-bound capability, not cryptographic or cross-process authority','Actual provider transactions/revocation/TOCTOU isolation require provider-specific proof'],
 'auxiliary_attempts':'after-build.txt preserved for accidental private-QA artifactglob; fixed only privatecsproj explicitCompile. Earlier8caseProgram reconstructed by reversing append-only ninthcase, matches original recorded sourcehash.'
}
(base/'review-final.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
print(json.dumps(result,indent=2))
