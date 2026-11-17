import json,struct,itertools,re,hashlib
from pathlib import Path
O=Path(__file__).resolve().parent
f=lambda x:struct.unpack('<f',struct.pack('<f',x))[0]
bits=lambda x:struct.unpack('<I',struct.pack('<f',x))[0]
qnames=['White','Green','Purple','Gold','Red']
def field(path,key):return float(re.search(r'^  '+key+r': ([-.0-9]+)$',Path(path).read_text(),re.M)[1])
powers=[field('Assets/CombatPrototype/Resources/QualityData/'+q+'.asset','power') for q in qnames]
items=[]
for t in ['sword','arms','accessory']:
 p='Assets/CombatPrototype/Resources/ItemData/'+t+'.asset'
 for q,power in enumerate(powers):items.append(dict(type=t,quality=qnames[q],power=power,attack=f(f(power)*f(field(p,'attackFactor'))),width=int(field(p,'width')),height=int(field(p,'height'))))
results=[];tested=0
for a,b,c in itertools.product(items,repeat=3):
 # Main weapon first; two distinct-ID board items. This is ordered Active list, not unordered set.
 if a['type']!='sword':continue
 tested+=1;v=[a['attack'],b['attack'],c['attack']]
 double=f(sum(v));seq=f(f(f(0)+v[0])+v[1]);seq=f(seq+v[2])
 if bits(double)==bits(seq):continue
 # Side by side, unrotated, within standard 8x6 board. Main stays InBag (not on board).
 fits=b['width']+c['width']<=8 and max(b['height'],c['height'])<=6
 if not fits:continue
 results.append(dict(items=[dict(a,id='round-main',role='Main',board=False,worn=False,overflow=False),dict(b,id='round-board-1',role='Board',board=True,worn=False,overflow=False,x=0,y=0),dict(c,id='round-board-2',role='Board',board=True,worn=False,overflow=False,x=b['width'],y=0)],float64_sum_then_float32=double,float64_sum_bits=bits(double),sequential_float32_sum=seq,sequential_bits=bits(seq),ulp_difference=abs(bits(double)-bits(seq)),difference=seq-double,AP_double=f(f(25)+double),AP_sequential=f(f(25)+seq),board_fits=fits))
assert results
r=dict(scope='pure Python static boundary, no Player',tested_ordered_3Active_combinations=tested,layout_valid_differences=len(results),assumptions=['Old Enumerable.Sum(float) uses float64 accumulator and casts result to float32. Mono System.Core implementation has NOT been confirmed from the historical Player binary.','Product B2AttackModel explicit float sum += item.Attack is modeled as float32 rounding after each addition. Runtime/JIT execution has not been measured.','All IDs distinct. Order is main then two board items. DataRevision=1 frozen stats from existing assets. Standard rig 8x6 with no blocked cells and zero attack bonus.','This is an uncovered precision/accumulation-order risk, NOT evidence of coefficient or stacking-rule changes, and NOT proof of actual historical runtime mismatch.'],examples=results[:10])
(O/'ROUNDING_BOUNDARY.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(dict(tested=tested,differences=len(results),first=results[0]),ensure_ascii=False))
