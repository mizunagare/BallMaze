# 阶段2存档与经济边界

保存格式仍v9；不新增存档槽、Profile/Run字段、布局修订、随机流版本或迁移。CombatHealth新增的是未序列化的只读累计观测属性，不被CombatCheckpoint/CaptureLegacy写入。新进程从0观测，实验侧将上一进程的统计保存到**独立测试指标文件**，绝不写回游戏存档或修改HP。

现有业务合同保持：

- 保护入场非消耗装备，穿戴本局战利品不赋予保护；药水/材料已消费不因死亡恢复。
- 地面掉落与已拾取、待结算、已提交、待领取分开；没有领取/结算的收益不加仓库。
- B1渡口木2/石1一次性原子扣费、回执、中断、取消与免费出口；B2实际制造成本/前置链；B3已保存随机状态；B4-R1实际导航与旧revision；Boss首次/重复奖励和徽章；教程均沿用原路径。
- 正常AI真实调用Commit、重复提交检查、Acknowledge、TransferMaterial、Craft、上盘和下一次Depart。新制造ID必须存在于新Run的入场装备；不能只显示一个布尔成功。
- 运行中暂停/退出后继续原Run；Pending/Committed及异常恢复由本轮既有规则的新进程用例验证。某个正常AI三进程闭环不等于所有迁移/故障状态都覆盖，结果分别列明。

本轮三构筑使用相同的**合成营地已有物品集合**，不是正式新玩家获得高品质胸挂或材料的奖励。局内/营地的实际消费均使用真实API与来源账，初始合成库存不算探索收益。

源码兼容不等于当前运行PASS。v1～v9、分页、满仓、重复结算、写盘失败和新进程恢复结果以本轮完整All为准，未完成前不得引用B10旧PASS冒充新验证。

用户ForestRuins与ProjectSettings的开工SHA256见START_BASELINE.json，完整运行后还需重新核对。禁止读取真实LocalLow档、将原档用作故障注入或为了迁移清档。测试指标/来源账投影可以公开；完整save.json、ground-loot页、迁移集合和内存转储不发布。

## 本轮已执行证据

最终All重新执行B05LegacyMigration/v7、B06v8、B09旧v1～v9及入口状态/中断恢复；B07Rules运行中、PendingResume、CommittedResume均PASS。B05/B06/A1/B1分页、来源账、迁移发布/缺页/失败重试、死亡/放弃、满仓待领取与重复提交测试本轮PASS，完整方法与实际退出码以FinalAll/results为准，不继承历史提交。

19案例57进程均完成；restore-projections记录每次两阶段Profile/Run/区域/seed/出口回执及layout/streams/ledger/gear/entities/ground/warehouse/recipes/hunts哈希，NEW_PROCESS_FULL_STATE_PASS由真实驱动比较原快照而得。后继Run ID必须不同于首Run；制造ID在新入场清单中。恢复是继续保存状态，不依赖重新抽种子。

完整合成save/分页保留外部，不提交；发布的事务/指标/身份哈希是合成投影。存档结构仍v9，没有迁移新增字段；TotalDamageTaken不入存档，新进程计数由实验外部文件合并，不改变Profile/Run。两用户原文件哈希经FinalAudit/user-input-proof再次一致。
