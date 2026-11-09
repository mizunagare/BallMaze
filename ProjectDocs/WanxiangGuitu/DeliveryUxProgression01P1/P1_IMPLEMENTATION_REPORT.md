# UX-PROGRESSION-01 P1 · 只读信息层实施报告

分支：`feature/ux-progression-01-p1`（基线 `design/ux-progression-01` @ `59190b7036307e69420d43e23e5610f2ddbab9fc`）
范围：P1-01 ~ P1-05，纯只读信息层。**不新增存档字段、不改 v9/v10、不改经济/掉落/随机流/护甲/经验/武器伤害/技能冷却。**

## 1. 开工前修订的设计口径（先改文档，再写代码）

| 项 | 问题 | 本批结论 |
|---|---|---|
| **D-08** | 源码审计把 `RunState.earnedRemaining[]` 定义为"本局新获得且尚未消耗"，设计却当成"本局累计所得" | 冻结四量：`GrossEarned` / `EarnedRemaining` / `CarriedIn` / `Spent`；进度用 `GrossEarned`（**排除带入**），消费后**不回退**；无 gross 信号时不得把 remaining 假装成累计 |
| **九卡可达性** | 遗迹无矿脉，`ruins.gather` 原定 8 单位不可达 | 改为 **6 单位**（2 箱最低 4 + 2 普通敌 2）；`forest.treasure` 删去"或 1 件本局装备"的模糊双指标 |
| 其余 | D-01/02/09/11/12/13 冻结口径；D-03 本批不持久化技能槽；D-15 不动 schema | 见 `DECISIONS.md` 的"P1 冻结记录"表 |

三份设计文档已同步修订：`DeliveryUxProgression01/{DESIGN.md §3.1.1/§3.2/§3.3/§3.5, DECISIONS.md, ACCEPTANCE_CRITERIA.md}`。

## 2. D-08：为什么"累计获得"在没有 gross 信号时不可精确反解

源码事实（本批逐行核对）：

| 事实 | 位置 |
|---|---|
| `Spend` 先从 `earned` 扣、再扣 `brought` | `AdventureRules.cs:8-12` |
| 局内唯一获得入口 | `PlayerInventory.Add` → `AdventureFlow.GainMaterial`（`AdventureFlow.cs:224`） |
| 局内消费入口 | `PlayerInventory.TryRemove` → `Flow.SpendMaterial`（`PlayerInventory.cs:107-115`）；调用方含出口修复 `AdventureFlow.Exits.cs:32-33`、铭刻 `AdventureLoadout.cs:128`、`CraftingCosts.Pay`、`HeroEquipment.cs:39-40`、`CampRuntime.cs:91,112`、`CampWorkbenchRuntime.cs:14` |
| 不变量 | `broughtRemaining[k] + earnedRemaining[k] == checkpoint.materials[k]`（`AdventureValidation.cs:49`） |
| v9 存档只存"当前剩余" | 不存 `spent`、不存 `brought` 初值 |

因此 `gross = earnedRemaining + spent`，而 `spent` 与 `brought` 初值均未持久化，**零 schema 下无法从存档反解 gross**。

本批采用的投影（`ObjectiveEvaluator.Live`）：

```
gross[k] = max( EarnedRemaining[k] , 运行时单调计数[k] )
exact    = 运行时计数命中本局 runId 且本局确有获得
```

- 两项都 **≤ 真值**，所以**假阳性（虚报达成）在结构上不可能**；
- 唯一代价：重进一个"本局发生过消费"的局，`exact=false` 且进度取持久下界（低报）；
- `ObjectiveLedger` 只存在于内存（`[NonSerialized]` 语义），不写 `RunState`、不写 `Profile`、不写存档。

三条反例的落点：见 `ACCEPTANCE.md` 的 `goal-not-farmable` / `objective-no-regress` / `b0-12-exact-false`（均由真实 Player 断言给出）。

## 3. 九张目标卡与可达性

完整逐卡证据见 `OBJECTIVE_CARD_MATRIX.csv`（含 file:line 与最低产量保证）。要点：

| 卡 | 条件 | 最低产量保证 |
|---|---|---|
| `forest.gather` | 本局新获得 12 单位材料 | 森林 42 矿点（`ForestLayout.cs:33`），单点 3–6（`AdventureResource.HarvestMinimum/MaximumExclusive`）→ 4 点即可 |
| `forest.treasure` | 开 3 箱 | 6 个 POI 各 1 箱（`ForestRegionRuntime.cs:29`） |
| `forest.challenge` | 1 精英/首领 | 3 精英 + 2 首领（`ForestLayout.cs:39,50-51`） |
| `ruins.gather` | 2 箱 + 6 材料 | 箱产 Ore1–3 + 晶1、隐藏箱 Ore3 + 晶2（`RuinsExploration.Chest`）→ 2 箱 ≥4，配 2 普通敌（各 1 皮）= 6 |
| `ruins.treasure` | 机关链 4 步 | `lever→door→archive→hidden`（`RuinsExploration.CanUse:24`、`RuinsLayout.cs:50`）确定性，无随机 |
| `ruins.challenge` | 守护者 | `c1:guardian` 固定生成（`RuinsExploration.DropEnemy`） |
| `cavern.gather` | 3 矿脉 + 10 矿晶 | 4 矿脉（`CrystalCavernLayout.cs:60-61,123-124`），每点 3–6 |
| `cavern.treasure` | 矿室箱 + 对岸箱 | `c22:chamber:chest` / `c23:far-shore:chest`（`CrystalCavernLayout.cs:156,160`） |
| `cavern.challenge` | 晶脊守望者 | `c24:boss:crystal-warden`（`CrystalCavernLayout.cs:18,96-98`） |

**两处真实设计错误已修正**（并显式记录在 `DESIGN.md §3.2`）：遗迹 Gather 8 → 6；森林寻宝删除"或 1 件本局装备"。

未达成的目标不显示为可选目标：`ObjectiveCatalog.For(region, goal)` 只返回真实存在的卡；`PreparationObjectiveLine` 在测试模式显式返回"无地区目标卡"。

## 4. 实现清单（新增 5 文件 / 修改 7 文件，另有 5 个 `.meta`）

| 文件 | 类型 | 作用 |
|---|---|---|
| `Assets/CombatPrototype/ObjectiveCatalog.cs` | 新增 | 9 卡纯数据 + 地区身份卡文案 + 7 武器角色卡 + 目标查找 |
| `Assets/CombatPrototype/ObjectiveEvaluator.cs` | 新增 | P1-01 只读求值器：`Live/Saved/Evaluate`、`ObjectiveLedger`（内存单调计数）、D-08 投影 |
| `Assets/CombatPrototype/AdventureFlow.Objectives.cs` | 新增 | P1-04 结算前抓只读快照 + "下一局三件事" + 目标角标 |
| `Assets/CombatPrototype/RouteCards.cs` | 新增 | P1-03 Top3 结构化 + `exclusionReasons` 本地化，顺序 = `RouteScoring.Ranked` |
| `Assets/CombatPrototype/SkillTradeoffs.cs` | 新增 | P1-05 14 项取舍（8 扩展 + 6 新武器），无值显示"—" |
| `Assets/CombatPrototype/AdventureFlow.UI.cs` | 改 | 结算页加目标角标与三件事；准备页重排为"目标行 / 手持+角色 / 地区身份卡 / 规则 / 携带 / 材料 / 出征" |
| `Assets/CombatPrototype/PlayerHudPresenter.cs` | 改 | P1-02 目标卡按 **目标卡** 而非 mode 分支刷新（遗迹/洞窟不再被覆盖）；卡片 250×92→250×124；帮助页接入 7 武器角色卡 + 14 项取舍 |
| `Assets/CombatPrototype/WeaponSkillPanel.cs` | 改 | P1-05 `1/2` 热键（Field/UI 关闭/非死亡/非翻滚才生效，切换不释放技能）+ 统一槽位语义 |
| `Assets/CombatPrototype/AdventureLoadout.cs` | 改 | 铭刻"不可逆"文案统一为常量 `EngraveWarning` / `EngraveShort`（D-11） |
| `Assets/CombatPrototype/WeaponLoadoutView.cs`、`CatInventoryPresenter.cs` | 改 | 引用同一常量 + 武器行追加角色卡 + 技能取舍行 |
| `Assets/CombatPrototype/AdventureFlow.cs` | 改 | 只加两处记账钩子（`GainMaterial/SpendMaterial` 里调 `ObjectiveLedger`）+ 运行期 `BeginRun/Clear` + `LockOutcome` 首行 `CaptureObjectives` |

### 4.1 由真实证据暴露并修正的显示层缺陷（1 处）

第一轮 13 条 Run 全部通过后，逐条读结算文本时发现自相矛盾：

```
未竟：扫箱 已达成 · 待撤离 · 未开宝箱 3/6 · 剩余敌人 13
下一步：森林 · 拔点（换一种目标）          <-- 与上一行冲突
```

触发点：`AdventureFlow.Objectives.Suggest` 只在 `!conditionsMet` 时考虑"再来一次"，
条件已满足但撤离失败（死亡/放弃）时直接落到"换一种目标"分支，
与角标 `目标条件已满足但未成功撤离` 以及本批口径"条件满足 **且** 成功撤离才算达成"相矛盾。

修正（唯一改动，3 行 + 注释）：

```csharp
if (p.conditionsMet && !p.achieved)
    return "再来一次 " + p.regionLabel + " · " + p.title + "（条件已满足，只差成功撤离）";
```

修正后同一 Run 的真实结算文本：

```
未竟：扫箱 已达成 · 待撤离 · 未开宝箱 3/6 · 剩余敌人 13
下一步：再来一次 森林 · 扫箱（条件已满足，只差成功撤离）
```

该改动触发重编（`Assembly-CSharp.dll` `69423fc4…` → `ce03e641…`）并**全部 13 条 Run 重跑**，
上表所有数字均来自修正后的构建；旧构建的证据完整保留在 `Evidence/Player/_attempts/driver-bf1cc894-build69423fc4/`。

只读边界（可被 `evaluator-readonly` 断言证伪）：新增代码不调用 `AdventureRandom.*`、`DropLoot`、`Earn`、`CommitSettlement`，不写 `RunState`/`Profile`/存档，不改 `RouteScoring` 权重与排序。

## 5. 真实 Player 验证（见 `PLAYER_RUN_MATRIX.csv`）

每个 Run 均为真实 `WanxiangGuitu.exe` 进程（`-force-d3d12`、独立 `-wanxiang-storage-root`），记录候选 SHA、EXE SHA、驱动 SHA、PID、Run ID、命令行与原始日志。

共 13 条主 Run（含 3 组成对跨进程），全部 `PLAYER_RUN_COMPLETED`、`exitCode=0`、`complete.txt=PASS`，合计 **1465 PASS / 0 FAIL / 9 SKIP**。

- 构建身份：`Assembly-CSharp.dll` = `ce03e64171bd136b7549182d2985f8c50328c23ef2a06fb3777732f7bfa06d3c`
- 启动器 EXE = `001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a`（Unity 固定壳，不随脚本变化，见 §6 L6）
- 候选源码 SHA = `23d00cc8e`（`UX-PROGRESSION-01 P1 (1/3)`）：构建时工作树源码与该提交逐字节一致，其后只有文档与证据提交
- 驱动 = `49c81de5c4e8660340ec8cf8c2a5695892c18ec802b7c486ac56bb3133250695`
- 纯发行包 `result=Succeeded errors=0 warnings=113`；`RuntimeInitializeOnLoads.json` 中驱动引用 = 0
- 命令行（每条 Run 均记录在 `Player.command.json`）：`WanxiangGuitu.exe -logFile <root>/Player.log -screen-width 1280 -screen-height 720 -screen-fullscreen 0 -force-d3d12 -wanxiang-storage-root <root>`，环境 `UNITY_TEST_ROOT=<root>`

每地区满足「成功 + 失败各一」：森林（gather/success、treasure/death）、遗迹（gather/success、challenge/abandon）、洞窟（gather/success、treasure/abandon）。

| Run | 地区 / 目标 / 路径 | 判定 | exit | complete.txt | PID | 起始(UTC) | 时长 | PASS/FAIL/SKIP | Run ID | EXE SHA(16) | build SHA(16) | 驱动 SHA(16) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `p1-cavern-gather-success` | cavern / gather / success | PLAYER_RUN_COMPLETED | 0 | PASS | 38264 | 15:16:08 | 19.7s | 207/0/1 | `int02-711bb38a95334cabbd67a84b543f016c` | `001aeebfb92718f8` | `ce03e64171bd136b` | `49c81de5c4e86603` |
| `p1-cavern-treasure-abandon` | cavern / treasure / abandon | PLAYER_RUN_COMPLETED | 0 | PASS | 31824 | 15:16:29 | 9.2s | 205/0/1 | `int02-761148ba00654f0aa75f9aded6c96e6d` | `001aeebfb92718f8` | `ce03e64171bd136b` | `49c81de5c4e86603` |
| `p1-forest-counter` | forest / gather / counter | PLAYER_RUN_COMPLETED | 0 | PASS | 37848 | 15:16:39 | 19.1s | 61/0/1 | `int02-c6203c9745fd44028c558c3c09a80ac6` | `001aeebfb92718f8` | `ce03e64171bd136b` | `49c81de5c4e86603` |
| `p1-forest-gather-success` | forest / gather / success | PLAYER_RUN_COMPLETED | 0 | PASS | 35304 | 15:15:04 | 22.9s | 207/0/1 | `int02-6fb1d7975bac4fdfaf8d8c922b28819e` | `001aeebfb92718f8` | `ce03e64171bd136b` | `49c81de5c4e86603` |
| `p1-forest-treasure-death` | forest / treasure / death | PLAYER_RUN_COMPLETED | 0 | PASS | 39992 | 15:15:28 | 12.0s | 208/0/1 | `int02-30e85c6a3c0e445180883745fa96961f` | `001aeebfb92718f8` | `ce03e64171bd136b` | `49c81de5c4e86603` |
| `p1-ruins-challenge-abandon` | ruins / challenge / abandon | PLAYER_RUN_COMPLETED | 0 | PASS | 41328 | 15:15:57 | 10.6s | 214/0/0 | `int02-ed391ca917384668a37b77b417e2a64b` | `001aeebfb92718f8` | `ce03e64171bd136b` | `49c81de5c4e86603` |
| `p1-ruins-gather-success` | ruins / gather / success | PLAYER_RUN_COMPLETED | 0 | PASS | 41632 | 15:15:40 | 16.2s | 215/0/0 | `int02-fd2324dacf7a42d8bf7e316f2368028e` | `001aeebfb92718f8` | `ce03e64171bd136b` | `49c81de5c4e86603` |
| `p1-xproc-cavern-1` | cavern / gather / xproc1 | PLAYER_RUN_COMPLETED | 0 | PASS | 1504 | 15:17:33 | 9.6s | 22/0/1 | `int02-0cf92721074a466e9fc653ee18c22d49` | `001aeebfb92718f8` | `ce03e64171bd136b` | `49c81de5c4e86603` |
| `p1-xproc-cavern-2` | cavern / gather / xproc2 | PLAYER_RUN_COMPLETED | 0 | PASS | 30968 | 15:17:43 | 5.9s | 25/0/1 | `int02-80f21fcc7cfa4a5eab6b93f3937d4bfd` | `001aeebfb92718f8` | `ce03e64171bd136b` | `49c81de5c4e86603` |
| `p1-xproc-forest-1` | forest / gather / xproc1 | PLAYER_RUN_COMPLETED | 0 | PASS | 31920 | 15:16:58 | 11.4s | 22/0/1 | `int02-450b27a41a8e437eb5c6984c6c0f8e33` | `001aeebfb92718f8` | `ce03e64171bd136b` | `49c81de5c4e86603` |
| `p1-xproc-forest-2` | forest / gather / xproc2 | PLAYER_RUN_COMPLETED | 0 | PASS | 21700 | 15:17:11 | 6.4s | 25/0/1 | `int02-dc0defce703549a7b42027e35220e05f` | `001aeebfb92718f8` | `ce03e64171bd136b` | `49c81de5c4e86603` |
| `p1-xproc-ruins-1` | ruins / gather / xproc1 | PLAYER_RUN_COMPLETED | 0 | PASS | 39196 | 15:17:18 | 7.4s | 28/0/0 | `int02-7ee2f8aee51c4b78aef3b597946ff686` | `001aeebfb92718f8` | `ce03e64171bd136b` | `49c81de5c4e86603` |
| `p1-xproc-ruins-2` | ruins / gather / xproc2 | PLAYER_RUN_COMPLETED | 0 | PASS | 39096 | 15:17:26 | 6.2s | 26/0/0 | `int02-973df1663fb6466eb6576562146c6d76` | `001aeebfb92718f8` | `ce03e64171bd136b` | `49c81de5c4e86603` |

## 6. 已知限制与 SKIP

逐条列出为实现真实 Player 观察而引入的脚手架，以及本批确实没有覆盖的部分。

### L1 观察脚手架（只存在于 `Evidence/Tools/IntDriver.cs.txt`，不在发行包里）

| 脚手架行为 | 目的 | 边界（未做的事） |
|---|---|---|
| 采集 / 撤离期间把英雄血量补满（`Health.RestoreHealth`） | 让"显示与求值"断言不被游荡精英打断，避免把显示问题变成死亡结局 | 不改敌人 HP、伤害、AI 参数、仇恨范围；不改护甲与经验 |
| 用 `hero.RestorePosition` 直接走到"离所有存活敌人最远的可用出口" | 从采集点抵达出口，不必穿过刚被激怒的怪群 | **不搬动任何敌人**、不改世界边界、不改掉落/宝箱/随机流 |
| 材料获取 / 开箱 / 机关 / 撤离 / 结算 / 放弃全部调用产品自身 API | 断言作用于产品真实路径 | 驱动从不直接写 `RunState`/`Profile`/材料数组 |

**已被移除的错误脚手架（失败记录保留）**：早期版本用"把存活敌人推到 45–140m 外"来清空撤离区，
导致 `enemy:enemy:10@-71.597857,-129.998734,334` 越出 `ForestLayout.WorldBounds`，
存档校验抛 `存档字段不完整或超出范围`，进而 `saveFailed=True`、`begin-extraction-0..5` 与 `-commit` 连续 FAIL。
该方案已彻底删除（`P1PushEnemiesAway` 一并移除），改为纯路径选择；失败证据保存在
`Evidence/Player/_attempts/` 的历史目录中，未改写、未删除。

### L2 SKIP 的语义

9 次 SKIP 全部是 `p1-ruins-no-vein-notice`：该断言只对遗迹有意义（遗迹没有矿脉），
在森林/洞窟运行中被显式 `Skip(region=…)`。不是失败，也不是被忽略的缺口。

### L3 未逐武器切换手持做运行时验证

`1/2` 热键在 `NewWeaponRegistry.Is()` 的两种分支（新武器 2 槽 / 旧武器 3 槽）都有断言，
但单次 Run 只手持一件武器；7 件武器的槽位语义由源码 + `p1-weapon-roles-7` 角色卡共同覆盖，
没有为每件武器重新走一遍装备流程。B1-01 因此按"源码"判定记 PASS，并在此声明范围。

### L4 三张挑战卡的"击败"未在一次 Run 预算内完成

`forest.challenge` / `ruins.challenge` / `cavern.challenge` 在本次 13 条 Run 中只验证了
HUD 显示、进度读数与路线 Top3，精英/守护者/守望者未被击杀。达成语义由另外两条路径交叉覆盖：
`p1-ruins-challenge-abandon`（0/1 → `目标未达成`）与 `p1-forest-gather-success`（达成 + 成功撤离）。

### L5 跨进程对需要 `--allow-existing-root`

`xproc2` 必须在 `xproc1` 的同一个 run-root 上以"继续存档"启动，这既是产品语义也是证据前提；
`run_player.py` 默认拒绝复用目录，故第二段显式加 `--allow-existing-root`，并在 `Player.command.json` 留痕。

### L6 EXE SHA 不能单独标识构建

`WanxiangGuitu.exe` 是 Unity 固定启动器壳，改动脚本后其 SHA 不变（两次构建都是 `001aeebf…`）。
真正的构建身份是 `WanxiangGuitu_Data/Managed/Assembly-CSharp.dll`（驱动记录为 `buildSHA256`，
本批 `ce03e641…`，上一版 `69423fc4…`）。因此每次重跑都要同时核对 DLL 哈希，不能只看 EXE。
另：`ValidateBuild` 带"必须全新输出"门禁，旧 `Release` 目录存在时直接 `BuildFailedException: fresh output required`，
所以每次构建前把上一版目录改名留档（`I:/WGUP01/Build/Release-prev-<HHMMSS>`），不删除、不复用。

### L7 本批 NOT_RUN

- **视觉外观**（字体、对齐、颜色、可读性）：无图形夹具与截图，只断言 HUD 字段值与文案，像素级结果 `NOT_RUN`
- **人工游玩**：可读性与节奏未经人工确认
- **性能**、原生输入 U16、EDR：沿用历史 `NOT_RUN`
- **C-01 ~ C-05**（技能槽持久化、目标奖励与永久回执、遗迹矿脉、难度档 / 第 3 技能 / 单件升级 / 新武器配方、v10 schema）：按设计冻结

## 7. 本批明确未做（禁止项自查）

- 未新增/修改 v9、v10 存档字段；未动 `AdventureValidation`；未改 `AdventureRules.Spend` 语义。
- 未发目标奖励、未加货币、未改材料产出/消耗/配方成本、未改掉落率与宝箱概率。
- 未改随机流、未改 `RouteScoring` 权重与 `Ranked` 排序。
- 未改护甲/经验/武器伤害/技能冷却；未补遗迹矿脉、未加武器配方/单件升级/第 3 技能/难度档。
- 未修改用户场景、`ProjectSettings`、`Packages`、真实存档。
- **未进入 P2**，未做技能槽持久化（D-03），未动 settlement 回执字段（D-15）。
