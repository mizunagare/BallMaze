# UX-PROGRESSION-01 P1C · 证据索引（Evidence/INDEX）

原始件一律逐字节留档，`*.log` 在 `Evidence/.gitignore` 里显式解除忽略（根 `.gitignore` 的 `*.log` 会吞掉它们）。

## 1. 目录结构

```
Evidence/
  PROTECTION_HASHES.tsv          27 个受保护文件 vs P1 交付点（ff81eb1cb），全 identical=YES
  INDEX.md                       本文件
  .gitignore                     只做一件事：让 *.log 能被提交
  Tools/                         p1c_run.sh / run_player.py / build_driver.py / summarize_runs.py
                                 build_closure_matrix.py / protection_hashes_p1c.sh / IntDriver.cs.txt
  Driver/
    p1c-forest-challenge/        该 Run 自己的 driver-injection.json + driver-compile.log
    p1c-ruins-challenge/
    p1c-cavern-challenge/
    _superseded/                 换 -deterministic 之前的编译记录（DLL 字节随 PE 时间戳变化，已作废）
  Player/
    p1c-forest-challenge/        主证据 1
    p1c-ruins-challenge/         主证据 2
    p1c-cavern-challenge/        主证据 3
    _attempts/                   9 个失败 / 中间批次，逐条见 §3
```

## 2. 每条主 Run 的 16 个原始件

| 文件 | 用途 |
|---|---|
| `Player.command.json` | 完整命令行、env、exe/构建/驱动三层 SHA、`observationPlayer=true` |
| `Player.exit.json` / `process.json` | 退出码、PID、是否被强制终止、是否超时 |
| `Player.log` / `stdout` / `stderr` | Unity Player 原始日志（含 Graphics/PhysX/输入系统初始化） |
| `assertions.tsv` | 驱动逐条断言（本批共 140 行 PASS / 0 FAIL） |
| `int-events.jsonl` | 结构化事件：identity / region-depart / target / interact / walk-stuck / fight / killed / settle / closed |
| `int-frames.tsv` | 逐帧采样：frame/time/timeScale/gameplayPaused/dead/phase/… |
| `p1c-trace-<region>.tsv` | 战斗逐 20 帧采样：距离、双方血量、威胁倒计时、是否在攻击距离、是否按键、附近敌人数 |
| `entry-audit.jsonl` | Boot→Title→ForestRuins 的入口审计（每个阶段一行） |
| `storage-audit.jsonl` | 存储根审计（确认写的是本次 Run 的独立目录） |
| `exe-sha256.txt` | 被测 exe 的 SHA |
| `run-summary.json` | 机器可读判定：`verdict` / `exitCode` / `completeTxt` / 三层 SHA / 归档清单 |
| `complete.txt` | 驱动写出的终态标记（`PASS` 才代表跑完） |
| `cavern-test.txt` | 模式标记（兼容历史批次） |

## 3. `_attempts/` 逐条说明（都不参与验收，只证明"没做成时是什么样"）

| 目录 | 断言 | 它证明了什么 |
|---|---|---|
| `smoke1` | 19 PASS / 2 FAIL | 早期驱动只会直线走位：被精英打到 `hp=8` 时英雄死亡，走位必须能打拦路敌 |
| `smoke2` | 27 PASS / 7 FAIL | 击杀首领后出口走位 94m 不动、拦路战 `inRange=0` —— 暴露"暂停中继续走位"的坑 |
| `smoke3` | 27 PASS / 8 FAIL | 与 smoke2 一致复现，确认不是偶发 |
| `forest-heal-assert` | 42 PASS / 1 FAIL | 目标全达成，只有 `p1c-no-harness-heal` 把"升级选活力 +25"误判成脚手架治疗 |
| `ruins-wall-pinned` | 22 PASS / 3 FAIL | 英雄被顶在 `z≈219.06`，`remain=68.89`，`fight` 段 39,941 帧靠不近 —— 符文石门挡路 |
| `ruins-door-closed` | 22 PASS / 3 FAIL | 加了看门狗后同样卡在 `z=219.12`，25 秒内判 `unreachable=True`，不再耗满预算 |
| `forest-guard-too-tight` | 46 PASS / 2 FAIL | 目标已达成（`目标达成 · 拔点 · 森林`），两条自检口径过粗：`maxStep=1.208`、`healEvents=2` |
| `cavern-uncommitted` | 20 PASS / 4 FAIL | 未提交挑战：贴身 40,863 帧、0 命中、守望者 360/360 不变 —— 挑战提交是硬门槛 |
| `cycle3-nondeterministic` | 三条全 PASS | 逻辑全绿，但每次编译的 DLL 字节因 PE 时间戳不同而不同，"同一版驱动"无法用 SHA 证明；换 `-deterministic` 后重跑，本目录作废 |

## 4. 三条主 Run 覆盖点

| Run | 覆盖 |
|---|---|
| `p1c-forest-challenge` | 卡 `forest.challenge` 拔点；拦路 2 敌；首领 `boss:tide` 290→0；清 1 只追兵后撤离；结算 `目标达成 · 拔点 · 森林` |
| `p1c-ruins-challenge` | 卡 `ruins.challenge` 守誓；机关 `c1:lever`→石门 `c1:door`（各 2 次真实 E）；守护者 `c1:guardian` 320→0；英雄被打到 44 血后 4 次翻滚存活；结算 `目标达成 · 守誓 · 遗迹` |
| `p1c-cavern-challenge` | 卡 `cavern.challenge` 试锋；前室提交挑战 `pendingChoices=0` 后按 E；守望者 `c24:boss:crystal-warden` 360→0；结算 `目标达成 · 试锋 · 洞窟` |

## 5. 复跑

见 `../TESTING.md`。要点：`p1c_run.sh <tag> "p1c:<region>" 600`；
驱动编译带 `-deterministic`，同源同引用必须产出同一个 DLL SHA（`8a8d0ef57451db77…`）。
