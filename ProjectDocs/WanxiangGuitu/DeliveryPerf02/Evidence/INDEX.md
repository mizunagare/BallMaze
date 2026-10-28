# PERF-02 证据索引

冻结输入94dcc009ff971272fc46d8c5b323cbb3251619b5；运行根`I:/WGP2/1028-080504-eef74f`。主归档[Run-1028-080504](Run-1028-080504)，大CSV/log无损gzip，所有行与失败保留，StorageAfter重复内容以精确SHA映射正本。

|内容|路径|
|---|---|
|完整原始/压缩SHA、大小、去重映射|[MANIFEST](Run-1028-080504/MANIFEST.json)|
|逐窗口P50/P95/P99/缺失/CPU/内存|[表格](Run-1028-080504/Analysis/MEASUREMENTS.md)、[JSON](Run-1028-080504/Analysis/summary.json)、[CSV](Run-1028-080504/Analysis/summary.csv)|
|实际LUID/DXGI、PDH/WMI全部状态、GPU Recorder候选|[capabilities](Run-1028-080504/Analysis/capabilities.json)、Runtime/System各例原始jsonl|
|全部帧、边界、Recorder枚举、探针payload/线程/帧时机、截图|[Runtime/Cases](Run-1028-080504/Runtime/Cases)，含C-Probe-R1～R5和9个Title|
|实际OS退出、命令、非活动桌面、原始Player日志/指纹|[Runtime/Attempts](Run-1028-080504/Runtime/Attempts)|
|三份冷导入构建完整报告/日志及实际注入源码|[A](Run-1028-080504/A)、[B](Run-1028-080504/B)、[C](Run-1028-080504/C)，每份ExecutedTools/Results|
|类型/Editor引用/EXE及程序集SHA|[BuildProof](Run-1028-080504/BuildProof)，含初次格式断言失败与重审|
|9窗口+3探针主矩阵，2定向诊断单列|[matrix-results](Run-1028-080504/matrix-results.json)、gpu-diagnostic-exit及gpu-diagnostic2-exit|
|硬件、GPU计数器集、固定Unity API参考|hardware、gpu-counter-sets、gpu-cim-classes、unity-api-reference根文件|
|源码/用户覆盖层/包保护|[ReadOnlyAudit](Run-1028-080504/ReadOnlyAudit)、[source-protection](Run-1028-080504/source-protection.json)|
|有限三类语义审查|[semantic-audit](Run-1028-080504/semantic-audit.json)、semantic-audit-rerun|
|执行工具和诊断版本|[ExecutedTools](Run-1028-080504/ExecutedTools)、[ToolVersions](Run-1028-080504/ToolVersions)、每份构建ExecutedTools|
|准备失败、外部校准、语法/数学测试和退出状态|根setup-first-failure、dxgi-calibration-first-failure、analysis-tests、ps-syntax、process-safety等|

实际Title截图与进程/产物/时间可关联，但不是原生UI/人工验收。所有Player均为临时非开发验收包，不发布二进制/Library/Temp或用户覆盖层正文。CAPABILITIES里保留原始错误；有效样本筛选仅用于统计，不删除原行或把无效0当真。

还原/重汇总及暂存字节完整性回执见本目录VERIFICATION与STAGED_VERIFICATION。没有继承旧PERF01 PASS；旧开放项继续保留，不因本批9窗口完成关闭。

[无损还原核对](VERIFICATION.json)：809个归档文件及251个精确去重副本，共1060个文件原始SHA均通过；还原后的9窗口/5探针完整summary.json与初次汇总逐字节相同。ExecutedTools为矩阵期间初始工具快照，分析阶段最终工具版本以final-tool-identities及当前固定提交源码为准；构建中的实际注入源码由各包ExecutedTools独立记录。
