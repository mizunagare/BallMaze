# CP06-B 原始证据索引

唯一隔离根 `I:/WGCombat/CP06B-1104-A`。产品冻结759340c8e7909b2cda43e20cc67af916016a47fc。原始目录不被发布工具修改；日志gzip与敏感路径脱敏仅用于发布副本。逐文件原SHA/发布SHA/编码见[manifest.json](manifest.json)。不上传可执行文件；本地可运行包有完整逐文件哈希。

## 统计与源身份

- [最终总表](FinalAnalysis2/summary.json)、[逐行CSV](FinalAnalysis2/results.csv)、[历史失败行](FinalAnalysis2/historical-failing-rows.json)。主矩阵Editor20进程789 PASS、非开发Player23进程824 PASS，未沿用旧PASS；不同专用构建/较早夹具按原命令与输入区分。
- [进程/输入一致性45项](delivery-consistency.json)、[保护34项](delivery-protection-audit.json)、[2355开工文件](protected-before.json)。主工程未提交场景/Settings/Recovery不提交。
- [源码输入](latest-source-inputs.json)、[测试输入](latest-test-inputs.json)、[纯构建后输入](latest-pure-inputs-after.json)、[输入差异](build-input-differences.json)、[字段差异](build-input-field-diffs.json)。5项隔离Unity写回不冒充等同。
- [新资产14项](asset-catalog.json)、[产品测试/纯包IL28类型](latest-assembly-audit.json)、[旧核心IL/v9布局30项](latest-legacy-il.json)、[旧四武器配对](legacy-baseline-pair.json)和[基线输入](BaselinePairInput/legacy.json)。

## B1 / B2 / B3 真实物理与动作

- [双刃Editor](TwinFinal4/probe.json)、[Player](PlayerTwinLatest4/probe.json)、[左右/交叉截图](PlayerTwinLatest4/basic.png)、[反击](PlayerTwinLatest4/counter.png)、[动作轨迹](PlayerTwinLatest4/basic.jsonl.gz)。
- [巨剑Editor](HeavyFinal4/probe.json)、[Player](PlayerHeavyLatest4/probe.json)、[蓄势](PlayerHeavyLatest4/heavy-slam.png)、[地波](PlayerHeavyLatest4/heavy-wave.png)。
- [镰刀Editor](ScytheFinal4/probe.json)、[Player](PlayerScytheLatest4/probe.json)、[回旋](PlayerScytheLatest4/scythe-reap.png)、[牵引](PlayerScytheLatest4/scythe-pull.png)。
- BoundaryFinal4与PlayerBoundaryLatest4：墙体、多Collider、暂停/死亡/取消/卸载等；CancelBefore1/CancelAfter1保留真实5/1到6/0。
- StatsBeforeEditor1、StatsAfterEditor1、PlayerStatsLatest4：属性/词缀真实几何与节奏，原8 FAIL保留。
- BossData1、PlayerBossLatest4：真实物理伤害及Boss控制免疫，不是自主讨伐。

## 正式奖励、旧随机流及恢复

- [同检查点Player配对](new-run-pair-player-final.json)、[Editor配对](new-run-pair-editor-canonical2.json)，首顺序误报new-run-pair-editor1.json仍在。
- ChannelControlData2/ChannelNormalData2及对应PlayerChannel*Latest4：实际旧核心/完整死亡/旧奖励多重集合与三流状态。
- PlayerChannelGroundLatest4、PlayerChannelPickedLatest4：实际检查点跨进程恢复，各连续3次真实LoadProgress。GroundPackage/PickedPackage保存文件及Expected对照元数据分别保留。
- [训练正式存档金丝雀](PlayerTrainingCanaryLatest4/training-storage-canary.json)、[严格比较器12项自测](ChannelComparatorSelfTest1/summary.json)。
- StorageEditor3、ResumeEditorData2、PlayerSaveLatest4、PlayerResumeLatest4；UpgradeEditorData1/UpgradePlayer1是合法结束旧Run再新森林，不伪称成功撤离。
- LegacyExpandedFinal4/LegacyExpandedPlayerLatest4：旧八技能/四武器；LegacyFormalData4/LegacyFormalPlayerLatest4：正式旧掉落/480规则。
- MigrationEditor1原超时；MigrationEditor2、MigrationEditor7、MigrationEditor8真实旧迁移日志。旧规则强制死亡刺激不算武器战斗。
- LegacySavePlayerLatest4首次aborted与候选包/旧集合完整保留；[LSR4重试](LSR4/probe.json)、[LRR4恢复](LRR4/probe.json)，根因仍未定位。

## 法杖及历史失败

NearPlayer1/2/3日志、实际死亡前ready证据保留；[NearEditor4](NearEditor4/probe.json)、[NearPlayer4](NearPlayer4/probe.json)各40项。原near=1.5m，追加.35/6/20m；真实Spawn/FirstCollision/Damage，未改CombatAim。专用构建见NearTestBuild4本地及相关输入/程序集审计。

## 构建、运行与性能

- [所有构建身份](build-identities.json)、[警告完整匹配行/摘要](FinalAnalysis2/builds-and-warnings.json)，各目录Unity.log.gz为完整原始日志发布副本。
- [最新纯发行完整文件SHA](LatestPureBuild4/release-files.json)、[Release回执](LatestPureBuild4/release.release.json)、[实际Bee](LatestPureBuild4/release.bee.json)、[BuildReport摘要](LatestPureBuild4/release.summary.txt)。本地LatestPureBuild4/Release可运行，Development=false，0错误98警告。
- [纯包启动退出](LatestPureSmoke4/runtime.json)及Player命令/日志：无原生输入结论。
- [Editor性能原始采样](PerformanceFinal4/performance.json)、[Player校准失败](PlayerPerformanceLatest4/performance.json)、[统计](FinalAnalysis2/performance-summary.json)。Player不能从失败计数器0推断零分配。完整帧/并发/GPU/长时间和预算NOT_RUN。

原生键鼠、独立人工、最终平衡与历史引擎问题见ACCEPTANCE；截图是受控实例，不能冒充人工试玩。本目录文件未以截图美观替代真实碰撞/业务回执。
