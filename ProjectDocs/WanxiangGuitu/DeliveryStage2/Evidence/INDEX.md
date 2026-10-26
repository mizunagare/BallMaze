# 阶段2证据索引

全部为本轮2026-10-27隔离合成输入；开始da0e14021e595b5d29d7b36e36866d760edf35e3，冻结07ee0e2612c69602b24670f5c8ede53a4396e5d7。交付固定SHA以本文件所在提交/交付消息定位。源码/产品输入、受控规则、Editor正常AI、非开发Player、原生UI、人工判断分开。

## 新完整 All

- [编排逐项JSON](FinalAll/ExistingFramework/ExistingFramework/results.json)、[CSV](FinalAll/ExistingFramework/ExistingFramework/results.csv)：154P/2预期F/3NR/2UR，实际命令、时间、退出码、超时；[协调退出回执](FinalAudit/coordinator-exit.json)。非预期FAIL0，不代表整阶段人工验收通过。
- [100seed CSV](FinalAll/Diagnostics/Rules/stage2-100-seeds.csv)、[20实际seed/21请求](FinalAll/Diagnostics/Rules/stage2-physical.csv)、[393路径/碰撞移动证明](FinalAll/Diagnostics/Rules/stage2-physical-paths.jsonl)、[真实CC尺寸](FinalAll/Diagnostics/Rules/stage2-controller-shape.json)。100纯规则与20受控场景独立，后者AI关闭但敌人碰撞保留。
- [三构筑×四武器真实属性](FinalAll/Diagnostics/Rules/stage2-builds.csv)、[自然失败/fallback/第三候选/全失败](FinalAll/Diagnostics/Rules/stage2-retry-boundaries.jsonl)。
- [19案例57进程逐步结果](FinalAll/Diagnostics/Stage2Matrix/results.json)、[输入和驱动哈希](FinalAll/Diagnostics/Stage2Matrix/execution-inputs.json)。每个`w*-s*`目录有stage2-input、metrics、transactions、process-result和score-normal分项；[冻结计划](../MATRIX_INPUTS.json)、[生成驱动来源](../DRIVER_PROVENANCE.json)、[实际执行源码](FinalAll/ExecutedSources/Stage2Matrix)。
- [逐条量化CSV](FinalAll/Diagnostics/Stage2Summary/matrix-results.csv)、[完整指标/样本均值波动](FinalAll/Diagnostics/Stage2Summary/matrix-summary.json)、[19条数量守恒及拾取/制造装备区分](FinalAudit/transaction-conservation.json)、[Boss阶段时间观测](FinalAudit/combat-observations.json)。不虚构统一货币价值，n1不称平衡完成。
- [两阶段新进程身份/状态摘要](FinalAll/restore-projections.json)：只有合成身份与哈希；实体/装备/来源/RNG在运行时全字段断言，完整save/pages不上传。
- [最终覆盖和192日志索引/143 Search上下文](FinalAudit/final-coverage-and-logs.json)、[全部脱敏完整日志ZIP](FinalLogs/logs-redacted.zip)、[原始/发布SHA映射](FinalLogs/log-manifest.json)。日志不删错误；1个合成负探针和JobTempAlloc/mono诊断另标，不称干净日志。
- [产品源码/输入/546执行驱动SHA](FinalAudit/source-build-provenance.json)、[用户文件保护](FinalAudit/user-input-proof.json)、[正式程序集运行类与测试剔除](FinalAudit/release-cat-check.json)、[276资源原始匹配](FinalAudit/cat-resource-input-check.json)、[全部构建warning标记](FinalAudit/build-warning-lines.json)。六项隔离构建配置差异明示，不宣称输入全字节相同。
- [BuildReport摘要](FinalAll/ExistingFramework/ExistingFramework/build-summary.json)：0错88警告；EXE/UnityPlayer/程序集SHA在最终覆盖JSON；正式无驱动与受控驱动Player不同哈希。
- [最终受控Player15步骤](FinalAll/ExistingFramework/Diagnostics/ControlledPlayer/results.json)：read/continue/new/pending实际回调和自退审计；不冒充原生。
- [环境只读发现](FinalAll/Diagnostics/Stage2Environment/environment.json)：仅用户console，没有独立授权输入会话；原生/四武器人工NOT_RUN。

## 真实运行截图（示例）

- [湖Boss潮矢，Editor正常AI](FinalAll/Screens/Stage2Matrix/w0-s1132820888-Boss-Lake/boss-telegraph-boss-tide-WaterFan.png)。
- [陆Boss真实收益Pending](FinalAll/Screens/Stage2Matrix/w0-s1132820888-Boss-Land/first-settlement-Land.png)：4装备中1件为局内制造，不全叫怪物掉落。
- [寻宝Pending](FinalAll/Screens/Stage2Matrix/w0-s745672572-Gather-Treasure/first-settlement-Treasure.png)。
- [正式无驱动Player已提交档标题](FinalAll/ExistingFramework/ExistingFramework/B09Screens/B09-Title-Committed/title-player.png)。

新增矩阵42张截图；继承出版器另含本次旧功能画面。画面确实来自本次运行，不是人工操作、独立审美或完整性能验收。原有UI/角色表现缺口仍留P0，不因数量测试通过宣称已优化。

## 失败、预跑及发布历史

[失败历史](../FAILURE_HISTORY.md)、[9个尝试根索引](Attempts/INDEX.json)、`Attempts/`下232诊断和40脱敏日志；原始外部根保留。`AttemptPublication1`保留第一次发布工具失败的部分输出。FinalAudit/initial-*保留矩阵尚未结束时的只读观察，不能用其NOT_COMPLETED字段覆盖最终结果。

原始本地完整日志、合成存档与分页留`D:/WanxiangValidationRuns`；GitHub只交脱敏日志/指标/断言投影和实际截图，无Library/Temp/构建/真实存档/转储。新旧失败不得以最终PASS覆盖。原生U16/人工NOT_RUN，UNKNOWN/青色帧/Search根因UNRESOLVED，交付后等待独立固定SHA复审。

暂存校验：[首次缺少21份被忽略日志的FAIL](FinalAudit/staged-check-1.json)、[显式补入后字节/LFS核对](FinalAudit/staged-check-2.json)。这属于证据发布质量检查，不与All游戏测试计数混算。
