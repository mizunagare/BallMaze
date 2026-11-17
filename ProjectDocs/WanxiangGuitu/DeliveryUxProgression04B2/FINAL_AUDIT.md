# UX-04-B2-FINAL · 装备收藏与库存管理最终审计

> 审计类型：**提交前只读审计**（不修改产品代码、不新增 Player Run、不重新构建、不暂存、不提交）
> 审计基线：`95caf234256613d4a6e4f89a8ab0dc09c397c6b2`
> 审计分支：`feature/ux-progression-04-b2`
> 执行日期：2026-11-16
> 结论标记：**[S]** 源码事实 · **[E]** Player 证据 · **[C]** 计算结果 · **[D]** 设计推论 · **[H]** 未验证假设

---

## 0. 结论摘要

# 结论：CONDITIONAL_PASS

**本结论不构成提交授权。** 九个审计章节中，A（Git）、B（攻击力模型独立复算）、F（存储兼容）、G（41 项保护域）、H（80 份证据）全部通过；C/D/E 三章存在 **7 项必须清除的条件项**（编号 C-01…C-07），其中 **C-01 / C-02 / C-03 涉及产品源码缺陷**，需负责人另行授权修复批次并重新验收后方可提交。

| 判定依据 | 结果 |
|---|---|
| 硬门禁（保护域 / v9 Schema / D-24 / 攻击系数 / 掉落随机流 / 制造成本 / 用户存档 / 证据完整性） | ✅ 全部 PASS，零改动 |
| B2-01 攻击力统一计算链（最高技术风险项） | ✅ **独立第三方复算 21/21 逐位相等** |
| B2-03 装备比较 / B2-05 容量与仓满反馈 | ✅ PASS |
| B2-02 排序 / B2-04 收藏整理 / IMGUI 控件放置 | ⚠️ 存在未披露缺陷，见 §11 |
| 交付文档与实现一致性 | ⚠️ `RISK_REGISTER.md` R-16、`INVENTORY_FILTERS.md` §排序、B2-02 PASS 声明与源码事实不符 |

> 为何不是 BLOCKED：未发现保护域破坏、存档/Schema 改动、数据丢失、证据伪造或验收造假；全部失败均为「保守拒绝 / 显示层缺陷 / 功能未接线」，不产生不可逆后果。
> 为何不是 PASS：C-01/C-02/C-03 属授权范围内的功能性缺陷且交付文档已声明「已实现/已消除」，文档与实现不一致，不得在只读审计中默认为通过。

---

## 1. 审计范围与只读纪律

| 项 | 状态 |
|---|---|
| 修改产品源码 | ❌ 未发生（`git diff HEAD` 仅 B2 实施批次的 5 文件，本轮未新增改动） |
| 新增 Player Run / 重新构建 | ❌ 未发生（仅复算与读取既有证据） |
| `git add` / 暂存 / 提交 / 推送 | ❌ 未发生（staged=0） |
| 合并 main / 启动 UX-05 | ❌ 未发生 |

本轮所有计算均为**离线复算**（Python float32 预言机）与**只读源码审读**，未调用任何 Unity 运行时、未触碰产品状态。

---

## 2. A · Git 审计 — PASS [S]

| 检查 | 值 |
|---|---|
| HEAD | `95caf234256613d4a6e4f89a8ab0dc09c397c6b2`（= 基线，本分支零提交） |
| tree | `e46232da0b87c97c39174fe58737c394a773b649` |
| branch | `feature/ux-progression-04-b2` |
| `git status --porcelain=v2` | 5 个 `.M` + 3 个 `? B2*.cs` + 其余为历史 untracked |
| `git diff --cached` | **空** ✅ |
| `git diff --check HEAD` | **clean** ✅ |
| `git diff HEAD --stat` | 5 files, `+110 / −34` |

**3 个新增源文件** [S]：`B2AttackModel.cs`、`B2InventoryQuery.cs`、`B2Collection.cs`
**5 个修改文件** [S]：`AdventureLoadout.cs`、`CatInventoryPresenter.cs`、`ContainerInventoryView.cs`、`CampRuntime.cs`、`CampInventoryView.cs`

| 确认项 | 结论 |
|---|---|
| 3 新增 + 5 修改，符合授权范围 | ✅ 8 个文件全部落在 B2-01~B2-05 批准范围 |
| 未修改存档 Schema | ✅ `CombatSaveData.cs`/`CombatSaveSystem.cs`/`AdventureValidation.cs` 零改动 |
| 未修改掉落 / 随机流 / 制造成本 | ✅ 相关 20 文件逐项 `git diff --quiet` 全部 UNCHANGED |
| 未修改 AdventureLoadout 攻击力计算系数 | ✅ `Attack`/`Defense` 仅改为委托 `B2AttackModel` 纯函数，表达式逐字等价（§3） |
| staged 为空 | ✅ `diff --cached --name-only` = 0 |
| 无无关产品源码修改 | ✅ `Assets/CombatPrototype/` 下受跟踪改动恰为上述 5 个 |
| B1 / UX-03 未被覆盖 | ✅ HEAD 即 B1 提交 `95caf2342`，其父 `e18dc50ca` 为 UX-03 提交，提交链完整 |
| 用户原有修改完整保留 | ✅ `Assets/Resources.meta`、历史 `Evidence/`、`ProjectDocs/` 历史交付目录 4 个 Unity 设置文件全部原状态（§7/§8） |

---

## 3. B · 攻击力模型独立审计 — PASS [S][C]

### 3.1 独立复算方法（不信任 GOLDEN Run 汇总）

审计要求「从原始装备输入复算，不能直接相信 GOLDEN Run 的汇总结果」。本次建立**第三方 float32 预言机**：

- **输入全部从源码/`*.asset` 原始定义取得**（非从 Run 读取）：
  - `QualityData/{White,Green,Purple,Gold,Red}.asset` → `power = 8 / 19 / 43 / 78 / 132` [S]
  - `*.asset` `attackFactor`：七武器 = 1、`accessory = 0.5`、`arms = 0.35` [S]
  - `bag_relic.asset` `attackBonus = 6`，`rig_heavy.attackBonus = 0` [S]
  - `AdventureCombat.cs:82` `SpearPower = 1.25`；`ThirdPersonHero.cs:10` `attackDamage = 25` [S]
  - `HeroProgression.cs:38` `AttackBonus = Rank(Strength) * 5` [S]
- **旧计算链从 `git show HEAD:.../AdventureLoadout.cs` 直接读取**（独立于工作树）：
  `Attack = Active.Sum(i.Attack) + rig.attackBonus + bag.attackBonus`，
  `Active = Unique.Where(i => !i.overflow && !i.worn && (i.board || i == Main))`
- 预言机用 IEEE-754 单精度位模式（`struct.pack('<f')`）逐位比对，与 Run 内 `Bits()` 同口径。

### 3.2 24 行黄金矩阵逐位复核结果 [C]

`UX04-B2-GOLDEN-FINAL` 共 24 行 `stage=golden`，其中 **21 行为位比较行**，另 3 行为 `G0-live` / `G7-preview` / `G8-filter`。

| # | 矩阵行 | 原始输入 | 独立复算 Attack | 独立 bits | legacyBits = unifiedBits |
|---|---|---|---|---|---|
| 1 | baseline | 白剑主武器，无容器加成 | 8 | 1090519040 | ✅ |
| 2 | main-White | Power 8 × 1 | 8 | 1090519040 | ✅ |
| 3 | main-Green | Power 19 × 1 | 19 | 1100480512 | ✅ |
| 4 | main-Purple | Power 43 × 1 | 43 | 1110179840 | ✅ |
| 5 | main-Gold | Power 78 × 1 | 78 | 1117519872 | ✅ |
| 6 | main-Red | Power 132 × 1 | 132 | 1124335616 | ✅ |
| 7–13 | weapon-{Sword,Spear,Staff,Bow,TwinBlades,Greatsword,Scythe} | 紫 Power 43 × 1 | 43 | 1110179840 | ✅ 7/7 |
| 14 | board-Accessory | 红 132 × 0.5 = 66 + 主 8 | 74 | 1116995584 | ✅ |
| 15 | board-Arms | 红 132 × 0.35 = 46.2 + 主 8 | 54.2 | 1113115853 | ✅ |
| 16 | reserve-red | 备用红剑不进 Active | 8 | 1090519040 | ✅ |
| 17 | state-InBag | 金剑未生效 | 8 | 1090519040 | ✅ |
| 18 | state-Board | 金剑 78 在盘 + 主 8 | 86 | 1118568448 | ✅ |
| 19 | state-Overflow | overflow 排除 | 8 | 1090519040 | ✅ |
| 20 | state-Worn | worn 排除 | 8 | 1090519040 | ✅ |
| 21 | container-bonus | 主 8 + bag_relic 6 | 14 | 1096810496 | ✅ |

**位比较合计 21/21 全部相等，0 不匹配** [C]。Defense 位模式亦逐行 `defBitsLegacy == defBitsUnified` 全部相等 [C]。

**AP / BasicPower 链独立复算**（`AP = 25 + loadoutAttack + progressionBonus`，`BP = AP × (Spear ? 1.25 : 1)`）：33 / 44 / 68 / 103 / 157 / 85 / 99 / 79.2 / 111 / 39 全部与 Run 吻合 [C]。长枪倍率独立复算 `68 × 1.25 = 85` ✅。

> **审计过程如实记录（失败不覆盖）**：预言机首次运行时，`container-bonus` 行 AP 出现一次 MISMATCH（算出 45、Run 为 39）。经定位为**审计预言机自身输入错误**——把 `active_sum=14`（已含 +6）与 `bagab=6` 重复计入。修正为 `active_sum=8, rigab=0, bagab=6` 后得 `AP = 25 + 14 + 0 = 39`，与 Run 完全一致。**属审计工具缺陷，非产品缺陷**，已如实保留并更正。

### 3.3 重点项覆盖结论

| 重点 | 结论 | 标记 |
|---|---|---|
| 主武器 | 5 品质逐位相等，Power 8/19/43/78/132 | [S][C][E] |
| 备用武器 | `reserve-red` / `uGUI-compare-1` 贡献恒 0 | [S][C][E] |
| 饰品 0.5 / 护臂 0.35 | 66 / 46.2 逐位相等 | [S][C][E] |
| 容器加成 | bag_relic +6，rig_heavy 0 | [S][C][E] |
| Overflow / Worn | 均被 `Active` 排除 | [S][C][E] |
| 长枪倍率 | `BasicPower = 68 × 1.25 = 85`，AP 不变 | [S][C][E] |
| **力量属性** | ⚠️ 源码链独立推导成立（`Rank(Strength)×5`，`Snapshot` 直接读取 `hero.Progression.AttackBonus` 同一 live 属性），但 **24 行矩阵中 `Rank(Strength)` 恒为 0，驱动无任何 Strength rank 变更，无真实 Player Run 验证非零力量等级** → 见条件项 **C-05** | [S][C][H] |
| 不存在第二套业务逻辑 | 实时链、预览、比较、金矩阵共用 `B2AttackModel.ComputeAttack`；sidecar 的 `LegacyAttack` 为独立测试 oracle | [S] |

---

## 4. C · PreviewReplacement 只读审计 — PASS（源码层）/ 证据覆盖不足（见 C-06）

### 4.1 源码层证明（覆盖用户要求的全部 9 项）[S]

`B2AttackModel.Preview()`（`B2AttackModel.cs:152-218`）的全部写入对象：

```csharp
var copy = real.Select(i => i.Clone()).ToList();   // 全量深拷贝，不改 gear.items
var c = candidate.Clone();                         // 候选深拷贝
copy.RemoveAll(i => i.id == c.id);                 // 只改 copy
string mainId = gear.mainWeapon;                   // 局部值拷贝
string reserveId = gear.reserveWeapon;             // 局部值拷贝
... c.board / c.worn / c.overflow / c.x / c.y     // 只改 c（副本）
copy.Add(c);                                       // 只改 copy
var rig1 = ContainersFor(copy, true);              // 静态只读查询
ev.after = Snapshot(copy, mainId, reserveId, rig1, bag1, hero);  // 只读
```

| 用户要求对比项 | 项目内对应实体 | 是否变化 | 依据 |
|---|---|---|---|
| GearItem 内容 | `gear.items[i]` 各字段 | 否 | 仅对 `Clone()` 副本写入 |
| Inventory | `PlayerInventory`（材料/药水） | 否 | `Preview` 无 `Inventory` 引用 |
| EquipmentGrid | 装备盘 `board` + `ContainerDefinition` | 否 | `ContainersFor(copy,…)` 只读、按 copy 求值 |
| Main / Reserve | `mainWeapon` / `reserveWeapon` | 否 | 仅局部字符串 `mainId`/`reserveId` |
| Worn / Overflow | `GearItem.worn` / `.overflow` | 否 | 仅改副本 `c` |
| AttackPower | `hero.AttackPower` | 否 | `Snapshot` 只读 `attackDamage` / `Progression.AttackBonus` |
| Container 状态 | `gear.Rig` / `gear.Bag` | 否 | 预览容器在副本上求值，未写回 |
| 存档 | `CombatSaveSystem` | 否 | 无 `SaveProgress` 调用 |

### 4.2 Player 证据层 [E]

- `G7-preview`：`readOnly=True`、`mainDelta=124`、`reserveDelta=0`、`mainAP=33→157`、`reserveAP=33→33`。
- `uGUI-compare-0..7`：8 个角色连续预览，`before.attackPower` 恒为 33（未因前一次预览漂移）。
- `verify` 无 error 行；6 个 FINAL Run 的 `Player.log` 无 `NullReferenceException` / `MissingMethodException` / `TypeLoadException`。

> ⚠️ **证据覆盖不足（C-06）**：`G7-preview` 的 `readOnly` 判定式仅为 `gear.items.Count == before && gear.mainWeapon == mainBefore`，即**只覆盖 9 项中的 2 项**（Count / Main）。其余 7 项的只读性由源码证明成立，但**没有逐字段的 before/after Player 快照**。审计要求的「必须证明预览不产生任何产品状态变化」在源码层满足、在 Player 证据层不充分。

---

## 5. D · 收藏身份审计 — 部分 PASS / 3 项条件 [S][E][D]

`B2Collection` 为进程内 `static HashSet<string>`（`StringComparer.Ordinal`）+ 进程级 `SessionToken`（`Guid` 前 12 位），**无 GearItem 字段、无 Schema 字段、无 JsonUtility 序列化** [S]。

| 用户要求 | 结论 | 标记 |
|---|---|---|
| 装备移动后收藏跟随正确 | ✅ **源码层**：`DepositEquipment`/`WithdrawEquipment` 均用 `item.Clone()`，`id` 由 `MemberwiseClone` 原样保留 → 收藏按 id 跟随 [S]。⚠️ 但**无 Player Run 实测「先收藏→入库→取回→仍被收藏」** | [S][H] |
| 取消收藏后保护解除 | ✅ `uGUI-fav-remove`（`removed=True count=0`）→ `uGUI-salvage-confirm`（`consumed=True ore=1`） | [E] |
| **分解后 token 清理** | ⚠️ **无任何清理钩子**：产品中 `B2Collection.Remove/Clear` 调用点数为 0（`grep` 确认）。收藏件因 `CanQuickDismantle` 门禁**不可被分解**，故不会产生「收藏件被分解」的残留；但装备经 `Restore()` / 结算 / 读档离开 `items` 时，收藏 id 会**长期残留** → 触发下方 C-01 误拦截 | [S][D] |
| 同一装备身份稳定 | ✅ 主键即 `GearItem.id`（GUID 字符串），`Clone()` 保留 | [S] |
| 不同装备不共享错误 token | ✅ 无 per-item token；`SessionToken` 是进程级单例，集合按 id 精确匹配（Ordinal） | [S] |
| 重启后收藏状态清空 | ✅ `UX04-B2-FAVSEED-FINAL` 种 3 件 → `UX04-B2-RESTART-FINAL` 全新进程 `count=0`、`tokenChanged=True`、`noneFavourite=True` | [E] |
| 不修改存档 | ✅ `B2Collection.cs` 无存档引用；Schema 文件零改动 | [S] |

### 5.1 发现的真实缺陷（C-01）：跨容器收藏导致整理被误拦截 [S][D]

`BatchPreservesFavourites(afterIds)` 以**全局** `ids` 集合比对**单个容器**的 id 列表：

```csharp
// SortBag:    B2Collection.BatchPreservesFavourites(preview.Select(i => i.id))   ← 仅 gear.items
// SortWarehouse: B2Collection.BatchPreservesFavourites(sorted.Select(i => i.id))  ← 仅 stored
foreach (var id in ids) if (!after.Contains(id)) return false;   // 任一收藏 id 不在本容器 → 拒绝
```

**复现路径** [D]：收藏一件白装 → 正常入库（`DepositEquipment` 不检查收藏，符合「允许正常入库」）→ 收藏 id 仍在全局集合但已不在 `gear.items` → 此后 `SortBag()` 恒返回 false 并提示「整理会遗漏收藏装备，已取消」，即使一件装备都没丢。对称地，收藏件在背包时 `SortWarehouse()` 恒被拒绝。

- 后果：**保守失败**（拒绝整理），不丢数据，但给出误导性提示，且属既有功能的回归。
- 授权冲突：D-01 / B2-04 要求「允许正常入库、取出和穿戴」「收藏状态不影响容器移动」；E 节要求「装备移动后收藏跟随正确」。
- 覆盖缺口：驱动中 `SortBag` / `SortWarehouse` 测试次数 **= 0**；`RISK_REGISTER.md` H-03 承认「未做缺件故障注入」，R-09 却标为「已缓解」。

---

## 6. E · IMGUI / uGUI 一致性 — 大部分 PASS / 2 项条件 [S][E]

### 6.1 一致性逐项核对

| 检查项 | IMGUI | uGUI | 同一业务规则 |
|---|---|---|---|
| 语义筛选 | `B2FilterState.SetTab(i)` + `B2InventoryQuery.Matches` | 同左 | ✅ |
| 品质筛选 | `CycleQuality()` → `qualityMask` | 同左 | ✅ |
| 装备分类 | 8 页签 `B2FilterTabs.Labels` | 同左 | ✅ |
| 收藏开关 | `B2Collection.Toggle(selectedId)` | `B2Collection.Toggle(sel.id)` | ✅ |
| 装备比较 | `gear.PreviewReplacement(item, CompareRoleValue)` | 同左 | ✅ |
| 快速入库 | `CampInventoryView.Draw()`「存入选中装备」→ `CampRuntime.DepositEquipment` | `CatInventoryPresenter.Details()`「存入永久仓库」+ `Camp()`「存入选中装备」→ 同方法 | ✅ |
| 取回 | `CampInventoryView.Draw()`「取回选中装备」→ `WithdrawEquipment` | `Camp()`「取回选中装备」→ 同方法 | ✅ |
| 分解保护 | `CanQuickDismantle` + `armedSalvageId` 两段式 | `CanQuickDismantle` + `salvage` 两段式 | ✅ 均汇入 `AdventureLoadout.Salvage` 单点门禁 |
| 二次确认 | `armedSalvageId`（`CancelInteraction`/`Select` 清除） | `salvage == item.id` | ✅ |
| 仓库满载 | 同 `CampRuntime.NotifyDeposit`「永久仓库已满（200/200 件）…装备未移动」 | 同左 | ✅ |
| **攻击力排序** | ⚠️ 见 C-02 | ⚠️ 见 C-02 | ⚠️ 两路径一致地「未接线」 |

**单点门禁核验** [S]：`grep -rn "\.Salvage("` 仅 2 处调用（`CatInventoryPresenter.cs:58`、`ContainerInventoryView.cs:178`），`AdventureLoadout.Salvage` 内 `SalvageAllowed`（B1 金红门禁）+ `B2Collection.CanQuickDismantle`（B2 收藏门禁）顺序不变，**无绕过入口**。

### 6.2 IMGUI 原生鼠标输入证据（要求保留）[E]

`UX04-B2-IMGUI-FINAL/b2-input-events.jsonl` 共 24 条，含 `native-mouse-down` / `native-mouse-up` 成对事件，8 个页签与 3 个循环按钮各带 `client=… screen=… scale=0.9 clientRect=1280x720 origin=1x31` 的真实坐标。`IMGUI-shared-rule` 观测 `sameRule=True`。证据文件完整保留于 80 份正式证据内。

### 6.3 发现的真实缺陷

**C-02 · 排序未接线，功能实际未落地** [S][D]

- `B2InventoryQuery.Apply()` 是唯一含 `OrderBy…` 的排序实现；产品代码中的调用点数为 **0**（`grep -rn "B2InventoryQuery.Apply" Assets/CombatPrototype` 仅命中 `B2InventoryQuery.cs:9` 的注释）。
- 两个 UI 的网格均只做过滤：`CatInventoryPresenter.Grid()` 用 `gear.items.Where(... Matches(...))`，`ContainerInventoryView.Grid()` 用 `foreach(var item in gear.items) + Visible(...)`，**都按 `gear.items` 原顺序绘制**。
- 因此 `CycleSort()` 只改变 `B2FilterState.Current.sort`、`Describe()` 文案与缓存 key（触发重建），**玩家可见的装备排列顺序从不改变**。
- 与 B2-02 授权「攻击力排序 / 品质排序 / 类型排序」及 `INVENTORY_FILTERS.md` §3 的 PASS 声明不符。
- 公允说明 [D]：本库存是**按 x/y 坐标摆放的网格**，本无「列表顺序」概念；`Apply()` 作为查询层纯投影能力存在且经 `G8-filter` 验证。需负责人书面确认是「排序仅作查询层能力（可接受）」还是「需在 UI 接线（需修复批次）」。

**C-03 · IMGUI 重复控件条遮挡标题** [S]

`ContainerInventoryView.Draw()` 第 65 行与第 67 行**重复调用** `B2Controls`：

```
65:  B2Controls(gear,bag,x,y);        ← 绘制 5 按钮于 Rect(x..x+356, y..y+26)
67:  B2Controls(gear,bag,x,y+338);   ← 同样 5 按钮于 y+338..y+364（正确位置）
```

第一处与第 54 行标题 `CombatUI.Text(new Rect(x,y,370,28), "装备盘 X/Y 格", 21, Gold)` **完全重叠** → 标题被按钮覆盖；界面出现两组重复的「品质↻/状态↻/排序↻/角色↻/★收藏」按钮。

- `RISK_REGISTER.md` R-16 声明「重做 UI 布局：已消除 / 新增内容写入既有 Rect」与事实矛盾。
- IMGUI 驱动的 `stripY = panelY + 338f` 只点击**第二处**，第一处重复控件**从未被 Player 验收覆盖**。
- 后果：显示层缺陷，不影响数据/状态；但属授权「不重做 UI 布局」范围内的回归。

---

## 7. F · 存储与兼容性 — PASS [S][E]

| 检查 | 值 / 结论 |
|---|---|
| 仓库 200 件 | ✅ `CampRuntime.Capacity` 未改；`warehouse-full-after` 实测 `count=200 (before=200)`，`reasonOK=True` |
| 背包 96 格 / 装备盘 48 格 | ✅ `B2InventoryQuery.CapacityLine` 输出「背包 96 格 · 装备盘 48 格 · 永久仓库 200/200 件」（`AdventureItems.BagWidth×BagHeight=12×8`、`BoardWidth×BoardHeight=8×6`） |
| v9 读档 | ✅ `UX04-B2-READBACK-FINAL`：`goldPresent=True redPresent=True goldLocked=True redLocked=True collectionEmpty=True`，0 error，`version=9` |
| 金红不可分解（D-16 保持） | ✅ `SalvageAllowed` 未改；`uGUI-B1-Gold/Red` 均 `SalvageAllowed=False stillOwned=True` |
| 收藏不持久化 | ✅ 进程内 HashSet；RESTART-FINAL `count=0`、token 改变；`READBACK` `collectionEmpty=True` |
| **用户原始存档 SHA** | ✅ `C:/Users/guan/AppData/LocalLow/DefaultCompany/万象归途/ForestRuins/save.json` = `dfff9c4f633656740fc252555f9215e124e52e2f1c225ebf6de032cc05e59003`（21799 bytes），与 B0/B1 记录完全一致；**mtime `2026-11-12 09:26:22` 早于全部 B2 运行（2026-11-14）**，强证据表明本批次从未写入 |
| Schema 零修改 | ✅ `CombatSaveData.cs` / `CombatSaveSystem.cs` / `AdventureValidation.cs` 均 UNCHANGED |

---

## 8. G · 保护审计（41 项保护域）— PASS [S]

`PROTECTION_SHA256.tsv`：41 行数据、8 列，`NEW=3 / YES=5 / NO=33`。

| 分类 | 文件 | 判定 |
|---|---|---|
| B2 批准新增（3） | `B2AttackModel.cs` / `B2InventoryQuery.cs` / `B2Collection.cs` | 授权范围内 |
| B2 批准修改（5） | `AdventureLoadout.cs` / `CatInventoryPresenter.cs` / `ContainerInventoryView.cs` / `CampRuntime.cs` / `CampInventoryView.cs` | 授权范围内 |
| 未改动（33） | 其余全部保护域 | ✅ |

逐项 `git diff --quiet HEAD` 复核：`CombatSaveData` / `CombatSaveSystem` / `AdventureValidation` / `AdventureItems` / `AdventureCatalog` / `AdventureCombat` / `AdventureRandom` / `AdventureRules` / `WeaponTraits` / `CraftingRecipeDefinition` / `ContainerDefinition` / `HeroProgression` / `ThirdPersonHero` / `HeroEquipment` / `CrystalCavernBoss*` / `RouteCards` / `WorldEventPoint` / `PlayerBindings` / `PlayerInput` **全部 UNCHANGED** ✅

| 保护项 | 结论 |
|---|---|
| UX-03 不变 / B1 不变 | ✅ HEAD 即 B1 提交、父提交即 UX-03，提交链未回退 |
| v9/v10/v11 Schema 不变 | ✅ 三个 Schema 文件零改动 |
| D-24 攻击力叠加规则不变 | ✅ `Attack`/`Defense` 表达式逐字等价（§3 独立复算证明） |
| 掉落率 / 随机流 / 制造成本 / 装备尺寸 / Boss 规则 / P1-P1C 挑战逻辑 | ✅ 相关文件零改动 |
| `ProjectSettings` / `Packages` / 场景 / Prefab | ✅ `git status --porcelain=v2` 对这些路径为空 |
| 4 个 Unity 设置文件 | ✅ `PC_RPAsset.asset` / `GraphicsSettings.asset` / `ProjectSettings.asset` / `URPProjectSettings.asset` 全部 UNCHANGED；`Assets/Resources.meta` 仍为 untracked 原状态 |

---

## 9. H · 80 份证据审计 — PASS [E]

`EVIDENCE/INDEX.json`：`finalRuns=6`、`finalRunsPass=6`、`totalEvidenceFiles=80`、`baselineCommit=95caf234…`、`productDllSHA256=875cfea8…`、`finalDriverDllSHA256=b7a46b0a…`、`unityVersion=6000.6.5f1`。

| Run ID | PID | mode | verdict | exit | complete | 观测行 | error | 文件 |
|---|---|---|---|---|---|---|---|---|
| UX04-B2-GOLDEN-FINAL | 51092 | golden | PLAYER_RUN_COMPLETED | 0 | PASS | 27 | 0 | 13 |
| UX04-B2-UGUI-FINAL | 39432 | ugui | PLAYER_RUN_COMPLETED | 0 | PASS | 34 | 0 | 14 |
| UX04-B2-IMGUI-FINAL | 47820 | imgui | PLAYER_RUN_COMPLETED | 0 | PASS | 16 | 0 | 13 |
| UX04-B2-FAVSEED-FINAL | 51788 | favseed | PLAYER_RUN_COMPLETED | 0 | PASS | 5 | 0 | 13 |
| UX04-B2-RESTART-FINAL | 50736 | restart | PLAYER_RUN_COMPLETED | 0 | PASS | 4 | 0 | 13 |
| UX04-B2-READBACK-FINAL | 47096 | readback | PLAYER_RUN_COMPLETED | 0 | PASS | 24 | 0 | 14 |

- 6 个 Run 的 `buildId` 全部为 `ux04b2-875cfea8-b70442f9-b7a46b0a`，`productDllSHA256` / `driverDllSHA256` / `exeSHA256` / `runtimeInitializeOnLoadsSHA256` / `scriptingAssembliesSHA256` / `startUtc` / `endUtc` 齐全 ✅
- **80/80 文件 SHA256 + 字节大小逐项重算复核：checked=80、missing=0、mismatch=0** ✅
- `PLAYER_RUN_MATRIX.csv`：41 行、7 列、`FAIL=0` ✅
- **历史失败保留** ✅：
  - `UX04-B2-UGUI-01` `PLAYER_RUN_FAILED` exit=3，`b2-failure.txt` 内容为 `uGUI: two-step dismantle did not consume the white item`（驱动误选 `Carried` 起始主武器，产品正确拒绝），`INDEX.json.preservedFailures` 记录了失败时的 `driverDllSHA256=827877e4…`
  - `UX04-B2-IMGUI-01/02/03`（InputSystem 事件不到达 IMGUI `Event.current` 的不确定诊断运行）与 `GOLDEN-01/02 / UGUI-02 / READBACK-01 / RESTART-01/02 / FAVSEED-01 / IMGUI-04`（中间驱动构建）共 **12 个目录全部原样保留、未删除未覆盖** ✅
  - 4 个构建回执（`b2-product-build.json` / `b2-product-compile.log` / `b2-driver-injection.json` / `b2-driver-injection-r4.json`）保留 ✅

---

## 10. I · 提交白名单（仅生成，未暂存）

已生成 `SUBMIT_WHITELIST.txt`，结构：

| 组 | 数量 | 内容 |
|---|---|---|
| A | 3 | B2 新增源码 `B2*.cs` |
| B | 5 | B2 修改源码 |
| C | 0 | ⚠️ 必要 `.meta` 缺失，见 C-04；**不臆造** |
| D | 12 | 正式交付文档 |
| E | 2 | 本轮审计产物（是否入库由负责人决定） |
| F | 4 | 可复现工具（建议纳入） |
| G | 4 | 构建回执 |
| H | 80 | 正式 Player 证据文件 |
| 合计 | 110 | 候选路径 |

**明确保留但不暂存**：12 个 B2 历史失败/诊断/中间运行目录（逐目录列出）。
**明确排除**：`Builds/`（含 `Builds/ux04b2/player` 隔离副本）、`Library/`、`Assets/Resources.meta`、4 个 Unity 设置文件、`ProjectSettings/` 其余、`Packages/`、场景/Prefab、临时日志、`Evidence/PH-R2*` / `Runs/` / `Runs03*` / `Runs04B0` / `Runs04B1/_builds|_roots`、历史 `DeliveryUxProgression03*/04/04B0/04B1/`、`PreImplementationAudit/`、用户真实存档。

> 操作提示（非本轮执行）：仓库启用 `core.sparseCheckout=true`，且 `.gitignore:24` 忽略 `*.log`；未来若获授权暂存，D/E/H 组路径需 `git add --sparse -f`，**严禁 `git add .`**。

---

## 11. 条件项清单（提交前必须清除）

| 编号 | 严重度 | 条件项 | 性质 | 建议处置 |
|---|---|---|---|---|
| **C-01** | 中 | `BatchPreservesFavourites` 以全局收藏集合比对单容器 id 列表 → 收藏件入库/在仓后 `SortBag`/`SortWarehouse` 恒被误拒绝；且无收藏 id 清理钩子 | 产品源码逻辑缺陷 | 改为「按容器范围比对」或「对 before/after 差集判定」；补 `SortBag`/`SortWarehouse` 负向+正向 Player Run |
| **C-02** | 中 | `B2InventoryQuery.Apply()` 产品调用点为 0；排序只改状态/文案，玩家可见顺序不变；与 B2-02 授权及文档声明不符 | 功能未接线 | 负责人书面确认「排序仅作查询层能力」，或授权 UI 接线 + 补排序 Player Run |
| **C-03** | 中 | `ContainerInventoryView.Draw()` 第 65/67 行重复 `B2Controls`，第一处遮挡「装备盘 X/Y 格」标题；R-16 声明与事实矛盾；该处从未被验收覆盖 | 产品源码 UI 缺陷 | 移除第 65 行重复调用；补 IMGUI 顶部区域截图/点击证据 |
| **C-04** | 低 | 3 个新增 `B2*.cs` 缺 `.meta`，而同目录既有 `.cs` 均有；用户 I 节要求「必要 meta」 | 提交完整性 | 由 Unity 编辑器导入生成稳定 `.meta` 并纳入白名单，或负责人书面豁免「由 Unity 自动生成」 |
| **C-05** | 低 | 力量属性仅源码链独立推导 + `Rank(Strength)=0` 的 G0-live 验证，**无非零力量等级的 Player Run** | 验收覆盖缺口 | 补一行非零 Strength rank 的金矩阵 + 真实 Player Run，或书面确认「共享 live 属性即等价」 |
| **C-06** | 低 | `G7-preview` 的 `readOnly` 仅覆盖 Count / Main 2 项，用户 C 节要求 9 项逐字段 before/after | 证据覆盖缺口 | 补逐字段快照（GearItem/Worn/Overflow/Rig/Bag/AP），或书面确认「源码 Clone 证明充分」 |
| **C-07** | 低 | 收藏件「入库→取回→仍被收藏」无 Player Run；`RISK_REGISTER.md` R-09 标「已缓解」但 H-03 承认未做故障注入 | 文档/证据不一致 | 补对应 Player Run，并同步修订 `RISK_REGISTER.md` / `INVENTORY_FILTERS.md` 措辞 |

> **C-01 / C-02 / C-03 涉及产品源码修改**，本轮为只读审计，未执行任何修复。需负责人单独授权「B2 修复批次」（含源码改动、重新构建、补 Player Run、全量 SHA 复核）后方可清除。

---

## 12. 最终判定与纪律维持

### 结论：**CONDITIONAL_PASS**

- **通过**：A、B（独立复算 21/21 逐位相等）、F、G、H 全项 PASS；C/D/E 的源码层只读性、单点门禁、双 UI 共享规则、IMGUI 原生鼠标证据、失败证据保留均核验通过。
- **条件**：C-01…C-07 未清除；其中 3 项需产品源码修复 + 重新验收。**在全部条件清除前，不得依据 `SUBMIT_WHITELIST.txt` 执行暂存或提交。**

### 纪律维持

| 项 | 状态 |
|---|---|
| 提交（commit） | ❌ 未执行，staged=0，HEAD 仍 `95caf234…` |
| 推送（push） | ❌ 未执行，`feature/ux-progression-04-b2` 无远端跟踪引用 |
| 合并 main | ❌ 未执行，main 未触碰 |
| 启动 UX-05 | ❌ 未执行 |
| 修改产品代码 / 新增 Player Run / 重新构建 | ❌ 未执行（本轮只读） |
| 使用 `git add .` | ❌ 未执行（仅生成白名单文本） |
| 失败证据删除/覆盖 | ❌ 未发生，12 个目录 + 1 个 FAIL 全部保留 |

---

*审计完成，已停止。等待负责人复审并决定：① 授权 B2 修复批次；② 或对 C-02/C-04/C-05/C-06/C-07 给出书面豁免后，重新提交审计结论。*
