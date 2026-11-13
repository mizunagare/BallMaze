# UX-04-B1 分解规则规格（DISASSEMBLY_RULES）

## 一、规则总览（D-16 = B-1）

| 品质 | 枚举值 | 是否可分解 | 界面表现 | 返还 |
|---|---|---|---|---|
| 白 White | 0 | ✅ 可 | 原样 | 铁矿 `quality+1` = 1 |
| 绿 Green | 1 | ✅ 可 | 原样 | 铁矿 `quality+1` = 2 |
| 紫 Purple | 2 | ✅ 可 | 原样 | 铁矿 `quality+1` = 3 |
| 金 Gold | 3 | ❌ 禁 | 「不可分解 · 可入库」禁用 | 无（拒绝，不消耗） |
| 红 Red | 4 | ❌ 禁 | 「不可分解 · 可入库」禁用 | 无（拒绝，不消耗） |

- **唯一阈值**：`item.quality < GearQuality.Gold`。D-24 维持现状，攻击力叠加规则不变。

## 二、服务端单点门禁（B1-02）

### 2.1 判定方法（`AdventureLoadout.cs`）

```csharp
public static bool SalvageAllowed(GearItem item)
    => item != null && item.quality < GearQuality.Gold;
```

### 2.2 分解入口（`AdventureLoadout.Salvage`）

```csharp
public void Salvage(GearItem item)
{
    if(!Owns(item)||item.worn||item.board||Carried(item)||ProtectedEntry(item)) return;
    if(!SalvageAllowed(item)){ hero.Inventory.NotifyMessage("传说/神话品质不可分解 · 可入库"); return; }
    if(hero.Inventory.Count(MaterialKind.Ore) > CampRuntime.MaterialLimit-((int)item.quality+1)
       || !hero.Inventory.CanCarryDelta(MaterialKind.Ore,(int)item.quality+1))
       { hero.Inventory.NotifyMessage("素材堆栈已满，未拆解装备。"); return; }
    items.Remove(item);
    hero.Inventory.Add(MaterialKind.Ore,(int)item.quality+1);
    hero.Inventory.NotifyMessage("已分解为铁矿。");
    Refresh();
}
```

### 2.3 门禁硬性约束

| 约束 | 满足情况 |
|---|---|
| 服务端单点判定（非纯 UI 隐藏） | ✅ 所有入口收敛至 `Salvage` |
| 拒绝不消耗装备 / 材料 | ✅ `SalvageAllowed` 在 `items.Remove` 之前返回 |
| 不影响制造 / 拾取 | ✅ 仅影响 `Salvage` 路径 |
| 不改变分解返还数量 | ✅ 白/绿/紫返还公式 `quality+1` 不变 |
| 不改变经济参数 | ✅ `MaterialLimit` / `Ore` 定义未改 |
| 所有分解入口受保护 | ✅ IMGUI + uGUI 共用同一判定 |

## 三、UI 提示规格（B1-03）

### 3.1 IMGUI 路径（`ContainerInventoryView.cs`）

- 行标签：
  ```csharp
  string b1Label = gear.ProtectedEntry(item) ? "入场保护 · 不可拆解"
                  : b1Locked ? "不可分解 · 可入库" : "分解为铁矿";
  ```
- 按钮启用条件：`!ProtectedEntry(item) && !b1Locked && !item.worn && !item.board && !Carried(item) && !dragging`。
- 金/红时按钮文本为「不可分解 · 可入库」且 `enabled=false`。

### 3.2 uGUI 路径（`CatInventoryPresenter.cs`）

- 明细文案：
  ```csharp
  bool b1Locked = !AdventureLoadout.SalvageAllowed(item);
  // 文案：b1Locked ? "传说/神话品质 · 不可分解 · 可入库" : "本局物资按原规则结算"
  ```
- 拆解按钮：
  ```csharp
  bool canSalvage = item.InBag && !gear.Carried(item) && !gear.ProtectedEntry(item) && !b1Locked;
  Button(b1Locked ? "不可分解 · 可入库" : "拆解换铁矿…", x, y+426, 293, () => salvage = item.id, canSalvage);
  ```
- 「确认拆解」仅在非锁定态（白/绿/紫且 `salvage==item.id`）出现；金/红无二次确认按钮。

### 3.3 UI 约束

| 约束 | 满足 |
|---|---|
| 金/红显示「不可分解 · 可入库」 | ✅ |
| 拆解按钮显式禁用 | ✅ `canSalvage=false` / `enabled=false` |
| 展示原因 | ✅ 文案含「传说/神话品质」 |
| 不改变布局 | ✅ 仅替换文本与启用态 |
| 不新增弹窗流程 | ✅ |
| 「可入库」仅在仓库可用时显示相关入口 | ✅ `InCamp && Items.Count<Capacity` 才渲染存入按钮 |

## 四、保护域（禁止改动）

**B1 严禁**修改以下任意项（完整清单见 `PROTECTION_SHA256.tsv`）：

1. `AdventureLoadout` 攻击力聚合数学（仅允许新增 `SalvageAllowed` 门禁与按钮禁用）
2. 武器伤害：`AdventureCombat.cs` / `GreatswordCombat.cs` / `NewWeaponCombat.cs` / `ScytheCombat.cs`
3. 掉落率 / 宝箱概率
4. 随机流：`WeaponTraits.cs`
5. 制造成本 / 配方：`CraftingRecipeDefinition.cs`
6. 装备尺寸 / 品质数值：`AdventureItems.cs`
7. 存档 Schema：v9 / v10 / v11（`CombatSaveSystem.cs` / `CombatSaveData.cs`）
8. Boss 规则 / 出征流程：`AdventureFlow.cs` / `CombatSession.cs`
9. P1 / P1C 已接受挑战逻辑
10. UX-03 产品功能与验收证据

> 实测：仅 `AdventureLoadout.cs`、`CatInventoryPresenter.cs`、`ContainerInventoryView.cs` 三项 `changed_vs_head=YES`，其余 21 项 `NO`。
