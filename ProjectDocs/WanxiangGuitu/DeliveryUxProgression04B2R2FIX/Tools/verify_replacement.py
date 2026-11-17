"""Independent read-only UX04B2R2FIX raw-evidence oracle. Never builds/launches Unity.
Only writes REPLACEMENT_ORACLE.{md,json,csv} under FIX/EVIDENCE.
No imports from runner; PASS/check booleans are deliberately not proof.
"""
import argparse, base64, collections, csv, hashlib, json, re, struct
from functools import lru_cache
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
FIX=Path(__file__).resolve().parents[1]
EXPECTED='ab3d5ba4f4a234598056915ab7b1dca4ad4be57f68298fc24d1b718d267a2df1'
DOMAINS={'GearItem','Inventory','EquipmentGrid','Main','Reserve','Worn','Overflow','AttackPower','Container'}
MODES={'accessory','arms','main','board-insufficient','legal-swap','illegal-swap'}
rows=[]; files=[]; identities=[]; summaries=[]; current='global'; final_batch=None
def check(name,ok,detail='',level='independent raw'):
    rows.append(dict(mode=current,check=name,pass_=bool(ok),level=level,detail=str(detail)))
def sha(b): return hashlib.sha256(b).hexdigest()
def load(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def lines(p): return [json.loads(x) for x in p.read_text(encoding='utf-8-sig').splitlines() if x.strip()]
def bits(n): return struct.pack('<f',float(n)).hex()
def single_equal(a,b): return bits(a)==bits(b)
def fnv(s):
    h=14695981039346656037
    raw=s.encode('utf-16-le',errors='surrogatepass')
    for i in range(0,len(raw),2): h=((h ^ int.from_bytes(raw[i:i+2],'little'))*1099511628211)&((1<<64)-1)
    return '%016x'%h
def raw_members(s):
    # Preserve exact serialized random/save substrings, not a reserialization.
    dec=json.JSONDecoder(); i=s.index('{')+1; out={}
    while True:
        while s[i].isspace() or s[i]==',': i+=1
        if s[i]=='}': return out
        key,j=dec.raw_decode(s,i); i=j
        while s[i].isspace() or s[i]==':': i+=1
        start=i; _,i=dec.raw_decode(s,i); out[key]=s[start:i]
@lru_cache(maxsize=None)
def asset(kind,id):
    p=ROOT/'Assets/CombatPrototype/Resources'/kind/(id+'.asset')
    t=p.read_text(encoding='utf-8-sig')
    files.append(dict(mode='immutable-definition',path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=sha(p.read_bytes()),manifestMatch=None))
    def val(k): return re.search(r'^  '+k+r': (.*)$',t,re.M).group(1)
    def cells(k):
        s=val(k)
        if s=='[]': return []
        block=re.search(r'^  '+k+r':([^\n]*(?:\n(?!  [A-Za-z_])[^\n]*)*)',t,re.M).group(1)
        pairs=re.findall(r'x: (-?\d+)[,\s]+y: (-?\d+)',block)
        if not pairs: raise ValueError('Unparsed nonempty cell array: '+str(p)+' '+k)
        return [dict(x=int(x),y=int(y)) for x,y in pairs]
    return dict(width=int(val('width')),height=int(val('height')),cells=cells('occupiedCells' if kind=='ItemData' else 'blockedCells'))
def local_cells(item,rotation=None):
    f=item['fields']; d=item['definition']; r=f['rotation'] if rotation is None else rotation
    if f['widthOverride']>0: w,h=f['widthOverride'],f['heightOverride']; cs=[]
    else:
        w,h=d['width'],d['height']; cs=d['occupiedCells']
        a=asset('ItemData',f['definitionId'])
        check('definition-source-geometry',a==dict(width=w,height=h,cells=cs),f['definitionId'])
    pts=[(p['x'],p['y']) for p in cs] or [(x,y) for y in range(h) for x in range(w)]
    return [(h-1-y,x) if r==1 else (w-1-x,h-1-y) if r==2 else (y,w-1-x) if r==3 else (x,y) for x,y in pts]
def allowed(d):
    a=asset('ContainerData',d['definitionId'])
    check('container-source-geometry',a==dict(width=d['width'],height=d['height'],cells=d['blockedCells']),d['definitionId'])
    return {(x,y) for y in range(a['height']) for x in range(a['width'])}-{(p['x'],p['y']) for p in a['cells']}
def index(items): return {i['fields']['id']:i for i in items}
def geometry(items,containers,label):
    used={True:{},False:{}}; legal={True:allowed(containers['rig']),False:allowed(containers['bag'])}
    for i in items:
        f=i['fields']; cells=local_cells(i)
        check('item-derived-cells',i['cells']==[list(p) for p in cells],label+' '+f['id'])
        if f['worn'] or f['overflow']: continue
        for x,y in cells:
            p=(x+f['x'],y+f['y']); board=f['board']
            check('geometry-allowed-no-overlap',p in legal[board] and p not in used[board],label+' '+f['id']+' '+str(p))
            used[board][p]=f['id']
    return used,legal
def state(s,label):
    c=s['canonical']; check('nine-domain-set',set(c)==DOMAINS,label)
    for k,v in c.items(): check('UTF16-FNV-'+k,fnv(v)==s['fingerprints'].get(k),label)
    d={k:json.loads(v) for k,v in c.items()}; its=s['itemsOrdered']; ix=index(its)
    check('unique-owned-IDs',len(ix)==len(its),label)
    ordered=sorted(its,key=lambda i:i['fields']['id'].encode('utf-16-be'))
    check('GearItem-raw-vs-itemsOrdered',d['GearItem']==ordered,label)
    check('Inventory-order',d['Inventory']['gearItemOrder']==[i['fields']['id'] for i in its],label)
    check('Inventory-warehouse',d['Inventory']['warehouseItems']==s['warehouse'],label)
    for k in ['Main','Reserve']:
        q=d[k]; check(k+'-exact-item',q['item']==ix.get(q['id']),label)
    for k,flag in [('Worn','worn'),('Overflow','overflow')]:
        check(k+'-exact-members',d[k]==[i for i in ordered if i['fields'][flag]],label)
    grid=[]
    for i in ordered:
        f=i['fields']; entry={k:f[k] for k in ['id','x','y','rotation','board','worn','overflow']}
        entry['cells']=[[x+f['x'],y+f['y']] for x,y in local_cells(i)]
        grid.append(entry)
        check('derived-flags',i['inBag']==(not f['board'] and not f['worn'] and not f['overflow']) and i['container']==(f['type'] in [9,10]),label)
        if f['dataRevision']>0:
            check('derived-attack-Single',single_equal(i['attack'],f['savedAttack']) and single_equal(i['defense'],f['savedDefense']),label)
    check('EquipmentGrid-reconstruction',grid==d['EquipmentGrid'],label)
    for sf in s['saveFiles']:
        b=base64.b64decode(sf['base64'],validate=True)
        check('save-base64-SHA-bytes',len(b)==sf['bytes'] and sha(b)==sf['sha256'],label+' '+sf['relativePath'])
    ap=d['AttackPower']; snap=ap['snapshot']
    for a,b in [('attackPower','attackPower'),('basicPower','basicPower'),('loadoutAttack','loadoutAttack'),('loadoutDefense','loadoutDefense'),('progressionBonus','progressionBonus')]:
        check('actual-snapshot-Single-'+a,single_equal(ap[a],snap[b]),label)
    check('Strength3',ap['strengthRank']==3 and single_equal(ap['progressionBonus'],15),label)
    geometry(its,d['Container'],label)
    return d

def audit_gates(p,changes,events,source):
    gates=lines(p/'original-root/measurement-gates.jsonl')
    check('two-natural-measurement-gates',len(gates)==2 and {g['operation'] for g in gates}=={'UI-Evaluate','UI-Commit'},level='natural autosave raw')
    rawg=(p/'original-root/measurement-gates.jsonl').read_text(encoding='utf-8-sig').splitlines()
    rawc=(p/'original-root/state-changes.jsonl').read_text(encoding='utf-8-sig').splitlines()
    # Strip string literals/comments before looking for forbidden calls/assignments.
    code=re.sub(r'"(?:[^"\\]|\\.)*"','""',source)
    code=re.sub(r'//[^\n]*|/\*.*?\*/','',code,flags=re.S)
    check('gate-source-no-save-or-clock-writes',not re.search(r'\.SaveProgress\s*\(|(?:autoSaveInterval|nextSave|LastSavedAt|timeScale|fixedDeltaTime|session\.Saves\.enabled)\s*=(?!=)|SetValue\s*\(',code),'Source read-only timer reflection; no save call/clock/interval/state writes','source review')
    previous_boundary=None
    for n,g in enumerate(gates):
        op=g['operation']; a=g['timerBefore']; b=g['timerAfter']
        check('gate-natural-timer-advance',b['lastSavedAt']>a['lastSavedAt'] and b['lastSavedAt']>=a['nextSaveReadonly'] and b['unscaledTime']>=b['lastSavedAt'] and b['realtime']>=a['realtime'],op,'natural autosave raw')
        check('gate-interval5-no-focus-change',single_equal(a['autoSaveIntervalReadonly'],5) and single_equal(b['autoSaveIntervalReadonly'],5) and a['focusEpoch']==b['focusEpoch'] and a['focused']==b['focused'] and 4.99 <= b['nextSaveReadonly']-b['lastSavedAt'] <= 5.01,op,'natural autosave raw')
        if previous_boundary is not None: check('successive-gates-advance',b['lastSavedAt']>previous_boundary,op,'natural autosave raw')
        previous_boundary=b['lastSavedAt']
        for side in ['saveFilesBefore','saveFilesAfter']:
            for sf in g[side]:
                data=base64.b64decode(sf['base64'],validate=True)
                check('gate-save-base64-SHA-bytes',len(data)==sf['bytes'] and sha(data)==sf['sha256'],op+' '+side+' '+sf['relativePath'],'natural autosave raw')
        check('gate-natural-save-really-changed-files',g['saveFilesBefore']!=g['saveFilesAfter'],op,'natural autosave raw')
        operations=[(k,c) for k,c in enumerate(changes) if c['tag']==op]
        check('gate-one-operation',len(operations)==1,op,'natural autosave raw')
        if len(operations)!=1: continue
        k,c=operations[0]; rawop=raw_members(rawc[k]); rg=raw_members(rawg[n])
        for side in ['before','after']:
            t=c[side]['saveTimer']
            check('operation-same-natural-boundary-SavedAt',single_equal(t['lastSavedAt'],b['lastSavedAt']) and single_equal(t['nextSaveReadonly'],b['nextSaveReadonly']) and t['focusEpoch']==b['focusEpoch'] and t['focused']==b['focused'] and single_equal(t['autoSaveIntervalReadonly'],5) and b['lastSavedAt']<=t['unscaledTime']<b['nextSaveReadonly'],op+' '+side,'natural autosave raw')
        rb=raw_members(rawop['before'])
        check('gate-after-to-operation-before-save-verbatim',rg['saveFilesAfter']==rb['saveFiles'],op,'natural autosave raw')
        waits=[i for i,x in enumerate(events) if x['kind']=='natural-autosave-gate-wait' and x['detail'].startswith(op+' ')]
        seen=[i for i,x in enumerate(events) if x['kind']=='natural-autosave-gate-observed' and x['detail'].startswith(op+' ')]
        check('gate-input-wait-observed-once',len(waits)==len(seen)==1 and waits[0]<seen[0],op,'natural autosave raw')
        if len(waits)==len(seen)==1:
            end=[i for i,x in enumerate(events) if i>seen[0] and x['kind']=='mouse-up' and x['detail'].startswith('ReplacementPreview:'+op[3:]+' ')]
            check('gate-no-focus-or-pause-through-operation',bool(end) and not any(x['kind'] in ['application-focus','application-pause'] for x in events[waits[0]:end[0]+1]),op,'natural autosave raw')

def audit_run(p):
    global current
    m=load(p/'run-manifest.json'); current=m['mode']; r=load(p/'original-root/result.json'); start=load(p/'process-start.json'); receipt=load(p/'build-receipt.json'); cmd=load(p/'Player.command.json')
    identities.append({k:r[k] for k in ['runId','mode','buildId','pid','productDLLSHA256','driverSHA256','exeSHA256']})
    check('designated-final-batch-original',p.parent.name==final_batch,str(p))
    if final_batch=='UI-A07':
        check('designated-A07-driver',r['driverSHA256']=='0c44b9c626cbe8d7fa27c83d6369a98c4cb112486e0859713ee57805e719fd45')
    if final_batch=='UI-A05':
        check('designated-A05-build-driver',r['buildId']=='ux04b2r2fix-ab3d5ba4-b70442f9-cf2b8de1' and r['driverSHA256']=='cf2b8de1b7ff2844ee7b724caacffa50e567532d4f338b8bb008aea8911010df')
    # Hash every manifest member, and account for unlisted members independently.
    manifest_files=m['files']
    for name,rec in manifest_files.items():
        q=p/name; b=q.read_bytes(); ok=len(b)==rec['bytes'] and sha(b)==rec['sha256']
        files.append(dict(mode=current,path=str(q.relative_to(ROOT)),bytes=len(b),sha256=sha(b),manifestMatch=ok))
        check('manifest-file-SHA-bytes',ok,name)
    actual={q.relative_to(p).as_posix() for q in p.rglob('*') if q.is_file()}
    check('manifest-complete-file-set',actual==set(manifest_files)|{'run-manifest.json'},str(actual-set(manifest_files)-{'run-manifest.json'}))
    mb=(p/'run-manifest.json').read_bytes(); files.append(dict(mode=current,path=str((p/'run-manifest.json').relative_to(ROOT)),bytes=len(mb),sha256=sha(mb),manifestMatch=None))
    for key in ['runId','mode','buildId','driverSHA256','exeSHA256']:
        check('identity-'+key,len({z[key] for z in [m,r,start,cmd]})==1,r[key])
    check('PID-binding',m['pid']==r['pid']==start['pid'] and r['pid']>0,r['pid'])
    product=sha((p/'Assembly-CSharp.input.dll').read_bytes()); driver=sha((p/'B2R2FixReplacementDriver.dll').read_bytes())
    check('product-DLL-identity',product==EXPECTED==r['productDLLSHA256']==m['dllSHA256']==receipt['productDLLSHA256'],product)
    check('driver-DLL-identity',driver==r['driverSHA256']==receipt['driverSHA256'],driver)
    exe=Path(cmd['arguments'][0]); check('executable-identity',sha(exe.read_bytes())==r['exeSHA256'],str(exe))
    source=(p/'ReplacementDriver.compiled.cs').read_text(encoding='utf-8-sig')
    check('driver-source-receipt',sha((p/'ReplacementDriver.compiled.cs').read_bytes())==receipt['executedSourceSHA256'])
    check('no-programmatic-click',not re.search(r'onClick\s*\.\s*Invoke|ExecuteEvents\s*\.',source),'compiled source lexical + reviewed Click coroutine','source review')
    check('physical-input-source',all(s in source for s in ['es.RaycastAll','InputSystem.QueueStateEvent','MouseButton.Left','InputSystemUIInputModule']),level='source review')
    check('standalone-Mono',r['isMono'] and not r['isEditor'] and m['exitCode']==0 and not m['timedOut'])
    changes=lines(p/'original-root/state-changes.jsonl'); obs=lines(p/'original-root/observations.jsonl'); events=lines(p/'original-root/input-events.jsonl')
    audit_gates(p,changes,events,source)
    for q in obs: check('observation-identity',q['runId']==m['runId'] and q['mode']==current and q['buildId']==m['buildId'])
    for n,q in enumerate(obs):
        if q['state']: state(q['state'],'observation '+str(n))
    raw=(p/'original-root/state-changes.jsonl').read_text(encoding='utf-8-sig').splitlines()
    for n,q in enumerate(changes):
        a=state(q['before'],q['tag']+' before'); b=state(q['after'],q['tag']+' after')
        if q['tag']!='UI-Commit' or not q['evaluation']['feasible']:
            check('query-or-failed-commit-nine-exact',q['before']['canonical']==q['after']['canonical'],q['tag'])
            z=raw_members(raw[n]); ba=raw_members(z['before']); bb=raw_members(z['after'])
            for k in ['random','saveFiles']: check('query-or-failed-commit-'+k+'-verbatim',ba[k]==bb[k],q['tag'])
    ui=[q for q in changes if q['tag']=='UI-Evaluate']; commits=[q for q in changes if q['tag']=='UI-Commit']
    check('one-Evaluate-one-Commit',len(ui)==len(commits)==1)
    if len(ui)!=1 or len(commits)!=1: return
    q=ui[0]; co=commits[0]; e=q['evaluation']; req=q['request']; bef=q['before']; aft=co['after']; ib=index(bef['itemsOrdered']); ia=index(aft['itemsOrdered'])
    cid,oid=e['candidateGearId'],e['replacedGearId']; check('machine-request-complete',all(k in req for k in ['candidateGearId','replacedGearId','target','rotation','role','roleValue']) and set(req['target'])=={'x','y'})
    check('machine-request-exact-IDs-role',req['candidateGearId']==cid and req['replacedGearId']==oid and req['roleValue']==e['role'] and cid!=oid and cid in ib and oid in ib)
    check('evaluate-commit-continuity',bef['canonical']==co['before']['canonical'] and co['request']==req)
    before_snap=json.loads(bef['canonical']['AttackPower'])['snapshot']
    for key,value in before_snap.items():
        check('prediction-before-actual-'+key,(value==e['before'][key]) if key in ['weaponType','activeCount'] else single_equal(value,e['before'][key]))
    check('request-scenario-role-target',req['role']==('Main' if current=='main' else 'Board') and req['rotation']==(1 if current=='board-insufficient' else 0) and (req['target']==dict(x=ib[cid]['fields']['x'],y=ib[cid]['fields']['y']) if current=='main' else req['target']==dict(x=0,y=2)))
    expected=current not in {'board-insufficient','illegal-swap'}
    check('independent-expected-feasibility',e['feasible']==expected)
    actual_ap=json.loads(aft['canonical']['AttackPower'])
    summaries.append(dict(mode=current,request=req,feasible=e['feasible'],reason=e['reason'],oldContribution=e['oldContribution'],newContribution=e['newContribution'],oldContributionAfter=e['oldContributionAfter'],newContributionBefore=e['newContributionBefore'],actualAP=actual_ap['attackPower'],actualAPSingleLE=bits(actual_ap['attackPower']),projectedAP=e['after']['attackPower'],projectedAPSingleLE=bits(e['after']['attackPower']),ownedIDsBefore=len(ib),ownedIDsAfter=len(ia),rawChanges=len(changes),additionalAPIQueries=sum(c['tag'].startswith('ADDITIONAL-API-') for c in changes),inputEvents=len(events)))
    controls=['Open','ModeReplace','Role:'+req['role'],'Candidate:'+cid,'Replaced:'+oid,'Evaluate','Commit','Close']
    if req['role']=='Board': controls+=['XPlus','XMinus','YPlus','YMinus']
    if req['rotation']: controls+=['Rotate']
    for control in controls:
        name='ReplacementPreview:'+control; matched=[]
        for n,event in enumerate(events):
            if event['kind']=='ugui-raycast' and event['detail'].startswith(name+' '):
                trio=events[n:n+3]
                if len(trio)==3 and 'accepted=True interactable=True' in event['detail'] and [x['kind'] for x in trio]==['ugui-raycast','mouse-down','mouse-up'] and all(x['detail'].startswith(name+' ') for x in trio): matched.append(trio)
        check('physical-accepted-down-up-'+control,bool(matched),name,'EventSystem/input raw')
    if expected:
        check('projection-unique-ID-multiset',collections.Counter(i['fields']['id'] for i in e['projectedItemsComplete'])==collections.Counter(i['fields']['id'] for i in bef['itemsOrdered']))
        check('actual-projection-full-fields', {k:v['fields'] for k,v in ia.items()}=={k:v['fields'] for k,v in index(e['projectedItemsComplete']).items()})
        check('actual-ID-multiset-preserved',collections.Counter(i['fields']['id'] for i in bef['itemsOrdered'])==collections.Counter(i['fields']['id'] for i in aft['itemsOrdered']))
        da={k:json.loads(v) for k,v in aft['canonical'].items()}; db={k:json.loads(v) for k,v in bef['canonical'].items()}
        for prop in ['attackPower','basicPower','loadoutAttack','loadoutDefense']:
            check('prediction-actual-Single-'+prop,single_equal(da['AttackPower'][prop],e['after'][prop]),bits(da['AttackPower'][prop])+'='+bits(e['after'][prop]))
        check('actual-main-reserve-projection',da['Main']['id']==e['projectedMainId'] and da['Reserve']['id']==e['projectedReserveId'])
        for key,value in da['AttackPower']['snapshot'].items():
            check('prediction-after-actual-'+key,(value==e['after'][key]) if key in ['weaponType','activeCount'] else single_equal(value,e['after'][key]))
        active=lambda its,main:{id for id,i in its.items() if not i['fields']['worn'] and not i['fields']['overflow'] and (i['fields']['board'] or id==main)}
        pre=active(ib,db['Main']['id']); post=active(ia,da['Main']['id'])
        check('exact-old-exits-new-enters',pre-post=={oid} and post-pre=={cid})
        check('selected-contribution-identity',single_equal(e['oldContribution'],ib[oid]['attack']) and single_equal(e['newContribution'],ib[cid]['attack']) and single_equal(e['oldContributionAfter'],0) and single_equal(e['newContributionBefore'],0))
        for id in ib:
            nonpos=lambda f:{k:v for k,v in f.items() if k not in ['x','y','rotation','board','worn','overflow']}
            check('non-position-state-preserved',nonpos(ib[id]['fields'])==nonpos(ia[id]['fields']),id)
            if id not in [cid,oid]: check('other-items-including-companions-unchanged',ib[id]==ia[id],id)
        if current=='main': check('normalMain-no-physical-move',all(ib[id]['fields']==ia[id]['fields'] for id in ib))
        else:
            f=ia[cid]['fields']; check('actual-request-placement',f['x']==req['target']['x'] and f['y']==req['target']['y'] and f['rotation']==req['rotation'] and f['board'])
            old=ia[oid]['fields']; src=ib[cid]['fields']
            check('old-real-ID-returned-to-source',ia[oid]['inBag'] and old['x']==src['x'] and old['y']==src['y'] and old['rotation']==ib[oid]['fields']['rotation'])
        check('fixture-container-not-body-bonus',single_equal(db['AttackPower']['snapshot']['containerBonus'],0),'UI fixture container bonus0; separate Worn API projection bonus6','UI normal behavior')
    d={k:json.loads(v) for k,v in bef['canonical'].items()}; used,allow=geometry(bef['itemsOrdered'],d['Container'],'UI pre geometric proof')
    if current=='board-insufficient':
        target={(x+req['target']['x'],y+req['target']['y']) for x,y in local_cells(ib[cid],req['rotation'])}
        collision={used[True].get(p) for p in target}-{None,oid}
        check('D-full-board',set(used[True])==allow[True],len(used[True]))
        check('D-target-in-bounds-other-collision',target<=allow[True] and bool(collision),str(sorted(target))+' collision='+str(collision))
    if current=='legal-swap':
        src=ib[cid]['fields']; old=ib[oid]
        returned={(x+src['x'],y+src['y']) for x,y in local_cells(old,old['fields']['rotation'])}
        check('E-legal-source-exchange-independent',returned<=allow[False] and all(used[False].get(p) in [None,cid] for p in returned),str(sorted(returned)))
    if current=='illegal-swap':
        src=ib[cid]['fields']; old=ib[oid]
        returned={(x+src['x'],y+src['y']) for x,y in local_cells(old,old['fields']['rotation'])}
        target={(x+req['target']['x'],y+req['target']['y']) for x,y in local_cells(ib[cid],req['rotation'])}
        check('F-target-otherwise-legal-selected-collision',target<=allow[True] and {used[True].get(p) for p in target}-{None}=={oid},str(sorted(target)))
        outside=returned-allow[False]
        check('F-return-swap-out-of-bounds-independent',bool(outside),str(sorted(outside)))
    api={x['tag']:x for x in changes if x['tag'].startswith('ADDITIONAL-API-')}
    for label in ['Reserve0','Worn-and-container-nonzero','BoardAdd-CanPlaceScan','BoardAdd-empty-or-full']:
        check('additional-API-present-'+label,'ADDITIONAL-API-'+label in api,level='ADDITIONAL API only')
    add=api.get('ADDITIONAL-API-BoardAdd-empty-or-full')
    if add:
        ev=add['evaluation']; olditems=add['before']['itemsOrdered']; oldix=index(olditems); ad={k:json.loads(v) for k,v in add['before']['canonical'].items()}; au,al=geometry(olditems,ad['Container'],'ADDITIONAL BoardAdd')
        empty=al[True]-set(au[True])
        check('API-BoardAdd-feasibility-independent',ev['feasible']==bool(empty),str(len(empty))+' legal empty cells','ADDITIONAL API only')
        if ev['feasible']:
            pi=index(ev['projectedItemsComplete']); aid=ev['candidateGearId']
            check('API-BoardAdd-preserves-owned-IDs',set(pi)==set(oldix) and len(pi)==len(ev['projectedItemsComplete']),level='ADDITIONAL API only')
            check('API-BoardAdd-preserves-other-full-items',all(pi[id]==i for id,i in oldix.items() if id!=aid),level='ADDITIONAL API only')
            check('API-BoardAdd-not-replace',not ev['replacedGearId'] and ev['after']['activeCount']==ev['before']['activeCount']+1 and pi[aid]['fields']['board'],level='ADDITIONAL API only')
            geometry(ev['projectedItemsComplete'],ad['Container'],'ADDITIONAL BoardAdd projection')
    reserve=api.get('ADDITIONAL-API-Reserve0')
    if reserve:
        ev=reserve['evaluation']; check('API-Reserve0',single_equal(ev['after']['reserveContribution'],0) and single_equal(ev['deltaAttackPower'],0),level='ADDITIONAL API only')
    worn=api.get('ADDITIONAL-API-Worn-and-container-nonzero')
    if worn:
        ev=worn['evaluation']; wi=index(ev['projectedItemsComplete'])[ev['candidateGearId']]
        check('API-Worn-body0-not-slot6',single_equal(ev['itemAttack'],0) and single_equal(wi['attack'],0) and wi['fields']['worn'] and single_equal(ev['newContribution'],6) and single_equal(ev['after']['containerBonus'],6) and single_equal(ev['after']['progressionBonus'],15) and single_equal(ev['deltaAttackPower'],6),'body Attack=0; container slot Contribution=6; Strength bonus=15','ADDITIONAL API only')
    authority=[x for x in obs if x['stage']=='authority-actual-reserve-worn-overflow']
    check('API-actual-authority-present',len(authority)==1,level='ADDITIONAL API only')
    if authority:
        sd=authority[0]['state']; aa={k:json.loads(v) for k,v in sd['canonical'].items()}; reserveid=aa['Reserve']['id']; ax=index(sd['itemsOrdered'])
        check('API-actual-Reserve0',reserveid in ax and ax[reserveid]['attack']>0 and single_equal(aa['AttackPower']['snapshot']['reserveContribution'],0),level='ADDITIONAL API only')
        check('API-actual-Overflow-positive-body',any(i['fields']['overflow'] and i['attack']>0 and not i['fields']['board'] and not i['fields']['worn'] for i in ax.values()),level='ADDITIONAL API only')
        strength=[x for x in obs if x['stage']=='authority-strength']
        check('API-Reserve-Overflow-actual-AP-unchanged',len(strength)==1 and single_equal(json.loads(strength[0]['state']['canonical']['AttackPower'])['attackPower'],aa['AttackPower']['attackPower']),level='ADDITIONAL API only')

def main():
    global current,final_batch
    ap=argparse.ArgumentParser(); ap.add_argument('--batch',required=True,help='Final batch explicitly designated by lead'); ap.add_argument('runs',nargs='+',type=Path); args=ap.parse_args(); final_batch=args.batch
    check('six-final-runs',len(args.runs)==6)
    seen=[]
    for p in args.runs:
        p=p.resolve()
        try:
            seen.append(load(p/'run-manifest.json')['mode']); audit_run(p)
        except Exception as ex: check('oracle-exception',False,repr(ex))
    current='global'; check('six-unique-modes',set(seen)==MODES and len(seen)==6)
    check('all-six-unified-build-driver',len(identities)==6 and len({(z['buildId'],z['productDLLSHA256'],z['driverSHA256'],z['exeSHA256']) for z in identities})==1)
    check('six-distinct-runIds-PIDs',len({z['runId'] for z in identities})==6 and len({z['pid'] for z in identities})==6)
    ff=load(FIX/'EVIDENCE/FLOAT-FINAL.json')
    check('existing-Mono-FLOAT-FINAL',ff['ULP']==0 and ff['cases']==7 and ff['actualCasePrefixComparisons']==24 and ff['allPrefixesBitwiseEqual'],'Existing Mono record only, no rerun / no Python R03 arithmetic','existing actual Mono')
    fails=[x for x in rows if not x['pass_']]; counts={}
    for mode in sorted(set(x['mode'] for x in rows)):
        rr=[x for x in rows if x['mode']==mode]; counts[mode]=dict(checks=len(rr),failed=sum(not x['pass_'] for x in rr),levels=dict(collections.Counter(x['level'] for x in rr)))
    report=dict(verdict='FAIL' if fails else 'PASS',scope='Independent raw artifact consistency oracle, not host OS attestation. No Unity execution. No runner import or trust of PASS flags.',failures=fails,statistics=counts,identities=identities,summaries=summaries,files=files,checks=rows,history='UI-A01 accessory verifier Worn expectation 0 failed; UI-A02 accessory/arms/main succeeded; D wheel120 could not reach old control and did not Evaluate. UI-A03 first three succeeded; D wheel8 still overshot (1296px/tick), no Evaluate, not product capacity failure. A04-PROBE quarterwheel D accepted (reported PID7972/exit0); a probe, not the unified final six. A05 first five reported PASS; F original FAIL must remain FAIL: all nine canonical and random unchanged but save bytes changed (revision1 to2 and new .bak) during natural 5-second unscaled autosave. Source CombatSaveSystem.LateUpdate independently confirms autonomous save; ApplyEquipment returns before mutation on projection failure. This timing explanation does not waive byte-level atomicity or promote A05 F to PASS. A06 was a natural-save-boundary F probe, not final acceptance. Historical A01/A02/A03/A04-PROBE/A05/A06-PROBE immutable, not final six.',floatFinal=ff)
    out=FIX/'EVIDENCE'; out.mkdir(exist_ok=True)
    (out/'REPLACEMENT_ORACLE.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    with (out/'REPLACEMENT_ORACLE.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['mode','check','pass_','level','detail']);w.writeheader();w.writerows(rows)
    text=['# REPLACEMENT ORACLE', '', '## Problems first', '']
    text+=['- '+x['mode']+' / '+x['check']+': '+x['detail'] for x in fails] or ['No independent-oracle failures.']
    text+=['','Verdict: **'+report['verdict']+'**','','## Method and limits','- Independently recomputed per-file SHA/bytes, UTF16 code-unit FNV, domain/raw links, save base64, exact query immutability, Single bits, full-field projection, ID/state preservation and asset-derived spatial constraints.','- UI EventSystem accepted raycast + down/up is separated from supplemental API probes. Source is reviewed read-only; raw logs are observations, not externally authenticated OS telemetry.','- Worn item body Attack=0 is distinct from container slot Contribution=6. Strength3 gives progressionBonus=15. Reserve and Overflow body attack do not imply active contribution.','- Natural save gates: independently validate timer advancement, fixed interval5, unchanged focus epoch, gate save base64/SHA, gate-after to operation-before exact bytes and both operation snapshots SavedAt matching the same natural boundary. Different saves are never ignored.','- Existing FLOAT-FINAL: Mono seven cases / 24 prefixes / ULP0; no new product execution or Python numerical R03 oracle.','','## Six-mode evidence levels','|Mode|Checks|Failures|Levels|','|---|---:|---:|---|']
    for mode,n in counts.items(): text.append('|'+mode+'|'+str(n['checks'])+'|'+str(n['failed'])+'|'+json.dumps(n['levels'],ensure_ascii=False)+'|')
    text+=['','## Exact UI requests and actual outcomes','Single bytes below are little-endian IEEE754 binary32 reconstructed only from serialized Mono values.','|Mode|Exact replaced ID → candidate ID|target / rotation / role|feasible|actual AP / projected AP bits|','|---|---|---|---|---|']
    for z in summaries:
        rq=z['request']; text.append('|'+z['mode']+'|'+rq['replacedGearId']+' → '+rq['candidateGearId']+'|'+str(rq['target'])+' / '+str(rq['rotation'])+' / '+rq['role']+'|'+str(z['feasible'])+'|'+str(z['actualAP'])+' / '+(z['projectedAPSingleLE'] if z['feasible'] else 'N/A: rejected')+'|')
    text+=['','## Independent geometric failure proofs']
    for rr in rows:
        if rr['check'] in ['D-full-board','D-target-in-bounds-other-collision','F-return-swap-out-of-bounds-independent','E-legal-source-exchange-independent']:
            text.append('- '+rr['mode']+' / '+rr['check']+': '+rr['detail'])
    text+=['','## Final run identities','|Mode|runId|PID|buildId|','|---|---|---:|---|']
    for z in identities: text.append('|'+z['mode']+'|'+z['runId']+'|'+str(z['pid'])+'|'+z['buildId']+'|')
    text+=['','Product SHA: '+EXPECTED,'','Driver SHA: '+(identities[0]['driverSHA256'] if identities else 'missing'),'','## Immutable history',report['history'],'','Complete rows and digests: [JSON](<I:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/EVIDENCE/REPLACEMENT_ORACLE.json>) / [CSV](<I:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R2FIX/EVIDENCE/REPLACEMENT_ORACLE.csv>).']
    (out/'REPLACEMENT_ORACLE.md').write_text('\n'.join(text)+'\n',encoding='utf-8')
    print(json.dumps(dict(verdict=report['verdict'],failures=fails,statistics=counts),ensure_ascii=False,indent=2))
    return 1 if fails else 0
if __name__=='__main__': raise SystemExit(main())
