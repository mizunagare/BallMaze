"""Stdlib-only static audit. Writes only beside this script; no driver import or Player launch."""
import pathlib,json,hashlib,re,csv,collections
ROOT=pathlib.Path.cwd(); OUT=pathlib.Path(__file__).resolve().parent
R=ROOT/'Evidence/Runs04B2R1/SESSION-20261116-1115/A03'
def read(p):return p.read_text(encoding='utf-8-sig')
def js(p):return json.loads(read(p))
def jl(p):return [json.loads(l) for l in read(p).splitlines() if l.strip()]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(n,o): (OUT/n).write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding='utf-8')
def link(p,line=None):return '<'+p.resolve().as_posix()+(('#L'+str(line)) if line else '')+'>'
def ids(raw):return [x['id'] for x in raw.get('items',[])+raw.get('warehouse',[])]
def identity(x):return {k:v for k,v in x.items() if k not in ['x','y','rotation','overflow','worn','board']}
D={}; hashes=[]; runs=[]; facts=[]; checks=[]; directories=[]
for p in sorted(R.iterdir()):
 if not p.is_dir():continue
 m=p.name; mf=js(p/'run-manifest.json'); result=js(p/'result.json'); cmd=js(p/'Player.command.json'); obs=jl(p/'r1-observations.jsonl'); inp=jl(p/'r1-input-events.jsonl'); st=jl(p/'r1-state-changes.jsonl')
 D[m]=dict(p=p,mf=mf,result=result,cmd=cmd,obs=obs,inp=inp,st=st)
 bad=[]
 allfiles=[]
 for f in sorted(p.rglob('*')):
  if not f.is_file():continue
  rel=f.relative_to(p).as_posix(); source=pathlib.Path(mf['runRoot'])/rel
  allfiles.append(dict(path=rel,bytes=f.stat().st_size,sha256=sha(f),inManifest=rel in mf['files'],sourceExists=source.exists(),sourceEqual=sha(source)==sha(f) if source.exists() else None))
 tree='\n'.join(v['path']+'\t'+str(v['bytes'])+'\t'+v['sha256'] for v in allfiles)
 directories.append(dict(mode=m,files=allfiles,treeSHA256=hashlib.sha256(tree.encode('utf-8')).hexdigest(),algorithm='SHA256 of UTF8 newline-joined path TAB bytes TAB SHA256; paths sorted by pathlib',sourceDifferences=[v['path'] for v in allfiles if v['sourceExists'] and not v['sourceEqual']],unlisted=[v['path'] for v in allfiles if not v['inManifest']]))
 for n,v in mf['files'].items():
  f=p/n; actual=sha(f) if f.exists() else None; ok=actual==v['sha256'] and f.stat().st_size==v['bytes'] if f.exists() else False
  hashes.append(dict(mode=m,path=f.relative_to(ROOT).as_posix(),actual=actual,expected=v['sha256'],ok=ok))
  if not ok:bad.append(n)
 exe=pathlib.Path(cmd['exe']); managed=exe.parent/(exe.stem+'_Data')/'Managed'
 for f,key in [(exe,'exeSHA256'),(managed/'Assembly-CSharp.dll','dllSHA256'),(managed/'B2R1ObservationDriver.dll','driverDllSHA256')]:
  actual=sha(f) if f.exists() else None;ok=actual==mf[key];hashes.append(dict(mode=m,path=f.relative_to(ROOT).as_posix(),actual=actual,expected=mf[key],ok=ok))
  if not ok:bad.append(key)
 rid='UX04B2R1-A03-'+m
 identity_ok=mf['runId']==result['runId']==cmd['runId']==read(p/'r1-run-id.txt').strip()==rid and mf['mode']==result['mode']==cmd['mode']==read(p/'r1-mode.txt').strip()==m and all(o['runId']==rid and o['mode']==m for o in obs)
 build_ok=mf['buildId']==cmd['buildId']=='ux04b2r1-'+mf['dllSHA256'][:8]+'-'+mf['exeSHA256'][:8]+'-'+mf['driverDllSHA256'][:8]
 ct=len(result['detail']); oc=[o for o in obs if o.get('stage')=='check']
 consistency=ct==result['checks']==result['passed']==len(oc) and result['failed']==0 and all(x['result']=='PASS' for x in result['detail']) and mf['resultJson']==result
 runs.append(dict(mode=m,runId=rid,pid=mf['pid'],exitCode=mf['exitCode'],buildId=mf['buildId'],identity_ok=identity_ok,build_ok=build_ok,hash_bad=bad,checks=ct,observation_checks=len(oc),consistency=consistency,evidenceDir_ok=pathlib.Path(mf['evidenceDir']).resolve()==p.resolve(),root=mf['runRoot'],complete=read(p/'r1-complete.txt').strip(),process_ok=mf['exitCode']==0 and not mf['timedOut'] and not mf['forcedTermination']))
def fact(m,name,ok,detail,lines=None):
 f=dict(mode=m,name=name,ok=bool(ok),detail=detail,lines=lines or []);facts.append(f);return f
for m,d in D.items():
 for ln,o in enumerate(d['obs'],1):
  raw=o.get('raw')
  if not raw:continue
  if m in ['strength0','strength3','golden']:
   main=next((x for x in raw['items'] if x['id']==raw['main']),None);gear=main['derivedAttack'] if main else 0
   expected=raw['baseDamage']+gear+raw['rank']*5+raw['rig']['attackBonus']+raw['bag']['attackBonus']
   fact(m,'raw-ap@'+str(ln),raw['bonus']==raw['rank']*5 and raw['attackPower']==expected and raw['basicPower']==expected,dict(rank=raw['rank'],bonus=raw['bonus'],gear=gear,base=raw['baseDamage'],ap=raw['attackPower'],expected=expected),[ln])
  if 'evaluationJson' in o and m.startswith('strength'):
   e=json.loads(o['evaluationJson']);c=json.loads(o['candidateJson']);rank=int(m[-1]); exp=raw['baseDamage']+c['derivedAttack']+rank*5
   fact(m,'preview-chain',e['before']['attackPower']==raw['attackPower'] and e['after']['attackPower']==exp and e['deltaAttackPower']==exp-raw['attackPower'],dict(candidate=c['id'],candidateAttack=c['derivedAttack'],rank=rank,expectedAfter=exp,before=e['before']['attackPower'],after=e['after']['attackPower']),[ln])
  if o.get('stage')=='sort' and 'publishedIds' in o:
   a=raw['items'];key=o['sortKey'];ordered=a if key=='None' else sorted(a,key=(lambda x:(-x['derivedAttack'],x['id'])) if key=='AttackDesc' else (lambda x:(-x['quality'],x['id'])) if key=='QualityDesc' else lambda x:(x['type'],x['id']))
   expected='|'.join(x['id'] for x in ordered)
   fact(m,'order-'+key,expected==o['publishedIds'],dict(count=len(a),key=key,expected=expected,published=o['publishedIds']),[ln])
  if o.get('stage')=='preview9':
   cb=json.loads(o['canonicalBeforeJson']);ca=json.loads(o['canonicalAfterJson']);hb=json.loads(o['beforeJson']);ha=json.loads(o['afterJson'])
   fact(m,'canonical-'+o['flow'],len(cb)==9 and cb==ca and hb==ha,dict(dimensions=list(cb),equal=cb==ca,hashEqual=hb==ha,candidate=o['candidateId']),[ln])
life=[]; target='e586b6ad6004480e831009b22ae8397e'
for ln,s in enumerate(D['collection']['st'],1):
 b=s['before'];a=s['after'];br=b['raw'];ar=a['raw'];bi=ids(br);ai=ids(ar);tag=s['tag'];destroy=tag=='life-7-dismantle'
 removed=list((collections.Counter(bi)-collections.Counter(ai)).elements());added=list((collections.Counter(ai)-collections.Counter(bi)).elements())
 common=set(bi)&set(ai); bm={x['id']:x for x in br['items']+br['warehouse']};am={x['id']:x for x in ar['items']+ar['warehouse']}
 stable=all(identity(bm[i])==identity(am[i]) for i in common)
 conserved=(removed==[target] and not added) if destroy else collections.Counter(bi)==collections.Counter(ai)
 ore=a['ore']-b['ore'];ok=stable and conserved and ore==(1 if destroy else 0)
 tb=sum(x['id']==target for x in br['items']);twb=sum(x['id']==target for x in br['warehouse']);ta=sum(x['id']==target for x in ar['items']);twa=sum(x['id']==target for x in ar['warehouse'])
 if tag=='life-2-deposit':ok &= (tb,twb,ta,twa)==(1,0,0,1) and b['favIds']==a['favIds']
 if tag=='life-3-withdraw':ok &= (tb,twb,ta,twa)==(0,1,1,0) and b['favIds']==a['favIds']
 if tag in ['life-6-ui-refusal','life-6-authoritative-refusal','life-7-arm']:ok &= b==a
 if tag in ['life-1-favourite','life-6-refavourite']:ok &= target not in b['favIds'] and target in a['favIds']
 if tag in ['life-4-unfavourite','life-7-unfavourite']:ok &= target in b['favIds'] and target not in a['favIds']
 itag={'life-7-dismantle':'life-7-confirm','C01-sortbag-warehouse-favourite':'life-sortbag-warehouse-favourite','C01-sortwarehouse-bag-favourite':'life-sortwarehouse-bag-favourite'}.get(tag,tag)
 events=[dict(line=i,**x) for i,x in enumerate(D['collection']['inp'],1) if x['detail'].startswith(itag+' ') or (tag=='life-6-authoritative-refusal' and x['kind']=='protection-api' and 'Salvage' in x['detail'])]
 record=dict(step=ln,tag=tag,ok=bool(ok),bagBefore=len(br['items']),warehouseBefore=len(br['warehouse']),bagAfter=len(ar['items']),warehouseAfter=len(ar['warehouse']),targetContainerCounts=[tb,twb,ta,twa],favBefore=[v for v in b['favIds'].split(',') if v],favAfter=[v for v in a['favIds'].split(',') if v],oreBefore=b['ore'],oreAfter=a['ore'],oreDelta=ore,removed=removed,added=added,identityStable=stable,inputEvents=events,rawStateLine=ln)
 life.append(record);fact('collection',tag,ok,record,[ln])
native=[]
for tag in ['C03-removed-duplicate-location','C03-kept-strip-sort-cycle']:
 events=[dict(line=i,**x) for i,x in enumerate(D['sort-imgui']['inp'],1) if x['detail'].startswith(tag+' ')]
 win=next(x for x in events if x['kind']=='native-window');down=next(x for x in events if x['kind']=='native-mouse-down');up=next(x for x in events if x['kind']=='native-mouse-up');pids=re.findall(r'(?:ownPid|windowPid|foregroundPid)=(\d+)',win['detail'])
 ok=pids==[str(D['sort-imgui']['mf']['pid'])]*3 and down['frame']<up['frame'] and down['time']<up['time']
 native.append(dict(tag=tag,ok=ok,events=events));fact('sort-imgui',tag,ok,events)
coll=D['collection'];res=D['restart'];seed=js(res['p']/'r1-seed.json');ri=js(res['p']/'r1-restart-input.json');co=coll['obs'][-1];ro=res['obs'][-1]
cb={x['id']:identity(x) for x in co['raw']['items']+co['raw']['warehouse']};rb={x['id']:identity(x) for x in ro['raw']['items']+ro['raw']['warehouse']}
restart=dict(pidBefore=coll['mf']['pid'],pidAfter=res['mf']['pid'],tokenBefore=co['SessionToken'],tokenAfter=ro['SessionToken'],favBefore=co['FavoritesCount'],favAfter=ro['FavoritesCount'],equipmentEqual=cb==rb,seed=seed,seedHashMatch=sha(res['p']/'r1-seed.json')==ri['seedSHA256'],saveHashMatch=sha(coll['p']/'isolated-save/save.json')==ri['saveSHA256'])
restart['ok']=restart['pidBefore']!=restart['pidAfter'] and restart['tokenBefore']!=restart['tokenAfter'] and restart['favBefore']==3 and restart['favAfter']==0 and restart['equipmentEqual'] and restart['seedHashMatch'] and restart['saveHashMatch'] and seed['profileId'] in read(coll['p']/'isolated-save/save.json') and seed['profileId'] in read(res['p']/'isolated-save/save.json')
fact('restart','life-8-same-character-restart',restart['ok'],restart)
g=js(D['guid']['p']/'r1-guid-manifest.json');new=g['newGuids'].split(',');old=g['preExisting'].split(',')
for n,ok,detail in [('C04-guid-format',len(new)==3 and all(re.fullmatch('[0-9a-f]{32}',x) for x in new),new),('C04-guid-unique',len(set(new))==3,new),('C04-guid-no-collision',not set(new)&set(old),dict(preExisting=len(old),intersection=list(set(new)&set(old))))]:fact('guid',n,ok,detail)
visual_names={'strength-character-screenshot','strength-hud-display','strength-default-hud-visible','strength-screenshot','strength-fallback-hud-mode','strength-fallback-hud-screenshot'}
for m,d in D.items():
 for idx,c in enumerate(d['result']['detail'],1):
  name=c['name'];obs=[(i,o) for i,o in enumerate(d['obs'],1) if o.get('stage')=='check' and o['flow']==name];states=[i for i,s in enumerate(d['st'],1) if s['tag']==name]
  matches=[f for f in facts if f['mode']==m and f['name']==name]
  if m.startswith('strength'):
   if any(name.startswith(x+'-') for x in ['strength-rank','strength-x5','strength-final-ap','strength-basic-power']):matches=[f for f in facts if f['mode']==m and f['name'].startswith('raw-ap@')]
   if name.startswith('strength-preview-'):matches=[f for f in facts if f['mode']==m and f['name']=='preview-chain']
   if name.startswith('strength-hud-mode-switch'):
    raw=[o['raw'] for o in d['obs'] if o.get('stage')=='strength' and o['flow'] in ['chain','hud','fallback-hud']];matches=[dict(name='raw UI-mode equality',ok=len(raw)==3 and all(x==raw[0] for x in raw))]
  if name.startswith('sort-'+m.split('-')[-1]+'-'):
   key=name.split('-')[-1];matches=[f for f in facts if f['mode']==m and f['name']=='order-'+key]
  if m=='preview9' and name.startswith('preview9-'):matches=[f for f in facts if f['mode']==m and f['name']=='canonical-role-'+name[9:]]
  if m=='golden':matches=[f for f in facts if f['mode']==m and f['name'].startswith('raw-ap@')]
  level='RECOMPUTED' if matches and all(f['ok'] for f in matches) else 'FAIL' if matches else 'RECORD_ONLY'
  visual=(m.startswith('strength') and any(name.startswith(x+'-') for x in visual_names)) or (m=='sort-imgui' and name in ['C03-no-duplicate-strip','C03-kept-strip-works','native-screenshot-C03-removed-duplicate-location','native-screenshot-C03-kept-strip-sort-cycle']) or (m=='sort-ugui' and name in ['screenshot-r1-sort-roster-bottom','screenshot-r1-sort-key-AttackDesc'])
  if visual:level='VISUAL_CORROBORATED'
  ev=[dict(line=i,**x) for i,x in enumerate(d['inp'],1) if name in x['detail'] or name.removeprefix('selected-id-') in x['detail']]
  checks.append(dict(index=len(checks)+1,mode=m,name=name,reported=c['result'],auditLevel=level,resultLine=8+idx,observationLines=[i for i,o in obs],stateLines=states,inputs=ev,computedFacts=[f['name'] for f in matches],reportedDetail=c['detail'],observationMatched=len(obs)==1))
summary=dict(scope='read-only static Player evidence audit; no build, no Player, no driver import',runs=len(runs),reportedPassRuns=sum(x['consistency'] and x['process_ok'] for x in runs),reportedChecks=len(checks),observationMapped=sum(c['observationMatched'] for c in checks),classification=dict(collections.Counter(c['auditLevel'] for c in checks)),hashRecords=len(hashes),hashFailures=sum(not x['ok'] for x in hashes),facts=len(facts),factFailures=[f for f in facts if not f['ok']],uniquePids=len({x['pid'] for x in runs}),isolatedRoots=len({x['root'] for x in runs}))
dump('PLAYER_REVIEW.json',dict(summary=summary,runs=runs,checks=checks,facts=facts,lifecycle=life,native=native,restart=restart));dump('FILE_HASHES.json',hashes);dump('DIRECTORY_HASHES.json',directories)
with (OUT/'CHECKS_99.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['index','mode','name','reported','auditLevel','resultLine','observationLines','stateLines','computedFacts','reportedDetail']);w.writeheader();w.writerows({k:v for k,v in c.items() if k in w.fieldnames} for c in checks)
md=['# UX04B2R1-FINAL 独立只读 Player 审计','', '## 结论', '',f"A03 九模式原始结果逐项计数为 {summary['reportedPassRuns']}/9 完成、99/99 报告 PASS；99 项均有同名原始 observations 检查记录。不能把该计数等同于 99 项全部独立证明。",f"独立重算/目视/仅记录分级：{summary['classification']}。文件与二进制 SHA256 校验 {summary['hashRecords']} 条，失败 {summary['hashFailures']}；独立事实 {summary['facts']} 条，失败 {len(summary['factFailures'])}。",'','只新增本目录审计脚本和报告；未导入原 driver、未构建、未启动 Player、未 git add/还原。原始长行 JSON 用独立 stdlib 脚本批量解析；人工通过 read 分段检查文本，read_image 查看真实截图。','', '## 身份、隔离、进程与哈希','', '|mode|RunID|PID|exit|check|身份/构建/隔离|hash异常|','|---|---|---:|---:|---:|---|---|']
for x in runs:md.append(f"|{x['mode']}|{x['runId']}|{x['pid']}|{x['exitCode']}|{x['checks']}|{x['identity_ok']}/{x['build_ok']}/{x['evidenceDir_ok']}|{x['hash_bad']}|")
md+=['', 'RunID 对齐 command/result/manifest/run-id 文本/每条 observation；九个 PID 与 runRoot 均互异。DLL、EXE、driver 对当前隔离构建文件真实 SHA256 复算，逐个 manifest.files 校验字节数及 SHA256。manifest 自身不在其自校验表内，仍属于未签名本地证据而非防篡改认证。', '',f"完整数值及逐文件哈希：[PLAYER_REVIEW.json]({link(OUT/'PLAYER_REVIEW.json')}) / [FILE_HASHES.json]({link(OUT/'FILE_HASHES.json')})。",'', '## C05 真实画面与数值链','', '真实原始截图目视：rank0 角色页普攻33；rank3 角色页普攻48，强力打击分别0级/3级。两者文案均为攻击力+5（单级说明，不代表三级总加成为5）。既有 IMGUI HUD 左上攻击分别33/48，防御0；默认 uGUI HUD 确实没有攻击数字，不冒充数值证据。','', '原始 raw：baseDamage25、主武器 derivedAttack8、rank×5为0/15，独立相加AP33/48，basicPower一致。Main候选真实 derivedAttack132；preview evaluation.before 33/48，after 25+132+0/15=157/172，delta124。ActiveRun originRunId 有值，出征通过产品API而非原生鼠标；非自然游玩升级证据。preview9 目录无截图，C05 preview 数值依据仅结构化 evaluationJson，非目视预览页面。']
md+=['', '## 独立目录指纹', '', f"全量目录文件共 {sum(len(d['files']) for d in directories)} 件（包含九个manifest），独立目录 SHA256 不依赖原 summary；[完整清单]({link(OUT/'DIRECTORY_HASHES.json')})。清单也记录runRoot现存同相对路径文件的比对；不存在的对应文件只标记，不当作相等。",'', '|模式|文件数|目录SHA256|同路径源可比数|源差异|','|---|---:|---|---:|---|']
for d in directories:md.append(f"|{d['mode']}|{len(d['files'])}|{d['treeSHA256']}|{sum(v['sourceExists'] for v in d['files'])}|{d['sourceDifferences']}|")
for m in ['strength0','strength3']:
 for k in ['character','hud','fallback-hud']:
  p=D[m]['p']/f'r1-{k}-strength-{m[-1]}.png';md.append(f"- [{m} {k}]({link(p)})")
md+=['','## C07 逐条收藏生命周期','',f'目标装备 {target}。数量从 before/after.raw 独立计算，不采用 verdict；每一步全部共同装备非位置身份字段保持，排序允许坐标变化。API守卫与输入链明确分列。','', '|step/tag|bag+warehouse before→after|目标 bag,warehouse before→after|收藏数|铁矿 delta|独立守恒/身份|输入依据|','|---|---|---|---|---:|---|---|']
for x in life:
 ev=','.join(str(e['line'])+':'+e['kind'] for e in x['inputEvents']) or '未记录对应输入（API/设置或仅状态）'
 md.append(f"|{x['step']} {x['tag']}|{x['bagBefore']}+{x['warehouseBefore']}→{x['bagAfter']}+{x['warehouseAfter']}|{x['targetContainerCounts']}|{len(x['favBefore'])}→{len(x['favAfter'])}|{x['oreDelta']}|{x['ok']}|{ev}|")
md+=['',f"原始状态：[collection state-changes]({link(coll['p']/'r1-state-changes.jsonl')})；[collection input-events]({link(coll['p']/'r1-input-events.jsonl')})。",'', 'UI收藏、存入、背包排序、取回、仓库排序、取消、普通整理、重收藏、禁用按钮点击、取消、预确认、确认均有 uGUI raycast+mouse-down/up。该 mouse 为注入 InputSystem 事件，不能称 Windows 原生硬件输入。权威 Salvage 拒绝是 protection-api（input第77行），其前后 item/fav/ore 完全保留；UI禁用拒绝另有75/76行down/up，不混为同一种测试。成功分解唯一移除目标，铁矿0→1；先显式取消收藏，因此不能独立证明 NotifyGearDestroyed 自动清收藏。PruneStale 为API联合容器测试，不能冒充玩家操作。','',f"同角色重启：PID {restart['pidBefore']}→{restart['pidAfter']}，session {restart['tokenBefore']}→{restart['tokenAfter']}，收藏3→0；全部装备跨背包/仓库非位置身份完全相等 {restart['equipmentEqual']}，seed与传入save哈希匹配 {restart['seedHashMatch']}/{restart['saveHashMatch']}，profileId在两个真实save中存在。独立结论 {restart['ok']}。restart input-events 为空（新进程读取保存不是鼠标动作）。",'', '## C03 Windows原生链','', 'ownPid/windowPid/foregroundPid 均2520，与manifest PID一致；第一个恢复前焦点属于13288，AttachThreadInput后才得到2520。初次 SetForegroundWindow=False 未隐藏。']
for x in native:md.append(f"- {x['tag']}: 验证{x['ok']}；"+'；'.join(f"L{e['line']} {e['kind']} frame={e['frame']} {e['detail']}" for e in x['events'] if e['kind'] in ['native-window','native-mouse-down','native-mouse-up']))
md+=['', '真实截图标题清晰无标题下重复条，保留左下操作条可见；另有背包目录分类条，不将不同职责分类条当成被删除重复控件。原生点击后排序None→AttackDesc，旧位置点击FilterKey不变，有原始同名check状态记录。']
for n in ['native-C03-removed-duplicate-location.png','native-C03-kept-strip-sort-cycle.png']:md.append(f"- [{n}]({link(D['sort-imgui']['p']/n)})")
md+=['','## 范围与证据缺口（仅登记）','', '- RECORD_ONLY 表示存在同名原始check，但缺少可独立重演该断言的输入/返回/完整前后数据，或本次未进行该截图逐像素目视；不得升级成独立PASS。详见逐99项表。','- C01 scoped/loss API守卫仅有check说明，无完整传参/返回；不把说明当独立复算。','- C06八角色九维 canonical 前后字符串独立比较一致；证明记录的状态只读，不证明所有角色after数字语义。没有预览截图。','- C05实际rank设置过程没有对应逐次升级输入记录；真实存量状态及数值链成立，但不证明自然玩家升级流程。','- 原始 input-events 多数不含RunID/PID，身份依赖所在独立目录、manifest、哈希及frame关联；C03专门记录原生窗口PID。','- exitCode=0来自采集manifest，无操作系统独立签名；仅验证现存本地链内部一致性，不能追溯证明采集时绝无篡改。','- 本次仅审计Player证据；不检查原代码实现，不进行新运行补证。','', '## 逐99项依据表','',f"[CSV]({link(OUT/'CHECKS_99.csv')})；JSON保留重算事实、原始输入行号及细节。",'', '|#|mode/check|原结果|独立级别|result/observation/state原始行|重算依据|','|---:|---|---|---|---|---|']
for c in checks:
 p=D[c['mode']]['p'];refs=f"[result:{c['resultLine']}]({link(p/'result.json',c['resultLine'])}) "+' '.join(f"[obs:{i}]({link(p/'r1-observations.jsonl',i)})" for i in c['observationLines'])+' '+' '.join(f"[state:{i}]({link(p/'r1-state-changes.jsonl',i)})" for i in c['stateLines'])
 md.append(f"|{c['index']}|{c['mode']}/{c['name']}|{c['reported']}|{c['auditLevel']}|{refs}|{', '.join(c['computedFacts']) or '原始记录/目视，限制如上'}|")
(OUT/'PLAYER_REVIEW.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2))
