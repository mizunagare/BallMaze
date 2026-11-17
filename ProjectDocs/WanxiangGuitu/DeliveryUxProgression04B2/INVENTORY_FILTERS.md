# UX-04-B2 · INVENTORY_FILTERS（B2-02 库存分类与筛选）

> 标记：**[S]** 源码事实 · **[E]** Player 证据 · **[C]** 计算结果 · **[D]** 设计推论 · **[H]** 未验证假设

## 1. 单一语义契约（消除整数 filter 分歧）

**实施前 [S]**：IMGUI `ContainerInventoryView.cs` 用 `static int filter`，`filter==1` 表示「非武器」；uGUI `CatInventoryPresenter.cs` 用实例 `int filter`，`filter==1` 表示「武器」。两条路径的整数语义**恰好相反**（见交付前审计 `UI_INTERACTION_SPEC.md`）。

**实施后 [S]**：
- 两条路径都读取**同一个** `B2FilterState.Current`（`B2FilterSpec` 语义对象）。
- 两条路径都渲染**同一张** `B2FilterTabs.Labels`（8 项），并通过**同一个** `B2FilterState.SpecForTab(int)` 把页签索引映射到语义。
- 两条路径的可见性判定都调用**同一个** `B2InventoryQuery.Matches(...)`。
- uGUI 保留的 `int filter` 已改为 `B2FilterState.Tab` 的**只读别名**，不再自行解释语义。
- IMGUI 中的 `filter=0` 已全部替换为 `B2FilterState.SetTab(0)`。

因此「两个界面各自维护不同的整数 filter 语义」已消除。[S]

## 2. 共享页签表与语义映射 [S]

`B2FilterTabs.Labels = { 全部, 武器, 饰品, 护臂, 品质, 状态, 排序, 收藏 }`

| 索引 | 标签 | `SpecForTab` 语义 |
|---|---|---|
| 0 | 全部 | `All / qualityMask=0 / All / None` |
| 1 | 武器 | `category=Weapon` |
| 2 | 饰品 | `category=Accessory` |
| 3 | 护臂 | `category=Arms` |
| 4 | 品质 | `qualityMask` 焦点到金/红（可循环切换五品质） |
| 5 | 状态 | `status=Unused`（可循环切换 8 种状态） |
| 6 | 排序 | `sort=AttackDesc`（可循环切换 7 种排序键） |
| 7 | 收藏 | `favoritesOnly=true` |

Player 证据 [E]：
- `UX04-B2-UGUI-FINAL`：真实 `InputSystem` 鼠标点击 8 个页签，`sharedTab` 依次 `0,1,2,3,4,5,6,7`，`spec` 与表中语义逐一吻合。
- `UX04-B2-IMGUI-FINAL`：原生 OS 鼠标点击 8 个页签，`sharedTab` 同样依次 `0..7`；三次循环按钮令 `FilterKey` 分别改变品质掩码、状态、排序键。
- `G8-filter`：共享语义表的 `weaponTabOK=True`，`filtered=4` 且 `allWeapon=True`，链的确定性 `chainDeterministic=True`。

## 3. 筛选维度 [S]

`B2FilterSpec` 字段：`category`、`qualityMask`（bit0..4 = 白/绿/紫/金/红，`0`=五品质全选）、`status`、`sort`、`favoritesOnly`、`text`。

| 需求 | 实现 | 标记 |
|---|---|---|
| 武器分类 | `B2Category.Weapon`（`GearItem.Weapon` = `(int)type<4 || NewWeaponRegistry.Is(type)`） | [S] |
| 饰品分类 | `B2Category.Accessory`（`type==GearType.Accessory`） | [S] |
| 护臂分类 | `B2Category.Arms`（`type==GearType.Arms`） | [S] |
| 五品质筛选 | `qualityMask` 位掩码 + `B2FilterState.CycleQuality()` 循环（全/白/绿/紫/金/红/金红） | [S] |
| 主武器状态 | `B2ItemStatus.Main`（`i.id == gear.mainWeapon`） | [S] |
| 备用武器状态 | `B2ItemStatus.Reserve`（`i.id == gear.reserveWeapon`） | [S] |
| 已穿戴状态 | `B2ItemStatus.Worn`（`i.worn`）；另有 `Board`/`Overflow`/`Warehouse`/`Unused` | [S] |
| 仓库状态 | `B2ItemStatus.Warehouse`（由来源集合 `warehouse` 标志判定，不改 `GearItem`） | [S] |
| 未使用状态 | `B2ItemStatus.Unused`（`InBag` 且非主/备/盘内） | [S] |
| 攻击力排序 | `B2SortKey.AttackDesc/AttackAsc`，键为 `GearItem.Attack` | [S] |
| 品质排序 | `QualityDesc/QualityAsc`，键为 `(int)quality` | [S] |
| 类型排序 | `TypeAsc`，键为 `(int)type` | [S] |
| 关键词检索 | `text` 对 `GearItem.Name` 做忽略大小写包含 | [S] |

`B2InventoryQuery.Apply` 是**纯投影**：返回新 `List<GearItem>`，不修改源集合、不合并/堆叠/删除任何物品。[S]

## 4. 来源展示：仅 `origin` + `originRunId` [S]

`B2InventoryQuery.SourceLabel(GearItem)` 只读 `GearItem.origin` 与 `GearItem.originRunId`：

| origin | 展示前缀 |
|---|---|
| `DeploymentProtected` | 入场保护 |
| `LegacyProtected` | 旧档保护 |
| `RunLoot` | 本局战利品 |
| `Unspecified` | 来源未标注 |

后缀为 `originRunId` 前 8 位。**未新增地区字段，未新增任何来源字段**；`AdventureState.cs` 的 `ItemOrigin`、`AdventureFlow.Supplies.cs` 的强校验 `i.originRunId==run.runId && i.origin==...` 全部零变化。[S]

IMGUI 原先调用 `AdventureFlow.SourceLabel(item)`（依赖局状态 `Protects`），已替换为 `B2InventoryQuery.SourceLabel(item)`；uGUI 原先不展示来源，现已展示同源标签。[S] Player 读档证据 [E]：`UX04-B2-READBACK-FINAL` 每件装备均输出 `source=...`，金/红可读。

## 5. 重复装备识别：只提示 [S]

`DuplicateKey` = `type | quality | definitionId | savedAttack | savedDefense | affixes(排序) | widthOverride | heightOverride`，**不含** `id`/坐标/`board`/`worn`/`overflow`/`origin`/`originRunId`。[S]

`DuplicateHints` 只返回计数；两条 UI 仅在详情文本追加「同类同属性 ×N（仅提示，不合并）」。**无自动合并、无删除、无任何写操作**。[S]

## 6. 两界面一致性（Player 证据）

| 检查 | IMGUI-FINAL | UGUI-FINAL | 标记 |
|---|---|---|---|
| 页签数 | 8 | 8 | [E] |
| 语义表 | `B2FilterTabs.Labels` | 同一张表 | [S] |
| 索引映射 | `SpecForTab` | 同一个 `SpecForTab` | [S] |
| 可见性判定 | `B2InventoryQuery.Matches` | 同一个 `Matches` | [S] |
| 真实输入 | 原生 OS `mouse_event`（IMGUI `Event.current`） | `InputSystem.QueueStateEvent`（uGUI `EventSystem`） | [E] |
| 结果 | 8/8 页签状态正确 | 8/8 页签状态正确 | [E] |

**输入机制说明 [S][E]**：`InputSystem.QueueStateEvent` 只进入 uGUI `EventSystem`，不会进入 IMGUI 的 `Event.current`；因此 IMGUI 验收改用 `user32.dll` 的 `SetCursorPos` + `mouse_event` 生成真实 OS 鼠标事件。`UX04-B2-IMGUI-01/02/03` 曾用 InputSystem 尝试，点击**虽已投递但未改变 IMGUI 状态**，已作为「不确定诊断运行」照实保留（`EVIDENCE/INDEX.json` 的 `supersededDiagnosticRuns`），并由 `IMGUI-04` / `IMGUI-FINAL` 的原生注入取代。

## 7. 未改动项 [S]

`PlayerBindings.cs`/`PlayerInput.cs`（19 个 `PlayerAction`、保留键、`R` 双语义）零变化；`Page` 枚举、页签行几何、面板尺寸、装备拾取/穿戴/移动路径零变化；未新增热键。[S]

## 8. 待验证假设 [H]

1. `B2FilterState` 是进程内静态单例，跨页面切换保持一致；进程重启后回到默认 spec（与收藏一致，符合「会话内」语义），本轮未专门做跨进程 spec 断言。
2. 排序键在并列时以 `id` 升序做稳定次序，未在 Player 中对全部并列组合做穷举验证。
3. IMGUI 原生注入坐标依赖 `CombatUI.Scale` 与窗口客户区原点；已在 1280×720 窗口验证，其他 DPI/缩放未实测。
