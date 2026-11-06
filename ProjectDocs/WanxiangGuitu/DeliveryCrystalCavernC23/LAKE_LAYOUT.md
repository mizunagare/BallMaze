# C2.3 开工兼容映射与布局（实施前）

基准 35efda203b0b36801139fa2cc80ab7ba895207af；main 72db192a527bd256e2ba18cd7ab334d8334051da，只读。独立工作树 H:/unity/WanxiangGuitu-Cavern-C23，隔离测试根 I:/WGCombat/C23-1106-A。启动前提交内存余量约 29 GB；不复制 Library，不结束已有程序。

| 版本 | revision | generation | 固定资源 |
|---|---:|---:|---|
| C2.1-CAVERN-1 | 7 | 10 | CrystalCavern/Cavern |
| C2.2-CAVERN-1 | 8 | 11 | CrystalCavernC22/Cavern |
| C2.3-CAVERN-1 | 9 | 12 | CrystalCavernC23/Cavern |

编号与路径未占用。旧 Generate/GenerateExpanded 和固定资源保留；显式判断三个版本，不使用 revision >= 8。仅新建洞窟 Run 使用 C2.3；v9 机关使用已有 SavedWorldEvent.used，资源/敌人/掉落继续现有快照，无新增材料或永久奖励字段。

布局：通道末端 x34,z410 向东进入湖岸。湖泊位于 x48..70,z399..421；南侧内环较短且有一名普通巡守，北侧外环经 z432 绕行较长且没有新增敌人。对岸 x78,z410 设置机关、普通宝箱及晶石；固定桥横跨湖面，关闭时两端实体门阻断，开启后双向连接。湖底低于岸面，深水无导航地面，以可见岸壁/护栏限制跌入；桥面是唯一横跨深水的可走地面。旧通道与隐藏矿室仍保留。

新增供给：铁矿脉1、晶石脉1、普通宝箱1、普通巡守1。全部使用已有普通奖励入口及本 Run 随机状态，增加总供给，不宣称经济不变；不修改旧来源概率、品质或随机调用。新实体统一 c23 命名空间，既有实体 ID 保留。

预期最小共享修改：CrystalCavernLayout（版本/事件/节点）；CrystalCavernRegion（版本资源绑定、桥门导航事务）；AdventureFlow（新 Run 默认）；WorldEventPoint（机关交互）；PlayerHudPresenter/SaveCatalog（版本与引导）；CrystalCavernAuthoring（新固定资源烘焙）。CombatAim、TargetAssist、镜头、七武器数值和既有技能冻结。

验证先保留基线不具备湖区的源码事实与运行证据；分开记录受控武器命中与正常 AI 连续出征。连续流程开始后不传送、不改生命、不冻结敌人、不注入 Damage。Editor/非开发观测副本/无驱动纯包分层。全部历史开放项、原生输入及人工体验状态保持原值。
`n最终落地几何以固定Prefab为准：低水面范围x48..70,z399..427，北岸z427..438，南岸z389..399，桥面z407.5..412.5。开工草案中的z421边界已由最终制作范围替代；旧C2.1/C2.2资源未改。
