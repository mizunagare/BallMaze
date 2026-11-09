# UX-PROGRESSION-01 · 源码审计（只读）

> 审计基线：`design/ux-progression-01`，起点 `09e2a6eb486ee36cc6d85a60ab4f629d0c522581`
> （`verify/cp06-integration-player-02-R1` tip，已通过 CP06-INTEGRATION-02-R1 限定范围复审）。
> 审计对象：`Assets/CombatPrototype/**/*.cs`（142 个脚本）、`Assets/CombatPrototype/Resources/**`（RecipeData 29 / ItemData 25 / QualityData 5 / ContainerData 6）。
> 本文件**只做现状标注**，不含任何代码改动。所有结论均给出 `文件:行号` 依据。

---

## 0. 审计结论摘要

| 结论 | 说明 |
|---|---|
| 底层循环已闭环 | 营地 → 出征 → 探索/战斗/采集 → 撤离 → 结算 → 制造 → 再出征，全部真实存在于代码与真实存档路径中，**不需要重做**。 |
| 目标系统"有骨架、无闭环" | `ExpeditionGoal` 三值已存在并写入 `RunState.goal`（`AdventureState.cs:21,33`），但只参与路线评分与一行文案，**没有达成判定、没有局内显示、没有完成回执**。 |
| 技能配置"可选择、不成立" | 每把武器固定 2 个扩展技能 + 1 个原技能，可点击切换，但**选择不持久化、无热键、无取舍说明**，且 3 把新武器的技能走独立冷却通道。 |
| 装备成长"可制造、不可升级" | 品质 5 档 + 配方 29 条 + 铭刻定向词缀已实现；**没有单件升级/重铸**，3 把新武器**没有配方**，只能靠 3%/8% 掉落或首领保底。 |
| 地区差异"已存在、未命名" | 三地区在几何、资源、事件链、首领上确实不同，但**没有把差异表达为玩家可理解的目标**；产品自己的 HUD 文案写着"暂无主线成果"（`AdventureFlow.UI.cs:21`）。 |
| 元进度"薄但正确" | 局内等级/技能在结算时清零（`AdventureRules.cs:34`），长期留存只有仓库、材料、配方、特殊奖励、首领徽章。不是缺陷，是**设计选择**，需要显式确认为"roguelite"身份。 |

---

## 1. 系统清单

| # | 系统 | 主入口 | 关键文件 | 现状 |
|---|---|---|---|---|
| S1 | 出征目标与路线 | `AdventureFlow.UI.DrawPreparation` | `AdventureState.cs`、`AdventureFlow.UI.cs`、`RouteScoring.cs`、`CraftingTargets.cs` | 骨架完整，缺闭环 |
| S2 | 七武器与八扩展技能 | `AdventureCombat.UseSkill` | `WeaponSkillExpansion.cs`、`NewWeaponCombat.cs`、`WeaponSkillPanel.cs`、`WeaponTraits.cs` | 功能完整，缺配置与表达 |
| S3 | 装备成长与制造 | `CampWorkbenchRuntime.Manufacture` | `CraftingTargets.cs`、`CraftingRecipeDefinition.cs`、`AdventureLoadout.cs`、`AdventureItems.cs` | 制造完整，缺升级线与新武器路径 |
| S4 | 三地区定位 | `AdventureFlow.Depart` | `ForestLayout.cs`、`RuinsLayout.cs`、`CrystalCavernLayout.cs`、`RuinsExploration.cs`、`ForestRewards.cs` | 内容差异真实，目标表达缺失 |
| S5 | 长期循环与元进度 | `AdventureRules.Plan` | `AdventureRules.cs`、`HeroProgression.cs`、`CampFacilities.cs`、`Onboarding.cs` | 结算严谨，动机生成器缺失 |

---

## 2. S1 · 出征目标与路线

### 2.1 已有功能

| 能力 | 实现 | 证据 |
|---|---|---|
| 三种出征目标枚举 | `ExpeditionGoal { Gather, Treasure, Challenge }` | `AdventureState.cs:21` |
| 目标写入本次 Run | `RunState.goal`，出征时 `goal=selectedGoal` | `AdventureState.cs:33`、`AdventureFlow.cs:130` |
| 营地目标选择 UI | 三个按钮，`SelectExpeditionGoal` 仅在营地且无结算时接受 | `AdventureFlow.UI.cs:7,37` |
| 目标影响路线评分 | `targetMatch` 按目标取"宝箱/敌人/材料期望"，并给出 `NO_TREASURE_REMAINING` / `NO_ENCOUNTER_REMAINING` 排除理由 | `RouteScoring.cs:84-89` |
| 路线评分完整维度 | 目标匹配、期望产出、撤离便利、新鲜度、距离成本、目的地/路径风险、精英暴露 | `RouteScoring.cs:9-112` |
| 目标文案反馈 | `GoalFeedback` 按目标输出"本局仍持有材料 / 已开宝箱 / 击败数" | `CraftingTargets.cs:108-111` |
| 目的地推荐（文本） | `Recommendations` 输出余敌/资源/箱子/路面装备/风险/撤离方式/评分 | `CraftingTargets.cs:57-83` |
| 路线 HUD 入口 | `M 路线` 按钮 + `路线` 详情页（地点收益摘要 + 连接 + 推荐） | `PlayerHudPresenter.cs:45,134` |
| 目标 HUD 面板 | 右上角"目标"卡：制造目标 / 遗迹目标 / 洞窟提示 / 教学 | `PlayerHudPresenter.cs:46,100` |
| 制造目标追踪 | 选择后写入 `Profile.craftingTarget`，制造成功即清除（一次性） | `CraftingTargets.cs:33-48` |
| 目标合法性校验 | `(int)run.goal` 必须在 0..2 | `AdventureValidation.cs:35` |

### 2.2 缺失功能

| 缺口 | 影响 | 证据 |
|---|---|---|
| **局内完全看不到本局目标** | 标题只在"非森林探索"模式显示目标，而遗迹/洞窟同样走 `ForestExploration` 模式，故三种地区**都不会显示目标** | `AdventureFlow.UI.cs:19`、`AdventureFlow.cs:121-122` |
| 目标无达成判定 | 只有 `TestChallenge` 模式有 `targetReached`，`ExpeditionGoal` 三者均无"完成"谓词 | `AdventureFlow.cs:35,59`、`AdventureState.cs:38` |
| 目标无完成回执 | 结算不记录"本局目标是否达成"，`SettlementRecord` 无相关字段 | `AdventureState.cs:56-68` |
| 目标不影响任何收益通道 | 目标仅改评分权重，不改变掉落/结算/解锁；`Plan` 不知道 `goal` | `AdventureRules.cs:14-33` |
| 目标与地区不匹配 | 遗迹/洞窟可选"寻宝/讨伐"，但地区无对应目标定义，评分分支靠 `RuinsLayout.Is` 兜底 | `RouteScoring.cs:45,53,63` |
| 无"为什么是这个地点"的可解释输出 | 推荐是一段长文本，无 Top3 排序卡片、无取舍对比 | `CraftingTargets.cs:64-74` |
| 目标选择不持久化 | `selectedGoal` 是运行时字段，重进游戏回到 `Gather` | `AdventureFlow.UI.cs:6` |
| 无目标历史 | `committedRuns` 只存 runId，不存目标与结果 | `AdventureRules.cs:32` |

### 2.3 需要设计决策

- **D-01**：目标达成是否改变收益？（建议：不改经济，只发"首次达成"数据回执 + 走既有配方解锁/特殊奖励通道。）
- **D-02**：目标是否允许局内切换？（建议：不允许，只在营地定；局内只展示进度。）
- **D-08**：目标计数用"本局所得"还是"当前持有"？（建议：必须用 `RunState.earnedRemaining`，否则"带着材料出征→立刻达成"可被刷。）

---

## 3. S2 · 七武器与八扩展技能

### 3.1 已有功能

| 能力 | 实现 | 证据 |
|---|---|---|
| 七武器 | 长剑/长枪/法杖/弓（`GearType 0..3`）+ 双刃/巨剑/镰刀（`11..13`） | `AdventureItems.cs:5`、`NewWeaponRegistry.cs:4-11` |
| 八扩展技能 | 每把旧武器 2 个，共 8 条完整参数（冷却/前摇/段数/间隔/倍率/距离/持续/宽度/蓄力/机制） | `WeaponSkillExpansion.cs:8-17` |
| 新武器 6 技能 | 每把 2 个，独立 motor（连段/蓄力破防/冲击波/群体牵引/反击） | `NewWeaponCombat.cs:10,39-46` |
| 技能槽切换 | 面板 `技能槽0/1/2`，点击调用 `Select(slot)`，带输入屏障 | `WeaponSkillPanel.cs:5`、`WeaponSkillExpansion.cs:38`、`NewWeaponCombat.cs:22` |
| 蓄力机制 | 按住 `Skill` 进入 `Charging`，松开或达 `def.charge` 锁定后释放 | `WeaponSkillExpansion.cs:46` |
| 共享冷却 | 施放即 `PrepareExpanded(def.cooldown)` → `skillAt`，与普攻/切武器分离 | `WeaponSkillExpansion.cs:66`、`NewWeaponCombat.cs:51` |
| 词缀 6 种 | 锐利/疾风/回响/汲取/猎首/聚能，白 0 条、绿/紫 1 条、金/红 2 条 | `WeaponTraits.cs:5-8`、`NewWeaponRegistry.cs:14` |
| 定向铭刻 | 晶石碎片 ×2，替换/追加第一条词缀；金/红保留第二条 | `AdventureLoadout.cs:124`、`WeaponLoadoutView.cs`（铭刻按钮区） |
| 手持/备用双武器 | `V` 切换，只有手持词缀生效，共用技能冷却 | `AdventureLoadout.cs:122-134`、`WeaponLoadoutView.cs` 标题行 |
| 局内基础技能 6 种 | 力量/铁皮/活力/迅捷/狂热/延伸，每次升级 3 选 1，等级无上限 | `HeroProgression.cs:5,38-43,100-130` |

### 3.2 缺失功能

| 缺口 | 影响 | 证据 |
|---|---|---|
| **技能槽选择不持久化** | 存档 schema 无该字段，读档/换场景回到槽 0 | `CombatSaveData.cs:5-22`（无 `skillSlot`） |
| **无槽位热键** | 只能鼠标点面板；战斗中切槽需移开视线 | `WeaponSkillPanel.cs:5`、`PlayerBindings.cs:21`（`Skill` 唯一 F） |
| 旧/新武器两套冷却通道 | `skillAt` 复用，但 `NewWeaponCombat` 有独立 `NewSkillAt` 语义；玩家无法从 UI 判断差异 | `WeaponSkillExpansion.cs:66`、`NewWeaponCombat.cs:50-51` |
| 无取舍说明 | 技能只有一句描述，没有冷却/前摇/段数/范围的可比数值 | `WeaponSkillExpansion.cs:9-16`（description 为唯一文案） |
| 无"构筑"概念 | 没有武器组合、词缀方向、技能槽的整体视图；`角色页` 只列基础技能等级 | `CatInventoryPresenter.cs:46` |
| 新武器技能无槽位概念 | `Selected` 只有 0/1，与旧武器 0/1/2 语义不一致 | `NewWeaponCombat.cs:22`、`WeaponSkillPanel.cs:7` |
| 词缀无档次/无冲突规则 | 6 条等权，可无限铭刻替换；没有"这套词缀在追求什么"的表达 | `WeaponTraits.cs:5-8`、`AdventureLoadout.cs:124` |

### 3.3 需要设计决策

- **D-03**：技能槽配置存哪里？（建议：新增可选存档字段，缺省=槽 0，向后兼容；若 schema 冻结则退化为 `GamePreferences` 本地配置。）
- **D-04**：是否给每把旧武器增加第 3 个技能？（本批禁止：属新增内容+数值平衡，需独立批次。）
- **D-09**：新武器是否纳入统一技能目录？（建议：保留独立 motor，但对外统一"2 槽 + 共享冷却"语义，避免玩家心智分裂。）

---

## 4. S3 · 装备成长与制造

### 4.1 已有功能

| 能力 | 实现 | 证据 |
|---|---|---|
| 品质 5 档 | 普通 8 / 优良 19 / 史诗 43 / 传说 78 / 神话 132（power） | `Resources/QualityData/*.asset` |
| 装备属性模型 | `Attack = Power × attackFactor`，`Defense = Power × defenseFactor`；武器 1.0、护甲 0.4、长裤 0.3、护臂 0.35/0.2、战靴 0.2、饰品 0.5/0.2 | `AdventureItems.cs:30-35`、`ItemData/*.asset` |
| 配方 29 条 | 4 武器 ×3 高档 + 4 防具 ×3 + 饰品 ×3 + 容器 ×2 | `Resources/RecipeData/`（29 个 asset） |
| 制造成本公式 | `n=品质+1`；木 `2n`、石 `n`、矿 `2n`、晶 `n-1`、核心 `max(0,n-3)` | `CraftingTargets.cs:12` |
| 配方解锁成本 | 紫及以上需先付 `unlockCost`，含前置链 | `CraftingRecipeDefinition.cs:7-24`、`CampWorkbenchRuntime.cs:36-40` |
| 容器 6 种 | 3 胸挂 + 3 背包，提供攻击/防御/移速/采集加成 | `AdventureCatalog.cs:10`、`ContainerData/` |
| 网格背包 | 形状/旋转/占格/溢出，容器决定网格尺寸 | `AdventureLoadout.cs:22-27,60-121` |
| 制造目标追踪 | 选目标 → 显示缺口（随身/仓库/需求/缺）→ 制造后自动结束追踪 | `CraftingTargets.cs:24-48` |
| 装备来源保护 | 入场装备受保护、失败归还；本局战利品失败丢失 | `AdventureRules.cs:16-25` |
| 保底通道 | 遗迹守护者必掉紫装；洞窟 Boss 必掉紫装新武器；特殊奖励固定紫镰/紫巨剑 | `RuinsExploration.cs:66`、`CrystalCavernBossRewards.cs:39-40`、`RuinsSpecialRewards.cs:28-30,84` |
| 仓库容量 | 200 件；溢出进"待领取" | `CampRuntime.cs:11`、`AdventureRules.cs:27-31` |

### 4.2 缺失功能

| 缺口 | 影响 | 证据 |
|---|---|---|
| **单件装备不可升级/重铸** | 追求只有"换更好的"，没有"把手上这把养起来" | 无对应 API；`AdventureLoadout` 只有 `Craft/Engrave` |
| **新武器无配方** | 双刃/巨剑/镰刀只能 3%/8% 掉落或首领保底 | `RecipeData/` 无 `weapon_twin_blades` 等；`NewWeaponDropRules.cs:4` |
| 词缀不可拆解/不返还 | 铭刻只增不减，错误投资无法回收 | `AdventureLoadout.cs:124` |
| 无同部位对比 | 背包/仓库不显示"换上后攻击/防御变化" | `WeaponLoadoutView.cs`、`CatInventoryPresenter` 无 diff |
| 制造目标是"一次性" | `Manufactured` 立即清除，玩家要重新选下一步 | `CraftingTargets.cs:47-48` |
| 无套装/协同 | 词缀、武器、容器之间无组合奖励 | 无对应数据 |
| 结算不汇总"下一局准备" | 结算页只列得失，不列"你还缺什么/下次去哪" | `AdventureFlow.UI.cs:54-71` |

### 4.3 需要设计决策

- **D-05**：新武器是否给配方？（建议：本批维持掉落+保底；若要给，需明确"新增经济通道"并获得授权。）
- **D-10**：是否引入单件升级？（本批禁止：直接改武器伤害/经济。替代方案：铭刻定向 + 品质跳档 + 藏品，已可实现"持续追求"。）
- **D-11**：词缀是否允许拆除返还？（涉及材料回收=经济变动，建议延后。）

---

## 5. S4 · 三地区定位

### 5.1 已有功能（客观差异）

| 维度 | 森林 `ForestRuins` | 古代遗迹 `AncientRuins` | 水晶洞窟 `CrystalCavern` |
|---|---|---|---|
| 版本 | `revision 5`，可选双首领 `bossVersion=1` | `revision 6`，`ruinsStage 5`（或 3 短版） | `revision 7/8/9/10`，C2.1→C2.4 |
| 兴趣点 | 7（入口/伐木林地/碎岩矿脉/遗迹营地/精英哨站/归途祭坛/湖岸物资点） | 5（入口/石柱广场/机关走廊/地下祭坛/守护者大厅） | C2.4 共 9（入口/矿脉/能量通道/隐藏矿室/湖/外环/内环/对岸/前室/竞技场） |
| 采集点 | 42 个（木 18 / 石 12 / 矿 12），每次 3–6 | **0**（设计上无矿脉） | 4 个（矿 2 / 晶 2） |
| 遭遇 | 11 普通/精英 + 2 首领（典狱长/潮汐） | 4（守卫/弓手/精英/守护者） | 4（矿脉巡守/晶核精英/内环巡守/晶脊守望者） |
| 首领 | 2，可选，永久徽章 + 首次奖励 | 1，可选，首次奖励 + 紫装保底 | 1，可选，首次奖励 + 紫装新武器保底 |
| 出口 | 3（入口免费/祭坛免费/渡口需木 2 石 1） | 2（入口/大厅，均免费） | 1（入口免费） |
| 事件链 | 无强制链，POI 自由 | **强链**：机关→石门→碑文→密室箱；`Objective` 逐段变化 | **空间机关**：矿室拉杆、湖桥拉杆、Boss 挑战祭坛 |
| 独有收益 | 新武器 3%/8% 掉落；哨站精英额外晶石；遗迹点 100% 宝箱装备 | 5 个永久特殊奖励（钥/残卷/印/遗镰/守护者初誓） | 首次击杀"晶脊初誓"；矿石/晶石密度最高 |
| 风险源 | 地形（湖/山脊）+ 精英哨站 + 2 首领 | 门/机关阻挡 + 守护者 | 能量脉冲伤害区 + 精英 + Boss |

证据：`ForestLayout.cs:19-52`、`RuinsLayout.cs:12-29`、`CrystalCavernLayout.cs:39-168`、`ForestRewards.cs:26-36`、`RuinsExploration.cs:12,60-75`、`CrystalCavernBossRewards.cs:28-60`。

### 5.2 缺失功能

| 缺口 | 影响 | 证据 |
|---|---|---|
| 森林无"地区目标" | 只有 POI 收益标签，没有"这局来森林做什么"的正式目标 | `ForestRewards.cs:54-61` 仅 `Summary` 一行 |
| 遗迹目标不可复用 | `RuinsExploration.Objective` 硬编码在 MonoBehaviour，无法被 HUD/结算复用为契约 | `RuinsExploration.cs:12` |
| 洞窟目标只是提示文案 | 按 `contentRevision` 分支输出一句提示，无进度 | `PlayerHudPresenter.cs:100` |
| 三地区无统一"目标卡"结构 | 三套文案、三种来源，玩家无法比较"去哪更值" | 上述三处分散实现 |
| 地区差异未量化展示 | 无"资源/挑战/奖励"三轴对比 | 无对应 UI |
| 遗迹无资源供给被当作缺陷 | 真实设计事实，但未在玩家侧解释"这里靠箱子与守护者" | `RuinsLayout.cs:18`、`CraftingTargets.cs:60` 仅一句"宝箱矿石与晶石" |

### 5.3 需要设计决策

- **D-12**：遗迹是否补矿脉？（建议：不补。保持"无采集、高保底"的身份；用目标卡解释。）
- **D-13**：是否给三地区加"难度档/推荐装备等级"？（涉及敌人数值=经济，需独立批次；本批只做"推荐准备"文案，不改数值。）

---

## 6. S5 · 长期循环与元进度

### 6.1 已有功能

| 能力 | 实现 | 证据 |
|---|---|---|
| 结算规则 | 成功=带回本局装备/材料/药水；失败=归还入场、丢失本局、清等级与临时技能 | `AdventureRules.cs:13-33` |
| 局内成长清零 | 回营 `level=1 / experience=0 / skills=0` | `AdventureRules.cs:34` |
| 永久留存 | 仓库（200）、材料、`unlockedRecipes`、`specialRewards`、`bossHunts`、`badges`、`regions` | `AdventureState.cs:12-18` |
| 配方永久解锁 | 成功撤离时把 `pendingRecipeProofs` 及其前置写入 `unlockedRecipes` | `AdventureRules.cs:28-31` |
| 首领讨伐记录 | 次数 + 回执 + 徽章；双首领额外徽章 | `ForestBossRules.cs:53-64` |
| 特殊奖励回执 | 6 个 ID，含"已领取/待领取"一致性校验 | `RuinsSpecialRewards.cs:16-23,76-134` |
| 待领取区 | 仓库满/材料溢出/特殊奖励都进 `pending`，需显式领取 | `AdventureFlow.UI.cs:76-88` |
| 新手引导 13 阶段 | 装备→仓库→工作台→出征→移动→采集→拾取→免费出口→结算→领取→制造→再出征→完成 | `Onboarding.cs:5` |
| 营地 4 设施 | 装备整备/永久仓库/营地工作台/森林出征 | `CampFacilities.cs:6-8` |
| 存档严谨性 | 版本校验、修订号、发布确认、待核对态 | `CombatSaveSystem.cs`、`AdventureFlow.cs:186-213` |

### 6.2 缺失功能

| 缺口 | 影响 | 证据 |
|---|---|---|
| **产品自认"暂无主线成果"** | HUD 直接写着这句话 | `AdventureFlow.UI.cs:21` |
| 无"下一局动机"生成器 | 结算后没有"你现在最该做什么"的下一步 | `AdventureFlow.UI.cs:54-71` |
| 地区精通无定义 | 三地区没有"掌握度"概念；`regions` 只有森林双首领一个标记 | `ForestBossRules.cs:54` |
| 无目标历史/统计 | `committedRuns` 只有 runId；无"本目标完成次数/最好成绩" | `AdventureRules.cs:32` |
| 无长期展示面 | 角色页只有基础技能等级与藏品一行 | `CatInventoryPresenter.cs:46` |
| 引导结束后无承接 | `TutorialStage.Complete` 之后无"第一个长期目标"推荐 | `Onboarding.cs:5,20` |

### 6.3 需要设计决策

- **D-06**：是否引入持久角色等级？（建议：**不引入**。保持 roguelite 身份；否则要改经验曲线，属禁区。）
- **D-07**：地区精通是否给数值？（建议：只给展示与既有解锁通道，不给战斗数值。）
- **D-14**：是否记录"目标历史"？（建议：新增只读统计，不参与结算奖励。）

---

## 7. 存档契约影响面

| 设计所需数据 | v9 现状 | 是否需新字段 | 风险 |
|---|---|---|---|
| 本局目标 | `RunState.goal` 已存在 | 否 | 无 |
| 目标进度 | 可由 `earnedRemaining` / 事件 `Used` / 敌人 `Dead` 实时推导 | 否（推荐） | 无 |
| 目标完成回执 | 无 | 是（`SettlementRecord` + `ProfileState`） | 需 schema 修订与迁移 |
| 技能槽配置 | 无 | 是（或退化为本地配置） | 需 schema 修订 |
| 地区精通 | 部分（`specialRewards`/`badges`） | 可复用，不必新增 | 无 |
| 目标历史统计 | 无 | 是（可选） | 需 schema 修订 |

**结论**：S1 的可视化与进度**零 schema 改动**即可落地；"完成回执/技能槽/历史"三项需要一次显式的存档修订决策（D-15），不得在实现批次里顺手改 schema。

---

## 8. 复用清单（明确"不要重复实现"）

1. `RouteScoring.Evaluate/Ranked` —— 路线评分与排除理由，**已完整**。
2. `CraftingTargets.Needs/Details/Recommendations` —— 缺口与推荐，**已完整**。
3. `RuinsExploration.Objective` 的阶段文案 —— 遗迹目标链，**已有**，只需上提为契约。
4. `RuinsSpecialRewards.Earn/Earned` —— 永久回执通道，**已有**。
5. `CrystalCavernBossRewards.Drop` —— 首领保底，**已有**。
6. `ForestRewards.ChestRanges/ChestGearChance` —— 地点收益表，**已有**。
7. `WeaponSkillCatalog.All` + `WeaponSkillDefinition` —— 8 技能参数，**已有**。
8. `WeaponTraits` + `Engrave` —— 词缀与铭刻，**已有**。
9. `AdventureRules.Plan` —— 结算得失，**已有且严谨**。
10. `CampWorkbenchRuntime.UnlockRecipe/Manufacture` —— 制造事务，**已有**。
11. `Onboarding` 13 阶段 —— 新手漏斗，**已有**。
12. `PlayerHudPresenter` 目标卡/路线页 —— 信息承载点，**已有**，扩展即可。

---

## 9. 审计方法与可复核性

- 只读检索：`Grep`/`Read` 于 `Assets/CombatPrototype`，未执行任何写入或构建。
- 资源清单：`Assets/CombatPrototype/Resources/RecipeData`（29）、`ItemData`（25）、`QualityData`（5）、`ContainerData`（6）。
- 数值来源：`QualityData/*.asset` 的 `power` 字段、`ItemData/*.asset` 的 `attackFactor/defenseFactor`、`ForestLayout.Generate` 的常量。
- 本文件与 `DESIGN.md` 的所有"已有"结论均可在上述行号直接复核；任何与代码不符之处以代码为准，并在复审时修订本文。
