# 阶段2现状审计、验收对应与最小差异方案

日期：2026-10-27。审计远端main/本地HEAD均为 `eb69b5ed8f1d508a0d6fccbca2b6eeb0eb1a5572`；此前阶段2冻结产品/测试为 `07ee0e2612c69602b24670f5c8ede53a4396e5d7`。本次仅源码/文档/已提交证据审计，不是独立复审结论，没有新启动Unity、Player、游戏测试或读取真实存档。新结果仅指本次文档完整性检查，游戏验证本轮NOT_RUN。

[正式基线2.1～2.9](STAGE2_VALIDATION_SPEC.md) · [滚动计划](DEVELOPMENT_PLAN.md) · [审计输入/用户文件SHA256](PlanAudit/2026-10-27-stage2/baseline.json)

## 判定口径

- **已有实现**：代码/数据存在实际业务路径，历史运行证据另标，不等于本轮新PASS或玩家体验通过。
- **需要修复**：已确认不一致，明确是文档还是产品。此次确认的是计划状态/基线映射文档问题；没有据此确认必须重写或新增玩法的产品缺陷。
- **需要补测**：已有机制但样本、场景、真实输入/人工/性能或故障证据不足；不能冒称功能缺失。
- **尚缺实现**：具体所需代码/观测确实没有，注明最小范围。本次仅发现普通敌逐只精确TTK观测缺口，不等于战斗机制缺失，未在本轮实施。

同一项可同时“已有实现+需要补测”；类别不与PASS/FAIL/NOT_RUN/UNRESOLVED混用。未列为缺陷不代表已经证明无缺陷。

## B07-R1～B10-R1真实落点

|批次|核对的源码|报告/实际边界|结论|
|---|---|---|---|
|B07-R1|ForestBossRules/Brain/Hud/Telegraph、BossWarningGeometry、CameraActorFade|[验收](DeliveryB07-R1/ACCEPTANCE.md)有六攻击真实物理规则、屏幕HUD/预警、正常AI/恢复；原生Boss战与人工NOT_RUN|双Boss机制/奖励已有；可读性和手感仍需人工，不重复做首领系统|
|B08|Onboarding/OnboardingFocus、CampFacilities、CampRuntime、PlayerHudPresenter|[报告](DeliveryB08/REPORT.md)教程绑定真实移动/拾取/结算/制造/新Run，hasTutorial区分旧档；设施走动+暂停合同|教程/营地已有；首次玩家理解与四武器独立试玩仍缺证|
|B09|GameEntry、SaveCatalog、CombatSaveSystem.Entry、NewProfileTransaction、TitleMenu|[验收](DeliveryB09/ACCEPTANCE.md)单自动档、确认与恢复；原角色动作历史边界不能当当前全猫骨骼能力|入口/单档与事务已有，无多槽、没有完整脚掌IK/全视角手感验收|
|B10/B10-R1|BootEntry、CatInventoryPresenter/CatActorVisual/CatWorldArt、B09入口及保存授权门禁|[B10报告](DeliveryB10/REPORT.md)、[P0复审台账](DeliveryB10/ReviewClosure/REPORT.md)实际在DeliveryB10内；程序化刚性猫部件/既有骨骼、翻滚程序化、NPC静态，概念不等于成品|不新造B10-R1目录或把当前模型称完整软蒙皮。无草药/食用蘑菇等新增业务经济，不能拿仅CREATED资产当配方能力|

B09旧角色资源审计是历史输入，当前黑猫表现以B10实际实现为准。P0报告末尾“阶段2未开工”是其2026-10-26历史状态，本轮不重写历史报告；当前计划明确指向后来已交付待复审的阶段2。

## 当前代码合同与参数

|主题|当前实际源码/数据|可观察机制与边界|
|---|---|---|
|四武器|[AdventureCombat](../../Assets/CombatPrototype/AdventureCombat.cs)、AdventureLoadout、WeaponTraits/WeaponHit|长剑近战/4m技能，长枪窄前向/7m技能，法杖投射/范围爆炸，弓箭/扇形箭；紫金红效果与六词缀存在。无箭支库存/法力/天气系统，不虚构依赖|
|三构筑|[AdventureCatalog](../../Assets/CombatPrototype/AdventureCatalog.cs)、[AdventureLoadout](../../Assets/CombatPrototype/AdventureLoadout.cs)、[已提交属性CSV](DeliveryStage2/Evidence/FinalAll/Diagnostics/Rules/stage2-builds.csv)|安全：重胸挂+白甲防御6.2/移速.95；采集：轻胸挂+采集包移动1.1/采集+1/76格（标准96）；讨伐：余白武器上盘攻击41（其它33）。这些是实验合成已有物品配置，不是新增新手奖励|
|推荐|[RouteScoring](../../Assets/CombatPrototype/RouteScoring.cs)、[RouteEvaluation](../../Assets/CombatPrototype/RouteEvaluation.cs)、[配置](../../Assets/CombatPrototype/Resources/RouteScoring.json)、[Navigation](../../Assets/CombatPrototype/ForestRegionRuntime.Navigation.cs)|真实NavMesh长度、PathComplete、出口接近/费用材料检查；剩余节点/未开箱/活敌/地面掉落；只读业务投影，导航缓存可变。新颖度实际是“未完成来源比例”，不是未到访概率；风险不是精确生存预测|
|地点收益|[ForestRewards](../../Assets/CombatPrototype/ForestRewards.cs)、AdventureResource、CombatEnemy、WorldEventPoint/CombatWorldEvents|林地木/皮、矿区石/矿、遗迹晶/矿及保证装备边界、哨站较高掉落机会、湖岸补给；ShouldDropChestGear处理roll=1保证边界。期望值查询不抽奖励|
|随机/生成|[AdventureRandom](../../Assets/CombatPrototype/AdventureRandom.cs)、ForestLayout/ForestTerrain/ForestRegionRuntime|新Run保存Rewards/Placement/Events version1，地图局部确定源、表现隔离；没有流字段的旧在途继续legacy语义。当前layout5/terrain1/boss1/generation8，各版本不混用|
|制造目标|[CraftingTargets](../../Assets/CombatPrototype/CraftingTargets.cs)、AdventureRecipes、[CampWorkbenchRuntime](../../Assets/CombatPrototype/CampWorkbenchRuntime.cs)|真实配方+未解锁前置成本/随身与仓库缺口；Manufacture真实消费/产物/同次保存；白装备成本木2石1矿2，品质与前置按数据，不另设测试捷径|
|成长/仓库|HeroProgression、PlayerInventory、[CampRuntime](../../Assets/CombatPrototype/CampRuntime.cs)、AdventureRules|局内等级六技能、药水、属性盘与双武器、200装备仓库、满仓待领取、材料转移；真实经济和物品身份不靠UI预览复制|
|结算/来源|[AdventureState](../../Assets/CombatPrototype/AdventureState.cs)、[AdventureRules](../../Assets/CombatPrototype/AdventureRules.cs)、[AdventureFlow](../../Assets/CombatPrototype/AdventureFlow.cs)|entryGear身份保护、brought/earned区分、唯一run:terminal，Pending→Committed→ACK，committedRuns与pending；冻结规则不改。Camp旧波次分支清场条件不等于当前森林撤离条件，Enter在冒险中接BeginExtraction|
|渡口/Boss|AdventureFlow.Exits、AdventureFlow.Bosses、[ForestBossRules](../../Assets/CombatPrototype/ForestBossRules.cs)|渡口木2石1一次原子消费/修复回执、免费出口；Boss独立身份/首次与重复记录、徽章永久，首奖生成不是自动拾取/入仓|
|存档/入口|[CombatSaveSystem](../../Assets/CombatPrototype/CombatSaveSystem.cs)、GroundLootStore、SaveLocationMigration、GameEntry、SaveCatalog|单自动档v9及v1～v9读取/迁移/备份，完整分页、旧布局/已定奖励恢复；正式Boot→Title→玩家选择；没有虚构槽位|
|观测|[CombatHealth](../../Assets/CombatPrototype/CombatHealth.cs)、Stage2Experiment、Summarize-Matrix|TotalDamageTaken实际扣血累计，排除回血/过量；不参与结果、不存档，测试外部指标合并进程。整局伤害/药水已有，普通敌逐只起止TTK没有|

## 逐项验收对应表

“历史”均指输入07ee/交付eb69的已提交结果。本次未重跑，不能记为本轮游戏PASS。证据总入口：[阶段2索引](DeliveryStage2/Evidence/INDEX.md)。

|ID / 基线|已有实现与源码落点|当前归类|当前证据与剩余工作|
|---|---|---|---|
|A1 / 2.3 四策略职责|ForestRewards、CraftingTargets、ForestBossRules、正常AI Gather/Treasure/Bypass/Land/Lake|已有实现；需要补测|历史采6/寻4/绕1/陆4/湖4，陆/湖同属讨伐。绕行样本n1，需独立玩家判断/更多同条件样本，不新增第四目标枚举|
|A2 / 2.3 真实路径/剩余/出口|RouteScoring.Evaluate/EvaluateExit、NavigationPath|已有实现；需要补测|历史路径与score-normal快照；不是图边长排名。人工路线认知、动态阻挡体验未终验|
|A3 / 2.3 只读性|AdventureRandom.Draw、RouteScoring/CraftingTargets、B3/RouteScoringRules|已有实现|业务/随机状态前后断言历史在；缓存更新不冒充奖励变化，代码改后需受影响重跑|
|A4 / 2.3 合法普通撤离|ForestLayout免费出口、AdventureFlow.BeginExtraction/Exits|已有实现|历史渡口与免费出口实走；不要求清场/稀有物，保持旧波次测试分支|
|A5 / 2.3 可复现/恢复|RunState/checkpoint/randomStreams、ForestRegionRuntime、CombatSaveSystem|已有实现|请求/实际seed/版本、fallback与跨进程历史；不重抽旧在途布局/奖励|
|A6 / 2.3 风险收益取舍与记录|RouteRisk、Stage2Experiment、Summarize-Matrix|已有实现；需要补测|数量/消耗/米数/承伤/时间/ID在；预声明机器人策略原因不等于人类选择，不能用混合组均值判平衡|
|B1 / 2.4 四武器探索/战斗/撤离|AdventureCombat.Strike/UseSkill、HeroDodge、Loadout|已有实现；需要补测|历史12基本+7补充，四白武器及双Boss；所有武器×所有低资源/近满包/换装条件未穷举，人工未跑|
|B2 / 2.4 安全构筑|Rig/board Defense、Damage/Dodge/药水|已有实现；需要补测|真实def6.2/速度.95；少量成功案例不足证明安全性提升的因果/成功率|
|B3 / 2.4 采集构筑|HarvestBonus/MoveBonus、AdventureResource.Hit|已有实现|匹配弓seed1两节点额外木2；采集包容量取舍已记录，人工效率待验证|
|B4 / 2.4 讨伐构筑|Loadout.Active/Attack、Combat/技能/药水|已有实现；需要补测|真实AP41、8个Boss矩阵；精确战斗效率与更广配对样本仍不足|
|B5 / 2.4 差异因果/无门槛|MATRIX_INPUTS/Stage2Builds、正常白武器流程|已有实现；需要补测|同弓seed1采集/护甲目标仅每构筑n1；不同seed/目标组不能归因构筑，不以单胜宣称平衡|
|C1 / 2.5 地面/背包/仓库/待领取边界|LootPickup、GainMaterial、AdventureState、AdventureRules.Plan|已有实现|历史事务/守恒19条；未拾取不进仓，局内制造装备与拾取装备分列|
|C2 / 2.5 死亡/放弃/撤离/待确认|AdventureRules.Plan/Spend、AdventureFlow.LockOutcome|已有实现|历史B05/B07异常规则；19正常矩阵无死亡/待领取，不冒充异常实战|
|C3 / 2.5 真实行为才变物资|拾取/制造/Commit、CraftingTargets/RouteScoring|已有实现|真实消费/ID与只读查询回归；UI预览不作为收益|
|C4 / 2.5 重复/故障/跨进程|CommitSettlement/Acknowledge、Camp.Commit、GroundLootStore|已有实现|历史分页、写盘、回调核对、满仓/重复提交与恢复；新变更需复跑，不因本次文档继承新PASS|
|C5 / 2.5 制造与前置|CraftingCosts/Needs、AdventureRecipes、UnlockRecipe/Manufacture|已有实现|真实木石矿等消耗/解锁链/产物，不加草药等仅有图标的经济|
|C6 / 2.5 三构筑永久成长/再次出征|Stage2Experiment+真实Camp/Flow/Loadout路径|已有实现；需要补测|历史19条制造增益/新Run/入场ID；合成预留材料明示，人工成长理解和更多路线配对未跑|
|D1 / 2.6 受影响既有回归|Invoke-LocalValidation -Stage2 -FullRegression -GameplayOnly|已有实现|历史All154P/2预期F/3NR/2UR；本次源码审计不重跑，游戏NOT_RUN|
|D2 / 2.6 100规则seed|Stage2Rules.Seeds|已有实现|历史100不同请求/含Boss，数据验证，不是物理通行|
|D3 / 2.6 20实际scene seed|Stage2Physics.Run|已有实现|历史21请求→20实际seed、393路径/148001CC步；AI关闭/敌人碰撞在，资源与出生点NavMesh接近不全冒充实际走到|
|D4 / 2.6 4武器×3seed至少12|MATRIX_INPUTS.json、Build-Driver/Invoke-Matrix|已有实现|历史19记录/57进程；不是36全因子、不是重复独立玩家样本|
|D5 / 2.6 三构筑|Stage2Builds/Rules.Builds、真实装备配置|已有实现|12属性组合与19实际循环；不新增职业系统|
|D6 / 2.6 Running/Pending/Committed异常恢复|B07Rules各Resume、B09中断恢复、矩阵身份断言|已有实现|历史多进程各自状态；某一正常循环不代表所有故障|
|D7 / 2.6 四武器独立人工|HUMAN_PLAY_PROTOCOL（仅协议）|需要补测|NOT_RUN；无独立人员/安全原生环境，不能由机器人/回调/截图替代|
|E1 / 2.7 撤离成功率|Summarize-Matrix.validSorties/extracted、实际Run身份|已有实现；需要补测|历史选定样本19/19，不是人类成功率。扩样需保留失败及统计分母，不能用缺失完成回执丢失败|
|E2 / 2.7 保留率|obtained/kept/consumed/lost逐材料|已有实现|无价值表则类别数量；分母0为NA，不计地面未拾取/不把制造转化当单纯损失|
|E3 / 2.7 净收益|assetsStart/End、runConsumed/campConsumed、守恒审计|已有实现|历史19守恒；净材料含制造转化，装备/药水/永久成长/待领取另列，不双扣|
|E4 / 2.7 单位时间|elapsedSeconds、UTC字段、netPerSimulationSecondByKind|已有实现；需要补测|当前为局内模拟窗口及含恢复到Pending墙钟；尚无统一完整入仓/制造墙钟效率，不冒充性能基准|
|E5 / 2.7 战斗效率|TotalDamageTaken/药水、attack-actions/boss-combat、phase80→81|已有实现（整局）；尚缺实现（逐敌精确观测）|普通敌逐只起止TTK NOT_RUN；Boss阶段含接近/观察不是最优TTK。先审查最小测试观测方案G4，不改伤害|
|E6 / 2.7 构筑对照/样本波动|groupsDescriptiveOnly、matchedBowSeed1Gather|已有实现；需要补测|均值/n/标准差在，配对n1；其他武器同条件构筑配对及足够重复不足，不设新玩法凑差异|
|E7 / 2.7 状态一致|restore-projections、事务/身份/随机状态断言|已有实现|历史同Run恢复及不同后继Run，唯一结算/ID不重奖；原生继续仍未跑|
|F1 / 2.8 退出/复审|报告/验收/证据及P0台账|需要补测；等待审核|自动化规模已有，完整玩家体验/原生/人工/性能与历史根因未关闭；本实施方不自行批准|
|P1 / 2.2、2.9 计划状态/正式对应|旧DEVELOPMENT_PLAN及旧6.4～6.9规范|需要修复（文档，本轮）|改为已交付待审、补正式2.1～2.9、逐项代码/证据/差异；不改历史交付结论|

## 差异清单与最小后续方案（未执行）

|ID|差异/类型|最小方案|前提/回归与范围边界|
|---|---|---|---|
|G1|计划状态和规范覆盖不完整；文档|本轮更新滚动计划、规范、此对应表与旧路线图导航|只文档校验，无产品/存档/测试框架改动，历史失败/报告不改写|
|G2|原生/四武器人工NOT_RUN；环境/补测|先取得获准独占交互环境与独立玩家，再按既有协议每武器1次，实际标题/营地/探索/结算/继续|不抢桌面/改快捷键/要求守候，不以私有桌面渲染或WM_CLOSE当原生；没有环境则保持BLOCKED|
|G3|构筑/策略因果样本不足；补测|复用现有矩阵，预登记同seed/目标/初始物品/策略配对与重复次数；先核对12最低记录的条件覆盖|先审批试验规模/时间，不删除既有失败或改难度，不新增成长机制；单样本只说明机制生效|
|G4|普通敌精确TTK与部分效率窗口缺观测；观测实现|拟在测试驱动按稳定敌人ID记录首个约定战斗动作/实际死亡时钟、阶段前后实际伤害/药水；补进程累计与暂停/回血/过量边界|仅在明确授权后加最小观测回归再实现；不改HP/伤害/AI/冷却/存档v9，不把phase时长换名当精确TTK|
|G5|完整性能基准缺证；补测/必要工具评估|先冻结硬件/分辨率/画质/负载/冷暖状态，用现有可用采样工具取得CPU/GPU/GC/内存/Draw/启动恢复有效数据|无数据则NOT_RUN；先测再给预算，不能用AI耗时、零计数推导优化，不批量性能重构|
|G6|UNKNOWN/青色帧/Search根因未定位；诊断|保存现有栈与证据；只有新因果线索/独立环境才设计定向实验|不因本计划重复关闭矩阵、吞日志、改生命周期/升级引擎；本轮UNRESOLVED|
|G7|部分UI/动作/美术仍非终稿；表现与补测|取得真实动态/人工具体反馈后，仅修与目标理解/预警/遮挡直接相关的可复现问题|不借阶段2重做B10、追加地图/商店/经济；资源存在不等于已审美验收|
|G8|若后续发现产品与合同不符；条件方案|给出稳定复现与失败回归→定位单一模块→最小修复→受影响All/正常AI/恢复/非开发构建|现在没有可据以启动的具体新产品缺陷；先提交差异请求明确授权，不把此行当通用开工许可|

G2～G8均是**提案/未执行**，本轮没有新增业务/观测代码、没有新测试运行或产品缺陷修复。v9/依赖保持，真正缺证不靠“新增系统”替代。

## 历史证据与本轮结论

已读取阶段2提交结果：100规则seed、20实际seed、19案例/57进程、三构筑、19守恒、非开发0错88警告、All154P/2预期F/3NR/2UR，0非预期F；143 Search异常与其它日志诊断继续开放。这是过去运行，不加进本次审计PASS计数，也不是独立审核认可。

- 本轮源码/文档/已提交结果存在性审计：执行，结果见[验证回执](PlanAudit/2026-10-27-stage2/validation.json)。
- 本轮规则、场景、Editor正常AI、非开发构建、正式Player、原生与人工、性能：**NOT_RUN**，原因是本轮仅审计/计划且没有代码变化。
- 当前阶段：自动化交付待独立复审，完整玩家体验退出条件未满足；UNKNOWN/青色帧/Search为UNRESOLVED，原生/人工/性能待补。
- ForestRuins和ProjectSettings原SHA256保持，不暂存/覆盖；不读取真实存档，不启动新批次。Git提交与远端核对完成后暂停等审核。


### 文档校验的首次失败（非游戏测试）

[首次检查回执](PlanAudit/2026-10-27-stage2/validation-first.json)中9项通过、1项FAIL：检查器错误要求Git规范化diff必须恰好列出两份用户文件；实际ProjectSettings只有换行/原始字节差异，规范化diff只列ForestRuins。两份用户文件的原始SHA256检查一直通过。

修正的是文档检查口径：Assets/Packages/ProjectSettings中的差异必须是已登记用户文件集合的**子集**，同时两份文件仍须逐字节SHA256相等、未删除/未暂存；不是忽略文件或放松产品测试。最终检查另写validation.json，首次FAIL不覆盖。本轮游戏/构建仍NOT_RUN。
