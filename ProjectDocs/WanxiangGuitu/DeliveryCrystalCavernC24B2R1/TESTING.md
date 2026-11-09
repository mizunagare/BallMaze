# CP06-C24-B2-R1 复跑说明与证据边界

## 1. 环境与「无 pwsh」的独立启动方案

| 项 | 值 |
|---|---|
| Unity Editor | `6000.6.5f1`，`C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe` |
| 项目版本 | `ProjectSettings/ProjectVersion.txt` = `6000.6.5f1` |
| .NET | `10.0.402`，`C:/Program Files/dotnet/dotnet.exe` |
| Roslyn | Unity 自带 `DotNetSdk/sdk/8.0.318/Roslyn/bincore/` |
| Python | `3.13.12`（Codex runtime） |
| git | `2.55.0.windows.3` |
| **PowerShell** | **仅 Windows PowerShell 5.1；`pwsh`（PowerShell 7）缺失** |

历史 B1 / C24B 的 `Invoke-Editor.ps1` / `Prepare-Player.ps1` / `Invoke-Player.ps1` / `Invoke-Pure.ps1`
均要求 PowerShell 7。本批**没有**伪造这些编排链的运行结果，而是提供了等价且完全独立的启动方案：

| 步骤 | 历史依赖 pwsh 的动作 | R1 独立替代 |
|---|---|---|
| 纯发行包构建 | `Invoke-Editor.ps1 -Method WanxiangBuild.ValidateBuild` | 直接 `Unity.exe -batchmode -executeMethod WanxiangBuild.ValidateBuild`，`UNITY_TEST_ROOT` 由启动器设置 |
| sidecar 驱动编译 | `Prepare-Player.ps1`（`dotnet csc.dll`） | `Evidence/Tools/build_driver.py`，编译器与引用列表与历史脚本一致 |
| 注入副本 | `RuntimeInitializeOnLoads.json` / `ScriptingAssemblies.json` | 同一工具，仅改隔离副本 |
| 观测 Player 启动 | `Invoke-Player.ps1`（`StartChild` + 独立桌面） | `Evidence/Tools/run_player.py`，`subprocess.Popen` 直接启动，记录 PID / 原生退出码 / stdout / stderr / `Player.log` |
| 存档隔离 | `-wanxiang-storage-root` | 完全一致，每个 run 一个全新根目录 |

> 结论：**本批的真实 Player 结果不依赖 pwsh**，但也没有把 Editor / 静态模型 / Python 计算冒充 Player。

## 2. 复跑顺序（严格）

所有工具默认**拒绝覆盖已有输出**。复跑必须使用新的 run 根目录、新的证据目录、新的构建目录。

### 2.1 基线与分支

```bash
git ls-remote --heads origin main fix/cp06-crystal-warden-b1 fix/cp06-crystal-warden-b2
git checkout -b <fresh-r1-branch> 98924a34b6df817aa5a979b50439a4515881744b
```

### 2.2 先修正证据关联工具（必须先于任何 Player 结论）

```bash
python Evidence/Tools/r1_correlate.py --self-test        # 三条硬规则自测
C24R1_EVIDENCE_OUT=<fresh-before-dir> python Evidence/Tools/r1_correlate.py
```

三条硬规则：**跨 Run 隔离**、**null 时间 → INCOMPLETE**、**缺失事件 → NOT_RUN**。
`b2-reevaluation.json` 只读重审 B2 的 `c05-correlation.json`，不改写 B2 任何文件。

### 2.3 构建纯发行包

隔离构建工程必须与仓库产品源码逐字一致，且**不含任何验证脚本**：

```bash
# 从干净工程移除 Assets/B1Verification/、Assets/Editor/*Validation*.cs
UNITY_TEST_ROOT='I:\WGCombat\<fresh>\PureBuild1' \
"C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe" \
  -projectPath 'I:\WGCombat\<fresh>\Project' \
  -executeMethod WanxiangBuild.ValidateBuild \
  -wanxiang-storage-root 'I:\WGCombat\<fresh>\PureBuild1' \
  -logFile 'I:\WGCombat\<fresh>\PureBuild1\Unity.log' -batchmode
```

验收：`WanxiangGuitu.exe.release.json` 存在、`summary.txt` 为 `result=Succeeded errors=0`、
`RuntimeInitializeOnLoads.json` 中验证驱动条目数 = **0**。

> R1 的第一次构建 `PureBuild1` 因隔离工程残留 `B1Verification` 而被**弃用**，
> 记录见 `Evidence/Runs/PureBuild1-DISCARDED/`。正式用的是 `PureBuild2`。

### 2.4 编译并注入 sidecar 驱动

```bash
cp -a PureBuild2/Release <fresh>/Observed/Release
python Evidence/Tools/build_driver.py \
  --managed '<fresh>/Observed/Release/WanxiangGuitu_Data/Managed' \
  --source  'Evidence/Tools/R1Driver.cs.txt' \
  --work    '<fresh>/Observed' \
  --data    '<fresh>/Observed/Release/WanxiangGuitu_Data' \
  --evidence 'Evidence/Runs/DriverBuild<fresh>'
```

验收：`driver-injection.json` 的 `compileExitCode=0`、`rootEntriesAfter` 比纯包多 1、
`validationBootEntries=1`。驱动源文件与 DLL SHA256 均记录。

### 2.5 运行观测 Player

```bash
# C05 同一 Run 完整时间线
python Evidence/Tools/run_player.py \
  --exe '<fresh>/Observed/Release/WanxiangGuitu.exe' \
  --managed '<fresh>/Observed/Release/WanxiangGuitu_Data/Managed' \
  --run-root 'I:\WGCombat\<fresh>\PlayerRuns\r1-c05-<fresh>' \
  --evidence 'Evidence/Player/r1-c05-<fresh>' \
  --mode r1-c05 --timeout 360

# 晶环样本（每个 case 一个独立 run）
python Evidence/Tools/run_player.py ... --mode r1-ring --case <case> --timeout 300
```

`<case>`：`band`、`inner-edge`、`outer-edge`、`inner-safe`、`outer-safe`、`wall`、`dodge`。

每次运行记录：`Player.command.json`（EXE SHA / Build SHA / 驱动 DLL SHA / Unity 版本 / 参数 / UTC）、
`process.json`（PID / 超时 / 强制终止）、`Player.exit.json`（原生退出码）、
`Player.log`、`Player.stdout`、`Player.stderr`、`assertions.tsv`、`run-identity.json`、
`timeline.tsv`、`c05-events.jsonl` 或 `ring-probes.jsonl`。

**失败运行原样保留**（`r1-c05-A1`、`r1-c05-A2` 及两次驱动编译失败日志），不改写为 PASS。

### 2.6 结果判定

```bash
C24R1_FORCE=1 python Evidence/Tools/r1_correlate.py          # 同一 Run 严格关联
python Evidence/Tools/r1_ring_analysis.py                    # 晶环 Player 矩阵
python Evidence/Tools/r1_projection_regression.py           # R1-04 定向回归
python Evidence/Tools/finalize_evidence.py                  # 保护哈希 / 全量清单
python Evidence/Tools/finalize_evidence.py --only-manifest  # 提交前刷新清单
```

## 3. 状态分层（不得合并成无解释的 PASS）

| 状态 | 含义 | 本批用途 |
|---|---|---|
| `PASS-STATIC` | 源码控制流 / 门禁审查 | R1-04 六项门禁、旧地图分支、投影无副作用 |
| `PASS-MODEL` | 确定性算术重算 | R1-04 alive/dead/collected 四态、工厂 uint 等价 |
| `PASS-EDITOR` | 真实 Unity Editor 批处理 | B2 已跑的 14/14+6/6+14/14（**本批未重跑**） |
| `PASS-PLAYER` | 真实观测 Player 原始事件 | R1-01 同一 Run 时间线、R1-02 RingProbe 矩阵 |
| `NOT_RUN` | 未执行、无原始证据 | 竖直带高度样本、暂停、死亡/离场取消、多 Collider、原生键鼠、人工 |
| `INCOMPLETE` | 有事件但缺身份 / null 时间 / 跨 Run | B2 历史 C05（原样保留） |
| `UNRESOLVED` | 证据冲突待复审 | 视结果填写 |

## 4. 明确 NOT_RUN / 不得冒充

- 本批**没有**重跑 B2 的 Unity Editor 几何契约运行；B2 的 `PASS-EDITOR` 是历史结论。
- 本批**没有**构建或运行无驱动纯发行包做标题/存档保护测试。
- 本批**没有**原生键鼠输入、独立人工游玩、性能或平衡验收。
- 竖直攻击带的 height 用例只存在于 B2 的 Editor/模型层，本批 Player 未覆盖。
- `pwsh` 缺失导致历史编排脚本未运行；本批改用 `run_player.py`，两者结果**不可混写**。

## 5. 保护规则

- 不修改 `ProjectSettings/`、用户场景、依赖、`Packages/`、B1/B2/C24B 历史报告与原始证据。
- 不修改真实存档；每个 Player run 使用 `-wanxiang-storage-root` 指向全新的隔离根。
- 不强推、不自动合并 `main`、不升级依赖、不新增 CI。
- 不提交 `Library/`、Player 二进制、凭据或受限供应商源码。
- 产品源码在本批**零修改**：B2 已接受的奖励投影与晶环几何实现保持不变。

## 6. 关键路径

| 用途 | 路径 |
|---|---|
| 隔离根 | `I:/WGCombat/C24B2R1-1109-A/` |
| 正式纯包 | `I:/WGCombat/C24B2R1-1109-A/PureBuild2/Release/` |
| 观测副本 | `I:/WGCombat/C24B2R1-1109-A/Observed{2,3,4,5}/Release/` |
| Player run 根 | `I:/WGCombat/C24B2R1-1109-A/PlayerRuns/` |
| 交付证据 | `ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/Evidence/` |
