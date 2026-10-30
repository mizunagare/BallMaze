from pathlib import Path
import json,csv,sys,collections
r=Path(sys.argv[1]);d=Path(sys.argv[2]);sets=[];runs=[];builds=[];identities=[]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
for p in sorted(r.glob('*/presentation.json')):
 j=read(p);counts=collections.Counter(x['status'] for x in j['rows']);sets.append(dict(attempt=p.parent.name,layer=j['layer'],counts=dict(counts),failures=[x for x in j['rows'] if x['status']=='FAIL'],open=[x for x in j['rows'] if x['status']=='UNRESOLVED']))
for p in sorted(r.glob('*/results.json')):
 j=read(p)
 for x in j if isinstance(j,list) else [j]:runs.append(dict(attempt=p.parent.name,**x))
for p in sorted(r.glob('*/build-report-messages.json')):
 j=read(p);builds.append(dict(attempt=p.parent.name,**{k:v for k,v in j.items() if k!='messages'}))
for p in sorted(list(r.glob('*/Game/ForestRuins/save.json'))+list(r.glob('*/WanxiangGuitu/ForestRuins/save.json'))):
 j=read(p);v=json.loads(j['payload']);a=v.get('activeRun') or {};f=v.get('profile') or {};identities.append(dict(attempt=p.parents[2].name,path=p.relative_to(r).as_posix(),profile=f.get('profileId'),run=a.get('runId'),seed=a.get('seed'),generationVersion=a.get('generationVersion'),contentRevision=a.get('contentRevision'),gear=[{k:x.get(k) for k in ('id','type','quality')} for x in v.get('gear',[])]))
summary=dict(note='Separate units; before/cue failures and intermediate builds retained. Health Damage.attack is LastAttackId context, not engine attacker attribution; projectile spawn carries true AttackId/ShotIndex. Fixed-rate controlled fixtures are not native/AI/human/performance tests.',assertionSets=sets,runs=runs,builds=builds,identities=identities,NOT_RUN=['native U16/physical input','human animation/readability/audio/comfort/fun/final feel','normal AI adventure and reward/settlement loop in this batch','full Profiler GPU/CPU/GC overhead','all quality/skill-rank combinations','dedicated spear/staff skill clips and independent Bow aiming clip activation'],UNRESOLVED=['retained near lateral-camera Staff basic and skill misses','historical D3D12 UNKNOWN/C15/cyan/Search/JobTempAlloc'])
(d/'SUMMARY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
with (d/'RUNS.csv').open('w',newline='',encoding='utf-8-sig') as f:
 keys=['attempt','name','scope','status','startUtc','endUtc','exitCode','timedOut','reason'];w=csv.DictWriter(f,keys,extrasaction='ignore');w.writeheader();w.writerows(runs)
print('sets',len(sets),'process/status rows',len(runs),'build variants',len(builds))
