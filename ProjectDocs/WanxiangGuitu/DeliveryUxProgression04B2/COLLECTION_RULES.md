# UX-04-B2 · COLLECTION_RULES（B2-04 收藏与误操作保护）

> 标记：**[S]** 源码事实 · **[E]** Player 证据 · **[C]** 计算结果 · **[D]** 设计推论 · **[H]** 未验证假设

## 1. 载体：会话内 `HashSet<string>` [S]

`Assets/CombatPrototype/B2Collection.cs`：

```csharp
public static class B2Collection {
    static readonly HashSet<string> ids = new HashSet<string>(StringComparer.Ordinal);
    public static readonly string SessionToken = Guid.NewGuid().ToString("N").Substring(0, 12);
    public static bool IsFavorite(string id);
    public static bool Toggle(string id);
    public static bool Add / Remove / Clear();
    public static bool CanQuickDismantle(GearItem item)
        => item != null && !IsFavorite(item.id) && AdventureLoadout.SalvageAllowed(item);
    public static bool BatchPreservesFavourites(IEnumerable<string> afterIds);
}
```

| 硬约束 | 落实 | 标记 |
|---|---|---|
| 不修改 `GearItem` | `AdventureItems.cs` 零变化，19 个字段不变 | [S] |
| 不修改 v9 Schema | `CombatSaveData.cs`/`CombatSaveSystem.cs`/`AdventureValidation.cs` 零变化 | [S] |
| 不增加持久化字段 | 无 `[Serializable]`、无 `JsonUtility` 写入、无存档字段 | [S] |
| 进程重启后清空 | 普通进程内静态字段；每次进程启动重新初始化 | [S][E] |
| 不引入耐久/维修/升星/新货币 | 无新增类型、无 `MaterialKind` 变更 | [S] |

`SessionToken` 仅用于验收时证明「这是一个新进程」；它不是持久化数据，也不写入存档。[D][E]

## 2. 收藏不能被快速分解（服务端单点）[S][E]

`AdventureLoadout.Salvage` 是**所有**分解入口的唯一汇聚点（IMGUI、uGUI、未来任何路径）。B2 在其内部加入**唯一**权威门禁，位于任何状态改变之前：

```
if (!Owns(item) || item.worn || item.board || Carried(item) || ProtectedEntry(item)) return;
if (!SalvageAllowed(item)) { "传说/神话品质不可分解 · 可入库"; return; }   // B1 D-16 未改
if (!B2Collection.CanQuickDismantle(item)) { "已收藏装备不可快速分解 · 请先取消收藏"; return; }  // B2-04
... 材料堆栈检查 ... items.Remove(item); Add(Ore, quality+1);
```

顺序保证 B1 的金/红门禁语义不被覆盖。[S]

**Player 证据（`UX04-B2-UGUI-FINAL`，全部真实鼠标点击）** [E]：

| 步骤 | 真实点击 | 观测 | 结论 |
|---|---|---|---|
| 收藏 | `★收藏` | `favorite=True count=1` | 收藏成功 |
| 尝试分解 | `已收藏 · 先取消收藏`（interactable=False） | `canQuickDismantle=False stillOwned=True ore=0` | **装备未消耗、材料未变** |
| 取消收藏 | `★取消收藏` | `removed=True count=0` | 主动取消允许 |
| 一次确认 | `拆解换铁矿…` | `armed; stillOwned=True` | 未消耗 |
| 二次确认 | `确认拆解` | `consumed=True ore=1` | 仅在二次确认后消耗 |

## 3. 重要破坏性操作二次确认 [S][E]

| 操作 | IMGUI | uGUI | 标记 |
|---|---|---|---|
| 分解 | 新增 `armedSalvageId` 两段式：先「分解为铁矿」→ 再「确认拆解」 | 既有 `salvage` 两段式保留，并叠加收藏门禁 | [S] |
| 批量整理 | `SortBag` / `SortWarehouse` 前置校验（见 §4） | 同左（同一业务方法） | [S] |
| 永久弃置 | 既有二次确认逻辑未改 | 既有 `discard` 两段式未改 | [S] |

IMGUI 原先是单击直接分解，本轮补齐为二次确认，与 uGUI 对齐。[S]

## 4. 收藏装备不能被批量整理误删 [S]

- `AdventureLoadout.SortBag()`：在 `CommitChange` 前校验 `preview != null && preview.Count == items.Count && B2Collection.BatchPreservesFavourites(preview.Select(i => i.id))`；不满足则提示「整理会遗漏收藏装备，已取消；原布局保留」并拒绝。[S]
- `CampRuntime.SortWarehouse()`：同样校验 `sorted.Length == stored.Count` 且收藏 id 全部保留。[S]
- 二者只重排坐标/顺序，本就不删除物品；新校验使「收藏不丢」成为显式不变量。[D]

## 5. 正常入库 / 取出 / 穿戴不受影响 [S][E]

收藏状态**不参与**以下任何判定：`DepositEquipment`、`WithdrawEquipment`、`SelectMain`、`SelectReserve`、`Place`/`Move`/`AutoMove`、`EquipContainer`、`Fit`。[S]

Player 证据 [E]：`UX04-B2-UGUI-FINAL` 的 `deposit-after`（金色入库 `0→1`）、`withdraw-after`（取回 `1→0`，`backInLoadout=True`），以及 B1 门禁金/红 `allowed=False` 均 PASS；收藏流程中同一件装备的入库/取出/穿戴未被阻断。[E]

## 6. 进程重启清空（跨进程实证）[E]

| 运行 | 进程 | 观测 |
|---|---|---|
| `UX04-B2-FAVSEED-FINAL` | A | `seeded=3 token=<A>`，写出 `_favseed.json`（token、count=3、3 个 id） |
| `UX04-B2-RESTART-FINAL` | **全新进程 B** | `collectionCount=0 token=<B>`、`priorSeedPresent=True`、`priorCount=3`、`tokenChanged=True`、`noneFavourite=True` |

即：进程 A 的 3 件收藏在进程 B 中既不在集合内、也没有任何 id 仍被标记为收藏，且会话令牌不同。这是「会话内、不持久化」的直接实证，而非仅从代码推断。[E]

## 7. 重复装备识别只提供提示 [S]

`B2InventoryQuery.DuplicateKey` / `DuplicateHints` 只做计数；两条 UI 只追加「同类同属性 ×N（仅提示，不合并）」文本。无自动合并、无删除、无写入。[S] 详见 `INVENTORY_FILTERS.md §5`。

## 8. 与 B1 的关系 [S][E]

| B1 成果 | 状态 |
|---|---|
| `SalvageAllowed = quality < Gold` | 未改 |
| 金/红「不可分解 · 可入库」文案与按钮禁用 | 未改 |
| 拒绝不消耗装备/材料 | 未改，`UX04-B2-UGUI-FINAL` 的 `uGUI-B1-Gold/Red` 均 `allowed=False stillOwned=True` |
| 金/红可入库/取回 | 未改，`deposit/withdraw` PASS |

B2 的收藏门禁是**加在 B1 门禁之后**的新准入条件，不改变 B1 行为。[S]

## 9. 待验证假设 [H]

1. `B2Collection` 是进程内静态类；Unity 域重载（Domain Reload）同样会清空，本轮只在「进程重启」维度做了跨进程实证。
2. 「批量整理」本轮未用真实点击把 200 件装满后再整理；保护以源码不变量 + 仓满场景的 Player 验证为主，未做「整理时故意构造缺件」的故障注入。
3. 收藏集合未设上限；极端数量下的性能未实测（当前为 `HashSet<string>`，O(1) 查询）。
