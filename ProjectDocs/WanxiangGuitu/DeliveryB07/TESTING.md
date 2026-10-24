# B07 复跑

Unity 6000.6.5f1，依赖沿用工程锁定版本；启动前隔离，合成存档，独立工程外工作目录。不要针对实际玩家存档运行故障注入。

## 完整运行

```powershell
& ./ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Invoke-LocalValidation.ps1 `
  -SourceProject D:/unity/WanxiangGuitu `
  -TestRoot D:/WanxiangValidationRuns/B07Final `
  -Phase All -FullRegression -B4 -B07 `
  -ShaderCacheSource D:/WanxiangValidationRuns/RouteScoreFinal/20261024-181305-74d5b037/Project
```

测试根父目录可替换，每次入口创建唯一子目录。缓存仅复制匹配版本的已结束隔离工程 ShaderCache，不复制 AssetDatabase、程序集或存档。冲突则跳过缓存或不安全步骤，不关闭用户程序。

`-B07` 在既有 Gather/Treasure/Bypass 之外增加 Land/Lake 两条正常 AI 流程，每条包含 Normal / Resume / FinalResume 三个进程，继续沿用原 Play 前隔离检查。只读目标与路线查询仍验证随机流不变。

## 定向规则

沿用 `DeliveryB4/Invoke-Directed.ps1`，Methods：`B07Probe.Run`、`B07SeedReplay.Run`、`B07Rules.Run/Resume/PendingResume/CommittedResume`、`B07Combat.Run`、`B07Interruptions.Run`、`B07Economy.Run`、`B07Liveness.Run`。`-NormalStrategies Land,Lake` 为 Boss 正常 AI 流程。必须使用已审查的结束工作目录 `-WorkerFrom`，缺少私有桌面 worker 不启动 Unity 到用户桌面。

- Rules：40个请求种子，至少30个不同实际 seed，旧无 Boss 布局快照重建、回执与保存故障、Running/Pending/Committed 新进程恢复、死亡保留徽章和再次出征。
- Combat：受控摄像机与命中/无敌/越界、中断、死亡。通过领域输入构造测试，**不是原生 UI**。
- Economy：1×1饰品填满背包，验证真实可接近掉落因格子不足而保留，整理后拾取一次、穿戴不保护，重复讨伐只生成绿装和核心1。
- Liveness：固定 seed 1/17、两个 Boss、满血/半血，共8组；普通 NPC 暂停的受控 AI 状态验证，不进行击杀，不作为正常 AI 胜利。
- 正常 AI：正常属性白弓/白剑，携带石2矿2与5瓶真实制作药水；合成营地仓库另有石1矿2供回营制作。森林实采木材后真实制作一把白弓，再讨伐目标 Boss、拾取紫装与核心、渡口或免费出口撤离、结算入仓、取材制造、再次森林出征与新进程继续。没有出征后直接补发物资、生命覆盖或 NPC 冻结。

## 证据分类与失败

每次命令、时间、退出码、超时、日志、结果都独立归档。所有历史失败保留，不用后续 PASS 覆盖。开发诊断曾复用已经结束的测试工程并归档修改前/实际执行源码，该类明确标为增量诊断，不能冒充最终干净副本。最终必须重新执行新的完整 All。

受控恢复比较按稳定 ID 排序，校验所需的布局、实体、装备、掉落、来源账与玩法随机流；不把枚举顺序、减少中的冷却和临时摄像机坐标当成业务身份。升级选项先通过实际选择流程完成，再建立最终恢复断言；另有原历史回归覆盖技能/冷却。

不执行原生 UI 或人工试玩时保留 NOT_RUN。背景 WM_CLOSE 仅证明该路径；UNKNOWN 根因仍 UNRESOLVED。超时不强杀进程、不称正常退出。用户 ProjectSettings 不进入提交。

## 最终运行的输入边界

最终完整 All：`D:/WanxiangValidationRuns/B07ReplayFinalAll/20261025-030948-1d4e2c00`。产品、注入规则、正常AI驱动统一冻结在 `f11676f08728e4c7a58b07e60c5eb6dd7c1b587f`。十项B07方法包含新增逐攻击中断与Editor隔离种子探针；所有实际运行代码另外按哈希封存。之前All4有准备后、正常AI启动前的驱动修订，明确保留其双输入记录，不能套用到本轮。

陆地使用先前死亡失败的原始种子1132820888，湖中使用既有成功种子745672572。种子只在新出征前通过Editor专用入口设置一次，要求有效隔离参数；不在正式Player编译，不改已有Run/存档种子，不在出征后传送或补发物资。其他种子的合法性由40请求种子的受控导航与确定性回归独立验证。

Boss正常AI驱动只在其测试Editor的Input System内禁用已有键鼠设备并添加测试键鼠；不禁用Windows硬件、不修改用户快捷键、不向真实桌面发送输入。观察目标Boss时先实际接近并等待三次释放，再进攻。敌人照常活动，伤害、生命、翻滚冷却和5瓶药水均不改。机器人现在先应对前摇，再决定接近；同时读取普通怪的真实攻击时钟使用原翻滚动作，接近远程小怪后交战。

`boss-world.csv`记录所有首领，不仅是被选中的目标；`attack-actions.csv`记录攻击请求，不能冒充逐次伤害来源；`dodge-actions.csv`仅记录原TryDodge成功。旧All3提前击杀的逐次伤害来源未被完整记录，不猜测；All5已观察三次后主角死亡，独立保留。

运行态恢复断言直接检查场景中的Boss生命、据点状态、死亡碰撞/攻击禁用、实际装备ID和六类材料余额，再比较检查点与地面掉落ID。空备用武器的null/空串按同一“未装备”处理；非空ID仍须严格一致。

补充定向方法为 `B07Interruptions.Run`、`B07SeedReplay.Run`，也已加入完整All。前者逐攻击验证前摇中断、恢复和就绪时钟、冲锋释放后受伤但抗硬直；没有击杀或领取奖励，不能作为正常AI胜利。

本轮完整All可复用已结束隔离副本的匹配版本ShaderCache，记录shader-cache-provenance；不复用AssetDatabase、已编译程序集或存档。它证明新副本重新导入/编译，不应宣称所有着色器从零编译。最终构建文件逐项哈希，另检查Assembly-CSharp.dll没有Editor种子入口。
