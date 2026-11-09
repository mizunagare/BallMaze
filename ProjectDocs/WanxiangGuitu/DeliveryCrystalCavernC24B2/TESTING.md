# CP06-C24-B2 复跑说明与证据边界

## 1. 环境（本批实测）

| 项 | 值 |
|---|---|
| Unity Editor | `6000.6.5f1`，`C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe` |
| `ProjectVersion.txt` | `m_EditorVersion: 6000.6.5f1` / `6000.6.5f1 (3ff58d469c8a)`（未改） |
| Python | 3.13.12 |
| git | 2.55.0.windows.3 |
| .NET | 10.0.402（Unity 自带 DotNetSdk 用于脚本编译） |
| PowerShell | 仅 Windows PowerShell 5.1；**`pwsh` (PowerShell 7) 缺失** |
| 隔离工程 | `I:/WGCombat/C24B2-1109-A/Project`（由 B1 的 `C24B1-1107-A/Project` 整目录复制，含 `Library`） |
| 仓库工作树 | `I:/unity/WanxiangGuitu`（linked worktree，non-cone sparse checkout） |

> 历史 B1 / C24B 的 `Invoke-Editor.ps1` / `Invoke-Player.ps1` 均要求 `pwsh`。本机缺失，
> 因此**没有**重跑历史编排链，也没有伪造新的观测 Player / 纯包日志。
> 本批改为直接调用 `Unity.exe -batchmode -executeMethod`，并把完整命令行、原生退出码、
> `Unity.log`、stdout/stderr 一起存档（见 `Evidence/Runs/Editor-RingContract-A1/`）。

## 2. 证据分层（不得跨层替代）

| 层 | 本批状态 | 产物 |
|---|---|---|
| 静态源码审查 / 控制流模型 | 已做 | `DESIGN_DECISIONS.md`、`REPORT.md`、`c05-correlation.json` 的 `controlFlowModel` |
| 确定性公式 / 源码等价模型 | 已做 | `route-fields-after.json`、`ring-matrix-after.json`、`reward-factory-equivalence.json` |
| **真实 Unity Editor（batchmode）** | **已运行，退出码 0** | `Evidence/Runs/Editor-RingContract-A1/`：命令、日志、`ring-contract.json`、退出回执 |
| 非开发观测 Player（sidecar 驱动） | `NOT_RUN` | 无；需 `pwsh` 编排 |
| 纯发行包（无驱动） | `NOT_RUN` | 无；本批未构建新包，未向任何包注入驱动 |
| 原生键鼠输入 / 独立人工 / 最终平衡 / 性能 | `NOT_RUN` | 无 |
| 冻结历史原始事件只读关联 | 已做（不是新运行） | `c05-correlation.json`、`phase-timeline.json` |

## 3. 复跑顺序（严格）

> **所有工具默认拒绝覆盖已有输出。** 复跑请指定新的输出目录：
> `C24B2_EVIDENCE_OUT=<新目录>`；仅在明确要重生成同一目录时加 `C24B2_FORCE=1`。
> `Evidence/Before/reproduce_before.py` 是**一次性**脚本，永远拒绝覆盖：
> 它必须在任何产品源码修改之前运行，否则会把「修复后」源码哈希写进修复前证据。

### 3.1 修复前复现（本批已在产品改动前执行，输出已冻结）

```bash
python ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2/Evidence/Before/reproduce_before.py
```

只读：从 B1 `arena-route.json`、四组 `ring-release.json` / `ring-damage.tsv`、
`ROUTE_AUDIT.md` / `RING_AUDIT.md`、C24B `WindupNewAudit1/audit.json` 与基线源码公式重算。
**不运行 Unity、不写存档、不推进 RNG、不创建物品、不产生 Player 日志。**
生成 `inputs.json`（25 个输入的 SHA256）、`route-fields-before.json`、
`ring-matrix-before.json`、`c05-timeline-before.json`、`before-repro.json`。

### 3.2 冻结合同（先写，后测）

`DESIGN_DECISIONS.md` 与 `Evidence/Tools/RingContract/contract.json` 在**任何测试之前**写入。
参数、容差、切线规则、14 组几何期望和 5 组运行期望都来自这里，工具不重新拟合。

### 3.3 确定性模型

```bash
T=ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2/Evidence/Tools/RingContract
C24B2_EVIDENCE_OUT=<新目录> python "$T/ring_contract.py"       # 14 组几何接触矩阵
C24B2_EVIDENCE_OUT=<新目录> python "$T/reward_projection.py"   # 逐字段前后 + 工厂载荷等价
C24B2_EVIDENCE_OUT=<新目录> python "$T/c05_correlate.py"       # C05 定向关联
```

- `ring_contract.py` 以 float32 逐行镜像 `CrystalCavernRingContact.Touches()`，
  并记录 `DESIGN_DECISIONS.md`、`contract.json`、产品源码的 SHA256。
- `reward_projection.py` 以 `git show a013c15a...:Assets/.../CrystalCavernBossRewards.cs`
  取基线源码，把新表达式归一化回去并删去新增只读辅助方法，要求**逐字相等**。
  因此复跑不依赖当前 `HEAD`，提交后仍可验证。
- `c05_correlate.py` 只读取 C24B 冻结的 TSV / JSON，不改历史文件。

### 3.4 真实 Unity Editor 运行

```bash
# 1) 复制隔离工程（不要在原历史工程上跑）
cp -a I:/WGCombat/C24B1-1107-A/Project I:/WGCombat/<新根>/Project

# 2) 同步本批产品源码（含两个新文件及 .meta）
SRC=I:/unity/WanxiangGuitu/Assets/CombatPrototype
DST=I:/WGCombat/<新根>/Project/Assets/CombatPrototype
cp "$SRC"/{RouteScoring.cs,CrystalCavernBossRewards.cs,CrystalCavernBossBrain.cs,\
CrystalCavernBossRewardProjection.cs,CrystalCavernRingContact.cs,\
CrystalCavernBossRewardProjection.cs.meta,CrystalCavernRingContact.cs.meta} "$DST"/

# 3) 注入 Editor 契约脚本（只进隔离工程，绝不进发行包）
cp .../Evidence/Tools/RingContract/C24B2RingContractEditor.cs.txt \
   I:/WGCombat/<新根>/Project/Assets/Editor/C24B2RingContractEditor.cs

# 4) 运行（输出目录必须全新）
"C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe" \
  -batchmode -nographics -quit \
  -projectPath "I:/WGCombat/<新根>/Project" \
  -executeMethod C24B2RingContractEditor.Begin \
  -wanxiang-b2-output "<新目录>/ring-contract.json" \
  -logFile "<新目录>/Unity.log"
```

实测命令、参数、起止时间见 `Evidence/Runs/Editor-RingContract-A1/Editor.command.json`
与 `Editor.exit.json`。该 Editor 脚本只调用真实产品函数，创建临时 GameObject 后
`DestroyImmediate` 清理；**不加载游戏场景、不驱动战斗、不写存档、不发布首奖**。
它同时完成整项目脚本编译（0 error），因此也是一次真实 Unity 编译检查。

### 3.5 观测 Player / 纯包（本批 `NOT_RUN`）

历史复跑需要 `Tools/Prepare-Player.ps1`、`Invoke-Player.ps1`、`Invoke-Pure.ps1`（PowerShell 7）。
本机 `pwsh` 缺失，故本批未执行。**不得**把 Editor 结果或 Python 模型写成 Player 通过。
后续复审若在具备 PowerShell 7 的环境补跑，必须新建运行目录、使用无驱动纯包，
并分别记录 `Player.command.json` / `Player.exit.json` / `process.json` / 断言与实际业务轨迹。

## 4. 判定口径

- 进程 `exitCode` 与断言分开判断；本批 Editor 退出码 0 且 `ring-contract.json` 为
  `EDITOR_CONTRACT_PASS` 才登记为 `PASS-RUN`。
- 几何接触、实体遮挡、翻滚免疫、实际扣血分别成列（`RingProbe`）；翻滚免疫 0 伤害
  **不是**几何测试失败。
- 有护甲时预期扣血用 `ArmorMitigation.Incoming(22, defense)`，不固定期待 22。
- 旧 `WindupNewAudit1`（toolVersion 2.0）`INCOMPLETE` 不改写；B2-03 是新增定向关联，
  不是把旧结果改成 PASS。旧 C02/C04 严格三维起点 FAIL 保持。
- 六份旧布局的排序比较口径沿用 B1 `ScoreComparison2` 的稳定 ID 对齐，不采样新输入。

## 5. 保护

- 未修改用户场景、`ProjectSettings/`、真实存档、未提交修改、任何旧交付证据。
- 未使用 `reset` / `clean` / force；未升级依赖、未新增 CI、未自动合并 `main`。
- 未提交 `Library/`、Player 二进制、凭据或受限供应商源码。
- `ProjectSettings/`、场景、旧证据与依赖的哈希清单见 `Evidence/After/protection.json`；
  全量文件哈希见 `Evidence/After/hash-manifest.json`。
