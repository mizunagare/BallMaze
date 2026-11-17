# UX-04-B2 · 待负责人决策项

> 标记：**[S]** 源码事实 · **[E]** Player 证据 · **[C]** 计算结果 · **[D]** 设计推论 · **[H]** 未验证假设
> 本轮只读，**不实施**。下列决策未获批准前不得进入编码。

---

## D-01（阻断级）实施范围授权

| 项 | 内容 |
|---|---|
| 问题 | 是否批准 B2 进入实施？批准哪些优先级？ |
| 选项 | ① 仅 P0（可见性/管理，零公式改动）；② P0+P1 对比；③ P0+P1+收藏；④ 仅先做「文档/原型」不碰产品源码 |
| 建议 | **① 或 ②**：P0 全部为零存档、零公式改动的视图+只读查询层；P1 对比需触及 `AdventureLoadout.cs`（见 D-02） |
| 依据 | [D] `IMPLEMENTATION_FILE_MATRIX.csv`；保护域清单 `PROTECTION_SHA256.tsv`（31 项） |
| 标记 | [D] |

## D-02（阻断级）是否允许等价重构 Attack 计算体

| 项 | 内容 |
|---|---|
| 问题 | 装备对比要求「结果必须来自当前实际装备计算链」。是否允许把 `AdventureLoadout.Attack/Defense` 的计算体抽成静态纯函数 `ComputeAttack(...)`，由实时属性与预览共用？ |
| 风险 | `AdventureLoadout.cs` 属于保护域「攻击力计算」；B1 已明确禁止修改攻击力计算。等价重构**不改变语义**但改动该文件 |
| 备选 | ② 不抽函数，改在 `AdventureLoadout` 内新增一个只读 `PreviewAttack(...)` 方法，内部仍调用同一 `Active` 判定；③ 对比功能暂缓，只做 P0 |
| 建议 | **②**（新增只读方法、不改现有 `Attack` getter 一行），或由负责人书面确认「等价抽取允许」 |
| 依据 | [S] `AdventureLoadout.cs:19,22-23`；[S][C] `EQUIPMENT_COMPARISON.md §4`；[E] B1 读档 `AttackPower=33` |
| 标记 | [S][D] |

## D-03 收藏是否必须跨重启保留

| 项 | 内容 |
|---|---|
| 问题 | 「收藏」是会话内临时（推荐），还是必须跨重启持久？ |
| 若临时 | 运行时 `HashSet<string>`，**零存档改动**，重启清空 [D] |
| 若持久 | 涉及 `GearItem` 新字段 / `ProfileState` 新列表 → **Schema 迁移**：版本白名单 1..9、6 类装备实例扩散、`ground-loot` 分页、校验器补全、旧构建静默丢字段（`SAVE_COMPATIBILITY.md §3`）→ 需 UX-05 或独立授权批次 |
| 建议 | **会话内临时**；持久需求另立批次 |
| 标记 | [S][D][H] |

## D-04 「获取地区」维度是否放弃

| 项 | 内容 |
|---|---|
| 事实 | `GearItem` 无地区字段；地区仅在局级 `RunState.region`，不随装备落盘（`AdventureState.cs:27`、`AdventureData.World` `:73`）[S] |
| 约束 | 需求原文「仅在已有数据支持时」「没有来源数据时不得增加新的来源字段」[S] |
| 建议 | B2 **不实现地区维度**；仅统一展示现有 `origin` + `SourceLabel`（目前只有 IMGUI 展示）[D] |
| 若坚持 | 需新增字段 + 局档案关联 + 迁移 → UX-05 / Schema 授权，且 `AdventureValidation.cs:35` 的 `origin` 强校验必须先评估 |
| 标记 | [S][D] |

## D-05 仓库 200 容量是否维持

| 项 | 内容 |
|---|---|
| 事实 | `Capacity=200` 被 4 处依赖：`CampRuntime.cs:11,98`、`AdventureValidation.cs:12`、`CombatSaveSystem.cs:285`、uGUI 硬编码 `/200`（`CatInventoryPresenter.cs:51`）[S] |
| 分析 | 金/红不可分解后缺消耗出口，长期累积；但本轮**无长周期 Player 采样**，不能断言 200 不足 [D][H] |
| 建议 | **维持 200**；本轮仅统一展示 + 仓满明确反馈 + 批量/重复识别/整理；记录 `stored.Count` 增长曲线后再评估扩容 |
| 标记 | [S][D][H] |

## D-06 「未使用 / 已装备 / 已收藏」的判定口径

| 项 | 内容 |
|---|---|
| 问题 | 「未使用」是否包含「在仓库中的装备」？「已装备」是否含 `worn` 容器与 `Carried` 主/备武器？ |
| 建议口径 | 未使用 = `InBag && !Carried && !board`（随身）；仓库项单列「仓库」状态；已装备 = `board || worn || Carried`；已收藏 = 会话内标记（可与前两者叠加） |
| 依据 | [S] `AdventureItems.cs:24`、`AdventureLoadout.cs:13-16` |
| 标记 | [S][D] |

## D-07 「重复装备」判定键

| 项 | 内容 |
|---|---|
| 问题 | `dupKey` 是否包含词缀顺序、特殊奖励标签 `RuinsSpecialRewards.ItemLabel(id)`（`AdventureItems.cs:25`）？ |
| 建议 | 建议 `type, quality, definitionId, savedAttack, savedDefense, affixes排序, widthOverride, heightOverride`；不含 `id` / 位置态 / 来源态；特殊标签是否纳入待定 |
| 标记 | [S][D][H] |

## D-08 统一交互的实现路径

| 项 | 内容 |
|---|---|
| 选项 | ① 新增独立 `InventoryQuery.cs` 纯查询层，两视图共用（推荐）；② 直接扩充 `ContainerInventoryView` 静态状态；③ 只做 uGUI 一侧 |
| 建议 | **①**：不改变现有共享点（`ContainerInventoryView` 拖拽状态、`CampInventoryView.Section` 已是共享），避免把筛选状态再塞进静态类 |
| 约束 | 不改热键（19 个 `PlayerAction` + 保留键冻结）、不改拾取/穿戴流程、不改 UI 风格、不重复实现业务逻辑 |
| 标记 | [S][D] |

## D-09 仓满 / 失败反馈由谁发出

| 项 | 内容 |
|---|---|
| 问题 | `CampRuntime.DepositEquipment` 目前在 `stored.Count>=Capacity` 时静默 `return false`（`:98`）；文案应由 `CampRuntime` 用 `NotifyMessage` 发，还是视图层按返回值发？ |
| 建议 | **视图层**发（保持 `CampRuntime` 纯业务、避免影响 `Commit` 回滚路径与 `Notice` 行为）；但需按返回值区分「仓满 / 携带中 / 非 InBag / 未选中 / Ready=false」——当前返回 bool 无法区分，需新增只读失败原因枚举或由视图预检 |
| 标记 | [S][D][H] |

## D-10 是否允许新增「批量存取」

| 项 | 内容 |
|---|---|
| 风险 | 多次 `SaveProgress` 对 `revision` / `Flow.Published` 的影响未验证；`Commit()` 有 `committing` 重入保护（`:68`）[S][H] |
| 建议 | 若批准，必须逐件走现有 API，禁止绕过 `Commit`；实施期以真实 Player 验证 revision 语义 |
| 标记 | [S][D][H] |

## D-11 实施批次划分与暂停点

| 项 | 内容 |
|---|---|
| 问题 | 沿用用户既定节奏：独立可运行批次 → 逐批验证 → 全量 SHA 校验 → 暂停待审？ |
| 建议 | 批 1 = P0 可见性（筛选/排序/来源/容量/反馈）；批 2 = P1 对比（含 D-02 决策）；批 3 = P1 收藏（含 D-03 决策）。每批独立 Player 运行、独立证据、独立暂停 |
| 依据 | [E] B1 交付节奏；[D] `PLAYER_ACCEPTANCE.md` |
| 标记 | [E][D] |

## D-12 本轮交付物处置

| 项 | 内容 |
|---|---|
| 问题 | `DeliveryUxProgression04B2/` 11 份文档是否入库、何时入库？ |
| 事实 | 本轮为只读审计，文档为新增 untracked 文件；**未提交、未推送、未建分支** [S] |
| 建议 | 待负责人复审后，按白名单单独提交（不 `git add .`）；B2 文档与 B1 交付物分开 |
| 标记 | [S][D] |

---

## 决策依赖图 [D]

```
D-01(范围) ──┬─> D-02(是否动 AdventureLoadout) ──> 批2 对比
             ├─> D-03(收藏是否持久) ─────────────> 批3 收藏 / 或转 UX-05
             ├─> D-08(统一路径) ──> 批1 P0
             └─> D-11(批次划分)
D-04(地区) ──> 若坚持则脱离 B2，进 UX-05/Schema
D-05(200容量) ──> 维持；改则进 UX-05/Schema
D-06/D-07/D-09/D-10 ──> 批1 实施细节
D-12 ──> 本轮交付物处置
```

**阻断项 [D]**：D-01、D-02 未决前，不得修改任何产品源码。D-03/D-04/D-05 若选择「持久/地区/扩容」，均脱离 B2 范围，须另行授权（UX-05 或 Schema 迁移）。
