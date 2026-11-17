"""Generate immutable-delivery index and all-attempt Player run matrix."""
import argparse, pathlib, json, csv, hashlib, shutil

def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--session',required=True);ap.add_argument('--delivery',required=True);ap.add_argument('--audit',required=True);ap.add_argument('--recompute',required=True)
    a=ap.parse_args(); session=pathlib.Path(a.session); delivery=pathlib.Path(a.delivery)
    targets=[delivery/'PLAYER_RUN_MATRIX.csv',delivery/'EVIDENCE'/'INDEX.json',delivery/'PROTECTION_SHA256.tsv']
    if any(p.exists() for p in targets): raise SystemExit('Refuse replacing final delivery artifact')
    manifests=[]; inventory=[]
    for p in sorted(session.rglob('run-manifest.json')):
        m=json.loads(p.read_text(encoding='utf-8')); m['manifestPath']=p.as_posix();manifests.append(m)
    fields=['runId','mode','buildId','dllSHA256','exeSHA256','driverDllSHA256','pid','exitCode','verdict','completeFlag','checks','passed','failed','manifest','result','inputEvents','stateChanges','observations']
    with targets[0].open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for m in manifests:
            row={k:m.get(k,'') for k in fields}; ev=pathlib.Path(m['manifestPath']).parent
            row.update({k:(m.get('resultJson') or {}).get(k,'') for k in ['checks','passed','failed']})
            row.update({'manifest':m['manifestPath'],'result':(ev/'result.json').as_posix(),'inputEvents':(ev/'r1-input-events.jsonl').as_posix(),'stateChanges':(ev/'r1-state-changes.jsonl').as_posix(),'observations':(ev/'r1-observations.jsonl').as_posix()});w.writerow(row)
    for p in sorted(session.rglob('*')):
        if p.is_file() and '_roots' not in p.parts:
            inventory.append({'path':p.as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)})
    history=pathlib.Path('ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2/EVIDENCE/INDEX.json')
    index={'scope':'UX-04-B2-R1; all attempts preserved','session':session.as_posix(),'historicalB2Index':{'path':history.as_posix(),'sha256':sha(history)},'runs':[{'runId':m['runId'],'mode':m['mode'],'manifest':m['manifestPath'],'verdict':m['verdict']} for m in manifests],'files':inventory,'workspaceAudit':a.audit,'independentRecompute':a.recompute,'snapshot':'I:/unity/WanxiangGuitu-UX04B2R1-snapshot-20261116-1108'}
    shutil.copyfile(pathlib.Path(a.audit)/'PROTECTION_SHA256.tsv',targets[2])
    index['deliveryFiles']=[{'path':p.as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(delivery.rglob('*')) if p.is_file() and p!=targets[1]]
    targets[1].parent.mkdir(parents=True,exist_ok=True); targets[1].write_text(json.dumps(index,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'runs':len(manifests),'files':len(inventory),'matrix':targets[0].as_posix(),'index':targets[1].as_posix()},ensure_ascii=False))
if __name__=='__main__': main()
