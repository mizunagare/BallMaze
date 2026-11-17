# UX-04-B2 · ACCEPTANCE（真实 Player 验收）

> 标记：**[S]** 源码事实 · **[E]** Player 证据 · **[C]** 计算结果 · **[D]** 设计推论 · **[H]** 未验证假设
> 完整机器可读索引：`EVIDENCE/INDEX.json`；逐项矩阵：`PLAYER_RUN_MATRIX.csv`（41 行，0 FAIL）

## 1. 验收基础设施（沿用 B1）[S]

| 组成 | 实现 |
|---|---|
| 产品构建 | `Tools/build_b2_product.py`：以 Unity Bee 的 `Assembly-CSharp.rsp`（150 源 / 336 引用）为基础，补 `UX_ACCEPTANCE` define + 3 个 B2 源文件，确定性 Roslyn 全源码重编译；**仅**把 DLL 写入隔离副本 `Builds/ux04b2/player/`（gitignored） |
| sidecar 驱动 | `Tools/build_driver_b2.py` 编译 `IntDriverB2.cs` → `B2ObservationDriver.dll`，仅注入副本的 `ScriptingAssemblies.json` / `RuntimeInitializeOnLoads.json` |
| 启动器 | `Tools/run_b2_player.py`：每个 Run 全新隔离存储根（`-wanxiang-storage-root`）、`-force-d3d12`、记录 exe/DLL/driver SHA、buildId、PID、起止 UTC、退出码、超时与原始日志 |
| 身份 | 产品 DLL `875cfea8…`；最终驱动 DLL `b7a46b0a…`；`buildId = ux04b2-875cfea8-b70442f9-b7a46b0a`；Unity 6000.6.5f1 |

**为何不走 Unity batchmode** [D]：该链会 `SetScriptingDefineSymbolsForGroup` 写 `ProjectSettings.asset`；B2 明确保护 ProjectSettings。全源码 Roslyn 重编译不触碰 ProjectSettings / Packages / 场景 / Prefab。

**原始事件** [S]：每次真实输入都写入 `b2-input-events.jsonl`（`button-found / mouse-down / mouse-up / native-mouse-down / native-mouse-up / button-disabled / button-missing`），状态写入 `b2-observations.jsonl`；`Player.log` / `Player.stdout` / `Player.stderr` / `entry-audit.jsonl` / `isolated-save/` 全部归档。

## 2. 最终 6 次 Run（同一构建身份）[E]

| Run ID | mode | PID | exit | verdict | 覆盖 |
|---|---|---|---|---|---|
| `UX04-B2-GOLDEN-FINAL` | golden | 51092 | 0 | PASS | 攻击力黄金矩阵 27 行观测 |
| `UX04-B2-UGUI-FINAL` | ugui | 39432 | 0 | PASS | uGUI 筛选/比较/收藏/分解/存取/仓满/v9 |
| `UX04-B2-IMGUI-FINAL` | imgui | 47820 | 0 | PASS | IMGUI 8 页签 + 3 循环 + 共享规则 |
| `UX04-B2-FAVSEED-FINAL` | favseed | 51788 | 0 | PASS | 进程 A 种下 3 件收藏并记录 token |
| `UX04-B2-RESTART-FINAL` | restart | 50736 | 0 | PASS | 全新进程 B 验证收藏清空 |
| `UX04-B2-READBACK-FINAL` | readback | 47096 | 0 | PASS | 播种 v9 存档 → `Continue()` 读回 |

6/6 `PLAYER_RUN_COMPLETED`、`b2-complete.txt=PASS`、0 错误观测、80 个证据文件 SHA256 100% 自洽。[E]

## 3. 需求逐项覆盖 [E]

| # | 需求 | 证据 | 结果 |
|---|---|---|---|
| 1 | 攻击力黄金矩阵 | `GOLDEN-FINAL`：24 行 `bitsEqual=True`，`G0 liveMatch=True` | PASS |
| 2 | 逐位对照旧结果 | `legacyBits == unifiedBits`（含 Defense 位模式） | PASS |
| 3 | IMGUI 筛选 | `IMGUI-FINAL`：原生 OS 点击 8 页签，`sharedTab 0..7` | PASS |
| 4 | uGUI 筛选 | `UGUI-FINAL`：真实 InputSystem 点击 8 页签，`sharedTab 0..7` | PASS |
| 5 | 装备比较 | `UGUI-FINAL`：真实点击「对比角色↻」×8，逐角色记录 AP/Δ/贡献 | PASS |
| 6 | 七武器及装备系数 | `GOLDEN-FINAL`：7 武器 + 饰品 0.5（66）+ 护臂 0.35（46.2）+ 长枪 1.25（85） | PASS |
| 7 | 收藏保护 | `uGUI-fav-add` / `uGUI-fav-blocked`：`canQuickDismantle=False stillOwned=True ore=0` | PASS |
| 8 | 收藏取消 | `uGUI-fav-remove`：`removed=True count=0`；随后二次确认分解成功 | PASS |
| 9 | 分解保护 | `uGUI-salvage-arm`（未消耗）→ `uGUI-salvage-confirm`（`consumed=True ore=1`） | PASS |
| 10 | 容器入库和取回 | `deposit-after` 0→1 / `withdraw-after` 1→0，`backInLoadout=True` | PASS |
| 11 | 仓库满载 | `warehouse-full-after`：200→200、`stillOwned=True`、明确原因文案 | PASS |
| 12 | v9 读档 | `READBACK-FINAL`：`goldPresent/redPresent/goldLocked/redLocked/collectionEmpty=True` | PASS |
| 13 | 进程重启后收藏清空 | `FAVSEED`(3 件, token A) → `RESTART`(0 件, token B, `noneFavourite=True`) | PASS |
| 14 | B1 金红门禁不回退 | `uGUI-B1-Gold/Red`：`allowed=False stillOwned=True` | PASS |
| 15 | 只读预览不改状态 | `G7-preview`：`readOnly=True` | PASS |
| 16 | 五品质 | `main-White/Green/Purple/Gold/Red` 全部逐位相等 | PASS |
| 17 | Overflow / Worn / 容器加成 | `state-Overflow`/`state-Worn`/`container-bonus` 全部覆盖 | PASS |

## 4. 真实输入机制（重要）[S][E]

- **uGUI**：`CatUI.Button` 生成 `UnityEngine.UI.Button`（`gameObject.name = label`）；驱动按名字定位、用 `RectTransformUtility.WorldToScreenPoint` 求屏幕中心，再通过 `InputSystem.QueueStateEvent` 投递 `MouseState` 的 down/up，由产品 `EventSystem` 消费。`UGUI-FINAL` 记录 8 组 `button-found + mouse-down + mouse-up`。[E]
- **IMGUI**：`CombatUI.Button` 用 `GUI.Button`，消费 `Event.current`（原生事件队列），`InputSystem.QueueStateEvent` **不会**到达它。驱动改为 `user32.dll` 的 `SetCursorPos` + `mouse_event` 生成真实 OS 鼠标事件，坐标按 `CombatUI.Scale` 与窗口客户区原点换算。`IMGUI-FINAL` 记录 11 组 `native-mouse-down/up` 且状态确实改变。[E]
- **禁止伪造验收** [S]：所有被测动作（筛选、比较角色循环、收藏、取消收藏、分解两步、入库、取回、仓满存入）均由真实鼠标事件触发；`AdventureLoadout.Salvage()` / `DepositEquipment()` 等底层方法**从未**被驱动直接调用来冒充动作。样本装备通过产品自己的 `AdventureItems.New` + `AdventureLoadout.Add` 准备（准备 ≠ 被测动作）；仓满状态通过产品自己的 `CampRuntime.Restore` 预置。

## 5. 失败记录保留（不覆盖）[E]

| Run | 结果 | 说明 |
|---|---|---|
| `UX04-B2-UGUI-01` | **PLAYER_RUN_FAILED** (exit 3) | 驱动误把「起始主武器（Carried）」选为分解目标；产品正确拒绝（B1 既有不变量）。该驱动缺陷已修正，但**失败运行、原始日志、`b2-failure.txt`、`run-manifest.json`（含当时的驱动 SHA `827877e4…`）全部原样保留**。修正后以新 ID `UGUI-02` / `UGUI-FINAL` 重跑。 |
| `IMGUI-01/02/03` | PLAYER_RUN_COMPLETED 但**不确定** | 用 InputSystem 尝试驱动 IMGUI，点击已投递但 `Event.current` 未消费，`sharedTab` 始终为 0。已作为「不确定诊断运行」记录在 `INDEX.json.supersededDiagnosticRuns`，**未删除、未改写**，由 `IMGUI-04` / `IMGUI-FINAL` 的原生注入取代。 |

其余中间运行（`GOLDEN-01/02`、`UGUI-02`、`READBACK-01`、`RESTART-01/02`、`FAVSEED-01`、`IMGUI-04`）均 PASS，因使用了中间驱动构建而被标记 superseded，但证据原样保留。[E]

## 6. 待验证假设 [H]

1. 验收窗口固定 1280×720 `-force-d3d12`；其他分辨率/DPI/图形后端未实测。
2. 仓满通过 `CampRuntime.Restore` 预置（准备阶段），非 200 次真实点击填满。
3. 未穷举所有 affix 组合与全部容器组合；等价性由共享表达式结构 + 24 行代表性矩阵共同支撑。
