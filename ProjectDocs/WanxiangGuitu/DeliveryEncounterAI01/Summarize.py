"""Read-only conditional encounter analysis. No estimated currency or imputed kills."""
import json,csv,sys,statistics,math
from pathlib import Path
root=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def quant(v):
 v=sorted(v)
 if not v:return {'n':0,'min':None,'p25':None,'median':None,'p75':None,'p95':None,'max':None}
 def q(p):
  a=(len(v)-1)*p;i=int(a);return v[i]+(v[min(i+1,len(v)-1)]-v[i])*(a-i)
 return dict(n=len(v),min=v[0],p25=q(.25),median=q(.5),p75=q(.75),p95=q(.95),max=v[-1])
def dump(name,data): (out/name).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
def csvout(name,rows):
 if not rows:return
 with (out/name).open('w',encoding='utf-8-sig',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(dict.fromkeys(k for r in rows for k in r)));w.writeheader();w.writerows(rows)
allrows=[];events=[];pairs={};processes=[]
for phase,folders in [('Before',['FinalBeforeMatrix']),('After',['FinalMatrix'])]:
 selected={}
 for folder in folders:
  p=root/folder/'process-results.json'
  if not p.exists():continue
  values=read(p);values=values if isinstance(values,list) else [values]
  for r in values:
   processes.append(dict(phase=phase,attempt=folder,**r))
   if r['status']=='PASS' and r['exitCode']==0:selected[(r['seed'],r['rep'])]=root/folder/f"S{r['seed']}-R{r['rep']}"
 for _,case in sorted(selected.items()):
  report=read(case/'matrix.json')
  for r in report['rows']:
   r=dict(r,phase=phase,evidence=str(case.relative_to(root)),status='PASS' if r['xpMatchesWhenSurviving'] else 'FAIL')
   raw=[json.loads(s) for s in (case/'Samples'/r['sample']/'events.jsonl').read_text(encoding='utf-8-sig').splitlines() if s]
   starts={e['attack']:e for e in raw if e['kind']=='telegraph'};releases=[e for e in raw if e['kind']=='release'];hits=[e for e in raw if e['kind']=='contact' and e['before']>e['after']]
   leads=[e['time']-starts[e['attack']]['time'] for e in releases if e['attack'] in starts]
   r['firstWarning']=min((e['time']-r['startedTime'] for e in starts.values()),default='');r['firstRelease']=min((e['time']-r['startedTime'] for e in releases),default='');r['firstDamage']=min((e['time']-r['startedTime'] for e in hits),default='');r['unreleasedWindupsAtCutoff']=len(starts)-len(releases)
   r['warningLeadMin']=min(leads) if leads else '';r['warningLeadMedian']=statistics.median(leads) if leads else ''
   # Within-case gaps only. Never join the end of one condition to another.
   for label,seq in [('release',releases),('contact',hits)]:
    gaps=[b['time']-a['time'] for a,b in zip(seq,seq[1:])]
    r[label+'GapMin']=min(gaps) if gaps else '';r[label+'GapMedian']=statistics.median(gaps) if gaps else ''
   cross=[b['time']-a['time'] for a,b in zip(hits,hits[1:]) if a['attack']!=b['attack']];r['crossAttackContactGapMin']=min(cross) if cross else '';r['sameAttackAdjacentContacts']=sum(a['attack']==b['attack'] for a,b in zip(hits,hits[1:]))
   r['dodgeBlockFractionOfContacts']=r['dodgeBlocks']/(r['damageEvents']+r['dodgeBlocks']) if r['damageEvents']+r['dodgeBlocks'] else ''
   for e in hits:
    begin=starts.get(e['attack']);events.append(dict(phase=phase,sample=r['sample'],kind=r['type'],policy=r['policy'],tier=r['tier'],entity=begin['entity'] if begin else 'UNRESOLVED',attack=e['attack'],time=e['time'],raw=e['raw'],defense=e['defense'],loss=e['before']-e['after']))
   allrows.append(r);pairs.setdefault(r['sample'],{})[phase]=r
paired=[]
for key,p in pairs.items():
 if set(p)!= {'Before','After'}:continue
 a,b=p['Before'],p['After'];checks={}
 for name in ['seed','rep','tier','type','policy','initialHP','initialDefense','initialPower','initialLevel','initialRanks','initialPositions','initialStreams']:
  checks[name]=a[name]==b[name]
 paired.append(dict(sample=key,status='PASS' if all(checks.values()) else 'FAIL',checks=checks))
stats=[]
for phase in ['Before','After']:
 for kind in sorted(set(r['type'] for r in allrows)):
  for policy in ['Stationary','Walk','CorrectDodge','WrongDodge']:
   group=[r for r in allrows if r['phase']==phase and r['type']==kind and r['policy']==policy]
   if not group:continue
   stats.append(dict(phase=phase,type=kind,policy=policy,n=len(group),deaths=sum(r['outcome']=='PLAYER_DEAD' for r in group),clears=sum(r['outcome']=='ENEMIES_DEAD' for r in group),censored=sum(r['outcome']=='WINDOW_END_CENSORED' for r in group),metrics={k:quant([r[k] for r in group if isinstance(r[k],(int,float)) and (k!='ttk' or r[k]>=0)]) for k in ['damage','heals','hitRate','dodgeBlockFractionOfContacts','ttk','elapsed','playerDistance','enemyDistance','blockedSeconds','repositionEpisodes','slotDenials','warningLeadMin','releaseGapMin','contactGapMin','crossAttackContactGapMin','sameAttackAdjacentContacts']}))
summary=dict(scope='Controlled conditional comparisons: stationary30, moving90, dodge90 (Triple early dodge); seed+rep fixed. Not balanced Cartesian experiment, not manual or final balance. -1TTK is censoring, no-value metrics remain absent. blockedSeconds is eye-LOS occlusion actor-seconds, NOT counted muzzle cancellations. Slot denials count ordinary-enemy polling attempts only, NOT distinct blocked attacks; Boss slot rejections were not instrumented.',processAttempts=processes,rows={p:sum(r['phase']==p for r in allrows) for p in ['Before','After']},pairedCount=len(paired),pairedFailures=sum(r['status']=='FAIL' for r in paired),unresolvedHitSources=sum(e['entity']=='UNRESOLVED' for e in events),groups=stats)
csvout('ENCOUNTER_MATRIX.csv',allrows);csvout('HIT_EVENTS.csv',events);dump('PAIRED_INPUTS.json',paired);dump('SUMMARY.json',summary)
print(json.dumps({k:v for k,v in summary.items() if k not in ['groups','processAttempts']},ensure_ascii=False))



