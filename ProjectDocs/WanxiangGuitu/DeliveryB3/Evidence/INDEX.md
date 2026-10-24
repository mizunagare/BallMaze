# B3 证据索引

- [SUMMARY](SUMMARY.json)：四轮真实汇总，失败保留；[源码对应](source-provenance.json)：73业务C#与最终副本匹配。
- [Before](Before/REPORT.md)：开始产品代码的耦合回归失败、B1物理路径失败；[原日志ZIP及哈希](Before/Logs)、[对应源码/测试](Before/Sources)。
- [Attempt1](Attempt1/REPORT.md)：噪声/查询已通过，布局比较及旧字段空对象失败；[断言](Attempt1/B3Assertions)、[源码](Attempt1/Sources)、[日志](Attempt1/Logs)。
- [Attempt2](Attempt2/REPORT.md)：旧字段合成存档失败、旧森林失败；[断言](Attempt2/B3Assertions)、[源码](Attempt2/Sources)、[日志](Attempt2/Logs)。
- [Final](Final/REPORT.md)：全新根、37/2/17/1，非预期FAIL0；[完整结果JSON](Final/results.json)、[CSV](Final/results.csv)、各command/exit回执列命令/时间/真实退出码。
- [B3规则断言](Final/B3Assertions/Rules/b3-results.txt)、[固定种子/跨流断言](Final/B3Assertions/Rules/b3-stream-results.txt)、[B2规则](Final/Rules/b2-results.txt)、[正常AI结果](Final/Normal/normal-results.txt)。
- [AI轨迹](Final/Normal/normal-ai.csv)、[初始化到退出审计](Final/Normal/storage-audit.jsonl)、[正常进程结果](Final/Normal/process-result-Normal.json)、[新进程](Final/Normal/process-result-Resume.json)。
- [真实正常AI运行图](Final/Screens)、[PNG及92受控截图哈希](Final/screens.json)、[全部构建文件哈希](Final/build-manifest.json)、[完整规则/构建/UI日志发布版](Final/Logs/logs-redacted.zip)。

原始运行根分别WanxiangB3Before/20261024-115233-bbe26a40、WanxiangB3After/20261024-115548-1b100cb9、WanxiangB3Final/20261024-115953-903a7d7a（这是失败的Attempt2，不是最终结果）、WanxiangB3Verified/20261024-120353-057d1bd3，均位于C:/Users/guan/Documents/unitytest。未删除任何原始失败。

只有Final对应本次最终实现；目录名不赋予PASS。发布日志按白名单脱敏，manifest列转换前后哈希。正常AI与受控规则/截图分开；没有原生U16或人工理解证据，不宣称通过。未上传真实或合成save、分页载荷、转储、构建二进制及缓存。
