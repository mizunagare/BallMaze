"""Read-only repository audit; writes receipts only under the supplied new output."""
import argparse, pathlib, hashlib, json, re, csv

def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f, 'sha256').hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--baseline',required=True)
    ap.add_argument('--output',required=True)
    a=ap.parse_args(); root=pathlib.Path.cwd(); out=pathlib.Path(a.output)
    out.mkdir(parents=True,exist_ok=False)
    baseline=json.loads(pathlib.Path(a.baseline).read_text(encoding='utf-8'))
    allowed={'Assets/CombatPrototype/AdventureLoadout.cs','Assets/CombatPrototype/ContainerInventoryView.cs','Assets/CombatPrototype/CatInventoryPresenter.cs','ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/Tools/IntDriverR1.cs','ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/Tools/run_r1_player.py'}
    changed=[]; missing=[]; rows=[]
    for entry in baseline['files']:
        p=root/entry['path']; current=sha(p) if p.is_file() else 'MISSING'
        status='UNCHANGED' if current==entry['sha256'] else ('AUTHORIZED_R1_EDIT' if entry['path'] in allowed else 'UNEXPECTED_CHANGE')
        rows.append([entry['path'],entry['sha256'],current,status])
        if status=='UNEXPECTED_CHANGE': changed.append(entry['path'])
        if current=='MISSING': missing.append(entry['path'])
    with (out/'PROTECTION_SHA256.tsv').open('w',encoding='utf-8',newline='') as f:
        w=csv.writer(f,delimiter='	');w.writerow(['file','prechange_sha256','current_sha256','status']);w.writerows(rows)
    targets=['Assets/CombatPrototype/B2AttackModel.cs.meta','Assets/CombatPrototype/B2Collection.cs.meta','Assets/CombatPrototype/B2InventoryQuery.cs.meta']
    guidfiles={}; malformed=[]
    for dirname in ['Assets','Packages','Library/PackageCache']:
        for p in (root/dirname).rglob('*.meta'):
            rel=p.relative_to(root).as_posix(); text=p.read_text(encoding='utf-8-sig',errors='replace')
            m=re.search(r'^guid: ([0-9a-f]{32})$',text,re.M)
            if m: guidfiles.setdefault(m.group(1),[]).append(rel)
            elif rel in targets: malformed.append(rel)
    new={p:next((g for g,ps in guidfiles.items() if p in ps),None) for p in targets}
    collisions={g:ps for g,ps in guidfiles.items() if len(ps)>1}
    new_ok=not malformed and len(set(new.values()))==3 and None not in new.values() and all(len(guidfiles[g])==1 for g in new.values())
    pre=[g for g,ps in guidfiles.items() if not any(p in targets for p in ps)]
    manifest={'preExisting':','.join(pre),'newGuids':','.join(new[p] or '' for p in targets)}
    (out/'guid-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
    result={'baselineFileCount':len(rows),'unexpectedChanges':changed,'missingFiles':missing,'authorizedEdits':[p for p,b,c,s in rows if s=='AUTHORIZED_R1_EDIT'],'newGuids':new,'newGuidUnique':new_ok,'allExistingGuidDuplicates':collisions,'result':'PASS' if not changed and not missing and new_ok else 'FAIL'}
    (out/'workspace-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='allExistingGuidDuplicates'},ensure_ascii=False,indent=2))
    return 0 if result['result']=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
