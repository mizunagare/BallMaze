# 分层验收

|范围|状态|证据|
|---|---|---|
|B1双刃独立动作、反击真实条件、取消/冷却/墙体|PASS|TwinFinal4与PlayerTwinLatest4，各55断言|
|B2巨剑、破防、地波首碰/遮挡/暂停与生命周期|PASS|HeavyFinal4与PlayerHeavyLatest4，各34|
|B3镰刀、分段去重/墙阻/连续牵引/Boss免疫|PASS|ScytheFinal4与PlayerScytheLatest4，各33|
|边界/死亡/切换/场景清理/四旧武器和八技能|PASS|BoundaryFinal4 96、LegacyExpandedFinal4 157、对应Player和LegacyIL|
|既有Frenzy/触及/回响新武器适用|PASS|StatsBeforeEditor1保留8 FAIL；StatsAfterEditor1与PlayerStatsLatest4各26 PASS|
|v9品质/词缀/装备/保存/独立进程、旧Run→正常新Run|PASS|StorageEditor3、ResumeEditorData2、PlayerSaveLatest4、PlayerResumeLatest4、UpgradeEditorData1、UpgradePlayer1|
|v1～v8迁移|PASS|MigrationEditor2、MigrationEditor7/8真实原规则日志；非人工/非新武器战斗|
|旧奖励及三流/全局不变，新通道概率版本与去重|PASS|LegacyFormalData4、LegacyFormalPlayerLatest4、new-run-pair-player-final、Channel*、12项比较器自测|
|训练不写正式存档|PASS|PlayerTrainingCanaryLatest4/training-storage-canary.json|
|历史法杖near实际首次碰撞和损血|PASS|NearEditor4与NearPlayer4各40；保留NearPlayer1/2/3 FAIL|
|正式构建/实际Bee/驱动剔除/产品输入|PASS|LatestPureBuild4、latest-assembly-audit、latest-legacy-il、delivery-consistency|
|纯发行启动训练/观察日志/实际退出|PASS|LatestPureSmoke4；后台关闭不代表原生操作|
|Editor限定LateUpdate区间CPU/GC校准与采样|PASS|PerformanceFinal4/performance.json；仅测量有效性|
|最新Player CPU/GC采样|NOT_RUN|PlayerPerformanceLatest4/performance.json校准失败；不填0、不推断零分配|
|原生U16|NOT_RUN|无真实物理操作者证据|
|新武器原生操作|NOT_RUN|PLAYER_GUIDE，仅准备协议|
|独立人工手感/动作/音质可读性|NOT_RUN|无独立试玩记录|
|最终平衡|NOT_RUN|候选参数与少量夹具不是平衡结论|
|完整帧/并发负载/预算|NOT_RUN|缺可靠采样和目标预算|
|长时间战斗|NOT_RUN|受控短序列不能替代长时间测试|
|UI01 D3D12 UNKNOWN|UNRESOLVED|历史状态保留|
|Editor青色帧根因|UNRESOLVED|历史状态保留|
|Editor.Search内部异常|UNRESOLVED|本轮原始Unity.log保留|
|历史C15关闭根因|UNRESOLVED|后续纯包退出成功不证明历史原因|
|外部诊断发送路径|UNRESOLVED|Bee全关不等于所有系统路径绝对关闭|
|偶发新Profile发布aborted|UNRESOLVED|LegacySavePlayerLatest4；LSR4/LRR4重试成功未定位根因|

主功能行实例统计Editor789 PASS、非开发Player824 PASS、最终0 FAIL；历史FAIL独立列在FinalAnalysis2/historical-failing-rows.json及FAILURE_HISTORY。开放项统一登记6 NOT_RUN与7 UNRESOLVED，Player校准失败归属完整性能开放项（不重复计数）。未宣称整批人工体验通过。每项文件从[INDEX](Evidence/INDEX.md)定位。

隔离构建输入与源码序列化配置并非逐文件相同：PC_RPAsset、URPGlobalSettings、EditorBuildSettings、ProjectSettings、GraphicsSettings五项差异及具体字段在[build-input-field-diffs](Evidence/build-input-field-diffs.json)。实际测试前输入与纯包构建后快照均保留，产品程序集IL等同不代表全部渲染/配置等同。未擅自恢复或回写用户文件；完整序列化构建输入等同性继续UNRESOLVED。Profile身份与实际Bee五项false另独立核验通过。
