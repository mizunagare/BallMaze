"""Read-only classification tests using actual new runner exit files.
The 293-PASS input is an EXPLICIT SYNTHETIC COPY, never a claim that gameplay passed 293.
"""
import argparse,copy,hashlib,importlib.util,json
from pathlib import Path
HERE=Path(__file__).resolve().parent
def main():
    a=argparse.ArgumentParser();a.add_argument('root',type=Path);a.add_argument('--output',type=Path,required=True);o=a.parse_args();o.output.mkdir(exist_ok=False)
    spec=importlib.util.spec_from_file_location('receipt_real',HERE.parent/'DeliveryCombatPresentation03/Receipt.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    rows=[]
    for mode in ('Editor','Runtime'):
        folder=o.root/mode;pr=folder/'process-results.json';ex=folder/('CP03Editor.Run.exit.json' if mode=='Editor' else 'CP03Runtime.exit.json');src=folder/'presentation.json'
        protected={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in (src,pr,ex)}
        clone=copy.deepcopy(json.loads(src.read_text(encoding='utf-8-sig')))
        clone['fixtureKind']='SYNTHETIC 293 PASS ASSERTIONS FOR READER TEST ONLY; not actual gameplay result'
        for row in clone['rows']:row['status']='PASS'
        synthetic=folder/'reader-tool-synthetic-293-pass.json'
        if synthetic.exists():raise ValueError('fresh synthetic assertion filename required')
        synthetic.write_bytes(json.dumps(clone).encode('utf-8'))
        contract=HERE.parent/'DeliveryCombatPresentation03R11/Contracts'/(mode+'.json')
        for name,data,evidence,extra,wanted,code in [('actual-open',src,True,{},'BLOCKED',2),('actual-exit-synthetic-293-pass',synthetic,True,{},'PASS',0),('scalars-only-no-proof',synthetic,False,dict(process_status='PASS',exit_code=0,timed_out=False),'INCOMPLETE',3),('timeout-claim-with-zero-exit',synthetic,True,dict(timed_out=True),'INCOMPLETE',3)]:
            args=dict(profile=mode,contract=contract,**extra)
            if evidence:args.update(process_receipt=pr,exit_receipt=ex)
            result=m.evaluate(data,**args);m.write(result,o.output/(mode+'-'+name))
            ok=result['overallStatus']==wanted and result['exitCode']==code
            if evidence and not extra:ok=ok and result['process']['evidenceStatus']=='PASS' and result['process']['exitCode']==0
            rows.append(dict(name=mode+'-'+name,status='PASS' if ok else 'FAIL',overall=result['overallStatus'],exitCode=result['exitCode'],expected=wanted,expectedExit=code,scope='Reader validation, NOT another Unity run; all-pass assertion clone is synthetic',originalSourceSHA256=protected))
        if any(hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h for p,h in protected.items()):raise ValueError('original evidence changed')
    result=dict(counts={s:sum(r['status']==s for r in rows) for s in ('PASS','FAIL')},rows=rows,note='Real Unity outcomes remain 291 PASS +2 UNRESOLVED. Originals were not modified.')
    (o.output/'results.json').write_bytes(json.dumps(result,indent=2).encode('utf-8'));print(json.dumps(result['counts']));return 1 if result['counts']['FAIL'] else 0
if __name__=='__main__':raise SystemExit(main())
