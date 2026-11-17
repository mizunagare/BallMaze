# UX-04-B2 · 未来实施批次的真实 Player 验收计划

> 标记：**[S]** 源码事实（含 file:line）· **[E]** Player 证据（本轮**未**产生，引用 B1 既有证据）· **[C]** 计算结果 · **[D]** 设计推论 · **[H]** 未验证假设
> **重要 [H]**：B2 是**只读审计轮**，本轮**未执行任何 Player 运行**、未启动 Unity、未注入驱动。本文件是**未来实施批次应执行的验收计划**，不是本轮结果。不得把下列计划当作已通过的证据。

---

## 1. 验收纪律（沿用 B1 已验证范式）[E][D]

| 约束 | B1 已验证做法 | B2 继承 |
|---|---|---|
| 真实 Player 输入 | `InputSystem.QueueStateEvent` 注入 `MouseState` down/up，按 `gameObject.name` 定位 uGUI `Button` 屏幕中心（`DeliveryUxProgression04B1/Tools/IntDriverB1.cs`） | 必须沿用，**禁止直接调用** `SelectMain` / `Salvage` / `DepositEquipment` 等底层方法伪造验收 |
| 隔离构建 | 复制 Acceptance 构建到 `Builds/ux04b1/player/`，sidecar 驱动 DLL 只注入副本，原构建保持纯净 | 未来批次须新建独立副本目录，不复用 B1 副本 |
| 独立存储根 | `-wanxiang-storage-root` 隔离用户存档 | 同上；用户真实存档零变化 |
| 证据归档 | `EVIDENCE/INDEX.json` 记录每文件 SHA256；28 文件 28/28 自洽 | 每批次独立 `INDEX.json`，失败证据**照实保留** |
| 全量 SHA 校验 | `PROTECTION_SHA256.tsv`（B1 补齐至 31 项） | 实施批次需重新生成并复核 |

B1 真实证据基线 [E]：`UX04-B1-DISMANTLE-01` / `UX04-B1-READBACK-01`，2 运行 / 2 PASS / 28 文件；`AttackPower=33`、v9 读档 10 件、金/红 `SalvageAllowed=False`；白/绿/紫真实分解、金/红拒绝不消耗、金入库再取回。

---

## 2. 验收环境前置条件 [D][H]

1. 负责人批准实施范围（见 `DECISIONS_REQUIRED.md`），并创建独立实施分支 [D]。
2. 确认基线 `95caf234…` 与 `feature/ux-progression-04` 一致，未覆盖 B1 / UX-03 成果 [S]。
3. 构建 Unity 6000.6.5f1 Player；确认 `CatInventoryPresenter.Running=True` 与 `InCamp=True` 可达（B1 `boot/entry` 观测已验证该默认态）[E][H]。
4. sidecar 驱动以 `csc.dll -deterministic` 编译，注册到 `RuntimeInitializeOnLoads.json` + `ScriptingAssemblies.json`（仅副本）[E][D]。

---

## 3. 验收矩阵（未来实施批次执行）[D][H]

> 全部为**待执行项**，标记 [H]。「预期」列来自源码事实 [S] 或计算 [C]，不是已观测结果。

| ID | 场景 | 真实 Player 操作 | 预期（源码/计算依据） | 关键不变量 | 标记 |
|---|---|---|---|---|---|
| P-01 | 五品质筛选 | 点击品质筛选「红」→ 观察列表 | 仅 `quality==Red` 装备可见；`GearQuality 0..4` | 物品数量/属性/位置不变 | [S][D][H] |
| P-02 | 类型筛选 | 点「武器」/「护臂」切换 | `i.Weapon` / `type==Arms` 分组正确；两 UI 路径结果一致（消除 filter 索引冲突） | IMGUI/uGUI 语义一致 | [S][D][H] |
| P-03 | 攻击力排序 | 点「攻击力↓」 | 按 `item.Attack` 降序；红剑 132 > 红饰品 66 > 红护臂 46.2 | 排序不改变 `AttackPower` | [C][H] |
| P-04 | 来源筛选 | 点「来源=本局战利品」 | 按 `origin==RunLoot` 过滤；`SourceLabel` 两路径均显示 | `origin/originRunId` 不被改写 | [S][D][H] |
| P-05 | 跨仓库检索 | 范围选「全部」→ 搜索仓库内金装备 | 仓库项以只读行出现并标注「仓库」；**不可拖放** | 不触发任何存取/存档写入 | [D][H] |
| P-06 | 对比-主武器 | 选中红剑 → 预览「设为主武器」 | `AttackPower 33 → 157`，Δ+124；`BasicPower` 同步 | 未点确认前 `items` 零变化 | [C][H] |
| P-07 | 对比-备用武器 | 同一红剑 → 预览「设为备用」 | **Δ=0**（`Active` 不含 Reserve） | 验证「备用贡献 0」，防朴素差值错误 | [S][C][H] |
| P-08 | 对比-饰品/护臂 | 红饰品放盘 / 红护臂放盘 | 分别按 `×0.5` / `×0.35` 计入 `Active.Sum` | 不使用简单差值 | [S][C][H] |
| P-09 | 对比-容器加成 | 预览更换 `bag_relic` | `Attack` Δ+6（容器 `attackBonus`），物品 `Attack=0` | 容器加成不能被漏算 | [S][C][H] |
| P-10 | 对比-长枪倍率 | 主武器 白长枪↔白长剑（同 `Attack=8`） | `AttackPower` Δ=0，`BasicPower` 由 41.25→33（Δ−8.25） | `SpearPower=1.25` 只影响普攻 | [S][C][H] |
| P-11 | 会话内收藏 | 点 ★ → 「仅看收藏」 | 仅收藏项可见；移动/穿戴/存取/分解行为不变；重启后清空 | 零存档写入 | [D][H] |
| P-12 | 金/红不可分解 | 金/红 → 拆解按钮 | 按钮禁用 + 「不可分解 · 可入库」；B1 门禁拒绝 | 装备数/材料数不变（B1 已验证 [E]） | [S][E][H] |
| P-13 | 金/红入库取回 | 金装备 → 存入仓库 → 取回 | `Deposit/Withdraw` 不查品质；`Clone()` 保属性 | 属性/词缀/id 不变（B1 已验证 [E]） | [S][E][H] |
| P-14 | 仓满反馈 | 仓库至 200 后再存入 | 明确「永久仓库已满（200/200）…装备未移动」文案 | 不修改 `Capacity=200` | [S][D][H] |
| P-15 | 容量展示一致 | 打开两路径营地页 | 均显示 `CampRuntime.Capacity`（消除 uGUI 硬编码 `/200`） | 文案一致 | [S][D][H] |
| P-16 | 批量存取 | 多选 → 批量存入/取回 | 逐件走现有 API + `Commit` 原子提交；失败逐件回报「未重复转移」 | 无物品丢失/重复 | [S][D][H] |
| P-17 | 重复件识别 | 同名同属性多件 | 列表显示「×N」；`dupKey` 不含位置/来源态 | `id` 仍唯一 | [S][D][H] |
| P-18 | 整理对等 | 两路径分别点「整理背包/整理仓库」 | 均可用；形状不兼容时保留原布局（`PreviewSortBag`） | 不丢物 | [S][D][H] |
| P-19 | 分解确认对等 | IMGUI/uGUI 分别点拆解 | 两路径均需二次确认 | 未确认不消耗 | [S][D][H] |
| P-20 | 热键回归 | Tab/B/C/E/H/V/Q/R/F1/F5/F9 | 全部保持 `PlayerBindings.cs` 定义；`R` 双语义不变 | 无新增绑定 | [S][H] |
| P-21 | 拾取穿戴回归 | `E` 拾取地面装备 → 设主武器 → 入盘 | `PickUp → Add → SelectMain → Place` 链路不变 | 拾取失败时掉落物保留 | [S][H] |
| P-22 | v9 读档兼容 | 载入 B1 种子 v9 档 | 10 件装备、金/红可读且锁定，`AttackPower=33` | 与 B1 READBACK 一致 | [E][H] |
| P-23 | 存档零变化 | 全程记录 `payload` 结构 / version / 校验 | version=9、字段集合 19、白名单 1..9 未变 | 用户真实存档 SHA 不变 | [S][E][H] |
| P-24 | 保护域 SHA | 复核 31 项保护清单 | 仅批准文件变更；攻击/掉落/随机/成本/Schema/Boss 零变化 | 与 B1 `PROTECTION_SHA256.tsv` 口径一致 | [S][E][H] |

---

## 4. 快照字段建议（沿用 B1 驱动）[E][D]

B1 `Snapshot()` 已输出：`Inventory_count / Inventory / EquipmentGrid / Main / Reserve / Worn / Overflow / ItemQuality / ItemPower / AttackPower / SavedAttack / MaterialCount / WarehouseCount / GearAttack`。未来批次建议补充：

`FilterSpec_active / VisibleCount / SelectedId / ComparisonRole / DeltaAttackPower / DeltaBasicPower / FavoritesCount / WarehouseCapacity / SaveVersion / SchemaFieldCount`。[D]

---

## 5. 判定规则 [D]

- 每条 P-xx 必须通过**真实输入事件日志**（`button-found` / `mouse-down` / `mouse-up`）证明操作来自 Player，而非直接调用底层方法。
- 失败项**照实保留**（不删除、不重跑覆盖），在 `INDEX.json` 中标记 `result=FAIL` 并附原始日志。
- 每个实施批次独立运行、独立 SHA 校验、独立暂停待审，与用户既定节奏一致 [E][D]。
- **`AttackPower` 相关断言（P-06~P-10）必须以运行时 `hero.AttackPower` 读回值核对**，不得只比对纸面公式 [C][H]。

---

## 6. 本轮未执行声明 [H]

本轮（UX-04-B2）为只读审计：**未启动 Unity Player、未注入 sidecar 驱动、未产生任何新的 `Evidence/Runs*` 运行、未生成 `INDEX.json`、未做 SHA 校验批次**。上述全部为计划。引用 B1 证据仅用于说明既有事实与可复用范式，不构成 B2 验收结论。
