import pathlib, csv, json, hashlib, collections
R=pathlib.Path.cwd()
D=R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression05Implementation'
O=D/'EVIDENCE/R2'
old=list(csv.DictReader((D/'FINAL_RUN_RECONCILIATION.csv').open(encoding='utf-8-sig')))
search=json.loads((O/'driver-search.json').read_text())
supplement=json.loads((O/'driver-search-supplement.json').read_text())
assert not any(search['matches'].values()) and not supplement['matches']
target=[v for v in old if v['driver_artifact_status']=='HISTORICAL_HASH_ONLY']
assert len(target)==114
result=[]
for row in sorted(target,key=lambda x:(x['driver_sha256'],x['run_id'])):
    product=R/row['product_artifact_path']
    assert hashlib.sha256(product.read_bytes()).hexdigest().upper()==row['product_dll_sha256']
    pdb=product.with_suffix('.pdb')
    result.append({
        'driver_sha256':row['driver_sha256'],'run_id':row['run_id'],
        'historical_group':row['group'],'historical_class_unchanged':row['recorded_class'],
        'r1_pass_source_gap':row['group']=='r1new79' and row['recorded_class']=='PASS',
        'hash_meaning':'POWERSHELL_LAUNCHER_SOURCE_SHA256',
        'exact_source_found':'NO','exact_source_location':'',
        'driver_binary_found':'N/A_INTERPRETED_POWERSHELL_SCRIPT',
        'driver_pdb_found':'N/A_SCRIPT_NOT_COMPILED',
        'compilation_parameters_found':'N/A_SCRIPT_NOT_COMPILED',
        'original_launch_parameters':'PARTIAL_MANIFEST; full original launcher command unavailable',
        'product_binary_found':'YES_EXACT_SHA256; not a replacement for launcher source',
        'product_binary_path':row['product_artifact_path'],'product_binary_sha256':row['product_dll_sha256'],
        'product_pdb_candidate':pdb.relative_to(R).as_posix() if pdb.is_file() else '',
        'product_pdb_scope':'Candidate symbol presence only; not a PowerShell source/PDB association',
        'independently_reproducible':'NO_EXACT_LAUNCHER_SOURCE_AND_FULL_INVOCATION',
        'recovery_status':'UNRECOVERED_NOT_PASS',
        'original_manifest':row['manifest'],'original_manifest_sha256':row['manifest_sha256'],
        'search_evidence':'EVIDENCE/R2/driver-search.json;EVIDENCE/R2/driver-search-supplement.json;EVIDENCE/R2/git-fsck.txt;EVIDENCE/R2/git-object-inventory.txt'
    })
with (D/'DRIVER_ARCHIVE_RECOVERY.csv').open('w',encoding='utf-8-sig',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(result[0]));w.writeheader();w.writerows(result)
summary={'rows':len(result),'uniqueHashes':len(set(x['driver_sha256'] for x in result)),'r1PassGaps':sum(x['r1_pass_source_gap'] for x in result),'recoveredExactSources':0,'independentlyReproducible':0,'historicalClasses':dict(collections.Counter(x['historical_class_unchanged'] for x in result))}
(O/'driver-recovery-summary.json').write_text(json.dumps(summary,indent=2))
print(json.dumps(summary))
