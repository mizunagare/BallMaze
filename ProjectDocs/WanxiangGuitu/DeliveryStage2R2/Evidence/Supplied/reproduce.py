"""Independent review probes for the exact S2-R1 Python audit.
Synthetic receipt data only. Does not load player saves, run Unity, or access network.
"""
from pathlib import Path
import argparse, json, hashlib, subprocess, sys

HERE=Path(__file__).resolve().parent
EXPECTED={'MatrixEvidence.py':'ee2f3973e74ea54cb0eda37e007c2b1315624b09','Summarize-Matrix.py':'5bd06e6bc57f20508e75618610ede40a3582253d'}

def write(p,d):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(d,sort_keys=True,ensure_ascii=False)+'\n',encoding='utf8')

def fixture(root, ident='one'):
    c=dict(id=ident,build='Safety',strategy='Gather',seed=1,weapon=3,target=4)
    f=root/ident;f.mkdir(parents=True)
    write(f/'stage2-input.json',c)
    meta=dict(schemaVersion=2,caseId=ident,attemptId='attempt-'+ident,blockId='block1',configSha256=hashlib.sha256((f/'stage2-input.json').read_bytes()).hexdigest(),codeInput='a'*64,driverInput='b'*64,launchedUtc='2026-10-27T00:00:00Z')
    write(f/'attempt.json',meta)
    m=dict(input=c,status='PASS',profile='profile-'+ident,run='run-'+ident,region='region-'+ident,secondRun='second-'+ident,secondRegion='second-region-'+ident,extracted=True,committed=True,acknowledged=True,secondForest=True,elapsedSeconds=60,damageTaken=0,potionsUsed=0,meters=90,obtained=[0,0,0,9,0,0],kept=[0,0,0,7,0,0],lost=[0]*6,measurementCompleteness='complete')
    write(f/'stage2-metrics.json',m)
    tx=[dict(label='depart',run=m['run'],profile=m['profile'],region=m['region']),dict(label='settlement-pending',run=m['run'],profile=m['profile'],region=m['region'],outcome='Extracted'),dict(label='acknowledged',profile=m['profile'],settlementStatus='Committed',ack=True),dict(label='verified-new-process-second-forest',run=m['secondRun'],profile=m['profile'],region=m['secondRegion'])]
    (f/'stage2-transactions.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in tx),encoding='utf8')
    for mode in ('Normal','Resume','FinalResume'):
        write(f/f'process-result-{mode}.json',dict(mode=mode,exitCode=0,timedOut=False))
        write(f/f'stage-result-{mode}.json',dict(meta,mode=mode,profile=m['profile'],firstRun=m['run'],run=m['run'] if mode=='Normal' else m['secondRun'],stage=1 if mode=='Normal' else 2,complete=True))
    return c,f,m,tx

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();out=a.output.resolve()
    if out.exists():raise ValueError('Output must be fresh')
    out.mkdir(parents=True)
    verified=[]
    for n,expected in EXPECTED.items():
        data=(HERE/'source'/n).read_bytes();actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if actual!=expected:raise ValueError('Source mismatch: '+n)
        verified.append(dict(file=n,gitBlob=actual,sha256=hashlib.sha256(data).hexdigest()))
    observations=[]
    def run(name,mutate):
        work=out/name;root=work/'matrix';root.mkdir(parents=True)
        c,f,m,tx=fixture(root)
        plan={'cases':[c],'inputIdentity':{'codeInput':'a'*64,'driverInput':'b'*64}}
        write(root/'owner.json',{'kind':'independent synthetic review only'})
        write(root/'preserved-processes.json',[]);write(root/'results.json',[])
        mutate(root,plan,c,f,m,tx)
        write(work/'plan.json',plan)
        process=subprocess.run([sys.executable,'-B',str(HERE/'source/Summarize-Matrix.py'),'--matrix',str(root),'--plan',str(work/'plan.json'),'--output',str(work/'summary')],capture_output=True,text=True)
        (work/'stdout.txt').write_text(process.stdout,encoding='utf8');(work/'stderr.txt').write_text(process.stderr,encoding='utf8')
        path=work/'summary/matrix-summary.json'
        result=json.loads(path.read_text()) if path.exists() else {}
        info={'case':name,'exitCode':process.returncode}
        for key in ('status','finalAcceptanceEligible','statisticsDiagnosticOnly','started','departed','knownTerminal','unknown','notStarted','counts','extractionSuccessRate'):info[key]=result.get(key)
        info['completeTimeMean']=result.get('completeTerminalStatistics',{}).get('Safety',{}).get('elapsedSeconds',{}).get('mean')
        info['partialWindows']=result.get('partialWindows');info['issues']=[{'case':r['input']['id'],'issues':r['issues']} for r in result.get('rows',[])]
        write(work/'observation.json',info);observations.append(info)
    run('01-control',lambda *args:None)
    def contradictory(root,p,c,f,m,tx):
        m.update(run=None,extracted=False,committed=False,acknowledged=False,secondForest=False);write(f/'stage2-metrics.json',m)
    run('02-original-contradiction-now-rejected',contradictory)
    run('03-stage-missing-rejected',lambda root,p,c,f,m,tx:(f/'stage-result-Resume.json').unlink())
    for value,name in [(None,'null'),([], 'array'),('complete','string'),(False,'boolean')]:
        run('04-stage-'+name,lambda root,p,c,f,m,tx,value=value:write(f/'stage-result-Resume.json',value))
    def missing(root,p,c,f,m,tx):
        c2,f2,m2,tx2=fixture(root,'two');p['cases'].append(c2);(f2/'stage2-metrics.json').unlink()
        write(root/'results.json',[{'name':'two.Normal','status':'FAIL'}])
        (f2/'stage2-transactions.jsonl').write_text(json.dumps(tx2[0])+'\n')
    run('05-missing-metrics-attempt-retained',missing)
    def partial(root,p,c,f,m,tx):
        c2,f2,m2,tx2=fixture(root,'two');p['cases'].append(c2)
        m2.update(status='FAIL',elapsedSeconds=2,extracted=False,measurementCompleteness='partial');write(f2/'stage2-metrics.json',m2)
        write(f2/'process-result-Normal.json',{'mode':'Normal','exitCode':1,'timedOut':False})
        (f2/'stage2-transactions.jsonl').write_text(json.dumps(tx2[0])+'\n')
    run('06-complete60-partial2-separated',partial)
    def skipped(root,p,c,f,m,tx):
        for x in list(f.iterdir()):x.unlink()
        write(root/'results.json',[{'name':'one.Normal','status':'NOT_RUN','detail':'Owned project occupied; no child process was launched'},{'name':'one.Resume','status':'NOT_RUN','detail':'Prior case stage skipped'},{'name':'one.FinalResume','status':'NOT_RUN','detail':'Prior case stage skipped'}])
    run('07-all-explicitly-not-run',skipped)
    def clash(root,p,c,f,m,tx):
        tx[1]['run']='unrelated-run';tx[1]['profile']='unrelated-profile';tx[1]['region']='unrelated-region'
        (f/'stage2-transactions.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in tx))
    run('08-conflicting-terminal-counted',clash)
    def modes(root,p,c,f,m,tx):
        p['cases'][0]=dict(c,requiredModes=['Normal'])
        (f/'stage-result-Resume.json').unlink();(f/'stage-result-FinalResume.json').unlink()
        (f/'process-result-Resume.json').unlink();(f/'process-result-FinalResume.json').unlink()
    run('09-plan-input-contract-mismatch',modes)
    write(out/'review-results.json',{'scope':'Independent offline synthetic inputs; not Unity/Player tests. Observed defects are not assertions that historical game runs were corrupted.','sources':verified,'observations':observations})
    for r in observations:print(r['case'],r['exitCode'],r['status'],'started',r['started'],'known',r['knownTerminal'],'rate',r['extractionSuccessRate'],'mean',r['completeTimeMean'])
if __name__=='__main__':main()
