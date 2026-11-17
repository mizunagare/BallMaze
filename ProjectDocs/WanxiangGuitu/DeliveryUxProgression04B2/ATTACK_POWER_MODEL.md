# UX-04-B2 · ATTACK_POWER_MODEL（B2-01 统一只读攻击力计算）

> 标记：**[S]** 源码事实 · **[E]** Player 证据 · **[C]** 计算结果 · **[D]** 设计推论 · **[H]** 未验证假设

## 1. 授权与边界

| 项 | 结论 | 标记 |
|---|---|---|
| D-02 | 批准等价重构 + `AdventureLoadout` 只读攻击力计算接口 | [S] |
| D-24 | 保持现有攻击力叠加规则（未改任何系数/求和式） | [S] |
| 不产生第二套业务逻辑 | `Attack`/`Defense` 实时属性与预览共用**同一个**纯函数 | [S] |
| 不修改实际装备状态 | 预览仅在 `Clone()` 副本上计算 | [S] |
| 不修改存档 | 无任何写入路径 | [S] |
| 不修改装备系数 | `attackFactor`/`Power`/`SpearPower` 全部未改 | [S] |

## 2. 权威计算链（源码事实）

```
AdventureLoadout.Active  = B2AttackModel.Active(items, mainWeapon)                    [S]
B2AttackModel.Active     = Unique.Where(!overflow && !worn && (board || i == Main))  [S]
                           Unique = GroupBy(id).First()   (LINQ 首次出现序)           [S]
                           Main   = Find(i.id==mainId && i.InBag && i.Weapon)        [S]
AdventureLoadout.Attack  = B2AttackModel.ComputeAttack(items, mainWeapon, Rig, Bag)  [S]
ComputeAttack            = Σ Active.Attack + rig.attackBonus + bag.attackBonus       [S]
ComputeDefense           = Σ Active(board).Defense + rig.defenseBonus + bag.defenseBonus [S]
HeroEquipment.AttackBonus= AdventureLoadout.Attack                                   [S]
ThirdPersonHero.AttackPower = attackDamage(25) + AttackBonus + Progression.AttackBonus [S]
                              Progression.AttackBonus = Rank(Strength)*5            [S]
AdventureCombat.BasicPower  = AttackPower * (MainWeapon==Spear ? SpearPower(1.25) : 1) [S]
GearItem.Attack             = dataRevision>0 ? savedAttack : LegacyAttack           [S]
savedAttack(new)            = Container ? 0 : Power * Definition.attackFactor       [S]
```

**D-24 等价性证明 [C][E]**：黄金矩阵用**逐字复刻的旧表达式**（`LegacyAttack`，写在 sidecar 里，独立于产品代码）与 `B2AttackModel.ComputeAttack` 对同一组真实运行时 `GearItem` 求 IEEE-754 位模式并比较。24 行全部 `bitsEqual=True`，`Attack` 与 `Defense` 均逐位相等，`G0-live` 中实时 `gear.Attack` 位模式与统一链相等（`liveMatch=True`）。[E] `Evidence/Runs04B2/UX04-B2-GOLDEN-FINAL/b2-observations.jsonl`

## 3. 只读接口

| 接口 | 位置 | 语义 | 标记 |
|---|---|---|---|
| `B2AttackModel.Active(list, mainId)` | `B2AttackModel.cs` | 复刻旧 `Active` 判定 | [S] |
| `ComputeAttack(list, mainId, rig, bag)` | 同上 | 权威链，实时属性委托 | [S] |
| `ComputeDefense(...)` | 同上 | 权威链 | [S] |
| `Snapshot(list, mainId, reserveId, rig, bag, hero)` | 同上 | 返回 `B2AttackSnapshot`（AttackPower / BasicPower / 各贡献） | [S] |
| `Preview(gear, hero, candidate, role)` | 同上 | 在 Clone 副本上模拟替换，返回前后与 Δ | [S] |
| `AdventureLoadout.AttackSnapshot()` | `AdventureLoadout.cs` | 只读实例入口 | [S] |
| `AdventureLoadout.PreviewReplacement(candidate, role)` | 同上 | 只读实例入口（D-02 指定） | [S] |
| `AdventureLoadout.ContainersFor(list, board)` | 同上 | 公开既有静态 `ContainerFor`，供副本计算 rig/bag | [S] |

`B2EquipRole`：`None / Main / Reserve / Board / Overflow / Worn / ContainerRig / ContainerBag`。[S]

**只读性 Player 证据 [E]**：`G7-preview` = `readOnly=True mainDelta=124 reserveDelta=0 mainAP=33→157 reserveAP=33→33`。预览前后 `gear.items.Count` 与 `gear.mainWeapon` 均未变。

## 4. 黄金矩阵（逐位对照旧结果）

来源：`UX04-B2-GOLDEN-FINAL`。`legacyBits`/`unifiedBits` 为 `BitConverter.SingleToInt32Bits` 值。[E][C]

| 场景 | legacy / unified | 位模式 | AttackPower | BasicPower | 关键点 |
|---|---|---|---|---|---|
| 实时基线 G0 | 8 / 8 | 1090519040 | 33 | 33 | `liveMatch=True` |
| 主武器 白 | 8 / 8 | 1090519040 | 33 | 33 | Power=8 |
| 主武器 绿 | 19 / 19 | — | 44 | 44 | Power=19 |
| 主武器 紫 | 43 / 43 | 1110179840 | 68 | 68 | Power=43 |
| 主武器 金 | 78 / 78 | — | 103 | 103 | Power=78 |
| 主武器 红 | 132 / 132 | 1124335616 | 157 | 157 | Power=132 |
| 长枪 紫 | 43 / 43 | 1110179840 | 68 | **85** | `SpearPower=1.25` |
| 饰品 红（盘内） | 74 / 74 | 1116995584 | 99 | 99 | `132×0.5=66` + 主 8 |
| 护臂 红（盘内） | 54.2 / 54.2 | 1113115853 | 79.2 | 79.2 | `132×0.35=46.2` + 主 8 |
| 备用 红 | 8 / 8 | 1090519040 | 33 | 33 | **备用贡献恒为 0** |
| Overflow 金 | 8 / 8 | 1090519040 | 33 | 33 | 不进入 Active |
| Worn 金 | 8 / 8 | 1090519040 | 33 | 33 | 不进入 Active |
| Board 金 | 86 / 86 | 1118568448 | 111 | 111 | 主 8 + 盘内 78 |
| 容器加成 | 14 / 14 | 1096810496 | 39 | 39 | `bag_relic +6`、`rig_heavy` |
| 七武器 | 全部逐位相等 | — | — | — | Sword/Spear/Staff/Bow/TwinBlades/Greatsword/Scythe |

**备用武器贡献为 0 [S][C]**：`Active` 的非 board 条件只有 `i == Main`；`Reserve` 虽 `InBag` 但不入选。矩阵 `reserve-red` 的 `reserveContribution=0` 且 `reserveAP=33→33`（Δ=0）。

**饰品 0.5 / 护臂 0.35 [S][E]**：`ItemData/accessory.asset:26 attackFactor: 0.5`、`arms.asset:26 attackFactor: 0.35`；旧档路径 `AdventureItems.cs:32` 同样为 `.5f/.35f`。Player 实测 `board-Accessory` = 66、`board-Arms` = 46.2（基于红 Power 132）。

**禁止简单差值 [D][E]**：`Preview` 走完整链。`Main`（红剑替换白剑）Δ=+124；`Reserve`（同一红剑）Δ=0；容器加成 Δ=+6（物品自身 `Attack=0`）；长枪替换使 `BasicPower` 变化而 `AttackPower` 可不变。任何 `candidate.Attack − current.Attack` 都会在这些场景出错。`EQUIPMENT_COMPARISON.md` 给出完整反例集。

## 5. 与保护域的关系

| 保护项 | 状态 | 标记 |
|---|---|---|
| 攻击力实际计算系数 | 未修改（`AdventureItems.cs`/`ItemDefinition.cs`/`QualityData` 零变化） | [S] |
| D-24 叠加规则 | 未修改，逐位等价 | [S][E] |
| `ThirdPersonHero.AttackPower` / `HeroEquipment` / `AdventureCombat` | 零变化 | [S] |
| v9/v10/v11 Schema | 零变化 | [S] |
| 随机流 / 掉落率 / 制造成本 / 装备尺寸 | 零变化 | [S] |

## 6. 待验证假设 [H]

1. 黄金矩阵覆盖的类型/品质组合为代表性采样，不穷举所有 affix 与容器组合；但旧/新两条链共享同一 `GearItem.Attack`，故对任意输入都逐位等价（等价性由表达式结构保证，非仅采样）。
2. `Preview` 的 `Board` 角色是「假设放置成功」的攻击力预演；实际放置仍需 `CanPlace` 通过，二者在实现中分离。
3. 本轮未在 Editor 内运行 Unity Test Framework；等价性以真实 Player 运行时的 IEEE-754 位模式比较为证。
