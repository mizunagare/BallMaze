# SKILL-STATE-01 复跑说明与证据分层

> 本文件给出**从零复跑**本批全部证据的命令、环境与判定规则。
> 所有路径为隔离工程路径，不触碰用户仓库场景、`ProjectSettings` 或真实存档。

## 1. 环境与工具链

| 项 | 值 |
|---|---|
| Unity Editor | `6000.6.5f1`（`C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe`） |
| .NET / Roslyn | Unity 自带 `DotNetSdk/sdk/8.0.318/Roslyn/bincore/csc.dll` + `C:/Program Files/dotnet/dotnet.exe` |
| Python | 3.13.x |
| PowerShell 7 (`pwsh`) | **缺失**；本批完全不依赖它 |
| 构建工程 | `I:/WGCombat/C24B2-1109-A/Project`（R1 清理过的隔离副本，验证 Boot=0） |
| 纯包（修复前） | `I:/WGCombat/SkillState01-1109-A/PureBuild1/Release` |
| 纯包（修复后） | `I:/WGCombat/SkillState01-1109-A/PureBuild2/Release` |
| 观测副本 | `Observed1`（修复前）、`Observed2`（修复后），均为纯包副本 + sidecar 注入 |

沿用 R1 的两个工具，**哈希未修改**：

| 工具 | SHA256（前 16） | 用途 |
|---|---|---|
| `Evidence/Tools/build_driver.py` | `846a44eb3065135a` | Roslyn 编译 sidecar DLL，注入副本的 `RuntimeInitializeOnLoads.json` / `ScriptingAssemblies.json` |
| `Evidence/Tools/run_player.py` | `9d7a160bdcfda757e` | 独立启动真实 Player，写 `cavern-test.txt` / `ring-case.txt`，记录 EXE/Build/驱动 SHA、PID、参数、日志、原生退出回执 |

新增工具：

| 工具 | 用途 |
|---|---|
| `Evidence/Tools/run_restore_read.py` | **新进程**读档：复用 `restore-write` 的同一存档根目录，但启动独立 PID；仅替换驱动输入文件，不改存档 |
| `Evidence/Tools/audit_r2_protection.py` | R2 保护哈希矛盾的严格核对 |
| `Evidence/Tools/static_audit.py` | 冻结源码事实与 SHA256 |
| `Evidence/Tools/skill_analysis.py` | 严格逐 case 判定（禁跨 Run join、null 不能 PASS） |
| `Evidence/Tools/finalize_evidence.py` | 保护哈希、构建身份、Player 清单、全量 SHA256 |
| `Evidence/Tools/SkillStateDriver.cs.txt` | 观测驱动源码（sidecar，不进纯包） |

## 2. 证据分层（不得互相冒充）

| 层级 | 本批内容 |
|---|---|
| `PASS-STATIC` | `Evidence/Before/static-audit.json`：11 个产品源码 SHA256 + 15 条冻结控制流事实 |
| `PASS-MODEL` | 冻结判据复算（TTL=3s、life=2.5s、暂停 2s/4s 与差值比较） |
| `PASS-PLAYER` | 每个 case 一个**独立真实 Player 进程**，各带 `runId / PID / buildSha / EXE SHA / 驱动 SHA`、命令行、`Player.log`、`process.json`、`Player.exit.json`、原始 `skill-events.jsonl` / `skill-frames.tsv` / `assertions.tsv` / `case-summary.json` |
| `NOT_RUN` | 未运行、状态不可安全进入、夹具未达成的子项（见第 5 节） |
| `INCOMPLETE` | 保留历史 C05 等，本批不改写 |

严格关联规则（沿用 R1）：**跨 Run 事件不 join；null 时间与缺失事件不得计 PASS**；
`time == 0` 是场景加载期的合法零值，不等同 null（见 `skill_analysis.py` 的修正说明）。
每项 check 记录输入行、比较表达式、操作数与结果。

## 3. 从零复跑（修复前 / 修复后）

### 3.1 纯发行包构建

```bash
UNITY="C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe"
PROJ='I:\WGCombat\C24B2-1109-A\Project'
ROOT='I:\WGCombat\SkillState01-1109-A\PureBuild<N>'
UNITY_TEST_ROOT="$ROOT" "$UNITY" -projectPath "$PROJ" \
  -executeMethod WanxiangBuild.ValidateBuild \
  -wanxiang-storage-root "$ROOT" -logFile "<log>" -batchmode
```

门禁：`result=Succeeded, errors=0`，且 `RuntimeInitializeOnLoads.json` 中验证 Boot 条目 = **0**。
修复前 `PureBuild1` 的 EXE/Assembly SHA 与 R2 纯包逐字一致；修复后 `PureBuild2`
只有 `Assembly-CSharp.dll` 变化（`WeaponSkillExpansion.cs` 一处有效时钟修复）。

### 3.2 sidecar 编译注入（只对副本）

```bash
python Evidence/Tools/build_driver.py \
  --managed "I:/WGCombat/SkillState01-1109-A/Observed<N>/Release/WanxiangGuitu_Data/Managed" \
  --source "I:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Tools/SkillStateDriver.cs.txt" \
  --work "I:/WGCombat/SkillState01-1109-A/Observed<N>" \
  --data "I:/WGCombat/SkillState01-1109-A/Observed<N>/Release/WanxiangGuitu_Data" \
  --evidence "I:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Runs/DriverBuild<N>"
```

编译器路径与引用列表由工具内置默认值提供（与历史 `Prepare-Player.ps1` 一致），
不需要在命令行拼写编译器可执行文件。

### 3.3 单个 case

```bash
python Evidence/Tools/run_player.py \
  --exe "I:/WGCombat/SkillState01-1109-A/Observed<N>/Release/WanxiangGuitu.exe" \
  --managed "<同上>/Managed" \
  --run-root "I:/WGCombat/SkillState01-1109-A/PlayerRuns/<case>-<suffix>" \
  --evidence "I:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliverySkillState01/Evidence/Player/<case>-A1" \
  --mode skill-state --case "<case>" --timeout 300
```

**`run_player.py` 拒绝复用已存在的 run-root 与 evidence 目录**。复跑必须使用新的
`-A2` / `-B1` 等后缀，绝不覆盖旧结果。修复前 14 个 run 已整体保存到
`Evidence/Before/Player-Runs-Before/`，修复后 run 在 `Evidence/Player/`。

### 3.4 新进程读档（C5）

```bash
# 进程 1：写档
python Evidence/Tools/run_player.py ... --case restore-write \
  --run-root ".../PlayerRuns/restore-write-B1" ...
# 进程 2：真正的新进程，复用同一存档根目录
python Evidence/Tools/run_restore_read.py \
  --exe "<same exe>" --managed "<same managed>" \
  --run-root ".../PlayerRuns/restore-write-B1" \
  --evidence ".../Evidence/Player/restore-read-A1" --case restore-read
```

`run_restore_read.py` 只覆盖 `cavern-test.txt` / `ring-case.txt` 两个驱动输入，
**不改 `WanxiangGuitu/` 下的存档**；写档 run 的原始证据已单独归档，两进程事件绝不 join。

### 3.5 判定与汇总

```bash
python Evidence/Tools/audit_r2_protection.py
python Evidence/Tools/static_audit.py
python Evidence/Tools/skill_analysis.py
python Evidence/Tools/finalize_evidence.py
```

## 4. case 清单

| 组 | case | 覆盖合同 |
|---|---|---|
| 符阵基线 | `field-baseline` | C1-1..C1-5 |
| 暂停矩阵 | `field-global-pause-4s`（真实 UI，`timeScale=0`） | C3-1 / C4 |
| 暂停矩阵 | `field-ui-only-2s`（**受控状态注入**，`< TTL`） | C3-2 / C4 |
| 暂停矩阵 | `field-ui-only-4s`（**受控状态注入**，`> TTL`） | C3-2 / C4-2 ← 负例 |
| 生命周期 | `field-switch-slot` / `field-switch-weapon` / `field-dodge` | C3-4 / C3-5 |
| 生命周期 | `field-death` / `field-unload` / `field-natural-expire` | C3-3 / C3-6 |
| 弓蓄力 | `bow-charge` / `bow-charge-cancel` | C2-1..C2-5 |
| 新进程 | `restore-write` + `restore-read` | C5-1..C5-5 |

**UI-only 暂停的可达性事实**：真实 UI 入口 `PlayerHudPresenter.SetDetails` 在打开面板时
**同时**置 `HudPanelOpen=true` 与 `Time.timeScale=0`（R2 已实测）。因此
`GameplayPaused=true && timeScale=1` 的状态在玩家正常菜单中**不可达**；本批通过
`sidecar` 设置公开字段 `HudPanelOpen` 作为 **CONTROLLED_STATE_INJECTION** 验证产品已支持的
状态合同，绝不写成「玩家正常菜单已复现」。每个此类 case 的 `case-summary.json` 都带
`controlledStateInjection=true`。

## 5. 已知限制与 `NOT_RUN`

| 项 | 状态 | 原因 |
|---|---|---|
| `GameplayPaused=true && timeScale>0` 的玩家正常菜单路径 | 不可达 | 产品 UI 入口同时冻结 timeScale；见上 |
| `field-natural-expire` 的「射空无命中」子项 | `NOT_RUN` | 移除目标夹具后弹体仍扫到 arena 地面几何，产生正常 `resolved` + 符阵；夹具未能制造空域飞行，不判产品 FAIL，也不计 PASS |
| 原生键鼠 / 独立人工试玩 | `NOT_RUN` | 本批为观测 Player + sidecar 业务入口，未做人工 |
| 纯包标题保护 / 全量七武器矩阵 | `NOT_RUN` | 本批仅定向审计技能状态，不重跑历史回归 |
| 场景卸载后 Boss 内部字段 | `NOT_RUN` | 卸载后对象销毁，不可观测 |

## 6. 失败与修正历史（全部保留，不改写）

| 记录 | 说明 |
|---|---|
| `Evidence/Runs/DriverBuild1/driver-compile-failed-1.log` | 首版驱动在 `try/catch` 中使用 `yield return`（CS1626）；改为 R1/R2 stack 驱动模式 |
| `Evidence/After/skill-player-matrix-initial.json` / `skill-player-checks-initial.tsv` | 分析工具首版把合法 `time=0` 当 null、把加载期 2 帧算进暂停窗口、把夹具造成的正常命中判产品 FAIL；保留原始判定 |
| `Evidence/Before/Player-Runs-Before/` | 修复前 14 个真实 Player run 的完整原始证据 |
| `Evidence/After/remote-verification.json` | 推送后远端完整 SHA 复核 |

以上修正只作用于**工具 / sidecar / 分析器**，未改产品冻结数值、容差、半径或 TTL。
产品负例 `field-ui-only-4s` 在任何版本判定中都保持 `FAIL-PLAYER`（修复前）。
