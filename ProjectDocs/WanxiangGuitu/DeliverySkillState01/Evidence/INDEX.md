# SKILL-STATE-01 证据索引

> 所有文件均为本批新增；B1 / B2 / R1 / R2 历史交付、失败与原始证据**未改写**。
> 修复前与修复后的 Player run 分目录保存，**绝不跨 Run join、绝不互相覆盖**。

## 目录树

```
DeliverySkillState01/
├── PROTECTION_AUDIT_R2.md          R2 protection.json 矛盾核对（独立勘误）
├── DESIGN_DECISIONS.md             测试前冻结的 C1–C5 判据、阈值、修复门槛
├── REPORT.md                       交付报告（范围、SHA、复现、修复、复验、保护）
├── ACCEPTANCE.md                   逐项验收表与 NOT_RUN 清单
├── TESTING.md                      从零复跑命令、环境、证据分层、失败历史
└── Evidence/
    ├── INDEX.md                    本文件
    ├── Before/                    修复前 / 开工核对证据
    │   ├── r2-protection-audit.json            601 变更分类、tree SHA 比对、误报结论
    │   ├── static-audit.json                  11 源码 SHA256 + 15 冻结控制流事实
    │   ├── skill-player-matrix-before.json    修复前严格矩阵（负例成立）
    │   ├── skill-player-checks-before.tsv     修复前逐 check 输入/表达式/结果
    │   └── Player-Runs-Before/                修复前 14 个独立真实 Player run（完整原始证据）
    ├── After/                      修复后结论与汇总
    │   ├── skill-player-matrix.json           修复后矩阵 + 前后对比 + PRODUCT_FIX_VERIFIED
    │   ├── skill-player-checks.tsv            修复后逐 check 明细
    │   ├── skill-player-matrix-initial.json   分析器首版错误判定（保留历史）
    │   ├── skill-player-checks-initial.tsv    同上 TSV
    │   ├── protection.json                    PROTECTION_PASS / 0 违规
    │   ├── build-identity.json                两次纯包 EXE/Assembly SHA 与门禁
    │   ├── player-runs.json                   28 个 run 清单（14 前 + 14 后）
    │   ├── hash-manifest.json                 全量 SHA256 清单（513 文件）
    │   └── remote-verification.json           推送后远端完整 SHA 复核（复核提交中新增）
    ├── Player/                     修复后 14 个独立真实 Player run
    ├── Runs/                       构建与注入记录
    │   ├── PureBuild1/             修复前干净纯发行包（与 R2 二进制一致）
    │   ├── PureBuild2/             修复后干净纯发行包（仅 Assembly 变化）
    │   ├── DriverBuild1/           修复前 sidecar 编译注入（含首次 CS1626 失败日志）
    │   └── DriverBuild2/           修复后 sidecar 编译注入
    └── Tools/                      可复跑工具与驱动源码
        ├── SkillStateDriver.cs.txt         sidecar 观测驱动（不进纯包）
        ├── build_driver.py                 沿用 R1，哈希 846a44eb…
        ├── run_player.py                   沿用 R1，哈希 9d7a160b…
        ├── run_restore_read.py             新进程读档启动器
        ├── audit_r2_protection.py          R2 保护矛盾严格核对
        ├── static_audit.py                 冻结静态审计
        ├── skill_analysis.py               严格逐 case 判定（--phase before/after）
        └── finalize_evidence.py            保护 / 构建身份 / run 清单 / 哈希清单
```

## 单个 Player run 的原始文件

每个 `Evidence/Player/<case>-A1/`（及 `Evidence/Before/Player-Runs-Before/<case>-A1/`）含：

| 文件 | 内容 |
|---|---|
| `Player.command.json` | EXE SHA256、Build SHA256、驱动 DLL SHA256、Unity 版本、完整启动参数、`UNITY_TEST_ROOT` |
| `process.json` / `Player.exit.json` | PID、起止 UTC、原生退出码、是否超时/强制终止 |
| `Player.log` / `Player.stdout` / `Player.stderr` | 引擎原始日志与原生输出 |
| `entry-audit.jsonl` / `storage-audit.jsonl` | 启动门禁与隔离存储审计 |
| `cavern-test.txt` / `ring-case.txt` / `exe-sha256.txt` | 驱动输入与 EXE 哈希 |
| `assertions.tsv` | 驱动层基础门禁（不判产品 PASS/FAIL） |
| `skill-events.jsonl` | **核心原始事件**：产品 `AdventureProjectile.Observed` / `WeaponSkillExpansion.Observed` + 驱动动作；每行含 `runId / processId / buildSha / productRunId / frame / time / unscaledTime / timeScale / gameplayPaused / fieldsCount / projectileCount / fieldObjectCount / pierceObjectCount` |
| `skill-frames.tsv` | 逐帧时钟、暂停标志、`fields` 计数、弹体/符阵/贯矢实例数、弹体世界坐标 |
| `case-summary.json` | 该 case 计数、暂停起止 `Time.time`、`fields` 起止、`controlledStateInjection`、反射可用性 |
| `complete.txt` / `failure.txt`（仅失败时） | 驱动结束回执 |
| `run-summary.json` | 归档清单与运行判定 |
| `restore-expect.json` / `restore-expect.from-writer.json` | 仅写档/读档 case：跨进程的期望值与只读副本 |

## 关键证据定位

| 需要核对 | 文件 |
|---|---|
| R2 `b1b2r1HistoryModified=true` 与 `protectedViolations=[]` | `Before/r2-protection-audit.json` + `../PROTECTION_AUDIT_R2.md` |
| 修复前负例（UI-only 4s） | `Before/Player-Runs-Before/field-ui-only-4s-A1/{case-summary.json,skill-events.jsonl,skill-frames.tsv}` |
| 修复后同一 case 转正 | `Player/field-ui-only-4s-A1/{case-summary.json,skill-events.jsonl,skill-frames.tsv}` |
| 前后矩阵与唯一变化 case | `After/skill-player-matrix.json` → `comparison.statusChangedCases` |
| 产品源码最小修复 | 仓库 `Assets/CombatPrototype/WeaponSkillExpansion.cs`（`git diff`） |
| 两次纯包身份 | `After/build-identity.json` + `Runs/PureBuild*/Editor.exit.json` |
| 新进程读档 | `Player/restore-write-A1/` 与 `Player/restore-read-A1/`（PID / runId 不同） |
| 保护与全量哈希 | `After/protection.json` / `After/hash-manifest.json` |
| 远端完整 SHA | `After/remote-verification.json` |

## 证据分层速查

| 层级 | 数量 |
|---|---|
| 真实观测 Player run | **28**（修复前 14 + 修复后 14），每个独立 PID / runId / buildSha |
| 纯发行包构建 | **2**（均 `errors=0`、验证 Boot 0） |
| sidecar 编译注入 | **2**（含 1 份保留的首次编译失败日志） |
| 静态冻结事实 | **15/15**，源码 **11** 份 SHA256 |
| 全量 SHA256 清单 | **513** 文件 |
| `NOT_RUN` 项 | 见 `../ACCEPTANCE.md` 第 9 节与 `../TESTING.md` 第 5 节 |

> 初始分析器错误判定、驱动编译失败、修复前全部 run 均**原样保留**，不重写为 PASS。
> UI-only 暂停一律标注 `CONTROLLED_STATE_INJECTION`，不伪称玩家正常菜单已复现。
