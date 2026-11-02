# GC 与 CPU 测量

完整 Player 逐 Solve 字节指标 **NOT_RUN**，不是零。Editor 逐作用域采样已校准，有效范围如下。

## 接口与校准

Unity 6000.6.5f1 / Mono v4.0.30319、64位。GC.GetAllocatedBytesForCurrentThread 在已知 new byte[65536] 下仍返回0，判定不可信。ProfilerRecorder GC.Alloc 的 Value 是 TimeNanoseconds，不是字节；非开发 Player 甚至 recorder 不可用。Physics Queries 的同步 CurrentValue 无法反映已知 Raycast/OverlapSphere/SphereCastAll 控制，查询数 NOT_RUN，不解释成0。

可靠 Editor 方法：ProfilerDriver.profileEditor + RawFrameDataView 在唯一 BRScoped.NNNN 样本的递归子节点中读取 GC.Alloc metadata[0]。它是实际已编译 CombatAim.Solve，未放影子实现，未改 Aim 插桩；委托和记录数组在作用域外创建。场景是独立、可复现的物理夹具，输入复用 CP04-B 实际骨骼发射点，**不是实时动画、实际发射或人工场景**。完整战斗功能另测。

每版本8次空操作、8次正分配、8次释放引用，再4距离各32次Solve（各16次预热）。正控均65568B；空和释放控均0。释放引用是负向控制，不期望“负分配”；GC.Collect在作用域外。152条 marker 与152条raw样本唯一对应，错误0。未用整帧GC减法推导Solve。

依据：[RawFrameDataView](https://docs.unity3d.com/cn/current/ScriptReference/Profiling.RawFrameDataView.html)、[metadata API](https://docs.unity3d.com/ja/6000.0/ScriptReference/Profiling.RawFrameDataView.GetSampleMetadataAsLong.html)、[Recorder options](https://docs.unity3d.com/cn/6000.0/ScriptReference/Unity.Profiling.ProfilerRecorderOptions.html)。原始 profiler.data 压缩归档与导出逐调用事件一并保留。

## Editor 配对结果

同硬件、同几何、同预热/采样配置，顺序运行。表中距离是夹具玩家至目标位置，不等于枪口到表面距离；0.35m修复版仍返回防倒射拒绝原因，此处不宣称极近命中通过。

|版本|距离 m|n|字节 min/median/max|CPU median / p95 μs|
|---|---:|---:|---|---|
|Baseline|0.35|32|2180/2180/2262|64.3 / 80.5|
|Baseline|1.5|32|2516/2516/2516|68 / 84.1|
|Baseline|6|32|3048/3048/3048|72.9 / 93.9|
|Baseline|20|32|3048/3048/3048|70.95 / 88.1|
|Fixed|0.35|32|2180/2180/2262|68.4 / 87.1|
|Fixed|1.5|32|4460/4460/4460|81.65 / 97.6|
|Fixed|6|32|3048/3048/3048|73.15 / 116.8|
|Fixed|20|32|3048/3048/3048|72.15 / 93.4|

[完整校准与分布](Evidence/Raw/editor-allocation-analysis.json)、[Baseline逐调用](Evidence/Raw/Baseline-solve-allocations.json)、[Fixed逐调用](Evidence/Raw/Fixed-solve-allocations.json)。1.5m新安全检查路径比旧提前拒绝路径更多工作，不是同一语义的优化对照。采样有Profiler开销，无未插桩CPU预算结论；没有通过任何产品改动消除分配。

## 非开发 Player

修复版实际真实释放后采样128次Solve，CPU中位数：0.35m 68.55μs、1.5m 96.55μs、6m 79.55μs、20m 69μs；各n32。同步字节计数正控失败、GC recorder UNAVAILABLE，字节全部NOT_RUN，不能填0。

实际并发攻击6模拟秒（720帧）：13次Spawn、峰值5枚，Main Thread正样本中位数3.2152ms；这是整帧并发负载上下文，不能作为逐Solve CPU/GC。真实初始命中33点伤害，Flight3590条、sweep-contact1、resolved1。详细 [player-performance-analysis](Evidence/Raw/player-performance-analysis.json)、[原始probe](Evidence/Raw/FixedPlayers/PlayerProbe/probe.json)。

基线非开发Player出现缺失脚本警告、未完成probe，已用普通WM_CLOSE中断自己的隔离进程。其退出0不是测量成功。基线Player CPU、字节与配对并发比较NOT_RUN，原因未确认，不归咎于产品。无有效GPU、显存或准确逐Solve物理查询数据，不报告性能优良。

## 已知工具风险

早期play-mode profiler捕获532MB但无法LoadProfile；之后基线play-mode15分钟有界超时；错误API导致独立隔离副本Safe Mode，修工具后另开运行目录；均保留。成功 edit-mode 原始 profiler 文件约771/776MB，gzip只作传输，未改变样本。没有用这些工具失败覆盖历史CP04数据。

[失败历史](FAILURE_HISTORY.md)。下一步如必须取得发行Player逐调用分配字节，需要能可靠正校准且提供分配大小的独立事件通道；不修改CombatAim来迎合测量，也不以Editor字节外推Player。
