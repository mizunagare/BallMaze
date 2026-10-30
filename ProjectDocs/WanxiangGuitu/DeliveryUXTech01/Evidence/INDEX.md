# UX-TECH-01 证据索引

固定制定bee8c58…；开工远端0ab582423c031528d824879a0026e9158f287bfe。以下均本轮独立生成，不继承旧PASS。源文件与构建输入以完整SHA256关联。

- [发布清单与原始/发布SHA256](manifest.json)：528个工程外合成证据文件。原始日志gzip归档，不替换成摘要；只排除缓存、二进制和用户覆盖层。
- [输入/构建/五项用户文件核验](final-bindings.json)，[原用户SHA](user-before.json)，[原始日志异常上下文](log-analysis.json)，[工具语法检查](tool-syntax.json)。
- [修复前9PASS/9FAIL](Before/uxtech.json)、[修复后18PASS](After/uxtech.json)；目录内executed源码/命令/Unity.log.gz/exit.json为各次真实输入。
- [默认/冲突/持久化26项](InputRules/input01-rules.json)。
- [虚拟uGUI与实际消费者239项](InputStory/input01-play-normal.json)、[新Editor进程恢复11项](InputStory/input01-play-resume.json)、[Run身份](InputStory/input01-identity.json)。
- [1280设置](InputStory/input-settings-1280.png)、[1920设置](InputStory/input-settings-1920.png)、[1280 HUD](InputStory/input-hud-1280.png)、[1920 HUD](InputStory/input-hud-1920.png)、[保存失败](InputStory/input-save-failed.png)：受控运行截图，不是原生或人工验收。
- [暂停6项](Pause/pause.json)、[原Editor日志](Pause/Unity.log.gz)：断言PASS同时保留Search异常UNRESOLVED，不能称干净退出。
- [NormalRetry1](NormalRetry1/results.json)、[NormalRetry2](NormalRetry2/results.json)、[NormalRetry3](NormalRetry3/results.json)：正常AI三进程。
- [AI实际业务轨迹](Normal-Gather2/normal-results.txt)、[路径/输入轨迹](Normal-Gather2/normal-ai.csv)、[第一次结算](Normal-Gather2/b4-first-settlement.json)、[checkpoint1](Normal-Gather2/b4-checkpoint-1.json)、[checkpoint2](Normal-Gather2/b4-checkpoint-2.json)、[存档审计](Normal-Gather2/storage-audit.jsonl.gz)。
- [首次构建失败](AcceptanceBuild/results.json)、[首次Player失败](Runtime/results.json)、[首次Player期限异常](Runtime/exception.txt)、[首次正常AI编译失败](Normal1/results.json)、[工具失败](ToolFailures/cleanup-attempts.txt)：不删除、不被后续PASS覆盖。
- [验收构建3原报告/全部99警告](AcceptanceBuild3/build-report-messages.json)、[全部输入](AcceptanceBuild3/build-inputs.json)、[PE/哈希](AcceptanceBuild3/pe-acceptance.json)；实际驱动源码同目录。
- [非开发Player虚拟输入18项](Runtime2/uxtech.json)、[OS退出码0/未强杀](Runtime2/UXTechRuntime.exit.json)、[命令/超时](Runtime2/results.json)、[Boot→Title→NewGame→Gameplay](Runtime2/entry-audit.jsonl.gz)、[Player原日志](Runtime2/Player.log.gz)。该夹具SuspendEntry后退出，不冒充完整退出保存/标题栏验收；v9持久化由InputStory/正常AI另证。
- [纯发行报告/全部96警告](PureBuild/build-report-messages.json)、[全部输入](PureBuild/build-inputs.json)、[无驱动/Editor引用PE检查与二进制哈希](PureBuild/pe-exclusion.json)。没有把构建成功宣称成纯发行原生操作通过。

[完整分层汇总](../SUMMARY.json)与[进程记录CSV](../RUNS.csv)保留各次exitCode、timedOut、命令与状态。Search/JobTempAlloc以及旧UNKNOWN/C15/青色帧未关闭；原生U16、真实设备与独立人工/完整性能NOT_RUN。推送不代表复审通过。

