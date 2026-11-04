# 性能数据与测量边界

硬件：i5-12400F（6核12线程）、约47.8GiB物理内存、RTX3060，驱动32.0.16.1742。Unity6000.6.5f1、URP17.6.0、D3D12。Player2请求1280×720，独立非输入桌面显示，非开发构建。另有用户进程/保留测试进程；不是独占机器基准。

真实Unity ProfilerRecorder连续采样180帧，视角是轻载自然地形夹具。没有双Boss、密集战斗、无限流式地形或产品玩家流程。原始首个0样本没有过滤。

|指标|EditorPlay1|Player2|含义|
|---|---|---|---|
|Main Thread均值|2.167ms|16.572ms|整帧标记，包含等待；不是MapMagic节点独占CPU|
|Main Thread p95|3.409ms|16.849ms|相同轻载场景，但Editor与Player帧循环不同，不作优化差值|
|Draw Calls均值 / p95|101.43 / 102|101.43 / 102|原始180帧，含首个0值|
|有效逐次GC|NOT_RUN|NOT_RUN|未完成正分配/零分配校准|
|GPU帧耗时|NOT_RUN|NOT_RUN|未取得有效GPU采样|

Editor整帧GC记录保留，但未经正/零校准，不能当成插件逐次分配。Player的GC计数器无效，未填0。Player1隐藏窗口Draw Calls全0，且截图失败，明确排除为有效渲染性能基准；保留全部原始数据。

生成等待：Generate3的6次实际节点完成时长见seed-results.csv；这是墙钟耗时，包含线程调度/初始化，不是Profiler CPU。EditorPlay1运行时生成seed9137约77.47ms，Player2约79.00ms，同样是单次墙钟观察，不构成统计性能结论。地形只有129×129、128m边长，图为Noise→Height，不代表复杂侵蚀/多区块工作负载。

Build1耗时57.28秒、0错误5警告；Build2增量耗时10.56秒、0错误0条新增BuildReport警告。前5条UAC0005警告没有修复，只因增量编译未再次发出，不能称消除。两轮结束日志都有JobTempAlloc剩余分配警告：**UNRESOLVED**，未确认是Unity、插件、构建流程或夹具；没有修改供应商代码或引擎设置。

Build2输出共105994986字节（182文件），可执行文件667136字节。完整文件和2400项输入哈希见证据。没有可靠加载/卸载内存追踪、纹理显存、过绘、持续多敌战斗样本或目标预算，这些保持NOT_RUN，不推断性能合格。

原始采样：[性能汇总](Evidence/Validation/performance-summary.json)、[Editor CSV](Evidence/Validation/EditorPlay1/main-thread.csv)、[Player CSV](Evidence/Validation/Player2/main-thread.csv)、[Draw Calls](Evidence/Validation/Player2/draw-calls.csv)、[构建日志](Evidence/Validation/Build2/Unity.log.gz)。
