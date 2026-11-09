# CP06-C24-B2-R2 证据索引

交付根目录：`ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/`
基线：`c388e9b7ecf9b5619a65fac81227eba68f61b832` · 分支：`fix/cp06-crystal-warden-b2-r2`
证据规模：约 4.0 MiB；27 个正式 Player run + 2 个失败历史目录（详见 `Evidence/After/hash-manifest.json`）。

---

## 1. 顶层交付

| 文件 | 内容 |
|---|---|
| `REPORT.md` | 完整技术报告：SHA、构建链、四项 Player 证据表、严格关联、失败历史、保护与结论 |
| `ACCEPTANCE.md` | 分层验收表（R2-00 ~ R2-04）、总体判定与复审重点 |
| `TESTING.md` | 复跑顺序、无 `pwsh` 独立启动链、用例清单与受控高度公式、状态分层、保护规则 |

## 2. 目录结构

```
Evidence/
├── INDEX.md                        本文件
├── Tools/                          可复跑工具
│   ├── build_driver.py              sidecar 编译 + 注入（与 R1 逐字一致，SHA 846a44eb…）
│   ├── run_player.py                独立观测 Player 启动器（与 R1 逐字一致，SHA 9d7a160b…）
│   ├── R2Driver.cs.txt              本批观测驱动源码（仅编译进隔离副本）
│   ├── r2_analysis.py               严格同一 Run 关联 + 四项矩阵判定
│   └── finalize_evidence.py         保护哈希 / 构建身份 / Player 清单 / 全量 SHA256
├── Runs/                           构建与编译记录
│   ├── PureBuild1/                  干净纯包 Editor.command / Editor.exit
│   └── DriverBuild{1,2,3}/          三版驱动编译与注入记录、首次编译失败日志
├── After/                          正式判定与汇总
│   ├── r2-player-matrix.json         R2_PARTIAL_OR_NOT_RUN（25 PASS-PLAYER / 2 NOT_RUN）
│   ├── r2-player-checks.tsv          每项 check 的输入行 / 表达式 / 结果
│   ├── r2-strict-correlation.json    crossRunJoins=0、null 不能 PASS
│   ├── protection.json              PROTECTION_PASS / 违规 0
│   ├── build-identity.json           纯包与观测副本身份
│   ├── player-runs.json             全部真实 Player run 清单
│   ├── remote-verification.json     推送后远端完整 SHA 复核
│   └── hash-manifest.json           全量 SHA256 清单（排除自身）
└── Player/                         每个用例一个独立真实 Player Run
    ├── <case>-A1/                   27 个正式用例
    ├── pause-warning-A1-FAILED/     驱动断言修正前的失败历史
    └── timescale-only-A1-FAILED/    对照语义修正前的失败历史
```

每个 `Player/<case>-A1/` 含：

| 文件 | 内容 |
|---|---|
| `Player.command.json` | EXE SHA / Build SHA / 驱动 DLL SHA / Unity 版本 / 启动参数 / UTC |
| `process.json` / `Player.exit.json` | PID、超时、强制终止、原生退出码 |
| `Player.log` / `Player.stdout` / `Player.stderr` | 原始日志与输出 |
| `run-identity.json` | runId / PID / buildSha / caseName / storageRoot |
| `case-summary.json` | 用例元数据、期望、观察计数（**非判定依据**） |
| `assertions.tsv` | 驱动侧断言（保留失败） |
| `ring-probes.jsonl` | 原始 `RingProbe` 全字段（取消用例可能为空文件 = 无伤害窗口） |
| `r2-events.jsonl` | 同一 Run 事件：caseStart / release / heroDamage / bodyDump / pause* / cancel* |
| `state-frames.tsv` | 每帧 frame/time/unscaledTime/timeScale/remaining/state/GameplayPaused/HP/releases/probes/tag |
| `body-dump.tsv` | `Bodies()` 只读快照：world center / radius / height / Transform / lossyScale |
| `collider-inventory.tsv` | 根/子 Collider 类型、isRoot、isTrigger、enabled、center、radius、height、direction |
| `entry-audit.jsonl` / `storage-audit.jsonl` | 入口与存档隔离审计 |
| `cavern-test.txt` / `ring-case.txt` | 本 run 的 mode 与 case |
| `complete.txt` / `run-summary.json` | 完成回执与运行摘要 |

## 3. 四项合同的原始证据入口

| 合同 | 用例数 | 关键原始证据 |
|---|---|---|
| R2-01 竖直高度 | 10 | `h-*-A1/{ring-probes.jsonl,body-dump.tsv,collider-inventory.tsv}`；world center.y = 1.08 / 2.28 / −2.12 / 2.29 / 3.08 |
| R2-02 GameplayPaused | 3 | `pause-*-A1/{state-frames.tsv,r2-events.jsonl,assertions.tsv}`；584/595/581 个 paused 帧，Remaining 与 HP 恒定 |
| R2-03 取消生命周期 | 8 | `cancel-*-A1/{r2-events.jsonl,ring-probes.jsonl}`；`cancelTrigger` 帧之后无 applied probe |
| R2-04 多 Collider | 6 | `b-*-A1/{ring-probes.jsonl,body-dump.tsv,collider-inventory.tsv}`；bodyCount=2、一次 release 最多 1 次 Damage |

## 4. 判定与状态分层

| 层 | 结论 | 位置 |
|---|---|---|
| `PASS-PLAYER` | 25/27 用例 | `Evidence/After/r2-player-matrix.json` 的 `perCase` |
| `NOT_RUN` | `cancel-unload-w`、`cancel-unload-a`（Boss 卸载后状态不可观测）；另 R2-02-9 UI-only 组合 | 同上 + `ACCEPTANCE.md` 第 3/4 节 |
| `PASS-EDITOR` | 纯发行包构建门禁（`errors=0`，验证 Boot 0） | `Evidence/Runs/PureBuild1/` |
| `PASS-STATIC` | 严格关联规则、保护哈希、产品源码零修改 | `r2-strict-correlation.json`、`protection.json` |
| `INCOMPLETE` / `UNRESOLVED` | 无 | — |

`r2-player-matrix.json` 总判定 **`R2_PARTIAL_OR_NOT_RUN`**：不把部分覆盖汇总成无解释的 PASS，
不把 Editor / 静态模型 / 驱动自述冒充 Player 结果。

## 5. 关键 SHA256

| 对象 | SHA256 |
|---|---|
| 纯包 `WanxiangGuitu.exe` | `001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a` |
| `Assembly-CSharp.dll`（Build SHA） | `3763776a762c00d25761d952b7cb4d881203fc3a43c568f1550eec7c412e6002` |
| 驱动 DLL（DriverBuild1 / Observed1） | `e9fc333239bf7128b1192b07151032990423f0d1cda2de1686540d11ab5edf1d` |
| 驱动 DLL（DriverBuild2 / Observed2） | `c0283fe07ab666bb2f61d4fd3d2fd52ab7960e0d3dc2fa12d7c9665eff7a823a` |
| 驱动 DLL（DriverBuild3 / Observed3） | `ed0387c70583126f5788ff81e201f8b51b54579fec665cdeca61fa36487c99a2` |

> 纯包 EXE / Assembly SHA 与 R1 `PureBuild2` **逐字一致**：R2 未修改任何产品源码。
> 每个 run 的实际驱动 DLL SHA 以该 run 的 `Player.command.json` 为准。

## 6. 失败历史索引

| 记录 | 路径 |
|---|---|
| 首次驱动编译失败 `CS7036` | `Evidence/Runs/DriverBuild1/driver-compile-failed-1.log` |
| `pause-warning` 断言修正前 | `Evidence/Player/pause-warning-A1-FAILED/` |
| `timescale-only` 对照语义修正前 | `Evidence/Player/timescale-only-A1-FAILED/` |
| 断言修正说明 | `REPORT.md` 第 8 节、`ACCEPTANCE.md` 复审重点第 3 项 |

## 7. 复跑入口

顺序与命令见 `TESTING.md`。最小复跑链：

```bash
python Evidence/Tools/r2_analysis.py --cases <case-list>   # 或全量
python Evidence/Tools/r2_analysis.py
python Evidence/Tools/finalize_evidence.py
python Evidence/Tools/finalize_evidence.py --only-manifest
```

所有工具默认拒绝覆盖已有输出；每个 Player run 必须使用全新的 `--run-root` 与 `--evidence` 目录。
