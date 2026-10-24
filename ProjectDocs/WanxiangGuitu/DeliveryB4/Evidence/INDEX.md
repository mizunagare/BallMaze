# B4 证据索引

- [完整 All 结果](FinalAll/results.json) / [CSV](FinalAll/results.csv) / [逐项报告](FinalAll/REPORT.md) / [命令与哈希清单](FinalAll/manifest.json)
- [30 seed 拓扑](FinalAll/B4Diagnostics/Rules/b4-topology.csv)；[物理导航、重试实际记录](FinalAll/B4Diagnostics/Rules/b4-physical.csv)
- [旧布局与耗尽查询](FinalAll/B4Diagnostics/Rules/b4-state-results.txt)；[宝箱拾取](FinalAll/B4Diagnostics/Rules/b4-pickup.txt)
- [Gather 三阶段轨迹](FinalAll/B4Diagnostics/Normal-Gather/normal-ai.csv)、[断言](FinalAll/B4Diagnostics/Normal-Gather/normal-results.txt)、[退出定位审计](FinalAll/B4Diagnostics/Normal-Gather/storage-audit.jsonl)
- [Treasure 轨迹](FinalAll/B4Diagnostics/Normal-Treasure/normal-ai.csv) / [Bypass 轨迹](FinalAll/B4Diagnostics/Normal-Bypass/normal-ai.csv)
- 每个 Normal-* 的 b4-checkpoint-1/2.json：合成快照断言、布局/随机流/来源账/仓库/配方；process-result-Normal/Resume/FinalResume.json 记录真实进程结果。不是玩家真实存档。
- [结算合成摘要](FinalAll/SettlementSummaries/)：省略 commit plan，含原始文件哈希；不发布完整 save.json 或 ground-loot 页。
- [完整规则/构建/截图日志脱敏ZIP](FinalAll/Logs/logs-redacted.zip) 与 [原始/发布哈希](FinalAll/Logs/log-manifest.json)
- [构建摘要](FinalAll/build-summary.json) / [所有构建文件哈希](FinalAll/build-manifest.json) / [源码与副本/输入/驱动哈希](Provenance/source-build-provenance.json)
- [本轮截图](FinalAll/b4-screens.json)，包含三张真实运行结算图及实际存在的受控UI选图；[全部92张受控截图哈希索引](FinalAll/screens.json)。未截到的阶段图不补造。
- [正式Player D3D12后台关闭/恢复](FinalAll/B4Diagnostics/Default-1/)；另有Default-2、D3D11-1、D3D11-2。每目录含真实命令/退出、process、timeline、analysis、完整Player日志与审计。不发布 before/after/loaded 保存内容。
- [执行驱动清单](FinalAll/executed-drivers.json)：各阶段实际驱动哈希，区分All准备时副本与之后安装的正常AI驱动。
- [全部定向尝试](Attempts/)：每个唯一目录保留独立 JSON/CSV、日志ZIP和当时测试/关键产品源码快照，包括失败；见 REPORT 的失败表。

原始本地最终根：`C:/Users/guan/Documents/unitytest/WanxiangB4All/20261024-132834-3bcdc2ee`。原始日志继续保留本机；发布副本标记脱敏与行尾规范化，不能宣称原始字节一致。未上传真实存档、凭据、Library、Temp、转储及构建二进制。

截图均为实际Unity运行，正常NPC AI的玩家为领域驱动；没有原生鼠标验收。UI01 UNKNOWN UNRESOLVED、原生U16及人工理解NOT_RUN保持不变。
