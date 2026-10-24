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

沿用 `DeliveryB4/Invoke-Directed.ps1`，Methods：`B07Probe.Run`、`B07Rules.Run/Resume/PendingResume/CommittedResume`、`B07Combat.Run`、`B07Economy.Run`、`B07Liveness.Run`。`-NormalStrategies Land,Lake` 为 Boss 正常 AI 流程。必须使用已审查的结束工作目录 `-WorkerFrom`，缺少私有桌面 worker 不启动 Unity 到用户桌面。

- Rules：40个请求种子，至少30个不同实际 seed，旧无 Boss 布局快照重建、回执与保存故障、Running/Pending/Committed 新进程恢复、死亡保留徽章和再次出征。
- Combat：受控摄像机与命中/无敌/越界、中断、死亡。通过领域输入构造测试，**不是原生 UI**。
- Economy：1×1饰品填满背包，验证真实可接近掉落因格子不足而保留，整理后拾取一次、穿戴不保护，重复讨伐只生成绿装和核心1。
- Liveness：固定 seed 1/17、两个 Boss、满血/半血，共8组；普通 NPC 暂停的受控 AI 状态验证，不进行击杀，不作为正常 AI 胜利。
- 正常 AI：正常属性白弓/白剑，携带石2矿2与5瓶真实制作药水；合成营地仓库另有石1矿2供回营制作。森林实采木材后真实制作一把白弓，再讨伐目标 Boss、拾取紫装与核心、渡口或免费出口撤离、结算入仓、取材制造、再次森林出征与新进程继续。没有出征后直接补发物资、生命覆盖或 NPC 冻结。

## 证据分类与失败

每次命令、时间、退出码、超时、日志、结果都独立归档。所有历史失败保留，不用后续 PASS 覆盖。开发诊断曾复用已经结束的测试工程并归档修改前/实际执行源码，该类明确标为增量诊断，不能冒充最终干净副本。最终必须重新执行新的完整 All。

受控恢复比较按稳定 ID 排序，校验所需的布局、实体、装备、掉落、来源账与玩法随机流；不把枚举顺序、减少中的冷却和临时摄像机坐标当成业务身份。升级选项先通过实际选择流程完成，再建立最终恢复断言；另有原历史回归覆盖技能/冷却。

不执行原生 UI 或人工试玩时保留 NOT_RUN。背景 WM_CLOSE 仅证明该路径；UNKNOWN 根因仍 UNRESOLVED。超时不强杀进程、不称正常退出。用户 ProjectSettings 不进入提交。
