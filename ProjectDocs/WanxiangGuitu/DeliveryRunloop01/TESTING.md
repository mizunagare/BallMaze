# RUNLOOP-01 复跑

只在工程外新建I:/WGCombat/<唯一根>并写owner.json。开工读取main完整SHA、git status、用户场景/ProjectSettings/Recovery及旧证据SHA。基线不符先停止。禁止真实存档、升级依赖/CI、关闭用户程序、抢桌面或强杀。

1. 复用DeliveryUI01/Invoke-Rules.ps1 -PrepareOnly准备root/P/Project与Prepare。可只读复制已确认没有Unity占用的旧拥有者工程Library缓存；不能复用占用副本或复制真实玩家档。
2. Before只在副本使用4ae4ca8f基线的AdventureFlow.cs、AdventureFlow.UI.cs、CombatSaveSystem.cs，仅注入RunloopFault.cs到Editor/B06LocalChecks；其他新夹具引用新观察属性，不要提前注入基线。用DeliveryCombat02/Invoke-Combat02.ps1 -Project <clone> -Output <new>/Before -Method RunloopFault.Run，保留实际exit1和故障结果。它通过真实放弃/提交路径触发after-publish异常，不直接指定结算状态。
3. 同步最终三个产品源到闲置副本，重复同一Fault为After，应核对live/disk均Committed及同修订。再注入本目录其余.cs.txt，全部只能在副本Editor目录，不能进入发行程序集。先用batch跑编译预检，避免Safe Mode；不能升级C#绕过工具错误。
4. Invoke-FrozenCycle.ps1使用参数Project、RunRoot，依次运行Run/Running/Pending/Committed/Final五独立进程。它复用旧Invoke-Checks与原Worker传输，启动前显式隔离；VerifiedShared必须不存在。每阶段保存源、主档、备份、expected、断言与进程回执。失败立即阻断依赖，不能改旧输出目录继续覆盖。
5. Invoke-Runloop.ps1记录本轮初始链与有限工具修复后的续跑；StartStage/Attempt允许只恢复已存检查点的未完成阶段，不再创建或伪造同一Run。所有首次失败目录保留。Frozen完整链独立新根，不继承初始链PASS。
6. RunloopCycle.Death为实际伤害死亡规则；RunloopOverflow.Run以明确合成的满仓初始状态完成真实采集/撤离/提交/领取。库存初值是固定夹具，不是玩家所得；实际变化必须走Hit/PickUp、Commit、ClaimPending、Craft/Transfer等原入口。
7. RunloopUncertain.Missing/Corrupt在独立合成根移动真实已发布档（保存精确字节），或写入明确坏档，再恢复原发布字节并走LoadProgress验证。禁止修改奖励/回执字段制造成功。断言提交与SaveProgress均被门禁阻止、完整读取清除临时状态、重复不增益。
8. RunloopEntry.Run使用真实Title/Forest场景生命周期和GameEntry业务请求，必须非batch（产品Start在batch故意跳过），用原Invoke-Checks独立StorageRoot。不是鼠标点击或最终Player。Catalog使用B09Rules.Run/Resume/Interrupt/Recover；先将Prepare/fixtures/v1～v6复制至独立Catalog/fixtures，并使用共享StorageRoot，每步独立Output；失败停止依赖。
9. 复用DeliveryCombat01/Invoke-Regression.ps1运行Input01/S2R1Observation/B07Combat与正常AI Normal/Resume/FinalResume；按原规则恢复副本Deferred文件。运行前确认前一进程结束；超时保留并停止复用，不强杀。
10. 原Build01Audit.Run执行非开发Windows构建，所有错误/警告归档。Inspect-Build.ps1只读PE元数据和二进制SHA；不等同于Player运行。本轮额外未知/Title/Overflow工具在文档目录，仅注入Editor副本；发行代码不能依赖它们。
11. Collect.py <root> <repo>只发布本批拥有者根；原始日志压缩仅脱敏凭据值，原SHA/发布SHA分开。所有新结果与历史分离。最后核对用户/历史SHA、实际源/副本、LFS、远端main，不force push。

源目录中Invoke-Additional.ps1是本轮已完成Build之后的依赖调用清单（Missing/Corrupt/Entry/Catalog），不是新测试框架。各脚本均复用旧Step与NativeProbe；Worker不在默认路径时应传给既有底层脚本的WorkerPath或记BLOCKED，不退回用户桌面。

时限：新夹具内部180秒、旧Invoke-Checks外部600秒、batch外部1200秒、旧AI沿用原420秒；没有为追求通过放宽时限。原生UI/人工与发行Player运行不支持或未执行时NOT_RUN，不以编排器0代替断言。实际运行输入含保护的本机未提交场景/设置，只有哈希不提交内容；构建副本设置差异见build-inputs，不能声称纯Git输入逐字节重现。
