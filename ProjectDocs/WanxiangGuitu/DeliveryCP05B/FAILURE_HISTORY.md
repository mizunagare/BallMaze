# 失败与未完成记录

原始I:/WGCombat/CP05B-1103-A下输出未覆盖；仓库镜像日志采用gzip，脱敏字段及前后SHA见各manifest。以下失败不能被后续PASS覆盖。

|尝试|实际情况|后续/结论|
|---|---|---|
|B1 Smoke1|训练没有AdventureFlow，CameraActorFade空引用；exit0不能证明成功|训练分支使用实际训练敌人，后续Smoke4无该异常|
|B1 Editor1|驱动组件在Editor程序集，协程未完成，超时/exit1|驱动移到隔离runtime程序集；Editor2完成|
|B1 Build3|移除Probe后Editor runner仍引用，编译失败|纯包同时移除两者，Build4成功|
|B2 Player1|跨Boot/Title驱动被销毁，缺少probe.json|INCOMPLETE；DDOL修复测试工具，运行器强制检查语义回执；Player2重跑|
|B3 Editor1|复制热Library后旧脚本GetClass缺失，Prefab组件缺失，未完成|普通关闭owned Editor，无强杀。AssetAudit3保留FAIL；ColdAssetAudit同四份源码SHA成功。内部引擎缓存根因未定位|
|B3 audit前两次|Unity占用门槛拒绝启动|工具阻断，不能记为Unity测试PASS；未重复启动第二个开发循环|
|CameraJumpBefore|目标跨50m后镜头缓存仍被中间墙挡住，实际离角色26.61238m|位置断点重锚定；After 6.85587m PASS|
|B3早期152 PASS|转向预算只检查内部累计，证据强度不足|没有覆盖这些旧PASS；增加实际起始/释放四元数角度断言|
|YawBeforePlayer|极小delta下Quaternion.Angle丢失小步进，内部0、实际20.61202°；exit1|标量yaw累计修复，YawAfter实际20.00013°/累计20°；真实伤害41.25不变|
|GC线程计数|正分配返回0|原行仍NOT_RUN；Editor另有原生Profiler校准，Player仍NOT_RUN|
|B2/B3 Player图像|B2十张/B3七十一张全黑|UNRESOLVED；保留原件，不作有效画面证据；Editor短序列独立标注|
|B1套用B3程序集矩阵|B1尚没有B2新增TargetAssist类型，通用八类型矩阵报告FAIL|保留assembly-b1-exclusion.json原结果；另做仅驱动排除检查b1-driver-exclusion.json PASS，不用该PASS冒充B1有软锁定|

最终EditorFinal/PlayerFinal各157 PASS、1 NOT_RUN，独立YawAfter16 PASS/1 NOT_RUN；不是清除上述FAIL的依据。历史法杖失败、D3D12 UNKNOWN、青色帧、C15及所有更早分支证据均保留。没有修改历史JSON，没有合并main。
