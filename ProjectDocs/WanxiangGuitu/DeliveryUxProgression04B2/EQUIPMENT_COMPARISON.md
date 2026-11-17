# UX-04-B2 · EQUIPMENT_COMPARISON（B2-03 装备比较）

> 标记：**[S]** 源码事实 · **[E]** Player 证据 · **[C]** 计算结果 · **[D]** 设计推论 · **[H]** 未验证假设

## 1. 强制约束与实现

| 要求 | 实现 | 标记 |
|---|---|---|
| 必须基于统一攻击力计算接口 | 两 UI 均调用 `AdventureLoadout.PreviewReplacement(candidate, role)` → `B2AttackModel.Preview` → `ComputeAttack`/`Snapshot` | [S] |
| 禁止简单装备属性相减 | 结果由克隆列表重跑完整链得出 | [S] |
| 展示当前 AttackPower | `ev.before.attackPower` | [S] |
| 展示替换后 AttackPower | `ev.after.attackPower` | [S] |
| 展示实际变化值 | `ev.deltaAttackPower`（另附 `deltaBasicPower`） | [S] |
| 展示装备自身 Attack | `ev.itemAttack` / `item.Attack` | [S] |
| 展示主副武器贡献 | `ev.after.mainContribution` / `reserveContribution` | [S] |
| 展示饰品与护臂贡献 | `ev.after.accessoryContribution` / `armsContribution` | [S] |
| 覆盖备用武器/饰品/护臂/长枪/Overflow/Worn/容器加成 | 8 个 `B2EquipRole` + 黄金矩阵覆盖 | [S][E] |

## 2. 两条 UI 的展示落点 [S]

| 路径 | 位置 | 展示内容 |
|---|---|---|
| IMGUI | `ContainerInventoryView.Details()`，`y+270` 的紧凑文本块 | `AP before→after (Δ...)`；`主/备/饰/臂/容` 贡献；顶部另显示 `攻击 +A / 防御 +D`、来源、重复件提示 |
| uGUI | `CatInventoryPresenter.Details()`，`y+132` 详情文本块 | `对比[角色] AP before→after Δ...`；`普攻Δ`；`装备自身攻击`；`主/备/饰/臂/容器` 贡献 |

两条路径使用**同一个** `ContainerInventoryView.CompareRoleValue`（静态）与**同一个** `CycleCompareRole()`，因此角色语义也统一。[S]

`不重做 UI 布局` [S]：所有新增信息都写入既有详情文本块（`Rect` 位置不变），未新增面板、未移动既有按钮；仅把 IMGUI 顶部标题拆为两段以容纳容量行。

## 3. 反例集：为什么「简单差值」是错的 [C][E]

基线：`attackDamage=25`、`Rank(Strength)=0`、穿戴标准容器（bonus=0）、`Main=白长剑(Attack=8)` → `AttackPower=33`、`BasicPower=33`。[C]

| # | 场景 | 真实 ΔAttackPower | 朴素 `cand.Attack − cur.Attack` | 结论 | 标记 |
|---|---|---|---|---|---|
| 1 | 红剑 `Attack=132` 设为主武器 | **+124**（33→157） | +124 | 偶然一致 | [C][E] |
| 2 | 同一红剑设为**备用武器** | **0**（33→33） | +124 | ❌ 错 124 | [C][E] |
| 3 | 更换 `bag_relic`（容器 `attackBonus=+6`，物品 `Attack=0`） | **+6**（33→39） | 0 | ❌ 漏算 | [C][E] |
| 4 | 红饰品放盘（`132×0.5=66`） | **+66**（33→99） | 视基准而定 | ❌ 系数不可忽略 | [C][E] |
| 5 | 红护臂放盘（`132×0.35=46.2`） | **+46.2**（33→79.2） | 视基准而定 | ❌ 系数不可忽略 | [C][E] |
| 6 | 主武器 白剑→白长枪（同 `Attack=8`） | `AttackPower` Δ=0，但 `BasicPower` 33→**41.25** | 0 | ❌ 漏掉 `SpearPower=1.25` | [C][E] |
| 7 | 候选 `overflow` 或 `worn` | **0**（不进入 Active） | >0 | ❌ 状态门 | [C][E] |
| 8 | 候选 `board` | 按 `i.Attack` 计入 Active | 未定义 | ❌ 需重跑 Active | [C][E] |

Player 实测（`GOLDEN-FINAL`）[E]：
- `G7-preview`：`mainDelta=124`、`reserveDelta=0`、`mainAP=33→157`、`reserveAP=33→33`、`readOnly=True`。
- `weapon-Spear`：`attackPower=68`、`basicPower=85`（68×1.25）。
- `weapon-Spear` 与 `weapon-Sword` 的 `AttackPower` 同为 68（紫 Power=43 + 25），但 `BasicPower` 不同 → 简单差值必然漏报。
- `container-bonus`：`containerBonus=6`、`attackPower=39`。
- `state-Overflow` / `state-Worn`：`attackPower=33`（不加属性）。

## 4. 角色覆盖 [S][E]

`B2EquipRole`：`None / Main / Reserve / Board / Overflow / Worn / ContainerRig / ContainerBag`。`UX04-B2-UGUI-FINAL` 通过真实点击「对比角色↻」连续切换 8 个角色，逐角色记录 `role / feasible / AP before→after / delta / 各贡献`，共 8 行观测。[E]

| 角色 | 对 Active 的影响 | 典型 Δ | 标记 |
|---|---|---|---|
| `Main` | 替换 `mainId`，旧主可能转备用 | +124（红剑） | [C][E] |
| `Reserve` | Active 不变（备用不入选） | 0 | [C][E] |
| `Board` | `board=true` → 进入 Active | +`i.Attack` | [C][E] |
| `Overflow` | 不进入 Active | 0 | [C][E] |
| `Worn` | 不进入 Active，但改变 rig/bag 加成 | 容器 bonus 差 | [C][E] |
| `ContainerRig/Bag` | 更换穿戴容器 → `ContainersFor(copy, ...)` 重算 | 容器 bonus 差 | [C][E] |

**长枪 [S][E]**：`B2AttackModel.Snapshot` 以 `Main.type` 决定 `weaponType`，`BasicPower = AttackPower × (Spear ? AdventureCombat.SpearPower : 1)`；`SpearPower` 常量本身**未修改**（`AdventureCombat.cs` 零变化）。

## 5. 只读与存档 [S][E]

- `Preview` 对 `gear.items.Select(i => i.Clone())` 的副本工作，`candidate.Clone()` 深拷贝 `affixes`；从不写回 `items`/`mainWeapon`/`reserveWeapon`。
- 不调用 `SaveProgress`，不触碰 `CombatSaveData`，不产生新的持久化字段。
- `G7-preview` 的 `readOnly=True` 为 Player 运行时断言。[E]
- UI 只渲染数值，点击「对比角色↻」只改一个进程内枚举，不改装备状态。[S]

## 6. 贡献口径 [S]

`B2AttackSnapshot` 的 `mainContribution / reserveContribution / accessoryContribution / armsContribution / boardContribution / containerBonus` 全部从**同一个** `Active` 集合派生（而非从 `item.Attack` 猜测）：

```
foreach (i in Active) {
  if (ReferenceEquals(i, main)) mainContribution += i.Attack;
  if (i.id == reserveId)        reserveContribution += i.Attack;   // 恒 0
  if (i.type == Accessory)      accessoryContribution += i.Attack;
  if (i.type == Arms)           armsContribution += i.Attack;
  if (i.board)                  boardContribution += i.Attack;
}
containerBonus = rig.attackBonus + bag.attackBonus;
```

## 7. 待验证假设 [H]

1. `Board` 角色是「假设放置成功」的预演；实际放置仍需 `CanPlace` 通过，实现中二者分离，本轮未对每个形状组合穷举验证。
2. `feasible=false` 的场景（如候选非武器设为主武器、候选是携带中的武器入盘）在预览中返回 `after=before` 并给出原因，未在 Player 中逐一断言全部拒绝文案。
3. 贡献分解未按「同类型多件」做穷举，但求和顺序与 `ComputeAttack` 一致，故总量逐位一致。
