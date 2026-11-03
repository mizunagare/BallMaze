# CP05-A 原型与授权边界

本轮只读设计，未创建可执行原型、未运行新Unity测试或构建。所有数值都是待验证实验输入。

## 基准与分批
设计分支design/cp05-third-person-combat从当前远端main72db192a527bd256e2ba18cd7ab334d8334051da创建；cc9b73679458b0b868d875890a16b4c5238fb878仅只读对照。隐私分支和main都不合并。未来实现前必须明确CP04-B修复是否进入原型基准，重新冻结源码、构建输入及24组历史发射合同。

1. 肩后构图＋避障，只评估相机/材质，不改Damage；再由真人观察屏幕占用与操作。
2. 统一Target Assist只读观察模式，记录候选和评分，不驱动任何攻击或转向；与自由瞄准同场景配对。
3. 授权后仅弓/杖接入选点，真实枪口及物理链不换；释放前重新检查。
4. 最后接入近战有限yaw仲裁，不新增位移、根运动、倍率或连招系统。每步固定SHA复审，不能因本设计自动开始。

## 最小拟授权文件（本轮均未修改）
|文件|后续理由|风险/限制|
|---|---|---|
|Assets/CombatPrototype/OrbitCamera.cs|肩偏移及连续避障|晕动、穿模、移动坐标系变化；不自动旋转镜头|
|Assets/CombatPrototype/CameraActorFade.cs|近距可恢复淡化|材质泄漏/墙后信息；不得改Collider|
|Assets/CombatPrototype/TargetAssist.cs（新，拟）|统一只读选点/滞回|目标跳动、隐式锁墙后目标、查询成本|
|Assets/CombatPrototype/AdventureCombat.cs|消费辅助意图、面向、释放采样|改变既有发射方向及攻击事务；严禁改伤害/冷却/释放时刻|
|Assets/CombatPrototype/CombatAim.cs|明确意图入口与枪口检查|CP04-B近距及防倒射回归；需单独明确授权|
|Assets/CombatPrototype/ThirdPersonHero.cs|移动/攻击yaw仲裁|移动和翻滚手感、多个rotation写入冲突|
|Assets/CombatPrototype/PlayerHudPresenter.cs|目标意图/真实阻挡标记|把意图误报为命中；UI只读|

FantasyActorVisual.cs仅在实测采样顺序无法协调时另提授权，不预先批准重写动画。PlayerInput.cs首个原型保持原绑定及屏障，不增加锁镜头/切目标键；若后来加换肩等输入，须另列PlayerBindings/UI/持久化影响申请。Scene/Prefab/ProjectSettings保持不改；未来用运行时参数还是配置资产，需另行审核，不在本轮创建。

## 未来固定输入与矩阵
基础矩阵：4武器×普攻/技能×0.35/1.5/6/20m×左/中/右/Orbit机位＝128条配对工况，近战远距允许真实落空，不能为凑PASS扩大攻击范围。每条记录源码/Player SHA、seed/revision、实体/装备身份、质量/词缀、库存、相机/骨骼pose、输入/游戏时间、AttackId及每弹ShotIndex；同条件反复，不把不同种子当A/B。

补充逐项：单敌/并排多敌/前后左右、移动/死亡/禁用目标；角色自身遮挡；真实树干、石头、墙；叶片视觉遮挡与无Collider装饰；相机能见枪口不通、反向情况、初始重叠；玩家连续甩镜头及小幅噪声；切换滞回/并列评分；启动/释放/恢复阶段取消、暂停恢复、失焦/UI屏障、死亡、场景卸载；箭扇形/杖侧球独立碰撞；多Collider与多目标近战。

## 可视化与数据层
- 只在隔离测试构建加overlay：C相机、near平面、centerRay；M骨骼枪口、O实际origin；绿色可达段/红色首撞段；候选owner/分项/选择原因；移动yaw与冻结forward。
- 每帧JSONL和逐事件Spawn/Flight/Collision/Impact/Damage必须按AttackId/ShotIndex关联，截图索引记录构建SHA、场景、frame及图层。颜色和标记不是命中证据。
- 相机构图测Hero/目标Renderer投影与准星遮挡面积、可见比例；物理记录Collider、owner、layer、trigger。不得关闭碰撞、换目标位置或注入Damage。
- 按无辅助/辅助同条件比较切换次数、滞回延迟、主动转向响应、选择失效率、真实首撞、落空原因。无目标不应偷改自由瞄准。
- 性能：实际Profiler CPU、GC、物理查询数、材质实例；无有效计数器标NOT_RUN。候选/overlay开销与产品分开，先测无观测对照，不能凭预算常数宣称优化。

## 分层验收
规则/投影数学、受控Editor、隔离非开发Player、纯发行回归、原生键鼠、独立人工分别记录。软件输入和机器人不得算真人。功能依据真实碰撞/Damage，镜头舒适性、自然面向、误吸目标必须由真实操作者判断。历史两法杖失败和24组方向证据不覆盖，任何合同差异列出旧/新数值、原因及批准记录。

暂停、取消、死亡和装备切换继续原语义；不修改随机流、经济、地图、v9或保存目标身份。退出后辅助目标全部失效，不恢复旧软锁定。设计批准仅表示允许后续指定原型，不能自动把方案状态转为产品PASS。
