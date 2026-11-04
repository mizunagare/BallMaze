# CP06-A实现、兼容与风险

## 审计基线

产品397d53fe87ce5b6c490c86c63d59015de26a46af，远端main核对为72db192a527bd256e2ba18cd7ab334d8334051da；独立feature/cp06-skill-expansion。现有每武器一个UseSkill，统一skillAt；存档v9经CaptureLegacy/RestoreCooldown保存其剩余值。四种旧基础攻击及技能有真实基准Editor/非开发Player数据，保留首次夹具等待错误。

现有素材：Knight等Legacy Animation含横斩、旋转、突刺、弓射、蓄弓、施法、受击、死亡；FantasyActorVisual手动采样并负责部件表现，非新增Humanoid资源。复用原AttackTimed、CombatFeedback音效与轨迹/施法反馈。没有空Animator或外来素材。新蓄势阶段展示独立蓄势标记，松开/到顶后再进行真正前摇，使释放处于动画有效区间；后续段提前准备而非命中后才播放。

## 产品文件

- AdventureCombat.cs：保留原MeleeGeometry、Release、Melee、Fire、AdventureProjectile、Sight、TrackMelee完整正文。10个精确接入点：partial、组件创建、技能名/描述/冷却、Pending观测、UseSkill分派、共享取消、衔接门槛和重置清理。槽0执行原分支。
- WeaponSkillExpansion.cs：8个不可变定义、稳定ID及新状态机，启动快照来源装备和AttackPower，使用现有skillAt消耗冷却；分段取消不退款。partial桥只调用原物理方法、CP04 CombatAim/CP05 Assist和原有限近战自动面向。
- SkillPhysicalEffects.cs：独立贯矢与符阵，旧弹体无改动。贯矢做初始Overlap/SphereCastAll排序及实体去重，实心障碍先于目标、最多三实体；符阵只由实际原弹体Resolved创建，三次Overlap及逐目标Sight检查。所有伤害经真实碰撞后进入原WeaponHit/资源Hit，测试无Damage注入。
- WeaponSkillPanel.cs：运行时uGUI三槽与阶段信息，按钮调用真实Select并建立原输入屏障；F等实际重绑定Skill操作沿用原消费者，无新增硬编码游戏按键。技能名/说明同步原HUD/帮助。

## 时序与生命周期

正常攻击恢复后可开始新技能；新技能完成0.22秒恢复后可再次普攻。多段按固定时间逐段释放，每段均真实查询，不以目标选择代替命中。玩家可移动；近战不增加位移，辅助沿用剑30/枪20度及原速度预算，释放按冻结方向；远程每段重新检查实际枪口与目标路径，保留自由镜头。

暂停/输入屏障/翻滚/失焦取消未完成段，不退冷却；已释放弹体及符阵暂停时冻结时间、碰撞和伤害，恢复继续。切武器取消未释放段，不清除已释放物；死亡、组件禁用、场景卸载及战斗重置清理。无真实相机的远程新技能在消耗冷却前拒绝。原旧技能的时序、品质分支和生命周期不变。

## v9及经济边界

不改存档类/版本/迁移。技能选择为临时设置，加载默认旧槽0；不会重放未释放动作。保存唯一公共技能冷却，新进程恢复后旧槽同样不能绕过剩余冷却。真实保存事务、Run/region/seed、装备ID、Profile/仓库/徽章/教程和三随机流独立验证。训练仍临时上下文，不写正式进度。

新技能固定范围和冷却来自本批定义，伤害使用实际AttackPower及原WeaponHit词缀结算；不宣称所有旧范围/品质特殊分支已自动映射到新技能，也不扩展技能树或新经济。原技能/普攻品质合同逐字保留。八组候选参数不是最终平衡结论，样本为受控功能验证，不等同独立玩家难度/手感结论。

## 风险和未执行

新的物理查询数组、命中集合、LineRenderer材质及短暂反馈有可量化性能风险；数量/寿命有界不等于性能已验收。本批未取得新Profiler CPU/GC基准，NOT_RUN，不复用CP05性能数值当新结论。原生物理键鼠、人工音质、审美与打击感NOT_RUN。旧引擎Search/JobTempAlloc、D3D12 UNKNOWN、青色帧、关闭旧样本根因继续保留，不以工具exit0关闭。
