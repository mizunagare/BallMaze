import argparse,csv,json,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',required=True);a=p.parse_args();root=Path(a.root);out=root/'Comparison';out.mkdir(exist_ok=False)
read=lambda folder,name:list(csv.DictReader((root/folder/name).open()))
key=lambda x:tuple(x[c] for c in ['weapon','action','body','distance','angle','height','duplicate','wall'])
b={key(x):x for x in read('Before','matrix.csv')};n={key(x):x for x in read('After','matrix.csv')};rows=[]
def check(ok,name,detail=''):rows.append({'name':name,'status':'PASS' if ok else 'FAIL','detail':detail})
check(len(b)==len(n)==684 and b.keys()==n.keys(),'identical 684 case keys')
unchanged=[k for k in b if not(k[0]=='1' and k[1]=='basic')]
check(all(b[k]['hit']==n[k]['hit'] and abs(float(b[k]['applied'])-float(n[k]['applied']))<.02 for k in unchanged),'all skills and other basics preserve hit and damage',str(len(unchanged)))
spear=[k for k in b if k[0]=='1' and k[1]=='basic'];check(all(not(n[k]['hit']=='1' and b[k]['hit']=='0') for k in spear),'thrust does not gain hits outside former volume')
check(all(abs(float(n[k]['applied'])-float(b[k]['applied'])*1.25)<.02 for k in spear if n[k]['hit']=='1'),'common thrust hits gain only measured 1.25 power')
def row(w,d,angle):return n[(str(w),'basic','normal',str(d),str(angle),'0','0','0')]
check(row(0,3,0)['hit']=='0' and row(1,3,0)['hit']=='1','far forward thrust reaches beyond sword')
check(row(0,0.75,70)['hit']=='1' and row(1,0.75,70)['hit']=='0','close sword sweep covers lateral miss of thrust')
for w in range(4):
 x=[v for k,v in n.items() if k[0]==str(w) and v['duplicate']=='1'][0]
 check(x['damageEvents']=='1' and x['hit']=='1','contained duplicate collider one basic hit '+str(w))
 x=[v for k,v in n.items() if k[0]==str(w) and v['wall']=='1'][0]
 check(x['hit']=='0','solid wall blocks basic '+str(w))
for body in ['normal','elite','boss']:
 def edge(folder,w):return max(float(x['distance']) for x in read(folder,'matrix.csv') if x['weapon']==str(w) and x['body']==body and x['hit']=='1')
 old=edge('BeforeBoundary',0);sword=edge('AfterBoundary',0);spear=edge('AfterBoundary',1)
 check(old==sword and spear>sword,'10cm actual body edge '+body,f'sword={sword},spear={spear},ratio={spear/sword}')
contract=read('Contracts','contracts.csv');check(len(contract)==15 and all(x['status']=='PASS' for x in contract),'15 actual quality/multi-target damage cases')
for phase in ['Before','After']:
 duels=read(phase,'duels.csv');check(len(duels)==24 and all(x['terminal']=='ENEMY_DEAD' for x in duels),'24 enabled-AI fixed-arena kills '+phase)
(out/'comparison.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
with (out/'comparison.csv').open('w',newline='',encoding='utf-8') as f:
 writer=csv.DictWriter(f,fieldnames=['name','status','detail']);writer.writeheader();writer.writerows(rows)
print({state:sum(x['status']==state for x in rows) for state in ['PASS','FAIL']});sys.exit(any(x['status']=='FAIL' for x in rows))
