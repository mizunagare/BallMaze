# COMBAT02 证据索引

开始71877635f3b5891abeccaff4032045156ce8af85；产品/工具冻结ef2ba04f90790607742d4b5b4f11bfbf93293026。最终交付以本索引的Git固定SHA为准。新运行根I:/WGCombat/C2-1028-2140，仅合成档。

- [条目汇总](FINAL_SUMMARY.json)、[验收CSV](ACCEPTANCE.csv)。17P/1历史预期F/4N/7U；另有首次恢复链4个exit1，绝不隐藏。
- [原始Before684](Runs/Before/matrix.csv)、[After684](Runs/After/matrix.csv)、[逐键对照](paired-matrix.csv)、[20条验证](Runs/Comparison/comparison.json)。
- [Before边界81](Runs/BeforeBoundary/matrix.csv)、[After边界81](Runs/AfterBoundary/matrix.csv)；胶囊半径/高度/中心逐行记录。
- [Before时序](Runs/Before/timing.csv)、[After时序](Runs/After/timing.csv)；保留帧抖动与冷启动样本。
- [Before24短战](Runs/Before/duels.csv)、[After24短战](Runs/After/duels.csv)、[均值/标准差/范围](paired-duels-summary.json)。固定场地启用敌AI，不是森林双Boss或人工。
- [15项真实伤害](Runs/Contracts/contracts.csv)、[16坡面](Runs/Slope/matrix.csv)。±10°碰撞体静态测试，不替代真实爬坡体验。
- [原188断言187/1](Runs/LegacyOriginal/combat01.json)、[唯一预期调整后的188P](Runs/LegacyAdapted/combat01.json)、[实际执行版本](Runs/LegacyAdapted/Executed-Combat01Checks.cs.txt)。
- [规则与正常AI六进程](Runs/Regression/results.csv)、[森林AI完整流程](Runs/Regression/Normal-Gather/normal-results.txt)、[轨迹](Runs/Regression/Normal-Gather/normal-ai.csv)、[实际seed/配装](Runs/Regression/Normal-Gather/metadata.txt)、[存储定位审计](Runs/Regression/Normal-Gather/storage-audit.jsonl)。
- [首次恢复前置失败](Runs/Recovery-Run/results.csv)、[原始完整日志](Runs/Recovery-Run/Unity.log.gz)。三次依赖失败分别保留在Recovery-Resume/PendingResume/CommittedResume，不能算有效恢复验证。
- [只读诊断新Run](Runs/RecoveryProbe/results.csv)、[Dump](Runs/RecoveryProbe/restore-diagnostic.txt)、[原驱动](B07Rules-before-diagnostic.cs.txt)、[仅增Dump的驱动](B07Rules-diagnostic.cs.txt)。新Run通过不关闭旧失败根因。
- 新Run [Running恢复](Runs/RecoveryProbe-Resume/results.csv)、[Pending故障重试](Runs/RecoveryProbe-PendingResume/results.csv)、[Committed确认及再出征](Runs/RecoveryProbe-CommittedResume/results.csv)、[状态标记](Runs/RecoveryProbe/b07-rules.txt)。expected各阶段副本与actual各阶段保留，不只留下最后一次。
- [构建所有警告](Runs/Build/build-report-messages.json)、[真实exit/timeout](Runs/Build/results.csv)、[EXE/DLL哈希及本批驱动剔除](Runs/Build/build-hashes.json)。发行实战操作NOT_RUN。
- [源/副本逐文件哈希](product-inputs.json)、[用户保护前](protected-before.json)、[保护后](protected-after.json)、[发布文件原始/发布哈希](published-manifest.json)。C#无差异；副本部分设置重序列化差异如实记录。

## 反馈前后图（受控）

同机位1280×720、白装无词缀、2m静态目标、相同Origin。RenderRequest仅用于有限轮廓对照；受击金色高亮遮住部分模型，不能称人工清晰度通过。raw与controlled都保留，没有用裁切隐藏缺陷。

|武器|Before|After|
|---|---|---|
|剑|[原图](Runs/VisualBefore/controlled-release-0.png)|[新图](Runs/VisualAfter/controlled-release-0.png)|
|枪|[原图](Runs/VisualBefore/controlled-release-1.png)|[新图](Runs/VisualAfter/controlled-release-1.png)|

raw-0/1位于相同目录。B07受控攻击截图位于Runs/Regression/B07Combat.Run，不冒称人工。GameView/青色帧历史不关闭。

所有完整Unity日志以gz归档，只做凭据值脱敏，不删除错误、警告或异常。原字节日志仍在工程外根，原/发布SHA均在manifest。各运行保存command/start/end/exit/timeout/desktop回执与实际测试源版本。共用measurement摘要的scope文字描述整套工具，Boundary/Contracts/Visual/Slope不包含短战；只能按执行方法与各CSV实际行数判定，不能把空duels表头算样本。
