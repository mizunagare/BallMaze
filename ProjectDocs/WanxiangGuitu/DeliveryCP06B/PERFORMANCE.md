# 性能测量范围与校准


实际硬件i5-12400F/RTX3060，Unity6000.6.5f1；完整硬件见Evidence/hardware.json。复用既有BR2原生Mono分配事件桥，仅隔离测试包加载，纯包无桥。


Editor：8次零分配与8次正分配65536B校准通过；Player：零动作观测48B而非0，校准失败，原始16样本保留。**最新Player CPU/GC NOT_RUN**。不将功能37 PASS、无效0或正分配失败当作性能通过。


实际计量是LateUpdate执行顺序160..180包含NewWeaponCombat175的主线程区间，Profiler标记加Stopwatch/事件回调。包含区间内物理/音效/反馈与观测开销；不含请求前分配、地波Update全飞行、整帧、GPU或纯发行完整开销，不是每次攻击总分配。


|Editor场景|有效区间帧数|p50 ms|p95 ms|max ms|区间累计GC B|

|---|---:|---:|---:|---:|---:|

|Greatsword/basic|126|0.1129|0.1840|3.1931|363598|

|Greatsword/skill0|173|0.1197|0.1894|1.1383|500416|

|Greatsword/skill1|175|0.1224|0.1902|1.3094|503188|

|Scythe/basic|85|0.1243|0.1612|0.7936|246960|

|Scythe/skill0|149|0.1307|0.2049|0.8038|447944|

|Scythe/skill1|98|0.1310|0.1909|1.4170|291380|

|TwinBlades/basic|39|0.1059|1.7852|3.5104|115210|

|TwinBlades/skill0|130|0.1137|0.1778|1.2834|409950|

|TwinBlades/skill1|69|0.1135|0.1772|0.9450|207364|


原始样本/校准/事件计数见Evidence/PerformanceFinal4/performance.json，Player失败见Evidence/PlayerPerformanceLatest4/performance.json，汇总见Evidence/FinalAnalysis2/performance-summary.json。未过滤失败/峰值。


并发多敌、多特效、GPU/显存、整帧主线程及渲染线程、持续音效回收和长时间资源变化仍NOT_RUN。功能测试只确认短序列结束与场景重建后的有限资源回收。未确定目标硬件预算，不自设通过阈值；简化生成图形/音效不是性能保证。
