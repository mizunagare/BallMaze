# UX-PROGRESSION-01 P1C · 验收映射（ACCEPTANCE）

判定只用 `Evidence/Player/p1c-*/assertions.tsv` 的真实 Player 断言、原始事件流与源码审计。
`PASS` 仅当证据存在；三条主 Run 之外的批次一律进 `_attempts/`，**不参与验收**，只用来证明"没做成时是什么样"。

- 证据根：`Evidence/Player/p1c-{forest,ruins,cavern}-challenge/`
- 3 条 Run 全部 `verdict=PLAYER_RUN_COMPLETED`、`exitCode=0`、`completeTxt=PASS`
- 合计 **140 PASS / 0 FAIL / 0 SKIP**
- 构建 SHA（`Assembly-CSharp.dll`）= `ce03e64171bd136b7549182d2985f8c50328c23ef2a06fb3777732f7bfa06d3c`
- 驱动 DLL SHA = `8a8d0ef57451db77…`（三条 Run 相同，`-deterministic` 编译）
- 驱动源码 SHA = `d7a7a3fe96779874…`

## A. 门槛类（G）—— 目标不是"走直线就能到"

| # | 条目 | 判定方式 | 断言 / 证据 | 结论 |
|---|---|---|---|---|
| G-01 | 遗迹守誓需要先解开石柱广场机关 | 真实 Player | `p1c-ruins-lever-used: presses=2`；`WorldEventPoint.Interact → RuinsExploration.Interact` | **PASS** |
| G-02 | 机关解开后才能开符文石门，门开才可通行 | 真实 Player | `p1c-ruins-door-open: presses=2,used=True,doorOpen=True` | **PASS** |
| G-03 | 洞窟试锋必须先在前室提交挑战，否则首领不接伤害 | 真实 Player | 正例 `p1c-cavern-challenge-committed: presses=2,pendingChoices=0`；反例见 `_attempts/cavern-uncommitted`（贴身 40,863 帧、0 命中、360/360 不变） | **PASS** |
| G-04 | 升级选择未处理时不可交互（产品规则，不是驱动猜测） | 源码 + 真实 Player | `WorldEventPoint.cs:27` `PendingChoices>0 → CanInteract=false`；驱动先等 `pendingChoices=0` 再按 E，证据里记了该值 | **PASS** |

## B. 闭合类（C）—— 击杀 → 条件满足 → 撤离 → 判达成

| # | 条目 | 断言 | 森林 | 遗迹 | 洞窟 |
|---|---|---|---|---|---|
| C-01 | 局内 HUD 目标卡与本次目标一致 | `p1c-hud-card-matches-goal` | PASS `forest.challenge` | PASS `ruins.challenge` | PASS `cavern.challenge` |
| C-02 | 起始进度为 0/1（负例基线） | `p1c-baseline` | PASS `0/1` | PASS `0/1` | PASS `0/1` |
| C-03 | 目标真实被击杀 | `p1c-fight-enemy-dead` + `-player-melee-damage` | PASS 290→0 | PASS 320→0 | PASS 360→0 |
| C-04 | 击杀后条件满足 | `p1c-objective-met` | PASS `已达成 · 待撤离` | PASS | PASS |
| C-05 | 未撤离不得判达成 | `p1c-no-achievement-before-extract` | PASS `achieved=False,met=True` | PASS | PASS |
| C-06 | HUD 进度跟随真实计数 | `p1c-hud-progress` / `-hud-tracks-kill` | PASS `hud=1,eval=1` | PASS | PASS |
| C-07 | 真实撤离 | `p1c-extract-began` / `p1c-outcome` | PASS `Extracted` | PASS | PASS |
| C-08 | 结算快照 + commit + ack | `p1c-settlement-snapshot` / `-commit` / `-ack` | PASS `forest.challenge` | PASS `ruins.challenge` | PASS `cavern.challenge` |
| C-09 | 判达成（三字段同时为真） | `p1c-achieved` | PASS `met/achieved/success=True` | PASS | PASS |
| C-10 | 角标文案 | `p1c-badge` | `目标达成 · 拔点 · 森林` | `目标达成 · 守誓 · 遗迹` | `目标达成 · 试锋 · 洞窟` |
| C-11 | 结算"下一局三件事"三条非空 | `p1c-next-steps` | PASS 3 条 | PASS 3 条 | PASS 3 条 |
| C-12 | Run 收尾干净 | `p1c-final-run-closed` | PASS `activeRun=null` | PASS | PASS |

## C. 自检类（H）—— 约束观察者本身

| # | 条目 | 判定口径 | 森林 | 遗迹 | 洞窟 |
|---|---|---|---|---|---|
| H-01 | 无脚手架回血 | `healEvents <= levelChoices` 且 `healsOutsideLevelUp=0` | PASS `0/2` | PASS `0/0` | PASS `0/0` |
| H-02 | 无瞬移 | `maxStep<2.5m` 且 `speed<=12m/s` | PASS `0.733m / 8.51m/s` | PASS `0.810m / 8.00m/s` | PASS `0.783m / 8.00m/s` |
| H-03 | 走位是真实输入 | `p1c-no-teleport` + `P1CMoveKeys`（相机相对 WASD） | PASS | PASS | PASS |
| H-04 | 战斗是真实输入且有命中 | `p1c-input-path`（按键数 > 0 且 `hits>0`） | PASS `18/8` | PASS `24/10` | PASS `27/10` |
| H-05 | 敌人真的打了英雄 | `p1c-real-threat`（`dodgePresses>0` 或 `minHp<maxHp`） | PASS `minHp=91` | PASS `minHp=44` | PASS `minHp=82` |
| H-06 | 相机不靠"掰视角"取巧 | `camera-fallback` 事件计数 | 0 | 0 | 0 |

## D. 反例类（N）—— 都是真跑出来的

| # | 反例 | 证据 | 结论 |
|---|---|---|---|
| N-01 | 不提交挑战 → 首领 0 伤害 | `_attempts/cavern-uncommitted`：`hits=0`，`hp=360`，贴身 40,863 帧 | **PASS（反例成立）** |
| N-02 | 不开石门 → 到不了守护者 | `_attempts/ruins-door-closed`：`remain=68.59`，`unreachable=True`；`_attempts/ruins-wall-pinned`：39,941 帧靠不近 | **PASS（反例成立）** |
| N-03 | 只显示不击杀 → 不能算达成 | P1 遗留的 `p1-ruins-challenge-abandon`（本批未复用）+ 本轮 `p1c-no-achievement-before-extract` 3/3 | **PASS** |
| N-04 | 测量口径过粗会误报 | `_attempts/forest-guard-too-tight`：目标已达成，但 `maxStep=1.208` 被判"瞬移"、升级回血被判"脚手架治疗" | **PASS（已修正，原样留档）** |

## E. 保护类（P）

| # | 条目 | 证据 | 结论 |
|---|---|---|---|
| P-01 | 产品源码零改动（相对 P1 交付点） | `Evidence/PROTECTION_HASHES.tsv` 27/27 `identical=YES`；`git diff ff81eb1cb -- Assets/ ProjectSettings/ Packages/` 为空 | **PASS** |
| P-02 | 驱动只注入观察副本 | `Evidence/Driver/p1c-*/driver-injection.json`：`copyOnly=true`，`runtimeInitializeOnLoads` 前后哈希；纯构建验证 Boot 条目 = 0 | **PASS** |
| P-03 | 每条 Run 的驱动同一版 | 三条 `run-summary.json` 的 `driverDllSHA256` = `8a8d0ef57451db77…`；`-deterministic` 保证同源同引用逐字节相同 | **PASS** |
| P-04 | 失败批次留档 | `Evidence/Player/_attempts/` 9 个目录，`Evidence/INDEX.md` 逐条说明它证明了什么 | **PASS** |

## F. 未覆盖（NOT_RUN，不推算）

| # | 项 | 原因 |
|---|---|---|
| L-01 | 重复性（每地区多次） | 本批每地区 1 条 Run，只证"能达成"，不证"稳定能达成" |
| L-02 | 洞窟开桥路径 | 环湖双路可绕行，`c23:bridge:lever` 未被使用 |
| L-03 | 先走到位、再单独开战的顺序 | 三条 Run 的目标都在接近段被打完（`p1c-fight` 段 `frames=0`），走位与战斗是同一套循环 |
| L-04 | 装备成长后重打 | 本批全部使用同一初始装备（`maxHp=100`） |
| L-05 | 人工复玩 / P2 | 不在本批范围 |
