"""Audit, not rewrite, all frozen release BuildReport warnings against current protected source."""
import argparse,collections,csv,hashlib,json,re
from pathlib import Path
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--report',type=Path,required=True);ap.add_argument('--source',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--previous',type=Path,required=True);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False)
 report=load(a.report);previous=load(a.previous);warnings=[m for m in report['messages'] if m['type']=='Warning'];old=collections.Counter(m['text'] for m in previous['messages'] if m['type']=='Warning');assert len(warnings)==91 and old==collections.Counter(m['text'] for m in warnings),'Warning input differs; investigate, never silently use old 91'
 impacts={
 'AdventureFlow.Exits':'InteractionResolver→出口查询/修复/撤离，限定场景与稳定出口ID',
 'AdventureFlow':'出征/恢复/冻结/结算时的世界对象收集',
 'AdventureCombat':'真实攻击/弹体命中/范围命中目标枚举',
 'AdventureRandom':'按owner/session确定随机流，查询归属不能意外改变作用域',
 'AdventureResource':'资源附近显示/主角查询，命中和掉落仍由原业务产生',
 'CampInventoryView':'营地旧管理界面的session查询（新UI接管后需核对调用条件）',
 'CombatEnemy':'敌人死亡掉落与session/世界归属',
 'CombatFeedback':'攻击/受击/战斗表现对象发现；不应影响奖励流',
 'CombatInventoryView':'旧背包/商店界面调用链；仅实际激活分支产生开销',
 'CombatSaveSystem':'保存/恢复的资源、敌人、事件与地面物稳定身份采集',
 'CombatSession':'场景session初始化与世界对象注册',
 'CraftingRecipeDefinition':'配方定义资源发现/查找，不应因顺序改变配方身份',
 'CraftingTargets':'只读制造目标/剩余资源与路线查询',
 'EncounterGuard':'据点警报与敌人群发现，需保留场景/encounter边界',
 'EnemyProjectile':'敌人弹体命中与碰撞目标收集',
 'ExtractionPoint':'出口与当前session交互归属',
 'ForestRegionRuntime':'森林模板、实体、出口、恢复和导航检查的枚举',
 'ForestRewards':'地点剩余收益/事件/资源查询，结果必须只读',
 'GameEntry':'Boot/Title进入或返回时清理旧世界；必须包括应清理的inactive对象',
 'GamePreferences':'设置应用时相机/HUD与当前存档位置的单例归属',
 'HeroEquipment':'装备预览/迁移旧装备接口的session归属',
 'InputSettingsPanel':'从真实设置位置载入/应用绑定',
 'InteractionResolver':'每次情境交互解析；显示和执行使用同一解析身份',
 'OnboardingFocus':'教程目标与资源/出口只读可达性查询',
 'PlayerInput':'输入采样重连/场景变更后的主角定位，禁止串到其他session',
 'PlayerInventory':'近邻/通知/交互和旧缓存字段清理',
 'RouteScoring':'只读路线风险/收益/实体状态计算',
 'ScenePresentation':'场景表现资源收集/清理，不得改变碰撞/导航',
 'WorldEventPoint':'事件/宝箱/祭坛与当前主角、session归属'}
 rows=[]
 for i,m in enumerate(warnings,1):
  text=m['text'];row=dict(id=f'W{i:03}',code='',file='',line='',column='',api='',risk='',canChangeRuntime='',regressionRequired=True,disposition='OPEN / 审计完成，不在本批修复',impact='',replacement='',recommendation='',sourceSha256='',snippet='',raw=text,rawSha256=hashlib.sha256(text.encode()).hexdigest(),linkedDiagnostic='')
  match=re.match(r'(.+?)\((\d+),(\d+)\): warning (CS\d+): (.*)',text,re.S)
  if match:
   path,line,col,code,msg=match.groups();path=path.replace('\\','/');f=a.source/path;lines=f.read_text(encoding='utf-8-sig').splitlines();ln=lines[int(line)-1];row.update(file=path,line=int(line),column=int(col),code=code,sourceSha256=sha(f),snippet=ln[max(0,int(col)-100):int(col)+180],impact=impacts.get(f.stem,'见精确源码位置；不以警告数量推导已执行频率'))
   if code=='CS0618':
    api=re.search(r"^'([^']+)'",msg)[1];row['api']=api
    if api=='FindObjectsSortMode':row.update(risk='信息',canChangeRuntime=False,replacement='与相邻FindObjectsByType调用一起移除排序枚举参数',recommendation='这是同一调用点的附加诊断，不代表又执行了一次查询；合并到对应API迁移计划，禁止孤立删除参数。')
    elif 'FindFirstObjectByType' in api:row.update(risk='中',canChangeRuntime=True,replacement='FindAnyObjectByType<T>()；如业务需要稳定选择，改为显式场景/稳定ID选择',recommendation='旧First依赖InstanceID；不能机械换Any。先验证单例唯一性与owner/scene，保留多session/恢复/隐藏对象边界后再授权小补丁。')
    elif 'FindObjectsInactive' in api:row.update(risk='中',canChangeRuntime=True,replacement='FindObjectsByType<T>(原FindObjectsInactive参数)',recommendation='必须保留Include/Exclude、scene过滤和显式稳定ID排序；漏掉inactive参数可能遗留旧世界或漏模板。')
    else:row.update(risk='低',canChangeRuntime=True,replacement='FindObjectsByType<T>()，保留原inactive/scene过滤和显式排序',recommendation='当前None本就无稳定返回顺序。固定版本仍可运行；未来小批迁移须核对First/索引假设。热点仅为静态候选，无调用栈证据不称已定位瓶颈。')
   elif code=='CS0414':
    field=re.search(r"The field '([^']+)'",msg)[1];name=field.split('.')[-1];refs=[dict(line=n+1,text=l.strip()) for n,l in enumerate(lines) if re.search(r'\b'+re.escape(name)+r'\b',l)]
    row.update(api=field,risk='低',canChangeRuntime=False,replacement='后续获准时删除真实死字段及其无效赋值',recommendation='当前是private、未SerializeField，只有声明/null或0赋值，没有读取。nearest/nearestEvent由InteractionResolver替代；nextAttack由AdventureCombat.attackAt负责。非有效保护状态、非当前性能瓶颈；删除后仍需E/H/攻击冷却/恢复回归。',references=refs)
   else:raise AssertionError(code)
  else:
   path=re.search(r'Serialized file "([^"]+)"',text)[1];f=a.source/path;s=f.read_text(encoding='utf-8-sig');block=s.split('GameObject:',1)[1].split('--- !u!',1)[0];obj=re.search(r'--- !u!1 &(\d+)',s)[1];version=re.search(r'^  serializedVersion: (\d+)',block,re.M);name=re.search(r'^  m_Name: (.*)',block,re.M)[1]
   row.update(code='SCENE_VERSION',file=path,api='GameObject serialized version 1 < minimum 6',risk='中',canChangeRuntime=True,replacement='单独获准的隔离场景升级/最小差异，再验证Boot与Title启动；不保存用户ForestRuins',impact='BootEntry/GameEntry根对象反序列化；当前兼容读取不代表未来导入器永久安全',recommendation='GameObject块缺少serializedVersion，按旧默认1读取；不要将Transform的version2误当成本诊断。原文件不改，冷导入与实际标题样本为最小复现；当前没有证据证明产品启动已因此损坏。',sourceSha256=sha(f),objectId=obj,objectName=name,objectSerializedVersion=version[1] if version else 'missing (legacy default 1)',snippet='GameObject fileID='+obj+'; serializedVersion missing; m_Name='+name)
  rows.append(row)
 for row in rows:
  if row['api']=='FindObjectsSortMode':row['linkedDiagnostic']=','.join(x['id'] for x in rows if x['file']==row['file'] and x['line']==row['line'] and x['code']=='CS0618' and x['api']!='FindObjectsSortMode')
 counts=collections.Counter(x['risk'] for x in rows);summary=dict(status='PASS',count=len(rows),codes=dict(collections.Counter(x['code'] for x in rows)),risk=dict(counts),frozenReport=str(a.report),reportSha256=sha(a.report),sameAsPlayer02=True,scope='91 warnings audited, none automatically fixed or closed; current/future migration risks separate; not a performance bottleneck attribution')
 (a.output/'warnings.json').write_text(json.dumps(dict(summary=summary,warnings=rows),ensure_ascii=False,indent=2),encoding='utf-8')
 fields=[k for k in rows[0] if k not in ('references',)]+['objectId','objectName','objectSerializedVersion']
 with (a.output/'warnings.csv').open('w',encoding='utf-8-sig',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(rows)
 md='# 91条发行警告逐条审计\n\n风险分布：'+str(dict(counts))+'。全部仍OPEN，未修改API或重存场景；信息级为同调用点的排序枚举附加诊断，不抹去对应API风险。完整原文、SHA、源码行/列、处置与读取核对见JSON/CSV。\n\n|ID|代码/位置|API|风险|Player路径与处置|\n|---|---|---|---|---|\n'
 for r in rows:md+='|'+r['id']+'|'+r['code']+' '+r['file']+':'+str(r['line'])+'|'+r['api'].replace('|','/')+'|'+r['risk']+'|'+r['impact']+'；'+r['recommendation'].replace('|','/')+'|\n'
 (a.output/'WARNINGS.md').write_text(md,encoding='utf-8');print(json.dumps(summary,ensure_ascii=False))
if __name__=='__main__':main()
