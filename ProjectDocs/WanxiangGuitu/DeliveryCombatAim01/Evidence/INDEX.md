# AIM01 证据索引

全部来自本轮唯一工程外根。`manifest.json`列原始路径、原始SHA与发布SHA；`.log.gz/.stdout.gz/.stderr.gz`保留上下文且凭据字段脱敏。不要把外部文件绝对路径当GitHub链接；本目录均为仓库相对链接，可从固定SHA打开。

- [固定旧例](BeforeFinal/before.json)、[旧时序](BeforeFinal/timeline.jsonl)、[最终同位置复验](FinalPaired/before.json)、[新时序](FinalPaired/timeline.jsonl)。同seed418和稳定ID；没有伪造旧版截图。
- [初始无内容误exit0核查](Before/technical-evaluation.json)、[物理API探针](PhysicsProbe/physics-probe.json)（若该文件实际名不同，以manifest为准）。
- [132项有限矩阵](RulesExtended/rules.json)、[每颗弹体观测](RulesExtended/projectile-events.jsonl)。
- [188时序](RegTiming/combat01.json)、[34区域/独立箭](RegArea3/area.json)、[代理夹具差异原样失败](RegArea2/area.json)、[对应接触日志](RegArea2/events.jsonl)。
- [选择目标](CraftShared/matrix-target.json)、[195事务回归](CraftShared/matrix-craftonly.json)、[新进程恢复](CraftShared/matrix-resume.json)。
- [最终运行时Core结果](Runtime/Attempts/105021-Observe-629c60/StorageAfter/result-Observe.json)、[Core OS/超时](Runtime/Attempts/105021-Observe-629c60/results.csv)、[完整Player日志](Runtime/Attempts/105021-Observe-629c60/player.log.gz)、[退出审计及合成存档](Runtime/Attempts/105021-Observe-629c60/StorageAfter/)。
- [最终Resume结果](Runtime/Attempts/105120-Observe-5085f8/StorageAfter/result-Observe.json)、[恢复前](Runtime/FinalStory/aim-before-exit.json)、[恢复后](Runtime/FinalStory/aim-resume.json)、[恢复OS/超时](Runtime/Attempts/105120-Observe-5085f8/results.csv)。
- 实际1280×720验收Player：[弓击石头](Runtime/FinalStory/aim-hit-Bow-Stone.png)、[杖击铁矿](Runtime/FinalStory/aim-hit-Staff-Ore.png)、[临时掩体](Runtime/FinalStory/aim-runtime-controlled-cover.png)。运行时事件/身份可对应；不是原生UI或人工试玩。
- [第一次运行时FAIL](Runtime/Attempts/103900-Observe-fe53b8/StorageAfter/result-Observe.json)；过早HP断言及稍后真实命中均在同次事件中；[中间准星裁切截图](Runtime/Story2/aim-hit-Bow-Stone.png)，与FinalStory不是同Run，不作为严格同位画面对照。
- [纯发行构建完整消息](ReleaseFinal/Results/build-report-messages.json)、[发行PE及二进制哈希](ReleaseFinal/release-metadata.json)、[发行输入](ReleaseFinalLaunch/build-inputs.json)。
- [验收构建完整消息](Runtime/T/AimFinal/Results/build-report-messages.json)、[验收输入](AcceptanceFinalLaunch/build-inputs.json)、[实际注入驱动](Runtime/DriverInputsFinal/)、[驱动输入摘要](Runtime/T/AimFinal/driver-inputs.json)。
- [授权源绑定](authorized-source-inputs.json)、[Git索引内容绑定](code-commit-binding.json)、[发布字节校验](publication-check.json)、[用户文件保护](protection-check.json)、[原始用户哈希](user-before.json)、[规则汇总](final-rule-summary.json)。

历史FAIL只增加后续结果，不回写历史结果。最终规则585PASS，不统计wrapper内部Note/循环重复检查为独立样本。原生UI、人工、完整正常AI全环与性能本批NOT_RUN；历史根因UNRESOLVED。
