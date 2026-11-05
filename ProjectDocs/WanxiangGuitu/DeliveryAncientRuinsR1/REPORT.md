# CP06-C1-R1 远古遗迹奖励与关卡验收

从固定产品基准 31950f7bbd1f7946157632a52f1efd3854780340 创建 fix/cp06-ancient-ruins-r1。开工远端 main 为 72db192a527bd256e2ba18cd7ab334d8334051da。使用独立工作树与独立合成档。固定交付 SHA 以包含本文件的分支提交为准。

永久特殊奖励与普通掉落分开。五个永久 ID 共用一个档案账本，两件装备进入持久化营地待领区，三件剧情、收藏或机关权益直接记账。使用原有 v9 原子保存和领取事务。新 Run 的普通箱与守护者常规战利品继续重新生成。旧在途档按字段缺省继续使用旧规则。

回响石像第二阶段加入定向矩形裂地直扫与有内圈安全带的回响外环，保留齐射并加强封印震波。Editor 和非开发 Player 均记录实际减血、规避、击杀和读取恢复。五区沿原地图 Collider 与 NavMesh 验证往返。地图几何没有调整。

源码保护核对 2,413 个前批保护路径、199 个供应商文件及 1,370 项仓库产品输入。旧森林、七武器、CP04/CP05、CP06-A/B 和发行诊断配置保持冻结。测试与纯包程序集的 40 个关键类型 IL 一致。纯发行构建为 Windows64 非开发，0 错误、104 警告。实际 Bee 五项服务关闭。启动到正式标题并后台退出，实际退出码 0，合成存档哈希不变。

隔离缓存与仓库逐文件核对存在 16 项原始字节差异。其中 8 项是空白差异，包括 AdventureFlow 单行末尾空格。另有三份遗迹材质的 _Color 浮点序列化差、EditorBuildSettings BOM、ProjectSettings 中文转义、URP 预筛选、全局设置列表和 GraphicsSettings 默认序列化。构建绑定实际隔离输入，对仓库全字节构建等同性保留 UNRESOLVED。

- [奖励规则](REWARD_RULES.md)
- [第二阶段与实测间隔](BOSS_PHASE2.md)
- [五区连通](REGION_CONNECTIVITY.md)
- [存档测试与复跑](SAVE_AND_REWARD_TESTS.md)
- [验收清单](ACCEPTANCE.md)
- [失败历史](FAILURE_HISTORY.md)
- [原始证据索引](Evidence/INDEX.md)

## 共享代码审计

| 文件或入口 | 必要改动 | 风险与回归 |
| --- | --- | --- |
| AdventureState、AdventureValidation、RuinsSpecialRewards | 添加 v9 可选档案账本与新 Run 规则位，校验孤立待领、事件与死亡回执 | 旧版字段缺省，按旧路运行。旧三区与五区合成快照恢复单独归档 |
| AdventureFlow、AdventureFlow.Bosses、AdventureFlow.World | 新局规则选择、守护者检查点、复用营地领取事务 | 关注发布前回滚、发布后核对和同一结算幂等。旧森林检查点保留旧核对分支 |
| RuinsExploration、CombatEnemy、ForestRegionRuntime.Ruins | 将 R1 遗迹死亡的常规掉落与首次回执并入同一个检查点，并选择相应 Boss 行为 | 真实死亡、重复死亡、重复加载、下一 Run 和旧三区回归 |
| RuinsBossBrain | 增加 R1 觉醒阶段、两种物理范围及候选时间参数 | 测试同时核对受击与规避，旧规则按存档标志保留 |
| AdventureItems、AdventureFlow.UI、CatInventoryPresenter | 固定特殊装备命名、永久收藏展示、待领保护 | 普通道具和原有库存事务继续使用原路径 |

## 验收统计

当前可验收的 36 个独立案例共 1200 条 PASS。分层统计为 controlled Editor 16 案例、542 断言。controlled Editor rules 1 案例、33 断言。isolated nondevelopment Player 19 案例、625 断言。旧森林另有 6 组受控检查。10 个历史失败案例保留 31 条 FAIL，不并入通过分母。详见验收清单与语义回执。

两层各覆盖七武器 × 五区。普攻和各区域默认技能核对真实命中，大厅另核对扩展槽位。镰刀牵引的实际位移与无扣血分别记录。遗镰经仓库取出、实际拆解、保存读取、新 Run 再开隐藏箱后，永久回执仍在且未再发。
