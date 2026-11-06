# B.1 开工方案与预注册比较口径

只修改三个非冻结入口：CrystalCavernBossRewards 的消息时机上下文、AdventureFlow.Bosses 的已确认后消息、CombatEnemy.DisplayName 的 C24 实例显示分支。没有新增持久化字段；不改保存算法、奖励生成、RouteScoring、Boss 环形判定、TargetAssist 或镜头。

提示测试：旧纯包只读副本保留 pre-publish 失败前错误消息；候选分别验证 before-publish 失败、after-publish 确认丢失、正常确认、重复重试、同档案旧首奖待领/已领取/已拆解的重复击杀。真实 NotifyMessage 的通知队列和计时器、检查点及 UI 截图分开留证。

N02 参考源 `37b25bb641c72deefe4e7e48f19f270711f7fc01`，不是 B。两端读取相同历史隔离合成在途存档。先登记：POI ID、状态、计数、出口身份、排序离散项精确相等；连续数值记录两端原始值、绝对差、相对差，绝对差 <= 0.0001 或相对差 <= 0.00001 为数值比较口径。该口径仅用于新 N02，不用于改写 B 的 C02/C04。运行后不调整门槛；无有效双端输入不判 PASS。

晶环：正常 AI 到达 P2 环招，分别记录内侧擦边、外侧擦边、明显环带和明确外侧安全。以实际 CharacterController 胶囊体几何推导环带相交作为独立几何判据，同时记录产品 root 判据和 Player HP。控制墙体 LOS、高度、翻滚状态、释放序号；不改半径或伤害。若存在语义差异，仅提案。

新纯包必须由候选源码生成，Development=false、Bee 五服务关闭，测试 sidecar 仅进入其副本。原 B 纯包、证据和统计只读。C02/C04 FAIL，C05 INCOMPLETE，不采样。
