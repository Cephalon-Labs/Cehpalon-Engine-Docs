"""Read-only independent native staging hash/link audit; no SDK execution."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,posixpath

BASE=Path('/mnt/d/Cephalon/Cehpalon-Engine-Samples/.local')
OUT=Path('/mnt/d/Cephalon/.worktrees/w2-collector-readiness/.local/precanonical-audit04')
def load(path):return json.loads(path.read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
problems=[]
def check(value,message):
 if not value:problems.append(message)
stage=load(BASE/'collector-final-app-staging.json');sdk=load(BASE/'startup-layout-sdk-staging.json');links=load(BASE/'startup-sdk-link-manifest.json');verification=load(BASE/'collector-sdk-reverification.json')
check(verification['source_manifest_sha256']==sha(BASE/'startup-layout-sdk-staging.json'),'SDK source-manifest binding differs')
check(verification['link_manifest_sha256']==sha(BASE/'startup-sdk-link-manifest.json'),'SDK link-manifest binding differs')
app_source,app_target=Path(stage['source']),Path(stage['target']);app_bytes=0
for row in stage['files']:
 a,b=app_source/row['path'],app_target/row['path'];app_bytes+=row['bytes']
 check(a.is_file() and b.is_file(), 'App source/target file missing: '+row['path'])
 if a.is_file() and b.is_file():check(a.stat().st_size==b.stat().st_size==row['bytes'] and sha(a)==sha(b)==row['sha256'],'App staged bytes differ: '+row['path'])
app_set={str(p.relative_to(app_target)) for p in app_target.rglob('*') if p.is_file()}
check(app_set=={row['path'] for row in stage['files']},'Native app has unexpected/missing files')
check(len(stage['files'])==67 and app_bytes==23281577,'Native app count/size differs')
check(stage['startup_tracing_enabled'] is False,'Startup tracing enabled in staged metadata')
check(sha(app_target/'SmallApi.Benchmark.dll')==stage['assembly_sha256'],'Staged assembly differs')
sdk_target=Path(sdk['target']);sdk_bytes=0
for row in sdk['files']:
 path=sdk_target/row['path'].replace('\\','/');sdk_bytes+=row['bytes']
 check(path.is_file() and not path.is_symlink(),'Native regular SDK file missing or link: '+row['path'])
 if path.is_file():check(path.stat().st_size==row['bytes'] and sha(path)==row['sha256'],'Native SDK file hash/size differs: '+row['path'])
for row in links:
 path=sdk_target/row['path'].replace('\\','/');check(path.is_symlink(),'Native SDK symlink missing: '+row['path'])
 if path.is_symlink():check(posixpath.normpath(os.readlink(path))==posixpath.normpath(row['target'].replace('\\','/')),'Native SDK symlink target differs: '+row['path'])
native_files,native_links=set(),set()
for path in sdk_target.rglob('*'):
 if path.is_symlink():native_links.add(path.relative_to(sdk_target).as_posix())
 elif path.is_file():native_files.add(path.relative_to(sdk_target).as_posix())
expected_files={row['path'].replace('\\','/') for row in sdk['files']};expected_links={row['path'].replace('\\','/') for row in links}
check(native_files==expected_files,'Native regular SDK file set differs')
check(native_links==expected_links,'Native SDK link set differs')
check(len(expected_files)==verification['regular_files_verified']==4178,'SDK regular-file count differs')
check(len(expected_links)==verification['symlinks_verified']==1668,'SDK symlink count differs')
result={'observed_at_utc':datetime.now(timezone.utc).isoformat(),'status':'passed' if not problems else 'findings','findings':problems,'samples_source_revision':stage['samples_source_revision'],'engine_revision':stage['engine_revision'],'app_regular_files':len(stage['files']),'app_bytes':app_bytes,'app_source_and_target_all_hashes_independently_checked':True,'app_assembly_sha256':stage['assembly_sha256'],'sdk_regular_files_independently_hashed':len(expected_files),'sdk_regular_bytes':sdk_bytes,'sdk_symlink_targets_independently_checked':len(expected_links),'sdk_target':str(sdk_target),'sdk_manifest_sha256':sha(BASE/'startup-layout-sdk-staging.json'),'sdk_link_manifest_sha256':sha(BASE/'startup-sdk-link-manifest.json'),'link_comparison':'Declared Windows separators normalized to POSIX and normpath; no link-target semantic change','scope':'Staging bytes and link identity only; no SDK process, test, request or timing. Actual loaded-module identity remains for runtime observation; no dedicated-resource/platform qualification.'}
(OUT/'staging-audit.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
