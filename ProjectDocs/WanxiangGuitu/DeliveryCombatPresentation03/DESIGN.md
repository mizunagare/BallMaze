# CP03 最小表现方案与审计结论

开工c7efb644f38387f7588f4bd58fe5697e4ecdd9c4（相对制定9fbe仅任务/计划）。源码/资源审计BASELINE_RESOURCE_AUDIT.json含54资产及46调用点；12个Knight legacy clips中Spin与Aiming真实存在，无专用长枪技能/法杖长施法片段。所有素材沿用原许可，不下载、创建或引入新资产。

真实链：Strike/UseSkill→原AttackAction/冷却→AttackTimed+AttackStarted→原releaseAt/Release→近战几何或实际Spawn→WeaponHit/CombatHealth实际承伤→Hit/Hurt/Defeat。动画采样不会调用Damage，反馈不产生奖励。

## 已运行基线

Before为201 PASS/22 FAIL/2 UNRESOLVED，固定120 capture-fps、seed418，真实武器攻击，无直接Damage/HP修改、无关闭Collider。负例分两种：
- 实际合同缺陷：装饰剑弧/枪线超出现有球/方向/slab；技能剑仍水平片段，已有Spin未用。
- 已证实的设计缺口：法杖无聚能层；弓与法杖共享Cast释放音；普通/精英/Boss非致死命中色相相同。这些不是伤害失败，属于任务明确要求的表现职责。

## 授权范围内实现

1. 仅剑技能复用已有2H_Melee_Attack_Spin，其他动作沿原采样时钟。AttackTimed新增可选skill参数，不修改动作总时长/释放时点。
2. AdventureCombat只替换表现参数/增加与既有SpawnMelee相邻的表现调用：实际radius/dot/width透传到有限LineRenderer池。剑横扫与技能环绕采用共享MeleeGeometry只读截面；枪沿前向截面，包含线宽余量内缩。主业务参数/循环与攻击分支不变。
3. 法杖启动复用现有GroundRing+Glow小型聚能（非范围/命中），真实RangedRelease或取消/死亡/Reset清理。复用代际号避免池回收后把别人的Impact当聚能移动或清除。至多跟踪一个当前聚能；池24上限不变。
4. 弓真实释放复用Swing音色，法杖保留Cast；不额外绘制箭，数量/方向来自原Spawn。非致死精英/Boss复用原Impact色相/有限粒子尺度分层，伤害数字仍来自同一个真实Damage。

## 必须保留的发射点边界

弓弦/杖首同时是正式ProjectileMuzzle来源。射击前改骨骼clip/采样会改变CombatAim输入，违反本批限制。因此不启用Aiming替换射击前片段、不改法杖骨骼时序，不拆新逻辑枪口/影子骨架；保留已有Shoot片段中的拉弦动作。专用弓/法杖/长枪技能动画仅提资源差距，后续需单独授权验证发射点合同。本批不把聚能当作新施法骨骼动画。

## 成本/生命周期

现有LineRenderer、Material、7合成音效与24/10/32池复用，没有新资源文件、shader或音频。WeaponSweep边界生成一次，原33点Draw只淡出；聚能每帧只读缓存combat/muzzle并检查代际/角色，不写玩法，不记录运行日志。粒子数上限仍24，新增分层可能增加单次粒子量；真实Profiler与人体感知NOT_RUN，不能宣称性能或手感优化完成。

## 不变项与未完成

不改CombatAim/MeleeGeometry函数、数值/释放表达式、冷却、AI、护甲、经济、地图、随机流、v9。Near Staff的CAMERA_SURFACE_BEHIND_MUZZLE继续单列UNRESOLVED，不被远距样本关闭。原生U16/人工观感/音质/舒适度/最终打击感NOT_RUN，历史引擎状态不变。

源码保守复核补充：新MeleeTrace继续采用旧Swing的装备品级色，不让形状改进丢失旧品级视觉。初版After/Extended与最终颜色保持版分开冻结，最终版另复测，不冒用旧结果。剑实际Contact宽度为Infinity，矛才有slab；设计/验证以实际代码为准。

## 资源/接入差距提案（未实施、需独立授权）

| 缺口 | 当前真实复用 | 候选与必要验收 |
|---|---|---|
| 专用长枪技能动作 | 同Stab片段+真实7m主段线 | 同Rig专用蓄势/贯穿clip；先审许可、骨骼与时间线，不下载/伪造现成资源 |
| 法杖长施法与独立爆裂动作 | 原Spellcast_Shoot+现有聚能/真实弹体Pulse | 兼容施法clip或可视层姿态方案；发射点等价、无新伤害/延时，先单独评估 |
| 独立弓瞄准clip安全接入 | Aiming真实存在但未启用，保留Shoot原采样 | 仅可视代理或另行批准的挂点合同研究；必须配对证明真实枪口/弹道不改，不在本批拆框架 |
| 专属蓄力/拉弦音色 | 现有7合成cue，远程声音留真实释放 | 原创/许可明确音源独立提案；音频预算/通道与人工听感评估，本批不新增 |

这些不列为已制作/接入/VERIFIED。现有Spin为双手片段，单手武器表现自然度仍需人工；源码、采样、截图通过不能替代该判断。
