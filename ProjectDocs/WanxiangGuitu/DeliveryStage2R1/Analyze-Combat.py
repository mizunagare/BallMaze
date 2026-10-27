"""Read-only, finite paired combat analysis. No save access or outcome imputation."""
import argparse,csv,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
root=a.run.resolve(strict=True)
if not a.run.is_absolute() or a.output.exists() or not (root/'owner.json').exists():raise ValueError('Owned run, fresh output required')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
if read(root/'preserved-processes.json')!=[]:raise ValueError('Cannot analyze active/preserved processes')
plan=read(Path(__file__).with_name('MATRIX_INPUTS.json'));rows=[];issues=[]
for category,cases in [('main',plan['cases']),('coverage',plan['coverage'])]:
 for case in cases:
  found=list((root/'Rules').glob('*/'+case['id']+'/attempt.json'))
  if len(found)!=1:issues.append(case['id']+': expected one registered attempt');continue
  folder=found[0].parent;row=dict(category=category,input=case,attempt=read(found[0]),scope='Controlled setup then normal AI; virtual test input, not native UI or human')
  for name in ('combat-measure','setup','stage2-metrics','process-result-Normal'):
   try:row[name]=read(folder/(name+'.json'))
   except (OSError,ValueError) as e:issues.append(case['id']+': '+name+' missing/invalid');row[name]={}
  m=row['combat-measure'];s=row['setup'];metric=row['stage2-metrics'];proc=row['process-result-Normal']
  if proc.get('exitCode')!=0 or proc.get('timedOut') is not False:issues.append(case['id']+': process did not complete normally')
  if m.get('runId')!=metric.get('run') or m.get('regionId')!=metric.get('region') or m.get('targetId')!=s.get('target'):issues.append(case['id']+': observation/lifecycle identity mismatch')
  if m.get('status')=='killed':
   if not (m.get('hits',0)>0 and m.get('death',-1)>=m.get('firstDamage',0)>=0 and abs(m['ttk']-(m['death']-m['firstDamage']))<1e-8 and m.get('firstAttack',-1)>=0 and m['firstAttack']<=m['firstDamage']+1e-8):issues.append(case['id']+': invalid exact kill clock')
  elif m.get('status')!='censored':issues.append(case['id']+': unfinished observation')
  if m.get('observationError'):issues.append(case['id']+': observation fault')
  row['path']=folder.relative_to(root).as_posix();row['evidenceSha256']={n:hashlib.sha256((folder/n).read_bytes()).hexdigest() for n in ('attempt.json','combat-measure.json','setup.json','stage2-metrics.json') if (folder/n).exists()};rows.append(row)
main=[r for r in rows if r['category']=='main'];coverage=[r for r in rows if r['category']=='coverage'];blocks=[]
if len(main)!=18 or len(coverage)!=8:issues.append('registered finite matrix not fully observed')
if len({r['combat-measure'].get('runId') for r in rows})!=len(rows):issues.append('Run identity reused')
for block in sorted({r['input']['blockId'] for r in main}):
 group=[r for r in main if r['input']['blockId']==block];by={r['input']['build']:r for r in group}
 same=[(r['setup'].get('target'),r['setup'].get('targetMaxHealth'),r['setup'].get('enemyDamage'),r['setup'].get('actualSeed'),r['setup'].get('revision'),r['setup'].get('fallback')) for r in group]
 if len(group)!=3 or set(by)!={'Safety','Gather','Boss'} or len(set(same))!=1:issues.append(block+': paired target/seed/layout mismatch')
 diffs=[]
 if 'Safety' in by:
  for build in ('Gather','Boss'):
   if build not in by:continue
   x,y=by[build]['combat-measure'],by['Safety']['combat-measure'];complete=x.get('status')=='killed' and y.get('status')=='killed'
   diffs.append(dict(build=build,reference='Safety',nEach=1,bothKilled=complete,ttkDifference=x['ttk']-y['ttk'] if complete else None,heroDamageDifference=x.get('heroDamage',0)-y.get('heroDamage',0),potionsDifference=x.get('potions',0)-y.get('potions',0),reason='Per-seed paired descriptive difference, not causal balance proof; censored TTK never pooled'))
 blocks.append(dict(block=block,conditions=same,caseIds=[r['input']['id'] for r in group],pairedDifferences=diffs))
result=dict(status='FAIL' if issues else 'PASS',scope='Analysis integrity, not all-win requirement or player balance acceptance',main=dict(planned=18,observed=len(main),killed=sum(r['combat-measure'].get('status')=='killed' for r in main),censored=sum(r['combat-measure'].get('status')=='censored' for r in main)),coverage=dict(planned=8,observed=len(coverage),killed=sum(r['combat-measure'].get('status')=='killed' for r in coverage),censored=sum(r['combat-measure'].get('status')=='censored' for r in coverage)),sampleLimit='n=1 per fixed condition; no significance, global build pooling or balance-complete claim',issues=issues,blocks=blocks,rows=rows,nativeUI='NOT_RUN',human='NOT_RUN',performance='NOT_RUN')
a.output.mkdir(parents=True);(a.output/'combat-summary.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
with (a.output/'combat-results.csv').open('w',newline='',encoding='utf8') as f:
 w=csv.writer(f);w.writerow(['category','case','attempt','run','target','actualSeed','fallback','status','firstAttack','firstDamage','death','TTK','preHit','encounterSeconds','hits','heroDamageUnattributed','potions','endReason'])
 for r in rows:
  m=r['combat-measure'];w.writerow([r['category'],r['input']['id'],r['attempt'].get('attemptId'),m.get('runId'),m.get('targetId'),r['setup'].get('actualSeed'),r['setup'].get('fallback')]+[m.get(k) for k in ('status','firstAttack','firstDamage','death','ttk','preHit','encounterSeconds','hits','heroDamage','potions','endReason')])
print(json.dumps({k:result[k] for k in ('status','main','coverage','issues')}));raise SystemExit(1 if issues else 0)
