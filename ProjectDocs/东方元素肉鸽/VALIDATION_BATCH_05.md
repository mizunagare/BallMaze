# B05 验收记录：V01～V22

日期 2026-10-23。工程 D:/unity/BallMaze/BallMaze；独立验证副本 C:/Users/guan/Documents/unitytest/MazeValidation。本次日志/截图/新流程及故障存档根目录 C:/Users/guan/Documents/unitytest/B05Validation；原模块回归沿用 C:/Users/guan/Documents/unitytest/T06Validation/regression 独立目录。规则、场景、实际构建分别执行，没有启用 CI 或升级 Unity/包。

## 环境和口径

Unity6000.6.5f1 (3ff58d469c8a)、Windows x64、URP17.6.0、InputSystem1.20.0、uGUI2.6.0。实际起点为已完成旧 T06 的 v7，本批增量到 v8。测试目录与玩家 persistentDataPath 分离；所有启动使用 batchmode，保存路径显式指向上述独立验证目录；原模块回归未改到真实玩家路径。

现有工程没有 Unity Test Framework 包，未安装/升级。NUnit Test Runner 为 NOT_RUN；规则由实际 Edit Mode executeMethod 工具执行，场景由实际 Play Mode 组件、时钟/输入/物理和断言执行。部分故障与容量采用明确夹具，不伪称人工长时间平衡试玩。原模块测试仅在 Editor 使用 LegacyHarness 隔离生命周期；另有完整启用 v8 的集成、UI 与 Player 测试。

## V01～V22

| ID | 结果 | 实际断言与证据 |
| --- | --- | --- |
| V01 | PASS | B05ScenarioCheck.Run.release.log：有敌人时完整定时撤离，收益装备一件/木材9，重复提交/读档仍一份；B05AdvancedCheck.Read.final.log 新 Editor 进程；Player 两进程永久状态一致 |
| V02 | PASS | Scenario 第5波 Boss 未死可启动5秒引导并成功；B05UICheck.Run.final.log 真实 E，击杀0/3仍能引导；独立 Player 也无需清场 |
| V03 | PASS | Scenario：背包暂停计时不动，受伤/出范围/再次交互取消，回 Running，同 Run 无结果无奖励 |
| V04 | PASS | Scenario：远处退出请求和旧 Camp.Enter 均不回营；H 与此统一入口，距离检查不能绕过；实际 H 输入补测另见 B05HInputCheck 日志 |
| V05 | PASS | Scenario：红护甲放入生效胸挂、新遗物背包穿戴后仍 RunLoot；死亡两件都丢失，原入场 ID 归还；RunLootWorn 截图 |
| V06 | PASS | Scenario + Advanced + EditChecks：本局来源优先消费，带入剩余守恒，已用药水不返，局内制作药水来源单独核算；Player 2瓶用后死亡剩1瓶 |
| V07 | PASS | Advanced：受保护法杖后端拒绝拆解，无铁矿收益；入场武器铭刻成本扣除，死亡恢复旧词缀但成本不退；EditChecks 成功保留实例修改、失败恢复原始快照 |
| V08 | PASS | B05LiveRegression.Run.log：原生 V、v8 同 Run 双槽/技能/普攻/切换冷却保存恢复、立即操作被拒；原 DualWeapon 回归验证暂停与弹体固有词缀快照 |
| V09 | PASS | Scenario 新红装与新容器未提前解锁配方，死亡不保留其所有权；现代 v8 恢复不调用旧装备补配方迁移；Player 新装备拾取后保存/恢复及最终配方集合检查 |
| V10 | PASS | Advanced 重复提交/重开/领取一次，物品/材料/待领取无重复；额外注入已存在的配方凭证接口验证重复凭证只解锁3个前置链ID，重复提交无新增；EditChecks 验证失败不提交凭证。没有新增正式凭证掉落源 |
| V11 | PASS | Advanced：同一更新引导结束请求与致死并发，统一 Death，后续不能改为成功 |
| V12 | PASS | B05CrashCheck 四阶段真实 Process.Kill：终局写盘前/后、结算提交前/后；四个新 Editor 读取过程均退出0且仅一份收益；另 Fault 钩子/写盘故障测试 |
| V13 | PASS | B05FaultCheck.Run.release.log 写盘失败重试、坏主档恢复 Pending 死亡备份；BlockedRecovery 双档坏时冻结、原字节保留、修复后重读；Consistency 待领取失败完整逻辑/运行时回滚 |
| V14 | PASS | Advanced 200件满仓收益进待领取，重读仍在、不可无限出征、满仓不能领取、背包可一次领取；UI 新进程200+2仍在，弃置需确认 |
| V15 | PASS | Scenario 补给6格满拾取失败保留地面物；CapacityEdges 满装备网格拾取保留、缩小容器失败恢复完整布局、药水产物空间不足不扣原料、铁矿一亿上限不吞拆解原装备；LiveRegression 旋转交换/掩码/迁移暂存 |
| V16 | PASS | Scenario/Advanced 主动放弃按失败结算；Player 正常退出后新进程恢复相同第三个 RunId、两次历史结算和1瓶药水，不自动成功/重开 |
| V17 | PASS | Player 实际采集节点归零、拾取、宝箱使用、完整保存再读；节点仍归零、宝箱仍已用不能重复；B05Consistency 核对人物材料、装备ID、敌人血量、资源、事件、掉落和随机状态同边界 |
| V18 | PASS（标明样例来源） | LegacyMigration v1～v6独立样例逐版本守恒/原字节备份/重读；V7Migration camp/run/pending/committed 四样例保存v8，保留Profile/Run/来源/终局/去重，不重发 |
| V19 | PASS | LegacyMigration：未知来源只保护迁移时已有物；新矿7个死亡丢失；旧已有材料剩余保留，不伪造胜利/徽章。v7已知来源沿用，未全量升级新战利品保护 |
| V20 | PASS | B05LoadFailureCheck.Run.release.log：出征初始化失败退营；同时营地回退失败则冻结/禁保存，原文件逐字节不变；修复后恢复唯一营地；提交后营地初始化失败保留 Committed，重试不发第二次；Fault 另验证出征写盘失败 |
| V21 | PASS | 原四批模块回归全执行，见下；另 v8 生命周期集成验证，非只用旧测试模式宣称新流程通过 |
| V22 | PASS | Advanced：原无尽模式第5波后进第6波；冒险测试真实攻击杀掉第5波 Boss 后也能进第6波，再主动撤离；正式badges/regions仍空；准备页两独立入口和目标标签可见 |

V12 写入进程退出 -1 是预期强制终止，不是忽略失败：必须有对应 kill-marker，且独立 ReadBeforeLock/ReadAfterLock/ReadBeforeCommit/ReadAfterCommit 各日志含 PROCESS_KILL_RECOVERY_PASS、退出0，才算通过。前终局写盘恢复最近完整检查点（可能仍在引导），后写盘恢复唯一 Pending；提交后恢复 Committed，不重抽/重发。

V20 当前架构复用同一 ForestRuins 场景，营地用现有暂停/场景内容装载，而非异步切换第二张地图。故测试的是这些实际世界初始化/回营装载边界，不宣称已做跨区域加载；跨区域在 B09。

## 四批模块回归

final-runner.txt 中以下过程均退出0：

- T06RegDualWeaponCheck.Run：原生 V、暂停、锋锐/汲取/处决/蓄能、四武器×五品质20技能路径、铭刻/弹体快照；B05Consistency 补疾速实际间隔与回响实际命中。
- T06RegDualGameplayRegression.Run：四武器实际攻击/技能、资源采集、Boss/宝箱掉落。
- T06RegWorkbenchCheck.Run/Read：29高级配方/前置链、18基础装备、基础容器、少材料/满包/写盘失败/重复解锁不扣费，跨进程永久进度。
- T06RegProgressionRuntimeCheck.Run：六基础技能、击杀经验一次、唯一三选一/排队、暂停/装备叠加/伤害。
- WorldEventsRuntimeCheck.Run：E最近目标、距离/遮挡、宝箱、祭坛与一次奖励。
- PotionRuntimeCheck.Run：真实Q、配方/上限、背包冷却暂停、使用与死亡。
- AutoWaveRuntimeCheck.Run：默认倒计时、技能/背包暂停、自动波次、死亡停止。
- HeroDodgeRuntimeCheck.Run：真实空格、移动距离、无敌/后摇、冷却/暂停。

B05LiveRegression 直接复用第一批网格控制器断言：定义/实例、品质形状、拖放旋转交换取消、三种胸挂/三种背包模板、容量缩小/掩码与被动效果，另在完整 v8 中研究制造后死亡保留配方。

## 本地构建与 Player

StandaloneWindows64 Development，ForestRuins 为明确构建入口。B05BuildCheck.Build.verified.log 和 BuildSummary.txt 记录实际结果；不以编译代替运行。

实际运行驱动 B05SmokeDriver 仅存在于验证副本，使用 -b05-smoke/-b05-read 和 B05Validation/player-profile。未安装到产品 Assets。不是玩家调试按钮；玩家实际入口由原生 UI 测试覆盖。

Player-smoke.final.log / Player-read.final.log、PLAYER_FULL_LOOP.txt / PLAYER_RESTART.txt：营地出征→移动/攻击→树木采集与拾取→装备材料→开箱→完整检查点恢复（不重开箱/资源）→存活敌人时5秒撤离→统一结算→回营装备/材料存取与制造→再出征→新红护甲穿戴→使用带入药水→死亡结算→回营→第三次出征带新矿3→正常退出→新进程继续相同Run。仓库1件、历史结算2次、药水1瓶、第三个Run未结算；最终数据与显示一致。

一名活跃AI测试敌人布置在感知范围外，其余受控以隔离存档验证；场景测试中的Boss/截图敌人也有明确夹具冻结。证据证明规则允许活敌撤离，不冒充真实长时间AI压力/平衡试玩。没有正式种子地图可测。

## 真实运行证据

screenshots/ 内每类 720p/1080p PNG 及记录修订/Run/数量的 txt：

| 类别 | 文件名前缀 |
| --- | --- |
| 出征清单/模式/目标/补给6格 | Departure |
| 敌人仍活（0/3）时5秒引导 | ExtractionCountdown |
| 新护臂已在生效区，标明死亡丢失 | RunLootWorn |
| 成功带回1装备/9木材 | SuccessSettlement |
| 死亡损失1装备/4晶石 | DeathSettlement |
| 仓库200/待领取2 | FullWarehousePending |
| 独立新进程恢复200+2 | RestartRestoredPending |

B05UICheck.Run.final.log/Restart.final.log：实际原生IMGUI按钮与E输入，种子物资和敌人位置/暂停由夹具设置，不是设计图。首次截图发现HUD叠到完整背包上，已修复并确认；不将占位图当运行证据。

## 失败、限制与 NOT_RUN

- 首次旧迁移测试在补给恰满的 v1 夹具直接加新铁矿，容量正确拒绝，旧断言误当保护丢失而失败。已先实际消耗旧皮腾格再采新矿，v1～v6重跑通过；原始失败日志保留。
- UnityEditor.Search.SearchDatabase 启动时既有 ArgumentOutOfRangeException 在验证副本仍出现；未删除用户 Library 掩盖，最终 Player 不出现。既有 FindObjectsByType/排序等过时警告保留，故不声称所有编辑器日志零异常。
- 故障测试 IOException 为主动注入的预期，必须断言未发奖/不覆盖/重试一致才判 PASS。
- NUnit Test Runner：NOT_RUN（工程未安装包，已有工具实际覆盖规则/场景）。
- 用户真实各版本私人历史档全面覆盖：NOT_RUN；v1～v6 为有各版依据的历史合成档，v7为本批修改前捕获的隔离运行档，不冒充用户实际档。
- 人工长时间流派平衡、非Windows平台、真实断电、防手工篡改/回滚：NOT_RUN，不宣称已实现。
- V23～V40：NOT_RUN，属于 B06～B13。正式森林路线、双Boss/跨局徽章、天气谜题与后续区域仅更新路线图，没有假场景/占位按钮。
- 当前随机状态仍复用既有完整快照；五类随机流隔离、配置化生成/真实路线通行验证在B06，不以本批固定场景冒充已完成。
- 恢复是完整检查点，飞行弹体/攻击前摇重置；强退不保证最后未写盘步骤。

## 复跑与交付位置

B05Validation/run-checks.ps1、run-advanced.ps1、run-final.ps1、run-release.ps1 保留实际命令与日志。脚本为本机绝对路径，故障夹具禁止指向玩家真实目录。产品代码、迁移、路线与本报告配套交付；无 Git 提交、无 CI、无引擎升级。

## 最终构建和原工程确认

最终构建实际值：

```text
Succeeded
errors=0
warnings=43
bytes=184070373
duration=00:00:11.4175503
```

两个最终 Player 进程退出0，无运行时异常；player-data-assertions.txt 独立读取最终 v8 数据，断言同一未结算 Run、历史2次且无重复、仓库1件、剩余药水1、本局新矿3、无提前解锁配方。

H原生输入补测 B05HInputCheck.Run.final.log 退出0：远处H不回营、合法H开始引导、再次H取消不发奖。首次断言误要求启动同一Update扣时后仍严格等于5，改为实际计时范围后重跑通过，未改产品行为。

原工程安装16个运行时文件差异（1个新partial文件，15个适配），现有每个文件安装前都匹配B05ChangeBackup的SHA256；安装后逐一与实际验证副本字节一致。未覆盖项目设置/场景/美术/用户改动，验证驱动和Editor工具未安装进产品Assets。另执行原工程 Unity -batchmode -quit 编译成功退出0，无C#编译错误，日志ActualProject-Compile.log。安装清单InstalledFiles.json。
