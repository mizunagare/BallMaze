"""Deterministic asset inventory; never marks runtime verification from file existence."""
import hashlib,json,re
from pathlib import Path
here=Path(__file__).resolve().parent;repo=here.parents[2];art=here/'ArtBible';resources=repo/'Assets/CombatPrototype/Resources/CatWorld'
files=[]
for p in sorted(resources.rglob('*')):
 if p.is_file(): files.append(dict(path=p.relative_to(repo).as_posix(),bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest(),gitTextNormalizedSha256=hashlib.sha256(p.read_bytes().replace(b'\r\n',b'\n')).hexdigest() if p.suffix!='.png' else None))
brief=(art/'UserBriefs/黑猫猫族世界_资产清单模板.md').read_text('utf8')
rows=[]
for asset,name in re.findall(r'^### (WX-[A-Z0-9-]+) (.+)$',brief,re.M):
 category=asset.split('-')[1];paths=[];reason='待完成逐项概念图与实际运行映射；不以资源存在冒称VERIFIED'
 if category=='UI':paths=['Assets/CombatPrototype/TitleMenu.cs','Assets/CombatPrototype/CatInventoryPresenter.cs','Assets/CombatPrototype/PlayerHudPresenter.cs']
 elif category in ('CHR','NPC','ENM','BOSS'):paths=['Assets/CombatPrototype/CatActorVisual.cs','Assets/CombatPrototype/Resources/CatWorld/Actors']
 elif category in ('WPN','EQP','ITM','MAT','ICO'):paths=['Assets/CombatPrototype/Resources/CatWorld/Props','Assets/CombatPrototype/Resources/CatWorld/Icons']
 elif category=='ENV':paths=['Assets/CombatPrototype/CatWorldScenery.cs','Assets/CombatPrototype/CatCampVisual.cs','Assets/CombatPrototype/CampRuntime.cs']
 elif category=='VFX':paths=['Assets/CombatPrototype/CombatFeedback.cs','Assets/CombatPrototype/ForestBossTelegraph.cs']

 base='Assets/CombatPrototype/'
 actor={'WX-CHR-001':'Hero','WX-NPC-001':'Keeper','WX-NPC-002':'Smith','WX-NPC-003':'Guide','WX-NPC-004':'Departure','WX-NPC-005':'Supplies','WX-ENM-001':'Bandit','WX-ENM-002':'Scout','WX-ENM-003':'Mushroom','WX-ENM-004':'WoodSpirit','WX-ENM-005':'Bandit','WX-ENM-101':'Hunter','WX-ENM-102':'Lynx','WX-BOSS-001':'Warden','WX-BOSS-002':'Tide'}
 props={'WX-WPN-001':'sword','WX-WPN-002':'spear','WX-WPN-003':'staff','WX-WPN-004':'bow','WX-EQP-001':'armor','WX-EQP-002':'trousers','WX-EQP-003':'arms','WX-EQP-004':'boots','WX-EQP-005':'ring','WX-EQP-006':'bag','WX-EQP-007':'armor','WX-ITM-001':'potion','WX-MAT-001':'wood','WX-MAT-002':'stone','WX-MAT-003':'ore','WX-MAT-004':'crystal','WX-MAT-008':'hide'}
 iconkeys=['bag','warehouse','workbench','camp','route','help','exit','bridge','boss','route','wood','stone','ore','crystal','potion','sword','spear','staff','bow','chest']
 if asset in actor:paths=[base+'Resources/CatWorld/Actors/'+actor[asset]+'.prefab',base+'CatActorVisual.cs',base+'CatCampVisual.cs']
 if asset in props:paths=[base+'Resources/CatWorld/Props/'+props[asset]+'.prefab',base+'Resources/CatWorld/Icons/'+props[asset]+'.png']
 if category=='ICO':
  code=int(asset.rsplit('-',1)[1]);key=iconkeys[code-1] if code<=10 else iconkeys[10+code-101];paths=[base+'Resources/CatWorld/Icons/'+key+'.png',base+'Resources/CatWorld/Icons/Bounds.json',base+'CatIconLayout.cs']
 if asset=='WX-CHR-002':paths=[base+'Resources/CatWorld/Materials/'+m+'.mat' for m in ['Fur','Cream','Cloth','Canvas','Leather','Steel','Red']]
 if category=='CHR' and 3<=int(asset.rsplit('-',1)[1])<=12:paths=[base+'FantasyActorVisual.cs',base+'CatActorVisual.cs']
 if asset=='WX-CHR-013':paths=[base+'Resources/CatWorld/Icons/portrait.png',base+'Resources/CatWorld/Icons/Bounds.json']
 if category=='UI' and int(asset.rsplit('-',1)[1])<100:paths=[base+'TitleMenu.cs',base+'CatUI.cs',base+'CatTitleStage.cs']
 if asset in ['WX-UI-108','WX-UI-109']:paths=[base+'ForestBossHud.cs',base+'ForestBossTelegraph.cs']
 status='INTEGRATED'
 if asset in {'WX-CHR-014','WX-ITM-002','WX-ITM-003','WX-MAT-005','WX-MAT-006','WX-MAT-007'}:status='CONCEPT_ONLY';paths=[];reason='没有单独角色立绘；不以模型或概念图冒充立绘'
 if asset in {'WX-ITM-002','WX-ITM-003','WX-MAT-005','WX-MAT-006','WX-MAT-007'}:
  key={'WX-ITM-002':'scroll','WX-ITM-003':'quest','WX-MAT-005':'herb','WX-MAT-006':'mushroom','WX-MAT-007':'cloth'}[asset];status='CREATED';paths=[base+'Resources/CatWorld/Props/'+key+'.prefab',base+'Resources/CatWorld/Icons/'+key+'.png'];reason='实际制作资源，当前经济无对应物品定义；不新增或假称可拾取、制造，未接入业务物品'
 if asset in {'WX-ENV-FOR-004','WX-ENV-RUIN-002','WX-ENV-RUIN-003','WX-VFX-006','WX-VFX-010'}:
  status='CONCEPT_ONLY';paths=[];reason={'WX-ENV-FOR-004':'未制作独立灌木/草丛组，不以树冠当草丛','WX-ENV-RUIN-002':'现有为石刻/祭坛，没有完整遗迹门框','WX-ENV-RUIN-003':'未制作专用遗迹台阶，不以平面路标替代','WX-VFX-006':'药水有真实业务和通知，未制作专用使用特效','WX-VFX-010':'撤离有进度与结果UI，未制作专用成功特效'}[asset]
 if asset=='WX-ENV-RUIN-001':paths=[base+'CombatWorldEvents.cs',base+'CatEventVisual.cs'];reason='复用真实祭坛石柱，非全新遗迹建筑组'
 if asset=='WX-ENV-FOR-008':reason='只接入石刻/祭坛/事件视觉，未制作完整遗迹建筑群'
 if asset=='WX-UI-001':reason='文字标题与原创猫头像，非独立手绘Logo字形'
 if asset=='WX-UI-010':reason='既有加载硬遮罩与提示，非淡入淡出动画'
 if asset=='WX-EQP-007':reason='胸挂真实容器业务；外观图使用护甲示意，没有新专用胸挂模型'
 if asset=='WX-NPC-005':reason='物资猫共用已有仓库，静态代理；没有独立商店/交易AI'
 if asset=='WX-ENM-005':reason='采用猫科森林兽替代外观；没有新增野猪AI'
 evidence=[]
 verification_path=art/'RUNTIME_VERIFICATION.json'
 if verification_path.exists() and status=='INTEGRATED':
  verification=json.loads(verification_path.read_text('utf8')).get('assets',{}).get(asset)
  if verification:
   evidence=verification['evidence'];assert evidence and all((here/e).is_file() for e in evidence)
   assert all(verification['checks'].values()) and all((repo/u).exists() for u in paths)
   status='VERIFIED';reason=verification['scope']+('; '+reason if not reason.startswith('待完成逐项') else '')
 resource_files=[]
 for location in paths:
  f=repo/location
  if f.is_file():
   raw=f.read_bytes();resource_files.append(dict(path=location,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),textNormalizedSha256=hashlib.sha256(raw.replace(b'\r\n',b'\n')).hexdigest() if f.suffix!='.png' else None))
 resource_type={'UI':'Runtime uGUI / source components','CHR':'Original rigid model / existing rig motion','NPC':'Static actor prefab and real facility proxy','ENM':'Enemy visual prefab over existing AI','BOSS':'Boss visual prefab over existing state machine','WPN':'Weapon prefab and icon','EQP':'Equipment icon/model','ITM':'Item model/icon','MAT':'Material model/icon','ICO':'Transparent PNG','ENV':'Procedural environment source','VFX':'Existing runtime feedback/telegraph'}.get(category,'Resource')
 use_locations=[] if status in {'CONCEPT_ONLY','CREATED'} else ['Boot/Title via TitleMenu and CatTitleStage' if category=='UI' and int(asset.rsplit('-',1)[1])<100 else 'ForestRuins runtime; component and prefab paths above, test versus native scopes separately recorded']
 rows.append(dict(assetId=asset,name=name,status=status,conceptSource='ArtBible/UserBriefs/黑猫猫族世界_概念提示词包.md',conceptImage='ArtBible/Concepts/Revisions/用户主要视觉参考_黑猫猫族世界.png',unityPaths=paths,resourceType=resource_type,resourceFiles=resource_files,useLocations=use_locations,source='Original procedural geometry/UI; existing CC0 rig and licensed fallback icons remain separately attributed',importSettings='C# runtime/uGUI source compiled by Unity' if category in {'UI','ENV','VFX'} else 'Mesh/Material/Prefab authored by CatWorldBake; PNG256 alpha, no mipmaps/uncompressed; existing rig clips reused',evidence=evidence,limitations=reason))
(art/'ASSET_INVENTORY.json').write_text(json.dumps(dict(scope='B10 current asset integration inventory; VERIFIED requires per-asset source/import/reference/runtime evidence, not file existence or human approval',assets=rows,files=files),ensure_ascii=False,indent=2)+'\n',encoding='utf8')
table=['# 黑猫猫族首版资产台账（技术验收与未完成项）','','原始9张及历次方向保留；最新用户黑猫猫族世界PNG为主视觉，STYLE_GUIDE v0.7为生产规范。概念不是实机，不将概念视觉复杂度等同实际资源完成度。完整文件大小/SHA256见ASSET_INVENTORY.json。','','|Asset ID|名称|状态|实际入口/限制|','|---|---|---|---|']
table += [f"|{r['assetId']}|{r['name']}|{r['status']}|{', '.join(r['unityPaths'])}；{r['limitations']}|" for r in rows]
(art/'ASSET_CATALOG.md').write_text('\n'.join(table)+'\n',encoding='utf8')
print(json.dumps(dict(assets=len(rows),files=len(files),verified=sum(r['status']=='VERIFIED' for r in rows),states={s:sum(r['status']==s for r in rows) for s in sorted({r['status'] for r in rows})})))
