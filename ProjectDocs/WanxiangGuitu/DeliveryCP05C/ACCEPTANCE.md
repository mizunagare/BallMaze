# CP05-C验收

基准7fc4f5dc3043bcbb69f63c2ebf267359741ccbbe。只验证本批两项缺陷，不更改冻结镜头/软锁定参数。

| 要求 | Editor | 非开发测试Player | 证据/边界 |
|---|---|---|---|
| 连续三次重开，无重名 | PASS | PASS | 两层probe的restart-1/2/3及restarts.jsonl |
| 暂停后重开 | PASS | PASS | paused-restart/new-instance-unpaused |
| 真实玩家死亡后重开 | PASS | PASS | real-ai-player-death/death-restart，实际敌人攻击 |
| 冲突失败后旧实例保留并重试 | PASS | PASS | collision-fault-*，外来同名scene不删除 |
| 多敌连续死亡、真实装备地面掉落 | PASS | PASS | death-0..5、real-equipment-drops-exercised |
| 一次死亡最多一次处理 | PASS | PASS | 每次完成计数+1；重复5次请求无物品/XP/RNG变化 |
| 卸载及重新进入 | PASS | PASS | old actors/materials、context、eventsystem、event订阅、external-unload/reenter |
| 正式森林掉落不回归 | PASS | PASS | 各480组规则及同Run实际死亡配对，不是用选中目标当命中 |
| 存档、背包、全局RNG不受训练影响 | PASS | PASS | canary字节、bag/global/local每次死亡及故障前后 |
| 正式场景不能使用训练上下文 | PASS | PASS | formal-context-registration-rejected |
| v9原样继续及三随机流 | PASS | PASS | formal-save-v9、paired-results |
| 四个冻结脚本、用户文件 | PASS | PASS | protection-final.json；本批未改Scene/Prefab/ProjectSettings/依赖 |
| 纯发行无驱动、Privacy五项服务关闭 | PASS | PASS | assembly-audit/release-identity；构建0错误98警告 |
| 纯发行启动/普通退出 | NOT_RUN | PASS | PureSmoke只烟测，无自动输入/战斗 |
| 原生键鼠 | NOT_RUN | NOT_RUN | 无物理操作者证据 |
| 人工体验 | NOT_RUN | NOT_RUN | 自动化/截图不替代 |
| 新增性能专项 | NOT_RUN | NOT_RUN | 本批无Profiler性能结论 |
| Editor退出JobTempAlloc及历史引擎问题 | UNRESOLVED | UNRESOLVED | 保留原始日志；不将退出码0当根因解决 |

最终核心功能共270条本轮断言PASS、0 FAIL（Editor/Player各135），独立8项审计自测通过。16项配对汇总复核与功能有重叠，单列不累加。历史失败单列于FAILURE_HISTORY，不被这一统计覆盖。

[Editor训练](Evidence/AfterTraining4/probe.json) · [Player训练](Evidence/AfterPlayer/probe.json) · [Editor森林](Evidence/AfterFormal/probe.json) · [Player森林](Evidence/AfterPlayerFormal/probe.json) · [配对](Evidence/paired-results.json) · [保护](Evidence/protection-final.json)
