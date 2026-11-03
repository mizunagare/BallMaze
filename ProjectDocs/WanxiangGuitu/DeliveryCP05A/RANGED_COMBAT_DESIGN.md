# 远程真实弹道设计

## 已有实现与版本边界
main已有CombatAim.Solve，不是单纯“从准星位置生成子弹”：中心Raycast选择intent，真实武器挂点计算方向，anchor→muzzle体积检查可修正origin，InitialContact/Sweep预测接触。AdventureProjectile在真实origin生成，每帧Overlap及半径0.16 SphereCast、Impact、WeaponHit/Resource.Hit，生命周期2.5s，暂停不移动/判定、不消耗life，死亡/卸载清理。飞行中不跟踪目标；切武器不会默认清掉已发弹体。

枪口来自handslot.r下CatWorld武器优先资源（旧AdventureWeapons为fallback），法杖“杖首晶体”、弓“弓弦”的子挂点；缺失时logical-fallback不是可靠动画枪口，必须单独诊断。剑/枪品质附加弹体目前使用身体前方逻辑origin，不能假称全四武器都已使用骨骼枪口。

main的负投影回退会清cameraCollider并使用相机方向。独立CP04-B cc9b73679458b0b868d875890a16b4c5238fb878保留cameraCollider身份，条件性验证同归属表面可达，不无条件倒射。本设计不合入该修复，不改写两项历史UNRESOLVED。未来原型先明确是否以CP04-B为基础；不可在旧main上悄悄重写同一修复。

## 拟定链路
Camera Ray → Target Assist（或Free）→实际目标表面Intent →该释放帧Actual Weapon Muzzle → anchor/barrel/overlap＋muzzle体积路径检查 →真实Direction →Spawn →Flight →FirstCollision →Impact →真实Damage。

目标选择不能跳过物理：相机看见而枪口被石头挡住则报告blocked，仍按原业务处理实际首撞/拒绝条件；不能把生成点传送至墙另一侧。相机被墙挡住也不能自动锁墙后敌人。自身排除仅明确所属主角Collider；护盾、敌人、墙体不可通用忽略。

- 无合法目标：继续原自由瞄准，不停火、不凭空找最近敌人。
- 对负投影：沿用CP04-B经授权的目标身份、防倒射、初始重叠和同实体首撞合同；不把全部负投影改成指向表面，不清空身份来消除报错。
- 初始重叠、moving target及不同动画枪口：释放帧重新采样，预览可过期，释放日志为准。已发弹体方向不可被新软目标反复旋转；不新增追踪弹/自动命中。
- 弓扇形各箭依旧独立方向和碰撞；法杖侧球各自真实Sweep，不能共享中间弹首撞结果。爆炸继续当前LOS/每弹目标去重合同。

原型观察对象须包括真实SpawnOrigin/方向、raw muzzle及其transform链、animation clip/poseTime、相机rayOrigin/near plane、目标表面及实体身份、墙体首碰、AttackId/ShotIndex与Damage时间。软目标身份与实际命中身份允许不同（移动/遮挡/散射），不能用前者直接发伤害。

不得改变伤害、冷却、释放时间、半径、弹速、生命周期、地图或v9。若未来确需偏离24组原发射方向，应先提交逐例配对差异及明确授权，不能重录基准伪装无变化。
