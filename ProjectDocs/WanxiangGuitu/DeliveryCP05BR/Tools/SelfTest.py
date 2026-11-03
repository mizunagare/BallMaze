from pathlib import Path
from copy import deepcopy
import json,sys
from Analyse import analyse
source=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=False);base=json.loads((source/'br-probe.json').read_text(encoding='utf-8-sig'));cases=[];stress='--stress' in sys.argv
def check(name,mutation,expected,field='measurementValidity'):
 folder=out/name;folder.mkdir();r=deepcopy(base);mutation(r);(folder/'br-probe.json').write_text(json.dumps(r),encoding='utf8');actual=analyse(folder,stress=stress);(folder/'analysis.json').write_text(json.dumps(actual,indent=2),encoding='utf8');cases.append({'name':name,'scope':'synthetic mutation of a copy; never real runtime result','field':field,'expected':expected,'actual':actual[field],'status':'PASS' if actual[field]==expected else 'FAIL'})
check('valid-control',lambda r:None,'PASS')
check('missing-positive',lambda r:r['samples'].__delitem__(next(i for i,x in enumerate(r['samples']) if x['kind']=='positive-65536')),'FAIL')
check('zero-positive',lambda r:[x.update(bytes=0,events=0) for x in r['samples'] if x['kind']=='positive-65536'],'FAIL')
check('nonzero-zero',lambda r:[x.update(bytes=4) for x in r['samples'] if x['kind']=='zero'],'FAIL')
check('duplicate-marker',lambda r:r['samples'][1].update(marker=r['samples'][0]['marker']),'FAIL')
check('missing-phase',lambda r:r['phases'].pop(),'FAIL')
check('missing-real-method',lambda r:r['samples'].__delitem__(next(i for i,x in enumerate(r['samples']) if x['kind']=='target-choose')),'FAIL')
check('invalid-native-event',lambda r:r['samples'][-1].update(invalid=1),'FAIL')
check('negative-time',lambda r:r['samples'][-1].update(cpuNs=-1),'FAIL')
check('init-unavailable',lambda r:r.update(nativeInit=-1),'FAIL')
if stress:
 check('short-stress',lambda r:r['phases'][-1].update(duration=3),'FAIL')
 check('actual-two-moving-control',lambda r:None,'PASS','workloadCoverage')
 def vertical_only(r):
  p=next(p for p in r['phases'] if p['name']=='two-moving');p['enemyAfter']=[dict(a,y=a['y']+.1) for a in p['enemyBefore']]
 check('vertical-not-horizontal-movement',vertical_only,'FAIL','workloadCoverage')
(out/'selftests.json').write_text(json.dumps(cases,indent=2),encoding='utf8');print(json.dumps(cases,indent=2));sys.exit(any(c['status']!='PASS' for c in cases))
