# B3 随机调用与兼容审查

开始本地/远端 main 均为 `0230ae0c8c0b57cb6dceb0f9aef566ad8e78c6cc`，保留 ProjectSettings.asset 未提交修改。用户已确认该边界补丁在源码与提交证据范围复审通过；不代表独立 Unity 运行。此次不改变 ShouldDropChestGear、不重写 B2。

| 原调用 | 用途 | 新 Run 所属随机源 | 旧在途 |
|---|---|---|---|
| ForestLayout.Generate | POI、节点、石块坐标 | 既有局部 System.Random(seed)，保持算法/布局revision3 | 加载保存布局，不重抽 |
| CombatWaveDirector.FindSpawn | 波次敌人坐标 | Placement | 原 Unity 全局流 |
| CombatWorldEvents.TryLocation | 波次事件位置 | Events | 原 Unity 全局流 |
| WorldEventPoint / ForestRewards | 宝箱装备概率、材料量 | Rewards | 原概率和全局流 |
| CombatEnemy / AdventureResource | 敌人掉装、皮料/晶石、采集量 | Rewards | 原概率和全局流 |
| AdventureItems / WeaponTraits | 装备品质、类型、词缀；实际制造词缀 | Rewards | 原算法和全局流 |
| HeroProgression.BeginChoice | 等级/祭坛技能候选 | Rewards，保存已抽 offers | 原全局流，保留已保存 offers |
| AdventureFlow.Depart | 新出征种子 | Guid 字节派生正 int，不受视觉/查询全局状态影响 | 不替换旧 seed |
| CombatFeedback | 演出偏移等 | 既有实例 System.Random(88217)，不保存 | 不变 |
| CombatSoundBank | 程序音效波形 | 既有每 cue 局部 System.Random(6721+cue) | 不变 |
| CombatFeedbackEffect | 火花 | 既有显式 ParticleSystem.randomSeed，禁用自动种子 | 不变 |
| CombatSaveSystem.randomStateJson | 兼容旧全局状态快照 | 保留，不作为新 Run 奖励来源 | 继续恢复原全局状态 |

`rg` 审查 Assets 全部 C#，无其他业务全局随机调用；Editor 测试驱动自有随机属于测试。UI、路线、配方缺口及图标加载未新增随机调用。

## 增量数据

RunState 增加默认 false 的 `hasRandomStreams` 和可选 `randomStreams`：version=1，rewards/placement/events 为 Unity Random.State 的 JSON 字符串。只给新出征初始化；沿用已有 Run seed、生成版本、森林布局及 v9 外层存档封装。随机算法版本独立于地图 generationVersion（仍5）及布局 revision（仍3）。旧档 hasRandomStreams 缺失/false 时，整局维持原全局流，下一次新出征才启用隔离；不猜测或补抽旧结果，不需要重写迁移文件。

初始化使用 seed XOR 三个固定通道盐，各自保留原 Unity 分布。同步抽样临时切换状态，finally 恢复调用者全局状态；不得跨帧/协程。只有抽样成功才推进该流。新 Run 的波次事件在初始化流后生成；恢复世界过程中重新建立临时对象不推进保存的流，最终仍采用原检查点的布局、事件、装备ID、地面掉落、offers 与状态。

Unity JsonUtility 会把 null 嵌套类在克隆/恢复后物化为空对象，因此不能靠类是否 null 判断旧档。明确标志为 false 时只允许空状态；true 则要求全部状态存在且合法。此兼容问题由实际旧森林夹具和合成旧字段回归暴露，失败记录保留。

存在启用标志但版本未知、状态缺失/不合法时拒绝加载/写入，不回退为“新种子重开”。原版本兼容、迁移前备份、分页、来源账和唯一结算保持原逻辑。新状态属于同一完整存档事务，写盘失败保留旧档；内存状态未确认时仍按原保存错误展示和重试。

## 明确边界

同一初始 seed、状态和操作顺序可重复相同奖励属性、材料和布局；装备唯一ID仍用 Guid，不承诺跨独立实验生成相同ID，但保存/恢复必须保留既有ID。不同操作顺序可改变同一个 Rewards 流后续结果，本批不实现 B4 路线，也不承诺每个实体独立奖励子流。旧在途仍有历史全局耦合，这是保留旧语义，不暗中启用新流。

营地/无 Run 的历史初始化与制造仍按原全局随机处理；它们不会影响下一新 Run 的种子或隔离状态。多场景调用带所属 Component；无上下文的兼容静态调用只允许唯一活动 Run，避免悄悄选择另一个世界。表现源保持现有实例随机，无需序列化演出噪声。
