# 发射合同与唯一产品改动

只修改CombatAim.Solve。CameraFor、Legal、SameOwner、射线80m、半径0.16、anchor高度、实际枪口、弹速、寿命、伤害、释放时间、冷却和保存格式均不变。新代码不选最近敌人，不移动枪口，不改变AdventureCombat/Impact。

## 目标、区域与可达性

相机仍首先选择排序后第一个合法射线命中。cameraCollider是这个选择的身份，即使拒绝汇聚也保留，不将它伪装成实际contact。

原非负投影路径不变。负投影或零向量进入原保护分支，只有同时满足下列条件才能作新近距汇聚：

1. 相机选中现存敌人或资源Collider（排除静态墙、地面及空选择）。
2. 该选中Collider的bounds中心相对有效枪口沿cameraDirection投影>0.001，且相对身体anchor在水平cameraDirection的前向投影>0.001。
3. barrelBlocked=false，方向非零。
4. 初始半径重叠若有，必须首先属于同一目标；否则向原命中表面作真实半径SphereCast，首碰撞必须SameOwner。

成功时保留原intentPoint、真实origin及cameraCollider，direction指向原表面，reason=CAMERA_TO_MUZZLE_NEAR_TARGET。其他情况继续CAMERA_SURFACE_BEHIND_MUZZLE：有效方向为相机向前方向，intent为该方向80m，不清除选择身份，并以obstructed明确拒绝原目标汇聚。

A安全的前向目标允许近距汇聚；B墙/其他首阻挡不准穿越、不忽略Collider；C目标中心落在不允许的枪口/身体背向区域仍保护，不生成朝后弹体；D初始重叠继续实际Overlap/Impact规则；E无合法目标的原默认路径保持。

最终contact仍由原初始Overlap与整段SphereCast给出。cameraCollider表示选择，intentPoint表示实际发射意图，contactCollider表示物理预测，三者不强行假定同一对象。新增逻辑只影响判定，不注入Damage。已授权原2个Staff近距方向改变，其余22组方向和24组origin逐值保持。旧合同文件不修改。
