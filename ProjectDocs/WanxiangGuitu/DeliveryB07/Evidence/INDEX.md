# B07 运行证据索引

最终完整 All 的目录在报告中记录；本页的 FinalAll 链接只指向该轮，不拼接旧通过项。所有存档为工程外隔离的合成数据。仓库没有玩家原档、ground-loot原页、Library、Temp、构建二进制或转储文件。

## 最终记录

- [完整命令、时间、退出码、超时及分类](FinalAll/results.json)、[CSV](FinalAll/results.csv)、[统计](FinalAll/counts.json)。两个预期负探针仍为FAIL，不改成PASS。
- [实际冒险、收益、进程与限制摘要](FinalAll/review-summary.json)。这里的Player记录是非开发构建启动、后台WM_CLOSE及新进程恢复，不是物理标题栏或原生键鼠验收。
- [80个产品脚本、注入测试与实际执行驱动的冻结输入证明](FinalAll/frozen-product-proof.json)。源脚本快照保留原字节；普通日志按清单脱敏和转UTF-8，原始/发布哈希分别记录。
- [源工程、隔离副本、全部构建输入及实际驱动哈希](FinalAll/Provenance/source-build-provenance.json)、[构建文件清单](FinalAll/build-manifest.json)、[构建摘要](FinalAll/build-summary.json)。不能只凭exe存根判断业务程序集一致。
- [受控命中子用例](FinalAll/combat-case-results.csv)、[逐攻击真实命中记录](FinalAll/B07Diagnostics/Rules/b07-hits.csv)、[逐攻击中断与恢复时钟](FinalAll/B07Diagnostics/Rules/b07-interrupts.csv)。
- [Editor隔离种子一次性探针](FinalAll/B07Diagnostics/Rules/b07-seed-replay.txt)：正式Player编译剔除入口，失败陆地种子在出征前固定，不改存档或在途种子。
- [Boss规则、故障与新进程恢复](FinalAll/B07Diagnostics/Rules/b07-rules.txt)、[导航种子数据](FinalAll/B07Diagnostics/Rules/b07-nav.csv)、[满包与重复收益](FinalAll/B07Diagnostics/Rules/b07-economy.txt)、[受控AI活性](FinalAll/B07Diagnostics/Rules/b07-liveness.txt)。
- [B07完整Editor日志](FinalAll/B07Logs/logs-redacted.zip)、[通用完整日志](FinalAll/Logs/logs-redacted.zip)。日志不删除异常；脱敏仅处理凭据，清单记录发布变化。

## 正常 NPC AI 冒险

| 策略 | 完整步骤与断言 | 行走/生命/材料轨迹 | Boss状态与攻击请求 |
|---|---|---|---|
| 陆地 | [Land](FinalAll/B4Diagnostics/Normal-Land/normal-results.txt) | [轨迹](FinalAll/B4Diagnostics/Normal-Land/normal-ai.csv) | [全首领状态](FinalAll/B07Diagnostics/Normal-Land/boss-world.csv)、[所选目标](FinalAll/B07Diagnostics/Normal-Land/boss-combat.csv)、[攻击请求](FinalAll/B07Diagnostics/Normal-Land/attack-actions.csv)、[翻滚](FinalAll/B07Diagnostics/Normal-Land/dodge-actions.csv) |
| 湖中 | [Lake](FinalAll/B4Diagnostics/Normal-Lake/normal-results.txt) | [轨迹](FinalAll/B4Diagnostics/Normal-Lake/normal-ai.csv) | [全首领状态](FinalAll/B07Diagnostics/Normal-Lake/boss-world.csv)、[所选目标](FinalAll/B07Diagnostics/Normal-Lake/boss-combat.csv)、[攻击请求](FinalAll/B07Diagnostics/Normal-Lake/attack-actions.csv)、[翻滚](FinalAll/B07Diagnostics/Normal-Lake/dodge-actions.csv) |

`boss-combat.csv`：时间、目标ID、状态、攻击、Boss生命、主角生命、实际释放数。`boss-world.csv`：时间、阶段、ID、状态、攻击、生命、释放数、x、z。攻击请求不是逐次命中归因；翻滚记录只在原TryDodge确实成功时写入。主角生命可能因实际升级或药水改变，不是覆盖生命。

该分类为隔离Editor内正常怪物AI和领域机器人，非人工操作、非最终Player原生战斗。敌人没有冻结，也没有直接设置胜利。初始合成物资及装备选择见TESTING。

## 截图与正式 Player

- [正常AI截图清单](FinalAll/b4-screens.json)：`Screens/Normal-Land`、`Screens/Normal-Lake`中的实际前摇和结算截图。
- [受控命中/四武器截图](FinalAll/b07-screens.json)：`B07Screens`。受控截图不能冒充正常AI、原生输入或人工试玩。
- 正式Player：`B07Diagnostics/B07-Land`与`B07Diagnostics/B07-Lake`保存两次启动的完整Player日志、process退出码/超时/强杀标记、timeline、analysis、b07-analysis与storage-audit。通用Default/D3D11 cell同样保留在FinalAll根下对应目录。
- [独立证据校验](Checks/final.json)：文件、压缩包CRC、发布哈希及禁止上传内容检查；不是玩法验收统计。

## 首次失败与每轮尝试

[完整失败说明](../FAILURE_HISTORY.md)。`Attempts`保留BeforeEntry、BeforeModelPartial、BaselineProbe、Directed1～4、CombatDiagnostic1～5、Composite1、Normal1、FixturePatch1、ReportLock1～2、GuardBefore/Before2/Before3/After、RecoveryBefore/After、RuntimeRestore/Restore2、AttackConditions/Conditions2/Conditions3、SeedBefore/After及各轮All。每个目录有独立结果、日志与源码说明，后续通过不覆盖历史失败。

部分早期增量诊断复用了已经结束的测试工程，不冒充干净重导入。原始产品源码快照与从Git重构的测试文本在各自source-snapshots/SCOPE中明确区分。模板owner描述有偏差的目录附纠正说明，不修改原日志。

UI-01历史65 PASS、2预期FAIL、20 NOT_RUN、1 UNRESOLVED及环境边界证据保留。D3D12 UNKNOWN、原生U16、人工可理解性分别保持UNRESOLVED、NOT_RUN、NOT_RUN；B07不会关闭它们。

最终轮补充：[Editor异常分类](FinalAll/exception-inventory.json)、[构建警告行索引](FinalAll/build-warning-lines.json)、[正式程序集剔除Editor入口](FinalAll/release-editor-hook-check.json)。最终All为115 PASS / 2预期FAIL / 27 NOT_RUN / 1 UNRESOLVED，0非预期失败；原生与人工项目保持开放。

[Git暂存证据字节复验](Checks/staged-bytes.json)及[首次换行差异](Checks/staged-bytes-before.json)均保留；这是交付工具检查，不计入游戏All。
