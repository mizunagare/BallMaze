"""Pure formula model; not Unity damage/AI evidence. Python standard library only."""
import csv,math,json
from pathlib import Path
out=Path(__file__).parent
attacks={'Ranged':9,'Melee':12,'Elite':20,'RootSlam':23,'AntlerCharge':27,'SeedVolley':12,'WaterFan':11,'TidalMark':24,'ShoreBite':21}
D=[0,2,5,10,15,19.2,25,30]
models=[('Old',0,0)]+[('A',x,0)for x in [.4,.5,.6]]+[('B',k,0)for k in [5,10,20,30]]+[('C',k,cap)for k in [10,20,30]for cap in [.6,.75,.8]]
def damage(kind,k,cap,raw,d):
 if not math.isfinite(raw)or raw<=0:return 0
 d=max(0,d)if math.isfinite(d)else 0
 if kind=='Old':v=raw-d
 elif kind=='A':v=raw-min(d,raw*k)
 elif kind=='B':v=raw-d*k/(d+k)
 else:v=raw*(1-min(cap,d/(d+k)))
 return max(1,v)
rows=[];summary=[]
for kind,k,cap in models:
 vals=[]
 for name,raw in attacks.items():
  previous=float('inf')
  for d in D:
   v=damage(kind,k,cap,raw,d);assert v<=previous+1e-12;previous=v
   row=dict(model=kind,K_or_cap=k,maxReduction=cap,attack=name,raw=raw,defense=d,final=v,reduction=1-v/raw,floor=v==1,hits100=math.ceil(100/v),hits100plus50=math.ceil(150/v),note='theoretical unhealed contacts, no timing/dodge/overkill claim');rows.append(row);vals.append(row)
 summary.append(dict(model=kind,K_or_cap=k,maxReduction=cap,floorRate=sum(x['floor']for x in vals)/len(vals),high9=damage(kind,k,cap,9,19.2),high12=damage(kind,k,cap,12,19.2),high27=damage(kind,k,cap,27,19.2)))
with(out/'ARMOR_FORMULA_COMPARISON.csv').open('w',newline='',encoding='utf-8-sig')as f:
 w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
with(out/'DAMAGE_CURVE.csv').open('w',newline='',encoding='utf-8-sig')as f:
 selected=[r for r in rows if r['model']=='C'and r['K_or_cap']==20 and r['maxReduction']==.75];w=csv.DictWriter(f,fieldnames=selected[0]);w.writeheader();w.writerows(selected)
(out/'formula-summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(len(rows),'model rows; selected C K20 cap.75; all monotonic; not actual combat')
