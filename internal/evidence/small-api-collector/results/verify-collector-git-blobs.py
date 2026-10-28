from pathlib import Path
import hashlib,json,subprocess
root=Path(__file__).resolve().parents[1]
relative=Path('small-api-benchmark/evidence/2026-10-28-collector')
revision='1aba2cf704d3137d1e11886fe87cc4c46b214c85'
manifest=json.loads((root/relative/'execution-retention-manifest.json').read_text())
proc=subprocess.Popen(['git','cat-file','--batch'],cwd=root,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
count=0;total=0
for item in [*manifest['entries'],{'path':'execution-retention-manifest.json','bytes':(root/relative/'execution-retention-manifest.json').stat().st_size,'sha256':hashlib.sha256((root/relative/'execution-retention-manifest.json').read_bytes()).hexdigest()}]:
    path=(relative/item['path']).as_posix()
    proc.stdin.write((revision+':'+path+'\n').encode());proc.stdin.flush()
    header=proc.stdout.readline().decode().strip().split()
    assert len(header)==3 and header[1]=='blob',(path,header)
    size=int(header[2]);assert size==item['bytes'],path
    digest=hashlib.sha256();remaining=size
    while remaining:
        block=proc.stdout.read(min(1048576,remaining));assert block,path
        digest.update(block);remaining-=len(block)
    assert proc.stdout.read(1)==b'\n',path
    assert digest.hexdigest()==item['sha256'],path
    count+=1;total+=size
proc.stdin.close();assert proc.wait(timeout=30)==0
report={'retained_samples_revision':revision,'entry_files_verified':count-1,'manifest_blob_verified':True,'all_git_blob_bytes_match_retained_hashes':True,'total_blob_bytes_including_manifest':total,'boundary':'Every retained source/result blob compared against its SHA256 without newline normalization; original native/worktree sources remain. No private fixtures or compiled artifacts included.'}
target=root.parent/'Cehpalon-Engine-Docs/internal/evidence/small-api-collector/results'
(target/'git-blob-readback.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
