# CP04-BR2 证据索引

原件根`I:/WGCombat/CP04BR2-1102-A`；独立分支新增资料，不改CP04-B/BR目录。[发布manifest](Raw/manifest.json)记录源SHA、发布SHA、大小和凭据脱敏标记。gzip解压恢复原件（日志仅在有凭据值时例外并标记）。没有上传Unity.dll/PDB、真实存档或测试工程Library；只发布相应身份/分析证据。

## UnityConnect

- [native DLL/PDB GUID、age、SHA](Raw/native-identity.json)，匹配当前6000.6.5f1。
- [原生函数符号](Raw/native-symbols.txt)、[反汇编](Raw/native-disassembly.json)、[解析callee](Raw/native-callees.txt)。首选VA，不是无ASLR假设。
- [服务虚表/实际getter映射](Raw/native-services.txt)、[Crash源码反汇编](Raw/native-service-disassembly.json)、[Crash子调用](Raw/native-crash-callees.txt)、[Cloud字段setter证明](Raw/native-cloud-field-proof.json)。setter仅反汇编，未调用。
- [纯构建](Raw/ConnectBuild/build.json)、[干净不Build控制](Raw/ConnectOpenControl/Connect/001.json)、[控制构建前](Raw/ConnectControlBuild/Connect/001.json)、[首次变true](Raw/ConnectControlBuild/Connect/002.json)、[只读getter](Raw/ConnectGetterAudit/Connect/001.json)。各目录Stages保留五文件原字节与SHA，command/desktop/exit及Unity.log.gz保留过程。
- [精确本轮输出的Bee](Raw/bee-services-current.json)、[消费IL](Raw/bee-services-il.json)、[错误cache归属的纠正](Raw/bee-cache-inventory-note.json)。初始cache inventory不能冒充运行回执。

## 分配与CPU

- [有效232作用域、调用栈/metadata](Raw/Allocation6/scoped-events.json)、[分解统计](Raw/allocation6-analysis.json)。前一成功轮[224作用域](Raw/Allocation5/scoped-events.json)独立保留。
- [Mono进程A](Raw/MonoPlayer/mono-probe.json)、[Mono进程B](Raw/MonoPlayerRepeat/mono-probe.json)，各152；各目录实际command、desktop-process、exit、Player.log.gz。
- [原生桥DLL原字节gzip](Raw/Native/BR2AllocationNative.dll.gz)、[编译日志](Raw/native-compile.log.gz)、[Mono导出](Raw/mono-exports.json)、[运行时模块SHA](Raw/runtime-identity.json)。源代码见Tests，DLL只用于隔离测试，不是产品资产。
- [离线校验器12自测](Raw/validation-selftests.json)、[本轮CPU分布](Raw/cpu-current.json)、[历史BR测量引用](Raw/br-reference-measurements.json)、[源码频率](Raw/frequency-source-audit.json)、[硬件](Raw/hardware.json)。历史引用非本轮PASS。

## 身份、保护、失败

- [产品与历史保护/规范化IL](Raw/protection-and-il.json)、[程序集方法审计](Raw/assembly-audit.json)、[纯发行不含原生桥/驱动](Raw/native-bridge-audit.json)、[probe构建None](Raw/MonoBuild/probe-build.json)。
- [首次缺辅助类日志](Raw/Allocation/Unity.log.gz)、[自有编译失败窗口](Raw/compile-window.json)、[56/224导出](Raw/Allocation3/scoped-events.json)、[完整失败轮Profiler](Raw/Allocation3/scoped-profiler.data.gz)、[140/224导出](Raw/Allocation4/scoped-events.json)。这些失败不被成功轮覆盖。
- [失败历史](../FAILURE_HISTORY.md)、[复跑](../TESTING.md)、[验收](../ACCEPTANCE.md)。本轮没有原生输入、人工体验或完整战斗新结果。

[交付文件/校准/进程证据机械校验](DELIVERY_VERIFY.json)：只证明交付一致性，不代表整体性能或人工验收。
