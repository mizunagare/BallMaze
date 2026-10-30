# 观测数据合同

- timeline.csv：weapon,skill,sample,attack,frame,time,releaseFrame,phase,motion,clip,poseTime,muzzleX/Y/Z,hp。attack来自真实AdventureCombat.LastAttackId；固定夹具动作窗口与武器项一一对应。
- events.jsonl stage=spawn/flight/contact/resolved：attack/shot来自真实AdventureProjectile实例AttackId/ShotIndex，from/to为实际位置；muzzle是Solve原始枪口，aim为实际解；sound为该时刻选中声道的clip标识，不是人耳听见或声学测量。
- stage=Damage：before/after/applied/lethal/frame来自CombatHealth.Observed。该原接口不含攻击者；attack字段仅当时LastAttackId上下文，尤其角色连续攻击可能有重叠动作，不据此作引擎级因果归因/每攻击伤害平衡统计。角色死亡的实际承伤/唯一deathTransition独立验证。事件身份使用文件路径+1基行号，不虚构Damage ID。
- 截图为固定1280×720相机的真实GameView、真实动作/释放帧，位于离地受控夹具，不是正式森林美术、原生操作或人工通过。保留全部原图不裁切。
- resource-unit：私有池回收探针只分配现有GroundRing以检查代际/所有权，不调用Hit或Damage，不作为武器命中证据。玩家死亡准备由原伤害参数的真实敌弹碰撞完成。
- 120 capture-fps是测试过程参数，不写ProjectSettings。记录缓冲在隔离驱动中，结束后落盘，不是产品观测框架；无有效Profiler时性能NOT_RUN。
