# 统一评分本轮证据

开始`491b72819dd7aac14b3c514098846288addc4f2c`，最终完整All `20261024-181305-74d5b037`。评分限定范围PASS；UI01 UNKNOWN未解决、原生U16/人工理解未执行，不因推送关闭。

- [实际JSON](FinalAll/results.json)、[CSV](FinalAll/results.csv)、[逐项报告](FinalAll/REPORT.md)、[86/2/19/1分类](FinalAll/classification.json)：实际exit0，两个负探针故意FAIL，无非预期FAIL、无遗留测试进程。
- [14场景原始分项](FinalAll/R1Diagnostics/Rules/score-components.jsonl)、[98行分项CSV](Derived/score-components.csv)、[派生来源](Derived/provenance.json)、[配置实读](FinalAll/R1Diagnostics/Rules/score-configuration.json)、[固定种子排序](FinalAll/R1Diagnostics/Rules/score-order.csv)、[断言标记](FinalAll/R1Diagnostics/Rules/score-results.txt)、[新进程完全一致数据](FinalAll/R1Diagnostics/Rules/score-checkpoint.txt)。排序CSV原始无表头，四列依次requestedSeed/actualSeed/defaultOrder/distanceOnlyOrder，保留原文件不改写。
- [真实导航](FinalAll/R1Diagnostics/Rules/r1-nav.csv)、[岸线物理](FinalAll/R1Diagnostics/Rules/r1-shore.csv)、[地形数据](FinalAll/R1Diagnostics/Rules/r1-terrain.jsonl)：本轮R1导航/通行/旧布局回归，不沿用原地形批次PASS。
- [经济与12评分快照汇总](FinalAll/adventure-economy-summary.json)，原始评分快照在FinalAll/R1Diagnostics/Normal-Gather、Normal-Treasure、Normal-Bypass；各stage1/2的finish/restored。正常AI轨迹、命令、进程退出码、审计及完整状态快照在FinalAll/B4Diagnostics/Normal-*，与受控规则/原生UI分开。
- [构建摘要](FinalAll/build-summary.json)、[77警告的完整匹配行（含编译重复）](FinalAll/build-warning-lines.json)、[完整构建哈希](FinalAll/build-manifest.json)、FinalAll/Logs完整脱敏归档。启动器SHA256 `001AEEBFB92718F8B49F0C0E0A03E313C54669552B08E952B2FEE3DDD143683A`不是游戏代码唯一证明；实际Managed/Assembly-CSharp.dll为`715864C6CE02341FE045EB26C9895B0908631615983964527B99E13C0C0B007F`，其余数据逐文件manifest。
- [初始787原始输入](Provenance/FinalRunInitial/source-build-provenance.json)、[最终77源码/787输入/63执行驱动](Provenance/Final/source-build-provenance.json)、[六项隔离设置差异](Provenance/Final/isolated-input-differences.txt)。Unity导入/构建重序列化和既有脚本设置差异未回写源工程，不能声称所有字节相同；用户ProjectSettings保持未提交。
- [Git暂存区证明](Provenance/git-index-proof.json)：77源与运行副本归一一致，配置JSON原字节与索引/副本相同，31份历史输入原字节相同。[静态检查](static-checks.json)：C#与测试检查exit0；全Assets的diff-check实际exit2，仅三个新Unity .meta空YAML值尾空格，保留测试时字节并完整记录，不能称全Assets格式检查PASS。[发布校验](publication-checks.json)：1152个清单条目哈希核对，1245文本/归档条目已知令牌/许可参数扫描；不是万能秘密检测声明。
- [1280受控地形](FinalAll/R1Screens/r1-overview-1280x720.png)、[1920受控地形](FinalAll/R1Screens/r1-overview-1920x1080.png)、[湖岸](FinalAll/R1Screens/r1-lakeshore-1920x1080.png)、[路线面板](FinalAll/R1Screens/r1-route-details-1920x1080.png)，尺寸/SHA见[图像清单](FinalAll/r1-screens.json)。另92张原UI矩阵本轮实际生成；受控镜头/截图不是原生输入或人工理解。

## 原始失败和非最终运行

- [模型缺失基线](Attempts/20261024-173252-93aa0cbb/results.json)：prepare PASS、RouteScoringProbe实际FAIL/exit1无超时；75源与491b基线归一后完全相等见baseline-proof.json，源码原字节快照附Sources。
- [初次定向](Attempts/20261024-174710-61c09908/results.json)：5PASS，模型/边界/恢复/R1三十seed。Editor.Search.SearchDatabase启动索引异常完整栈在原归档，不过滤、不归为产品关闭根因。此运行尚无后来的白装精确缺口及无出口可见提示断言，不冒充最终版本。
- [首轮All](Attempts/20261024-175127-c8a88fa8/results.json)：机器86/2/19/1、实际exit0；[验收分类](Attempts/20261024-175127-c8a88fa8/classification.json)因[无出口旧提示源码审计FAIL](source-audit-ui-exclusion.json)而标非最终验收FAIL。未伪称原测试已包含该UI断言，也未篡改历史退出码。修复后全新完整All独立运行。

旧地形批次的所有失败、辅助启动隔离失误及原UI01记录继续留在上级Evidence，不覆盖。这里只发布合成测试数据、指定诊断与源哈希，未发布真实玩家存档、完整save.json、分页物品文件、转储、构建二进制或Library/Temp。
