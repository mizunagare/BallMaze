from pathlib import Path
import json,csv,sys
root=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(exist_ok=True)
def load(p):return json.loads(p.read_text(encoding='utf-8-sig'))
assertions=[]
for rel in ['Before/uxtech.json','After/uxtech.json','InputRules/input01-rules.json','InputStory/input01-play-normal.json','InputStory/input01-play-resume.json','Pause/pause.json','Runtime/uxtech.json','Runtime2/uxtech.json']:
 p=root/rel
 if not p.exists():continue
 j=load(p);rows=j.get('rows') or [dict(name=x,status=j['status']) for x in j.get('checks',[])]
 assertions.append(dict(path=rel,scope=j.get('layer',j.get('scope','controlled rules')),passCount=sum(x['status']=='PASS' for x in rows),failCount=sum(x['status']=='FAIL' for x in rows),count=len(rows)))
runs=[]
for p in sorted(root.glob('*/results.json')):
 j=load(p)
 for row in j if isinstance(j,list) else [j]:runs.append(dict(directory=p.parent.name,**row))
builds=[]
for p in sorted(root.glob('*/build-report-messages.json')):
 j=load(p);builds.append(dict(directory=p.parent.name,**{k:v for k,v in j.items() if k!='messages'}))
result=dict(note='Separate assertion sets and process/status records; never sum units as acceptance rate. Baseline/tool failures retained.',assertions=assertions,runs=runs,builds=builds,notRun=['native physical input/U16','real OS focus and hardware hotplug','independent human usability/playtest','complete performance','all modal/device combinations'],unresolved=['historical D3D12 UNKNOWN','old C15','Editor cyan frame','Editor.Search','JobTempAlloc'])
(out/'SUMMARY.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
with (out/'RUNS.csv').open('w',newline='',encoding='utf-8-sig') as f:
 keys=['directory','name','scope','status','startUtc','endUtc','exitCode','timedOut','reason'];w=csv.DictWriter(f,keys,extrasaction='ignore');w.writeheader();w.writerows(runs)
table='\n'.join('|'+a['path']+'|'+str(a['passCount'])+'|'+str(a['failCount'])+'|'+str(a['count'])+'|' for a in assertions)
btable='\n'.join('|'+b['directory']+'|'+b['result']+'|'+str(b['errors'])+'|'+str(b['warnings'])+'|'+b['options']+'|' for b in builds)
report=f'''# UX-TECH-01 交付报告

制定基线 `bee8c58db551e27739151723849410100528029b`；开工远端及实际输入 `0ab582423c031528d824879a0026e9158f287bfe`（相对bee只增加任务/计划，未改产品）。最终完整SHA由包含本报告的Git提交和交付回复绑定，不把输入SHA冒充最终提交。本批不是独立复审结论。

## 实际修改

只修改3个产品文件：PlayerInput将死亡拒绝前置，并在解锁鼠标缺EventSystem时fail-closed；InputSettingsPanel在失焦/设备epoch变化后等待释放再捕获；GamePreferences在临时文件写入和BeforePublish之后再次检查外部修改，冲突不覆盖、不应用。19动作定义、别名/冲突、保留键和v1偏好格式不变。v9、战斗/AI数值、经济、地图、随机流和依赖均未修改。

[设计/状态图](DESIGN.md)与[30文件消费者清单](consumer-inventory.json)记录原始指针/保留键及业务安全门，未为产生差异重写框架。设置第二次哈希核验不是跨进程文件锁；极窄的最终检查—Replace竞态仍不作绝对互斥保证。

## 真实断言（不同集合不相加）

| 集合 | PASS | FAIL | 总数 |
|---|---:|---:|---:|
{table}

Before为修复前产品负例，不删除；After为相同18断言。InputStory含虚拟uGUI、实际移动/攻击/技能/E-H/渡口一次扣费/偏好失败及恢复，239项中包含大量布局边界断言，不能当作239种玩法。Resume是新Editor进程同Profile/Run/区域/seed/流/修复回执/装备ID/来源账/布局核验。

Runtime2仅隔离非开发Player虚拟输入与真实产品消费者、受控死亡/设置故障夹具，不是正常AI冒险、原生鼠标或人工试玩。实际Boot/Title后显式业务确认；驱动不在纯发行构建。

## 正常AI与边界

NormalRetry1/2/3独立进程的实际状态见Evidence/NormalRetry*/results.json与Normal-Gather2轨迹/检查点/保存审计：采集、实际渡口修复、撤离结算、入仓制造、再次森林出征与新进程恢复。未以停用敌人的定向夹具代替正常AI。

Pause为受控计时夹具：投射物由真实Fire产生，菜单暂停超过6秒寿命阈值，验证真实Update冻结和关闭后恢复；不是一场正常战斗胜利。尚未穷尽全部模态/敌人/设备交叉组合。

## 非开发构建

| 目录 | 构建 | 错误 | 警告 | Options |
|---|---|---:|---:|---|
{btable}

第一次CS0117、Runtime期限退出、Normal1缺旧观测依赖和工具退出尝试均保留在[失败历史](FAILURE_HISTORY.md)。不能将Normal1进程exit0改称冒险成功；编译扫描实际FAIL。警告全部原文归档，未过滤。

PureBuild PE验明无UXTech/既有测试驱动类型及UnityEditor引用；Acceptance PE单独标记允许且要求UXTech驱动。实际exe/UnityPlayer/Assembly-CSharp哈希及源码/全构建输入/五项用户文件一致性见Evidence/final-bindings.json和各PE回执。构建不是原生退出或手感验收。

## 已知限制与保护

原生U16/物理键鼠、OS焦点/拔插、独立人工理解/舒适度/手感和完整性能 NOT_RUN。UNKNOWN、旧C15、青色帧、Search、JobTempAlloc历史根因 UNRESOLVED，未重复无新线索实验，也未改写历史FAIL。最终状态逐项见[验收](ACCEPTANCE.md)。

主工程用户ForestRuins、ProjectSettings及Recovery五项原SHA保留；未提交这些改动。测试副本使用Git场景/设置，用户覆盖层仅在工程外DeferredUserInputs保护。所有合成进度在唯一隔离根；未访问真实存档、激活桌面、强杀进程、升级依赖或启用CI。

[复跑](TESTING.md) · [证据索引](Evidence/INDEX.md) · [完整分层结果](SUMMARY.json) · [进程明细](RUNS.csv)。交付后暂停，等待固定SHA独立审核。
'''
(out/'REPORT.md').write_text(report,encoding='utf-8')
print('rendered',len(runs),'process/status rows;',len(assertions),'assertion sets')
