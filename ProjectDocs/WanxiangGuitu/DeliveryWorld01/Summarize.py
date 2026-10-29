"""Read-only finite WORLD matrix and source audit; never repairs evidence."""
import pathlib,json,csv,sys,collections,math
r=pathlib.Path(sys.argv[1]);repo=pathlib.Path(sys.argv[2]);doc=repo/'ProjectDocs/WanxiangGuitu/DeliveryWorld01';e=doc/'Evidence';e.mkdir(exist_ok=True)
def read(p):return json.loads((r/p).read_text(encoding='utf-8-sig'))
samples=['418-A3','418-B','419-A','419-B','420-A','420-B'];matrix=[];maps={};bad=[]
def segment_box(a,b,center,size):
 lo,hi=0.,1.
 for axis in ['x','y','z']:
  low=center[axis]-size[axis]/2+.15;high=center[axis]+size[axis]/2-.15;delta=b[axis]-a[axis]
  if abs(delta)<1e-9:
   if a[axis]<low or a[axis]>high:return False
  else:
   u,v=(low-a[axis])/delta,(high-a[axis])/delta
   lo=max(lo,min(u,v));hi=min(hi,max(u,v))
   if lo>hi:return False
 return hi>max(0,lo) and lo<1
for name in samples:
 p='Samples/'+name+'/Shared/';nav=read(p+'content-nav.json');m=json.loads(nav['layoutJson']);maps[name]=m
 checks=[]
 for f in sorted((r/p).glob('cycle-*.json')):checks+=json.loads(f.read_text(encoding='utf-8-sig'))['checks']
 final=read(p+'cycle-final.json');combat=list(csv.DictReader((r/p/'ordinary-combat.csv').read_text(encoding='utf-8-sig').splitlines()))[0]
 # Geometry analysis is explicitly offline over actual Unity NavMesh corners, not another scene run.
 crossings=[]
 for row in nav['rows']:
  for a,b in zip(row['path'],row['path'][1:]):
   lake=m['terrain'];center=dict(lake['lakeCenter']);center['y']+=2
   if segment_box(a,b,center,dict(x=lake['lakeSize']['x'],y=10,z=lake['lakeSize']['z'])):crossings.append(row['id']+':lake')
   center=dict(lake['ridgeCenter']);center['y']+=2
   size=dict(lake['ridgeSize']);size['y']+=5
   if segment_box(a,b,center,size):crossings.append(row['id']+':ridge')
 status='PASS' if nav['unique'] and nav['readOnly'] and all(x['status']=='PASS' for x in nav['rows']+checks) and not crossings and float(combat['endHealth'])==0 and float(combat['strikes'])>0 and float(combat['heroAfter'])>0 else 'FAIL'
 row=dict(sample=name,status=status,profile=nav['profile'],run=nav['run'],region=nav['region'],requested=nav['requestedSeed'],actual=nav['actualSeed'],revision=nav['revision'],generationVersion=nav['generationVersion'],attempt=nav['attempt'],fallback=nav['fallback'],generationFailures=nav['failures'],navRows=len(nav['rows']),checks=len(checks),combat=combat,crossings=crossings)
 matrix.append(row)
 if status!='PASS':bad.append(name)
repeats={str(seed):maps[a]==maps[b] for seed,a,b in [(418,'418-A3','418-B'),(419,'419-A','419-B'),(420,'420-A','420-B')]}
if not all(repeats.values()) or len({x['run'] for x in matrix})!=6 or len({x['region'] for x in matrix})!=6:bad.append('repeat layout or identity')
before=read('Before/feedback.json');after=read('After/feedback.json')
if not after['consistent'] or not after['queryReadOnly']:bad.append('feedback')
def result(phase):
 values=read(phase+'/results.json');values=[values] if isinstance(values,dict) else values
 return all(x['status']=='PASS' and x.get('exitCode')==0 and not x.get('timedOut') for x in values)
phases=['Death','Fault','Missing','Corrupt','RecoveryMatrix','Overflow','BossEconomy','WeaponContracts','RangedArea','Boundary','PoiRun','PoiResume','Build02','Build03']
phaseResults={p:'PASS' if result(p) else 'FAIL' for p in phases};bad+= [k for k,v in phaseResults.items() if v!='PASS']
reg=read('Regression/results.json');ai=[x for x in reg if x['name'].startswith('AI.')]
if len(ai)!=3 or any(x['status']!='PASS' or x.get('timedOut') or x.get('exitCode')!=0 for x in reg):bad.append('regression')
b=read('Build03-Store/build-report-messages.json');pe=read('Build03/release-inspection.json');protect=read('protection-check.json')
if b['result']!='Succeeded' or b['errors']!=0 or b['options']!='None' or pe['status']!='PASS' or not protect['unchanged']:bad.append('build/boundary/protection')
status={'scope':'WORLD-01 controlled Editor/navigation + normal AI + build, not native/human/Player gameplay','current_status':'PASS' if not bad else 'FAIL','failures':bad,'samples':matrix,'repeatLayout':repeats,'differentSeedLayouts':len({json.dumps({k:maps[x][k] for k in ['points','routes','terrain']},sort_keys=True) for x in ['418-A3','419-A','420-A']}),'topologyVariants':len({json.dumps(maps[x]['routes'],sort_keys=True) for x in ['418-A3','419-A','420-A']}),'beforeFeedback':before,'afterFeedback':after,'phaseResults':phaseResults,'regression':reg,'build':{k:b[k] for k in ['result','errors','warnings','seconds','options']},'fullCompileBuild':{k:read('Build02-Store/build-report-messages.json')[k] for k in ['result','errors','warnings','seconds','options']},'findings':[{'id':'WORLD-F01','state':'FIXED','independentReview':'AWAITING'}],'deferred':[{'id':x,'status':'NOT_RUN'} for x in ['IsolatedAcceptancePlayerGameplay','ReleasePlayerGameplay','NativeU16','IndependentHuman','PerformanceBudget','CoreHintGroundOnlyExhaustedLegacyDedicatedRuns']]+[{'id':x,'status':'UNRESOLVED'} for x in ['D3D12_UNKNOWN','EditorCyan','EditorSearch','JobTempAlloc','OldC15']]}
(e/'status.json').write_text(json.dumps(status,ensure_ascii=False,indent=2),encoding='utf-8')
with (e/'seed-matrix.csv').open('w',encoding='utf-8',newline='') as f:
 fields=['sample','status','profile','run','region','requested','actual','revision','generationVersion','attempt','fallback','navRows','checks'];w=csv.DictWriter(f,fields,extrasaction='ignore');w.writeheader();w.writerows(matrix)
# Per-entity roles tied to the actual first layout. No fabricated materials/systems.
m=maps['418-A3'];rows=[]
def audit(i,kind,role,source,state='已有且可复现',note=''):rows.append(dict(id=i,kind=kind,role=role,current_state=state,source=source,evidence='Evidence/Samples/*/Shared/content-nav.json',limitations=note))
roles=['营地出征后的入口与附近免费出口','木材资源和木/皮料箱，常见制造材料','石/矿资源与矿料箱','晶石箱、铁矿与必出随机装备，地面需拾取','精英遭遇、皮/晶和高装备机会，Boss可选','免费撤离及通行/宝箱/祭坛','补给型材料箱与湖岸，非药水保证来源']
for p in m['points']:audit(p['id'],'POI',p['label']+'：'+roles[int(p['id'].split(':')[1])],'ForestLayout.Generate / ForestRewards.ChestRanges')
for n in m['nodes']:audit(n['id'],'resource',['木材','石头','铁矿'][n['kind']]+'；受击耗尽产生地面掉落，拾取才记 earned','AdventureResource.Hit / LootPickup.PickUp')
for x in m['encounters']:audit(x['id'],'boss' if x['boss'] else 'encounter',x['poi']+'；'+(['普通近战','普通远程','精英','森林首领'][x['type']])+'；警戒/脱战，死亡掉落一次','EncounterGuard / CombatEnemy.DropLootOnce / ForestBossBrain','已有且可复现','Boss经济专项为受控实际伤害/事务，不冒充正常AI讨伐胜利')
for p in m['points'][1:]:
 audit(p['id']+':chest','event','本地点真实材料倾向/装备概率，Used先置位，未拾取留地','WorldEventPoint.Interact / ForestRewards')
 audit(p['id']+':altar','event','一次真实技能选择；不是任务或永久成长树','WorldEventPoint.Interact / HeroProgression')
for x in m['exits']:audit(x['id'],'exit',x['label']+('；随身木2石1原子修复，本局有效' if x['repairRequired'] else '；免费，无清场前置')+'；引导/取消/受击中断','AdventureFlow.Exits / ExtractionPoint')
audit('WORLD-F01','feedback','核心缺口提示与实际森林首领/地面来源一致；修复前误称无来源','CraftingTargets.Recommendations','已有且可复现','修复前规则或状态断点；Before/After/feedback.json；等待固定SHA复审')
audit('HUD-priority','feedback','教程/制造目标优先；所选出征类型和可选地点在详情','PlayerHudPresenter / CraftingTargets.GoalFeedback','已有但反馈不清','可发现性待独立人工；未新增地图或方向系统')
audit('risk-personal','decision','HP/药水/容量供玩家判断，评分只读敌人/路程/收益/出口','RouteScoring / PlayerHudPresenter','已有但反馈不清','未将血药/空格自动折入分数，不能虚构成功率')
audit('save-identities','contract','请求/实际seed、revision、generationVersion、regionInstanceId分离，旧快照恢复','ForestRegionRuntime / AdventureFlow / CombatSaveSystem')
audit('ledger','contract','地面、随身、Pending、Committed、仓库、待领取分离','AdventureRules / CampRuntime / GroundLootStore')
for i,role in [('full-map','完整地图/小地图'),('weather-traps','天气/陷阱'),('quest-tree','大型任务树/事件框架'),('new-currency','统一货币/物资估值')]:audit(i,'absent',role,'当前源码没有完整对应机制','当前没有此机制','不是本批新增授权')
audit('direction-proposal','proposal','轻量方向/唯一目标可发现性提案','CONTENT_PROPOSALS.md','需要后续设计批准的建议','未实施')
with (doc/'CONTENT_AUDIT.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.DictWriter(f,['id','kind','role','current_state','source','evidence','limitations']);w.writeheader();w.writerows(rows)
print('samples',len(matrix),'repeat',repeats,'audit rows',len(rows),'failures',bad)
if bad:raise SystemExit(1)
