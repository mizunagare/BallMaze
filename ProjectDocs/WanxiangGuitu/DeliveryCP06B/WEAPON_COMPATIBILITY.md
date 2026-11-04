# CP06-B：修改前兼容映射

基准e1f13446601e4324a67c472eecd3419a6c317e65，独立feature/cp06-new-weapons。本文先提交，再开始产品修改。main仍72db192a527bd256e2ba18cd7ab334d8334051da；CP06-A分支保持原提交，不合并历史分支。

|当前实现/缺口|最小映射|必要共享文件/风险|验证|
|---|---|---|---|
|GearType 0..10已保存，0..3武器/9胸挂/10背包|追加11 TwinBlades、12 Greatsword、13 Scythe，按B1/B2/B3逐个启用；永不重排|AdventureItems、AdventureCatalog；使用显式IsWeapon与稳定definitionId，保留旧GearIds数组|旧0..10逐值、旧档、未知类型拒绝|
|GearItem.Weapon<4，Name/Icon按数组索引|新增注册表分派，不以名称作身份|AdventureItems；旧分支原文保留|主副装备/背包/品质/词缀|
|v9校验限制type<=10；旧v6<9|只扩充v9允许集合及definition绑定，旧迁移不改|AdventureValidation、CombatSaveSystem；旧程序不能读取含新类型的新档，回滚须保留原档/备份，不能静默重置|v1-v9旧数据及新v9跨进程|
|原Roll Range(0,9)及Rewards流耦合|保留旧Roll逐值不变。追加独立新武器通道方案已询问用户；未明确前不接正式掉落|CombatEnemy、AdventureFlow现有contentRevision；仅新Run解锁对应批次，旧在途保持原奖励|旧流前后/480规则/实际死亡及新掉落恢复|
|AdventureCombat多处>=2当远程，4格技能数组|新武器提前分派到独立Twin/Greatsword/Scythe状态机；显式旧远程判定，旧Release/几何/弹体不变|AdventureCombat及扩展桥；每武器独立参数/阶段，公用物理内核不等于统一行为|旧4武器和8技能、法杖2近距|
|CP06-A面板3槽；新类型会得到空定义|旧武器保持原3槽，新武器展示独立两技能，旧8技能定义不改|WeaponSkillPanel分支接入；不写v9技能选择，新技能用既有公共冷却保存|UI回调、取消/冷却/保存|
|TargetAssist冻结，Update也把>=2当远程|不改其源码；新近战使用独立有限面向，分别配置角度/速度；旧4武器仍原TargetAssist|新增NewWeaponMeleeAssist；不得使用反射篡改旧评分|转角上限/不转相机/墙体|
|HeroDodge无敌时CombatHealth直接return，没有真实闪避命中回执|只在已通过原调用链的实际攻击于无敌窗被拒绝时发瞬态Evaded事件；不因空翻滚发回执|CombatHealth仅该拒绝分支，护甲公式/损血正文不改；双刃一次消费短窗，普通无触发无强化|实际敌人攻击、无敌窗内/外、重复消费/重启|
|敌人无通用牵引/破防/质量状态|B2/B3才新增最小瞬态控制；Boss/ForestBoss免疫，普通CC限速Move，实体障碍有效；有Rigidbody遵循实际质量，CC无质量须明确配置代理值|CombatEnemy必要早期门控/新控制组件；不改基础数值或已释放弹体威胁|明确GuardBroken、速度/距离/墙体/免疫/暂停清理|
|旧模型持右手，现有动画含横斩/旋转/突刺/重切|新增自制模型Prefab及双手挂点，复用许可已在库的剪辑并加分件/骨骼程序化姿态，不冒充新完整骨骼包|新资源/独立动作组件；保留旧FantasyActorVisual采样，新武器才应用附加姿态|绑定/动作时序/实际Player截图|
|UI把<4武器/>=4装备分类|以GearItem.Weapon/注册表分类，旧工作台配方不增加|CatInventoryPresenter分类、PlayerHudPresenter近战准星隐藏、WeaponTraits描述新分支|背包/仓库/主副切换/名称图标|

不改CombatAim、TargetAssist、OrbitCamera、CameraActorFade、旧武器数值/八技能定义、老掉落权重及旧随机流、PRIVACY-A配置、用户场景/ProjectSettings。新增仅使用v9现有type/definitionId/affixes/冷却/contentRevision，不增加进度字段。缺口或未测状态不得改写为PASS。

分轮：B1双刃通过Editor/非开发Player并保存可运行包后才进入B2；B2同样验证后才进入B3；三轮完成再统一回归/纯发行。动画、原生和人工状态分别记录。
