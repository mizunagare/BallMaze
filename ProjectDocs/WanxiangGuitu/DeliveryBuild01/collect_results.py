"""Publish diagnostic receipts, never Players/caches/saves; all historical roots read-only."""
import argparse,csv,hashlib,json,re,shutil
from pathlib import Path
from collections import Counter
from datetime import datetime,timezone

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path('D:/WGB01'));ap.add_argument('--evidence',type=Path,required=True);a=ap.parse_args()
 a.evidence.mkdir(parents=True,exist_ok=True);runs=[];warning_sets={}
 for root in sorted(a.root.iterdir()):
  if not root.is_dir() or not (root/'owner.json').exists():continue
  owner=read(root/'owner.json');dest=a.evidence/'Runs'/root.name;dest.mkdir(parents=True,exist_ok=True)
  if not owner['kind'].startswith('BUILD-01'):raise ValueError('Unknown owner')
  for f in root.iterdir():
   if f.is_file():shutil.copy2(f,dest/f.name)
   elif f.name in ['ReadOnlyAudit','ExecutedTools']:shutil.copytree(f,dest/f.name,dirs_exist_ok=True)
  row=dict(run=root.name,root=str(root),case=owner.get('case','Preflight'),project=owner.get('project'),build=None)
  data=root/'Results'
  if data.exists():
   dd=dest/'Results';dd.mkdir(exist_ok=True)
   for f in data.iterdir():
    if f.is_file() and f.name not in ['s2r1-inputs.json','method-plan.json']:shutil.copy2(f,dd/f.name)
   # Build summary only, never full executable output or synthetic saves.
   if (data/'Release/BuildSummary.txt').exists():shutil.copy2(data/'Release/BuildSummary.txt',dd/'BuildSummary.txt')
   report=data/'build-report-messages.json'
   if report.exists():
    r=read(report);asset=read(data/'asset-before.json');types=Counter(m['type'] for m in r['messages']);errors=[m for m in r['messages'] if m['type']=='Error']
    warnings=[m['text'] for m in r['messages'] if m['type']=='Warning'];classes=Counter()
    for w in warnings:
     cs=re.search(r'warning (CS\d+)',w)
     classes[cs[1] if cs else 'scene serialized version' if 'below the supported minimum' in w else 'other']+=1
    warning_sets[root.name]=warnings
    hashes={}
    for name in ['WanxiangGuitu.exe','UnityPlayer.dll','WanxiangGuitu_Data/Managed/Assembly-CSharp.dll']:
     f=data/'Release'/name;hashes[name]=dict(bytes=f.stat().st_size,sha256=sha(f))
    dll=(data/'Release/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll').read_bytes()
    tokens=['Build01Audit','Input01Rules','Input01Play','WGA1NormalResume']
    excluded={t:t.encode() not in dll for t in tokens}
    row['build']=dict(result=r['result'],errors=r['errors'],warnings=r['warnings'],messageCounts=dict(types),warningCategories=dict(classes),errorsDetail=errors,seconds=r['seconds'],bytes=r['bytes'],asset=asset,hashes=hashes,editorClassNamesAbsent=excluded,quality='PASS' if r['result']=='Succeeded' and r['errors']==0 else 'FAIL',expectedTargetReproduction=asset['pathLength']==260 and len(errors)==2 and all('TraceRenderingLayerMask.urtshader' in m['text'] for m in errors))
    # Correlate real import failure with file/read/type evidence; log line order is not a timestamp.
    lines=(data/'Build01Audit.Run.log').read_text(encoding='utf-8',errors='replace').splitlines();exceptions=[]
    for i,line in enumerate(lines):
     if line.startswith('DirectoryNotFoundException:'):
      exceptions.append(dict(line=i+1,text=line,context=lines[max(0,i-1):i+16]))
    write(dd/'import-exception-context.json',exceptions)
    row['build']['packageDirectoryNotFoundCount']=len(exceptions)
    write(dd/'product-hashes.json',hashes)
  runs.append(row)
 builds=[r for r in runs if r['build']]
 summary=dict(utc=datetime.now(timezone.utc).isoformat(),scope='Controlled Editor imports and non-development build. No Player/native/human test implied.',runs=runs,buildCounts=dict(PASS=sum(r['build']['quality']=='PASS' for r in builds),expectedTargetFAIL=sum(r['build']['expectedTargetReproduction'] for r in builds),unexpectedBuildFAIL=sum(r['build']['quality']=='FAIL' and not r['build']['expectedTargetReproduction'] for r in builds)),warningSetsEqual=len({tuple(v) for v in warning_sets.values()})<=1)
 write(a.evidence/'RESULTS.json',summary)
 with (a.evidence/'RESULTS.csv').open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=['run','case','buildResult','errors','warnings','logs','quality','expectedTargetReproduction','pathLength']);w.writeheader()
  for r in runs:
   b=r['build'] or {};w.writerow(dict(run=r['run'],case=r['case'],buildResult=b.get('result','NOT_RUN'),errors=b.get('errors'),warnings=b.get('warnings'),logs=b.get('messageCounts',{}).get('Log'),quality=b.get('quality','NOT_RUN'),expectedTargetReproduction=b.get('expectedTargetReproduction',False),pathLength=b.get('asset',{}).get('pathLength')))
 print(json.dumps(summary['buildCounts']))
if __name__=='__main__':main()
