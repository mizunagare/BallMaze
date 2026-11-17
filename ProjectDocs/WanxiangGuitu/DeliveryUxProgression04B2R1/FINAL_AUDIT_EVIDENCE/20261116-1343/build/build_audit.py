"""Hash build artifacts and inputs only; never runs a build or Player."""
import pathlib,json,hashlib,csv
R=pathlib.Path.cwd(); S=R/'Evidence/Runs04B2R1/SESSION-20261116-1115'; O=R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/build';O.mkdir(parents=True,exist_ok=True)
def load(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
p=load(S/'_build/receipt/b2-product-build.json'); d=load(S/'_build/driver-A03/receipt/r1-driver-injection-A03.json'); sm=load(S/'_build/receipt/source-manifest.json'); checks=[]
def verify(label,path,expected,size=None):
    path=pathlib.Path(path); exists=path.is_file(); actual=sha(path) if exists else 'MISSING'; n=path.stat().st_size if exists else None
    checks.append({'label':label,'path':str(path),'expectedSHA256':expected,'actualSHA256':actual,'bytes':n,'expectedBytes':size,'result':'PASS' if actual==expected and (size is None or n==size) else 'FAIL'})
player=R/p['isolatedCopy']; managed=player/'WanxiangGuitu_Data/Managed'
verify('R1 product assembly in Player',managed/'Assembly-CSharp.dll',p['productDllSHA256'],p['productDllBytes'])
verify('R1 archived product assembly',S/'_build/Assembly-CSharp.dll',p['productDllSHA256'],p['productDllBytes'])
verify('pre-B2 Acceptance assembly',R/'Builds/WanxiangGuitu.Acceptance/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll',p['preB2AcceptanceDllSHA256'])
verify('current A03 sidecar driver',managed/'B2R1ObservationDriver.dll',d['driverDllSHA256'],d['driverDllBytes'])
verify('current driver source',d['source'],d['sourceSHA256'])
verify('executed driver source',d['executedSource'],d['executedSourceSHA256'])
verify('product compile log',p['compileLog'],p['compileLogSHA256'])
verify('driver compile log',d['compileLog'],d['compileLogSHA256'])
verify('Roslyn compiler',p['compiler'],p['compilerSHA256'])
verify('product response file',p['responseFile'],p['responseSHA256'])
for e in sm['sources']:verify('source inventory',R/e['path'],e['sha256'])
rsp=pathlib.Path(p['responseFile']).read_text(encoding='utf-8-sig').splitlines(); sources=[l.strip().strip('"') for l in rsp if l.strip().strip('"').endswith('.cs')]; defs=[l for l in rsp if l.startswith('-define:')]; refs=[l for l in rsp if l.startswith('-r:') or l.startswith('-reference:')]
manifest_paths={e['path'].replace(chr(92),'/') for e in sm['sources']}; compiled={x.replace(chr(92),'/') for x in sources}
for mode in ['sort-ugui','sort-imgui','strength0','strength3','preview9','guid','golden','collection','restart']:
    m=load(S/'A03'/mode/'run-manifest.json')
    verify('EXE for '+mode,player/'WanxiangGuitu.exe',m['exeSHA256'])
    checks.append({'label':'run build identity '+mode,'result':'PASS' if m['buildId']=='ux04b2r1-6f876c60-b70442f9-5a2654de' and m['dllSHA256']==p['productDllSHA256'] and m['driverDllSHA256']==d['driverDllSHA256'] else 'FAIL'})
    checks.append({'label':'old Acceptance harness not requested '+mode,'result':'PASS' if '--acceptance' not in m['arguments'] else 'FAIL'})
for name,key in [('RuntimeInitializeOnLoads.json','runtimeInitializeOnLoadsAfter'),('ScriptingAssemblies.json','scriptingAssembliesAfter')]:verify('injection '+name,player/'WanxiangGuitu_Data'/name,d['injection'][key])
summary={'identity':'ux04b2r1-6f876c60-b70442f9-5a2654de','sourceInventoryCount':len(sm['sources']),'sourceInventoryChanged':[x['path'] for x in checks if x['label']=='source inventory' and x['result']!='PASS'],'compiledSourceCount':len(sources),'compiledUniqueSourceCount':len(compiled),'compiledSourcesOutsideInventory':sorted(compiled-manifest_paths),'inventoryNotCompiled':sorted(manifest_paths-compiled),'defineCount':len(defs),'hasUX_ACCEPTANCE':'-define:UX_ACCEPTANCE' in defs,'referenceCount':len(refs),'checks':checks,'result':'PASS' if all(x['result']=='PASS' for x in checks) else 'FAIL','limitations':['This is Acceptance-define compiled product C#, not a newly built release Player.','166 refers to the Assets source inventory; editor-only inputs are not all part of Assembly-CSharp.','A03 sidecar currently available only in excluded Builds tree; no A03 driver binary is archived in Evidence.','Pre-B2 Acceptance DLL, rebuilt product DLL, and sidecar driver are three different identities.']}
(O/'BUILD_IDENTITY_RECALCULATED.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8'); print(json.dumps({k:v for k,v in summary.items() if k!='checks'},ensure_ascii=False,indent=2));raise SystemExit(summary['result']!='PASS')
