# COMBAT-PRESENTATION-03：四武器动作辨识度与分层战斗反馈

- 项目：万象归途（WanxiangGuitu）
- 仓库：mizunagare/BallMaze
- 固定制定基线：9fbe3a854dc799e581f7681efe5720eb253d71a5
- 前置：GAMEPLAY-UX02 限定技术复审；真实小数伤害与反馈禁用生命周期已修复
- 目标：让剑、矛、法杖、弓在动作节奏、视觉语言和命中反馈上具有可辨识的职责
- 性质：表现层专项；先资产/事件审计，再基于现有资源做最小改进
- 人工试玩暂不可用：观感、易读性、音质、舒适度和最终打击感继续 NOT_RUN
- 完成后：推送、核对完整SHA、等待独立复审

## 1. 设计目标与四武器视觉语言

四种武器必须在不改变战斗数值的前提下，让玩家从动作、轨迹、命中反馈中区分：

- **剑：横向、连续、宽幅。** 普攻体现横扫；技能体现旋风/环绕的范围感。避免把普通命中和技能爆发做成同一种火花。
- **矛：前向、线性、穿刺。** 普攻突出蓄势/突刺/收势；技能突出长距离贯穿方向。视觉线不能超出真实MeleeGeometry。
- **法杖：施法、聚能、弹体释放、爆裂。** 普攻明确单发直击和飞行时间；技能突出主弹命中后的爆裂层级。爆裂范围必须对应真实爆炸判定，不能视觉误导。
- **弓：拉弦、瞄准、释放、箭矢飞行。** 普攻单箭轨迹明确；技能扇形箭雨的多箭方向与真实发射方向对应。不能用视觉箭矢暗示未发射或未命中的箭。

以上是表现语言目标，不是已实现结论。Codex必须先盘点项目现有动画片段、骨骼/武器挂点、技能实际事件、资源和调用链；不得假设存在某个clip或可直接复用某个prefab。

## 2. 固定基线已知的系统入口（开工必须重读）

- AdventureCombat.cs：AttackAction、启动/释放/结束时间、真实Release、剑/矛近战几何、法杖/弓弹体方向及技能多段发射。
- FantasyActorVisual.cs：当前AttackTimed按武器选片段，剑与默认近战共享1H_Melee_Attack_Slice_Horizontal，矛用2H_Melee_Attack_Stab，弓用2H_Ranged_Shoot，法杖用Spellcast_Shoot；动作通过Legacy Animation.SampleAnimation采样。
- CatActorVisual.cs：猫族刚性部件绑定既有骨骼，不能破坏挂点与旧模型骨骼合同。
- CombatFeedback.cs：AttackStarted、Swing、RangedRelease、Hit、EnemyAttack、BossWarning、BossRelease、ProjectileImpact、AddProjectileTrail；表现独立随机，不应消耗AdventureRandom。
- CombatFeedbackEffect.cs：Slash、Thrust、Impact、GroundRing及有限对象池。
- CombatSoundBank.cs：七种运行时合成音效；不是外部录音素材。
- OrbitCamera.cs：相机跟随和受击震动。
- CombatHealth.Damage：真实生命变化后触发FantasyActorVisual.Hurt与CombatFeedback.Hit。
- GAMEPLAY-UX02保留的法杖1.5m侧置相机未命中：CAMERA_SURFACE_BEHIND_MUZZLE；6m成功样本不是修复，不得在本批顺手改瞄准业务。

## 3. 审计先行

先生成：
1. 四武器普攻/技能事件时序表：输入、动作clip、动作起始、实际释放帧、弹体/近战业务、真实Damage、表现、动作结束/取消。
2. 每种武器实际可用动画clip、时长、采样方式、绑定骨骼/挂点、是否缺失。
3. 现有CombatFeedback调用点与武器/攻击阶段映射。
4. 特效/音效/伤害数字与真实Damage/Projectile事件的关联方式。
5. 现有资源可复用表及缺失项。若无专用动画，不得虚构已有资源。
6. 缺陷分类：真实表现缺陷、资源缺失、纯观感待人工、测试/观测缺口。

## 4. 允许的最小改进方向

仅当审计证实有真实问题，优先：
- 为现有武器动作建立明确的阶段/姿态映射，避免不同武器误用相同动作；优先复用已存在并已验证的clip。
- 在不更改真实释放时间的前提下，让动作启动/释放/恢复表现与AdventureCombat AttackAction时间线协调；取消未释放动作时正确恢复，不出现假释放。
- 剑挥砍与矛突刺使用不同形状/方向/持续时间的表现，但表现几何不得冒充真实伤害体积。
- 法杖聚能/发射/命中爆裂分层，命中爆裂只能由真实ProjectileImpact/Damage路径触发；未命中不显示命中特效。
- 弓拉弦/发射/箭矢飞行分层；多箭表现数量与实际Spawn一致。
- 受击反馈可区分玩家与敌人、普通与致死，但不得重复触发或遮盖Boss预警/关键UI。
- 为表现事件增加只读、低开销、可关联的观测ID/时间戳时，必须证明不会改变业务顺序、随机流或性能显著性；默认优先复用现有AttackID、帧和Damage观察，不新增全局事件框架。

若现有动作资源不足，先提交资源差距与候选方案；不得擅自下载/引入新资源。新增原创表现资源必须单独列出来源、许可、大小和平台成本，并先以独立提案评估。

## 5. 明确禁止

不得修改：
- 伤害、范围、冷却、攻击启动/释放时间、弹速、碰撞体、MeleeGeometry、CombatAim；
- 武器特性、护甲、敌人AI/数值、经验、经济、掉落、地图、撤离、随机流；
- v9存档结构、迁移、结算与来源账；
- Unity/URP/Input System版本或引入动画/音频/VFX中间件。

不得用动画事件直接造成伤害、用特效/声音当命中证据、用预览轨迹替代实际弹体、用屏幕闪白/过量震屏制造打击感。不得为通过测试而关闭碰撞、改目标HP或注入Damage。

不得将自动化动作片段/截图/时序通过宣称真人认为动作更清晰或更爽。

## 6. 验证矩阵

四武器每种均覆盖：
1. 普攻启动、真实释放、命中、未命中、结束；
2. 技能启动、多段/多弹发射（若该技能实际定义）、命中/未命中、结束；
3. 释放前取消、暂停/恢复、死亡/切武器取消；
4. 近距与远距有效目标；法杖近距侧置相机历史负例单独保留；
5. 动作clip实际存在、绑定模型可采样、无缺clip/异常姿态；
6. 视觉轨迹与实际近战几何/Projectile Spawn方向对应；
7. 命中特效/伤害数字/声音仅由真实业务事件触发；
8. 普通、精英、Boss、森林双Boss受击/致死反馈不重复、不丢失；
9. 特效池/音效声道/材质实例和场景卸载清理；
10. 非开发验收Player与纯发行构建分层（若执行）。

所有样本固定seed、Profile/Run/attempt、武器ID、AttackID、帧/时间、clip、真实释放、弹体/几何结果、Damage before/after和表现事件。未采集指标NOT_RUN，不填0。

性能方面至少检查本轮新增的每帧采样、Material实例、粒子、Trail和日志/观测开销；若无有效Profiler基准，性能继续NOT_RUN，不声称优化。

## 7. 交付物

在 ProjectDocs/WanxiangGuitu/DeliveryCombatPresentation03/ 下：
- TASK.md
- DESIGN.md（四武器视觉语言、clip/挂点清单、事件时序图）
- REPORT.md
- ACCEPTANCE.md
- TESTING.md
- FAILURE_HISTORY.md
- Evidence/INDEX.md（原始时序、Damage/Projectile日志、clip/资源哈希、构建和用户文件保护）

必须明确列出近距法杖历史未命中是否仍存在，不得被远距成功样本覆盖。保留所有首次失败、夹具失败、编译失败和历史引擎异常。

## 8. Codex执行指令

读取本任务，核对远端main完整SHA。先审计AdventureCombat/FantasyActorVisual/CatActorVisual/CombatFeedback/CombatFeedbackEffect/CombatSoundBank/CombatHealth及动画、武器和特效资源，建立四武器动作阶段与真实业务事件时序图。

只修复可复现的表现层缺陷；不要改战斗数值、释放时间、命中几何、CombatAim、AI、随机流、经济、地图或v9。不得为了产生代码差异重写动画系统。新资源缺失先提案，不擅自引入第三方资源。

完成相同输入前后对照、四武器普攻/技能、命中/未命中/取消/暂停/死亡等验证，保留法杖近距历史负例。构建与测试分层记录，提交报告、验收、复跑、失败历史和证据，推送后重新核对完整SHA并暂停等待独立复审。

人工试玩、动作观感、可读性、音效质感、舒适度和最终打击感继续NOT_RUN。
