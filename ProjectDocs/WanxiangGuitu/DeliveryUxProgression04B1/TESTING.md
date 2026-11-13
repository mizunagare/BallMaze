# UX-04-B1 测试方法论与核验

## 一、构建与运行链

| 阶段 | 工具 | 产物 |
|---|---|---|
| 1. 隔离副本 | 复制 `Builds/WanxiangGuitu.Acceptance` → `Builds/ux04b1/player/`（gitignored） | 隔离运行环境 |
| 2. 驱动编译 | `Tools/build_driver_b1.py` 用 `csc.dll -deterministic` 编译 `IntDriverB1.cs` | `B1ObservationDriver.dll`（确定性哈希 `79e773e4…`） |
| 3. 注入 | 写入 `RuntimeInitializeOnLoads.json` + `ScriptingAssemblies.json` | 驱动仅在副本启动 |
| 4. 启动 | `Tools/run_b1_player.py` 以 `-wanxiang-storage-root` 隔离存储 + `--seed-save`（读档模式） | 真实 Player 运行 |
| 5. 归档 | 收集 `Player.log`、`b1-observations.jsonl`、`b1-input-events.jsonl` 等 | `EVIDENCE/INDEX.json` 28 文件 |

> 关键约束：驱动 DLL **只进隔离副本**；原 Acceptance 构建 `ScriptingAssemblies.json` 未注入 `B1ObservationDriver` → 正式包零污染。

## 二、确定性编译

- 使用 Roslyn `csc.dll -deterministic`，保证同一源码产出同一 SHA256，便于复现与审计。
- 构建指纹：
  - Acceptance 构建 EXE：`b70442f9…`
  - Acceptance 构建 DLL：`1dd1b676…`
  - B1 驱动 DLL：`79e773e4…`

## 三、保护域核验（禁止改动项）

### 3.1 原则
B1 仅允许在「分解门禁 + 按钮禁用」层面做最小改动，**严禁**触碰：攻击力聚合数学、武器伤害、掉落率、宝箱概率、随机流、制造成本、装备尺寸、v9/v10/v11 Schema、Boss 规则、P1/P1C 已接受挑战逻辑，且 UX-03 产品功能与验收证据不得被覆盖。

### 3.2 核验方式
- `git diff --quiet HEAD` 判定 `Assets/` 下文件是否实际变更（规避 CRLF/LF 归一化导致的字节级伪差异）。
- 仅 3 个文件 `changed_vs_head = YES`：`AdventureLoadout.cs`、`CatInventoryPresenter.cs`、`ContainerInventoryView.cs`（均为 B1 批准项）。
- 其余 21 项 `NO`，见 `PROTECTION_SHA256.tsv`。

### 3.3 保护域清单（节选关键项）

| 文件 | 保护域 | 是否变更 |
|---|---|---|
| `AdventureCombat.cs` / `GreatswordCombat.cs` / `NewWeaponCombat.cs` / `ScytheCombat.cs` | 武器伤害 / 普攻 | NO |
| `AdventureLoadout.cs` | 攻击力聚合（仅 Salvage 门禁） | YES（B1 批准） |
| `CombatSaveSystem.cs` / `CombatSaveData.cs` | 存档 Schema / 读档 | NO |
| `AdventureItems.cs` | 品质数值 / 装备尺寸 / 物品定义 | NO |
| `CampRuntime.cs` | 永久仓库 / 存取 | NO |
| `PlayerInventory.cs` | 背包 / 材料 | NO |
| `CraftingRecipeDefinition.cs` | 制造成本 / 配方 | NO |
| `WeaponTraits.cs` | 词缀 / 随机流 | NO |
| `AdventureFlow.cs` / `CombatSession.cs` | 出征/Boss / 战斗挑战循环 | NO |
| `CatInventoryPresenter.cs` / `ContainerInventoryView.cs` | 库存 UI（仅分解按钮） | YES（B1 批准） |

### 3.4 用户资产保护
- 用户真实存档 SHA256：`dfff9c4f…`，运行前后一致 → **未变更**。
- 隔离存储根确保即便异常也不会写回用户存档。

## 四、失败保留策略

- 本批次 2 次运行（DISMANTLE / READBACK）均 PASS，**无失败运行**。
- 若运行失败，按规「原样保留」全部产物（含 `Player.log`、`b1-observations.jsonl`），不删除、不改写，并在 `EVIDENCE/INDEX.json.failedRunsPreserved` 登记。

## 五、可复现性

- 重跑命令（在 `DeliveryUxProgression04B1/Tools/` 下）：
  1. `python build_driver_b1.py` → 生成驱动 DLL
  2. `python run_b1_player.py` → 执行 dismantle 与 readback 两轮真实 Player 运行
- 两轮退出码均为 0；`EVIDENCE/INDEX.json` 内 28 文件 SHA256 自洽（28/28 一致）。
