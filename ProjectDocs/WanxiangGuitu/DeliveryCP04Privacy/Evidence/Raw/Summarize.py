from pathlib import Path
import json,hashlib,re
r=Path('I:/WGCombat/CP04PRIVACY-1103-A');checks={};old=json.loads((r/'protected-reference.json').read_text(encoding='utf-8-sig'));bad=[]
for x in old:
 p=Path(x['root'])/x['path'];h=hashlib.sha256(p.read_bytes()).hexdigest() if p.exists() else None
 if h!=x['sha256']:bad.append({'path':str(p),'sha256':h})
checks['productAndUser']={'count':len(old),'changed':bad};checks['aimSHA256']=hashlib.sha256(Path('H:/unity/WanxiangGuitu-CP04/Assets/CombatPrototype/CombatAim.cs').read_bytes()).hexdigest()
network=[]
for name in ['DisabledPlayer','DisabledPlayerChildAudit']:
 j=json.loads((r/name/'endpoint-observations.json').read_text(encoding='utf-8-sig'));runtime=json.loads((r/name/'runtime-result.json').read_text(encoding='utf-8-sig'));children=[];main_tcp=0;main_udp=0;child_tcp=0;child_udp=0
 for x in j['samples']:
  main_tcp+=len(x['tcp']);main_udp+=len(x['udpLocalEndpoints'])
  for c in x.get('children',[]):
   children.append(c['name']);child_tcp+=len(c['tcp']);child_udp+=len(c['udpLocalEndpoints'])
 network.append({'run':name,'samples':len(j['samples']),'mainTcpSnapshots':main_tcp,'mainUdpLocalEndpointSnapshots':main_udp,'children':sorted(set(children)),'childTcpSnapshots':child_tcp,'childUdpLocalEndpointSnapshots':child_udp,'childObservationAvailable':name.endswith('ChildAudit'),'runtime':runtime,'privacyConclusion':'UNRESOLVED: snapshots do not prove absence of sends/payloads'})
(r/'runtime-summary.json').write_text(json.dumps(network,indent=2));(r/'protection.json').write_text(json.dumps(checks,indent=2));print(checks);print([(x['run'],x['samples'],x['children']) for x in network])
source=Path('H:/unity/WanxiangGuitu-CP04/Assets');hits=[]
for p in source.rglob('*.cs'):
 if 'Editor' in p.parts:continue
 for i,line in enumerate(p.read_text(encoding='utf-8-sig').splitlines()):
  if re.search(r'UnityWebRequest|HttpClient|WebClient|UploadHandler|UnityConsent|enableCaptureExceptions',line):hits.append({'path':str(p),'line':i+1,'text':line})
(r/'product-network-source-scan.json').write_text(json.dumps({'method':'Readonly lexical scan of product runtime .cs; absence is not proof against native/third-party paths','terms':['UnityWebRequest','HttpClient','WebClient','UploadHandler','UnityConsent','enableCaptureExceptions'],'hits':hits},indent=2))
