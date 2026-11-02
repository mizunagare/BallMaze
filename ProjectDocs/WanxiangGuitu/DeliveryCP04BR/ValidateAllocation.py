"""Offline validation of exported scoped allocation metadata, never substitutes for profiling."""
import json,copy,unittest
from pathlib import Path

def validate(j):
 try:
  scopes=j['scopes'];raw=j['raw'];names=[s['marker'] for s in scopes];rn=[s['marker'] for s in raw]
  if j['errors'] or len(scopes)!=152 or len(raw)!=152 or len(set(names))!=152 or len(set(rn))!=152 or set(names)!=set(rn):return False
  by={x['marker']:x for x in raw};cal={k:[] for k in ['zero','positive-65536','release-reference']}
  for s in scopes:
   a=by[s['marker']]['allocations']
   if any(type(x['bytes']) is not int or x['bytes']<0 for x in a):return False
   if s['kind'] in cal:cal[s['kind']].append(sum(x['bytes'] for x in a))
  return cal['zero']==[0]*8 and cal['release-reference']==[0]*8 and len(cal['positive-65536'])==8 and all(x>=65536 for x in cal['positive-65536'])
 except (KeyError,TypeError):return False

if __name__=='__main__':
 import argparse
 a=argparse.ArgumentParser();a.add_argument('fixed',type=Path);a.add_argument('baseline',type=Path);a.add_argument('output',type=Path);v=a.parse_args();f=json.loads(v.fixed.read_text(encoding='utf8'));b=json.loads(v.baseline.read_text(encoding='utf8'));checks=[]
 def check(name,j,expected):
  actual=validate(j);checks.append({'name':name,'expected':expected,'actual':actual,'status':'PASS' if actual==expected else 'FAIL'})
 check('fixed-real',f,True);check('baseline-real',b,True)
 x=copy.deepcopy(f);x['raw']=[];check('missing-raw',x,False)
 x=copy.deepcopy(f);x['raw'][1]['marker']=x['raw'][0]['marker'];check('duplicate-marker',x,False)
 x=copy.deepcopy(f);x['errors']=['metadata failed'];check('metadata-error',x,False)
 x=copy.deepcopy(f);x['raw'][1]['allocations']=[];check('zero-positive-control',x,False)
 x=copy.deepcopy(f);x['raw'][0]['allocations']=[{'bytes':32}];check('nonzero-empty-control',x,False)
 x=copy.deepcopy(f);x['raw'][2]['allocations']=[{'bytes':-65536}];check('negative-allocation-size',x,False)
 x=copy.deepcopy(f);x['raw'][1]['allocations'][0]['bytes']='65568';check('invalid-metadata-type',x,False)
 x=copy.deepcopy(f);del x['scopes'];check('missing-scopes',x,False)
 v.output.write_text(json.dumps({'scope':'Offline validation of authentic profiler export; not a new Unity run','rows':checks},indent=2));print(len(checks),'checks');raise SystemExit(1 if any(x['status']=='FAIL' for x in checks) else 0)
