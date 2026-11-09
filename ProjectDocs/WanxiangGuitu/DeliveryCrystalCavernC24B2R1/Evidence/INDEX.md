# CP06-C24-B2-R1 证据索引

交付根目录：`ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/`
基线：`98924a34b6df817aa5a979b50439a4515881744b` · 分支：`fix/cp06-crystal-warden-b2-r1`
证据总量：约 1.7 MiB / 221 个文件（以 `Evidence/After/hash-manifest.json` 为准）。

---

## 1. 顶层交付

| 文件 | 内容 |
|---|---|
| `REPORT.md` | 完整技术报告：SHA、工具修正、四个 R1 子项、构建链、失败历史、保护与结论 |
| `ACCEPTANCE.md` | 分层验收表（R1-00 ~ R1-05）与待复审重点 |
| `TESTING.md` | 复跑顺序、无 `pwsh` 的独立启动方案、状态分层、保护规则 |
| `RING_WARNING_VISUAL_PROPOSAL.md` | R1-03 晶环预警可读性最小设计（DESIGN_ONLY） |

## 2. 目录结构

```
Evidence/
├── INDEX.md                         本文件
├── Before/                          无 Player 事件时的严格工具基线（不冒称 PASS）
│   ├── c05-strict-correlation.json  10 项全部 NOT_RUN
│   ├── c05-strict-checks.tsv
│   └── b2-reevaluation.json
├── After/                           正式判定与汇总
│   ├── c05-strict-correlation.json  PASS-PLAYER_SAME_RUN_C05 (10/10)
│   ├── c05-strict-checks.tsv        每项 check 的输入行 / 表达式 / 结果
│   ├── b2-reevaluation.json          B2「10/10」只读重审（保留原文件）
│   ├── r1-tool-selfcheck.json        三条硬规则自测
│   ├── ring-player-matrix.json       RING_PLAYER_MATRIX_PASS (7/7)
│   ├── ring-player-checks.tsv
│   ├── ring-player-matrix-initial.json   初始 4/7（断言错误，失败历史）
│   ├── ring-player-checks-initial.tsv
│   ├── projection-regression.json   PROJECTION_REGRESSION_PASS (8/8)
│   ├── projection-cases.tsv
│   ├── protection.json              PROTECTION_PASS / 违规 0
│   ├── build-identity.json          纯包与观测副本身份
│   ├── player-runs.json             10 次真实 Player run 清单
│   ├── remote-verification.json     推送后远端完整 SHA 复核
│   └── hash-manifest.json           全量 SHA256 清单（排除自身）
├── Tools/                           可复跑工具（拒绝对既有输出覆盖）
│   ├── r1_correlate.py              严格同一 Run 关联（R1-R4 硬规则）
│   ├── r1_ring_analysis.py          晶环 Player 矩阵判定
│   ├── r1_projection_regression.py  R1-04 定向回归
│   ├── build_driver.py              sidecar 驱动编译 + 注入
│   ├── run_player.py                独立观测 Player 启动器（不依赖 pwsh）
│   ├── finalize_evidence.py         保护哈希 / 构建身份 / 全量清单
│   └── R1Driver.cs.txt              观测驱动源码（仅编译进隔离副本）
├── Runs/                            构建与编译记录
│   ├── PureBuild1/                  首次构建命令/退出回执（后被弃用）
│   ├── PureBuild1-DISCARDED/        弃用原因 + 含两个历史 Boot 的 RuntimeInitializeOnLoads
│   ├── PureBuild2/                  正式干净纯包（Editor.command / Editor.exit）
│   └── DriverBuild{1,2,3,4}/       各版驱动 DLL 编译与注入记录、失败日志
└── Player/                          10 次真实观测 Player 的原始证据
    ├── r1-c05-A1/   A1 失败（NRE）
    ├── r1-c05-A2/   A2 失败（challenge FAIL）
    ├── r1-c05-A3/   A3 成功：同一 Run C05 完整时间线
    └── r1-ring-{band,inner-edge,outer-edge,inner-safe,outer-safe,wall,dodge}-A1/
```

每个 `Player/<run>/` 含：`Player.command.json`（EXE SHA / Build SHA / 驱动 DLL SHA / Unity 版本 /
启动参数 / UTC）、`process.json`（PID / 超时 / 强制终止）、`Player.exit.json`（原生退出码）、
`Player.log`、`Player.stdout`、`Player.stderr`、`assertions.tsv`、`cavern-test.txt`、
`complete.txt`、`exe-sha256.txt`、`run-identity.json`、`storage-audit.jsonl`、
`entry-audit.jsonl`、`timeline.tsv`，以及
`c05-events.jsonl`（仅 C05）或 `ring-probes.jsonl` + `ring-case.txt` + `ring-summary.json`（晶环）。

## 3. 关键原始证据

| 证据 | 路径 | 内容 |
|---|---|---|
| C05 同一 Run 事件 | `Evidence/Player/r1-c05-A3/c05-events.jsonl` | 18 事件，1 身份，0 null 时间；`warning → bossHealth → release → heroHealth → recoveryEnd → transitionBegin → p2Release` |
| C05 逐帧时间线 | `Evidence/Player/r1-c05-A3/timeline.tsv` | 每帧 frame/time/state/attack/remaining/bossHP/heroHP/phase/releases |
| C05 身份 | `Evidence/Player/r1-c05-A3/run-identity.json` | runId `ce7b7cd3442e4b8ba628f34d887d0391` / PID 32980 / buildSha |
| RingProbe 原始记录 | `Evidence/Player/r1-ring-*/ring-probes.jsonl` | 每样本 20–24 帧全字段 |
| 严格关联 | `Evidence/After/c05-strict-correlation.json` | `PASS-PLAYER_SAME_RUN_C05`，10/10 |
| 晶环矩阵 | `Evidence/After/ring-player-matrix.json` | `RING_PLAYER_MATRIX_PASS`，7/7 |
| 投影回归 | `Evidence/After/projection-regression.json` | `PROJECTION_REGRESSION_PASS`，8/8 |
| 保护哈希 | `Evidence/After/protection.json` | `PROTECTION_PASS`，违规 0 |

## 4. 关键 SHA256

| 对象 | SHA256 |
|---|---|
| 正式纯包 `WanxiangGuitu.exe` | `001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a` |
| `Assembly-CSharp.dll`（Build SHA） | `3763776a762c00d25761d952b7cb4d881203fc3a43c568f1550eec7c412e6002` |
| B2 `c05-correlation.json`（冻结） | `7d7d78a0972126103d1d8f2f1b5f0590ead5cd2dba8c008e9b7ce08bdcd82b9a` |
| 弃用构建 `RuntimeInitializeOnLoads.json` | `8e8a9ea67c8ce7013d341b86ed0b9d0fa26fb591121303083251476eae201dc2` |
| 驱动 DLL（最终版 DriverBuild4） | `d48506bff6179ec01bb67cc53cbdddc974cbc976550a7dfbda1d92d3d73ba392` |
| 驱动 DLL（C05 A3 版 DriverBuild3） | `4e1c9d21bfa110f9bb198a73a8c8bc4ed0fb229b9a3d50eff7f68b3914a49777` |

各 Player run 的 EXE / Build / 驱动 DLL SHA 以该 run 的 `Player.command.json` 为准；
全量文件哈希见 `Evidence/After/hash-manifest.json`。

## 5. 状态分层索引

| 层 | 结论 | 证据位置 |
|---|---|---|
| `PASS-STATIC` | 工具硬规则、B2 重审、六项门禁、旧地图分支、投影无副作用 | `Evidence/After/{r1-tool-selfcheck,b2-reevaluation,projection-regression}.json` |
| `PASS-MODEL` | alive/dead/collected 四态、任意 uint 工厂等价 | `Evidence/After/projection-regression.json` |
| `PASS-EDITOR` | 纯发行包构建门禁（`errors=0`，验证 Boot 0） | `Evidence/Runs/PureBuild2/`、`build-identity.json` |
| `PASS-PLAYER` | 同一 Run C05（10/10）、晶环矩阵（7/7） | `Evidence/Player/`、`Evidence/After/` |
| `NOT_RUN` | 竖直带高度、暂停、取消路径、多 Collider、原生输入/人工 | `ACCEPTANCE.md` R1-02-9 ~ 13、`ring-player-matrix.json` 的 `notRunOrUnimplemented` |
| `INCOMPLETE` | B1 历史 C05（原样保留）、无 Player 事件时的工具基线 | B1 `WindupNewAudit1/audit.json`、`Evidence/Before/` |
| `UNRESOLVED` | 无（本批未发现产品行为与冻结合同冲突） | — |

## 6. 失败历史索引

| 记录 | 路径 |
|---|---|
| 弃用的不纯纯包 | `Evidence/Runs/PureBuild1-DISCARDED/discard-reason.json` |
| 编译失败 `CS0619` | `Evidence/Runs/DriverBuild1/driver-compile-failed-1.log` |
| 编译失败 `CS0128` | `Evidence/Runs/DriverBuild4/driver-compile-failed-1.log` |
| Player A1 NRE | `Evidence/Player/r1-c05-A1/failure.txt` |
| Player A2 challenge FAIL | `Evidence/Player/r1-c05-A2/assertions.tsv` |
| 分析断言错误初始判定 | `Evidence/After/ring-player-matrix-initial.json` |

## 7. 复跑入口

顺序与命令见 `TESTING.md`。所有工具默认拒绝覆盖，复跑必须使用新目录。
最小复跑链：

```bash
python Evidence/Tools/r1_correlate.py --self-test
python Evidence/Tools/r1_correlate.py
python Evidence/Tools/r1_ring_analysis.py
python Evidence/Tools/r1_projection_regression.py
python Evidence/Tools/finalize_evidence.py
python Evidence/Tools/finalize_evidence.py --only-manifest
```
