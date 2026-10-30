# COMBAT-PRESENTATION-03 报告

制定基线 `9fbe3a854dc799e581f7681efe5720eb253d71a5`；实际开工 `c7efb644f38387f7588f4bd58fe5697e4ecdd9c4`（仅TASK/计划前进）。最终SHA由包含本报告的提交及交付回复绑定，不把冻结输入当最终提交。交付后暂停，等待独立复审。

## 实现与资源边界

审计12个Knight legacy片段、骨骼/挂点、54项资产、实际Start→Release→Damage链后，只改4个产品文件：

- `FantasyActorVisual.cs`：剑技能复用既有2H_Melee_Attack_Spin；其他片段/采样循环不变；取消清理对应聚能。
- `AdventureCombat.cs`：仅4类表现调用变化，透传原skill与实际radius/dot/width；所有攻击分支、数值、释放/冷却表达式、CombatAim、MeleeGeometry、Projectile/Pulse原文不变。
- `CombatFeedbackEffect.cs`：复用原LineRenderer/Glow，剑横扫/环绕用共享只读截面并内缩线宽，枪线使用实际主段长度；修复原弧寿命后段越锥、枪端越球与技能仍画短枪线。代际号防池回收后错清理。
- `CombatFeedback.cs`：法杖复用既有小型GroundRing聚能，真实释放/取消/死亡清理；弓真实释放用Swing，法杖用Cast。远程启动不预占释放声限流。普通/精英/Boss非致死色相与有限Impact尺度分层，保留玩家红、致死金和旧装备色。

没有新增/下载动画、音频、shader、纹理或prefab，54项资产原SHA一致。现有KayKit/Kenney资源与既有原创猫族模型沿用原许可，7种合成音效不变。没有创建新全局事件框架。

**弓弦/杖首也是实际ProjectileMuzzle。** 直接改弓/法杖射击前骨骼采样会改变发射点，故未擅自切Aiming、重定时或引入影子枪口。弓保留Shoot片段已有拉弦部分，法杖用现有聚能表现补层。专用枪技能/法杖长施法/独立弓动作的资源差距与候选方案见DESIGN，不能描述为已完成完整专用动画。剑技能复用双手Spin用于当前持剑模型，动作自然度仍待人工。

## 本轮真实结果（集合不相加为通过率）

| 集合 | PASS | FAIL | UNRESOLVED | 说明 |
|---|---:|---:|---:|---|
| Before2 | 205 | 22 | 2 | 修订正确几何合同后的有效基线 |
| After | 227 | 0 | 2 | 相同229项/输入，22项技术或设计缺口关闭 |
| Extended | 271 | 0 | 2 | 实际武器死亡、真敌弹死亡取消、池代际、暂停与卸载 |
| Final | 279 | 0 | 2 | 保留旧装备色分支并补测 |
| VisualCueBefore | 74 | 4 | 0 | 新启动音映射预占同cue限流窗口的状态负例 |
| VisualCueAfter | 78 | 0 | 0 | 不改攻速/限流，声音留给真实远程释放 |
| Final2 | 291 | 0 | 2 | 最终版完整Editor矩阵 |
| Runtime2 | 291 | 0 | 2 | 最终非开发验收Player，原合成检查点正常继续 |

前两批截图VisualBefore/After和最终音色变体VisualCueBefore/After各保留16张原图，固定1280×720相机/120 capture-fps。截图来自离地受控夹具真实动作和释放，不是正式森林美术、原生操作或人工体验证据。

真实Strike/UseSkill和Projectile产生Damage；没有直接调用Damage、写HP、关闭目标Collider或注入奖励。AI禁用仅用于受控夹具，不宣称正常AI胜利。普通近战、精英、普通Boss及森林双Boss死亡由真实武器造成；玩家死亡取消由原伤害的真实EnemyProjectile碰撞造成。

公开AttackID/ShotIndex、逐帧clip/PoseTime/释放、Damage before/after及原始截图见Evidence。Damage观察本身不含攻击者，日志attack是LastAttackId上下文，不能将连续重叠动作按此作引擎级伤害归因；详见EVIDENCE_SCHEMA。

## 严格不变验证

`locked-contract.json`核对：剥离明确列出的表现调用后AdventureCombat与基线逐字等价；13个玩法/AI/存档/随机/音效库/镜头文件及动画LateUpdate采样循环保持原文。Before2/Final2的24个同条件真实Spawn，位置和方向实测最大差均为0；最终新增暂停箭样本单列，不隐藏额外样本。9份关键源码与最终两个构建全输入逐项匹配。未改数值、释放、CombatAim、几何、AI、经济、地图、随机流、v9/迁移、依赖或CI。

## 构建、运行与性能

Unity 6000.6.5f1，Windows，原正式构建入口Options=None。最终AcceptanceBuild2为0错误/192警告，PureBuild2为0错误/96警告，全部原警告保留，不过滤、不宣称已修复。中间构建另列，不冒充最终输入。

Runtime2从Boot/Title通过受控Continue加载Final2真实生成的seed418合成检查点，复制前后SHA相同、没有改payload；实际exit0、无超时、forcedTermination=false。它是公开战斗API的隔离验收Player，不是虚拟/原生键鼠、人工、正常AI冒险或完整结算验收。

纯发行PE不含CP03/旧验收驱动类型、无UnityEditor引用。驱动仅在隔离Assets/CP03AcceptanceOnly，产品仓库没有运行时驱动。PE、exe/UnityPlayer/程序集哈希、全部输入及检查点复制回执可追溯。

复用24特效/10声道/32数字、共享Material与33点缓冲；新增聚能有每帧只读跟随/代际检查，新增近战阶段Find查找存在分配风险，非致死分层可能增加单次粒子数（上限仍24）。没有有效Profiler/真实硬件开销对照，CPU/GC/GPU、音质、显著性能影响继续NOT_RUN，不填0、不宣称优化。测试日志在隔离驱动缓冲后落盘。

## 失败、开放项与保护

初轮剑宽度错误假设、全部旧FAIL、近距法杖样本、启动音预占负例、工具解析/查找失败和中间变体均保留。法杖近距侧置相机基本/技能仍返回CAMERA_SURFACE_BEHIND_MUZZLE并未命中，继续两项UNRESOLVED；远距通过没有关闭它。没有修改CombatAim。

原生U16、人工观感/可读性/音质/舒适度/最终打击感、正常AI冒险与完整Profiler仍NOT_RUN。独立动作命中关键帧的艺术校准、全部品质/技能等级组合、完整自然战斗/结算不由本批替代。历史UNKNOWN/C15/青色帧/Search/JobTempAlloc根因保持UNRESOLVED，exit0不是干净引擎证明。

用户Scene/ProjectSettings/Recovery五项原SHA不变，不提交覆盖层；唯一工程外合成根CP03-1031-A，测试场景/设置使用Git原字节。无真实玩家存档访问、桌面抢占、用户程序关闭或强杀。

[设计](DESIGN.md) · [验收](ACCEPTANCE.md) · [复跑](TESTING.md) · [失败历史](FAILURE_HISTORY.md) · [分层汇总](SUMMARY.json) · [证据](Evidence/INDEX.md)。推送不代表独立审核通过。
