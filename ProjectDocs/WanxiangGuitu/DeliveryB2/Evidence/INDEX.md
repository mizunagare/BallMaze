# B2 证据索引

- [汇总与构建/结果](SUMMARY.json)、[72个C#源码对应](source-provenance.json)。
- [Attempt1](Attempt1/REPORT.md)：保留两个非预期失败及两个预期探针，exit1；原始规则/正常AI日志发布副本。
- [Attempt2](Attempt2/REPORT.md)：推荐截断回归失败，exit1；正常AI及新进程通过。
- [Final](Final/REPORT.md)：最终新根，34 PASS / 2预期探针FAIL / 17 NOT_RUN / 1 UNRESOLVED；实际命令/时间/退出码/超时在results及各回执。
- [B2规则断言](Final/Rules/b2-results.txt)、[正常AI结果](Final/Normal/normal-results.txt)、[轨迹CSV](Final/Normal/normal-ai.csv)、[初始化至退出审计](Final/Normal/storage-audit.jsonl)。完整规则/构建/受控UI日志在 Final/Logs/logs-redacted.zip，原始/发布哈希在 log-manifest.json。
- [全部构建文件哈希](Final/build-manifest.json)、[实际正常AI截图](Final/Screens)、[92张受控截图哈希](Final/screens.json)。
- [首轮独立视觉](Visual/results.json)、[最终独立视觉](VisualFinal/results.json)、[逐帧语义回执](VisualFinal/b2-visual.jsonl)、[实际截图](VisualFinal/Screens)、[PNG分辨率/哈希](VisualFinal/screens.json)。mode0=HUD，1=目标详情，2=路线，3=目标详情150%；各720p、1080p。均为受控合成设置、NPC禁用，不能替代原生U16或人工理解。

所有原始运行根留 `C:/Users/guan/Documents/unitytest/WanxiangB2/时间戳-ID`；独立视觉在 WanxiangB2Visual。没有真实玩家存档/转储/构建二进制/Library/Temp上传。发布脚本采用显式诊断白名单和既有脱敏器；不是原始日志字节副本，manifest列出转换前后SHA。

UI-01关闭异常、后台与标题栏边界及65/2/20/1历史仍在 [DeliveryUI01历史索引](../../DeliveryUI01/Evidence/INDEX.md)，本批没有继承它们为新PASS。最终提交和远端完整SHA见交付消息及本文件所在固定提交。
