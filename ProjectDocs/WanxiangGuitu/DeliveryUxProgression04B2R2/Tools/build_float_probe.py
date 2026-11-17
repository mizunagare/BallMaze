"""Compile only the R2 observation sidecar in a brand-new Player copy."""
import argparse,pathlib,shutil,subprocess,json,hashlib,datetime
R=pathlib.Path.cwd()
def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def dump(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True)
    if p.exists():raise RuntimeError('Refuse replacing '+str(p))
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--session',required=True);ap.add_argument('--copy',required=True);a=ap.parse_args()
    session=(R/a.session).absolute();dest=(R/a.copy).absolute();source=R/'Builds/ux04b2r1/SESSION-20261116-1115/player'
    if session.exists() or dest.exists():raise SystemExit('All build/evidence/copy destinations must be NEW')
    # Existing frozen artifacts are inputs only, never rewritten.
    frozen=R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343'
    rows=list(__import__('csv').DictReader((frozen/'SUBMIT_WHITELIST.csv').open(encoding='utf-8-sig')))
    errors=[r['path'] for r in rows if not (R/r['path']).is_file() or (r['sha256']!='SELF_REFERENTIAL_META' and sha(R/r['path'])!=r['sha256'])]
    if errors:raise SystemExit('Frozen original changed: '+repr(errors))
    work=session/'_build';work.mkdir(parents=True);dump(work/'preflight-frozen961.json',{'checked':len(rows),'changes':errors})
    shutil.copytree(source,dest)
    data=dest/'WanxiangGuitu_Data';managed=data/'Managed';product_before=sha(managed/'Assembly-CSharp.dll')
    assert product_before=='6f876c6090ce57e498359bf93fb812583f848d3064612c10940f24f83c389db7'
    src=R/'ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2/Tools/FloatProbe.cs';executed=work/'FloatProbe.executed.cs';shutil.copyfile(src,executed)
    names=['mscorlib','netstandard','System','System.Core','Assembly-CSharp','UnityEngine.CoreModule','UnityEngine.PhysicsModule','UnityEngine.ScreenCaptureModule','UnityEngine.ImageConversionModule','UnityEngine.AIModule','Unity.InputSystem','UnityEngine.ScriptingModule','UnityEngine.JSONSerializeModule','UnityEngine.UI','UnityEngine.UIModule','UnityEngine.TextRenderingModule']
    references=[managed/(n+'.dll') for n in names];assert all(p.is_file() for p in references)
    compiler=pathlib.Path('C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Data/DotNetSdk/sdk/8.0.318/Roslyn/bincore/csc.dll');dotnet='C:/Program Files/dotnet/dotnet.exe';dll=managed/'B2R2FloatProbe.dll'
    cmd=[dotnet,str(compiler),'-nologo','-target:library','-nostdlib+','-deterministic','-out:'+str(dll)]+['-r:'+str(p) for p in references]+[str(executed)]
    p=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace')
    (work/'driver-compile.log').write_text(json.dumps(cmd,ensure_ascii=False)+'\n'+p.stdout+'\n'+p.stderr,encoding='utf-8')
    if p.returncode!=0:raise SystemExit('Observation driver compilation failed; retained log. Exit='+str(p.returncode))
    initp=data/'RuntimeInitializeOnLoads.json';asmp=data/'ScriptingAssemblies.json';before={'runtime':sha(initp),'assemblies':sha(asmp)}
    init=json.loads(initp.read_text(encoding='utf-8-sig'));asm=json.loads(asmp.read_text(encoding='utf-8-sig'))
    removed=[e for e in init['root'] if e.get('assemblyName') in ('B2R1ObservationDriver','B2R2FloatProbe')];init['root']=[e for e in init['root'] if e not in removed]
    entry={'assemblyName':'B2R2FloatProbe','nameSpace':'B2R2Float','className':'Driver','methodName':'Boot','loadTypes':0,'isUnityClass':False};init['root'].append(entry)
    assert len(asm['names'])==len(asm['types']);pairs=[(n,t) for n,t in zip(asm['names'],asm['types']) if n not in ('B2R1ObservationDriver.dll','B2R2FloatProbe.dll')];pairs.append(('B2R2FloatProbe.dll',16));asm['names']=[x[0] for x in pairs];asm['types']=[x[1] for x in pairs]
    # These TWO files belong ONLY to the new disposable Player copy.
    initp.write_text(json.dumps(init,ensure_ascii=False,separators=(',',':')),encoding='utf-8');asmp.write_text(json.dumps(asm,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    assert sha(managed/'Assembly-CSharp.dll')==product_before
    shutil.copyfile(dll,work/'B2R2FloatProbe.dll');shutil.copyfile(managed/'Assembly-CSharp.dll',work/'Assembly-CSharp.input.dll')
    receipt={'scope':'R2 observation sidecar compile ONLY; existing product copied unchanged','compileExitCode':p.returncode,'compiler':str(compiler),'compilerSHA256':sha(compiler),'command':cmd,'compileLogSHA256':sha(work/'driver-compile.log'),'source':src.as_posix(),'sourceSHA256':sha(src),'executedSource':executed.as_posix(),'executedSourceSHA256':sha(executed),'productDLLSHA256':product_before,'driverSHA256':sha(dll),'exeSHA256':sha(dest/'WanxiangGuitu.exe'),'copy':str(dest),'removedOldInitializerEntries':removed,'initializer':entry,'registrationBefore':before,'registrationAfter':{'runtime':sha(initp),'assemblies':sha(asmp)},'references':[{'path':str(p),'sha256':sha(p)} for p in references]}
    receipt['buildId']='ux04b2r2-float-'+product_before[:8]+'-'+receipt['exeSHA256'][:8]+'-'+receipt['driverSHA256'][:8]
    dump(work/'build-receipt.json',receipt);print(json.dumps({k:receipt[k] for k in ['scope','buildId','productDLLSHA256','driverSHA256','sourceSHA256','compileExitCode']},indent=2))
if __name__=='__main__':main()
