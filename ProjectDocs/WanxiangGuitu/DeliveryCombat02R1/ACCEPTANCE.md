# COMBAT02-R1 验收

15 PASS；保留首版工具1 FAIL、6 NOT_RUN、6历史UNRESOLVED。主要对照：3次真实exit1复现、3次真实exit0修复；另7次普通夹具验证独立统计。原始失败不改写，不代表整体游戏或独立复审通过。

|ID|状态|层级|证据与边界|
|---|---|---|---|
|R1-01|PASS|source-review|[归档限定复审，远端/本地开工fc11一致](Evidence/../REVIEW_AND_TASK.md)|
|R1-02|PASS|input-audit|[可重放与缺失状态分开，无伪造旧Run Guid](Evidence/../INPUTS.md)|
|R1-03|PASS|historical-preservation|[127项锁定文件及旧aggregate未变；另59原始源证据未变](Evidence/Bindings/original-lock-after.json)|
|R1-04|PASS|controlled-reproduction|[未就绪夹具3个独立进程均exit1，原Single失败3/3；诊断通过不改写子FAIL](Evidence/Analysis/trials.json)|
|R1-05|PASS|read-only-observer|[PID/Unity/方法/场景/Ready/Run/实体引用/磁盘状态/调用栈完整采集](Evidence/Observed/01/Stores/snapshots.jsonl.gz)|
|R1-06|PASS|causal-classification|[历史路径切换与新保存调用栈/帧序一致，定位夹具先于延迟Start](Evidence/OriginalReference/storage-audit.jsonl.gz)|
|R1-07|PASS|minimal-test-fix|[只等产品初始化及下一实际帧，不改产品恢复/生成](Evidence/../Tests/B07RulesReady.cs.txt)|
|R1-08|PASS|controlled-postfix|[三个独立非batch进程均exit0无超时，原Run全规则完成](Evidence/Fixed/03/Runs/results.csv)|
|R1-09|PASS|contract-diff|[56个Need语法片段（含声明）及2处Single完全相同；360/600秒不变](Evidence/assertion-contract.json)|
|R1-10|PASS|derived-checks|[42项检查通过；观察器不推进四类随机状态](Evidence/Analysis/checks.json)|
|R1-11|PASS|product-and-user-binding|[358项源输入不变、115C#副本及产品DLL一致、用户五项不变](Evidence/Bindings/product-inputs-after.json)|
|R1-12|PASS|compile-preflight|[API读法适配后编译预检exit0，不算业务样本](Evidence/Compile/results.csv)|
|R1-13|PASS|canonical-nonbatch|[最终无探针/无固定seed夹具3个非batch进程通过；普通中间版3次另档](Evidence/Integrated/03/Runs/results.csv)|
|R1-14|PASS|batch-compatibility|[最终普通夹具1个batch进程通过，未放宽600秒时限](Evidence/Batch/results.csv)|
|R1-15|PASS|existing-entry-link|[共享PrepareOnly实际注入与Stable源SHA一致，未启动Unity](Evidence/Bindings/prepare-link.json)|
|R1-H01|FAIL|retained-tool-failure|[首版观察器编译错误/600秒超时，真实Unity exit未知，不计入3+3业务样本](Evidence/CompilerFailure/results.csv)|
|R1-N01|NOT_RUN|scope-or-environment|[原故障瞬间逐字节/句柄完全重放，原始瞬间内存缺失](Evidence/../REPORT.md)|
|R1-N02|NOT_RUN|scope-or-environment|[原生U16](Evidence/../REPORT.md)|
|R1-N03|NOT_RUN|scope-or-environment|[独立人工试玩/可理解性](Evidence/../REPORT.md)|
|R1-N04|NOT_RUN|scope-or-environment|[最终发行Player战斗操作](Evidence/../REPORT.md)|
|R1-N05|NOT_RUN|scope-or-environment|[完整性能/All/正常AI/新构建，本批未要求亦未执行](Evidence/../REPORT.md)|
|R1-N06|NOT_RUN|scope-or-environment|[编译失败Editor93960的安全清理未成功；不强杀，不计正常退出](Evidence/../REPORT.md)|
|OLD-U01|UNRESOLVED|unchanged-historical|[旧C15](Evidence/../REPORT.md)|
|OLD-U02|UNRESOLVED|unchanged-historical|[D3D12 UNKNOWN](Evidence/../REPORT.md)|
|OLD-U03|UNRESOLVED|unchanged-historical|[Editor青色帧](Evidence/../REPORT.md)|
|OLD-U04|UNRESOLVED|unchanged-historical|[Editor.Search](Evidence/../REPORT.md)|
|OLD-U05|UNRESOLVED|unchanged-historical|[JobTempAlloc](Evidence/../REPORT.md)|
|OLD-U06|UNRESOLVED|unchanged-historical|[旧Editor启动阻塞](Evidence/../REPORT.md)|
