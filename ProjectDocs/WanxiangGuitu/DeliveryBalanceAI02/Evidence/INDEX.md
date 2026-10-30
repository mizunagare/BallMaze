# BAL02 证据索引

本目录均为本轮合成数据，来自唯一拥有根；manifest.json列原始与发布SHA。日志.gz凭据脱敏，hp.csv.gz保留完整逐帧原件内容；不是性能采样。

- [旧规则负例](BeforeRules/rules.json)、[真实防御来源](BeforeRules/defense-sources.json)、[新42规则](AfterRules2/rules.json)、[85边界](Math/math.json)。
- [旧216受控样本](BeforeMatrix/matrix.json)、[新216受控样本](AfterMatrix/matrix.json)；各Samples目录含每次events.jsonl及hp.csv.gz。汇总见交付根BALANCE_MATRIX.csv、HIT_EVENTS.csv、PAIRED_INPUTS.json与SUMMARY.json。
- [旧v9生成](LegacySave/recovery-save.json)、[旧v9原输入](LegacySave/Store/)、[新进程9条恢复/低HP撤离](LegacyLoad/recovery-load.json)。
- [AIM31](AimFrozen/before.json)、[AIM132](AimRules/rules.json)、[时序188](CombatTiming/combat01.json)、[范围34](RangedArea/area.json)、[Boss经济](BossEconomy/b07-economy.txt)。
- [正常AI真实轨迹](Normal-Gather3/normal-results.txt)、[成长只读观测](Normal-Gather3/BalanceObservation/states.jsonl)、[首局检查点](Normal-Gather3/b4-checkpoint-1.json)、[后继检查点](Normal-Gather3/b4-checkpoint-2.json)；[第一进程](NormalLaunch3/results.csv)、[继续/结算](NormalResume3/results.csv)、[后继恢复](NormalFinalResume3/results.csv)。截图仅受控Editor截图，不是原生/人工。
- [验收Player真实Damage](Runtime/Attempts/122815-Observe-b88576/StorageAfter/result-Observe.json)、[逐击](Runtime/ArmorStore/armor-runtime-hits.csv)、[Player完整日志](Runtime/Attempts/122815-Observe-b88576/player.log.gz)、[退出/超时](Runtime/Attempts/122815-Observe-b88576/results.csv)。
- [第二Player恢复](Runtime/Attempts/122910-Observe-30c2f4/StorageAfter/result-Observe.json)、[退出/超时](Runtime/Attempts/122910-Observe-30c2f4/results.csv)、[旧v9夹具输入SHA](Runtime/fixture-inputs.json)。
- [纯发行构建所有消息](Build/Results/build-report-messages.json)、[发行PE/哈希](Build/release-metadata.json)、[发行输入](BuildLaunch/build-inputs.json)；[验收构建消息](Runtime/T/Armor/Results/build-report-messages.json)、[验收输入](RuntimeBuildLaunch/build-inputs.json)。
- [观测前源/观测版及清单](InstrumentBefore/manifest.json)、[新观测源清单](InstrumentAfter/manifest.json)、[P还原](clean-P.json)、[F还原](clean-F.json)、[冻结源与保护](source-bindings.json)、[Git索引绑定](code-commit-binding.json)、[发布字节校验](publication-check.json)、[用户哈希](protection-check.json)。
- 原始工具失败：[AfterRules日志](AfterRules/Unity.log.gz)、[重复类原日志](Normal-Gather/Normal.log.gz)、[失败进程仅正常关闭回执](Normal-Gather/owned-editor-close.json)、[batch等待失败日志](NormalLaunch2/Unity.log.gz)。历史源不覆写。

当前产品521规则断言PASS、受控旧/新各9Run/216样本、正常AI三进程、验收Player两进程分别统计。死亡/删失不隐藏；原生/人工/最终难度/完整性能NOT_RUN，历史引擎根因UNRESOLVED。
