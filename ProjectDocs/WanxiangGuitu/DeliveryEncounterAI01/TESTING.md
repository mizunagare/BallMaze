# 本机复跑与证据口径

Unity 6000.6.5f1；工程外新根 `I:/WGCombat/EAI01-*`，本次根 `EAI01-1030-A` 不可重用。使用合成档、独立副本；不得访问真实玩家档、激活私有桌面、关闭用户程序或强杀超时进程。所有入口复用DeliveryUI01既有Step/worker，不建立第二套进程框架。

1. 先记录本地/远端完整SHA、用户修改及SHA256、owner.json。用DeliveryUI01/Invoke-Rules.ps1的PrepareOnly准备P/Project旧产品、F/Project新产品。仅在副本把用户Scene/Settings/Recovery保存到Deferred，替换成开工Git版本；不动主工程原件。Library仅是空闲旧测试副本缓存，不当作已执行测试证据。
2. 保存旧版EncaiRepro.Run真实AI/物理负例。首次编译失败及后续首修失败全部保留。场地/敌人/初始冷却是明确受控夹具，不是自然森林或人工输入。
3. Instrument.py只在拥有副本包裹CombatEnemy、ForestBossBrain、EnemyProjectile原有Damage/GainExperience各一次，并添加只读事件。原始/观测源与SHA分别保留。BAL01Trace仅存在隔离观测构建；不增加随机调用、不伪造命中或奖励。
4. 两版使用同一最终EncaiMatrix模板及config。`Invoke-Matrix.ps1`每次新建目录，每seed/rep一个独立进程；418/419/420，rep0原地30秒、rep1移动攻击90秒、rep2可见预警反应闪避90秒（Triple为明确的早闪反例）。四档真实合成装备防御0/3.2/7.6/19.2，固定20级避免条件中升级改变属性。每进程10组×4档=40条件，9Run/版本、360条件/版本。不是全排列，也不是每种策略3次相同配置重复实验。
5. 矩阵仅在条件边界恢复初始状态、定位及停用非目标实体；被测敌人和真实碰撞不冻结，条件内只经实际AI、武器、移动、闪避、治疗、Damage与掉落。实际死亡/清场提前终止，未完成保留删失TTK=-1。Guard在矩阵局部场景中停用，导航/警戒/回家由EncaiGuard实际生成森林另测，不能互相冒充。
6. 矩阵使用明确按条件重置的legacy全局RNG，Flow处于不持久化的夹具恢复区；不是正常Run-owned随机流。实际正常AI和恢复另测。初始位置、属性、等级、RNG序列全部逐条件配对，UUID本来独立不要求相等。

```powershell
& ./ProjectDocs/WanxiangGuitu/DeliveryEncounterAI01/Invoke-Check.ps1 -Project "$owned/F/Project" -Output "$owned/NewRepro" -Method EncaiRepro.Run -NoGraphics
python -X utf8 -B ./ProjectDocs/WanxiangGuitu/DeliveryEncounterAI01/Instrument.py $repo "$owned/F/Project" "$owned/NewInstrumentation"
& ./ProjectDocs/WanxiangGuitu/DeliveryEncounterAI01/Invoke-Matrix.ps1 -Project "$owned/F/Project" -RunRoot "$owned/NewMatrix"
```

正式汇总脚本使用FinalBeforeMatrix/FinalMatrix。本次中间BeforeMatrix、BeforeMatrixRetry、AfterMatrix为历史尝试；不能用它们覆盖最终扩充矩阵。新的复跑如改目录应先更新分析输入，不能合并多个尝试挑最佳结果。

`hp.csv`无头列：time,frame,HP,Defense,potionCooldown,level,XP。events.jsonl含预警/释放/发射/实际接触/经验及逐帧状态/位置。投射物通过实际attack键回溯发射来源，不猜最近敌人。源不明保留UNRESOLVED；本次为0。预警后未释放数量包含取消及截止仍待发，不能全部称取消；slotDenials仅是普通敌轮询拒绝次数，不是独立攻击数；Boss拒绝次数未采集；blockedSeconds是眼部LOS遮挡累计actor-seconds，不是枪口取消次数。

Summarize.py生成ENCOUNTER_MATRIX、HIT_EVENTS、PAIRED_INPUTS及SUMMARY。分位数为排序线性插值，样本量保留；删失不填0TTK。同招独立扇形弹的多次接触，与不同攻击之间的错峰分开统计；预测预约不构成全局伤害节流。

## 回归、正常AI和纯发行构建

旧矩阵结束后，Invoke-Regression.ps1先用旧产品BAL02Recovery.Save生成合法v9，再把四个授权新源复制到拥有副本、移走runtime观测类至Editor，原字节复制合成Store供新进程Load。之后执行Guard、护甲/数学、AIM、时序、区域、Boss经济与Run/Pending/Committed、随机流、B1渡口与恢复；失败继续独立项，占用则停止相关后续，不强杀。各方法输出不同目录，旧结果不继承。

新矩阵结束后，Invoke-NormalAndBuild.ps1先通过安全非batch私有桌面入口执行Normal/Resume/FinalResume。既有Gather驱动使用Input System合成输入及真实游戏API；不是原生键鼠。没有出征后传送/冻结敌人/直接改HP；营地合法合成起始材料另列。依次走实际战斗/采木、拾取、木2石1渡口、保存、新进程继续、正常撤离、唯一结算、入仓/取材/制造、新森林Run与再恢复。

纯构建前恢复四个未经观测注入的产品源，BAL01Trace移入Editor；矩阵代码移出非矩阵编译路径。Build01Audit.Run调用原WanxiangBuild.Build，Options=None，完整消息不筛选；Inspect-Build读取PE元数据确认不含观测/验收/Editor驱动，计算exe/UnityPlayer/Assembly-CSharp哈希。非开发构建成功不等于本次已执行发行Player或原生标题栏关闭。

Collect.py只发布拥有根的合成证据，排除项目副本、Library、用户Deferred和发行二进制；日志/逐帧数据gzip，保留原SHA和发布SHA。Verify-Publication.py检查索引字节/LFS oid与授权范围。最终提交后重新读取远端完整SHA，固定链接交付并暂停。

## 限制

原生UI、独立人工、最终难度/趣味、完整性能、自然双Boss同场仍NOT_RUN。未直接计数的NavMesh失败、方向抖动和所有取消组合不填0；Guard有限样本与原始状态时间线不能外推到任意场景。D3D12 UNKNOWN、青色帧、Search等历史根因仍UNRESOLVED，不额外重跑关闭实验。

