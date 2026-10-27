# S2-R2 证据索引

原始运行根：`D:/WanxiangValidationRuns/S2R2/20261027-115821-offline/`。本批仅离线Python；没有Unity、Player、新战斗、原生输入或真实玩家存档操作。合成夹具、摘要及源码按原字节发布，`-text`保留配置hash和换行；未发布实际游戏完整存档/分页/缓存/转储。

- [开工与来源](../START_BASELINE.json)：远端/main、原工作区两文件哈希、实际被审两个Git payload匹配、任务书来源；最初ZIP缺失保留历史，后来补齐见Supplied/。
- [工具快照](Tools/)：Reviewed为修改前源码，Frozen为本次冻结实际运行源码与脚本；SHA256在[最终分层结果](FINAL_RESULTS.json)。
- [原35修改前](Offline/Existing35Before/results.json)：35P。
- [最终58矩阵修改前](Offline/TaskMatrix58Before/results.json)：16P/42F；每例有原始输入、命令、stdout/stderr、summary和assertion，可核对错误PASS/错误资格与诊断不足。
- [新严格检查遇到旧夹具](Offline/Existing35UnchangedAfter1/results.json)：29P/6F；Pending补region的原因与唯一改动详见失败历史，不修改断言期望。
- [冻结原35](Offline/Delivered35/results.json)：35P；不是重新执行Unity。
- [冻结新增58](Offline/Delivered58/results.json)：58P；三阶段12根类型负例及12结构/缺失负例单独列明。注册、合同、身份与晚期技术失败分支不互相冒充。
- [首次历史兼容误拒](History/HistoricalAfter1/historical-comparison.json)：实际Snapshot缺outcome，正确独立结算证据当时未被采用；失败保留，不将其说成原数据被污染。
- [冻结历史只读对照](History/DeliveredHistory/historical-comparison.json)：10组46原案例，828行级与50组级值一致，Source inputManifest未变；原CSV字节一致。
- 对照明细：[旧19](History/DeliveredHistory/Historical19/matrix-summary.json)、[示例主配对组](History/DeliveredHistory/paired-Lake-1/matrix-summary.json)、[示例覆盖组](History/DeliveredHistory/coverage-Ordinary-1/matrix-summary.json)、[完整正常三阶段](History/DeliveredHistory/NormalThreeStage/matrix-summary.json)。其余6组及所有子命令/stdout/stderr在同一History目录。
- [最初测试入口语法错误](Failures/harness-first-error.json)、[错误版脚本](Failures/Test-R2-first-syntax-error.py.txt)；未执行案例，不归因产品。
- 早期51/52/57矩阵各轮尝试与所有摘要保留于Offline/；均是有限离线断言版本，不是扩大真实战斗样本量。
- [分层最终结果](FINAL_RESULTS.json)、[发布清单](PUBLICATION_MANIFEST.json)：不把旧35＋新增58＋46只读案例相加成游戏总PASS。原包已补齐；运行/原生/人工/性能NOT_RUN，历史根因UNRESOLVED。

主要数据集的原始合成输入按原字节保存在各目录`reconstructed-synthetic-inputs.zip`及input-manifest.json中。先解压到新的拥有者目录，再用现有CLI读取其matrix/owner.json，搭配plan.json（原35使用MATRIX_INPUTS.json）写到新的外部输出复核；不要覆盖本目录。这些是本机重建夹具；审核配套原ZIP及其只读对照另存于Supplied/，两者不混用。历史摘要只供审核，不含恢复原始存档所需全部源文件，完整历史CLI复跑需要本机原始拥有者根，不能重建缺失的checkpoint/身份。

- 现代schema不能使用legacy降级：Delivered58的R2-06-no-schema-downgrade。最终工具冻结d5d3fd7c；Tools/FirstFreeze4cc及旧57结果保留为先前尝试。

- [原包接收](Supplied/supplied-package-intake.json)、[476文件核验](Supplied/supplied-package-verification.json)、[原ZIP](Supplied/WanxiangGuitu_S2R1_Review_Evidence.zip)、[原样12观察](Supplied/OriginalPackageReplay/review-results.json)、[同一输入的12候选断言](Supplied/SuppliedCandidateReplay/supplied-comparison.json)。原包未改；初始BLOCKED已解除，不将原脚本观察到缺陷称产品PASS。

- 最终新冻结的Delivered35/Delivered58/DeliveredHistory均重新执行；原包12逻辑观察与提供结果一致见[原样对照](Supplied/original-replay-agreement.json)。原233冻结及57/58初期尝试保留历史。
