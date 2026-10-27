"""Offline review probes; synthetic data only, no Unity/game execution or player saves.
Run: python reproduce.py --output <new-empty-directory>
The repository summarizer is unmodified and its Git blob identity is checked.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

SOURCE_BLOB = '23900d40329126aa33d8fbcd90668050199347a5'

def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def case(name: str) -> dict:
    return dict(id=name, build='Safety', strategy='Gather', seed=1, weapon=3, target=4)

def receipt(config: dict, run: str | None, seconds: float = 60) -> dict:
    return dict(input=config, status='PASS', run=run, extracted=True,
                committed=True, acknowledged=True, secondForest=True,
                obtained=[0,0,0,9,0,0], kept=[0,0,0,7,0,0],
                elapsedSeconds=seconds, damageTaken=0, potionsUsed=0, meters=90)

def probe(root: Path, name: str, kind: str, source: Path) -> dict:
    work=root/name; work.mkdir(parents=True)
    shutil.copyfile(source, work/'Summarize-Matrix.py')
    configs=[case('completed')]
    if kind in ('missing', 'partial'): configs.append(case('started-then-interrupted'))
    write_json(work/'MATRIX_INPUTS.json', {'cases':configs})
    matrix=work/'matrix'; matrix.mkdir()
    write_json(matrix/'owner.json', {'kind':'SYNTHETIC_OFFLINE_REVIEW_ONLY'})
    steps=[]
    for i, config in enumerate(configs):
        folder=matrix/config['id']; folder.mkdir()
        data=receipt(config, f'synthetic-run-{i}')
        if kind == 'contradiction':
            data.update(run=None, extracted=False, committed=False, acknowledged=False, secondForest=False)
        if i == 1:
            # Independent departure evidence remains, but the final metric file is absent or partial.
            (folder/'stage2-transactions.jsonl').write_text(json.dumps({'label':'depart','run':'synthetic-run-1','profile':'synthetic-profile'})+'\n', encoding='utf8')
            steps.append({'name':config['id']+'.Normal','status':'FAIL','reason':'synthetic failure after departure'})
            if kind == 'missing': continue
            data.update(status='FAIL', extracted=False, elapsedSeconds=2)
        write_json(folder/'stage2-metrics.json', data)
        for mode in ('Normal','Resume','FinalResume'):
            failed=i==1 and kind=='partial'
            write_json(folder/f'process-result-{mode}.json', {'mode':mode, 'exitCode':1 if failed else 0,'timedOut':False})
            if not failed: steps.append({'name':config['id']+'.'+mode,'status':'PASS'})
    write_json(matrix/'results.json', steps)
    child=subprocess.run([sys.executable,str(work/'Summarize-Matrix.py'),'--matrix',str(matrix.resolve()),'--output',str((work/'summary').resolve())],capture_output=True,text=True,check=False)
    (work/'stdout.txt').write_text(child.stdout,encoding='utf8');(work/'stderr.txt').write_text(child.stderr,encoding='utf8')
    summary=json.loads((work/'summary/matrix-summary.json').read_text())
    observed={'name':name,'kind':kind,'processExit':child.returncode,'aggregateStatus':summary['status'],
              'planned':summary['planned'],'validSorties':summary['validSorties'],
              'extractionSuccessRate':summary['extractionSuccessRate'],'counts':summary['counts'],
              'safetyTimeStats':summary['groupsDescriptiveOnly']['Safety']['elapsedSeconds']}
    if kind=='baseline':
        assert child.returncode==0 and summary['validSorties']==1 and summary['extractionSuccessRate']==1
        observed['reviewResult']='CONTROL_MATCHES'
    elif kind=='missing':
        assert child.returncode==1 and summary['validSorties']==1 and summary['extractionSuccessRate']==1 and summary['counts']['FAIL']==1
        observed['reviewResult']='REPRODUCED: started attempt is absent from the rate population; failure still makes aggregate FAIL'
    elif kind=='contradiction':
        assert child.returncode==0 and summary['status']=='PASS' and summary['validSorties']==0
        observed['reviewResult']='REPRODUCED: aggregate PASS despite missing Run identity and false terminal lifecycle flags'
    else:
        stats=summary['groupsDescriptiveOnly']['Safety']['elapsedSeconds']
        assert child.returncode==1 and stats['n']==2 and stats['mean']==31
        observed['reviewResult']='REPRODUCED: failed partial 2-second sample is pooled with completed 60-second sample'
    write_json(work/'review-observation.json',observed)
    return observed

def main() -> None:
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    root=args.output.resolve()
    if root.exists(): raise SystemExit('Refusing to overwrite output; choose a fresh path')
    source=Path(__file__).with_name('Summarize-Matrix.py');raw=source.read_bytes()
    actual=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    if actual!=SOURCE_BLOB: raise SystemExit('Source blob mismatch; refusing to test altered code')
    root.mkdir(parents=True)
    outcomes=[probe(root,name,kind,source) for name,kind in [('control','baseline'),('missing-receipt','missing'),('contradictory-receipt','contradiction'),('partial-statistics','partial')]]
    result={'scope':'Independent offline Python probes against byte-identical repository summarizer; synthetic fixtures, NOT Unity or product validation',
            'sourceGitBlob':actual,'probes':outcomes,'historicalRunEffect':'Not established: current delivered 19 cases were reported complete. These probes do not prove their data is corrupted.'}
    write_json(root/'review-results.json',result)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
