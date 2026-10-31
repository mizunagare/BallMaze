# 相机、枪口与碰撞几何

所有向量为Unity世界坐标，单位m，完整原始数据见[Matrix/diagnosis.json](Evidence/Matrix/diagnosis.json)的shots、rayHits、projection及trace。

历史相机世界位置(305,24,295)，目标脚点(300,20,301.5)，目标中心(300,21,301.5)，CharacterController bounds大小约(0.8,2,0.8)、layer0、非Trigger。相机透视FOV65°，aspect1.7777778，近裁剪0.05、远裁剪160。完整投影矩阵原样记录。Camera Forward与实际ViewportPointToRay方向分别记录，不把二者预设为逐位相同。

历史实际Ray Origin约(304.971344,23.982828,295.037170)，Direction约(-0.572894394,-0.343419135,0.744214594)。射线从近裁剪面开始，而非直接从transform.position开始。Raycast距离80、LayerMask ~0、Ignore Trigger；Legal再排除本人、禁用、异场景和Trigger。首个合法表面约(300.192841,21.118382,301.244629)，距离射线起点8.340965m。

|实际释放采样|普攻|技能|
|---|---|---|
|动画|Spellcast_Shoot|Spellcast_Shoot|
|poseTime|约0.4200|约0.4667|
|枪口/Spawn|(299.574738,20.649759,300.918518)|(299.586700,20.643410,300.880585)|
|表面投影|-0.272345155|-0.239441678|
|实际速度|16|14|
|初始寿命|2.5s|2.5s|

实际挂点链：主角/角色外观/Rig/root/hips/spine/chest/upperarm.r/lowerarm.r/wrist.r/hand.r/handslot.r/主武器外观/杖首晶体/ProjectileMuzzle。没有使用逻辑fallback替代真实杖首；barrelBlocked=false，origin等于rawMuzzle。

枪口保护先检查身体anchor(position+up*1.25)初始重叠，再以半径0.16对anchor→muzzle扫掠。实际弹体每帧先OverlapSphere，再SphereCastAll半径0.16，并使用真实Impact/WeaponHit。法杖爆炸仍需真实碰撞触发，不能因为爆炸半径接近目标就凭空Damage。

原历史夹具在(300,20,300)的受控空间，场景地面未成为首命中。扩展ground为另建启用BoxCollider地面；muzzle-wall两项实际首撞墙，目标伤害0。第一轮camera-wall候选位置未被相机射线命中，只是一次未成功构造相机遮挡的观测，不记遮挡通过。额外camera-wall-verified使射线真实首撞墙，负投影约-2.40219/-2.36746，保留两组原始数据。

orbit组只调用原OrbitCamera.LateUpdate计算一次正常姿态，再冻结相机以隔离几何；不是玩家操纵相机。该组6/20m中心准星未对准目标，零伤害不直接归为产品瞄准缺陷。未做原生鼠标或动态手感验收。
