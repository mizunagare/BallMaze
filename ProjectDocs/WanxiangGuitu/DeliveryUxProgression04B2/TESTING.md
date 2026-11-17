# UX-04-B2 · TESTING（构建、验证与保护审计）

> 标记：**[S]** 源码事实 · **[E]** Player 证据 · **[C]** 计算结果 · **[D]** 设计推论 · **[H]** 未验证假设

## 1. 基线与分支 [S]

| 项 | 值 |
|---|---|
| 基线 Commit | `95caf234256613d4a6e4f89a8ab0dc09c397c6b2` |
| 远端 `feature/ux-progression-04` | 推送前核对 = `95caf234…`（一致） |
| 独立工作分支 | `feature/ux-progression-04-b2`（新建，未推送） |
| main | `72db192a527bd256e2ba18cd7ab334d8334051da`（未变化） |
| B1 成果 | 完整保留（`feature/ux-progression-04` 未修改） |

## 2. 产品源码变更范围 [S]

| 文件 | 类型 | 内容 |
|---|---|---|
| `Assets/CombatPrototype/B2AttackModel.cs` | 新增 | B2-01 统一只读攻击力计算 |
| `Assets/CombatPrototype/B2InventoryQuery.cs` | 新增 | B2-02 语义筛选 / 来源 / 重复提示 / 容量文案 |
| `Assets/CombatPrototype/B2Collection.cs` | 新增 | B2-04 会话内收藏 |
| `Assets/CombatPrototype/AdventureLoadout.cs` | 修改 | D-02 等价重构 + 只读接口 + 收藏门禁 + 整理保护 |
| `Assets/CombatPrototype/ContainerInventoryView.cs` | 修改 | IMGUI 统一筛选/比较/收藏/二次确认/容量 |
| `Assets/CombatPrototype/CatInventoryPresenter.cs` | 修改 | uGUI 统一筛选/比较/收藏/容量 |
| `Assets/CombatPrototype/CampRuntime.cs` | 修改 | 仓满明确原因 + 整理保护 |
| `Assets/CombatPrototype/CampInventoryView.cs` | 修改 | 容量文案统一 |

`git diff HEAD --stat` = 5 files changed, 110 insertions(+), 34 deletions(-)，另 3 个新增未跟踪文件。`git diff --check HEAD` 干净（无尾随空白/冲突标记）。[S]

## 3. 编译验证 [S][E]

| 阶段 | 工具 | 结果 |
|---|---|---|
| 产品全源码重编译 | `Tools/build_b2_product.py`：Unity Bee `1900b0aE.dag/Assembly-CSharp.rsp`（148 defines + 补 `UX_ACCEPTANCE` = 149，336 refs，150 源）+ 3 个 B2 源，`csc.dll -nostdlib+ /deterministic` | **0 error**，仅既有 CS0618 弃用告警 |
| 产品 DLL | `Assembly-CSharp.dll` = `875cfea8…`，868864 bytes | 写入隔离副本 |
| sidecar 驱动编译 | `Tools/build_driver_b2.py`，16 个引用 DLL，`-deterministic` | **0 error**，2 个既有 CS0618 告警 |
| 最终驱动 DLL | `B2ObservationDriver.dll` = `b7a46b0a…`，58368 bytes | 仅注入副本 |
| 注入 | 副本 `RuntimeInitializeOnLoads.json` + `ScriptingAssemblies.json` | `DRIVER_INJECTED`，后续 `--replace` 仅替换 DLL，两个 json 的 SHA 前后相同 |

编译日志：`Evidence/Runs04B2/_build/receipt/b2-product-compile.log`、`b2-driver-compile-r4.log`；收据：`b2-product-build.json`、`b2-driver-injection-r4.json`。[S]

**构建产物隔离** [S]：原始 `Builds/WanxiangGuitu.Acceptance/.../Assembly-CSharp.dll` 仍为 `1dd1b676…` 未变；`Builds/ux04b2/` 已 gitignore。用户真实存档从未写入（每次 Run 使用全新 `-wanxiang-storage-root`）。

## 4. 等价性（黄金矩阵）验证方法 [S][E]

- 在 sidecar 内实现**逐字复刻的旧表达式** `LegacyAttack` / `LegacyDefense`（独立于产品代码，作为 oracle）。
- 对同一组真实运行时 `GearItem` 分别求 `LegacyAttack` 与 `B2AttackModel.ComputeAttack`。
- 用 `BitConverter.SingleToInt32Bits` 比较 IEEE-754 位模式（不是 `Mathf.Approximately`），`Defense` 同样比较。
- 共 24 个矩阵行 + `G0-live`（实时 `gear.Attack` 位模式）+ `G7-preview` + `G8-filter`。`GOLDEN-FINAL` 27 行观测，`bitsEqual/ bitsEqualDefense/ liveMatch` 全部 True，0 错误。[E]
- 覆盖：五品质主武器、七武器类型、饰品/护臂盘内、备用武器、InBag/Board/Overflow/Worn 四态、容器加成、长枪倍率、只读预览、共享筛选规则。[E]

## 5. 保护域全量审计 [S]

`PROTECTION_SHA256.tsv`：41 个保护域，逐文件记录 `baseline_sha256 / current_sha256 / git_blob_oid / size_bytes / changed_vs_head / b2_change_nature`。

| 分类 | 数量 | 说明 |
|---|---|---|
| `NEW` | 3 | 3 个 B2 新增源文件（B2 批准新增） |
| `YES` | 5 | 5 个 B2 批准修改文件 |
| `NO` | 33 | 全部保护域未改动 |

判定口径用 `git diff --quiet HEAD`（规避 `*.cs text` + `core.autocrlf=true` 的 CRLF/LF 伪差异）；未改文件的 `current_sha256` 取 HEAD blob 内容。[S][C]

| 保护项 | 结果 |
|---|---|
| v9/v10/v11 Schema（`CombatSaveData` / `CombatSaveSystem` / `AdventureValidation` / `AdventureState`） | 未改 |
| 攻击力系数（`AdventureItems` / `ItemDefinition` / `QualityData` / `AdventureCombat`） | 未改 |
| D-24 叠加规则 | 逐位等价 |
| 掉落率 / 宝箱概率 / 随机流（`AdventureRandom` / `WorldEventPoint` / `CrystalCavernBoss*`） | 未改 |
| 制造成本（`CraftingRecipeDefinition`） | 未改 |
| 装备尺寸（`AdventureItems.Sizes` / `ContainerDefinition`） | 未改 |
| Boss 规则 / P1-P1C 挑战逻辑（`AdventureFlow` / `AdventureRules` / `Route*` / `*Layout`） | 未改 |
| `ProjectSettings` / `Packages` / 场景 / Prefab | `git status` 为空 |
| `PlayerBindings.cs` / `PlayerInput.cs`（全部热键） | 未改 |
| UX-03 已完成内容 | 未回退 |

## 6. 失败与中间运行的处理 [E]

- `UX04-B2-UGUI-01`（FAIL，exit 3）**原样保留**，含 `b2-failure.txt`、原始观测/输入/日志及当时的驱动 DLL SHA。原因：驱动误选 `Carried` 起始主武器作为分解目标；产品行为正确。修正驱动后以新 Run ID 重跑，未覆盖任何失败证据。
- `IMGUI-01/02/03` 曾以 InputSystem 驱动 IMGUI，点击投递但 `Event.current` 未消费；如实标记为「不确定诊断运行」，保留并由原生 OS 注入取代。
- 所有中间 PASS 运行也原样保留，在 `EVIDENCE/INDEX.json.supersededDiagnosticRuns` 中说明。
- 全部 18 个运行目录均未删除、未覆写。[E]

## 7. 终检命令结果 [S]

| 命令 | 结果 |
|---|---|
| `git branch --show-current` | `feature/ux-progression-04-b2` |
| `git rev-parse HEAD` | `95caf234…`（基线未变，未提交） |
| `git status --porcelain=v2 --untracked-files=no` | 仅 5 个 B2 批准的 `.M` |
| `git diff HEAD --stat` | 5 files, +110/−34 |
| `git diff --check HEAD` | 干净 |
| `git diff --cached --stat` | 空（**未暂存**） |
| `git status --porcelain=v2 -- ProjectSettings Packages *.unity *.prefab` | 空 |
| `git ls-remote origin refs/heads/feature/ux-progression-04-b2` | 不存在（**未推送**） |

## 8. 待验证假设 [H]

1. 全源码重编译使用 Unity 生成的 `.rsp`（149 defines / 336 refs）与 `-define:UX_ACCEPTANCE`，与 Unity batchmode 的 Bee 构建等价；未额外跑一次 Unity `BuildPlayer` 做二进制对照（该动作会写 ProjectSettings，故未执行）。
2. 未运行 Unity Test Framework 单元测试；等价性与功能以真实 Player 运行时断言为证。
3. 未在 macOS/Linux 或非 D3D12 后端验证。
