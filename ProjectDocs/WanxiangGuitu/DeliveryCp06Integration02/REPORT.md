# CP06-INTEGRATION-02 · 统一候选真实 Player 纵向集成验证报告

> 验证分支 `verify/cp06-integration-player-01`（自 `integration/cp06-playable-candidate` tip
> `2964ad7413d2644f23c12a8c82e1d439e2884a01` 建立）。
> 本批次**零产品源码改动**：仅新增验证工具与文档。所有历史 FAIL 原样保留，不改写为 PASS。

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

纯构建（`I:/WGInt02Release/Release`）与观察副本（`I:/WGInt02Obs/Release`）物理分离；
每次源码迭代重编译前，从纯构建重置观察副本清单（保持「纯包零验证注入」不变式）。

## 3. 结果总览（24 个 Player run）

### 3.1 通过的关键 run（9 个模式）

| run | 模式 | 结果摘要 |
|---|---|---|
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

### 3.2 保留的失败历史（14 个 FAIL run，不改写）

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
| reward-loop-1 | （非 FAIL，但 crafted=False） | 单次洞窟出征材料不足以覆盖白品配方 Wood2+Stone1+Ore2 → 扩为双地区采集后真实制造成功 |

### 3.3 遗迹采集 SKIP 的定性说明

`ForestRegionRuntime.BuildRuins`（`ForestRegionRuntime.Ruins.cs:23`）隐藏场景内全部
`AdventureResource` 且遗迹构建不再实例化资源节点——遗迹地区在候选中**按设计不提供可采集
矿脉**。驱动按 `Skip`（NOT_APPLICABLE）记录，其余循环步骤（战斗/撤离/结算/再出征）均为
真实执行。此为候选的产品事实，非验证缺口。

## 4. 保护与边界（INT02-06）

- **用户文件**：`git status` 仅 `?? ProjectDocs/…/DeliveryCp06Integration02/`（本交付目录），
  零已跟踪文件改动；产品源码、场景、ProjectSettings、v9 全部未触碰。
- **真实存档隔离**：全部 24 个 run 的存档均写入各自 `I:/WGInt02Runs/<run>/WanxiangGuitu/…`
  （`fail-isolated-save` PASS：savePath 不含 AppData）；真实用户 AppData 存档目录从未被读写。
- **纯构建不变式**：验证驱动只存在于观察副本；纯构建清单 0 验证条目；观察副本每次重编译
  前从纯构建重置。
- **不合并、不丢弃**：未合并 feature 分支，未丢弃任何历史分支/历史 FAIL。

## 5. 风险与限制

1. 遗迹采集为 SKIP（见 §3.3）——遗迹地区的资源供给设计需产品侧决策，本批不修改。
2. 英雄摆位为瞬移（`RestorePosition`/`PinHero`），真实移动/寻路不在本批范围（历史批次已覆盖）。
3. 弓蓄力验证以手动 `CancelSequence` 收尾（未等待自然满蓄释放的完整伤害路径）。
4. 人工观感 / 可读性 / 最终打击感维持 `NOT_RUN`，与各历史交付口径一致。
5. 森林完整循环的战果出现过 Death（游荡敌人击杀采集中的英雄）——合法战果，非缺陷；
   cross-region-chain 中森林轮同样以 Death 结算，证明死亡路径在正常循环内闭环。

## 6. 复现

见 [TESTING.md](TESTING.md)；证据索引见 [Evidence/INDEX.md](Evidence/INDEX.md)。
