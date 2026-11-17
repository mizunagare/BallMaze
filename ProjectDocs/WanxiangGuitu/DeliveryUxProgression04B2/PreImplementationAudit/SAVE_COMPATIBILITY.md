# UX-04-B2 · 存档兼容性（v9 / v10 / v11）

> 标记：**[S]** 源码事实（含 file:line）· **[E]** Player 证据 · **[C]** 计算结果 · **[D]** 设计推论 · **[H]** 未验证假设
> 本轮**只读**：未修改任何存档、Schema、版本字段、校验器。

---

## 1. 当前存档结构（源码事实）

### 1.1 信封

```csharp
[Serializable] public class CombatSaveEnvelope {
    public int version = 9;                       // CombatSaveData.cs:41
    public long revision;
    public string savedAtUtc, payload, checksum;
}
```

- 写入：`SaveProgress()` → `CaptureLegacy()` → `session.Flow.Compose(live)` → `AdventureData.Clone(data)` → `JsonUtility.ToJson(disk)` → `envelope.version = session.Flow.Enabled ? 9 : 6` → `checksum = Checksum(payload)` → `.tmp` + `File.Replace` 原子发布（`CombatSaveSystem.cs:75-106`）[S]
- v9 时 `GroundLootStore.Pack(disk, folder)` 把 `loot` 分页到 `ground-loot/*.json`（`:87`）；读档 `Unpack`（`:235`）[S]
- 写入还限制 `payload` ≤ 8MB（`:94`）、`checksum` 为 SHA256（`:222-225`）[S]

### 1.2 版本白名单（关键）

`CombatSaveSystem.ReadChecked` (`:227-241`) [S]：

```csharp
if (envelope.version != 1 && ... && envelope.version != 9)
    throw new NotSupportedException("未知存档版本");
```

| 事实 | 值 | 标记 |
|---|---|---|
| 接受版本 | **1,2,3,4,5,6,7,8,9** | [S] `:232` |
| v10 / v11 | **全项目 `*.cs` 未找到任何定义或白名单条目** | [S] |
| v6 | 旧波次流程（`session.Flow.Enabled==false` 时写入） | [S] `:89` |
| v7 / v8 归档 | 读档时自动备份 `save-v7-before-pve-v8.json` / `save-v8-before-v9.json`（`:236-238`） | [S] |
| 迁移 | `AdventureMigration.Normalize / UpgradeV7`；`sourceVersion<9` 触发 `SaveRecoveryMigration()` 重存为 v9（`:163,205,239`） | [S] |

### 1.3 装备数据的落盘位置 [S]

| 数据 | 类型 / 位置 | 声明 |
|---|---|---|
| 随身装备 | `CombatCheckpoint.gear : GearItem[]`，`mainWeapon` / `reserveWeapon` | `CombatSaveData.cs:27` |
| 永久仓库 | `CombatCheckpoint.warehouseGear : GearItem[]`、`warehouseMaterials : int[]`，以及 v9 的 `ProfileState.warehouse` | `:11-12`、`AdventureState.cs:12` |
| 地面装备 | `SavedLoot.gear`（`loot` 数组 / v9 分页文件） | `:40` |
| 入场装备 | `RunState.entryGear : GearItem[]` | `AdventureState.cs:39` |
| 待领取装备 | `PendingReward.item` | `AdventureValidation.cs:17` |

- `CaptureLegacy()` 写入：`warehouseGear=session.Camp.Items.Select(Clone).ToArray()`（`:114`）、`gear=...items.ToArray(), mainWeapon, reserveWeapon`（`:118`）[S]
- v9 实际由 `AdventureFlow.Compose`（`AdventureFlow.cs:82-88`）把等价数据放到 `ProfileState.warehouse` / `profile.camp` / `activeRun.checkpoint`；顶层 `warehouseGear/gear` 在 v9 信封中不填充 [S]
- 恢复路径：`CombatSaveSystem.cs:170,175,177`（v<7）、`:213`（`RestoreWorld`）、`AdventureFlow.cs:95,111,131`（v≥7）[S]

### 1.4 GearItem 序列化：无字段白名单 [S]

`GearItem` 标记 `[Serializable]`（`AdventureItems.cs:7`），19 个 public 字段**全部**由 `JsonUtility.ToJson` 写入。`GroundLootStore.cs:29` 对 `SavedLoot.gear` 同样整体序列化。项目中**不存在**针对 `GearItem` 的反射字段枚举或字段白名单（唯一 `GetFields()` 在 `RouteEvaluation.cs:50`，作用于自身 float 字段）[S]。

### 1.5 校验器（逐字段 `Require`）[S]

| 校验器 | 位置 | 关键约束 |
|---|---|---|
| `CombatSaveSystem.Validate` | `:247-282` | `game=="ForestRuins"`、wave/level 范围、materials 长度 3/6、`ValidateContainers/Warehouse`、`reserveWeapon` 合法性（`:281`） |
| `ValidateCurrentItem` | `:311-323` | id≤64、`NewWeaponRegistry.Valid(type)`、`quality 0..4`、`dataRevision==1`、`rotation 0..3`、`savedAttack/Defense` 有限非负、`affixes` 仅武器≤2 且不重复、`definitionId` 必须存在、`worn` 仅容器且 `x==y==-1`、`overflow` 则 `x==y==-1`、容器 `savedAttack==0 && savedDefense==0` |
| `ValidateContainers` | `:324-339` | `gear.Length 2..1024`、id 唯一、**恰好 1 个 worn 胸挂 + 1 个 worn 背包**、网格 `Allows` 且不重叠、`mainWeapon` 必须 `Weapon && InBag` |
| `ValidateWarehouse` | `:283-289` | `warehouseGear.Length<=Capacity(200)`、仓库物品 `!board && !worn && !overflow && x==y==-1`、全局 id 唯一 |
| `AdventureValidation.Validate` | `:27-59` | `p.warehouse.Length<=200`、`pending.Length<=4096`、`origin` 一致性（`:35`：`i.originRunId==run.runId && i.origin==...`）、`Loose()`（`:22`） |
| `AdventureValidation.Loose` | `:22` | `quality<=4`、`dataRevision==1`、`savedAttack/Defense` 有限 |

---

## 2. B2 方案对存档的影响：零 [D]

| B2 功能 | 是否写入存档 | 理由 |
|---|---|---|
| 分类 / 筛选 / 排序 / 搜索 | ❌ | 只读投影（视图 + 纯查询层） |
| 装备对比 | ❌ | 在 `Clone()` 副本上预览，不改 `items` |
| 会话内收藏 | ❌ | 运行时 `HashSet<string>`，不进 `GearItem`、不进 `CombatSaveData` |
| 容量展示统一 / 仓满文案 | ❌ | 视图 / `NotifyMessage` |
| 批量存取 | ⚠️ 间接 | **逐件走现有 `DepositEquipment`/`WithdrawEquipment` → `Commit → SaveProgress(false)`**，与现有单次存取同一写入路径，Schema 不变 |
| 重复件识别 / 库存整理 | ❌ / ⚠️ | 识别只读；`SortBag`/`SortWarehouse` 会改 `x/y` 并经 `Commit` 落盘，但**字段集合不变** |

**结论 [D]**：B2 全部核心能力不新增字段、不改枚举、不改版本、不改校验器、不改 payload 结构。唯一可能触发存档写入的是用户主动执行「整理/存取」，且走既有原子提交，与 B1 之前的存档字节结构兼容。

---

## 3. 若未来新增持久字段（跨重启收藏）的影响评估 [S][D][H]

| 影响面 | 评估 | 标记 |
|---|---|---|
| 是否需 bump 版本 | 技术上**不必**：`JsonUtility.FromJson` 忽略未知键，旧构建读新档不报错；但**强烈建议**作为显式 Schema 迁移并配套版本策略，因为无法区分「不支持该字段的旧构建」 | [S][H] |
| 旧构建读新档 | 新字段被静默忽略 → 收藏状态**丢失但不报错**；`checksum` 针对 payload 整体（`:89,233`），旧构建按整串校验仍通过 | [S][H] |
| 新构建读旧档 | 新字段取 CLR 默认值（bool=false / 引用=null）；需显式定义默认值语义 | [H] |
| 校验器 | 现有 `Require` 逐字段，**不会拒绝新字段**，但也**不会校验**它 → 完整性缺口；应在 `ValidateCurrentItem`/`Loose`/`Profile` 补 `Require` | [S][D] |
| 扩散面 | 新增字段会进入 `gear`/`warehouseGear`/`ProfileState.warehouse`/`SavedLoot.gear`/`RunState.entryGear`/`PendingReward.item` **全部**装备实例，并进入 `ground-loot` 分页文件 | [S][D] |
| `origin` 强校验 | `AdventureValidation.cs:35` 对 `run.checkpoint.gear` 强校验 `originRunId/origin`；任何借用或改写来源字段的方案都会直接触发 `InvalidDataException` | [S] |
| 200 上限 | 与仓库字段同时修改会牵动 `AdventureValidation.cs:12` 与 `CombatSaveSystem.cs:285` 两处硬编码 | [S] |
| 结论 | **跨重启收藏 = Schema 迁移**，需 UX-05 或独立授权批次；本轮禁止 | [D] |

---

## 4. v9 读档兼容性证据（B1 真实 Player）[E]

| 证据 | 值 | 来源 |
|---|---|---|
| 读档运行 | `UX04-B1-READBACK-01`，2 运行 / 2 PASS / 28 证据文件哈希自洽 | `DeliveryUxProgression04B1/EVIDENCE/INDEX.json` |
| 读档结果 | `version=9 revision=4`，10 件装备全部载入，`AttackPower=33` | `Evidence/Runs04B1/UX04-B1-READBACK-01/b1-observations.jsonl` |
| 金/红读回 | `神话·长剑`(红) / `传说·长剑`(金) `SalvageAllowed=False`、`UIWouldShowLocked=True`，`goldPresent=True redPresent=True` | 同上 `verify` 行 |
| 保存 | `SaveProgress=True`，`b1-persisted-save.json` = 17727 字节 | `PLAYER_RUN_MATRIX.csv` F8 |
| 用户原档 | SHA `dfff9c4f633656740fc252555f9215e124e52e2f1c225ebf6de032cc05e59003` 运行前后未变 | `FINAL_AUDIT.md §E` |

**推论 [E][D]**：v9 旧档可完整读入金/红装备，B1 的新门禁是**运行时计算**（`SalvageAllowed` 按 `quality`），不依赖任何新增存档字段 → 证明「纯计算/纯视图」类功能可在不触碰 Schema 的前提下实现。B2 沿此模式设计。

---

## 5. 保护域核对（本轮零变化）[S]

| 项 | 状态 |
|---|---|
| v9 / v10 / v11 Schema | 未修改；v10/v11 不存在 |
| `CombatSaveEnvelope.version` | 未修改 |
| 版本白名单 `1..9` | 未修改 |
| `GearItem` 字段集合（19） | 未修改 |
| `CombatSaveData` / `CombatCheckpoint` 字段 | 未修改 |
| `AdventureValidation` / `CombatSaveSystem.Validate*` | 未修改 |
| `CampRuntime.Capacity=200` / `MaterialLimit` | 未修改 |
| `AdventureItems.Sizes` / `Power` / `attackFactor` | 未修改 |
| 掉落率 / 随机流 / 制造成本 / 攻击力公式 | 未修改 |
| `ProjectSettings` | 未修改 |
| 用户存档 | 未读取写入（本轮仅做源码审计） |

---

## 6. 待验证假设 [H]

1. `JsonUtility.FromJson` 忽略未知键的行为基于 Unity 常规语义，本轮**未**做跨构建读档 Player 验证。
2. 新增字段后旧构建是否仍能通过 `checksum` 校验，需实际双构建回归；当前结论为源码级推论。
3. `GroundLootStore.Pack/Unpack`（`:87,235`）对新增字段的分页往返行为未验证。
4. B2 若实施「批量存取」，多次 `SaveProgress` 对 `revision` 递增与 `Flow.Published` 的影响未验证。
