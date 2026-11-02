# 失败、修正与未执行项

旧CP04-B/BR证据均只读。新输出独立目录，不用后续成功覆盖失败。

|尝试|原始结果|处理|
|---|---|---|
|Allocation|缺CP03Cases辅助类，CS0103，Safe Mode|保留Unity.log/编译窗口；补齐现有辅助类。只普通关闭身份核对的自有测试对话框，不算原生验收|
|Allocation2|重启时旧进程尚未结束，预启动占用阻断|未启动第二个Unity，不强杀；等旧进程退出后另开Allocation3|
|Allocation3|进程0但仅56/224 raw作用域|INCOMPLETE，不采信工具旧的“有样本即成功”；完整Profiler原件也归档|
|Allocation4|进程1、140/224作用域|INCOMPLETE；采样同时导出导致导出器自身被分析，帧保留窗口不足；不作为有效配对|
|Allocation5|224/224，控制有效|采集和解码分离，停止Profiler后读取原始metadata/调用栈，另开目录保留旧失败|
|Allocation6|232/232，控制有效|新增8条旧fallback方向公共helper测量，解释532B剩余差额；未改旧Solve|
|native符号工具|非零模块基址并成功枚举；GetLastError遗留487|成功API后last-error不定义，不把该旧值当加载失败；另用PE/PDB GUID/age核验匹配|
|接口清点|首次查询不存在ProfilerModule.dll|实际API位于CoreModule，清点失败不是测量0|
|托管服务查询|首个PowerShell查询未执行成功|以FindManagedServices.ps1重跑，保存明确IL，不猜测结果|
|服务触发假设|最初怀疑普通Insights getter直接为true|实际getter为0，已否定；CrashReporting覆写getter为1，进一步读取EngineDiagnostics/旧Cloud字段定位桥接|
|Bee缓存归属|初始宽泛glob包含继承cache，并以所在工程标签归类|保留初始inventory但不能用于构建身份；以DestinationPath精确匹配本轮输出，另写current文件|
|构建与关闭日志|obsolete、JobTempAlloc等警告|原日志全保留，不过滤、不降低断言、不试探修改产品生命周期|

[初始编译日志](Evidence/Raw/Allocation/Unity.log.gz)、[窗口](Evidence/Raw/compile-window.json)、[56/224](Evidence/Raw/Allocation3/scoped-events.json)、[140/224](Evidence/Raw/Allocation4/scoped-events.json)、[完整原Profiler](Evidence/Raw/Allocation3/scoped-profiler.data.gz)、[缓存归属纠正](Evidence/Raw/bee-cache-inventory-note.json)。

原生写入硬件调用栈、真实网络载荷/同意行为、未插桩发行完整性能、原生输入和人工体验没有执行。旧D3D12等未解决项保持原状。所有新工具只在隔离环境中运行；没有产品修复或历史结果重分类。
