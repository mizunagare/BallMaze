# UX04B2R1-FINAL：原B2黄金矩阵补充独立只读审计

## 结论与边界

- 原B2黄金矩阵 **21/21 Attack位比较、21/21 Defense位比较通过，0不匹配**；不是采信旧FINAL_AUDIT、summary或驱动bitsEqual布尔值，而是本次从装备输入重算，再比较原观测的legacy/unified整数位值。
- AP/BP **21/21文本精度一致**。原B2只保存0.###文本，未保存AP/BP原始位字段；本次提供计算位值，但不得把它夸大为AP/BP历史逐位实测通过。
- 原B2六份FINAL manifest **6/6通过**；逐文件字节数与SHA256 **74/74一致**，exit=0、未超时、未强杀、complete=PASS、0 error、各1 done。未重跑Player或构建，未重复A03主复算。
- **历史双计修正链无法完整证实**：有旧报告文字声明，但未发现首次45失败与修正后39的原始审计脚本/运行输出；不能把本次新证据冒充历史保留记录。

## 输入来源与独立性

1. 原始[黄金观测](<Evidence/Runs04B2/UX04-B2-GOLDEN-FINAL/b2-observations.jsonl>)，seq4–24为21个goldenName行；seq2入口给出8件、主武器ID及2件worn。
2. 同一Run的[原始v9存档](<Evidence/Runs04B2/UX04-B2-GOLDEN-FINAL/isolated-save/save.json>)：payload.profile.camp.gear的8件完整装备（savedAttack/savedDefense/dataRevision/state/ID）、mainWeapon、skills[0]=0。其为运行保存结果而非逐合成行before快照；入口count/Main匹配，原驱动黄金测试在克隆列表构造候选，不向真实库存加入候选。
3. 原[驱动](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2/Tools/IntDriverB2.cs#L297-L401>)只用于获取合成输入的type/quality/state/容器选择，**不使用其结果作为oracle**。未保存候选GUID/affixes，故用独立唯一占位ID重建；词缀不参与本次Attack/Defense表达式。
4. 旧HEAD=95caf234256613d4a6e4f89a8ab0dc09c397c6b2；本次只读git show导出的[旧Loadout](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/golden/old_HEAD_AdventureLoadout.cs.txt#L16-L23>)与[旧GearItem](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/golden/old_HEAD_AdventureItems.cs.txt#L30-L52>)用于确认Main、Unique首项、Active、Attack/Defense及FreezeNewStats表达式。
5. 从5份QualityData、9份ItemData、4份ContainerData资产读取power/factor/bonus；**18份资产字节均与旧HEAD相同**。详细路径、SHA256、字节数与equals_old_HEAD见[JSON输入账本](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/golden/GOLDEN_REVIEW.json>)。品质power=8/19/43/78/132，武器attackFactor=1，饰品=.5，护臂=.35，二者defenseFactor=.2。
6. 基础攻击25、力量rank×5、长枪×1.25来自[英雄](<Assets/CombatPrototype/ThirdPersonHero.cs#L10-L22>)、[成长](<Assets/CombatPrototype/HeroProgression.cs#L38>)、[战斗](<Assets/CombatPrototype/AdventureCombat.cs#L82-L84>)；本B2存档力量为0，不能外推非零力量覆盖。

## 计算方法与位值

[独立脚本](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/golden/review_golden.py>)不导入任何既有审计器。struct.pack/unpack('<f')冻结资产乘法、容器左结合加法、AP左结合加法和BP乘法为float32。旧LINQ Sum浮点的double累加后转换与产品逐次float32累加均核对；本矩阵每行最多2个Active项，两种累加最终位值相同。

| 输入组 | 行数 | Attack | uint32位值 | Defense位值 |
|---|---:|---:|---:|---:|
| baseline/main-White/reserve-red/state-InBag/Overflow/Worn | 6 | 8 | 1090519040 | 0 |
| main-Green | 1 | 19 | 1100480512 | 0 |
| main-Purple与7武器 | 8 | 43 | 1110179840 | 0 |
| main-Gold | 1 | 78 | 1117519872 | 0 |
| main-Red | 1 | 132 | 1124335616 | 0 |
| board-Accessory | 1 | 74 | 1116995584 | 1104360243 |
| board-Arms | 1 | 54.20000076293945 | 1113115853 | 1104360243 |
| state-Board | 1 | 86 | 1118568448 | 0 |
| container-bonus | 1 | 14 | 1096810496 | 1077936128 |

逐行计算值、Attack/Defense原始两列位值、AP/BP计算位值和文本比较详见[CSV](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/golden/GOLDEN_REVIEW.csv>)与[JSON](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/golden/GOLDEN_REVIEW.json>)。例：护臂AP=79.19999694824219，bits=1117677158，历史文本79.2；长枪AP=68、BP=85（bits=1118437376）。

## 6/6 manifest逐文件复验

| FINAL Run | files | 结果 |
|---|---:|---|
| GOLDEN | 12 | PASS |
| UGUI | 13 | PASS |
| IMGUI | 12 | PASS |
| FAVSEED | 12 | PASS |
| RESTART | 12 | PASS |
| READBACK | 13 | PASS |

六个manifest均取自Evidence/Runs04B2/UX04-B2-{mode}-FINAL；逐项路径/size_ok/hash_ok保存在[JSON](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/golden/GOLDEN_REVIEW.json>)。这证明所列历史证据与manifest一致，不替代人工操作覆盖，也不表示磁盘当前DLL与历史构建同一。

## container-bonus双计：历史记录缺失，不能补造

- 找到旧[FINAL_AUDIT:114](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2/FINAL_AUDIT.md#L114>)文字：“首次45，误将active_sum=14再加bagab=6；修正为8+0+6，AP39”。这仅是历史声明，**本次没有把它用作数值输入或通过依据**。
- 路径glob列出原B2文档/Tools与原Run文件；内容检索范围、模式和结果已保存在[history_search](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/golden/history_search.json>)。原B2目录仅该旧报告相关叙述命中，原B2 Runs、R1 Tools与R1 EVIDENCE未检出该首次失败/修正记录。
- 因而：**可确认声明存在，无法证实“首次失败与修正脚本/输出已原样保留”**。不等同证明历史事件未发生，也不虚构缺失文件。
- 本次独立重算：Active只有白主剑8；[rig_heavy](<Assets/CombatPrototype/Resources/ContainerData/rig_heavy.asset#L28-L29>) attack0/defense3；[bag_relic](<Assets/CombatPrototype/Resources/ContainerData/bag_relic.asset#L28-L29>) attack6/defense0。因此Attack=8+0+6=14，AP=25+14+0=39（bits1109131264），Defense=3。绝不把包含容器加成的14再次当active_sum。

## 不混淆产品旧preview风险

旧[B2AttackModel](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/_baseline_snapshot/B2AttackModel.cs#L200-L211>)穿戴候选时只将新副本worn并追加，未卸旧同类；[旧Loadout ContainerFor](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/golden/old_HEAD_AdventureLoadout.cs.txt#L31-L35>)FirstOrDefault可能仍选旧容器，造成替换预览沿用旧bonus。该产品数值风险与“审计oracle把+6算两遍”根因不同。本黄金container-bonus行直接传rigHeavy/bagRelic，不调用容器replacement preview，故21/21通过**不能关闭**该preview数值风险；同样审计oracle修正也不能证明产品preview已修复。

## 本轮写入边界

仅在本golden目录新增审计脚本、旧HEAD摘录和报告JSON/CSV；未改任何既有源码、工具、历史证据、文档；未构建、未启动Player、未git add/reset/checkout/restore/clean。执行脚本exit0；曾有一次Python路径反斜杠转义导致启动失败，改用正斜杠后正常；该启动失败与历史oracle双计不是同一事件。
