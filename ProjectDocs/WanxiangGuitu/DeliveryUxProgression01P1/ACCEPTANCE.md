# UX-PROGRESSION-01 P1 · 验收映射（ACCEPTANCE）

判定只用真实 Player 断言（`assertions.tsv`）与源码审计，二者都可复核。
`PASS` 仅当证据存在；缺证据一律 `NOT_RUN`，**不推算、不代填**。

- 证据根：`Evidence/Player/<run>/assertions.tsv`、`run-summary.json`、`int-events.jsonl`
- 13 条 Run 全部 `verdict=PLAYER_RUN_COMPLETED`、`exitCode=0`、`complete.txt=PASS`
- 合计 **1465 PASS / 0 FAIL / 9 SKIP**（SKIP 全部且仅为非遗迹地区的 `p1-ruins-no-vein-notice`）
- 本轮 build SHA（`Assembly-CSharp.dll`）= `ce03e64171bd136b7549182d2985f8c50328c23ef2a06fb3777732f7bfa06d3c`
- 驱动 SHA = `49c81de5c4e8660340ec8cf8c2a5695892c18ec802b7c486ac56bb3133250695`

## A. B0 类（目标系统）

| # | 条目 | 判定方式 | 断言/证据 | 结论 |
|---|---|---|---|---|
| B0-01 | 目标卡定义完整（9/9，1–3 条件，只读可判定） | 源码 + 矩阵 | `grep -c "new ObjectiveCard(" == 9`；`OBJECTIVE_CARD_MATRIX.csv` 9 行 × 14 列且逐行含 `source_evidence` / `minimum_yield_proof` | **PASS（源码）** |
| B0-02 | 局内目标可见（3 地区 × 3 目标 × 2 次进入 = 18/18） | 真实 Player | `-hud-card-matches-goal` 37 PASS / `-hud-line1` 37 / `-hud-line2-budget` 37 / `-hud-line3` 37；每地区 2 个 Run × 3 目标 × 2 轮 = 12 次，9 张卡各 ≥2 次，18/18 覆盖 | **PASS** |
| B0-03 | 进度真实（与场景真实计数一致，0 帧容差 + 刷新窗口） | 真实 Player | `-progress-not-below-held` 37（驱动侧 `P1IndependentPrimary` 独立计数，不复用求值器）、`-hud-tracks-progress` 7（如 `hud=18,evaluator=18,cardId=forest.gather`）、`-progress-moved` 7（非回退断言 `after>=before`） | **PASS** |
| B0-04 | 反刷（带 30 木材不采集 = 0；消费后不回退） | 真实 Player | `p1-carried-is-zero: hud=0,carried=30,earned=0`；`p1-counter-harvest: earned=18 want=12`；`p1-spend-no-regress: spent=True,before=18,after=18,spentRecorded=5,earnedNow=13` | **PASS** |
| B0-05 | 路线 Top3 与 `RouteScoring.Ranked` 一致 | 真实 Player | `-route-top3-order` 37 PASS，逐项比对 `Top3Ids` 与 `RankedIds` 前缀（如 `poi:2>poi:1>poi:4 vs poi:2>poi:1>poi:4>poi:6>…`） | **PASS** |
| B0-06 | 排除理由可读、无内部常量泄漏 | 真实 Player | `-route-excluded` 37 PASS，输出仅中文短语（如 `隐藏矿室 · 无通行路径`） | **PASS** |
| B0-07 | 结算"下一局三件事"（3 地区 × 成功/失败） | 真实 Player | `-settlement-next-steps` 37 PASS，三条均非空；成功路径例（洞窟/掘脉）与失败路径例（森林/扫箱）均归档 | **PASS** |
| B0-08 | 地区身份卡（一句话 + 三轴 + 推荐目标） | 真实 Player | `p1-prep-region-card` 13 PASS（≥4 行）；`p1-ruins-no-vein-notice` 4 PASS + 9 SKIP（非遗迹地区语义性跳过，见限制 §L2） | **PASS** |
| B0-09 | 零经济改动（产出/掉落/宝箱/配方/结算得失 diff = 0） | 保护文件 diff | `Evidence/PROTECTION_HASHES.tsv` 22/22 `identical=YES`（含 `AdventureRules.cs`、`ForestRewards.cs`、`RuinsExploration.cs`、`CrystalCavernLayout.cs`、`CraftingTargets.cs`、`PlayerInventory.cs`） | **PASS** |
| B0-10 | 零随机调用（新增代码对 `AdventureRandom` 调用 = 0） | 静态检索 | `grep -n "AdventureRandom" {ObjectiveCatalog,ObjectiveEvaluator,AdventureFlow.Objectives,RouteCards,SkillTradeoffs}.cs` → 0 命中 | **PASS（源码）** |
| B0-11 | 失败不加重（死亡/放弃结算字段与基线一致） | 真实 Player + diff | `AdventureRules.cs` blob 与基线逐字节相同；`-death-outcome-kind: Death`、`-abandon-confirm` 32 PASS、`-death-commit` / `-abandon-ack` 全部 PASS | **PASS** |
| B0-12 | 跨进程恢复；发生过消费时允许 `exact=false` 且不得高于重进前 | 源码 + 真实 Player | 3 地区成对跨进程：`-xproc-same-run` 3、`-xproc-from-save-flag` 3、`-xproc-not-exact-after-spend` 3、`-xproc-hud-value-not-above-persisted` 3、`-xproc-persisted-bound-matches-held` 3，全 PASS | **PASS** |
| B0-13 | 只读求值器（1000 次求值后语义快照与随机流逐字不变） | 真实 Player | `evaluator-readonly` 7 PASS：`revision=3->3,rngSame=True,saveSame=True,calls=1000` | **PASS** |
| B0-14 | 世界卸载后结算快照仍可显示 | 真实 Player | `-settlement-snapshot` 37 PASS（`card=<id>`），且在 `AcknowledgeSettlement()` 之后读取（此时 `ActiveRun==null`，见 `p1-no-objective-reward: activeRun=null`） | **PASS** |

## B. B1 类（武器 / 技能 / 铭刻）

| # | 条目 | 判定方式 | 断言 | 结论 |
|---|---|---|---|---|
| B1-01 | 7/7 武器统一"2 扩展槽 + 基础动作"语义 | 源码 + 真实 Player | `p1-weapon-roles-7` 13 PASS（7 武器均有角色与理由）；`WeaponSkillPanel` 槽标签 `[0] 基础动作` / `[i] 名称`；`p1-hotkey-1/2` 在 `modern`/旧武器两种分支下取值 0/1 vs 1/2 | **PASS**（运行时只覆盖当前手持武器的分支，见 §L3） |
| B1-02 | 14/14 技能取舍条完整（无值显示"—"） | 真实 Player | `p1-skill-rows-14` 13、`p1-skill-row-fields` 13、`p1-skill-dash-for-missing` 13，全 PASS | **PASS** |
| B1-03 | `1/2` 切槽生效且不触发技能 | 真实 Player | `p1-hotkey-1` 7、`p1-hotkey-2` 7、`p1-hotkey-no-cast` 7（冷却值切换前后不变），输入为真实 `KeyboardState` 事件 | **PASS** |
| B1-04 | 不误触（UI 打开 / 翻滚中） | 真实 Player | `p1-hotkey-ui-blocked` 7、`p1-hotkey-roll-blocked` 7 | **PASS** |
| B1-05 | 铭刻"不可逆"常驻提示 | 真实 Player | `p1-engrave-warning` 13 PASS（两处 UI 共用 `AdventureLoadout.EngraveWarning/EngraveShort`，均含"不可逆"/"不返还"） | **PASS** |

## C. 负例（10 条）

| # | 负例 | 断言 / 证据 | 结论 |
|---|---|---|---|
| N-01 | 带 30 木材不采集 → 进度 0 | `p1-carried-is-zero: hud=0,carried=30,earned=0` | **PASS** |
| N-02 | 采 12 后消费 5 → 进度不回退 | `p1-spend-no-regress: before=18,after=18,spentRecorded=5` | **PASS** |
| N-03 | 未撤离时不得判达成 | `-no-false-positive` 37 PASS（撤离前 `achieved=false`） | **PASS** |
| N-04 | 死亡不达成 | `p1-forest-treasure-death-outcome-kind: Death` + `p1-forest-treasure-fail-not-achieved: achieved=False` | **PASS** |
| N-05 | 放弃不达成 | `p1-ruins-challenge-fail-not-achieved`、`p1-cavern-treasure-fail-not-achieved`（`-fail-not-achieved` 3 PASS） | **PASS** |
| N-06 | 条件满足但失败 → 角标为"未成功撤离" | `p1-forest-treasure-fail-badge: 目标条件已满足但未成功撤离 · 扫箱 · 森林` | **PASS** |
| N-07 | 不可达目标不显示为可选 | `ObjectiveCatalog.For` 只返回真实卡；遗迹 Gather 已由不可达的 8 单位修正为可达的 6 单位（`OBJECTIVE_CARD_MATRIX.csv` `revised_in_p1`） | **PASS（源码）** |
| N-08 | 测试模式不显示地区目标卡 | `PreparationObjectiveLine` 在 `SelectedRegion()==null` 时返回"本局为测试模式：无地区目标卡（目标卡只在森林/遗迹/洞窟生效）" | **PASS（源码）** |
| N-09 | UI 打开 / 翻滚中按 `1/2` 不改槽位 | `p1-hotkey-ui-blocked` 7、`p1-hotkey-roll-blocked` 7 | **PASS** |
| N-10 | 目标层不发奖励（结算后无 ActiveRun、无额外物品） | `p1-no-objective-reward: activeRun=null`（7 PASS）；`AdventureFlow.Objectives.cs` 无 `Earn`/`DropLoot`/`TryRemove` 调用 | **PASS** |

## D. C 类（本批不做，标 `NOT_RUN`）

| # | 条目 | 原因 |
|---|---|---|
| C-01 | 技能槽持久化（D-03） | 本批冻结：不持久化 → `NOT_RUN` |
| C-02 | 目标奖励发放与永久回执（P2） | 本批为纯显示层 → `NOT_RUN` |
| C-03 | 遗迹矿脉补充（D-12 / D-04） | 明令禁止 → `NOT_RUN` |
| C-04 | 难度档、第 3 技能、单件升级、新武器配方 | 明令禁止 → `NOT_RUN` |
| C-05 | v10 schema 变更 | 明令禁止 → `NOT_RUN` |

## E. 合计

| 类别 | 条目数 | PASS | NOT_RUN |
|---|---|---|---|
| B0 | 14 | 14 | 0 |
| B1 | 5 | 5 | 0 |
| 负例 | 10 | 10 | 0 |
| C 类 | 5 | 0 | 5（按设计冻结） |
| **总计** | **34** | **29** | **5** |
