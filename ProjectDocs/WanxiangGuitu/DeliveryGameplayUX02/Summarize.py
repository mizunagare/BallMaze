import json,csv,sys
from pathlib import Path
root=Path(sys.argv[1]);out=Path(sys.argv[2]);sets=[];runs=[];builds=[];timelines=[]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
for p in sorted(root.glob('*/presentation.json')):
 j=read(p);sets.append(dict(directory=p.parent.name,layer=j['layer'],PASS=sum(x['status']=='PASS' for x in j['rows']),FAIL=sum(x['status']=='FAIL' for x in j['rows']),total=len(j['rows']),failures=[x for x in j['rows'] if x['status']=='FAIL']))
for p in sorted(root.glob('*/results.json')):
 j=read(p)
 for row in j if isinstance(j,list) else [j]:runs.append(dict(directory=p.parent.name,**row))
for p in sorted(root.glob('*/build-report-messages.json')):
 j=read(p);builds.append(dict(directory=p.parent.name,**{k:v for k,v in j.items() if k!='messages'}))
for p in sorted(root.glob('*/attack-timeline.csv')):
 rows=list(csv.reader(p.open(encoding='utf-8-sig')));groups={}
 for r in rows:groups.setdefault((int(r[0]),int(r[1]),int(r[2])),[]).append(r)
 events=[json.loads(l) for l in (p.parent/'damage-events.jsonl').read_text(encoding='utf-8-sig').splitlines()] if (p.parent/'damage-events.jsonl').exists() else []
 for (w,skill,attack),samples in groups.items():
  hits=[(i+1,e) for i,e in enumerate(events) if e['entity']==f'timeline-{w}-{skill}'];release=max(int(r[5]) for r in samples)
  timelines.append(dict(attempt=p.parent.name,acceptedAction=attack>0,weapon=w,skill=skill,attack=attack,startFrame=int(samples[0][3]),startTime=float(samples[0][4]),releaseFrame=release,firstDamageFrame=hits[0][1]['frame'] if hits else None,damageEvents=len(hits),actualDamage=sum(e['applied'] for _,e in hits),damageEventLines=[i for i,_ in hits]))
identities=[]
for p in sorted(root.glob('*/Game/ForestRuins/save.json')):
 j=read(p);d=json.loads(j['payload']) if isinstance(j.get('payload'),str) else j.get('payload',{});run=d.get('activeRun') or {};profile=d.get('profile') or {}
 identities.append(dict(attempt=p.parents[2].name,path=p.relative_to(root).as_posix(),version=j.get('version'),revision=j.get('revision'),profile=profile.get('profileId'),run=run.get('runId'),seed=run.get('seed'),generationVersion=run.get('generationVersion'),contentRevision=run.get('contentRevision'),regionInstanceId=run.get('regionInstanceId')))
summary=dict(note='Assertion/process units separate. All failures retained. Damage event IDs are file path + 1-based JSONL line; attack association is controlled fixture context, not an invented engine attacker ID.',assertionSets=sets,runs=runs,builds=builds,identities=identities,NOT_RUN=['native keyboard/mouse U16','human animation/audio/readability/comfort/fun/hit feel','normal AI adventure in this batch','full performance and logging overhead benchmark','all missing shader/audio device combinations','exhaustive all scene/modal cancellation combinations'],UNRESOLVED=['historical D3D12 UNKNOWN/C15/cyan/Search/JobTempAlloc','near lateral-camera Staff safe-direction miss remains unchanged, needs separate gameplay/aim evaluation'])
(out/'SUMMARY.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
for name,values in [('RUNS.csv',runs),('TIMELINES.csv',timelines)]:
 with (out/name).open('w',newline='',encoding='utf-8-sig') as f:
  keys=list(values[0]) if name=='TIMELINES.csv' and values else ['directory','name','scope','status','startUtc','endUtc','exitCode','timedOut','reason'];w=csv.DictWriter(f,keys,extrasaction='ignore');w.writeheader();w.writerows(values)
print(len(sets),'assertion sets;',len(runs),'process/status rows;',len(timelines),'grouped attempt timelines (including invalid fixtures)' )
