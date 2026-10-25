"""Derive only the supplied ended All. Reuse B08 summary and add B09 results."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args();here=Path(__file__).resolve().parent
subprocess.run([sys.executable,'-B',str(here.parent/'DeliveryB08/Summarize-Evidence.py'),'--run',str(a.run),'--output',str(a.output)],check=True)
read=lambda p:json.loads(p.read_text(encoding='utf-8-sig'));out=read(a.output);rows=read(a.run/'results.json')
out['b09Methods']={r['name']:dict(status=r['status'],exitCode=r['exitCode'],timedOut=r['timedOut']) for r in rows if r['name'].startswith(('B09','normal-ai.Entry'))}
out['formalTitles']=[dict(cell=p.parent.name,**read(p)) for p in sorted(a.run.glob('B09-Title-*/b09-title-analysis.json'))]
root=a.run/'Normal-Entry';points=[root/f'b08-checkpoint-{i}.json' for i in [1,2,3]]
if all(p.exists() for p in points):
 first,second,third=map(read,points)
 out['entryAdventure']=dict(scope='Actual Title uGUI callbacks then Editor bot / normal NPC AI; NOT native input',checkpoints=[dict(stage=v['stage'],profile=v['profile'],run=v['run'],region=v['region'],layoutSha256=hashlib.sha256(v['layout'].encode()).hexdigest(),streams=v['streams'],ledger=v['ledger'],gear=v['gear'],warehouse=v['warehouse'],tutorial=v['tutorial']) for v in [first,second,third]],differentRuns=first['run']!=second['run'],exactFinalResume=all(second[k]==third[k] for k in second if k!='stage'),journal=(root/'normal-results.txt').read_text(encoding='utf-8-sig').splitlines())
else:out['entryAdventure']=dict(status='NOT_RUN',reason='Incomplete checkpoints; see actual failed dependency')
out['limitations'].update(nativeMenu='NOT_RUN',editorCyanRootCause='UNRESOLVED',animationImplementation='Existing compatible Generic/Legacy clips used; Dodge procedural, no Humanoid replacement claimed')
a.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf8');print(json.dumps({'b09Methods':out['b09Methods'],'counts':out['counts'],'unexpectedFailures':out['unexpectedFailures']}))
