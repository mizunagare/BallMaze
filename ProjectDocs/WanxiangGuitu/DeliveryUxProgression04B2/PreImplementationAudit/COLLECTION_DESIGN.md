# UX-04-B2 · B / D：装备分类筛选 + 收藏与锁定设计

> 标记：**[S]** 源码事实（含 file:line）· **[E]** Player 证据 · **[C]** 计算结果 · **[D]** 设计推论 · **[H]** 未验证假设

---

## 第一部分 · B：装备分类与筛选方案

### B.0 原则：优先使用现有数据，不新增来源字段

`GearItem` 已有 `origin` + `originRunId`（`AdventureItems.cs:9-10`），且被 v9 存档校验**强约束**：`AdventureValidation.cs:35` 要求 `i.originRunId==run.runId && i.origin==(入场保护?...:ItemOrigin.RunLoot)` [S]。因此**任何新增「来源字段」或修改 `origin` 语义都会破坏存档校验** [S][D]。B2 全部筛选维度必须基于现有可派生数据。

### B.1 六项筛选维度逐条可行性

| # | 需求 | 现有数据 | 可行性 | 实现口径 | 标记 |
|---|---|---|---|---|---|
| 1 | 按武器类型筛选 | `GearType`（14 值含 TwinBlades/Greatsword/Scythe）+ `NewWeaponRegistry.Is()` + `AdventureItems.TypeName()` | ✅ 已有 | 按 `type` 精确分组；武器组用 `i.Weapon`（`(int)type<4 || Is(type)`），容器组用 `i.Container` | [S] `AdventureItems.cs:5,23,26,58` |
| 2 | 按品质筛选 | `GearQuality 0..4` + `QualityName()` + `Color()` | ✅ 已有 | 五档多选 | [S] `:6,59-60` |
| 3 | 按攻击力排序 | `item.Attack`（`savedAttack`/`LegacyAttack` 已统一）、`item.Defense`、`Power` | ✅ 已有 | 以 `Attack` 为主键排序；**需注明这是「装备自身攻击」，不等于对 `AttackPower` 的实际贡献**（备用/容器/状态门见 `EQUIPMENT_COMPARISON.md`） | [S] `:30,34-35` [D] |
| 4 | 按装备状态筛选 | `InBag`/`board`/`overflow`/`worn`/`Carried(Main,Reserve)`/`ProtectedEntry`/`SalvageAllowed` | ✅ 已有（全部派生） | 状态枚举；`ProtectedEntry` 依赖 `AdventureFlow.Protects`（`AdventureFlow.cs:228`），`SalvageAllowed` 为 B1 静态门 | [S] |
| 5 | 按获取地区 / 来源分类 | `origin` 4 值 + `originRunId` + `SourceLabel()`；**地区仅在 `RunState.region`（局级），`GearItem` 上无地区字段** | ⚠️ **部分可行** | 仅可按 `origin` 类别（入场保护 / 本局战利品 / 旧档保护 / 未指定）与 `originRunId` 归类；**按「获取地区」不可实现**——需关联局档案，且局结束后 `RunState` 不随装备持久化 | [S] `AdventureState.cs:22,27`、`AdventureFlow.Supplies.cs:15` |
| 6 | 按未使用 / 已装备 / 已收藏分类 | 前两者可派生；「已收藏」**无任何现有标记** | ⚠️ 前两项 ✅，第三项需设计 | 「未使用」= `InBag && !Carried && !board`；「已装备」= `board || worn || Carried`；「已收藏」见第二部分 | [S][D] |

### B.2 第 5 项的明确边界 [S][D]

- 需求原文限定「**仅在已有数据支持时**」且「**没有来源数据时不得增加新的来源字段**」。源码事实：装备级来源数据只有 `origin/originRunId`，**没有地区/区域字段**；`RunState.region`（`ForestRuins` / 遗迹 / 晶穴）属于局状态，不随单件装备落盘（`AdventureData.World()` 会把 `warehouseGear` 等清空，`AdventureState.cs:73`）。
- 因此 B2 **不实现「按获取地区分类」**，也不新增任何来源字段；仅把现有 `SourceLabel`（目前**只有 IMGUI 展示**，`ContainerInventoryView.cs:129`）统一到两条 UI 路径上，作为「来源」维度的只读展示 [D]。
- 若未来确需地区维度，应属于 UX-05 或 Schema 迁移范畴（需新增字段 + 迁移 + 校验放通），本轮禁止 [D]。

### B.3 现有筛选实现的不一致（必须统一）[S]

| 路径 | 筛选项 | 判定式 | 差异 |
|---|---|---|---|
| IMGUI `ContainerInventoryView.cs:50,60` | `{"全部","装备","武器","素材"}`，`filter` 静态 | `Visible(i) => filter==0 || (filter==1 && !i.Weapon) || (filter==2 && i.Weapon)`；`filter==3`（素材）**不显示任何装备** | 4 项、索引语义为「装备=非武器」 |
| uGUI `CatInventoryPresenter.cs:32,41` | `{"全部","武器","装备","材料","消耗品","任务物品"}` | `filter==0 || (filter==1 && i.Weapon) || (filter==2 && !i.Weapon)`；`filter>=3` 改为显示材料面板 | 6 项、索引 1/2 与 IMGUI **恰好相反** |

**关键风险 [S]**：两条路径的 `filter` 索引语义冲突（IMGUI `1=非武器` / uGUI `1=武器`），若把二者合并为一个共享筛选状态而不同时改写两处判定，会产生「选中武器却显示护甲」的错误。B2 建议以**语义枚举**（而非整数索引）作为共享筛选契约，两视图各自渲染 [D]。

### B.4 统一筛选服务草案 [D]

新增一个**纯查询层**（无 MonoBehaviour、不落盘、不改 `GearItem`）：

```
InventoryQuery.Filter(IEnumerable<GearItem> src, FilterSpec spec) -> IEnumerable<GearItem>
FilterSpec { GearType? type; GearQuality[] qualities;
             Status status; OriginKind origin; SortKey sort; bool desc; string text; }
```

- 输入源：`gear.items`（随身）、`camp.Items`（仓库）、两者并集（带「所在位置」标签）[D]。
- 排序键：`Attack` / `Defense` / `quality` / `type` / `Cells().Count()` / `Name`；**排序结果不得被解释为战力变化** [D]。
- 关键词检索：`item.Name`、`AdventureItems.TypeName(type)`、`WeaponTraits.Names[affix]` [D]。
- 复用现有 `PreviewSortBag()`/`SortWarehouse()` 的排序口径（容器优先 → 占格降序 → id 升序，`AdventureLoadout.cs:75-78`、`CampRuntime.cs:63`）作为「整理」而非「筛选」的实现 [S][D]。
- 该服务**只读**，不产生任何存档写入或物品变更 [D]。

---

## 第二部分 · D：收藏与锁定

### D.1 现状：不存在任何收藏/锁定字段 [S]

全项目 `*.cs` 搜索 `favorite / Favorite / starred / pinned / isLocked / bookmark / 收藏 / 锁定`：**无 per-item 持久标记**。`GearItem` 无 partial 定义，19 个字段已枚举完毕（`INVENTORY_AUDIT.md §1.1`）。`RuinsSpecialRewards.CollectionLabel`（`RuinsSpecialRewards.cs:105`）与 `ProfileState.specialRewards` 是**档案级奖励回执**，不是装备收藏 [S]。

### D.2 优先方案：不增加持久化字段的临时收藏 [D]（推荐）

| 方案 | 载体 | 跨重启 | 存档影响 | 评价 |
|---|---|---|---|---|
| **A. 会话内临时收藏（推荐）** | 运行时 `HashSet<string>` 存 `GearItem.id`，挂在现有 presenter / 一个纯 C# 服务上；**不写入 `GearItem`、不写入 `CombatSaveData`** | ❌ 重启即清空 | **零** | ✅ 满足「不引入不必要的存档复杂度」；id 全局唯一且 `Clone()` 保留（`AdventureItems.cs:44`），可作为稳定键 |
| B. 复用现有字段承载收藏 | 借用 `originRunId` / `affixes` / `widthOverride` 等 | ✅ | ❌ 破坏校验：`AdventureValidation.cs:35` 强校验 `originRunId`；`ValidateCurrentItem` 校验 `affixes` 仅武器 ≤2、`widthOverride<=12` | ❌ **禁止** |
| C. 新增 `GearItem` 持久字段 | `bool favorite` | ✅ | 需 Schema 变更 | ⚠️ 见 §D.3，需另行授权 |
| D. 新增 `ProfileState` 独立收藏列表 | `string[] favoriteIds` | ✅ | 需 Schema 变更 + 校验放通 + 迁移 | ⚠️ 复杂度高于 C，不推荐 |

**方案 A 语义 [D]**：仅影响「筛选视图的默认分组 / 置顶 / 高亮」，**不改变**物品身份、属性、容器位置、穿戴、存取、分解。收藏状态丢失时不影响任何玩法结果 → 无存档复杂度。

### D.3 若要求跨重启保留：v9 Schema 影响评估 [S][D][H]

| 影响面 | 事实 / 推论 | 标记 |
|---|---|---|
| 序列化机制 | `CombatSaveData` 整对象 `JsonUtility.ToJson(disk)`（`CombatSaveSystem.cs:88`），**无字段白名单**；`GearItem` 新增字段会自动进入 payload | [S] |
| 版本白名单 | `ReadChecked` 仅接受 `version 1..9`（`CombatSaveSystem.cs:232`）；**无 v10/v11** | [S] |
| 校验器 | `ValidateCurrentItem`（`:311-323`）逐字段 `Require(...)`；`AdventureValidation.Loose`（`:22`）、`Profile()`、`Validate(run)` 的 `originRunId` 一致性（`:35`） | [S] |
| 新增字段是否被拒 | `JsonUtility.FromJson` 忽略未知 JSON 键 → 旧档读入新字段取默认值；新增字段**不会被现有校验器显式拒绝**，但也**不会被校验**（完整性缺口） | [S][H] |
| 兼容性风险 | 新档含新字段 → 旧构建读入忽略该字段，不报错；但 **checksum 基于 payload**（`:89,233`），跨构建读写同一档可能导致「收藏状态静默丢失」而非报错；此外 `GroundLootStore.Pack`（`:87`）把 `loot` 分页到独立 json，新增字段同样扩散 | [S][H] |
| 迁移工作量 | 需新增字段 → 全量校验器补 `Require` → `AdventureValidation` 补一致性 → 版本策略（是否 bump 到 v10 并放通白名单）→ 旧档迁移/默认值 → 跨版本回归 | [D] |
| 结论 | **跨重启保留 = Schema 迁移**，属于 UX-05 或独立授权批次，**本轮禁止** | [D] |

### D.4 「锁定装备能否阻止分解」[S][D]

现有 `Salvage` 已有 5 道准入 + 1 道品质门（`AdventureLoadout.cs:214-219`）：`Owns` / `!worn` / `!board` / `!Carried` / `!ProtectedEntry` → `SalvageAllowed(quality<Gold)` → 铁矿堆栈。**当前分解保护已覆盖**：穿戴容器、盘内装备、主/备武器、入场保护装备、金/红装备 [S]。

- **金/红是否还需额外锁定？** 不需要 [S][D]：B1 的 `SalvageAllowed` 已按品质硬拒，任何额外锁定对金/红都是冗余；B1 真实 Player 证据显示金/红拒绝后装备数与材料数均不变 [E]。额外锁定只会增加状态与存档复杂度，违反「不引入不必要的存档复杂度」。
- **白/绿/紫是否需要锁定？** 这是「误操作保护」的合理诉求，但应优先用**交互层**手段（二次确认）而非新持久字段 [D]：uGUI 已有二次确认范式（`CatInventoryPresenter.cs:44` 的 `salvage` 确认态），IMGUI 目前是单击直接分解（`ContainerInventoryView.cs:137`）——**两条路径保护不对等** [S]。统一为「二次确认 + 会话内锁定集合」即可，无需 Schema 变更 [D]。
- 若未来要「锁定」持久化，应与 §D.3 一并评估，不在本轮 [D]。

### D.5 收藏状态是否影响容器移动与穿戴 [D]

**结论：不影响。** 收藏/锁定应定义为**纯视图标记**：不参与 `CanPlace`/`Fit`/`SelectMain`/`SelectReserve`/`DepositEquipment`/`WithdrawEquipment`/`Salvage` 的任何判定（除非明确把它作为 `Salvage` 的额外准入，且需在服务端单点实现）[D]。理由：一旦参与移动/穿戴判定，就会改变「找到装备 / 管理库存」之外的玩法语义，并可能在 `Commit()` 回滚路径（`CampRuntime.cs:90`）产生状态不一致 [S][D]。

### D.6 不得引入的内容（硬约束核对）[S][D]

| 禁止项 | B2 方案是否触碰 |
|---|---|
| 装备耐久 / 维修 / 升星 | ❌ 不触碰 |
| 新货币 | ❌ 不触碰（材料种类固定 6 种 `MaterialKind`，`PlayerInventory.cs:6`） |
| 修改存档 | ❌ 方案 A 零写入 |
| 新增来源字段 | ❌ 明确拒绝 |
| 修改 B1 / main | ❌ 不触碰 |

---

## 7. 待验证假设 [H]

1. 会话内 `HashSet<string>` 的生命周期（跨页面切换 / 跨局 / 营地进出）尚未定义，需负责人确认「收藏保留到何时」。
2. `JsonUtility` 对未知键的忽略行为基于 Unity 常规语义，本轮未做跨构建读档 Player 验证。
3. 「来源按 `origin` 展示」是否需要保留 `SourceLabel()` 的「死亡丢失 / 失败归还」措辞，需产品确认（涉及局语义，B2 不改写）。
