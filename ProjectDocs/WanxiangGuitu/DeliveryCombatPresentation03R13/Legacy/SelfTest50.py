"""Tool self-tests use synthetic receipts/source mutations; never product state."""
import argparse,collections,contextlib,copy,importlib.util,io,json,runpy,subprocess,sys,tempfile
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parents[2]/'DeliveryCombatPresentation03'
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ProcessFixtures import write_process, association_paths, cli_association

def module(name,file):
    s=importlib.util.spec_from_file_location(name,HERE/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--original-root',type=Path,required=True);o=ap.parse_args();o.output.mkdir(exist_ok=False)
    receipt=module('receipt','Receipt.py');audit=module('locked','Audit-Locked.py');rows=[]
    def check(name,ok,detail=''):rows.append(dict(name=name,status='PASS' if ok else 'FAIL',detail=detail))
    contract=HERE.parent/'DeliveryCombatPresentation03R11/Contracts/Editor.json'
    template=json.loads(contract.read_text(encoding='utf-8-sig'))
    def report(statuses):
        data=copy.deepcopy(template)
        for row in data['rows']:row['status']='PASS'
        for i,status in enumerate(statuses):data['rows'][i]['status']=status
        return data
    cases=[('all-pass',report(['PASS']),'PASS',0),('pass-fail',report(['PASS','FAIL']),'FAIL',1),('pass-unresolved',report(['PASS','UNRESOLVED']),'BLOCKED',2),('mixed',report(['PASS','FAIL','UNRESOLVED']),'FAIL',1),('missing',None,'INCOMPLETE',3),('bad-json','{','INCOMPLETE',3),('empty',report([]),'INCOMPLETE',3),('unknown',report(['WHATEVER']),'INCOMPLETE',3),('duplicate',report(['PASS','PASS']),'INCOMPLETE',3),('not-run',report(['PASS','NOT_RUN']),'INCOMPLETE',3),('bad-rows',dict(layer='x',scope='x',rows={}), 'INCOMPLETE',3),('duplicate-json-key','{"layer":"a","layer":"b","scope":"s","rows":[]}', 'INCOMPLETE',3)]
    cases[6][1]['rows']=[]
    cases[8][1]['rows'][1]['name']=cases[8][1]['rows'][0]['name']
    for name,data,status,exitcode in cases:
        d=o.output/name;d.mkdir();src=d/'presentation.json'
        if data is not None:src.write_text(data if isinstance(data,str) else json.dumps(data),encoding='utf-8')
        pr,ex=write_process(d,'Editor','PASS',0,False)
        proc=subprocess.run([sys.executable,str(HERE/'Receipt.py'),'--receipt',str(src),'--output',str(d/'Report'),'--exit-code','0','--profile','Editor','--contract',str(contract),'--process-receipt',str(pr),'--exit-receipt',str(ex)]+cli_association(pr.parent,'Editor'),capture_output=True,text=True)
        (d/'stdout.txt').write_text(proc.stdout,encoding='utf-8');(d/'stderr.txt').write_text(proc.stderr,encoding='utf-8')
        q=json.loads((d/'Report/acceptance.json').read_text(encoding='utf-8'));md=(d/'Report/REPORT.md').read_text(encoding='utf-8')
        check(name,proc.returncode==exitcode and q['overallStatus']==status and '**'+status+'**' in md and (d/'Report/assertions.csv').is_file(),str(proc.returncode)+' '+q['overallStatus'])
    src=o.output/'all-pass/presentation.json'
    for name,ps,ec,to,expected in [('nonzero','FAIL',7,False,'FAIL'),('timeout','FAIL',None,True,'INCOMPLETE'),('unstarted','NOT_RUN',None,False,'INCOMPLETE')]:
        pr,ex=write_process(src.parent,'Editor',ps,ec,to)
        q=receipt.evaluate(src,ps,ec,to,contract=contract,profile='Editor',process_receipt=pr,exit_receipt=ex,**association_paths(pr.parent,'Editor'));check('process-'+name,q['overallStatus']==expected and q['process']['status']!='PASS')
    pr,ex=write_process(src.parent,'Editor','PASS',0,False)
    check('external-launcher-failure',receipt.evaluate(src,external_failure=True,contract=contract,profile='Editor',process_receipt=pr,exit_receipt=ex,**association_paths(pr.parent,'Editor'))['overallStatus']=='FAIL')
    removed=o.output/'required-case-removed.json';data=report(['PASS']);data['rows'].pop();removed.write_text(json.dumps(data),encoding='utf-8')
    result=receipt.evaluate(removed,contract=contract,profile='Editor',process_receipt=write_process(removed.parent,'Editor','PASS',0,False)[0],exit_receipt=removed.parent/'CP03Editor.Run.exit.json',**association_paths(removed.parent,'Editor'))
    check('required-case-removed',result['overallStatus']=='INCOMPLETE' and any('FROZEN_ASSERTION_SET_MISMATCH' in e for e in result['errors']))
    # Reproduce broad-delete bypass in old audit with a text fixture, not live source.
    repo=HERE.parents[2];prefix='Assets/CombatPrototype/'
    old=lambda f:audit.original(repo,prefix+f+'.cs')
    curr=lambda f:audit.norm((repo/(prefix+f+'.cs')).read_bytes())
    current=curr('AdventureCombat');baseline=old('AdventureCombat')
    check('exact-positive',len(audit.adventure(baseline,current))==4)
    def reject(name,fn):
        try:fn();check(name,False,'mutation accepted')
        except (audit.AuditError,ValueError):check(name,True,'mutation rejected')
    line=next(l for l in current.splitlines() if '?.MeleeTrace(' in l)
    mutations={'same-line-extra-gameplay':current.replace(line,line+' Time.timeScale=0;'),'duplicate-trace':current.replace(line,line+'\n'+line),'missing-trace':current.replace(line+'\n',''),'changed-argument':current.replace('MeleeTrace(hero,a.type,radius,dot,','MeleeTrace(hero,a.type,radius+1,dot,'),'extra-allowed-call':current.replace('        CombatFeedback.Find(this)?.AttackStarted(hero,type,skill);','        CombatFeedback.Find(this)?.AttackStarted(hero,type,skill);\n        CombatFeedback.Find(this)?.AttackStarted(hero,type,skill);'),'unrelated-logic':current.replace('var visited=new HashSet<Component>();','var visited=new HashSet<Component>();Time.timeScale=0;'),'changed-release':current.replace('float area=a.area;','float area=a.area*2;')}
    for name,text in mutations.items():reject('audit-'+name,lambda text=text:audit.adventure(baseline,text))
    source=o.output/'old-bypass';source.mkdir();(source/prefix).mkdir(parents=True)
    for n in ('AdventureCombat','FantasyActorVisual')+audit.LOCKED:(source/(prefix+n+'.cs')).write_text(curr(n),encoding='utf-8')
    (source/(prefix+'AdventureCombat.cs')).write_text(mutations['same-line-extra-gameplay'],encoding='utf-8')
    evidence=o.output/'old-bypass-evidence';evidence.mkdir()
    for name in ('Before2','Final2'):
        (evidence/name).mkdir();(evidence/name/'events.jsonl').write_bytes((o.original_root/name/'events.jsonl').read_bytes())
    original_bytes={prefix+n+'.cs':subprocess.check_output(['git','-C',str(repo),'show',audit.BASE+':'+prefix+n+'.cs']) for n in ('AdventureCombat','FantasyActorVisual')+audit.LOCKED}
    old_script=subprocess.check_output(['git','-C',str(repo),'show','72db192a:ProjectDocs/WanxiangGuitu/DeliveryCombatPresentation03/Audit-Locked.py']).decode('utf-8-sig')
    log=io.StringIO()
    with patch.object(sys,'argv',['Audit-Locked.py',str(source),str(evidence)]),patch.object(subprocess,'check_output',side_effect=lambda cmd:original_bytes[cmd[-1].split(':',1)[1]]),contextlib.redirect_stdout(log):exec(compile(old_script,'old-audit','exec'),{'__name__':'__main__'})
    (o.output/'old-audit-bypass.txt').write_text(log.getvalue(),encoding='utf-8');check('old-bypass-reproduced','PASS:' in log.getvalue())
    a=old('FantasyActorVisual');b=curr('FantasyActorVisual');check('sampling-positive',bool(audit.sampling(a,b)))
    reject('sampling-clock-mutation',lambda:audit.sampling(a,b.replace('float dt=camp?Time.unscaledDeltaTime:Time.deltaTime;','float dt=1;')))
    reject('sampling-duplicate-marker',lambda:audit.sampling(a,b+'\n    void LateUpdate()\n'))
    first=audit.spawns(o.original_root/'Before2/events.jsonl');final=audit.spawns(o.original_root/'Final2/events.jsonl');check('24-spawn-positive',len(audit.paired(first,final))==24)
    for name,mut in [('missing',lambda b:b.pop(next(iter(first)))),('origin',lambda b:b[next(iter(first))]['from'].__setitem__('x',999)),('direction',lambda b:b[next(iter(first))]['aim'].__setitem__('z',0)),('extra',lambda b:b.__setitem__((999,1),next(iter(b.values()))))]:
        b=copy.deepcopy(final);mut(b);reject('spawns-'+name,lambda b=b:audit.paired(first,b))
    duplicate=o.output/'duplicate-spawn.jsonl';sample=json.dumps(next(iter(final.values())));duplicate.write_text(sample+'\n'+sample);reject('spawns-duplicate-identity',lambda:audit.spawns(duplicate))
    invalid=o.output/'nan-spawn.jsonl';obj=copy.deepcopy(next(iter(final.values())));obj['from']['x']=float('nan');invalid.write_text(json.dumps(obj));reject('spawns-nonfinite',lambda:audit.spawns(invalid))
    # Check every locked path by injecting one local source mutation in a temporary fixture.
    frozen={prefix+n+'.cs':old(n) for n in ('AdventureCombat','FantasyActorVisual')+audit.LOCKED}
    with patch.object(audit,'original',side_effect=lambda repo,path:frozen[path]):
        (source/(prefix+'AdventureCombat.cs')).write_text(current,encoding='utf-8')
        for n in audit.LOCKED:
            f=source/(prefix+n+'.cs');f.write_text(curr(n)+'\n// forbidden mutation\n',encoding='utf-8')
            reject('locked-'+n,lambda:audit.audit(source,o.original_root));f.write_text(curr(n),encoding='utf-8')
    # CLI exit and failure report are checked too, not only in-process exceptions.
    finalfile=evidence/'Final2/events.jsonl'
    with finalfile.open('a',encoding='utf-8') as f:f.write('\n'+json.dumps(next(iter(final.values())))+'\n')
    command=[sys.executable,str(HERE/'Audit-Locked.py'),str(repo),str(evidence),'--output',str(o.output/'negative-audit-cli.json')]
    proc=subprocess.run(command,capture_output=True,text=True)
    (o.output/'negative-audit-cli.stdout.txt').write_text(proc.stdout+proc.stderr,encoding='utf-8')
    check('audit-cli-exit-report',proc.returncode==1 and json.loads((o.output/'negative-audit-cli.json').read_text())['status']=='FAIL')
    result=dict(counts=dict(collections.Counter(r['status'] for r in rows)),rows=rows)
    (o.output/'selftest.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result['counts']));return 1 if result['counts'].get('FAIL') else 0
if __name__=='__main__':raise SystemExit(main())
