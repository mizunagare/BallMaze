# UX-04-B2 · E：仓库管理设计

> 标记：**[S]** 源码事实（含 file:line）· **[E]** Player 证据 · **[C]** 计算结果 · **[D]** 设计推论 · **[H]** 未验证假设

---

## 1. 现状逐项核验

| E 需求 | 当前实现 | 结论 | 标记 |
|---|---|---|---|
| **容量展示** | IMGUI：`永久仓库 · 装备 {camp.Items.Count}/{CampRuntime.Capacity} 件 · 存取后立即保存`（`CampInventoryView.cs:19`）；uGUI：`永久仓库 {s.Camp.Items.Count}/200`（`CatInventoryPresenter.cs:51`，**硬编码 200**） | ⚠️ 已展示但**两路径不一致**：一处用常量、一处硬编码字面量；背包/装备盘另有 `{gear.UsedCells}/{gear.Rig.Capacity} 格`（`ContainerInventoryView.cs:47`） | [S] |
| **容器满时反馈** | `DepositEquipment` 在 `stored.Count>=Capacity` 时**直接 `return false`，无任何提示**（`CampRuntime.cs:98`）；UI 侧按钮 `enabled` 条件含 `camp.Items.Count<CampRuntime.Capacity`（`CampInventoryView.cs:34`）或 `s.Camp.Items.Count<CampRuntime.Capacity`（`CatInventoryPresenter.cs:44`），即**按钮静默置灰**；双击转移失败时给通用文案「转移未完成：检查空间、携带保护与存档状态」（`CatInventoryPresenter.Transfers.cs:20`） | ⚠️ **缺少「仓库已满」明确反馈**；失败原因被合并成通用文案 | [S] |
| **金红装备存放** | `DepositEquipment` **不检查品质**（`:95-100`）；`WithdrawEquipment` 只查 `CanAdd`（`:101-106`）；`Clone()` 保留全部 19 字段（含 `savedAttack/affixes/origin`） | ✅ 已支持，属性不变 | [S][E] B1 F6/F7 真实 Player 入库再取回 PASS |
| **装备快速入库** | ① IMGUI 营地页「存入选中装备」（`CampInventoryView.cs:34`）；② uGUI 详情页「存入永久仓库」（`CatInventoryPresenter.cs:44`）；③ uGUI 营地页「存入选中装备」（`:51`）；④ uGUI 双击转移（`CatInventoryPresenter.Transfers.cs:19`） | ✅ 已有 4 条路径，但**入口分散、无批量** | [S] |
| **装备快速取回** | ① IMGUI「取回选中装备」（`CampInventoryView.cs:35`）；② uGUI「取回选中装备」（`:51`）；③ uGUI 双击（`Transfers.cs:19`）；另有 `AutoMove` 用于 overflow 找回 | ✅ 已有，同样分散 | [S] |
| **重复装备识别** | `GearItem` 有 `id`（唯一）、`definitionId`、`quality`、`affixes`、`savedAttack/savedDefense`、`originRunId`；`Owns()` 按 id 判重（`:53`）；`stored.Any(i=>i.id==id)` 防重复入库（`:98`）；存档强制全局 id 唯一（`CombatSaveSystem.cs:328`） | ⚠️ **仅有「同一件」判定，无「同名同属性重复件」识别**；UI 列表只显示 `item.Name`（`CampInventoryView.cs:56`、`CatInventoryPresenter.cs:51`） | [S] |
| **库存整理** | `AdventureLoadout.SortBag()`（`PreviewSortBag` + `camp.CommitChange`，`:75-82`）；`CampRuntime.SortWarehouse()`（`:63`）；**仅 uGUI 有「整理背包（营地）/ 整理仓库」按钮**（`CatInventoryPresenter.cs:33,51`），IMGUI 无 | ⚠️ 两路径功能不对等 | [S] |
| **误操作保护** | `CampRuntime.Commit()` 原子提交 + 保存失败**整体回滚**（`:66-94`）；`PreviewContainer` 空间不兼容时拒绝且不动物品（`:140-160`）；分解有 uGUI 二次确认但 IMGUI 单击直分（`ContainerInventoryView.cs:137`） | ⚠️ 存取已很强；分解侧两路径不对等 | [S] |

---

## 2. 重点分析：当前 200 容量是否足够

### 2.1 200 的精确语义 [S][C]

- `CampRuntime.Capacity=200` 是**仓库件数上限**（`stored.Count`，`CampRuntime.cs:11-12,98`），**不是格数**，与背包/装备盘网格容量（96/48 格，`ContainerDefinition.Capacity`）**完全独立** [S][C]。
- v9 存档校验把 200 **硬编码进两处**：`AdventureValidation.cs:12` `p.warehouse.Length<=200`，`CombatSaveSystem.cs:285` `data.warehouseGear.Length<=CampRuntime.Capacity` [S]。
- 随身 `items` 上限是 `1024`（`CombatSaveSystem.cs:326`），但受网格形状实际约束（默认 96 格；金 6 格 / 红 9 格 → 理论上限远小于 1024）[S][C]。
- 待领取 `pending.Length<=4096`（`AdventureValidation.cs:12`），领取到仓库也受 200 限制（`AdventureFlow.World.cs:22`）[S]。

### 2.2 结构性压力源 [S][C][D]

| 压力源 | 事实 | 影响 |
|---|---|---|
| B1 金/红不可分解 | `SalvageAllowed = quality < Gold`（`AdventureLoadout.cs:212`） | 金/红**失去唯一消耗出口**，只能入库或留在背包 → 长期单调累积 [S][D] |
| 掉落品质分布 | `AdventureItems.RollQuality` 阈值：Boss 12% 红 / 非 Boss 0.5% 起 + luck；金约 4% 起（`:78-85`） | 每局都会产生金/红，长期累积速率非零 [S][C] |
| 材质堆栈 | `MaterialLimit=1 亿`（`CampRuntime.cs:11`），分解产出 `quality+1` 铁矿 | 材料侧不构成瓶颈 [S][C] |
| 弃置路径 | 仅 `Flow.DiscardPending` 针对**待领取**奖励（`CatInventoryPresenter.cs:53`）；**仓库内装备无主动丢弃/销毁入口** | 仓库只进不出（取回除外），无清理手段 [S][D] |

### 2.3 判断 [D][H]

- **短期（当前版本节奏）**：200 件足够。默认背包 96 格、单件 1~9 格，玩家在一次会话内可管理的装备量级远低于 200；B1 真实 Player 运行的仓库计数为 0→1→0（`PLAYER_RUN_MATRIX.csv` F6/F7），未触及上限 [E]。
- **长期（金/红只增不减）**：存在累积风险，但**是否需要扩容取决于实际留存数据**，本轮无 Player 长周期采样，**不能据此断言 200 不足** [D][H]。
- **结论 [D]**：B2 **不修改容量、不修改容器结构**。优先通过「可见性」而非「扩容」解决管理问题：容量展示统一、仓满明确反馈、重复件识别、快速批量存取、跨「背包+仓库」统一检索。扩容若需要，须作为独立授权批次，且必须同步修改 `CampRuntime.Capacity`、两处存档校验、两处 UI 文案，并评估旧档兼容 → 属于 UX-05 / Schema 迁移范畴 [S][D]。

> 硬约束核对 [S][D]：不得未经授权增加容量或修改容器结构；不得修改 `ContainerDefinition.cs`、`AdventureItems.Sizes`、`CampRuntime.Capacity`、`AdventureValidation`/`CombatSaveSystem` 的校验阈值。

---

## 3. 改进方案（全部零存档改动）[D]

### 3.1 P0：容量与反馈

| 改进 | 口径 | 落点 | 存档影响 |
|---|---|---|---|
| 统一容量文案 | 两路径统一读 `CampRuntime.Capacity`（消除 `CatInventoryPresenter.cs:51` 的硬编码 `/200`），同时显示 `已用/上限/剩余` | 仅视图 | 无 [D] |
| 仓满明确反馈 | `DepositEquipment` 在 `stored.Count>=Capacity` 分支给 `NotifyMessage("永久仓库已满（200/200）：请先取回或整理，装备未移动。")`；其他失败分支（未选中 / 携带中 / 非 InBag / 重复 / `Ready=false`）分别给原因 | `CampRuntime.cs` 或视图层 | 无（仅提示）[D] |
| 取回失败反馈 | 已有「背包空间不足，装备仍保留在永久仓库」（`:104`）→ 保持不变并统一到两路径 | 视图 | 无 [D] |
| 按钮禁用原因可见 | 按钮置灰时附一行原因文字，避免「静默不可点」 | 视图 | 无 [D] |

### 3.2 P0：快速存取与批量

- 在统一列表上提供「多选 → 批量存入/取回」，但**必须逐件走现有 `DepositEquipment`/`WithdrawEquipment`**，不得绕过 `Commit()` 原子提交与 `Ready` 检查 [S][D]。
- 批量失败时逐件回报，保持「物品未重复转移」语义（`Transfers.cs:20`）[D]。
- 保留现有双击转移与单击按钮，减少操作步骤而不新增热键 [D]。

### 3.3 P0：重复装备识别

定义「同类重复件」判定键（**纯计算，不新增字段**）[D]：

```
dupKey = (type, quality, definitionId, savedAttack, savedDefense,
          affixes 排序后序列, widthOverride, heightOverride)
```

- `id` 仍为唯一身份，不可用于「重复」判定；`id` 只用于精确选中与防重复入库 [S]。
- 展示：在列表行追加「×N」计数与「同名同属性」标记；检索时可按 `dupKey` 聚合 [D]。
- **不含** `origin/originRunId/x/y/board/worn/overflow/rotation`（这些是位置/来源态，不应影响是否重复）[D]。

### 3.4 P0：库存整理对等

- 把「整理背包 / 整理仓库」按钮补到 IMGUI 路径（复用 `gear.SortBag()` / `camp.SortWarehouse()`），或把两路径收敛到同一渲染入口 [D]。
- 整理前用 `PreviewSortBag` 的既有「形状无法完整整理则保留原布局」语义（`:78-80`），**不得强制丢物** [S][D]。
- 「整理」与「筛选/排序」分离：前者改变 `x/y` 并触发 `Commit` 存档；后者只读视图，不写盘 [D]。

### 3.5 P0：误操作保护补齐

- 把 uGUI 已有的分解二次确认范式统一到 IMGUI（当前 IMGUI 单击即分解）[S][D]。
- 金/红保持 B1 的 `SalvageAllowed` 硬拒 + 「不可分解 · 可入库」提示，**不新增锁定字段**（见 `COLLECTION_DESIGN.md §D.4`）[S][E]。
- 存取失败一律「物品未移动 / 未重复转移」，与 `Commit` 回滚语义一致 [S][D]。

---

## 4. 与 B1 / 保护域边界 [S][D]

| 约束 | 本方案 |
|---|---|
| 不修改 B1 | B1 的 `SalvageAllowed` 与三处 UI 提示保持不变 |
| 不修改容器容量/结构 | 200 / 96 / 48 / `Sizes` / `ContainerDefinition` 全部不动 |
| 不修改掉落率、随机流、制造成本、攻击力 | 不触碰 `AdventureItems.Roll*`、`AdventureRandom`、`CraftingCosts`、`AdventureLoadout.Attack` |
| 不修改存档 Schema | 全部改进为视图层或仅提示文案；批量存取仍走既有 `Commit` |
| 金红可管理 | 依赖已验证的 `Deposit/Withdraw` 无品质检查路径 [S][E] |

---

## 5. 待验证假设 [H]

1. 「200 是否足够」缺长周期 Player 采样；未来应记录 `stored.Count` 随时间/局数的增长曲线后再定扩容。
2. 批量存取在 `Commit()` 的单次原子提交下是否会触发多次 `SaveProgress`（性能/存档 revision 语义）尚未验证。
3. `dupKey` 是否应包含词缀顺序、`RuinsSpecialRewards.ItemLabel(id)` 特殊标签（`:25`）需产品确认。
4. 仓满文案由 `CampRuntime` 还是视图层发出，需确认是否影响 `Notice`/`HudNotificationQueue` 的既有行为。
