"""Strict final non-development Player title smoke; never claims native input."""
import argparse, hashlib, json, struct
from PIL import Image
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--kind',required=True);a=p.parse_args()
events=[json.loads(x) for x in (a.root/'entry-audit.jsonl').read_text(encoding='utf-8-sig').splitlines()]
process=json.loads((a.root/'process.json').read_text(encoding='utf-8-sig'))
log=(a.root/'player.log').read_text(encoding='utf-8-sig',errors='replace')
expected={'Missing':('Missing',False),'Ready':('Ready',True),'Corrupt':('Corrupt',False),'Incompatible':('Incompatible',False),'Pending':('Ready',True),'Committed':('Ready',True)}[a.kind]
ready=next((e for e in events if e['phase']=='title-ready'),{})
image=(a.root/'title-player.png').read_bytes()
checks={'ready':process['ready'],'exit0':process['exitCode']==0,'ended':process['ended'],'notTimeout':not process['timedOut'],
 'noForce':not process['forcedTermination'],'correctScene':ready.get('scene')=='Title','noGameplayObjects':ready.get('gameObjects')==0,
 'truthfulCatalog':(ready.get('status'),ready.get('canContinue'))==expected,
 'rendered':any(e['phase']=='title-rendered' for e in events),'quitAudit':any(e['phase']=='title-quit' for e in events),
 'png':image[:8]==b'\x89PNG\r\n\x1a\n' and struct.unpack('>II',image[16:24])==(1280,720),
 'noNativeCrash':not any(x in log for x in ['Got a UNKNOWN','Native Crash Reporting','Crash!!!','Unhandled Exception:']),
 'noUnrequestedSave':not (a.root/'storage-audit.jsonl').exists()}
im=Image.open(a.root/'title-player.png').convert('RGB');checks['notCyanFailureFrame']=sum(r<15 and g>245 and b>245 for r,g,b in im.getdata())/(im.width*im.height)<.4
if a.kind in {'Pending','Committed'}: checks['terminalPhase']=ready.get('savePhase')=={'Pending':'结算待确认','Committed':'结算已保存，待回营'}[a.kind]
before=json.loads((a.root/'save-before.json').read_text(encoding='utf-8-sig'))
current=a.root/'WanxiangGuitu/ForestRuins'
after={f.relative_to(current).as_posix():hashlib.sha256(f.read_bytes()).hexdigest().upper() for f in current.rglob('*') if f.is_file()}
checks['saveBytesUnchanged']=before==after
out={'status':'PASS' if all(checks.values()) else 'FAIL','kind':a.kind,'checks':checks,'ready':ready,'process':process,
 'scope':'Actual final Player default Title scene and observational capture. Background WM_CLOSE only. Native UI / titlebar / human NOT_RUN.'}
(a.root/'b09-title-analysis.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(out,ensure_ascii=False));raise SystemExit(0 if all(checks.values()) else 1)
