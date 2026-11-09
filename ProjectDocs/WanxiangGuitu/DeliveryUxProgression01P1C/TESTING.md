# UX-PROGRESSION-01 P1C · 复跑说明（TESTING）

本批只补一件事：三地区 **Challenge 目标的真实达成闭环**（击杀 → 撤离 → 结算判达成）。
产品源码零改动，能不能复现完全取决于"构建 → 观察副本 → 注入驱动 → 跑 Player → 汇总"这条链。

分支 `feature/ux-progression-01-p1c-challenge`，基线 `ff81eb1cb`（P1 交付点）。

## 0. 前置

| 项 | 值 |
|---|---|
| Unity | `6000.6.5f1`（Player 与编译器都取自这一版） |
| 纯构建 | `I:/WGUP01/Build/Release`（`Assembly-CSharp.dll` SHA = `ce03e641…a06d3c`） |
| 观察副本 | `I:/WGUP01/Observe/Release`（**只在这里**注入驱动） |
| 运行根 | `I:/WGUP01/Runs/<tag>-<HHMMSS>` |
| 证据根 | `ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1C/Evidence/`

纯构建里 `RuntimeInitializeOnLoads.json` 的验证 Boot 条目数 = 0；驱动只加到副本，
`Evidence/Driver/driver-injection.json` 里 `copyOnly=true` 与前后哈希就是这条边界的凭证。

## 1. 一条命令跑一个地区

```bash
bash ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1C/Evidence/Tools/p1c_run.sh \
     p1c-ruins-challenge "p1c:ruins" 600
```

参数：`<证据目录名> <模式> [超时秒]`。脚本做四件事：

1. 把旧 `Observe/Release` 挪到 `Observe/Release-<tag>-<ts>`（保留，不删）；
2. 从 `Build/Release` 重新 `cp -a` 一份干净副本；
3. `build_driver.py` 用 **Unity 自带 Roslyn** 编译 `Tools/IntDriver.cs.txt` 并注入副本，
   记录编译器 SHA、参数、退出码、DLL SHA、编译日志 SHA；
4. `run_player.py` 起独立进程跑 Player，把原始件归档到证据目录。

三种模式：`p1c:forest`、`p1c:ruins`、`p1c:cavern`。

## 2. 只在需要时重编驱动

证据目录名以 `-nosrc` 结尾时，脚本**跳过**重建副本与编译，直接复用当前副本：

```bash
bash …/p1c_run.sh p1c-ruins-nosrc "p1c:ruins" 600
```

同一批交付内部必须用同一份驱动，所以正常流程不要用它。

## 3. 汇总

```bash
python ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1C/Evidence/Tools/summarize_runs.py
```

只读 `Evidence/Player/*` 的原始件，输出 `PLAYER_RUN_MATRIX.csv`；
缺失项写 `MISSING`，不改写任何判定。

## 4. 保护比对

```bash
bash ProjectDocs/WanxiangGuitu/DeliveryUxProgression01P1C/Evidence/Tools/protection_hashes_p1c.sh
```

判定只用 `git diff --quiet ff81eb1cb -- <path>`（不比较工作区字节，避免 CRLF 误报；
不把缺失文件当相同）。本批 27 个受保护文件应全部 `identical=YES`。

## 5. 失败也要留档

跑挂了**不要删**证据目录，改名挪进 `Evidence/Player/_attempts/<原因>/`。
本批 `_attempts/` 里有 7 个失败/中间批次，报告里逐条说明了原因与它证明了什么。

## 6. 判读要点

| 断言 | 它到底证明了什么 |
|---|---|
| `p1c-walk-target` | 真的用 WASD 走到了目标身边（`remain<=stop+0.8`，无瞬移） |
| `p1c-fight-enemy-dead` | 目标 `Health.Dead==true`，且 `-player-melee-damage` 有逐次扣血样本 |
| `p1c-objective-met` / `-no-achievement-before-extract` | 条件满足但**未撤离时不得判达成** |
| `p1c-achieved` / `p1c-badge` | 结算快照里 `conditionsMet && achieved && settledSuccess` |
| `p1c-no-harness-heal` | 回血次数 ≤ 真实升级选择次数（`healsOutsideLevelUp=0`） |
| `p1c-no-teleport` | 单帧位移 < 2.5m **且** 归一化速度 ≤ 12m/s（冲刺 7 / 翻滚约 9） |
| `p1c-input-path` | 攻击/翻滚/技能都是真实设备事件，且有命中 |
| `p1c-real-threat` | 敌人真的打到了英雄（`minHp < maxHp` 或确有翻滚） |

## 7. 已知的运行期噪声

- 首次进入 Player 约 4–6 秒用于场景与 NavMesh 构建，`p1c-hud-card` 的 10s 窗口要留够。
- 洞窟/遗迹的导航是运行时烘焙，帧率抖动偶发把单帧位移顶到 1m 以上 —— 所以瞬移判据用速度。
- 结算时 `timeScale=0`，此时不要依赖 `Time.time` 推进做超时判断。
