# T06 本地验收记录

日期：2026-10-23。最终结论：A01～A19 在本报告列出的原型规则、合成旧档与故障模型下 PASS。没有使用用户真实存档进行损坏、清空或故障注入。没有 GitHub Actions/CI，也没有 Git 提交。

## 环境与方法

- 实际工程：`D:/unity/BallMaze/BallMaze`；验证副本：`C:/Users/guan/Documents/unitytest/MazeValidation`。
- Unity 6000.6.5f1 / Windows x64 / URP 17.6.0 / Input System 1.20.0 / uGUI 2.6.0，原版本不升级。
- 所有下列日志、测试存档和证据根目录：`C:/Users/guan/Documents/unitytest/T06Validation`。
- 规则测试实际在 Edit Mode `-executeMethod T06EditChecks.Run -quit` 执行。Play Mode 工具打开 ForestRuins 后 EnterPlaymode，用真实场景组件、定时更新、输入事件或明确标注的夹具布置断言。不将编辑源码等同于运行通过。
- 原项目没有 Unity Test Framework 包：其 NUnit Test Runner 流程为 **NOT_RUN**，没有为此安装/升级包；对应规则与场景测试通过现有 Editor 执行工具实际运行。
- 旧回归工具中，仅编辑器的 LegacyHarness 可隔离新生命周期来执行原模块断言；另有启用完整 v7 生命周期的 T06LiveRegression、Matrix、Consistency、Fault、UI 及 Player 运行验证，不以旧模式单独证明闭环。

## 验收矩阵

| ID | 结果 | 实际证据/断言 |
| --- | --- | --- |
| A01 | PASS | T06MatrixCheck.Run.fixed.log、Read.fixed.log；真实拾取/定时撤离/回营，独立 Unity 进程重读；Player 两进程亦通过 |
| A02 | PASS | Matrix：武器、胸挂、背包等入场 ID/布局全部归还；新制造/拾取实例丢失；之前仓库物品仍在 |
| A03 | PASS | Matrix + EditChecks：材料穷举先花本局来源；局内制作并使用药水；失败仅返还带入剩余；铭刻成本不返还 |
| A04 | PASS | Matrix 同 Run 保存读取再放弃；Consistency 核对材料、装备 ID、敌人血量、资源、事件、掉落和随机状态同边界恢复；正常退出的 Player 跨进程存档读取 |
| A05 | PASS | Matrix 重复提交/重开结算；同 Run 去重记录一次、物品仅一份；待领取重复领取拒绝 |
| A06 | PASS | T06FaultCheck.Run.release.log：终局保存前/后、结算写盘前/后钩子注入中断，再从磁盘恢复；Pending/Committed 一致 |
| A07 | PASS | Matrix：撤离成功请求与同更新致死并存，唯一 Death；测试目标实际战斗完成另见 A18 |
| A08 | PASS | Matrix：仓库 200，收益进待领取，读档仍在、阻止出征、满仓不能领、背包可一次领取；Consistency 验证领取写盘失败完整 Profile/运行时回滚再重试；UI 重启 200+2 |
| A09 | PASS | Fault：坏路径写盘失败与重试，损坏主档恢复 Pending 死亡备份，不复活；BlockedRecovery：双档损坏冻结并保留原字节，修复后恢复；Consistency：待领取领取失败无所有权漂移 |
| A10 | PASS（合成样例） | T06MigrationCheck.Run.final.log：v1～v6 各自人工/运行时合成历史测试档；逐版本断言原版本存在的 ID/数值/词缀/位置/材料/配方/进度；原字节迁移备份与重复读取断言 |
| A11 | PASS | Migration：旧物资首次 LegacyProtected；迁移后新得铁矿 7 个死亡损失，旧矿剩余保护；不授胜利或徽章，重复读取同 Run/ID |
| A12 | PASS | Matrix：后端拒绝拆解入场备用法杖；武器铭刻后死亡恢复原词缀，成本不返还，新制造物仍按本局新增处理 |
| A13 | PASS | T06LiveRegression.Run.final.log：真实 V 输入，v7 同 Run 双槽及技能/攻击/切换冷却恢复，立即动作被拒；DualWeapon 回归暂停与飞行弹体词缀快照 |
| A14 | PASS | LiveRegression：调用原拖放/旋转/交换控制器、容器更换/容量/掩码断言；构造 v6 非法锚点与缺模板实例，归还/重读后仍在迁移暂存/待领取，阻止出征，无 ID 丢失 |
| A15 | PASS | T06RegDualWeaponCheck.Run.final.log：四武器×五品质 20 个技能路径、锋锐/汲取/处决/蓄能、词缀铭刻与弹体快照；Consistency：疾速实际普攻间隔、回响实际扩大近战技能命中；四武器实际伤害另见 DualGameplayRegression |
| A16 | PASS | T06RegWorkbenchCheck.Run/Read.final.log：29 高级配方及前置链逐个解锁制造、18 基础装备、基础容器、重复解锁/少材料/满包/写盘失败不扣费，跨进程永久解锁/仓库；LiveRegression：v7 营地研究制造后死亡仍保留配方 |
| A17 | PASS | Matrix 无尽第 5 波后能第 6 波；DualGameplayRegression 四武器采集/Boss/宝箱；WorldEventsRuntimeCheck 真实 E/宝箱/祭坛/最近目标/暂停；RegProgression 六技能三选一/升级队列；Potion 真实 Q/制作/暂停冷却；AutoWave 倒计时与成长；HeroDodge 实际空格/无敌/冷却回归 |
| A18 | PASS | Matrix：真实主角攻击击杀第 5 波测试 Boss，挑战目标由战斗识别，定时撤离后 TestChallengeComplete；badges/regions 仍空；无正式森林奖励 |
| A19 | PASS | Fault：出征写盘前失败退回完整营地；结算提交后回营装载失败，磁盘已 Committed，重读/确认不重复发奖，没有第二个 Run |

A10 的真实用户历史档案全覆盖验证为 **NOT_RUN**：未取得用户各历史版本档，不能冒称合成样例为真实档。A07 测试采用同更新撤离成功请求与致死；有限 Boss 测试不自动结算，仍需撤离，因而不存在另一个 Boss 自动发奖入口。

## 构建与实际 Player

`T06BuildCheck.Build.release.log`、`BuildSummary.txt`：StandaloneWindows64 Development 构建成功，错误 0，警告 37，数据 184057194 字节，最终增量构建约 12.35 秒。首次完整成功构建约 2 分钟。

输出：`C:/Users/guan/Documents/unitytest/T06Validation/BuildSmoke/AdventureTest.exe`。

- `Player-smoke.final.log` / `BUILD_PLAYABLE_LOOP_SMOKE.txt`：实际独立 Player 启动，营地 → 出征 → CharacterController 移动/真实攻击 → 拾取 → 定时撤离 → 提交/回营 → 再出征 → 致死 → 提交/回营。永久仓库 1 件、历史结算 2 次。
- `Player-read.final.log` / `BUILD_RESTART_SMOKE.txt`：第二个全新 Player 进程恢复相同永久仓库 1 件与两次结算，等级为 1。
- 使用有图形设备的批处理 Player；冒烟驱动仅验证副本中存在，通过 `-t06-smoke / -t06-read` 启用，不安装到实际项目。明确使用 T06Validation/build-profile，自动玩家路径初始化在批处理模式跳过。
- `player-results.txt`：两个进程退出码均为 0。最终 Player 日志没有运行时异常。

## 运行截图

真实 Unity Play Mode 画面；战斗/仓库容量由隔离夹具布置，操作使用实际原生 IMGUI 按钮和 E 输入。不是概念图，也不是人工长时间打满全部波次。每类均保留 1280×720 与 1920×1080 PNG 及记录修订号/Run/数量的 txt。

| 内容 | 路径（证据根目录下） |
| --- | --- |
| 出征与携带清单（材料与药水固定显示） | screenshots/Departure720.png、Departure1080.png |
| 3 秒撤离引导 | screenshots/ExtractionCountdown720.png、ExtractionCountdown1080.png |
| 成功结算（带回 1 装备、9 木材） | screenshots/SuccessSettlement720.png、SuccessSettlement1080.png |
| 死亡结算（损失 1 装备、4 晶石） | screenshots/DeathSettlement720.png、DeathSettlement1080.png |
| 200 件满仓、2 项待领取 | screenshots/FullWarehousePending720.png、FullWarehousePending1080.png |
| 新 Unity 进程恢复 200+2 | screenshots/RestartRestoredPending720.png、RestartRestoredPending1080.png |

UI 日志：T06UICheck.Run.final.log、T06UICheck.Restart.final.log。已检查截图并做一次修复确认，解决准备/结算多行摘要被裁切，让材料与奖励/损失数量直接可见。

## 失败记录与修复

保留中间失败日志，不冒充一次全绿：

1. UI 初次启动/按钮夹具：开始截图时遗漏 batchmode，自动初始化了默认目录的全新空 Profile；确认目录和文件首次创建于 10:17:06，无原有存档或迁移档。已将该新目录完整移到 `accidental-fresh-profile`，默认路径原先无 ForestRuins 目录；未使用它做故障测试。之后全部批处理显式隔离。按钮夹具另因种子数据恢复将页签切到 Items，修正回 Camp 页后实际点击通过。
2. 首次 Player 编译失败：编辑器测试开关在 Player 分支写为 const，实例访问触发 CS0176；改为只读实例属性 false，Player 无可启用的 LegacyHarness。
3. 原 ProgressionRuntimeCheck 假设裸攻击 25、裸防御 0；前几批主武器已提供基础装备属性。测试基准更新为当前基础攻击+装备属性+技能，与实际系统一致，RegProgression 重跑通过；未为通过测试削弱装备属性。
4. 第一次 Player 冒烟暴露 Shader.Find 的 URP Unlit 在构建中被剥离；补入 Resources/CombatFeedback/AdventureUnlit.mat 显式保留资源引用，再构建并实际启动/攻击/两进程恢复通过。没有把“构建成功”等同于“Player 可运行”。
5. 校验中补强营地提交失败的整个 Profile 快照回滚，不只回滚可见运行时背包。Consistency 的满仓待领取领取故障/重试通过。

## 已知日志与未运行范围

- 验证副本的 UnityEditor.Search.SearchDatabase 在启动时产生既有 ArgumentOutOfRangeException；源于编辑器搜索索引，不在最终 Player 中出现，未通过删除用户工程 Library 掩盖。保留日志，不能称 Editor 全日志零异常。
- 多条既有 FindObjectsByType/FindFirstObjectByType 过时 API 警告，以及既有 nextAttack 未使用警告；本批未为清警告改写无关系统。
- 故障日志中 IOException 是主动注入的预期结果，对应断言要求没有奖励/所有权变动后才算通过。
- 人工长时间平衡试玩、非 Windows 构建、真实断电、手工篡改防护 **NOT_RUN**；不属于本批已验证能力。事务中断采用明确故障边界钩子与磁盘重读，不声称进行了真实电源断电。
- ForestRuins 仍为测试关；正式森林/湖泊 Boss/区域徽章/自由营地等没有制作。
- 退出恢复是完整一致检查点，飞行弹体/前摇重置，强退不保证最后未写盘动作，详见 T06_ADVENTURE_LOOP.md。

## 本机复跑

测试源码保留于验证副本 `Assets/CombatPrototype/Editor/T06*.cs`，旧模块回归为 `T06Reg*.cs`，规则工具 `T06EditChecks`。执行脚本 `run-final.ps1 / run-fixed.ps1 / run-release.ps1` 与各版本日志保留在证据目录。脚本使用本机绝对路径，不会自动推送代码、启用 CI 或修改真实玩家存档。复跑请使用独立副本与新的测试目录；不要把故障夹具指向真实档案。

## 原工程同步确认

18 个运行时 C# 文件（7 新增、11 适配）及 1 个保留 Shader 引用材质已按文件差异安装。安装前所有原 CombatPrototype 文件与完整备份 SHA256 一致；安装后运行时文件逐一与验证副本一致。未覆盖项目设置、场景、美术资源、用户未提交修改，未安装验证用运行驱动或 Editor 测试脚本。实际工程另外执行 Unity `-batchmode -quit`，成功退出码 0，无 C# 编译错误：`ActualProject-Compile.log`。文件哈希与安装清单见 `InstalledFiles.json`。
