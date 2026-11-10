# 证据索引 · UX-PROGRESSION-02

基线 `design/ux-progression-02` ← `verify/ux-progression-01-p1c` @ `4550348f17890965a760fb42822d5178e50d002e`

本批是**只读审计**，因此证据不是 Player Run，而是「源码行号 + 配置数值 + 对 P1C 原始断言的再引用」。
所有引用均可用文末命令逐条复核。

---

## 1. 交付文件

| 文件 | 作用 | 主要依据 |
|---|---|---|
| `REPORT.md` | 总报告：五域结论、关键读数、边界自证 | 全部 |
| `WEAPON_ROLE_MATRIX.csv` | 7 武器 × 24 列（判定形状、区间、时序、取消、弹体、词缀作用、证据行号、缺口） | `AdventureCombat.cs`、`GreatswordCombat.cs`、`ScytheCombat.cs`、`NewWeaponCombat.cs`、`NewWeaponRegistry.cs` |
| `WEAPON_ROLE_CARDS.md` | 7 张角色卡（含「适合谁 / 什么时候变差 / 未验证项」） | 同上 |
| `SKILL_BUILD_MATRIX.csv` | 14 技能 × 23 列（含 `vs_slot0` 对比、暂停/取消语义、品质联动） | `WeaponSkillExpansion.cs`、`SkillPhysicalEffects.cs`、`WeaponHit.cs` |
| `EQUIPMENT_AFFIX_MATRIX.csv` | 6 词缀 + 5 品质 + 铭刻 + 容器 + 分解 + 叠加 | `WeaponTraits.cs`、`AdventureItems.cs`、`AdventureLoadout.cs`、`ContainerData/*.asset` |
| `EQUIPMENT_GAPS.md` | 8 条装备缺口（G1–G8）与「现有系统是否足够」判定 | 同上 |
| `CRAFTING_PROGRESSION_MATRIX.csv` | 7 类制造目标 × 解锁/成本/瓶颈/局数估算 | `RecipeData/*.asset`（29 个）、`CraftingCosts.cs`、`CraftingTargets.cs` |
| `REGION_MOTIVATION_MATRIX.csv` | 三地区 17 列（首次/重复价值、稀缺材料、一次性/可重复奖励、保底线、耗尽后动力） | `ForestLayout.cs`、`RuinsLayout.cs`、`CrystalCavernLayout.cs`、`RuinsSpecialRewards.cs`、`CrystalCavernBossRewards.cs` |
| `NEXT_RUN_MOTIVATION_AUDIT.md` | 三段建议的生成规则转录 + 六问审计 + 可实施修正（只提案） | `AdventureFlow.Objectives.cs`、`RouteScoring.cs`、`ObjectiveEvaluator.cs` |
| `Evidence/NEXT_RUN_REPLAY_MATRIX.csv` | 用 P1C 三条真实 Run 反查建议的实际输出字符串 | `DeliveryUxProgression01P1C/Evidence/Player/*/assertions.tsv` |
| `DESIGN_OPTIONS.md` | A/B/C 三方向的依赖、成本、风险、顺序 | 上述全部 |
| `DECISIONS_REQUIRED.md` | D-16 ～ D-24 九条新决策 | 上述全部 |
| `ROADMAP.md` | UX-03 ～ UX-06 批次划分、前置、验收口径、风险登记 | 上述全部 |

---

## 2. 源码引用锚点（可直接 grep 复核）

| 事实 | 位置 |
|---|---|
| 7 武器枚举与三把新武器 | `NewWeaponRegistry.cs:1-40` |
| 普攻释放比例表 `basicRelease` | `AdventureCombat.cs:37` |
| 技能释放比例表 `skillRelease` | `AdventureCombat.cs:181` |
| 普攻间隔/指向辅助 | `AdventureCombat.cs:71` |
| 近战几何（dot → 半角） | `AdventureCombat.cs:60-90` |
| 巨剑蓄势下劈 | `GreatswordCombat.cs:3,5,6,10` |
| 镰刀弧形 + 牵引 | `ScytheCombat.cs:3,5,6,10` |
| 双刃三段 + 反击 | `NewWeaponCombat.cs:10,11,12,32,43,44` |
| 14 个扩展技能定义 | `WeaponSkillExpansion.cs:9-16,39,46,53` |
| 留场符阵生命周期 | `SkillPhysicalEffects.cs:18-25` |
| 词缀生效点 `WeaponHit.Apply` | `WeaponHit.cs:7-11` |
| 回响/聚能的实际分支 | `AdventureCombat.cs:151,186-189` |
| 品质 Power 表 | `QualityData/*.asset`（白 8 / 绿 19 / 紫 43 / 金 78 / 红 132） |
| 单件攻击/防御系数 | `AdventureItems.cs:30-35,52`；`ItemData/*.asset` |
| 装备尺寸由类型决定 | `GearItem.BaseSize`（`AdventureItems.cs:27`） |
| 盘内叠加 `Active.Sum(Attack)` | `AdventureLoadout.cs:19-22` |
| 铭刻（不可逆） | `AdventureLoadout.cs:9,128-136` |
| 分解返还 | `AdventureLoadout.cs:208-212` |
| 制造目标 `(int)type < 9` | `CraftingTargets.cs:20` |
| 制造解锁与成本 | `CraftingCosts.cs:12`；`CampWorkbenchRuntime.cs:17-38` |
| 新武器掉率 | `NewWeaponDropRules.cs:4-7` |
| 洞窟首领奖励（含紫 10%） | `CrystalCavernBossRewards.cs:28-60` |
| 遗迹每箱必掉装备 | `ForestRewards.cs:37` |
| 遗迹 5 件藏品 | `RuinsSpecialRewards.cs:13-19,78-96` |
| 三地区布局与出口 | `ForestLayout.cs:33,39,46`；`RuinsLayout.cs:14-29`；`CrystalCavernLayout.cs:47-71,102-130` |
| 目标卡与建议 | `ObjectiveCatalog.cs`；`AdventureFlow.Objectives.cs`；`ObjectiveEvaluator.cs:40-62` |
| 路线排序输入 | `CraftingTargets.cs:57-83`；`RouteScoring.cs:84-89`（读 `ExpeditionGoal` **枚举**当 `targetMatch` 代理，全文件 0 处 `Objective`/`achieved` → 不读目标卡与进度） |

---

## 3. 对 P1C 证据的再引用（未重跑）

| 引用内容 | 来源 |
|---|---|
| 三条 Run 的结算文案（`目标达成 · 拔点/守誓/试锋 · 地区`） | `DeliveryUxProgression01P1C/Evidence/Player/p1c-*/assertions.tsv`（`p1c-badge`） |
| 目标进度与达成 | 同上（`p1c-objective-progress`、`p1c-objective-met`、`p1c-achieved`） |
| 下一局建议的实际字符串 | 同上（`p1c-next-steps`）→ 汇总进 `Evidence/NEXT_RUN_REPLAY_MATRIX.csv` |
| 真实击杀读数（8 / 10 / 10 次命中；290 / 320 / 360 → 0） | 同上（`p1c-fight-enemy-dead`、`-player-melee-damage`） |

**本批未启动任何 Player 进程**，上述引用全部是读取既有文件。

---

## 4. 复核命令

```bash
# 1. 本批零产品改动
git diff --stat 4550348f1 HEAD -- Assets ProjectSettings Packages
git diff --name-only 4550348f1 HEAD | grep -E "\.cs$"     # 应为空

# 2. 只有一处交付目录 + 两份状态增量
git diff --name-only 4550348f1 HEAD | grep -v "^ProjectDocs/"

# 3. 14 个扩展技能数量
grep -c "case \"" Assets/CombatPrototype/WeaponSkillExpansion.cs   # 或读矩阵行数-1

# 4. 配方组成（29 = 27 gear_* + 2 container_*）
ls Assets/CombatPrototype/Resources/RecipeData/*.asset | wc -l
ls Assets/CombatPrototype/Resources/RecipeData/*.asset | grep -c "gear_"

# 5. 新武器无配方入口
ls Assets/CombatPrototype/Resources/RecipeData/ | grep -iE "twin|great|scythe"   # 应为空

# 6. 路线与目标的耦合边界（读枚举，不读卡片）
grep -n "ExpeditionGoal" Assets/CombatPrototype/RouteScoring.cs      # 应命中 84-89 行
grep -n "Objective\|achieved" Assets/CombatPrototype/RouteScoring.cs # 应为空（不读目标卡与进度）
grep -n "Ranked\|RouteScoring" Assets/CombatPrototype/AdventureFlow.Objectives.cs  # 应为空（结算不读路线）

# 7. 回响对普攻无效（普攻 Release 不读 area）
grep -n "area\|reach" Assets/CombatPrototype/AdventureCombat.cs | head
```

---

## 5. 证据缺口（本批无法补齐的）

| 缺口 | 为什么补不了 | 需要什么 |
|---|---|---|
| 每地区重复性（≥3 局） | 本批只做审计，禁止重跑 Player | 下一批（UX-03 回归或专项重复性批） |
| 7 把武器的手感差异 | 源码不可得 | 人工复玩或 7 条真实武器 Run |
| 14 个技能的实际释放 | P1C 只用了长剑 | 专项技能批（真实按键释放 + `MeleeObservation` 记录） |
| 装备品质分布 | 多局统计才能得出 | 重复性批 |
| UI 实际渲染 | 本批只读文案生成逻辑 | UI 走查批 |
