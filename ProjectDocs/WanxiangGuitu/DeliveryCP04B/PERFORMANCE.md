# 实测性能与缺项

硬件：i5-12400F、RTX3060、既有Windows/Unity6000.6.5f1，1280×720、独立非活动测试桌面，无硬件独占。hardware.json、日志与每轮实际命令保存。固定120Hz模拟不等于120FPS性能预算。

## Solve查询和CPU

测试克隆只把三种Physics调用替换成原API计数包装器；原始/修复克隆的精确变换审计通过，不改命中规则。最终使用真实释放事件记录的杖首坐标冻结输入，避免最早Idle枪口微基准遗漏负投影分支；旧数据不删。

1.5m负投影：旧实测每次1 RaycastAll、2 OverlapSphere、2 SphereCastAll；修复实测1、3、3。0.35m实测1、2、0；6/20m为1、2、2。实际产品未插计数器，其对应查询数量不冒称直接采到；由同逻辑的精确克隆测量，并独立计时实际CombatAim.Solve。

每单元128次、预热32次，每条件一个批次。Editor同进程计数克隆的1.5mProfiler每调用约12.762us（旧）与16.929us（修复）；跨进程实际产品Profiler约10.679us与18.113us。原始Stopwatch、Profiler整批纳秒及每格全部数据见PerfAnalysis，不删37.5us等离群样本。不能把单批差异当精确产品成本或性能达标，包装器/Recorder也有开销。

## 并发实际弹体

前后实际产品各6模拟秒约720帧，12次真实Spawn、峰值5个在飞弹体；Main Thread有效718帧，中位数约7.5302ms/7.62455ms。非开发Player另有独立采样。该值含渲染、Observer、查找与场景开销，不是单独Projectile.Update成本，也不是完整战斗性能预算；不宣称优化收益。

## GC与Profiler可用性

已知new byte[65536]保留引用，线程分配API仍返回0：逐Solve字节NOT_RUN，最终receipt以-1+NOT_RUN_CALIBRATION_FAILED标记，raw0另存；最初未校准raw0不作为通过依据。Editor内部GC.Alloc句柄可用、整帧GC可读，仍未可靠归属每次Solve字节，不拿整帧值替代。非开发Player的线程/整帧GC不可用，NOT_RUN。

非开发Player自定义Solve Profiler marker不可用，因此其marker耗时NOT_RUN；实际Stopwatch计时和Main Thread Recorder另行保存，不冒称同一指标。理论估计和对象数上限没有填入Profiler结果。

因此测量收集部分完成，GC指标未完成；性能不宣称全面通过。

采样器的variant字面量fixed-real在BeforePerfFrozen指当轮真实旧产品，在AfterPerfFrozen才指修复产品；以phase与CombatAim.executed.cs.txt为版本依据。baseline-counted/fixed-counted始终是两份对应只读计数克隆，不混淆为当轮产品代码。
