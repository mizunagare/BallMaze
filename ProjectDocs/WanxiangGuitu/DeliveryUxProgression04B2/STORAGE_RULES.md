# UX-04-B2 · STORAGE_RULES（B2-05 仓库与 UI 统一）

> 标记：**[S]** 源码事实 · **[E]** Player 证据 · **[C]** 计算结果 · **[D]** 设计推论 · **[H]** 未验证假设

## 1. 三种容量，明确区分 [S][E]

`B2InventoryQuery.CapacityLine(gear, camp)` 是**两条 UI 共用的唯一**容量文案生成函数：

```
"背包 {gear.Bag.Capacity} 格 · 装备盘 {gear.Rig.Capacity} 格 · 永久仓库 {camp.Items.Count}/{CampRuntime.Capacity} 件"
```

| 概念 | 值（默认容器） | 语义 | 来源 | 标记 |
|---|---|---|---|---|
| 背包 | **96 格** | `bag_standard` 12×8 = 96，`ContainerDefinition.Capacity = width*height − blockedCells.Length` | 网格格数，形状相关 | [S][C] |
| 装备盘 | **48 格** | `rig_standard` 8×6 = 48 | 网格格数，形状相关 | [S][C] |
| 永久仓库 | **200 件** | `CampRuntime.Capacity = 200` | `stored.Count` 件数，与网格无关 | [S][C] |

Player 实测 [E]：`UX04-B2-UGUI-FINAL` 的 `warehouse-full-before` 输出 `背包 96 格 · 装备盘 48 格 · 永久仓库 200/200 件`。

**容量 200 未修改** [S]：`CampRuntime.Capacity` 常量、`AdventureValidation.cs:12` (`p.warehouse.Length<=200`)、`CombatSaveSystem.cs:285` (`<=CampRuntime.Capacity`) 全部零变化。容器结构（`ContainerDefinition.cs`、`AdventureItems.Sizes`）零变化。[S]

## 2. 仓库满时的明确原因 [S][E]

`CampRuntime.DepositEquipment` 由原先「静默 `return false`」改为逐分支明确反馈（同一个业务方法，两 UI 共用）：

| 失败分支 | 文案 |
|---|---|
| `!Ready` | 营地数据未就绪或结算待处理，装备未移动。 |
| 非 `InBag` | 请选择背包内未穿戴、未暂存的装备；装备未移动。 |
| `Carried` | 主武器 / 备用武器 / 穿戴中的装备需先替换或卸下，装备未移动。 |
| **仓满** | **永久仓库已满（200/200 件）：请先取回或整理，装备未移动。** |
| 重复 id | 该装备已在永久仓库，未重复转移。 |

Player 证据 [E]：`warehouse-full-after` → `count=200 (before=200) stillOwned=True notice=永久仓库已满（200/200 件）：请先取回或整理，装备未移动。 reasonOK=True`。即**装备数、仓库数均未变化，原因文案明确**。[E]

`WithdrawEquipment` 原有的「背包空间不足，装备仍保留在永久仓库」文案保持不变。[S]

## 3. 展示落点（两界面共用）[S]

| 路径 | 位置 | 内容 |
|---|---|---|
| IMGUI `ContainerInventoryView` | 顶部 `y+0` 右侧 410×28 | `CapacityLine`（去硬编码后由统一函数生成） |
| IMGUI `CampInventoryView` | 顶部标题 | `永久仓库 · {CapacityLine} · 存取后立即保存` |
| uGUI `CatInventoryPresenter.Items()` | 左下既有文本块（`0,387`） | 追加 `CapacityLine` + `B2FilterState.Describe()` |
| uGUI `CatInventoryPresenter.Camp()` | `560,55` | 由 `永久仓库 {n}/200` 改为 `CapacityLine`（消除硬编码 `/200`） |

**不重做 UI 布局** [S]：所有新增内容写入既有 `Rect`；唯一几何调整是把 IMGUI 顶部 440 宽的背包标题拆成 240 宽标题 + 410 宽容量行（同一行内，未移动任何既有控件坐标）。面板尺寸、页签行坐标、网格坐标、按钮坐标全部保持。[S]

## 4. IMGUI / uGUI 使用同一业务逻辑 [S][E]

| 能力 | 共享实现 |
|---|---|
| 筛选/排序/来源/重复提示 | `B2FilterState` + `B2InventoryQuery` |
| 攻击力比较 | `AdventureLoadout.PreviewReplacement` → `B2AttackModel` |
| 收藏与门禁 | `B2Collection` + `AdventureLoadout.Salvage` |
| 容量文案 | `B2InventoryQuery.CapacityLine` |
| 仓满原因 | `CampRuntime.DepositEquipment` |
| 整理保护 | `AdventureLoadout.SortBag` / `CampRuntime.SortWarehouse` |

两个视图只负责渲染与转发输入，不持有业务判定。[S]

## 5. 热键与流程保护 [S]

| 项 | 状态 |
|---|---|
| 19 个 `PlayerAction`（W/S/A/D/Shift/Space/MouseLeft/F/V/Q/E/H/Tab/B/C/R/M/F1） | `PlayerBindings.cs` 零变化 |
| 保留键 `Escape/F2/F3/F5/F9/Digit1-3/N` | 零变化 |
| `R` 双语义（World=放弃 / Management=旋转） | 零变化 |
| `PlayerInput.cs` 上下文 | 零变化 |
| 装备拾取（`LootPickup.PickUp`）、穿戴、移动、容器更换 | 零变化 |
| `PlayerInventory.Page` 7 值枚举、页签路由 | 零变化 |

B2 新增能力全部通过页面内按钮触发，**未占用任何热键**。[S]

## 6. 保护域核对 [S]

`ProjectSettings` / `Packages` / 场景 / Prefab / v9 Schema / 攻击力系数 / D-24 / 掉落率 / 宝箱概率 / 随机流 / 制造成本 / 装备尺寸 / Boss 规则 / P1-P1C 挑战逻辑 —— `git status` 与 `PROTECTION_SHA256.tsv` 均为零变化（41 域中 33 域 `NO`，仅 3 新增 + 5 B2 批准修改）。[S]

## 7. 待验证假设 [H]

1. 容量行显示的是**当前穿戴容器**的 `Capacity`；更换 `rig_light`/`rig_heavy`/`bag_relic` 后数值会随之变化（26/50/44 格），本轮只在默认标准容器下做了 Player 实测。
2. 仓满验证通过产品自身的 `CampRuntime.Restore` 预置 200 件（准备阶段），随后用**真实点击**触发一次被拒的存入作为被测动作；未逐个真实点击 200 次填满。
3. 高 DPI / 非 1280×720 窗口下 `CombatUI.Scale` 变化会影响 IMGUI 原生点击坐标换算；本轮仅验证 1280×720。
