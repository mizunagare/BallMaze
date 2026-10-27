# PERF-01 证据索引

运行根：`D:/WGPF/1027-224456-e570002e`，开工输入`6f2abca5f89fc80fc5d298623eda12f557654b78`；正式采样分布仅来自本批实际Player，旧PLAYER02证据只作明确的合成输入与复审背景。

主归档：[Run-1027-224456](Run-1027-224456)。大CSV/log无损gzip，MANIFEST保存原始/压缩SHA256与大小；重复StorageAfter按精确SHA映射到正本，没有丢行或覆盖。

|内容|位置|
|---|---|
|完整字节清单与去重映射|[MANIFEST](Run-1027-224456/MANIFEST.json)|
|硬件/驱动/电源只读信息|[hardware](Run-1027-224456/hardware.json)|
|1152项输入与开工Git/用户覆盖层哈希|[ReadOnlyAudit](Run-1027-224456/ReadOnlyAudit)、[最终保护](Run-1027-224456/source-protection.json)|
|新Release构建完整报告与原日志|[Release](Run-1027-224456/R/20261027-224721-Short-9b5789bc)|
|V1/V2校准与V3/V4正式采样构建/临时注入源码|[Runtime/T](Run-1027-224456/Runtime/T)中每个ExecutedTools/Results与哈希|
|发行排除与临时注入证明、exe/程序集SHA|[BuildProof](Run-1027-224456/BuildProof)（每包143模块+PE类型/引用）|
|8×3最终窗口与3次额外OFF的明确名单|[accepted-runs](Run-1027-224456/AnalysisFinal/accepted-runs.json)|
|逐窗口P50/P95/P99、加载、内存、开销|[MEASUREMENTS](Run-1027-224456/AnalysisFinal/MEASUREMENTS.md)、[summary JSON](Run-1027-224456/AnalysisFinal/summary.json)、[CSV](Run-1027-224456/AnalysisFinal/summary.csv)|
|所有大于P99的原始帧索引（不删样本）|AnalysisFinal/outliers.csv.gz|
|每次完整帧、场景/阶段事件、实际业务回执、合成存档/快照、真实截图|[Runtime/Cases](Run-1027-224456/Runtime/Cases)，含校准和全部失败|
|完整Player日志、真实退出码/超时、非活动桌面、命令/输入/保存指纹|[Runtime/Attempts](Run-1027-224456/Runtime/Attempts)|
|精确PID每秒Windows内存/CPU与GPU不可用错误|[Runtime/System](Run-1027-224456/Runtime/System)，早期工具文件占用例的系统CSV仍在Cases中|
|首轮15/7/6与补跑独立结果|[suite-results](Run-1027-224456/suite-results.json)、[recovery-results](Run-1027-224456/recovery-results.json)、console/exit/completion|
|修正前工具/首轮冻结副本|[ToolVersions](Run-1027-224456/ToolVersions)|
|91条完整原文/风险/API/建议/源码行列与SHA|[WARNINGS](Run-1027-224456/WarningAudit/WARNINGS.md)、[JSON](Run-1027-224456/WarningAudit/warnings.json)、[CSV](Run-1027-224456/WarningAudit/warnings.csv)|
|独立导入诊断，不混入91条|[import-diagnostics](Run-1027-224456/import-diagnostics.json)|
|运行时shader/异常日志索引（不裁剪原日志）|[runtime-diagnostics](Run-1027-224456/runtime-diagnostics.json)|
|分析测试、工具语法、归档还原与独立重汇总核对|analysis-validation/identity回执，见MANIFEST列出的根文件|

[归档还原与重汇总核对](VERIFICATION.json)：2,230个原始文件加843个精确去重副本，全部3,073个文件无损还原；37例的14组派生结果完全一致。初版说明误写16组，原件`VERIFICATION_INITIAL.json`保留，修正只涉及说明数字，不改变校验数据或结论。分析数学/缺失/零值8项测试通过，首次7项结果也保留。

[暂存区字节核对](STAGED_VERIFICATION.json)：2,230个归档条目全部与Git index或本机LFS对象一致，包括99个LFS指针；这是本机完整性证明，远端上传与完整HEAD另行核对，不混称已推送。

截图均为隔离非活动桌面的实际Player捕获，例：Gather R1成功与首轮升级弹窗失败、Boss窗口、Loop后继Run；具体路径/时间/产物由Cases与Attempts关联。不能当作原生UI或人工可理解性验收。没有上传Player、Library、Temp、用户场景正文、真实档或凭据。

历史状态不关闭：UNKNOWN/Editor青色帧/Search/JobTempAlloc UNRESOLVED，原生U16/人工NOT_RUN。新发行包警告审计PASS不等于91项已修复，新基线建立不等于性能预算通过。交付后等待独立固定SHA复审。
