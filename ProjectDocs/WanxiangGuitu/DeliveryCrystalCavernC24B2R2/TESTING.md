# CP06-C24-B2-R2 复跑说明与证据边界

## 1. 环境与启动链

| 项 | 值 |
|---|---|
| Unity Editor | `6000.6.5f1` |
| .NET / Roslyn | `C:/Program Files/dotnet/dotnet.exe` + Unity `DotNetSdk/sdk/8.0.318/Roslyn/bincore/` |
| Python | `3.13.12` |
| **PowerShell** | 仅 Windows PowerShell 5.1，**无 `pwsh`（PowerShell 7）** |

本批**沿用 R1 的独立启动机制**，不依赖 `pwsh`：

| 步骤 | 工具 |
|---|---|
| 干净纯发行包 | 直接 `Unity.exe -batchmode -executeMethod WanxiangBuild.ValidateBuild`，`UNITY_TEST_ROOT` 由启动器设置 |
| sidecar 驱动编译 + 注入 | `Evidence/Tools/build_driver.py`（与 R1 版本逐字一致，SHA `846a44eb…`） |
| 观测 Player 启动 | `Evidence/Tools/run_player.py`（与 R1 版本逐字一致，SHA `9d7a160b…`） |
| 分析 | `Evidence/Tools/r2_analysis.py`、`finalize_evidence.py` |

`build_driver.py` / `run_player.py` 与 R1 的 SHA256 完全相同，仅驱动源码 `R2Driver.cs.txt` 为本批新增。
每个 Player run 使用全新 `-wanxiang-storage-root` 隔离根，记录 EXE SHA / Build SHA / 驱动 DLL SHA /
PID / runId / 命令行 / stdout / stderr / `Player.log` / 原生退出码。

## 2. 复跑顺序（严格，输出拒绝覆盖）

```bash
# 0) 基线与分支
git ls-remote --heads origin main fix/cp06-crystal-warden-b1 \
    fix/cp06-crystal-warden-b2 fix/cp06-crystal-warden-b2-r1
git checkout -b <fresh-r2> c388e9b7ecf9b5619a65fac81227eba68f61b832

# 1) 干净纯发行包（隔离工程不得含任何验证脚本）
UNITY_TEST_ROOT='I:\WGCombat\<fresh>\PureBuild1' \
"C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe" \
  -projectPath 'I:\WGCombat\<fresh>\Project' \
  -executeMethod WanxiangBuild.ValidateBuild \
  -wanxiang-storage-root 'I:\WGCombat\<fresh>\PureBuild1' \
  -logFile 'I:\WGCombat\<fresh>\PureBuild1\Unity.log' -batchmode
```

验收：`summary.txt` 为 `result=Succeeded errors=0`；`RuntimeInitializeOnLoads.json`
中验证驱动条目数 = **0**（本批 28 项 root、0 个验证 Boot）。

> R2 纯包 EXE SHA `001aeebf…` / Assembly SHA `3763776a…` 与 R1 `PureBuild2` **逐字一致**，
> 证明 R2 未改任何产品源码。

```bash
# 2) 编译并注入 sidecar（仅改隔离副本）
cp -a PureBuild1/Release <fresh>/Observed/Release
python Evidence/Tools/build_driver.py \
  --managed '<fresh>/Observed/Release/WanxiangGuitu_Data/Managed' \
  --source  'Evidence/Tools/R2Driver.cs.txt' \
  --work    '<fresh>/Observed' \
  --data    '<fresh>/Observed/Release/WanxiangGuitu_Data' \
  --evidence 'Evidence/Runs/DriverBuild<fresh>'

# 3) 每个用例一个独立 Player Run
python Evidence/Tools/run_player.py \
  --exe '<fresh>/Observed/Release/WanxiangGuitu.exe' \
  --managed '<fresh>/Observed/Release/WanxiangGuitu_Data/Managed' \
  --run-root 'I:\WGCombat\<fresh>\PlayerRuns\<case>-<fresh>' \
  --evidence 'Evidence/Player/<case>-<fresh>' \
  --mode r2 --case <case> --timeout 300

# 4) 严格判定（禁止跨 Run join）
python Evidence/Tools/r2_analysis.py
python Evidence/Tools/finalize_evidence.py
python Evidence/Tools/finalize_evidence.py --only-manifest
```

## 3. 用例清单与受控参数

水平位置在所有几何用例固定在环带中间 `origin + dir * 3.2`（`dr=0`），
因此 `geometry` 差异**只来自高度**。冻结合同：
`InnerRadius=2.2` / `OuterRadius=6.0` / `HalfHeight=1.2` / `ε=0.0001` / `rawDamage=22` / 闭集切线。

`body.center.y = origin.y + Collider.center.y`，`stem = height/2 - radius = 0.6`，
`reach = radius + ε = 0.4001`：

| 用例族 | `center.y` | 期望 `geometry` | 说明 |
|---|---|---|---|
| `h-in-*` | `1.0` | TRUE | 完全处于竖直带内 |
| `h-tangent-top-*` | `2.2` | TRUE | `vgap=0.4`，上端闭集切线 |
| `h-tangent-bottom-*` | `-2.2` | TRUE | `vgap=0.4`，下端闭集切线 |
| `h-just-out-*` | `2.21` | FALSE | `vgap=0.41 > reach` |
| `h-above-*` | `3.0` | FALSE | 完全带外 |

`*-cc` 用 `CharacterController`；`*-cap` 禁用 CC、只用根 `CapsuleCollider(direction=1)`。

| 类别 | 用例 |
|---|---|
| R2-01 高度 | `h-in-cc`、`h-tangent-top-cc`、`h-tangent-bottom-cc`、`h-just-out-cc`、`h-above-cc`、`h-in-cap`、`h-tangent-top-cap`、`h-tangent-bottom-cap`、`h-just-out-cap`、`h-above-cap` |
| R2-02 暂停 | `pause-warning`、`pause-active`、`timescale-only`（对照，明确标注非 UI-only 替代） |
| R2-03 取消 | `cancel-{death,leave,boss,unload}-{w,a}`（`-w`=Warning，`-a`=Active） |
| R2-04 多 Collider | `b-none`、`b-first`、`b-second`、`b-both`、`b-both-multi`、`b-trigger-child` |

R2-04 用两个有效根胶囊（`CharacterController` + 根 `CapsuleCollider`），
各自 `center.y = 1`（带内）或 `5`（带外）组合出「都不接触 / 仅第一个 / 仅第二个 / 都接触」；
`b-trigger-child` 另加 root trigger `SphereCollider` 与子物体装饰 `CapsuleCollider`，
验证 `Bodies()` 只纳入根对象 enabled 非 trigger 胶囊。

## 4. 真实产品入口（不得绕过）

| 合同 | 使用的产品入口 |
|---|---|
| UI 暂停 | `PlayerHudPresenter.Instance.SetDetails("帮助")` / `SetDetails("")` |
| 玩家死亡 | `CombatHealth.Damage(9999)`（真实伤害入口，非 SetHP） |
| 离开 Arena | `ThirdPersonHero.RestorePosition(P(80,410),90)` → `CrystalCavernBossRules.InsideArena` 失败 |
| Boss 死亡 | `CombatEnemy.Health.Damage(9999)` → `StopDeadAttacks()` → `StopDeath()` |
| 场景卸载 | `GameEntry.ReturnToTitle(CombatSession)` |
| 判定观测 | `CrystalCavernBossBrain.RingProbed`（只读事件） |

**没有**直接写 `HudPanelOpen` 等内部字段伪造暂停，没有 `Destroy` 对象绕过生命周期，
没有用 `Touches()` 模型结果代替 Player 判定。`CrystalCavernRingContact.Bodies()` 仅用于
**记录受击体快照**（`body-dump.tsv`），判定完全来自 `RingProbe.geometry`。

> 产品事实：真实 UI 入口 `SetDetails` 会**同时**置 `HudPanelOpen=true` 与 `Time.timeScale=0`。
> 因此「`GameplayPaused=true` 且 `timeScale>0`」的 UI-only 组合无法经产品入口安全进入，
> 本批记录的是产品真实值，并把 `Time.timeScale=0` 单独作为**对照 case**，不冒充 UI-only。

## 5. 状态分层与禁止项

`PASS-STATIC` / `PASS-MODEL` / `PASS-EDITOR` / `PASS-PLAYER` / `NOT_RUN` / `INCOMPLETE` / `UNRESOLVED`
不得合并成无解释的 PASS。

- 每个用例**独立 Run**，禁止跨 Run join；`r2-strict-correlation.json` 记录 `crossRunJoins=0`。
- null / 缺失字段 → `INCOMPLETE`；缺失事件或文件 → `NOT_RUN`；两者**永不计入 PASS**。
- 每项 check 记录输入行、表达式、操作数、结果（`r2-player-checks.tsv`）。
- 失败运行（含驱动断言修正前的初始失败）原样保留，不改写为 PASS。
- 未改产品几何、奖励投影、Boss 状态机、伤害、预警时长、随机流；**未事后调容差或半径**。
- 未重跑 R1 已通过的 7/7 核心矩阵；R1 结论保持原样。
- 未运行原生键鼠 / 独立人工 / 纯包标题与存档保护验收。

## 6. 保护规则

不修改 `ProjectSettings/`、用户场景、`Packages/`、B1/B2/R1 历史报告与原始证据、真实存档；
不强推、不自动合并 `main`、不升级依赖、不新增 CI；
不提交 `Library/`、Player 二进制、凭据或受限供应商源码。

## 7. 关键路径

| 用途 | 路径 |
|---|---|
| 隔离根 | `I:/WGCombat/C24B2R2-1109-A/` |
| 正式纯包 | `I:/WGCombat/C24B2R2-1109-A/PureBuild1/Release/` |
| 观测副本 | `I:/WGCombat/C24B2R2-1109-A/Observed{1,2}/Release/` |
| Player run 根 | `I:/WGCombat/C24B2R2-1109-A/PlayerRuns/` |
| 交付证据 | `ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/` |
