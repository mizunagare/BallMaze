# 已复现和已定位；产品仍UNRESOLVED

原案例w2-s0-near、w2-s1-near在未改产品的真实Editor中再次得到hpLoss=0、CAMERA_SURFACE_BEHIND_MUZZLE。[原始断言](Evidence/Historical/presentation.json)、[三维原始记录](Evidence/Historical/aim-diagnosis.jsonl.gz)、[原始Spawn/Flight/Damage](Evidence/Historical/events.jsonl.gz)、[分析](Evidence/Analysis/analysis.json)。291 PASS与2 UNRESOLVED保留；R1.3分类器将进程PASS/0与整体BLOCKED/2正确分开。

因果链：相机中心射线首个合法命中是目标CharacterController，而非地面或墙；动画实际杖首枪口位于另一位置。CombatAim.Solve对 `Dot(cameraHit - projectileOrigin, cameraRayDirection) <= .001` 作防倒射判定。两样本投影为-0.272345155m与-0.239441678m，因此抛弃该目标表面，将发射方向改为相机射线平行方向，意图点改到80m。Spawn真实使用这个origin/direction。预测hasContact=false，实际飞行窗口无首次碰撞、无Damage。

原历史夹具只观察约1秒后清理弹体；本轮38项扩展与2项补充均等待3.2模拟秒，超过真实2.5秒寿命，结束时零在飞弹体。相同侧置1.5米扩展样本仍无伤害。因此不能把旧短观察窗口当成唯一原因。[实际全程轨迹](Evidence/Matrix/diagnosis.json)。

这定位了固定样本的防倒射分支与侧置视差行为，尚未授权选择新的玩法瞄准合同。不能直接删防倒射条件：相机前遮挡墙同样触发该分支，见CameraWall真实补充；极近0.35m时同一reason又可由初始重叠命中目标。reason本身不是命中成败结论。

两个历史问题本轮不关闭。产品修复等待单独授权；原生操作、真实森林自由瞄准体验、最终平衡NOT_RUN。不同相机偏移或姿态改变可观察结果，不代表已修复。
