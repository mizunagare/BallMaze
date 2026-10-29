# GAMEPLAY-UX04 证据索引

开始main eb11dd3d8350f7e7a89d94d2e45d4cfd203f53e9；最终产品fb9dcb828787c6f73b9d5bc078df3d516593d85c；测试5dfe7c39585a03549b67a1cdf675adbca33571a5。所有受控数据来自拥有根I:/WGCombat/GUX04-1029-A，不是真实玩家存档。

- [统一JSON](Summary/summary.json)、[856条CSV](Summary/assertions.csv)、[断言JSON](Summary/assertions.json)：当前断言与历史执行分开，不把包装器exit0当成整体验收。
- [范围矩阵CSV](Summary/range-matrix.csv)、[完整120样本/实际HP](Shared07/matrix-run.json)、[旧轮廓顶点](Before03/vertices.json)、[候选/bounds](Before03/candidate.txt)、[释放帧](Before03/release.txt)。
- [最初修复前结果](Before02/result.json)、[正确释放帧负例](Before03/result.json)；Before为内存门槛NOT_RUN。首轮夹具源码没有独立字节冻结；不补造记录。其后各Output复制了实际测试文本，所有早期失败保留。
- [目标准备](Shared07/matrix-target.json)、[营地新进程](Shared07/matrix-resume.json)、[在途新进程](Shared07/matrix-runcraftresume.json)、[目标断言时间线](Summary/goal-timeline.json)。Store与RunCraftStore保留实际v9主备/分页档，时间线不是逐帧录像。
- [最终UI10项](Final3/UI/result.json)、[滚动/HUD17项](Scroll08/scroll.json)、[1280配方](Scroll08/controlled-recipe-1280x720.png)、[1920配方](Scroll08/controlled-recipe-1920x1080.png)、[仓库](Scroll08/controlled-warehouse-1280x720.png)：均为受控回调/RenderRequest，不是原生UI或人工。
- [领域时序188项](TimingDomain-Store/combat01.json)、[UX02 60项](Final2/UX02Regression/ux02.json)、[品质15项](Final2/MeleeContracts/contracts.csv)、[远程34项](Final2/RangedArea/area.json)、[恢复33项](Final2/RecoveryMatrix/matrix.json)、[输入26项](Final2/Input/input01-rules.json)。
- [正常AI轨迹](Final3/Normal-Gather/normal-ai.csv)、[操作标记](Final3/Normal-Gather/normal-results.txt)、[第一Run检查点](Final3/Normal-Gather/b4-checkpoint-1.json)、[再次出征检查点](Final3/Normal-Gather/b4-checkpoint-2.json)、[真实结算](Final3/Normal-Gather/b4-first-settlement.json)、[暂停只读诊断](Final3/Normal-Gather/pause-diagnostics.jsonl)。
- [Normal进程](Final3/Normal-Gather/process-result-Normal.json)、[Resume进程](Final3/Normal-Gather/process-result-Resume.json)、[FinalResume进程](Final3/Normal-Gather/process-result-FinalResume.json)、[启动到退出存储审计](Final3/Normal-Gather/storage-audit.jsonl)。虚拟输入/领域交互不冒充原生。
- [最终发行构建完整警告](Final3/Build/build-report-messages.json)、[构建原日志](Final3/Build/Unity.log.gz)、[PE与发行SHA](Final3/Build/release-inspection.json)、[1387输入](Final3/Build/build-inputs.json)、[后续一项Editor夹具差异](Bindings/build-input-comparison.json)。
- [产品源绑定](Bindings/source-bindings.json)、[初始绑定保留](BindingsHistory/source-bindings-initial.json)、[测试源哈希](BindingsHistory/final-test-source-hashes.json)、[五用户文件/历史Git保护](Bindings/protection-check.json)、[开工用户哈希](Bindings/user-before.json)、[结束用户哈希](Bindings/user-final.json)。
- [旧AI续程失败回执](Normal-Gather/process-result-Resume.json)、[旧AI完整日志](Normal-Gather/Resume.log.gz)、[Editor GPU fatal完整日志](Final2/CombatTiming/Unity.log.gz)、[GPU崩溃真实exit](Final2/CombatTiming/UX04CombatTiming.Run.exit.json)、[旧batch夹具deadline](CombatTiming/combat01.json)。均未由后续PASS关闭。

[manifest.json](manifest.json)记录每份发布字节、大小、源路径、原始SHA256及发布SHA256。日志仅做凭据脱敏/gzip，异常正文不删，未脱敏原件仍在本机隔离根。未上传真实存档、Library、Temp、完整发行包或内存转储。

第一次完整相关编排、Final2及最后HUD定向复验分别留有sequence.jsonl；失败传播与依赖NOT_RUN不改写。详见[失败历史](../FAILURE_HISTORY.md)和[验收表](../ACCEPTANCE.md)。
