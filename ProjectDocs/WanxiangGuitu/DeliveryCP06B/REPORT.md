# CP06-B 交付：双刃、巨剑、镰刀

分支 `feature/cp06-new-weapons`，不合并 main。开始基线 `e1f13446601e4324a67c472eecd3419a6c317e65`（CP06-A）。产品冻结 `759340c8e7909b2cda43e20cc67af916016a47fc`；最终文档提交身份以本文件所在固定 Git 提交为准。main 核对仍为 `72db192a527bd256e2ba18cd7ab334d8334051da`。推送不代表独立复审通过。

## 实际实现

双刃：左右交替、第三段交叉；六段影袭连舞；反击只消费真实敌人攻击在翻滚无敌窗被拒绝产生的短暂回执，空翻滚不强化。巨剑：慢重斩、蓄势下劈和可测试非Boss破防状态；地波逐段真实碰撞并被墙阻挡。镰刀：有方向的弧形基础攻击、三段回旋、受视线/速度/质量及Boss免疫约束的连续牵引，无瞬移。三种武器分别使用独立motor和阶段参数。

类型追加11/12/13，稳定definitionId；主副装备、背包/仓库、品质、词缀、UI及持久化接入。复用既有动画加程序化骨骼姿态，原创简化模型/图标/三种音效，不是新增完整骨骼动画包。详细范围见[设计](NEW_WEAPON_DESIGN.md)、[兼容](WEAPON_COMPATIBILITY.md)、[资源](ANIMATION_AND_ASSETS.md)、[参数](BALANCE_PROPOSAL.md)。实际资源清单与SHA见[asset-catalog](Evidence/asset-catalog.json)。

关键源码：`NewWeaponRegistry.cs`、`NewWeaponCombat.cs`、三个motor、`EnemyWeaponControl.cs`、`NewWeaponVisual.cs`、`NewWeaponDropRules.cs`、`NewWeaponDrop.cs`。共享系统只接入必要分支/事件；原CombatAim、TargetAssist、OrbitCamera、CameraActorFade完整保留。旧四武器及八技能通过精确IL和实际规则回归保护。

## 独立追加掉落（用户已批准）

旧抽取池、概率、品质、词缀、顺序及三随机流均不插入新项。新Run创建时固定NWD1:3规则；旧在途Run不补开。普通3%、精英8%、Boss0，最多一件，三类型等权；品质45/37/14/3.5/.5%，所有阶段私有SHA派生。既有死亡一次性、实体身份、地面物品与保存恢复机制防重复；无新增v9字段。是额外供给，可能提高现有分解产矿与制造收益，不宣称经济或最终平衡不变。见[DROP_RULES](DROP_RULES.md)。

## 本轮真实验证

[完整明细](Evidence/FinalAnalysis2/results.csv)：最终选定Editor **789 PASS /0 FAIL**，隔离非开发Player **824 PASS /0 FAIL**。分别来自20与23个真实进程夹具，重复setup行按trial+index区分，不伪称1613种不同玩法。45项[进程与冻结输入一致性](Evidence/delivery-consistency.json)通过，包含各语义回执对应NativeProbe退出证据。旧迁移v1～v8另有独立Editor规则日志，不混入主汇总；v9保存/跨进程在主矩阵。所用夹具分别记录产品版本，Near4/Upgrade及较早存储回归不是全部同一次最新构建。

B1、B2、B3各自先Editor/Player和可运行包再进入下一轮，历史结果均保留。最新纯发行构建 **0错误/98警告**；最新测试构建 **0错误/225警告**。五项Bee诊断服务false，Development=false；28种产品类型测试/纯包IL一致，纯包无NW/CP6/CPC驱动、Editor引用及测试原生桥。30项旧IL/字段布局检查与34项源码/保护检查通过。纯包启动训练、实际日志与退出0单列，不作为纯包人工战斗或原生菜单退出。见[构建与警告](Evidence/FinalAnalysis2/builds-and-warnings.json)、[程序集审计](Evidence/latest-assembly-audit.json)、[纯包启动](Evidence/LatestPureSmoke4/runtime.json)。

新通道同检查点对照：旧完整掉落多重集合和三流逐值一致，Unity全局不变；追加0对1。装备UUID原始值保留，跨独立运行新生成UUID不拿来冒充一致；只从配对payload比较中排除。真实生成、落地、拾取、保存与新进程重复加载单独覆盖。训练金丝雀证明合成正式存档字节不变。见[配对](Evidence/new-run-pair-player-final.json)、[独立恢复](Evidence/PlayerChannelGroundLatest4/probe.json)、[训练隔离](Evidence/PlayerTrainingCanaryLatest4/training-storage-canary.json)。

CPU/GC只有限定区间测量：Editor正/零分配校准通过；最新Player校准失败，因此Player CPU/GC **NOT_RUN**，不把其37项功能PASS冒充性能通过。完整帧/GPU/多敌并发/长时间/硬件预算未验收。见[PERFORMANCE](PERFORMANCE.md)。

## 失败与限制

[失败历史](FAILURE_HISTORY.md)保留初始缺实现、取消动作不同步、Frenzy/Reach/回响遗漏、近距夹具失效与比较器顺序问题。新档首次发布一次aborted，候选存档及原回执保留；LSR4/LRR4复测通过但根因仍UNRESOLVED。StorageEditor1原PASS摘要被错误复用输出覆盖，原进度与SeedPackage仍在，报告明确披露，未伪造恢复原摘要。

最终开放登记 **6 NOT_RUN /7 UNRESOLVED**，逐项见[验收](ACCEPTANCE.md)。历史失败不从目录删除，不被最终PASS替换。原生U16、人工可读性/手感/音质、最终平衡没有通过。没有新增武器专属配方/出售系统，也没有新地图或旧经济重构。

2355项开工保护文件复核，用户场景/ProjectSettings/Recovery保持原状，允许变化仅在独立分支获准产品文件。1213产品输入保持冻结源码身份；主工程用户文件未提交。完整日志发布副本仅压缩/脱敏，原始SHA与发布SHA见[manifest](Evidence/manifest.json)。本地可玩包与操作见[PLAYER_GUIDE](PLAYER_GUIDE.md)。完成本批后暂停等待固定SHA独立复审。

本批新武器主矩阵是受控真实运行时代码/物理调用与敌人攻击刺激，不是自主完整搜打撤AI冒险；没有将其标成原生玩家全流程。最新纯包仅可玩包构建与启动/退出验证，未自动注入操作。

隔离构建输入与源码序列化配置并非逐文件相同：PC_RPAsset、URPGlobalSettings、EditorBuildSettings、ProjectSettings、GraphicsSettings五项差异及具体字段在[build-input-field-diffs](Evidence/build-input-field-diffs.json)。实际测试前输入与纯包构建后快照均保留，产品程序集IL等同不代表全部渲染/配置等同。未擅自恢复或回写用户文件；完整序列化构建输入等同性继续UNRESOLVED。Profile身份与实际Bee五项false另独立核验通过。
