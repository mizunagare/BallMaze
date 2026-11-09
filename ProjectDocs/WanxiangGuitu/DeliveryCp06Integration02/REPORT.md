# CP06-INTEGRATION-02 · 统一候选真实 Player 纵向集成验证报告

> 验证分支 `verify/cp06-integration-player-01`（自 `integration/cp06-playable-candidate` tip
> `2964ad7413d2644f23c12a8c82e1d439e2884a01` 建立）。
> 本批次**零产品源码改动**：仅新增验证工具与文档。所有历史 FAIL 原样保留，不改写为 PASS。
>
> **R1 修订（`verify/cp06-integration-player-02-R1`）**：本报告出现的一切计数
> 只来自 [RUN_LEDGER.csv](RUN_LEDGER.csv) 单一来源（由 `Evidence/Tools/r1_ledger.py`
> 机械生成）。R1 做了三件事：①R1-01 统一 24 个**原始** Run 的分类（旧 14/12/12 三处
> 矛盾见 [ERRATA.md](ERRATA.md)）；②R1-02 追加 8 个「弓自然释放」Run 并给出真实
> 输入证据（见 §3.4）；③R1-03 给出森林 Run ID 的原始来源
> （[FOREST_RUN_ID_PROVENANCE.md](FOREST_RUN_ID_PROVENANCE.md)，结论 **DIRECT**）。
> 因此全文口径为 **32 个独立 Player Run = R0 24（13 PASS / 11 FAIL）+ R1-02 8（4 PASS / 4 FAIL）**。

## 1. 范围与方法

对统一候选执行 INT02-01～06 六个重点的真实验证：

1. **INT02-01 构建身份**：候选纯发行构建 + 隐私门禁 + 确定性 SHA（见 [PLAYABLE_CANDIDATE_BUILD.md](PLAYABLE_CANDIDATE_BUILD.md)）。
2. **INT02-02 三地区完整出征循环**：森林 / 古代遗迹 / 水晶洞窟各一条「营地→出征→真实战斗→采集→撤离→结算→回营→再出征」循环（[THREE_REGION_RUN_MATRIX.csv](THREE_REGION_RUN_MATRIX.csv)）。
3. **INT02-03 跨地区状态切换 + 跨进程在途恢复**（[CROSS_REGION_STATE_MATRIX.csv](CROSS_REGION_STATE_MATRIX.csv)）。
4. **INT02-04 七武器与八技能真实输入组合冒烟**（[WEAPON_SKILL_SMOKE_MATRIX.csv](WEAPON_SKILL_SMOKE_MATRIX.csv)）。
5. **INT02-05 奖励→制造→结算→回营→再次出征**（reward-loop-2）。
6. **INT02-06 失败路径与用户文件保护**（fail-paths-2）。

方法约束（全部遵守）：

- 未合并任何 feature 分支（验证分支直接自候选 tip 建立）。
- 未修改经济、掉落、随机流、XP、护甲、武器数值、v9、地图布局或用户文件。
- 完整游戏循环全部经真实业务入口（标题确认/继续 → `Flow.Depart` → `Combat.Strike` →
  `InteractionResolver.Execute` → `Flow.BeginExtraction` → `Flow.CommitSettlement` →
  `Flow.AcknowledgeSettlement` → `Loadout.Craft` → 再次 `Flow.Depart`）。
- 英雄仅做**摆位**（`RestorePosition`/`PinHero` 瞬移到目标相邻处，属即时位姿修正，非场景
  加载），战斗伤害、矿脉采空、掉落拾取、结算入账全部为真实产品逻辑产生。
- 每个 run 独立隔离 run-root + 存储根（`-wanxiang-storage-root`），禁止跨 Run 拼接。

## 2. 验证基础设施（本批新增，交付于 Evidence/Tools/）

| 工具 | 作用 |
|---|---|
| `build_driver.py` | 用 Unity Roslyn 编译 `IntDriver.cs.txt` → `CavernValidationDriver.dll`，仅注入观察副本的两个 JSON 清单（防重复注入守卫） |
| `IntDriver.cs.txt` | sidecar 驱动：`[RuntimeInitializeOnLoadMethod]` 启动，读 `cavern-test.txt` 选模式，全部断言/事件带身份三元组（runId/processId/buildSha），`complete.txt`/`failure.txt` 判定 |
| `run_player.py` | 创建隔离 run-root（拒绝复用/拒绝覆盖证据目录；跨进程场景提供 `--allow-existing-root` 预置存档通道）、直启 exe、归档全部原始输出 |
| `r1_ledger.py` | **R1-01**：只读 `Evidence/Player/<run>/` 原始文件，机械生成 [RUN_LEDGER.csv](RUN_LEDGER.csv) 与 `r1-ledger-summary.json`，并做「runId 唯一 + 分类闭合」双重校验 |

纯构建（`I:/WGInt02Release/Release`）与观察副本（`I:/WGInt02Obs/Release`）物理分离；
每次源码迭代重编译前，从纯构建重置观察副本清单（保持「纯包零验证注入」不变式）。

## 3. 结果总览（32 个 Player run：R0 24 + R1-02 8）

> 计数唯一来源 [RUN_LEDGER.csv](RUN_LEDGER.csv)：32 行 / 32 个唯一驱动 runId /
> 17 PASS / 15 FAIL / 0 INCOMPLETE，分类闭合（32 = 17 + 15）。
> 其中 `phase=R0` 子集为 13 PASS + 11 FAIL，与 R1-01 结论一致。

### 3.1 通过的关键 run（R0 13 个 + R1-02 4 个 = 17 个 PASS）

| run | 模式 | 结果摘要 |
|---|---|---|
| forest-loop-6 | 森林完整循环 | 完整出征循环通过（29 断言 0 FAIL）；**旧 INDEX 误将其列入失败表**，见 [ERRATA.md](ERRATA.md) §3；被 forest-loop-7 取代 |
| forest-loop-7 | 森林完整循环 | 敌人 45→0 击杀（33 真实伤害）、Wood 采集→拾取 4、Extracted、commit/ack、再出征新 runId |
| ruins-loop-3 | 遗迹完整循环 | c1:guard 60→0 击杀、采集 **SKIP**（遗迹按设计无活跃矿脉）、Extracted、再出征新 runId |
| cavern-loop-1 | 洞窟完整循环 | watcher 60→0 击杀、Ore 采集→拾取 6（重复拾取被拒）、Extracted、再出征新 runId |
| cavern-boss-1 | Boss 交战 | 真实挑战交互→Boss 受击 33→合法撤离 Extracted |
| cross-region-chain-1 | 跨区链 | 三地区连续出征循环，各 runId 独立、区域身份正确（森林 Death 为合法战果） |
| xproc-1 / xproc-2 | 跨进程恢复 | 进程 1 中途存档退出→进程 2 经真实 Continue() 恢复同一 run（runId/region/instance/seed 全一致） |
| weapon-smoke-2 | 七武器 | 全部 7 武器 select+Strike+released 通过 |
| skill-smoke-3 | 八技能 | 两地区双槽技能+弓蓄力+法杖符阵弹体全通过 |
| reward-loop-2 | 奖励制造循环 | 森林 Wood4+Stone5、洞窟 Ore3+Crystal4 采集→撤离结算→**真实制造白品剑**（items 8→9）→再出征 |
| fail-paths-2 | 失败路径 | 撤离阻断拒绝、真实致死→Death 结算→区域卸载→ack 回营→再次出征、隔离存档 |
| reward-loop-1 | 奖励循环（材料不足版） | **场景 PASS，但 `crafted=False`**：单区出征材料不足以覆盖白品配方，**不代表制造成功**；被 reward-loop-2 取代 |
| **bow-pierce-natural-8**（R1-02 采信） | 弓蓄势贯矢自然释放 | 半蓄力 + 满蓄力两发均由真实松键释放，各唯一 release/唯一 spawn，各贯穿 2 目标（60→5.43→0），冷却 10.17s 且冷却期施放被拒，两发弹体均自然销毁（见 §3.4） |
| bow-pierce-natural-4 / -6 / -7 | 弓自然释放（过程 Run） | 同一链路的早期通过 Run，断言集较窄（-4 多目标为 SKIP、-6 目标列表未记录、-7 第二发因产品冻结提前收尾），均被 natural-8 取代 |

### 3.2 保留的失败历史（15 个 FAIL run = R0 11 + R1-02 4，不改写）

| run | 失败断言 | 根因（均为驱动侧问题或产品真实行为，非候选缺陷） |
|---|---|---|
| forest-loop / -2 | real-damage damage=0 | 距离 2.43m 超出 1.8m 近战半径（未摆位相邻） |
| forest-loop-3 | began=0 dist=1.10 | 删除一次性 RestorePosition 导致出征遗留 stale 战斗状态阻塞 Ready |
| forest-loop-4 / -5 | began=0 | **同帧 `PlayerInput.Focus()`+`Strike()`**：Focus 内部 `Barrier()` 置 `barrier=frameCount`，使 `UIBlocked=true`、`Ready=false` —— 诊断确认 uiBlocked=True 为唯一阻塞项 |
| ruins-loop / -2 | vein-present | 遗迹真实无活跃矿脉（`BuildRuins` 隐藏全部场景内 AdventureResource 且不重建）；第一次读到 MonsterHide 为时序巧合 |
| weapon-smoke-1 | strike-Sword | 出征过渡帧内首次攻击被瞬态 Ready 条件拒绝（后续武器全过） |
| skill-smoke-1 | skill-use-cavern-s2 | 双技能槽共享同一冷却（`PrepareExpanded` 置 `skillAt`），未等待即施放被产品**合法拒绝** |
| skill-smoke-2 | staff-projectile-forest | 驱动弹体计数器锁定首个 AttackId，跨地区新弹体被过滤（洞窟通过、森林误报 FAIL） |
| fail-paths-1 | forest-depart（第二次） | 死亡结算后未调用 `AcknowledgeSettlement()`，`HasResult` 未清 → `DepartureReason` 合法拒绝出征（产品行为正确） |
| bow-pierce-natural-1（R1-02） | bow-pierce-contact-1 contacts=0,blocked=1；bow-cooldown-active-1 remaining=0 | 驱动用敌人自身 Y 取射击点 → 英雄被放到地形以下（`pierce-spawn y=-3.44`），弹体撞地；且冷却断言置于 5s 飞行等待之后 |
| bow-pierce-natural-2（R1-02） | bow-muzzle-height muzzle.y=0.3128 | 驱动假设弓 Muzzle 在胸口（+0.6m），产品弓弦源实际约 +0.30m；改为相对地面判定 |
| bow-pierce-natural-3（R1-02） | bow-charging-2 timeout=5 | 第二次施放前未重新 `PlayerInput.Focus(true)`，11s 冷却后按键无 Down 边沿 |
| bow-pierce-natural-5（R1-02） | bow-projectile-lifecycle-2 timeout=8 | 生命周期等待未考虑产品在 `Time.timeScale==0`（升级选卡/死亡 Freeze）时**按设计冻结弹体**；重复命中用跨弹体全局计数亦误判 |

> `reward-loop-1` **不属于**本失败集合（`complete.txt=PASS`、exit 0、37 断言 0 FAIL）；
> 旧 §3.2 把它列在失败表内并标「（非 FAIL，但 crafted=False）」，是旧「14 个 FAIL」
> 的主要来源之一。现已移入 §3.1 并记 `ACCEPTED_SCENARIO_ONLY`，详见 [ERRATA.md](ERRATA.md) §2。

### 3.3 遗迹采集 SKIP 的定性说明

`ForestRegionRuntime.BuildRuins`（`ForestRegionRuntime.Ruins.cs:23`）隐藏场景内全部
`AdventureResource` 且遗迹构建不再实例化资源节点——遗迹地区在候选中**按设计不提供可采集
矿脉**。驱动按 `Skip`（NOT_APPLICABLE）记录，其余循环步骤（战斗/撤离/结算/再出征）均为
真实执行。此为候选的产品事实，非验证缺口。

### 3.4 R1-02 · 弓蓄势贯矢「自然释放」真实输入证据（bow-pierce-natural-8）

采信 Run：`bow-pierce-natural-8`（`complete.txt=PASS`、exit 0、**56 断言全 PASS / 0 FAIL / 0 SKIP**）。
身份三元组：driver `runId=int02-b26ff2947c5a431696f3adf586cda690`、`processId=37188`、
`buildSha=4ce1624c77141e2da6878c29082b8e62e7ac26a5cce3b03518a201992fb4a4e3`。

输入方式：真实 `KeyboardState` 事件（`InputSystem.QueueStateEvent`，绑定键 `F`）**按住、
保持、松开**，全程未调用 `CancelSequence()`，也未直接调用 `Release()` API——同 Run 内
`bow-no-manual-cancel-1/-2` 以 `cancelDelta=0` 直接证明。

| 阶段 | 帧 | 观测值（原始事件） |
|---|---|---|
| 选中弓 + 点击产品技能槽按钮 `技能槽2` | — | `bow-slot-selected`、`bow-slot-skill`：`expanded.Selected=2`、`Definition.id=bow.pierce`、`charge=1,startup=0.3,cooldown=11` |
| 瞄准（相机固定点迭代 + 弹道预演） | 219 | `actualLateral=0.3488`，目标 `enemy:2`、次目标 `enemy:4` |
| 第一发：按下 F → Charging | 222 | `start bow.pierce attack=1`，`bow-charging-1`、`bow-held-input` |
| 半蓄力后**真实松键** | 304 | `skill-key-up heldSeconds=0.511 chargeFractionAtKeyUp=0.504` |
| 蓄力锁定 | 305 | `charge-locked charge=0.515`（`elapsed>=def.startup` 且已松键） |
| 释放（唯一） | 349 | `release attack=1`、`bow-release-unique-1 bowReleases=1`、`cancelDelta=0` |
| 弹体生成（唯一） | 349 | `pierce-spawn projectileId=pierce:1` |
| 冷却（真实） | 349 | `bow-cooldown-active-1 remaining=10.1749`（cd=11s，飞行未消耗判定窗口）；冷却期 `combat.UseSkill()` 被拒（`bow-cooldown-refuses-cast-1`） |
| 贯穿命中 1 | 413 | `pierce-contact target=enemy:2 collider=CharacterController:野猫盗匪 hp 60→5.4279 damage=54.572` |
| 贯穿命中 2 | 437 | `pierce-contact target=enemy:4 hp 60→5.4279 damage=54.572`（同一 attack=1 的第二目标） |
| 弹体生命周期 | 661 | `lifecycle-end remainingPierceObjects=0, paused=False, timeScale=1` |
| 第二发：满蓄力 | 840 | `charge-locked charge=1.0` = `def.charge`（`bow-max-charge-2`），持续按住直至产品上限 |
| 释放 + 生成（各唯一） | 888 | `release attack=2 charge=1.0`、`pierce-spawn projectileId=pierce:2`、`cancelDelta=0` |
| 贯穿命中 3/4 | 928 / 954 | `hp 5.4279→0`（`enemy:2`）、`hp 5.4279→0`（`enemy:4`） |
| 产品冻结 | 956 | `lifecycle-end remainingPierceObjects=1, paused=True, timeScale=0, progressionChoosing=True`——升级选卡使全局时间停止，产品**按设计**不再推进弹体 |
| 选卡后恢复 | 958 | `choice-resolved-for-lifecycle choices=1`（`HeroProgression.SelectChoice`，与玩家点卡同一入口） |
| 弹体销毁 | 1225 | `lifecycle-end-resumed remainingPierceObjects=0, paused=False, timeScale=1` |

合同核对结论：

- **唯一性**：每发只产生 1 次 `bow.pierce release` + 1 次 `pierce-spawn`（`bow-release-unique-1/-2`、`bow-pierce-spawn-once-1/-2`）。
- **贯穿**：单发弹体在同一 `attack` 内依次命中 2 个不同目标（`pierceChain=2[enemy:2/enemy:4]`），产品上限 3；`bow-pierce-once-per-target-1` 以 `perProjectileRepeats=0` 证明**同目标不重复命中**。
- **伤害**：同一目标各结算一次（54.572 / 5.4279），HP 前后均有原始事件可核。
- **冷却 / 技能状态**：release 后 `remaining=10.17s`，冷却期施放被产品拒绝，结束时 `expanded.Busy=False`。
- **弹体生命周期**：存活 ≤2.5s / 访问 ≤3 目标后销毁，两发均观测到 `remainingPierceObjects=0`。

**未冒充项**：驱动会为弹道把英雄瞬移到射击点（`RestorePosition`，受控导航，会顺带清空冷却），
因此真实冷却断言被放在**任何摆位之前**；两发之间不重跑完整循环、不重建 Player。

## 4. 保护与边界（INT02-06）

- **用户文件**：`git status` 仅 `?? ProjectDocs/…/DeliveryCp06Integration02/`（本交付目录），
  零已跟踪文件改动；产品源码、场景、ProjectSettings、v9 全部未触碰。
- **真实存档隔离**：全部 32 个 run 的存档均写入各自 `I:/WGInt02Runs/<run>/WanxiangGuitu/…`
  （`fail-isolated-save` PASS：savePath 不含 AppData）；真实用户 AppData 存档目录从未被读写。
- **纯构建不变式**：验证驱动只存在于观察副本；纯构建清单 0 验证条目；观察副本每次重编译
  前从纯构建重置。
- **不合并、不丢弃**：未合并 feature 分支，未丢弃任何历史分支/历史 FAIL。

## 5. 风险与限制

1. 遗迹采集为 SKIP（见 §3.3）——遗迹地区的资源供给设计需产品侧决策，本批不修改。
2. 英雄摆位为瞬移（`RestorePosition`/`PinHero`），真实移动/寻路不在本批范围（历史批次已覆盖）。
3. **弓蓄力已由「手动 `CancelSequence` 收尾」升级为真实松键自然释放**（R1-02，见 §3.4）：
   半蓄力（松键 0.504）与满蓄力（1.0）两发均有唯一 release、唯一 spawn、贯穿、逐目标 HP 与
   弹体销毁证据。`skill-smoke-3` 的手动取消证据**保留不改写**，仅作历史记录。仍未覆盖的是
   「人工试玩主观感受」与「蓄力过程中被敌人打断/取消」的组合路径。
4. 人工观感 / 可读性 / 最终打击感维持 `NOT_RUN`，与各历史交付口径一致。
5. 森林完整循环的战果出现过 Death（游荡敌人击杀采集中的英雄）——合法战果，非缺陷；
   cross-region-chain 中森林轮同样以 Death 结算，证明死亡路径在正常循环内闭环。
6. 弹体在 `Time.timeScale==0`（升级选卡 / 死亡 Freeze）时**按设计冻结**、不推进也不销毁；
   R1-02 已用「产品自身选卡入口恢复后继续飞行直至销毁」的证据区分「产品暂停」与「弹体泄漏」。

## 6. 复现

见 [TESTING.md](TESTING.md)；证据索引见 [Evidence/INDEX.md](Evidence/INDEX.md)。
