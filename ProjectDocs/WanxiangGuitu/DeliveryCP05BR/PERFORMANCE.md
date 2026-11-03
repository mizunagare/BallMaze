# 性能基线与优化提案（未修改产品）

固定产品基准、Unity6000.6.5f1、RTX3060、D3D12、1280×720；CPU/OS见[hardware](Evidence/hardware.json)。不预设性能预算。以下是原型训练场有限样本，不是完整森林或长期战斗基准。

## 采样方法和有效性

复用BR2测试专用原生Mono profiler桥（来源提交`28a54a2f0554153e96d15202e4228aee3908241a`）。其gc_allocation回调调用实际mono_object_get_size，在当前线程Begin/End作用域累计，无托管回调，不写产品方法。桥DLL SHA为`08f3ec20924613f58b381d9a52f5a8b464439d8fee17ab621a618227de555f91`。只用于隔离Editor/非开发测试Player，纯发行包没有该驱动/导入引用或DLL。

每进程先做8次65536B正分配、8次零动作、8次释放引用校准：正控实际65568B含数组头；零/释放引用控为0，invalid事件0。这里的0只用于校准，**产品方法均有实测非零分配**。旧线程接口返回0的无效结果未被改写。

最终Editor 1,116条：24校准、448逐查询、644个Update-to-EndOfFrame区间。472个完整query/control作用域同时与Unity Profiler CPU/GC metadata比对，全匹配、缺失0、字节差异0。PlayerFinal 2,172条、Repeat 2,215条、Gated 2,223条，原始正/零校准均通过。帧数因不锁帧率而不同，不能把不同采样数量直接解释为性能提升。

每组方法16次；相机通过反射调用，明确含反射开销；Fade.Refresh为真实渲染状态更新；Choose执行真实只读目标/物理查询；另有实际RaycastAll、SphereCastAll控制组。表中的elapsed是Stopwatch墙钟，不能称Player线程CPU或GPU帧时间。Editor另有真正Unity CPU scope值。Profiler事件本身有观测成本，未测得完全无插桩差值，不能据此判断最终FPS。

六种场景为自由、仅肩后、肩后+远程、全部辅助、双敌真实移动、十活敌及连续实发弹体。前四种为固定视角静态查询fixture；全部辅助在Staff下开启两个flag，**不代表同时执行了剑枪面向逻辑**。双敌初始摆放在隔离夹具中避免被障碍挡住，最终两者均水平移动>0.05m；没有改AI参数。密集场景保留全部碰撞，朝空闲方向实际开火，至少4秒/240区间，不注入Damage，不以杀敌作为该渲染负载的验收。原杀敌空引用作为独立FAIL保留，没有将朝空闲方向发射宣称为修复该缺陷。

下表由原始采样生成，EditorFinal与PlayerFinal中位值；完整n/mean/min/max/p95见各analysis.json。模式之间目标可见性、淡化命中、演员移动和初始稳定帧不同，只能描述当次负载，**不能据此声称单一开关的因果性能收益**。

|模式/方法（每组16次）|Editor中位B|Editor elapsed μs|Player中位B|Player elapsed μs|
|---|---:|---:|---:|---:|
|free/camera-reflection-inclusive|208.0|29.65|208.0|19.25|
|free/fade-refresh|18868.0|301.3|18868.0|164.45|
|shoulder-only/camera-reflection-inclusive|208.0|30.6|208.0|21.1|
|shoulder-only/fade-refresh|1876.0|180.95|1876.0|123.05|
|shoulder-ranged/camera-reflection-inclusive|208.0|29.75|208.0|20.35|
|shoulder-ranged/fade-refresh|1876.0|176.1|1876.0|107.6|
|shoulder-ranged/target-choose|4512.0|73.7|4512.0|38.7|
|all-assists/camera-reflection-inclusive|208.0|30.9|208.0|22.55|
|all-assists/fade-refresh|1876.0|176.45|1876.0|111.0|
|all-assists/target-choose|4512.0|73.9|4512.0|40.05|
|two-moving/camera-reflection-inclusive|208.0|22.6|208.0|14.0|
|two-moving/fade-refresh|1876.0|200.4|1876.0|136.75|
|two-moving/target-choose|216.0|41.1|216.0|18.05|
|ten-moving-projectiles/camera-reflection-inclusive|208.0|25.2|208.0|18.0|
|ten-moving-projectiles/fade-refresh|1876.0|200.45|1876.0|148.4|
|ten-moving-projectiles/target-choose|216.0|45.85|216.0|24.55|

Update-to-EndOfFrame区间不覆盖该帧所有早期Update，含测试协程/呈现观察成本，**不是整帧CPU或完整AI成本**。不能将逐方法微基准之和当作真实整帧。四秒属于有限连续样本，不是长期稳定性测试。

## 源码对应与风险

- OrbitCamera：横移/后臂/连续位移SphereCastAll，以及ClearAt的OverlapSphere产生数组；相机调用样本包含反射成本。没有删除避障或真实碰撞。
- CameraActorFade：每次Restore读取sharedMaterials数组并对每个材质使用LINQ查找；Refresh有HashSet、命中/重叠数组、三个高度数组、Renderer数组；淡化时为每Renderer创建材质数组。居中遮挡实际中位18868B/调用，清晰肩后1876B/调用。材质副本按源材质缓存，但数组和查询仍每次分配。
- TargetAssist：0.1秒缓存候选集合，候选验证仍逐次RaycastAll/InitialContact/Sweep；后两者复用冻结CombatAim helper中的数组/LINQ路径。4512B和216B样本差异主要来自合法候选/遮挡/视野，不能把216B当作普遍上限。目标扫描缓存与实际每帧预览/释放求解不是同一个频率。
- 每阶段记录Resources.FindObjectsOfTypeAll材质数、fade拥有数与Renderer数；场景用完整销毁/卸载/重新创建隔离。短样本中的材质增加是观测，尚不能证明永久泄漏或长期无泄漏。

## 等待授权的最小优化方向

1. 先减少Fade的LINQ闭包/重复sharedMaterials和Renderer数组，保留恢复所有权、材质颜色/透明度及OnDisable/Destroy清理；缓存需在模型/场景变化时失效。需要授权CameraActorFade.cs。
2. 再评估相机有上限的NonAlloc查询；缓冲溢出必须完整fallback，保持全部遮挡。需要授权OrbitCamera.cs；不能截断命中来降低开销。
3. TargetAssist候选刷新及RaycastAll改动必须保留原评分、滞回、顺序与同次释放新鲜枪口检查。暂不提议改变刷新周期、预览频率或CombatAim。

以上没有实施，也不承诺省下多少字节。未来须同输入/同可见性做配对，并验证墙体、目标切换、实际命中及缓存失效。本批原生物理输入、长期并发、完整森林/首领、整帧Main/Render Thread、GPU、性能预算均NOT_RUN；不能从原生分配采样推导人工手感或整体性能通过。
