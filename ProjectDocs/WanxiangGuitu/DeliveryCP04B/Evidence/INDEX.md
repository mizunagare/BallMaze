# CP04-B 证据索引

工程外根I:/WGCombat/CP04B-1102-A。原始文件未覆盖；日志/JSONL发布副本gzip及凭据值脱敏，源/发布SHA分别登记。Release二进制与Library不上传，留在本机；哈希与PE证明归档。旧调查Reference仅作只读来源，不合并本分支。

- [完整发布清单/双SHA](manifest.json)
- [最终分类：174PASS/1UR/3NR，整体BLOCKED](AssessmentDelivery/assessment.json)；[CSV](AssessmentDelivery/checks.csv)；[实际分类退出2](assessment-delivery-exit.json)
- [各真实运行路径](AssessmentDelivery/run-paths.json)；[保护核对](AssessmentDelivery/protection.json)；[2329项原始保护SHA](protected-before.json)
- [构建副本1163项核对及5项差异](product-input-binding.json)；[5项原始差异索引](BuildInputDrift/index.json)
- [Editor24组](AssessmentDelivery/Editor-paired24.json)；[Player24组](AssessmentDelivery/Player-paired24.json)
- [最终计数克隆精确变换审计](counter-clone-audit.json)；[执行源哈希](final-test-inputs.json)
- [性能汇总JSON](PerfAnalysis/metrics.json)；[CSV](PerfAnalysis/metrics.csv)；[硬件](hardware.json)
- [旧产品38项本轮重跑](BeforeMatrix/diagnosis.json)
- [前版本真实性能探针](BeforePerfFrozen/performance.json)；[后版本](AfterPerfFrozen/performance.json)
- [原生线程分配失败前的初版探针](Performance/performance.json)，其raw0不可作为零分配结果；早期Idle枪口BeforePerformance/AfterPerformancePaired不替代最终冻结释放姿态数据。
- [验收构建完整警告/错误](AcceptanceBuildShippingInput/build.json)；[纯发行构建](PureBuildShippingInput/build.json)
- [验收PE/二进制SHA](acceptance-metadata.json)；[纯发行无驱动PE证明/二进制SHA](pure-metadata.json)
- [工具失败01](tool-failure-01.json)；[目录布局失败02](tool-failure-02.json)；[失败03](tool-failure-03.json)与[退出码纠正说明](tool-failure-03-correction.json)
- [首次运行器执行源](Invoke-Players.first-executed.ps1.txt)；[修正后控制汇总](RunnerControl/player-batch-progress.json)；[PowerShell语法](powershell-parse.json)

## 分层真实业务数据

每个目录都有对应命令、NativeProbe host退出、实际desktop子进程、Runner结果、完整Unity/Player日志和存档审计。API受控测试不是原生输入/人工试玩。初始嵌套目录按真实路径引用，未改路径伪装平铺。

|层/套件|真实业务数据|完整日志|
|---|---|---|
|EditorHistorical|[数据](AfterHistorical/presentation.json)|[日志](AfterHistorical/Unity.log.gz)|
|PlayerHistorical|[数据](PlayerHistorical/presentation.json)|[日志](PlayerHistorical/Player.log.gz)|
|EditorMatrix|[数据](AfterMatrix/diagnosis.json)|[日志](AfterMatrix/Unity.log.gz)|
|PlayerMatrix|[数据](PlayerHistorical/PlayerMatrix/diagnosis.json)|[日志](PlayerHistorical/PlayerMatrix/Player.log.gz)|
|EditorWall|[数据](AfterWall/diagnosis.json)|[日志](AfterWall/Unity.log.gz)|
|PlayerWall|[数据](PlayerHistorical/PlayerMatrix/PlayerWall/diagnosis.json)|[日志](PlayerHistorical/PlayerMatrix/PlayerWall/Player.log.gz)|
|EditorBoundary|[数据](AfterBoundary/diagnosis.json)|[日志](AfterBoundary/Unity.log.gz)|
|PlayerBoundary|[数据](PlayerHistorical/PlayerMatrix/PlayerWall/PlayerBoundary/diagnosis.json)|[日志](PlayerHistorical/PlayerMatrix/PlayerWall/PlayerBoundary/Player.log.gz)|
|EditorLifecycle|[数据](AfterLifecycle/lifecycle.json)|[日志](AfterLifecycle/Unity.log.gz)|
|PlayerLifecycle|[数据](PlayerHistorical/PlayerMatrix/PlayerWall/PlayerBoundary/PlayerLifecycle/lifecycle.json)|[日志](PlayerHistorical/PlayerMatrix/PlayerWall/PlayerBoundary/PlayerLifecycle/Player.log.gz)|
|EditorDeath|[数据](AfterDeath/lifecycle.json)|[日志](AfterDeath/Unity.log.gz)|
|PlayerDeath|[数据](PlayerHistorical/PlayerMatrix/PlayerWall/PlayerBoundary/PlayerLifecycle/PlayerDeath/lifecycle.json)|[日志](PlayerHistorical/PlayerMatrix/PlayerWall/PlayerBoundary/PlayerLifecycle/PlayerDeath/Player.log.gz)|
|PlayerPerf|[数据](PlayerHistorical/PlayerMatrix/PlayerWall/PlayerBoundary/PlayerLifecycle/PlayerDeath/PlayerPerf/performance.json)|[日志](PlayerHistorical/PlayerMatrix/PlayerWall/PlayerBoundary/PlayerLifecycle/PlayerDeath/PlayerPerf/Player.log.gz)|

记录中的Shot是实际Spawn事件，Trace含逐帧Flight/首次Collision，Damage来自真实Health.Observed。无事件即无命中，不用截图或方向变化替代。影子计数克隆只作查询/计时测量，不能充当实际战斗命中证据。

旧main及历史UR原件未改；本分支新近距PASS仍需独立复审。旧引擎开放项、原生UI/人工体验、逐Solve分配及输入等同性不由这些数据自动关闭。

[Editor与Player分别绑定自身旧回执、各291项不变与两项加强](core-contract-compare.json)；[拒绝错误跨层比较的初次工具失败](tool-failure-04.json)；[发布校验](publication-check.json)。
