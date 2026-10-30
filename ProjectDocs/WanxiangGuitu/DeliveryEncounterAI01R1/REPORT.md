# ENCOUNTER-AI-01-R1：已释放威胁的所有权修复

开工本地/远端main均为 `b040b550a5725511a34867de4a2cb27dc56a2b95`。本批只修改ForestBossBrain.cs一行：OnDisable保留CancelIntent，移除无条件ClearReleasedThreat。最终完整SHA见提交后重新读取远端main的交付块；推送不代表独立复审通过。

## 已确认根因与实际修复

弹体owner是仍活动的CombatEnemy，单独禁用ForestBossBrain不会停止其Update。已释放的有限预测记录也由CombatEnemy持有，但旧OnDisable跨越所有权边界清掉它，导致其他敌人的HasAttackSlot提前放行。

旧版两个Boss的真实发射均重现该路径：弹体继续移动，CombatEnemy与GameObject仍活动，威胁窗消失。最终同一受控夹具在418、419上分别68PASS/12FAIL；12个断言是同一缺陷在两个Boss×命中/外部销毁路径的重复观察，不是12种独立产品缺陷。

修复后，取消前摇仍不补发、不推进序列；已发记录跨AI禁用/恢复保持。真实命中、弹体消耗/外部销毁及有限窗过期后，其他敌人实际经过前摇造成Damage，Boss也重新经过新预警和释放。没有直接Fire/Begin/Release、设置威胁时刻/序列或注入Damage来造通过。

仍采用原有限预测窗，**不是每弹即时注册表**。命中/外部Destroy后可保守保留至预测时刻加既有间距，过期自动解除；本批不承诺即时退还、不增加逐弹跟踪，也不扩大到CombatEnemy单组件禁用的所有组合。

## 本轮新证据

| 层 | 结果 | 边界 |
|---|---|---|
| 最终聚焦回归 | 3新进程，418/419/420各80PASS，共240PASS/0FAIL | 初始位置/隔离非目标明确受控；自然AI选择和释放原招式，真实弹体/物理/Damage |
| 同输入旧/新 | 418、419各68PASS/12FAIL→80PASS | 驱动字节、配置和初始射线记录逐字节一致，见input-binding |
| 原必要定向与生命周期 | 新19+13PASS | EncaiRepro与EncaiGuard重跑；不继承旧524 |
| 其他受影响回归 | B3随机、Boss经济及Running/Pending/Committed四进程全部exit0 | 共8个既有回归进程，含19/13上述两项；实际回执原文归档 |
| 非开发全量构建 | PASS，0错误/96警告 | 完整首次报告保留，不筛选警告 |
| 最终缓存构建 | PASS，Options=None，0错误/2警告 | Boot/Title序列化版本警告；缓存没有重放全部编译告警，不表示前94条已修复 |
| 发行PE/输入绑定 | PASS | R1驱动不在发行程序集，无UnityEditor引用；单产品源与最终构建输入逐字节一致 |
| 纯发行Player运行、完整正常冒险、原生UI、人工、性能 | NOT_RUN | 本批聚焦生命周期，不继承先前Player/正常AI/人工结果 |

最终结构化新断言272PASS（240+19+13）。原批次524PASS、全部失败及原始证据完整保留，原目录Git差异为空；它们仍是原批次结果，不计入R1新通过数。

## 初始失败与夹具修正

首轮工具编译因固定Unity的SceneHandle隐式int转换被禁用失败，改用GetRawData并保留原log。旧夹具把普通敌Guard配空区域但未停用，探针一直未警戒，产生4个恢复失败；仅修正测试夹具，产品Guard不改。正确夹具旧版仍保留12项本缺陷失败。

初始补充419出现“潮矢实际命中”FAIL，原失败不重分类。只读Unity诊断发现原射线被石柱在9.611793米处阻挡；它不能当成无遮挡必命中的夹具。新夹具先从最多8个现有NavMesh点选择可用无遮挡初始姿态，逐候选记录碰撞；419保留原被挡候选，选择右侧候选后仍由自然Boss发射/真实命中。没有删除障碍、改射程、换seed或放宽命中断言。新选择规则用于旧/新两版共同对照，不把不同夹具的输入混称一致。详见FAILURE_HISTORY和initial-lanes。

## 保护与开放项

Boss数值/序列、护甲、武器、经验、经济、掉落、RNG、地图和v9均不改；未新增字段/迁移/依赖/CI。5个用户文件SHA不变，未提交用户ForestRuins、ProjectSettings或Recovery。测试工程/合成档在 `I:/WGCombat/ER1-1030-A`，未操作真实玩家档、抢桌面、关闭用户程序或强杀进程。

历史D3D12 UNKNOWN、旧C15、Editor青色帧、Search等根因继续UNRESOLVED；原生U16与人工理解继续NOT_RUN。不扩大为所有攻击/组件组合已关闭或最终难度通过。交付后暂停等待独立复审。
