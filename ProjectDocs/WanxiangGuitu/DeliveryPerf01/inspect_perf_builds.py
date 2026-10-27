"""Read-only byte-aligned module scan; pair with existing PLAYER02 PE metadata proof."""
import argparse,hashlib,json
from pathlib import Path

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 builds={'Release':a.root/'R/20261027-224721-Short-9b5789bc','PerfV3':a.root/'Runtime/T/20261027-230850-Short-134355e0','PerfV4':a.root/'Runtime/T/20261027-235711-Short-c34fdb0b'}
 tokens=['PlayerAcceptanceDriver','-p02-mode','PerfSampler','perf-config.json','PERF01 temporary sampler']
 results=[]
 for name,b in builds.items():
  modules=[]
  for f in sorted((b/'Results/Release/WanxiangGuitu_Data/Managed').glob('*.dll')):
   raw=f.read_bytes();hits=[x for x in tokens if x.encode() in raw or x.encode('utf-16-le') in raw]
   modules.append(dict(module=f.name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),hits=hits))
  matches=[m for m in modules if m['hits']]
  passed=bool(modules) and (not matches if name=='Release' else len(matches)==1 and matches[0]['module']=='Assembly-CSharp.dll' and matches[0]['hits']==tokens)
  results.append(dict(name=name,path=str(b),status='PASS' if passed else 'FAIL',modules=modules))
 a.output.write_text(json.dumps(dict(toolSha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),scope='All managed modules, UTF8/UTF16LE at arbitrary byte alignment; combine with PE references/type and clone source proof. Not native input or gameplay proof',builds=results),indent=2),encoding='utf-8')
 print([(r['name'],r['status'],len(r['modules'])) for r in results])
 if any(r['status']!='PASS' for r in results):raise SystemExit(1)
if __name__=='__main__':main()
