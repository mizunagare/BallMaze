# UX-04-B2 · F：交互设计与统一方案（IMGUI / uGUI）

> 标记：**[S]** 源码事实（含 file:line）· **[E]** Player 证据 · **[C]** 计算结果 · **[D]** 设计推论 · **[H]** 未验证假设

---

## 1. 两条现有路径的真实结构

### 1.1 路径 A：IMGUI（`GUI.Button` / `OnGUI`）

```
PlayerInventory.OnGUI (PlayerInventory.cs:191-219)
  └─ 若 CatInventoryPresenter.Running 则整体让位 (:193)
  └─ CombatInventoryView.Draw (:201)
       ├─ 页签 7 项 (:12-14) → bag.OpenPage((Page)i)
       └─ switch(bag.CurrentPage) (:16-24)
            Items     → AdventureInventoryView.Draw → ContainerInventoryView.Draw
            Crafting  → AdventureInventoryView.Draw(craft=true)
            Equipment → ContainerInventoryView.Containers
            Character → CombatInventoryView.Character
            Overflow  → ContainerInventoryView.Overflow
            Weapons   → WeaponLoadoutView.Draw
            Camp      → CampInventoryView.Draw
```
组件库：`CombatUI.Button/Text/Panel/Fill`（`CombatUI.cs`）。[S]

### 1.2 路径 B：uGUI（`UnityEngine.UI` + EventSystem）

```
CatInventoryPresenter (CombatSession.cs:41 挂载；DefaultExecutionOrder 21000)
  Start() 建 Canvas (ScreenSpaceOverlay) (CatInventoryPresenter.cs:10-12)
  LateUpdate() 每 0.15s 脏检查 key → Build() (:13-16)
  Build() 页签 7 项 + switch(CurrentPage) (:27-30)
       Items/Crafting/Equipment/Character/Overflow/Weapons/Camp
  partial: .Scroll.cs（滚动位置）/ .Transfers.cs（点击/双击/拖拽）/
           .Workbench.cs（制作/容器比较）
```
按钮通过 `CatUI.Button(...)` 生成，`gameObject.name = label`（`CatInventoryPresenter.cs:19-20`），真实输入注入依赖此命名（B1 Player 运行已验证）[S][E]。[S]

### 1.3 已有共享点（不得重复实现）[S]

| 共享资产 | 说明 |
|---|---|
| `AdventureLoadout` / `CampRuntime` / `AdventureFlow` | **全部业务逻辑**唯一归属；两视图只调用 |
| `ContainerInventoryView` 静态状态 | `BeginDrag/DropOn/RotateSelection/CancelInteraction/Dragging/Grab/GrabPoint/Rotation/Select` 同时被 IMGUI 自身（`:23-37,66-81`）与 uGUI（`CatInventoryPresenter.cs:23-24,39`、`CatGridSlot.cs:55-65`）复用 |
| `CampInventoryView.Section` 静态状态 | uGUI `Camp()` 复用（`CatInventoryPresenter.cs:48`） |
| `PlayerInventory.Page` 7 值枚举 | 两路径共用（`PlayerInventory.cs:31`） |
| `CombatSaveSystem`/`AdventureValidation` | 两路径共用同一存档与校验 |

**关键事实 [S]**：业务逻辑从未被实现两套，重复的是**视图渲染 + 筛选状态 + 交互细节**。B2 的统一方案应只新增「共享查询层」，不新建第二套业务服务。

### 1.4 已确认的不对等（统一时必须消除）[S]

| 项 | IMGUI | uGUI |
|---|---|---|
| 筛选索引语义 | `filter 1=非武器,2=武器`（`ContainerInventoryView.cs:60`） | `filter 1=武器,2=非武器`（`CatInventoryPresenter.cs:32,41`）**相反** |
| 筛选项数 | 4（含「素材」但不显示装备） | 6（含材料/消耗品/任务物品） |
| 来源标签 `SourceLabel` | 显示（`:129`） | **不显示** |
| 整理背包 / 整理仓库 | 无 | 有（`:33,51`） |
| 分解确认 | 单击直接分解（`:137`） | 二次确认（`:44`） |
| 存入仓库 | 仅营地页（`:34`） | 详情页 + 营地页 + 双击（`:44,51`、`Transfers.cs:19`） |
| 容器比较预览 | `Containers()`（`:139-160`） | `Workbench.cs:32-46`（更详细：容量/攻击/防御/加成 Δ） |
| 攻击力 Δ 展示 | 无 | 容器更换页有链级 Δ（`:43`） |

---

## 2. 统一交互方案 [D]

### 2.1 三层契约

```
[业务层]  AdventureLoadout / CampRuntime / AdventureFlow / CombatSaveSystem   ← 不动
   ↑ 只调用，不复制
[查询层]  InventoryQuery（新增，纯 C#、无状态落盘）
   · Filter / Sort / Search / Group(重复件) / StatusOf / ComparePreview
   · 共享「语义枚举」FilterSpec（消除整数索引歧义）
   · 会话内收藏 HashSet<string>（只在查询层，不进 GearItem）
   ↑ 只读投影
[视图层]  IMGUI 渲染器 + uGUI 渲染器（各自画，共用 InventoryQuery 结果）
```

- **不重复实现两套业务逻辑** [D]：所有判定（状态、品质、可否分解、可否入库、对比 Δ）只存在于查询层 / 业务层；视图只负责把结果画出来。
- **不改变现有热键** [S][D]：见 §2.2，B2 不新增任何 `PlayerAction`、不改绑定、不加键盘快捷键；新增能力全部用**页面内按钮/标签**承载。
- **不破坏拾取与穿戴** [D]：不动 `LootPickup.PickUp`、`InteractionResolver`、`AdventureLoadout.Add/Place/AutoMove/SelectMain/SelectReserve`；B2 只加**只读**筛选与对比，不改任何写入路径的准入条件。
- **保持当前 UI 风格** [D]：IMGUI 继续用 `CombatUI.*`，uGUI 继续用 `CatUI.*`；配色沿用 `AdventureItems.Color(quality)`、字号/间距沿用现有 `Rect`（IMGUI 1120×670 面板 `CombatInventoryView.cs:7-8`；uGUI 1160×720 面板 + 1280×800 参考分辨率 `CatInventoryPresenter.cs:11-12`）。
- **优先减少操作步骤** [D]：一次筛选 → 一次点击选中 → 同屏对比；存取支持批量；取消「先切页才能操作」的多跳路径。

### 2.2 冻结的热键表（不得改动）[S]

`PlayerBindings.cs:7,19-23`：`W/S/A/D`(移动) `LeftShift`(冲刺) `Space`(翻滚) `MouseLeft`(普攻) `F`(技能) `V`(切换武器) `Q`(药水) `E`(交互) `H`(出口/撤离) `Tab`(背包) `B`(物品页) `C`(角色页) `R`(World=放弃冒险 / Management=旋转装备，上下文复用) `M`(路线) `F1`(帮助)。
保留键 `Escape, F2, F3, F5, F9, Digit1/2/3, N`（`:50`）。[S]
> 硬编码使用点：`CombatSaveSystem.cs:62-63`（F5/F9）、`PlayerInventory.cs:125`（Esc）、`HeroProgression.cs:94-96`（1/2/3）等 [S]。B2 **不占用任何保留键**，避免与 `R` 双语义冲突 [D]。

---

## 3. 关键页面线框 [D]

### 3.1 统一「背包与胸挂」页（IMGUI / uGUI 同构）

```
┌─ 冒险者行囊 / 猫族冒险行囊 ────────────────────────────────────────────────┐
│ [背包与胸挂][制作][更换容器][角色][迁移暂存][双武器与词缀][营地仓库]        │  ← 现有 7 页签，不变
├────────────────────────────────────────────────────────────────────────────┤
│ 筛选条（新增，纯视图）                                                     │
│  类型[全部▾] 品质[□白 □绿 □紫 □金 □红] 状态[全部▾] 来源[全部▾] 收藏[□仅看] │
│  排序[攻击力▾][↓]   搜索[__________]   [清空筛选]                        │
│  范围: (● 随身  ○ 仓库  ○ 全部)  ← 只读投影，仓库项标注「仓库」            │
├──────────────────────────┬───────────────────────────┬────────────────────┤
│ 属性盘 (rig)             │ 随身背包 (bag)            │ 详情 / 对比面板    │
│  UsedCells/Capacity 格   │  W×H 网格                 │ ┌────────────────┐ │
│  ┌─┬─┬─┬─┐              │  ┌─┬─┬─┬─┬─┬─┐            │ │ [图标] 名称    │ │
│  ├─┼─┼─┼─┤  拖放/旋转    │  ├─┼─┼─┼─┼─┼─┤  拖放     │ │ 类型 品质      │ │
│  └─┴─┴─┴─┘  R 旋转(不变) │  └─┴─┴─┴─┴─┴─┘           │ │ 攻击/防御 占格 │ │
│                           │                          │ │ 状态: 主/备/盘/  │ │
│  攻击 +N 防御 +N         │  [更换胸挂/背包]          │ │       暂存/穿戴 │ │
│                           │  [整理背包(营地)] ←补齐    │ │ 来源: SourceLabel│ │
│                           │  [整理仓库] ←补齐         │ │ ★收藏(会话内)  │ │
├──────────────────────────┴───────────────────────────┤ ├────────────────┤ │
│ 对比区（选中候选后展开，见 3.2）                      │ │ [设为主武器]   │ │
│                                                       │ │ [设为备用]     │ │
│                                                       │ │ [放入/收回盘]  │ │
│                                                       │ │ [存入仓库]     │ │
│                                                       │ │ [不可分解·可入库]│ │
│                                                       │ │ [拆解换铁矿…]  │ │
│                                                       │ └────────────────┘ │
├────────────────────────────────────────────────────────────────────────────┤
│ 永久仓库 143/200 件 · 剩余 57  ← 统一用 CampRuntime.Capacity（去硬编码）  │
│ 提示/通知（仓满、取回失败、B1 拒绝原因）                                  │
└────────────────────────────────────────────────────────────────────────────┘
```

- 筛选条是**新增的唯一 UI 区块**，不改变现有网格/按钮坐标语义 [D]。
- 「范围=全部」时把仓库项以只读行追加到右侧列表并标注来源，**不产生任何存取动作** [D]。
- 品质/状态/来源/收藏徽标沿用 `AdventureItems.Color` 与现有 `CombatUI`/`CatUI` 配色 [D]。

### 3.2 装备对比面板（新增，同构）[D]

```
┌─ 装备对比 ──────────────────────────────────────────────────┐
│                │ 当前                  │ 候选                 │
│ 名称           │ 普通·长剑               │ 神话·长剑             │
│ 武器类型       │ 长剑 (Weapon)          │ 长剑 (Weapon)         │
│ 品质           │ 白                     │ 红                    │
│ 装备自身攻击   │ +8                     │ +132                  │
│ 防御 / 占格    │ +0 / 1格               │ +0 / 9格              │
│ 当前装备状态   │ 主武器 · InBag         │ 背包内 · 未生效        │
│ 主/备武器状态  │ 主                     │ 未配置（备用贡献 0）   │
│ 来源           │ 本局战利品·死亡丢失     │ 本局战利品·死亡丢失    │
│ 分解           │ 可分解                 │ 不可分解 · 可入库      │
├──────────────────────────────────────────────────────────────┤
│ 对角色实际 AttackPower 的变化（重跑完整计算链，见 EQUIPMENT_  │
│ COMPARISON.md §4）：                                         │
│    攻击力  33 → 157    Δ +124                                │
│    普攻    33 → 157    Δ +124   (长枪倍率 1.25 时另计)        │
│    ※ 若候选设为「备用」，Δ = 0（备用武器贡献为 0）            │
│    ※ 容器加成 / 饰品 0.5 / 护臂 0.35 均由链计算，非简单差值   │
├──────────────────────────────────────────────────────────────┤
│ [设为主武器] [设为备用] [放入装备盘] [存入仓库] [关闭]         │
└──────────────────────────────────────────────────────────────┘
```

### 3.3 营地仓库页（存取）[D]

```
┌─ 营地仓库 · 装备 143/200 件（剩余 57） · 存取后立即保存 ─────────────────┐
│ [装备存取][材料存取][营地工作台][待领取]  ← 现有 4 区，不变               │
│ 随身背包 (筛选/排序/搜索/重复件分组 ×N)   永久仓库 (同样筛选)             │
│  ☑ 普通·长剑 ×3   [重复件]              ☐ 神话·长剑  红 攻击+132       │
│  ☐ 神话·护臂  红 攻击+46.2             ☐ 传说·饰品  金 攻击+39        │
│  … 多选 …                                … 多选 …                      │
│ [存入选中 (N)]  [取回选中 (N)]  [整理背包] [整理仓库]                    │
│ 反馈：永久仓库已满（200/200）：请先取回或整理，装备未移动。              │
│       背包空间不足，装备仍保留在永久仓库。                              │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 4. 关键交互流程 [D]

### 4.1 找到想要的装备（减少步骤）

```
玩家打开背包(Tab/B，热键不变)
  → 筛选条设「品质=金/红」+「排序=攻击力↓」或直接搜名称
  → InventoryQuery 在 随身/仓库 上做只读投影
  → 两视图渲染同一结果集
  → 单击选中 → 右侧详情+对比面板
```
原先需「切到营地页 → 逐条滚动找 → 再切回」，现在 1 次筛选 + 1 次点击 [D]。

### 4.2 比较并装备

```
选中候选 → 对比面板自动以「设为主武器」为默认预览角色
  → 调用 ComputeAttack(clone(items), cand.id, Rig, Bag)（同一链）
  → 显示 ΔAttackPower + ΔBasicPower + 备用/容器/状态说明
  → 玩家点「设为主武器」→ 才真正调用 gear.SelectMain(item)（现有路径，不改）
  → 未点击确认前 items 零变化
```
**对比与执行分离**：预览只读，执行仍走原 API [D]。

### 4.3 金/红库存管理

```
金/红 → 详情显示「不可分解 · 可入库」(B1 保持)
  → 「存入仓库」→ CampRuntime.DepositEquipment（无品质检查）
  → Commit 原子保存；仓满给明确文案
  → 需要时「取回」→ WithdrawEquipment（CanAdd 检查）
  → 对比面板仍可显示其作为主武器时的 ΔAttackPower
```
B1 真实 Player 已验证该链路可用 [E]。

### 4.4 收藏（会话内）

```
点击 ★ → InventoryQuery.Favorites.Add(item.id)
  → 「仅看收藏」筛选 / 置顶 / 高亮
  → 不影响移动、穿戴、存取、分解；重启清空
```
零存档写入 [D]。

---

## 5. 硬约束核对 [S][D]

| 要求 | 方案 |
|---|---|
| 不重复实现两套业务逻辑 | 查询层单一实现，两视图只渲染 |
| 不改变现有热键 | 19 个 `PlayerAction` + 保留键全部冻结，新增能力仅用页面按钮 |
| 不破坏拾取与穿戴流程 | 不触碰 `PickUp`/`Add`/`Place`/`SelectMain`/`SelectReserve`；只读筛选 |
| 保持当前 UI 风格 | 沿用 `CombatUI`/`CatUI`、品质色、面板尺寸 |
| 优先减少操作步骤 | 筛选条 + 同屏对比 + 批量存取 |
| 不修改存档 / B1 / main / 保护域 | 全部为视图层 + 只读查询层 |

---

## 6. 待验证假设 [H]

1. IMGUI 的 `OnGUI` 每帧重绘与 uGUI 的 0.15s 脏检查（`CatInventoryPresenter.cs:15`）对共享查询层缓存的刷新时机未验证；需确认筛选结果不会滞后一帧或与拖拽状态冲突。
2. `CatUI.Button` 的 `gameObject.name=label` 是 B1 真实输入注入的定位依据 [E]；新增按钮若与现有按钮同名会造成定位歧义，实施时需命名去重。
3. 新增筛选条在 1120×670 / 1160×720 面板内的空间占用未做实测；若不容纳需改为可折叠行，属实施期布局验证。
4. 「范围=全部」把仓库项投影到背包页，可能与 `CatGridSlot` 拖放命中检测（`.Transfers.cs:8`）冲突；实施期须确保仓库投影项**不可拖放**。
