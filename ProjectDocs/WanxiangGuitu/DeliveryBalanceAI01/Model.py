import pathlib,json,csv,math,sys
root=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);d=json.loads((root/'Before02/runtime-baseline.json').read_text(encoding='utf-8-sig'));en=d['enemies'];first=d['first'];growth=d['growth'];normal=next(e['xp'] for e in en if e['type']=='Melee');full=sum(e['xp'] for e in en);ordinary=sum(e['xp'] for e in en if not e['boss']);boss=sum(e['xp'] for e in en if e['boss']);rows=[];summary=[]
def threshold(l,c):
 n=l-1
 return first+growth*n if c=='legacy' else first+growth*n+math.ceil(growth*n*n/4) if c=='conservative' else first+15+growth*n+growth*n*n//2 if c=='moderate' else first+30+round(growth*1.5)*n+round(growth*.7)*n*n
for curve in ['legacy','conservative','moderate','slow']:
 cumulative=0
 for level in range(1,31):
  req=threshold(level,curve);rows.append(dict(curve=curve,level=level,required=req,cumulativeToEnter=cumulative,normalKillsEstimate=math.ceil(cumulative/normal),normalKillsToAdvanceEstimate=math.ceil(req/normal),normalXp=normal,forestNonBossXp=ordinary,fullForestXp=full,twoBossShare=boss/full));cumulative+=req
 def at(xp):
  level=1
  while xp>=threshold(level,curve):xp-=threshold(level,curve);level+=1
  return dict(level=level,remainder=xp)
 summary.append(dict(curve=curve,singleOrdinary25=at(25),twoOrdinary50=at(50),ordinaryEncounter115=at(115),nonBossForest=at(ordinary),fullForest=at(full),firstBoss150=at(150)))
with (out/'PROGRESSION_CURVES.csv').open('w',newline='',encoding='utf-8') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
(out/'curve-model.json').write_text(json.dumps(dict(scope='Model using measured runtime XP/config; not measured run duration or balance proof',first=first,growth=growth,fullForestXP=full,nonBossXP=ordinary,bossXP=boss,curves=summary,selected='moderate',reason='Keep a normal 25XP kill below first threshold, retain early progression in two ordinary kills, reduce full-clear model L11 to L7; no HP/damage/reward buffs'),ensure_ascii=False,indent=2),encoding='utf-8')
print(full,ordinary,boss,summary)
