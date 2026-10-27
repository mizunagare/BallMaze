# INPUT-01 证据索引

所有运行均使用START_BASELINE中工程外唯一根和合成进度。只发布诊断/衍生身份/原始日志/源码快照/截图，不发布真实存档、构建二进制、Library、Temp或凭据。文件按原字节保存，完整清单在Runtime/PUBLICATION_MANIFEST.json。

- [开始与用户文件hash](../START_BASELINE.json)、[动作映射](../INPUT_ACTIONS.md)、[失败历史](../FAILURE_HISTORY.md)。
- [审核包3996文件校验](ReviewSource/verification.json)、[审核结论](ReviewSource/REVIEW_RESULTS.json)、[审核侧中断记录](ReviewSource/reviewer_attempts.json)：来源是用户提供的S2-R2固定复审，不冒称INPUT批重新执行35/58/12或独立复审。
- [最终分层结果、31源码与产物hash](Runtime/FINAL_RESULTS.json)：源保护文件字节不变；克隆ProjectSettings两行Unicode转义另列，不伪称字节相同。
- [最终完整受影响All JSON](Runtime/FinalFrozenValidation/results.json)、[CSV](Runtime/FinalFrozenValidation/results.csv)、[计数](Runtime/FinalFrozenValidation/counts.json)、[命令/时间/日志总览](Runtime/FinalFrozenValidation/REPORT.md)。35P/2预期负探针FAIL/92NR/2历史UR，0非预期FAIL；不是所有玩家体验通过。
- [26产品规则](Runtime/FinalFrozenValidation/Rules/input01-rules.json)、[239虚拟输入/uGUI断言](Runtime/FinalFrozenValidation/Rules/input01-play-normal.json)、[11新进程标题继续断言](Runtime/FinalFrozenValidation/Rules/input01-play-resume.json)、[检查点身份](Runtime/FinalFrozenValidation/Rules/input01-identity.json)。包含布局逐元素断言，不能相加为独立游戏次数。
- [焦点观测](Runtime/FinalFrozenValidation/Rules/refocus-observation.json)、[鼠标消费者逐帧](Runtime/FinalFrozenValidation/Rules/mouse-consumer-trace.txt)。具体Unity日志、process/desktop receipts及ExecutedSources在同目录及上一级；虚拟InputSystem事件不是原生键鼠。
- [正常AI轨迹](Runtime/FinalFrozenValidation/Normal-Gather/normal-ai.csv)、[真实业务标记](Runtime/FinalFrozenValidation/Normal-Gather/normal-results.txt)、[首局结算](Runtime/FinalFrozenValidation/Normal-Gather/b4-first-settlement.json)、[阶段1](Runtime/FinalFrozenValidation/Normal-Gather/b4-checkpoint-1.json)、[阶段2](Runtime/FinalFrozenValidation/Normal-Gather/b4-checkpoint-2.json)。三个进程的完整日志/退出回执、原始随机/来源账/路线快照同目录，不是人工操作。
- [构建汇总](Runtime/FinalFrozenValidation/Build/BuildSummary.txt)、[原构建日志](Runtime/FinalFrozenValidation/Build/WanxiangBuild.ValidateBuild.log)、[只读BuildReport的97条消息](Runtime/BuildReportInspection2/build-report-messages.json)。Succeeded但2 Error/91 Warning；I14质量UNRESOLVED，不写成0错。
- [正式Player缺档入口](Runtime/FinalFrozenValidation/B09-Title-Missing/entry-audit.jsonl)、[有效档入口](Runtime/FinalFrozenValidation/B09-Title-Ready/entry-audit.jsonl)、[实际退出回执](Runtime/FinalFrozenValidation/B09-Title-Ready/process.json)。两个标题的原Player日志和title-player.png同目录；退出方式是后台WM_CLOSE，不是标题栏点击/U16。
- [原生环境边界](Runtime/interactive-environment.json)：仅用户活动控制台、无已授权独占环境或运行测试VM，原生/独立人工NOT_RUN。

## 实际截图（均非原生/人工验收）

|画面|1280×720|1920×1080|
|---|---|---|
|自定义键帽与150%HUD|[图](Runtime/FinalFrozenValidation/Rules/input-hud-1280.png)|[图](Runtime/FinalFrozenValidation/Rules/input-hud-1920.png)|
|同一键位设置面板|[图](Runtime/FinalFrozenValidation/Rules/input-settings-1280.png)|[图](Runtime/FinalFrozenValidation/Rules/input-settings-1920.png)|

[冲突](Runtime/FinalFrozenValidation/Rules/input-conflict.png)、[保存失败](Runtime/FinalFrozenValidation/Rules/input-save-failed.png)、[新进程标题](Runtime/FinalFrozenValidation/Rules/input01-resume-title.png)、[标题设置内键位](Runtime/FinalFrozenValidation/Rules/input01-title-settings.png)。分辨率与边界/重叠/键帽/按钮裁切断言在受控239条检查内。原图不裁切、不替换为概念图。

## 所有尝试独立保留

Runtime下InitialValidation、DirectedTrace、DirectedInput2/3/4/5、FinalValidation、FinalFrozenValidation分别对应不同输入版本/条件；各自results/命令/源码/失败不能跨轮拼接通过。FinalValidation为06e冻结的历史All，不能冒称最终f16；FinalFrozenValidation才是最终本轮All。Runtime/BuildReportInspection保留辅助工具CS0266失败，BuildReportInspection2只读成功；两者均发生在发布构建后，不回写发布结果。

本机原件拥有者根保留完整合成进度；公开摘要不具备重新恢复游戏所需全部原件，复跑应从TESTING重新生成。原生U16、独立人工、完整性能NOT_RUN，UNKNOWN/青色帧/Search/JobTempAlloc及本轮包导入/构建质量根因继续UNRESOLVED。
