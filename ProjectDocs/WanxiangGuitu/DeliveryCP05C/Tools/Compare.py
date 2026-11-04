from pathlib import Path
import json,sys
root=Path(sys.argv[1]);out=Path(sys.argv[2]);rows=[]
def check(n,ok,d):rows.append(dict(name=n,status='PASS' if ok else 'FAIL',detail=d))
for layer,a,b in [('Editor','BeforeFormal2','AfterFormal'),('Player','BeforePlayerFormal','AfterPlayerFormal')]:
 if not (root/b/'formal-death.json').exists():check(layer+'-evidence',False,'Missing final evidence');continue
 ar=json.loads((root/a/'formal-rules.json').read_text());br=json.loads((root/b/'formal-rules.json').read_text());check(layer+'-480-rules',len(ar['rows'])==480 and ar==br,'All qualities, attributes, affixes and three stream states exactly paired')
 x=json.loads((root/a/'formal-death.json').read_text());y=json.loads((root/b/'formal-death.json').read_text());keys=['targetId','run','region','seed','wave','randomBefore','randomAfter','bagBefore','bagAfter','xpBefore','xpAfter','levelBefore','levelAfter'];diff=[k for k in keys if x.get(k)!=y.get(k)];check(layer+'-real-death-state',not diff,'Differing fields: '+str(diff))
 def semantic(d):return sorted([{k:v for k,v in r.items() if k!='actualId'} for r in d['drops']],key=lambda r:json.dumps(r,sort_keys=True))
 check(layer+'-actual-drops',len(x['drops'])>0 and semantic(x)==semantic(y),'Fresh ground IDs separately recorded; actual kind/amount/gear attributes identical')
 check(layer+'-ground-ID-unique',len({d['actualId'] for d in y['drops']})==len(y['drops']),'Original IDs retained in raw receipt')
 for n,d in [(a,x),(b,y)]:check(layer+'-'+n+'-global-and-bag',d['globalBefore']==d['globalAfter'] and d['bagBefore']==d['bagAfter'],'No global RNG draw or premature bag credit')
for n in ['AfterTraining4','AfterFormal','AfterPlayer','AfterPlayerFormal']:
 p=root/n/'probe.json'
 if not p.exists():check(n+'-semantic',False,'Missing');continue
 d=json.loads(p.read_text());check(n+'-semantic',len(d['rows'])>0 and not d['error'] and all(r['status']=='PASS' for r in d['rows']),str(len(d['rows']))+' actual assertions')
out.write_text(json.dumps(dict(rows=rows,status='FAIL' if any(r['status']=='FAIL' for r in rows) else 'PASS'),indent=2),encoding='utf8');print(json.dumps(rows));sys.exit(any(r['status']=='FAIL' for r in rows))
