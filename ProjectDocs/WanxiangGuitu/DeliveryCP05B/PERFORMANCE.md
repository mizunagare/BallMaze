# 性能采样与限制

设备日志：Unity6000.6.5f1，非开发Windows Player，D3D12，RTX3060，1280×720独立桌面。不是目标最低硬件；没有获得性能预算。

[原生Profiler采样](Evidence/B3/ScopedPerfEditor/scoped-perf.json)通过Main Thread自定义scope内的GC.Alloc metadata计数，**实际产品方法**，不是影子实现。8组每类校准：正分配65536实际含数组头65568B；零分配与仅释放引用都0B。72个唯一scope全部匹配、无采样错误。释放引用不代表回收负字节。样本包含首次调用；没有删除较慢样本。

|编辑模式查询fixture|样本|B/次范围|平均B/次|Profiler CPU均值ms|
|---|---:|---:|---:|---:|
|OrbitCamera.LateUpdate（含反射调用）|16|96–128|126|0.193413|
|TargetAssist.Choose|16|2340–2340|2340|0.202819|
|原生CombatAim自由Solve|16|3872–4606|3917.875|0.269425|

数据是受控编辑模式查询，含编辑器/反射/冷调用成本，不是正式Player逐帧开销，也不是开启/关闭辅助的整局配对性能。CPU原始Stopwatch另存summary，禁止将本表作为性能达标。TargetAssist候选扫描有0.1秒缓存，但实际物理查询仍分配；以后可单独申请非分配查询优化，当前没有改CombatAim。

最终非开发API Player：100次相机反射调用合计0.3275ms；100次真实目标选择查询合计2.4943ms。只报告测量结果，不根据这两个小样本推导整体FPS。

原线程分配接口校准失败：65536B正分配返回0，Editor/Player原probe该行均NOT_RUN。新增原生Profiler方法只修复Editor独立测量；**Player逐调用GC仍NOT_RUN**。没有把整帧GC当逐调用GC。

GPU Frame Time、长期多弹体并发、主/渲染线程整帧预算、音效声道/纹理内存、动态分辨率、长时间资源增长：NOT_RUN。短战斗轨迹有真实弹体创建/命中/销毁和暂停恢复，不能替代长期性能基准。
