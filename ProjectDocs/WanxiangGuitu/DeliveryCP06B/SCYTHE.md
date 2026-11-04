# B3 镰刀

独立ScytheMotor：普攻 .8s间隔、.3s启动、3m/85度半角、80%攻击；回旋收割三段（.28s间隔），3.4m/125度半角，每段45%，同目标每段去重，不是360度无条件命中。灵魂牵引 .4s启动，4.5m/50度半角，Sight后添加1s有限控制，逐帧检查遮挡并通过CharacterController.Move移动。使用实际enemy.speed，上限3.2m/s；有RB按其质量，无RB采用明确代理质量普通1/精英2。距离到1m停止，不改transform、不瞬移。Boss/ForestBoss免疫。

原创四部件长柄弧刃模型；实际右挂点、原Spin/Slice剪辑与程序化补充。完整专属镰刀骨骼动作、人工观感仍未验收。音效为新合成ScytheSweep，走既有声道池。

B3Editor1 33 PASS，含真实拾取、伤害、两目标三段去重、限速牵引、暂停恢复、墙阻挡、Boss免疫、背后不命中。B3Player1独立非开发Player同样33 PASS，actual exitCode=0。统一回归另行执行，不能继承。
