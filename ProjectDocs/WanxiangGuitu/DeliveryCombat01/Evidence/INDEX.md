# COMBAT-01 证据索引

本轮归档：[Run-1028-093640](Run-1028-093640/analysis.json)。开工SHA `d37b9ba98deea109fa67900314a2f6864b24c98a`；最终源码以本索引所在固定SHA为准。执行环境Unity6000.6.5f1，Windows隔离副本与合成存档。

| 证据 | 路径 | 说明 |
|---|---|---|
| 审计汇总与输入哈希 | [analysis.json](Run-1028-093640/analysis.json) | 1152项产品输入、仅4项产品变化、5项用户文件保护、两最终构建完整消息、旧新条件对应 |
| 完整结果索引 | [results.csv](Run-1028-093640/results.csv) | 分层逐项，不把不同统计单位合并 |
| 发布原件清单 | [manifest.json](Run-1028-093640/manifest.json) | 1143个原件；原始SHA与发布SHA，超时仍活动日志明确partialSnapshot |
| 开工源与任务 | [Inputs](Run-1028-093640/Inputs/) | 工作区、输入SHA、原任务，未复制用户场景内容 |
| 原负例 | [Baseline2/combat01.json](Run-1028-093640/Baseline2/combat01.json) | 92 PASS /33 FAIL；运行原版本代码 |
| 最终受控检查 | [After4/combat01.json](Run-1028-093640/After4/combat01.json) | 188 PASS；固定418、真实Physics和HP；不是正常AI或原生输入 |
| 受控时序截图 | [After4](Run-1028-093640/After4/) | startup-0～3、active-0～3-0/1；空中几何夹具不冒充森林体验 |
| 受控退出/日志检查 | [After4/results.json](Run-1028-093640/After4/results.json) | 规则与原始日志分开检查；Search与JobTempAlloc仍开放 |
| 历史回归和正常AI | [Regression1/results.json](Run-1028-093640/Regression1/results.json) | Editor受控3过程、正常AI3过程；每项实际退出码和超时 |
| 正常AI完整身份与来源账 | [Normal-Gather](Run-1028-093640/Regression1/Normal-Gather/) | 采集、渡口、结算、制造、再次出征及跨进程恢复 |
| 首次Player失败 | [Story/result-Main.json](Run-1028-093640/Story/result-Main.json) | 忽略升级UI导致采集超时；原失败快照/轨迹保留 |
| 最终Player六阶段 | [Attempts](Run-1028-093640/Attempts/) / [Story2](Run-1028-093640/Story2/) | 与旧失败分别保存；实际虚拟输入和运行时代码，不是原生U16 |
| 来源账与经济核账 | [story-business.json](Run-1028-093640/ProductIdentity/story-business.json) | 23 PASS，真实收获、消耗、入仓、制造及恢复 |
| 纯发行驱动剔除 | [proof-Release.json](Run-1028-093640/ProductIdentity/proof-Release.json) / [all-modules-Release.json](Run-1028-093640/ProductIdentity/all-modules-Release.json) | BuildOptions.None，0错93警告，143程序集检查 |
| 临时验收构建 | [proof-Acceptance.json](Run-1028-093640/ProductIdentity/proof-Acceptance.json) | T3：0错116警告；驱动只在隔离副本 |
| 实际发行标题 | [title-player.png](Run-1028-093640/ReleaseSmoke/title-player.png) | 实际无驱动非开发Player，不是概念图或Editor对象 |
| 关闭超时 | [process.json](Run-1028-093640/ReleaseSmoke/process.json) | FAIL；WM_CLOSE非原生标题栏关闭，无强杀、无伪造退出码 |
| 额外Editor启动阻塞 | [Baseline3/results.json](Run-1028-093640/Baseline3/results.json) / [SaveRun/results.json](Run-1028-093640/SaveRun/results.json) | 600秒超时，战斗用例未执行；原进程保留 |
| 残留测试进程记录 | [owned-processes.json](Run-1028-093640/Inputs/owned-processes.json) | 只记录本轮拥有者根，不关闭用户程序 |

完整Player日志、Editor日志、命令、开始/结束时间、退出码、超时、合成存档和运行源码均在对应目录。`.log.gz` 是原日志的无损压缩，`gzip` 解压后与manifest原始SHA一致，不是过滤后的日志。

复核发布原件：`python -B verify_evidence.py Evidence/Run-1028-093640`。不需要访问原机器的真实存档，不安装或升级依赖。该离线校验不是新的Unity运行。

原生U16、独立人工、完整性能预算、历史引擎根因均保持原状态。详见[ACCEPTANCE](../ACCEPTANCE.md)；推送不等于复审通过。
