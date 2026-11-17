# UX-04-B2：装备收藏与库存管理 · 正式实施报告

> 标记：**[S]** 源码事实 · **[E]** Player 证据 · **[C]** 计算结果 · **[D]** 设计推论 · **[H]** 未验证假设
> 结论：**B2-01 ~ B2-05 全部实施完成；真实 Player 验收 6/6 PASS；保护审计通过。已暂停等待复审。**

## 0. 授权与基线 [S]

| 项 | 值 |
|---|---|
| D-01 | 批准 P0 + P1 |
| D-02 | 批准等价重构及 `AdventureLoadout` 只读攻击力计算接口 |
| D-24 | 保持现有攻击力叠加规则 |
| D-16 | 保持 B1 金红装备不可分解 |
| 品质 | 白 / 绿 / 紫 / 金 / 红 |
| 仓库容量 | 200，不修改 |
| 收藏 | 仅会话内，不持久化 |
| 基线 Commit | `95caf234256613d4a6e4f89a8ab0dc09c397c6b2` |
| 远端核对 | `feature/ux-progression-04` = `95caf234…`（一致） |
| 工作分支 | `feature/ux-progression-04-b2`（新建，未推送） |
| main | `72db192a…`（未变化）；B1 成果完整保留 |

## 1. 实施结果总览 [S][E]

| 批次 | 内容 | 结果 |
|---|---|---|
| **B2-01** | 统一只读攻击力计算；`Attack`/`Defense` 等价重构委托同一纯函数；`PreviewReplacement` 只读模拟替换；黄金矩阵逐位对照 | PASS |
| **B2-02** | 统一语义筛选（8 页签 / 五品质 / 主备 / 已穿戴 / 仓库 / 未使用 / 攻击·品质·类型排序 / 来源仅 origin+originRunId）；IMGUI 与 uGUI 共用同一规则 | PASS |
| **B2-03** | 装备比较基于统一接口，展示当前/替换后 AttackPower、实际变化、装备自身 Attack、主副武器贡献、饰品护臂贡献；覆盖备用/饰品/护臂/长枪/Overflow/Worn/容器加成 | PASS |
| **B2-04** | 会话内 `HashSet<string>` 收藏；单点禁分解；批量整理保护；可取消收藏；正常存取穿戴不受影响；重启清空；重复件只提示；破坏性操作二次确认 | PASS |
| **B2-05** | 容量 200 不变；明确区分背包 96 格 / 装备盘 48 格 / 仓库 200 件；仓满明确原因；两 UI 同一业务逻辑；热键与布局保护 | PASS |

## 2. 产品源码变更 [S]

**新增 3 个文件**：`B2AttackModel.cs`、`B2InventoryQuery.cs`、`B2Collection.cs`
**修改 5 个文件**：`AdventureLoadout.cs`、`ContainerInventoryView.cs`、`CatInventoryPresenter.cs`、`CampRuntime.cs`、`CampInventoryView.cs`

`git diff HEAD --stat` = 5 files, **+110 / −34**；`git diff --check HEAD` 干净；暂存区为空。[S]

## 3. 构建与验收 [E]

| 项 | 值 |
|---|---|
| 产品 DLL | `875cfea8…`（868864 B），全源码确定性重编译，**0 error** |
| 最终 sidecar 驱动 DLL | `b7a46b0a…`（58368 B），**0 error** |
| buildId | `ux04b2-875cfea8-b70442f9-b7a46b0a` |
| 最终 Run | 6 次，全部 `PLAYER_RUN_COMPLETED` / `PASS` / exit 0 / 0 错误观测 |
| 证据 | `EVIDENCE/INDEX.json`：80 个文件，SHA256 自洽 80/80 |
| 矩阵 | `PLAYER_RUN_MATRIX.csv`：41 行，0 FAIL |

### 关键 Player 证据 [E]

- **逐位等价**：24 行 `legacyBits == unifiedBits`，`G0 liveMatch=True`；实时 `AttackPower=33`（25+8+0）与 B1 读档一致。
- **七武器/系数**：长枪 `BasicPower 85 = 68×1.25`；饰品 `132×0.5=66`；护臂 `132×0.35=46.2`；红剑主武器 `33→157 (Δ+124)`。
- **备用武器贡献 0**：`reserveAP=33→33`，`reserveDelta=0`，而主武器替换 `mainDelta=124`。
- **只读预览**：`G7-preview readOnly=True`（装备数/主武器未变）。
- **两 UI 筛选**：uGUI（真实 InputSystem 点击）与 IMGUI（原生 OS 鼠标）各 8/8 页签状态正确，共用同一 `SpecForTab`/`Matches`。
- **收藏/分解**：收藏后 `canQuickDismantle=False stillOwned=True ore=0`；取消收藏后两段式确认 `consumed=True ore=1`。
- **B1 不回退**：金/红 `allowed=False stillOwned=True`；金装备入库 `0→1`、取回 `1→0`。
- **仓满**：`200→200 stillOwned=True`，明确文案「永久仓库已满（200/200 件）：请先取回或整理，装备未移动。」
- **重启清空**：进程 A 种下 3 件收藏（token A）→ 全新进程 B `collectionCount=0`、token 不同、`noneFavourite=True`。
- **v9 读档**：`goldPresent/redPresent/goldLocked/redLocked/collectionEmpty=True`，`SaveProgress=True version=9`。

### 真实输入机制 [S][E]

所有被测动作均由真实鼠标事件触发，**未直接调用底层方法伪造验收**。uGUI 用 `InputSystem.QueueStateEvent` 驱动 `EventSystem`；IMGUI 用 `user32.dll` 原生 `SetCursorPos`+`mouse_event` 驱动 `Event.current`（InputSystem 合成事件不到达 IMGUI，此发现已如实记录）。样本装备与仓满状态通过产品自身工厂/`Restore` 准备（准备 ≠ 被测动作）。

## 4. 失败记录（照实保留，不覆盖）[E]

| Run | 结果 | 说明 |
|---|---|---|
| `UX04-B2-UGUI-01` | **FAIL** (exit 3) | 驱动误选 `Carried` 起始主武器作分解目标；产品正确拒绝。驱动已修正，但失败运行、原始日志、`b2-failure.txt` 与当时驱动 SHA 全部原样保留；以新 ID 重跑 |
| `IMGUI-01/02/03` | 不确定诊断 | InputSystem 点击已投递但未改变 IMGUI 状态；如实标记 `supersededDiagnosticRuns`，由 `IMGUI-04`/`IMGUI-FINAL` 原生注入取代 |

全部 18 个运行目录均未删除、未覆写。[E]

## 5. 保护审计 [S]

`PROTECTION_SHA256.tsv`：**41 个保护域**，`NEW=3`（B2 新增）、`YES=5`（B2 批准修改）、`NO=33`（全部未改动）。

| 保护项 | 状态 |
|---|---|
| v9/v10/v11 Schema、校验器、存档写入 | 未改 |
| 攻击力实际计算系数 / D-24 | 未改（逐位等价） |
| 掉落率 / 宝箱概率 / 随机流 / 制造成本 / 装备尺寸 | 未改 |
| Boss 规则 / P1-P1C 挑战逻辑 / UX-03 成果 | 未改，未回退 |
| `ProjectSettings` / `Packages` / 场景 / Prefab | `git status` 为空 |
| 全部 `PlayerAction` 与热键 | 未改 |
| 仓库容量 200 / 容器结构 | 未改 |
| 用户真实存档 | 从未写入（每 Run 独立 `-wanxiang-storage-root`） |

**构建方式说明** [D]：为遵守「禁止修改 ProjectSettings」，未运行 Unity batchmode 构建链（该链会写 scripting define symbols），改用 Unity Bee `.rsp` 做全源码确定性 Roslyn 重编译，并仅把 DLL 写入 gitignored 隔离副本。原始 Acceptance 构建 DLL 仍为 `1dd1b676…` 未变。

## 6. 交付清单（12 份）[S]

| # | 文件 |
|---|---|
| 1 | `REPORT.md`（本报告） |
| 2 | `ACCEPTANCE.md` |
| 3 | `TESTING.md` |
| 4 | `ATTACK_POWER_MODEL.md` |
| 5 | `INVENTORY_FILTERS.md` |
| 6 | `EQUIPMENT_COMPARISON.md` |
| 7 | `COLLECTION_RULES.md` |
| 8 | `STORAGE_RULES.md` |
| 9 | `PLAYER_RUN_MATRIX.csv` |
| 10 | `EVIDENCE/INDEX.json` |
| 11 | `PROTECTION_SHA256.tsv` |
| 12 | `RISK_REGISTER.md` |

（另附 `Tools/` 下 4 个可复现工具：`build_b2_product.py`、`IntDriverB2.cs`、`build_driver_b2.py`、`run_b2_player.py`；实施前只读审计阶段的 8 份文档已归档于 `PreImplementationAudit/` 保留，另 3 份同名文档 `REPORT.md`/`EQUIPMENT_COMPARISON.md`/`RISK_REGISTER.md` 已用正式实施版覆盖。）

## 7. 遗留假设 [H]

1280×720/D3D12 单一窗口验证；仓满为准备阶段预置；批量整理未做故障注入；`Board` 预览假设放置成功；未跑 Unity `BuildPlayer` 二进制对照；未穷举全部 affix/容器组合。详见 `RISK_REGISTER.md` H-01~H-07。

## 8. 停止条件与纪律 [S]

- ✅ 完成 B2-01 ~ B2-05
- ✅ 完成真实 Player 验收（6/6 PASS）与保护审计（41 域）
- ✅ **未自动提交**：`git diff --cached` 为空，HEAD 仍为 `95caf234…`
- ✅ **未推送**：远端不存在 `feature/ux-progression-04-b2`
- ✅ **未合并 main**：main `72db192a…` 未变
- ✅ **未启动 UX-05**
- ✅ 新分支 `feature/ux-progression-04-b2` 已创建但未提交任何内容
- ✅ 工作区另有 Unity 生成的 `Assets/Resources.meta`（untracked，非 B2 改动）与历史 Evidence 目录，均未纳入变更

**已完成并暂停，等待负责人复审。**
