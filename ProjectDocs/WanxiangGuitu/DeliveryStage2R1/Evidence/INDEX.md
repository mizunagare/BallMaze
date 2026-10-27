# S2-R1 证据索引

主要冻结执行根：`D:/WanxiangValidationRuns/S2R1/FrozenValidation/20261027-102526-ad379719`；原始完整日志/合成存档/构建留在本机，不上传存档/分页/缓存/转储。仓库日志通过既有redactor脱敏并转UTF-8，原/发布SHA256在manifest；PNG按原字节复制。不是原生鼠标键盘或人工试玩。

- [分层最终结果与用户保护](FINAL_RESULTS.json)：35离线断言、31定向步骤、18+8观测、3进程完整正常AI、构建与开放事项；不跨层加总。
- [原ZIP核验](ReviewIntake/intake.json)、[旧原脚本复现](OriginalReproduction/review-results.json)、[原审阅工具材料](ReviewIntake/OriginalReviewSource/)；最初缺任务书的阻断记录保留，后来用户给出I盘路径已解决。
- [修复前29断言](Offline/SummaryBefore/results.json)、[分组缺陷首次失败](Offline/GroupingBeforeFix/results.json)、[ACK过严的5项失败](Offline/SummaryAfter5/results.json)、[最终35断言](Offline/SummaryFinal/results.json)。每条有独立stdout/stderr、assertion、summary和CSV；负例child FAIL为预期，首次失败不覆盖。
- [历史19条最新只读重审](Offline/Historical19Audit3/matrix-summary.json)、[214值对比与模块哈希](Offline/Historical19Comparison3.json)；Audit1及首次分组比较失败仍保留。新schema不回填旧记录。
- [冻结编排结果](FrozenValidation/Diagnostics/results.json)、[CSV](FrozenValidation/Diagnostics/results.csv)、[所有30Unity完整脱敏日志](FrozenValidation/Logs/logs-redacted.zip)、[原/发布日志manifest](FrozenValidation/Logs/log-manifest.json)。
- [26场逐例观测CSV](FrozenCombat/combat-results.csv)、[分项/配对差/输入/身份/时钟/结局/哈希JSON](FrozenCombat/combat-summary.json)；Main18与Coverage8分别报告，按6区组各n1。未合成跨目标构筑均值。
- [实际父进程结束后的绑定审计](FrozenCollection/collection.json)：8组均通过现有矩阵汇总。父Editor进程按事前parentMethod匹配；一组3/4例共享进程，未伪称每例独立进程。
- [普通敌跨进程结果](FrozenValidation/Diagnostics/Rules/Recovery-Ordinary/recovery-result.json)、[湖Boss跨进程结果](FrozenValidation/Diagnostics/Rules/Recovery-Lake/recovery-result.json)，对应外置观测检查点、JSONL、动作和真实保存定位审计在相邻目录；4次独立Editor启动在编排表中。
- [既有完整正常AI三阶段](Stage2Protocol/Diagnostics/results.json)、[实际业务断言](Stage2Protocol/Diagnostics/w0-s1-Safety-Gather/normal-results.txt)、[新协议独立汇总](Stage2ProtocolAudit/matrix-summary.json)。此冒险使用较早准备副本，102份产品源与冻结版一致；真实原驱动来源不同于R1受控战斗，不冒称Editor程序集全相同。
- [受控Boss截图42张](FrozenValidation/Screens/Rules/)：实际Editor相机截屏。例：[湖Boss岸边攻击前摇](FrozenValidation/Screens/Rules/paired-Lake-1/Lake-s1-Boss/boss-telegraph-boss-tide-ShoreBite.png)。仅辅助定位运行，不替代原生或美术终稿验收。
- [构建与输入审计](FrozenReleaseAudit2/release-audit.json)、[BuildReport原文](FrozenReleaseAudit2/BuildSummary.txt)、[窄运行引用错误门禁](FrozenRuntimeLogGate.json)。exe/DLL哈希、102 runtime源、依赖、用户文件与全部warning标记/异常上下文可核对。88 BuildReport警告与182日志标记行口径不同。
- [旧All审计器拒绝记录](ReleaseAuditCompatibilityFailure.json)、[完整拒绝栈](ReleaseAuditCompatibilityFailure.txt)；没有加假report.finalized步骤。新的小型只读审计按定向真实结束合同，不改变原All审计。
- [改前事件探针](ObservationBefore/Diagnostics/results.json)、[第一次普通预试](Failures/PilotOrd1/Diagnostics/results.json)、[第一次湖Boss/入口失败](Failures/PilotLake1/Diagnostics/results.json)、[恢复首次失败与正常关闭清理](Failures/RecoveryPilot/Diagnostics/results.json)、[翻滚/尸体断言失败](Failures/LakeAfterGuard/Diagnostics/results.json)、[中间复测6步通过](BoundaryRecovery2/Diagnostics/results.json)。所有根独立，不把预试并入主18样本。

正式Player原生UI、四武器独立人工、完整性能NOT_RUN；UNKNOWN/青色帧/Search及JobTempAlloc因果未定位。历史UI01 65/2/20/1、阶段2 All154/2/3/2保留历史，不移作本轮PASS。
