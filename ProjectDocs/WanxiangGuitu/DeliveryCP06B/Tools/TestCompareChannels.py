from pathlib import Path
import sys,json,copy,subprocess
root=Path(sys.argv[1]);root.mkdir(exist_ok=False);tool=Path(__file__).with_name('CompareChannels.py');source=Path(sys.argv[2]);a=json.loads((source/'ChannelControlData2/channel-pair.json').read_text(encoding='utf-8'));b=json.loads((source/'ChannelNormalData2/channel-pair.json').read_text(encoding='utf-8'));cases=[]
def add(name,mutate,expected):
 x=copy.deepcopy(a);y=copy.deepcopy(b);mutate(x,y);folder=root/name;folder.mkdir();(folder/'a.json').write_text(json.dumps(x),encoding='utf-8');(folder/'b.json').write_text(json.dumps(y),encoding='utf-8');run=subprocess.run([sys.executable,str(tool),str(folder/'a.json'),str(folder/'b.json'),str(folder/'report.json')],capture_output=True,text=True,encoding='utf-8');(folder/'stdout.txt').write_text(run.stdout,encoding='utf-8');(folder/'stderr.txt').write_text(run.stderr,encoding='utf-8');report=json.loads((folder/'report.json').read_text(encoding='utf-8'));cases.append(dict(name=name,status='PASS' if report['status']==expected and run.returncode==(0 if expected=='PASS' else 1) else 'FAIL',actual=report['status'],exitCode=run.returncode,expected=expected))
add('positive',lambda x,y:None,'PASS')
add('enumeration-order',lambda x,y:y['legacy'].reverse(),'PASS')
add('changed-amount',lambda x,y:y['legacy'][0].update(amount=999),'FAIL')
add('missing-old-drop',lambda x,y:y['legacy'].pop(),'FAIL')
add('extra-old-drop',lambda x,y:y['legacy'].append(copy.deepcopy(y['legacy'][0])),'FAIL')
add('changed-quality',lambda x,y:y['legacy'][-1].update(quality=4),'FAIL')
add('changed-affix',lambda x,y:y['legacy'][-1].update(affixes=[5]),'FAIL')
add('changed-stream',lambda x,y:y.update(after='bad'),'FAIL')
add('changed-global',lambda x,y:y.update(globalAfter='bad'),'FAIL')
add('changed-run',lambda x,y:y.update(run='other'),'FAIL')
add('duplicate-supplement',lambda x,y:y.update(additional=2),'FAIL')
add('old-control-has-extra',lambda x,y:x.update(additional=1),'FAIL')
(root/'summary.json').write_text(json.dumps(dict(status='PASS' if all(c['status']=='PASS' for c in cases) else 'FAIL',cases=cases),indent=2),encoding='utf-8');print(len(cases),'checks');sys.exit(any(c['status']!='PASS' for c in cases))
