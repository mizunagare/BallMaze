# 开工行为审计（49aadd50）

本批锁定ArmorMitigation、CombatHealth、经验/武器/配置数值、v9、经济、掉落、RNG和布局。任务中的EnemyBrain.cs当前不存在；通用AI实际在CombatEnemy，波次首领BossBrain，森林首领ForestBossBrain，导航/警戒在EncounterGuard。

| 类型 | 源码实际行为 |
|---|---|
| 普通近战 | 森林发现11米；水平1.7米接近，.65秒锁向前摇，水平75°半角、范围+已有.15容差、LOS；原始伤害12，恢复.35秒；间隔1.3秒（从准备时加前摇）。无独立目标选择或环形封位系统 |
| 远程 | 森林发现11米；小于4.5后退，大于preferredDistance7或失去视线时接近；12米内且眼部LOS时准备；.8秒锁点，发射点根+1.25m再前移.7m，8m/s、半径.16、6秒寿命；原始9，恢复.45、间隔2。发射前不再检查枪口段，碰撞从前移点开始 |
| 精英 | 基础140HP、20伤害，接近2.6米，1.1秒前摇，60°半角、恢复.65、间隔2.1；不是新招式，主要范围/时序/数值差异 |
| 波次Boss | Slam/Charge/Fan，1.4/1.5/1.2秒预警，既有各招范围、24及原比例派生伤害/投射速度，结束2.2秒ready；当前不参加通用普通敌预定释放时间排队 |
| 森林Boss | 两套三招及怒阶段，来自ForestBossRules。Warden根震23/冲锋27/散射12；Tide潮矢11/标记24/岸击21。状态Idle/Tracking/Telegraph/Attacking/Recovery/Hurt/Returning/Dead。怒阶段既有cooldown×.75不变；不参加普通敌排队 |

通用错峰只检查同目标、同场景、两敌距离<8米、另一普通敌WindingUp，与拟定释放时刻差<.24则暂缓准备。它不考虑Boss或飞行到达时间。前摇锁定origin/direction/aim，期间不追踪转向。近战是水平根距离/锥+眼部LOS，不是完整3D武器Collider。

EncounterGuard发现时同POI警戒传播；敌人离home>24或玩家离home>31进入返回，距home<1.2复位。导航按.35秒或目标变化>3米刷新完整NavMeshPath，无路则零移动。普通无guard时Steer探测前方1.1米并试45/90/135度，不设计复杂队形。角色碰撞仍可能形成队列，本批不假造已有封位系统。

EnemyProjectile扫掠排除友方敌人，首个有效碰撞消耗；目标死亡/owner消失或失活时清理；暂停冻结移动/寿命。Actor OnDisable取消普通前摇；森林Boss OnDisable只隐藏提示，未清除状态/直到时间；森林与波次Boss对GameplayPaused仅return，不顺延绝对until/releaseAt，和普通敌顺延行为不同。UI通常同时timeScale=0，但组件GameplayPaused单独成立时仍应保持一致。

正常地图支持：Warden与poi4精英同区；Tide与poi6近战/远程同区。有限矩阵Boss混合只取同poi6既有Tide+普通敌，不为凑矩阵改布局/加敌种。诊断的Warden/波次Boss+近战是明确的受控组合，不称自然地图遭遇。

## 实际旧例

BeforeRepro第一次编译因固定Unity版本已禁用GetInstanceID失败，改用对象引用去重，原失败保留。BeforeRepro2真正执行原AI Update，6PASS/9FAIL：窄高掩体下眼部视线为真，3枚弹体从墙另一侧生成，英雄实际掉27HP且未重定位；相距14米两射手释放/命中间隔0；森林/波次Boss与近战实际命中间隔.02秒；森林Boss禁用后重启释放旧隐藏攻击；GameplayPaused且世界时钟活跃时前摇1.5秒→0，恢复即命中。原始事件/HP/位置/帧均保留。

这些是受控几何/时钟边界，不是独立人工，也不证明每张地图都会出现。只修这些已复现合同，不通过数值膨胀制造难度。
