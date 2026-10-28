# 91条警告的有限源码语义复核

本批只复核3个代表类别，全部91项仍OPEN；不迁移API、不重存场景、不把静态审查当运行等价证明。原PERF01风险分类与失败历史不重写，原文清单与固定源码94dcc009ff971272fc46d8c5b323cbb3251619b5关联。场景序列化2条保持原处置，不作为第4类继续扩展。

## 1. FindObjectsByType与排序枚举（72条关联诊断）

36个枚举附加诊断与36个API重载诊断关联，不能当72次实际运行调用。当前None返回值本来不承诺顺序；迁移到无排序参数也不能证明所有消费者等价。必须检查后续First/数组下标、scene过滤、inactive Include/Exclude、模板和稳定实体ID。特别是GameEntry旧世界清理、ForestRegionRuntime模板/恢复、CombatSaveSystem实体采集，不能漏掉inactive导致旧世界残留或把模板当活体。敌人、掉落、事件的业务身份来自实体ID，不应由对象枚举顺序替代。

最小未来方案：按单一调用点证明过滤与消费，保留原inactive语义，必要时明确owner/scene和稳定ID排序；禁止全局机械替换。必要回归：旧世界卸载、同时存在模板和活体、已清空据点恢复、掉落分页、唯一结算、交互显示/执行、RNG只读查询。当前没有Profiler调用栈证明该类为已确认性能瓶颈。

## 2. FindFirstObjectByType（14条）

当前First的选择与InstanceID排序相关，不等于业务单例或当前Run身份；替换Any可能选择不同实例。AdventureRandom、PlayerInput、GamePreferences、CombatSession等归属路径须检查上下文：是否有活动/非活动旧session、是否通过owner组件定位、启动/场景过渡是否有两个实例。某次测试只观察到一个session不等于所有恢复路径永远唯一。

最小未来方案：对单例先验证唯一性，对已具上下文的调用用显式scene/owner引用，不用未排序First偷换身份。必要回归：Boot→Title→Continue、返回标题、坏档拒绝、Pending/Committed恢复、旧世界销毁、多session负例、随机流与进度路径不串档。仅建议，不实现。

## 3. CS0414三个字段

PlayerInventory.nearest/nearestEvent为private非SerializeField，仅声明/null赋值，当前交互来自InteractionResolver；ThirdPersonHero.nextAttack仅声明/0重置，实际攻击冷却来自AdventureCombat.attackAt。静态字面搜索未发现反射读取，但不能证明所有动态反射路径不存在。不是有效存档字段，也没有证据将其称为当前性能瓶颈。

最小未来清理应独立获准后删字段及无效赋值，保留交互器与AdventureCombat原状态；回归E/H目标一致、付费动作不偷偷切换、武器切换不刷新冷却、死亡/恢复/暂停边界。当前不删字段、不改变类布局或生命周期。

## 证据口径

本轮脚本重新读取这3类别所对应的完整文件，输出源码SHA、精确行列与引用上下文；与PERF01 warning原文逐条关联。此处是语义风险审查，不声称API迁移等价、动态反射穷尽或警告已修复。最终验证结论以本批REPORT与原始只读审计JSON为准。
