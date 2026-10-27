"""Read-only input/package/history audit; output only to an explicit owned BUILD-01 root."""
import argparse, hashlib, json, re, subprocess
from pathlib import Path
from datetime import datetime, timezone

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ext(p): return Path('\\\\?\\' + str(p.resolve()))
def record(p):
    q=ext(p)
    return dict(path=str(p),length=len(str(p)),normalExists=p.exists(),extendedExists=q.exists(),bytes=q.stat().st_size if q.exists() else None,sha256=sha(q) if q.exists() else None)
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    if not (a.out/'owner.json').exists(): raise ValueError('Owned output root required')
    dest=a.out/'ReadOnlyAudit';dest.mkdir(exist_ok=False)
    names=['Assets/CombatPrototype/ForestRuins.unity','ProjectSettings/ProjectSettings.asset','ProjectSettings/ProjectVersion.txt','Packages/manifest.json','Packages/packages-lock.json']
    data=dict(utc=datetime.now(timezone.utc).isoformat(),head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=a.source,text=True).strip(),status=subprocess.check_output(['git','status','--porcelain'],cwd=a.source,text=True),inputs=[record(a.source/n) for n in names],history=[])
    old=Path('D:/WanxiangValidationRuns/Input01/20261027-151043-585c2866')
    target='Editor/Lighting/ProbeVolume/RenderingLayerMask/TraceRenderingLayerMask.urtshader'
    for sub in ['InitialValidation/20261027-152314-acb2b3ad','FinalValidation/20261027-160155-e683b048','FinalFrozenValidation/20261027-161647-ab2a444e']:
        p=old/sub/'Project';packages=[]
        for b in (p/'Library/PackageCache').glob('com.unity.render-pipelines.*@*'):
            j=json.loads((b/'package.json').read_text(encoding='utf-8'));r=dict(folder=str(b),name=j['name'],version=j['version'],packageJson=record(b/'package.json'))
            if j['name']=='com.unity.render-pipelines.core':
                f=b/target;r.update(asset=record(f),meta=record(Path(str(f)+'.meta')),metaContent=ext(Path(str(f)+'.meta')).read_text(),importer=record(b/'Editor/UnifiedRayTracing/UnifiedRTShaderImporter.cs'))
                (dest/(sub.split('/')[0]+'-UnifiedRTShaderImporter.cs.txt')).write_bytes((b/'Editor/UnifiedRayTracing/UnifiedRTShaderImporter.cs').read_bytes())
            packages.append(r)
        log=old/sub/'Rules/Input01Rules.Run.log'
        matches=[]
        if log.exists():
            lines=log.read_text(encoding='utf-8',errors='replace').splitlines()
            for i,line in enumerate(lines):
                if line.startswith('DirectoryNotFoundException:'):
                    m=re.search(r'path "([^"]+)"',line);f=Path(m[1]) if m else None
                    matches.append(dict(line=i+1,text=line,file=record(f) if f else None,context=lines[max(0,i-1):i+16]))
        data['history'].append(dict(root=str(old/sub),projectLength=len(str(p)),packages=packages,importLog=str(log),exceptions=matches))
    (dest/'inputs-history.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    # Full source input identity, excluding no files within the three copied source trees.
    manifest=[]
    for folder in ['Assets','Packages','ProjectSettings']:
        for f in sorted((a.source/folder).rglob('*')):
            if f.is_file():manifest.append(dict(path=f.relative_to(a.source).as_posix(),bytes=f.stat().st_size,sha256=sha(f)))
    (dest/'source-files.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(dict(out=str(dest),sourceFiles=len(manifest),historicalRoots=len(data['history']))))
if __name__=='__main__':main()
