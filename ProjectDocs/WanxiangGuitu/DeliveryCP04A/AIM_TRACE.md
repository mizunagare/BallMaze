# 实际调用链和观测边界

正式源码只读链：AdventureCombat.Strike/UseSkill → BeginAttack（原时序）→ Release → CombatAim.Solve → Fire → AdventureProjectile.Spawn → Update（初始接触/真实扫掠）→ Impact → WeaponHit.Apply或AdventureResource.Hit → CombatHealth.Observed。

诊断驱动仅调用真实Strike/UseSkill，订阅既有AdventureProjectile.Observed和Health.Observed；不调用Spawn、不调用Damage、不覆盖生命、速度、命中结果或Collider开关。每个fixture使用原CreateEncounter初始化敌人，禁用敌人AI以固定几何，原角色动画和攻击释放仍运行。固定相机、站位和装备是受控测试配置，不是原生键鼠验收。

每个真实spawn保存Camera位置/Forward/投影/裁剪面、射线、全部有序RaycastHit、actual muzzle骨骼链/动画采样、实际Spawn/Direction、预测contact。每帧flight保存from/to；初始重叠/sweep-contact及resolved保存实际对象；Damage另存前后HP与applied。全数据见Matrix/diagnosis.json、CameraWall/diagnosis.json；Historical另保留旧结构JSONL及timeline。

38项矩阵：四距离0.35/1.5/6/20m × 四相机右/中/左/Orbit × 普攻/技能 =32，加枪口墙/相机墙候选/地面×2=6。另两项确认相机遮挡。38项中28有真实伤害、10无伤害；补充两项均无伤害。数值是观测计数，不是38个命中验收PASS。

原历史矩阵24组发射坐标与方向逐值一致，额外暂停箭维持单独身份；见paired-24.json，未移动旧目标、未改变旧距离或断言。

进程与业务分层：三次Editor原生进程各退出0、无超时；新诊断断言6 PASS指证据一致性，不指命中缺陷修复。Historical语义仍BLOCKED/2。未进行正式Player、原生UI、人工试玩、新构建或性能测量。
