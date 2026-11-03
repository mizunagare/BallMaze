# B2 远程软锁定检查点

TargetAssist只产生意图，不产生Damage；弓/杖经原CombatAim.Solve后可使用合法目标表面重新求真实枪口方向，保留原cameraCollider身份、barrelBlocked以及CP04-B防倒射条件。原CombatAim.cs字节不变。释放瞬间重新验证体积通路，无目标返回原生自由解；移动投射物不追踪，不忽略墙体。配对组保留原镜头/自由瞄准开关。

本机可玩非开发包：I:/WGCombat/CP05B-1103-A/B2/ReleaseBuild/Release。B2/TestBuild2为含隔离API驱动的验收Player，不能当纯可玩包。两者Bee五服务false；构建均0错误，警告完整保留。纯包SmokeRelease READY并exit0；没有原生输入或人工试玩证据。

实际Editor1和非开发Player2各99 PASS、1 NOT_RUN。Staff普攻/技能0.35/1.5/6/20m、弓多距离普攻/近距技能、自由对照、实体去重/有效性、滞回、暂停清除、真实墙首撞及Damage均有独立轨迹。不是完整128矩阵，也不是最终平衡/手感验收。

Player1驱动在Boot→Title被销毁，没有probe.json，保留INCOMPLETE和普通关闭记录；不得由exit0认定业务通过。已为隔离驱动加DontDestroyOnLoad并对运行器增加缺失语义回执检查，Player2重跑成功。

有截图及两组法杖6m真实运行截帧序列（自由/辅助），来源为非开发API验收Player，不是物理输入。GC校准仍无效，NOT_RUN；CPU原始采样不承诺性能预算。

训练新增真实生命显示、重开独立训练场景与原CombatFeedback；重开销毁旧场景再创建新角色，不直接覆盖HP、结算或存档。未修改AI脚本、经济、随机流或伤害公式。
