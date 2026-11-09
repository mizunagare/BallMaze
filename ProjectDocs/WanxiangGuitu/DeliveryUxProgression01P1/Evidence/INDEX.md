# Evidence INDEX · UX-PROGRESSION-01 P1

证据原则：原始文件只增不改。任何失败、超时、越界、被移除的脚手架都留在 `Player/_attempts/` 下，
不删除、不重写、不改判。

## 0. 本批身份

| 项 | 值 |
|---|---|
| 分支 | `feature/ux-progression-01-p1` |
| 设计基线 | `design/ux-progression-01` @ `59190b7036307e69420d43e23e5610f2ddbab9fc` |
| 构建身份（`Assembly-CSharp.dll` SHA256） | `ce03e64171bd136b7549182d2985f8c50328c23ef2a06fb3777732f7bfa06d3c` |
| 启动器 EXE SHA256 | `001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a` |
| 观察驱动 DLL SHA256 | `49c81de5c4e8660340ec8cf8c2a5695892c18ec802b7c486ac56bb3133250695` |
| 纯发行包 | `result=Succeeded errors=0 warnings=113`；`RuntimeInitializeOnLoads.json` 中驱动引用 = 0 |

EXE 是 Unity 固定启动器壳，改动脚本后 SHA 不变；构建身份以 `Assembly-CSharp.dll` 为准（见报告 §6 L6）。

## 1. 目录结构

```
Evidence/
├── INDEX.md                     # 本文件
├── PROTECTION_HASHES.tsv        # 22 个受保护文件的基线 vs 本批 blob 比对（全部 YES）
├── Driver/
│   ├── driver-injection.json    # 驱动编译命令行、编译器 SHA、注入清单与结果
│   └── driver-compile.log       # Roslyn 编译输出（0 error）
├── Tools/
│   ├── IntDriver.cs.txt         # 观察驱动源码（唯一含脚手架的文件）
│   ├── build_driver.py          # 只对观察副本注入；先编 csc 再写 Boot 清单
│   ├── run_player.py            # 新建隔离 run-root，拒绝复用/覆盖，归档全部文件
│   ├── run_batch2.sh            # 本批 13 条 Run 的批量入口
│   ├── summarize_runs.py        # 由归档产物生成 PLAYER_RUN_MATRIX.csv
│   └── protection_hashes.sh     # 生成 §2 的比对表
└── Player/
    ├── p1-<run>/                # 13 条主 Run，每条 15 个原始文件
    └── _attempts/               # 历史失败尝试，按驱动 SHA 归档，只增不改
```

每条 Run 的 15 个文件：`Player.command.json`（完整命令行 + 环境变量 + 三层 SHA）、
`Player.exit.json`、`Player.log`、`Player.stdout`、`Player.stderr`、`process.json`（PID/时间线）、
`assertions.tsv`（逐条断言与数值）、`int-events.jsonl`（驱动事件流）、`int-frames.tsv`（逐帧样本）、
`entry-audit.jsonl`、`storage-audit.jsonl`、`exe-sha256.txt`、`cavern-test.txt`（模式）、
`complete.txt`（PASS/FAIL）、`run-summary.json`（判定汇总）。

## 2. 13 条主 Run 的用途与关键断言

| Run | 覆盖点 | 代表性断言（原样摘自 `assertions.tsv`） |
|---|---|---|
| `p1-forest-gather-success` | 森林 · 采集 · 成功撤离 | `p1-forest-gather-achieved-matches-met` / `-success-settled` / `hud=18,evaluator=18` |
| `p1-forest-treasure-death` | 森林 · 扫箱 · 死亡 | `-fail-not-achieved: achieved=False` / `-fail-badge: 目标条件已满足但未成功撤离 · 扫箱 · 森林` |
| `p1-forest-counter` | 反刷（continue 存档后带料进场） | `p1-carried-is-zero: hud=0,carried=30,earned=0` / `p1-spend-no-regress: before=18,after=18,spentRecorded=5` |
| `p1-ruins-gather-success` | 遗迹 · 清点 · 成功撤离；机关链 | `p1-ruins-gather-achieved-matches-met` / `-success-settled` / `p1-ruins-no-vein-notice` PASS |
| `p1-ruins-challenge-abandon` | 遗迹 · 守誓 · 放弃 | `-fail-not-achieved: achieved=False` / `-fail-badge: 目标未达成 · 守誓 · 遗迹 守护者 0/1` |
| `p1-cavern-gather-success` | 洞窟 · 掘脉 · 成功撤离 | `-achieved-matches-met` / `-success-settled` / `hud=4,evaluator=4,cardId=cavern.gather` |
| `p1-cavern-treasure-abandon` | 洞窟 · 双箱 · 放弃 | `-fail-badge: 目标未达成 · 双箱 · 洞窟 矿室宝箱 0/1` |
| `p1-xproc-{forest,ruins,cavern}-1` | 跨进程第一段：选目标、采集、消费、存盘 | `xproc-select-goal` / `xproc-harvest` / `xproc-spend` / `xproc-save` |
| `p1-xproc-{forest,ruins,cavern}-2` | 跨进程第二段：继续存档，读回只读快照 | `xproc-same-run` / `xproc-not-exact-after-spend` / `xproc-hud-value-not-above-persisted` / `xproc-persisted-bound-matches-held` |

每条主 Run 还会扫 3 个目标 × 2 轮，产出 `hud-card-matches-goal` / `hud-line1` / `hud-line2-budget` /
`hud-line3` / `route-top3-order` / `route-excluded` / `settlement-next-steps` / `settlement-snapshot` /
`progress-not-below-held` / `no-false-positive` 各 37 次（跨 13 条 Run 汇总）。

## 3. 历史失败尝试（保留，未改写）

| 目录 | 内容（按驱动 SHA 归档的整批 Run） |
|---|---|
| `_attempts/driver-6c8261` | 6 条：3 完成 / 3 失败（早期驱动基建阶段） |
| `_attempts/driver-6080378d` | 3 条：2 完成 / 1 失败 |
| `_attempts/driver-03029fe8` | 13 条：10 完成 / 3 失败（撤离期被打断、`commit` 失败） |
| `_attempts/driver-601671a9` | 13 条：6 完成 / 7 失败（`saveFailed=True` 越界连锁） |
| `_attempts/driver-6e134b21` | 13 条：9 完成 / 4 失败 |
| `_attempts/driver-prev` | 14 条：10 完成 / 4 失败（含 `enemy:enemy:10@-71.597857,-129.998734,334` 越界） |
| `_attempts/driver-bf1cc894-build69423fc4` | 13 条全完成，但结算文本"已达成 · 待撤离"与"下一步：换一种目标"自相矛盾（已修正，见报告 §4.1） |
| `_attempts/p1-forest-gather-success-r0..r4` | 森林采集单点的 5 轮早期失败（采集期被精英击杀、HUD 采样竞态、条件满足但数值未镜像等） |

这些目录里的 `run-summary.json` / `assertions.tsv` 保持原始判定，本批**没有**把它们改成 PASS。

## 4. 复现路径

```bash
# 1) 纯发行构建（ValidateBuild 要求全新输出目录，旧目录须改名留档，不能复用）
UNITY_TEST_ROOT='I:/WGUP01/Build' "…/Unity.exe" -projectPath 'I:/unity/WanxiangGuitu' \
  -executeMethod WanxiangBuild.ValidateBuild -wanxiang-storage-root 'I:/WGUP01/Build' \
  -logFile 'I:/WGUP01/Build/Unity.log' -batchmode

# 2) 观察副本 + 驱动注入（只改副本）
cp -a I:/WGUP01/Build/Release/. I:/WGUP01/Observe/Release/
python Evidence/Tools/build_driver.py --managed …/Observe/Release/WanxiangGuitu_Data/Managed \
  --source Evidence/Tools/IntDriver.cs.txt --work I:/WGUP01/Observe/driver \
  --data …/Observe/Release/WanxiangGuitu_Data --evidence Evidence/Driver

# 3) 13 条真实 Player Run（需要在沙箱外跑，否则 run-root 子目录不持久）
bash Evidence/Tools/run_batch2.sh

# 4) 汇总与保护比对
python Evidence/Tools/summarize_runs.py
bash Evidence/Tools/protection_hashes.sh
```

完整命令、前置条件与验收口径见 `../TESTING.md`。
