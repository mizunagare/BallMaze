import json
from pathlib import Path

ev=Path('ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation/UX05-IMGUI-R2/EVIDENCE')
def diff(a,b,p=''):
    if type(a) != type(b): return [p]
    if isinstance(a,dict):
        return sum([diff(a.get(k),b.get(k),p+'/'+k) for k in sorted(a.keys()|b.keys())],[])
    if a != b: return [p]
    return []
for name in ['MIXED-A05','EMPTY-A01','UNKNOWN-A02']:
    folder=ev/name/'WanxiangGuitu/ForestRuins-v10'
    before=json.loads((folder/'save.json.bak').read_text('utf-8-sig'))
    after=json.loads((folder/'save.json').read_text('utf-8-sig'))
    print(name, 'envelope',diff(before,after))
    old=json.loads(before['payload']);new=json.loads(after['payload'])
    print(name,'payload',diff(old,new))
