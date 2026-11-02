"""Fail-closed validation of BR2 allocation evidence. Does not execute Unity or replace calibration."""
import json,copy
from pathlib import Path

def editor(j):
 try:
  scopes=j['scopes'];raw=j['raw'];a={x['marker']:x for x in raw}
  if len(scopes)!=232 or len(raw)!=232 or len(a)!=232 or len({x['marker'] for x in scopes})!=232 or j['errors']:return False
  values={k:[] for k in ['zero','positive-65536','release-reference']}
  for s in scopes:
   allocations=a[s['marker']]['allocations']
   if any(type(x['bytes']) is not int or x['bytes']<0 for x in allocations):return False
   if s['kind'] in values:values[s['kind']].append(sum(x['bytes'] for x in allocations))
  return values['zero']==[0]*8 and values['release-reference']==[0]*8 and values['positive-65536']==[65568]*8
 except (KeyError,TypeError):return False

def player(j):
 try:
  rows=j['rows']
  if j['nativeInit']!=1 or len(rows)!=152 or any(type(x['rawBytes']) is not int or x['rawBytes']<0 or x['invalid']!=0 for x in rows):return False
  for kind in ['zero','positive-65536','release-reference']:
   z=[x for x in rows if x['kind']==kind]
   if len(z)!=8:return False
   if kind=='positive-65536':
    if any(x['rawBytes']<65536 or x['events']!=1 for x in z):return False
   elif any(x['rawBytes'] or x['events'] for x in z):return False
  for d in [.35,1.5,6,20]:
   if len([x for x in rows if x['kind']=='solve' and abs(x['distance']-d)<.001])!=32:return False
  return True
 except (KeyError,TypeError):return False

if __name__=='__main__':
 r=Path('I:/WGCombat/CP04BR2-1102-A');e=json.loads((r/'Allocation6/scoped-events.json').read_text());p=json.loads((r/'MonoPlayer/mono-probe.json').read_text());p2=json.loads((r/'MonoPlayerRepeat/mono-probe.json').read_text());rows=[]
 def check(name,fn,j,expected):
  actual=fn(j);rows.append({'name':name,'expected':expected,'actual':actual,'status':'PASS' if actual==expected else 'FAIL'})
 check('actual-editor',editor,e,True);check('actual-player',player,p,True);check('actual-second-process',player,p2,True)
 x=copy.deepcopy(e);x['raw']=x['raw'][:-1];check('editor-truncated',editor,x,False)
 x=copy.deepcopy(e);x['raw'][1]['marker']=x['raw'][0]['marker'];check('editor-duplicate',editor,x,False)
 x=copy.deepcopy(e);x['raw'][1]['allocations']=[];check('editor-zero-positive',editor,x,False)
 x=copy.deepcopy(e);x['errors']=['unresolved metadata'];check('editor-error',editor,x,False)
 x=copy.deepcopy(p);x['nativeInit']=0;check('native-not-enabled',player,x,False)
 x=copy.deepcopy(p);x['rows'][1]['rawBytes']=0;check('native-positive-fails',player,x,False)
 x=copy.deepcopy(p);x['rows'][0]['rawBytes']=32;check('native-zero-fails',player,x,False)
 x=copy.deepcopy(p);x['rows'][1]['invalid']=1;check('native-bad-size-event',player,x,False)
 x=copy.deepcopy(p);x['rows'].pop();check('native-incomplete',player,x,False)
 (r/'validation-selftests.json').write_text(json.dumps({'scope':'Offline evidence validator selftests; not product or human acceptance','rows':rows},indent=2));print(len(rows),'selftests',sum(x['status']=='PASS' for x in rows),'PASS');raise SystemExit(any(x['status']=='FAIL' for x in rows))
