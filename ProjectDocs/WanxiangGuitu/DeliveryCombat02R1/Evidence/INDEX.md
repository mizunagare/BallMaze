# COMBAT02-R1 证据索引

开工fc11e2a3ee2d3a31254ce7625b7ff9da3a636b5a；产品输入未变。最终证据版本由本文件的Git固定SHA识别。

- [分层汇总](SUMMARY.json)、[验收CSV](ACCEPTANCE.csv)、[6个有效业务进程](Analysis/trials.json)、[42条派生检查](Analysis/checks.json)。
- 原历史佐证：[存储审计](OriginalReference/storage-audit.jsonl.gz)，前11行属于首次失败进程；[原aggregate原值](OriginalReference/aggregate-status.json)。四个原exit1位于OriginalReference/Recovery-*。
- [旧127项锁定文件](Bindings/original-lock-after.json)、[59项原始文件对原发布manifest](Bindings/original-raw-vs-published.json)。原目录没有覆盖。
- [原始输入精度](../INPUTS.md)、[事后存档元数据](Bindings/original-save-metadata.json)。不能把它当原故障瞬间快照。
- [源码358项](Bindings/product-inputs-after.json)、[115个C#源/副本](Bindings/product-csharp-binding.json)、[原/本轮相同Editor产品DLL](Bindings/product-editor-assemblies.json)、[用户5文件](Bindings/protected-after.json)。
- [未减弱的断言片段](assertion-contract.json)：56个Need语法片段含声明，2处Single均相同。不是56个运行时测试用例。

|独立进程|原规则真实结果|实际状态/存储证据|源码/命令/退出|
|---|---|---|---|
|Observed-1|[exit1，匹配复现](Observed/01/Runs/results.csv)|[全快照](Observed/01/Stores/snapshots.jsonl.gz)、[实际存储审计](Observed/01/Stores/storage-audit.jsonl.gz)|[执行C#](Observed/01/Runs/Executed-B07Rules.cs.txt)、[命令](Observed/01/Runs/B07Rules.Run.command.json)、[退出](Observed/01/Runs/B07Rules.Run.exit.json)|
|Observed-2|[exit1，匹配复现](Observed/02/Runs/results.csv)|[全快照](Observed/02/Stores/snapshots.jsonl.gz)、[实际存储审计](Observed/02/Stores/storage-audit.jsonl.gz)|[执行C#](Observed/02/Runs/Executed-B07Rules.cs.txt)、[命令](Observed/02/Runs/B07Rules.Run.command.json)、[退出](Observed/02/Runs/B07Rules.Run.exit.json)|
|Observed-3|[exit1，匹配复现](Observed/03/Runs/results.csv)|[全快照](Observed/03/Stores/snapshots.jsonl.gz)、[实际存储审计](Observed/03/Stores/storage-audit.jsonl.gz)|[执行C#](Observed/03/Runs/Executed-B07Rules.cs.txt)、[命令](Observed/03/Runs/B07Rules.Run.command.json)、[退出](Observed/03/Runs/B07Rules.Run.exit.json)|
|Fixed-1|[exit0，原Run规则完成](Fixed/01/Runs/results.csv)|[全快照](Fixed/01/Stores/snapshots.jsonl.gz)、[实际存储审计](Fixed/01/Stores/storage-audit.jsonl.gz)|[执行C#](Fixed/01/Runs/Executed-B07Rules.cs.txt)、[命令](Fixed/01/Runs/B07Rules.Run.command.json)、[退出](Fixed/01/Runs/B07Rules.Run.exit.json)|
|Fixed-2|[exit0，原Run规则完成](Fixed/02/Runs/results.csv)|[全快照](Fixed/02/Stores/snapshots.jsonl.gz)、[实际存储审计](Fixed/02/Stores/storage-audit.jsonl.gz)|[执行C#](Fixed/02/Runs/Executed-B07Rules.cs.txt)、[命令](Fixed/02/Runs/B07Rules.Run.command.json)、[退出](Fixed/02/Runs/B07Rules.Run.exit.json)|
|Fixed-3|[exit0，原Run规则完成](Fixed/03/Runs/results.csv)|[全快照](Fixed/03/Stores/snapshots.jsonl.gz)、[实际存储审计](Fixed/03/Stores/storage-audit.jsonl.gz)|[执行C#](Fixed/03/Runs/Executed-B07Rules.cs.txt)、[命令](Fixed/03/Runs/B07Rules.Run.command.json)、[退出](Fixed/03/Runs/B07Rules.Run.exit.json)|

每个Stores目录还有scenes.jsonl.gz、observer启动信息、保存前后调用栈、原始b07导航CSV与合成档。Observed保留first-harness-exception.json和exceptions.jsonl.gz完整堆栈；Fixed没有捕获到该异常。原始Unity日志均在相应Runs/Unity.log.gz。所有before/after请求的accepted seed、attempt、fallback、failures在Analysis/*-generation.csv，40请求完整；完整Actor/Brain/Scene实例信息在快照。

## 失败历史

[CompilerFailure/Unity.log.gz](CompilerFailure/Unity.log.gz)保留首版新增观察器CS0619；[前置失败源](CompilerFailure/Trace-before-api-fix.cs.txt)才是该次编译输入。通用运行器在结束时另存的Executed源码只是后置副本，不能据文件名认定已执行。修正API后[编译预检](Compile/results.csv)真实exit0，然后才运行6个业务进程。

[编译失败600秒超时](CompilerFailure/results.csv)没有实际Unity退出码；[清理未退出](CompilerFailure/cleanup-exit.json)、[安全窗口身份拒绝](CompilerFailure/cleanup-guard.json)均不算正常退出。该隔离PID93960仍保留，未强杀。Requested/Executed-OwnedAbort是保存的请求源，没有执行成功回执。

[全部发布文件manifest](manifest.json)记录原始/发布SHA；原始日志仍在工程外拥有者根。压缩及凭据值脱敏不删除异常、错误、失败样本。不提供人工/原生UI/正式Player或性能PASS。原C15、UNKNOWN、青色帧、Search、JobTempAlloc、旧Editor启动阻塞原状态保留；原COMBAT02总表和aggregate仍FAIL。


## 普通夹具与共享准备入口

- Canonical/01～03：不带探针或固定seed的中间普通版，各自源码/命令/结果均保留。
- [最终普通版Integrated-01](Integrated/01/Runs/results.csv)、[02](Integrated/02/Runs/results.csv)、[03](Integrated/03/Runs/results.csv)：双模式最终源3个非batch进程均exit0。各自Executed-B07Rules.cs.txt可对SHA。
- [batch兼容](Batch/results.csv)、[实际最终源码](Batch/Executed-B07Rules.cs.txt)：1次batch真实exit0，原600秒时限。
- [共享准备入口注入SHA](Bindings/prepare-link.json)、[旧入口原字节](Bindings/Invoke-Rules-before.ps1)。只新增Stable映射，不覆盖旧B07历史源。

上述7次与主要同seed3+3诊断分开统计，不冒称正常AI、正式Player或人工。
