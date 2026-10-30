# 本轮证据索引

所有运行根为工程外 `I:/WGCombat/EAI01-1030-A`。P/F副本、Library、用户Deferred和发行二进制不进入仓库；以下为拥有合成数据的归档。日志及逐帧jsonl/hp.csv经gzip压缩，manifest同时记录原始与发布SHA256。只读解压查看，不将历史结果覆盖为新运行。

## 版本与保护

- [owner.json](owner.json)：原开工产品SHA49aadd50和拥有根。
- [user-before.json](user-before.json)、[input-binding.json](input-binding.json)：5用户文件原始/最终SHA一致；4产品源与纯构建输入逐字节匹配；14合同源不变。
- [FrozenBefore-inputs.json](FrozenBefore-inputs.json)、[FrozenAfter-inputs.json](FrozenAfter-inputs.json)：最终两版受控运行副本的完整Assets/Packages/ProjectSettings文件清单，包含明确标记的隔离观测注入；不等同纯发行输入。
- BeforeInstrumentation、AfterInstrumentation、FinalInstrumentation：原源/观测源、注入模板和各SHA；FinalInstrumentation对应最终新矩阵和正常AI。

## 修复前后定向证据

| 目录 | 结果与用途 |
|---|---|
| [BeforeRepro/Unity.log.gz](BeforeRepro/Unity.log.gz) | 首次工具编译失败 |
| [BeforeRepro2/repro.json](BeforeRepro2/repro.json) | 原AI实际6PASS/9FAIL，事件见同目录events.jsonl.gz |
| [AfterRepro/repro.json](AfterRepro/repro.json) | 首修13PASS/2FAIL，堵穿透但重定位失败 |
| [AfterRepro2/repro.json](AfterRepro2/repro.json) | 侧移后原15项PASS |
| [LateBeforeRepro/repro.json](LateBeforeRepro/repro.json) | 增加已释放弹体晚进入近战负例，7PASS/10FAIL |
| [LateAfterRepro/repro.json](LateAfterRepro/repro.json) | 首修仍18PASS/1FAIL |
| [FinalRepro/repro.json](FinalRepro/repro.json) | 最终19PASS；动态遮挡、错峰、禁用/暂停，原始events同目录 |

每目录含实际命令、资源门槛、worker PID、退出码/超时、完整日志及当次测试模板。受控场地/定位不当原生操作。

## 独立进程矩阵

- [FinalBeforeMatrix/process-results.json](FinalBeforeMatrix/process-results.json)、[FinalMatrix/process-results.json](FinalMatrix/process-results.json)：各9进程exit0。
- 各 `S418-R0` ～ `S420-R2` 下 `enc-config.json`、`matrix.json`、`Launch/` 和 `Samples/<sample>/events.jsonl.gz`、`hp.csv.gz`；每进程40条件，各360记录。
- [汇总](../SUMMARY.json)、[每条件CSV](../ENCOUNTER_MATRIX.csv)、[真实逐击来源](../HIT_EVENTS.csv)、[360配对](../PAIRED_INPUTS.json)。源码Summarize.py提供分位数、删失及指标口径。
- BeforeMatrix / BeforeMatrixRetry / AfterMatrix保留初始216条件口径及编译、退出分类错误，不混作最终360条件。

## 当前回归与实际业务

- [首次回归结果](regression-processes.json)、[中断](regression-interruption.json)、[原包装器](Failed-Invoke-Regression.ps1.txt)、[未执行项续跑](regression-continuation-processes.json)。17业务阶段均有实际exit0；首次编排中断不删除。
- [EncaiGuard13断言](EncaiGuard-Run/guard.json)：实际导航/警戒/追击返回、只读RNG、弹体生命周期。
- BAL02Rules-Run/rules.json（42）、BAL02Math-Run/math.json（85）、Aim01Rules-Run/rules.json（132）、UX04CombatTiming-Run/combat01.json（188）、Combat03Area-Run/area.json（34）。
- LegacySaveStore/recovery-save.json（2）、LegacyLoadStore/recovery-load.json（9）；原合成v9 Store按字节复制后由新进程正常读取，不改最终编码存档。
- [BossRulesStore/b07-rules.txt](BossRulesStore/b07-rules.txt)：六招/独立身份、39不同布局导航、首杀/重复、Running/Pending/Committed恢复；实际字段快照同目录。
- B07Economy-Run、B3StreamRules-Run、WGB1Routes-Run及[FerryRulesStore/b1-results.txt](FerryRulesStore/b1-results.txt)：经济/随机/路线/费用来源账与新进程恢复。规则探针是受控域验证，不当正常AI Boss胜利。
- [Normal三阶段与构建进程结果](normal-build-processes.json)、[正常AI业务回执](Normal-Gather/normal-results.txt)、Normal-Gather/normal-ai.csv、metadata.txt、完整save审计/expected/actual/结算和[只读观测](Normal-Gather/EncounterObservation/states.jsonl.gz)。目录内截图是Editor AI受控捕获，不是原生或人工。

## 发行与追溯

- [完整构建报告/警告](PureBuild/build-report-messages.json)：Options=None，0错误/96警告。
- [发行PE/哈希](PureBuild/release-inspection.json)：无隔离观测/验收驱动或UnityEditor引用，exe/UnityPlayer/核心程序集SHA。
- [纯构建全部输入](PureBuild/build-inputs.json)、asset-before/after.json：实际URP包路径、版本、输入；[源码绑定](input-binding.json)与之核对。
- [manifest.json](manifest.json)：所发布原始证据路径、原SHA、压缩后SHA与字节数。
- publication-check.json：提交索引的原字节/LFS oid及授权范围检查；不等于独立复审或全部游戏验收通过。

原生U16、独立人工、自然双Boss同场、完整性能和全面Nav故障/抖动计数未执行，见ACCEPTANCE。UNKNOWN、青色帧、Search等历史根因仍UNRESOLVED。没有将构建成功、后台进程退出、机器人或截图标记为人工体验通过。

[result-audit.json](result-audit.json)逐项重审524断言、18矩阵进程、17回归及3正常AI/构建/PE，并对720条件的实际逐击HP与累计计数核对：0.01HP容差内全部一致，最大差0.00390625（浮点累计差），没有用零代替缺测。
