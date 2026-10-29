# RUNLOOP-01 证据索引

工程外拥有者根I:/WGCombat/RUN01-1029-A；所有本轮数据独立，历史目录未回写。manifest记录原始/发布SHA；日志gzip仅脱敏凭据值。

| 路径 | 证据 |
|---|---|
| Before/fault-result.json | 修复前diskCommitted/rev4与livePending/rev3、错误反馈、actualexit1 |
| After/fault-result.json | 同一故障注入修复后状态/修订/Profile一致、actualexit0 |
| Cycle | 初次编译失败及执行源，不删除 |
| Stages/Running、Committed-2 | 两次夹具时序/表示失败和原始期望 |
| Stages/*-2、*-3、Shared | 有界修正及初始跨进程链，旧阶段文件保留 |
| Verified/Run | 真实出征/采集/一拾一留，9断言及Running主备档 |
| Verified/Running | 出口条件/提示/失败/取消/受击/倒计时，16断言及Pending主备档 |
| Verified/Pending | 发布前失败、发布后核对、唯一提交，8断言及Committed主备档 |
| Verified/Committed | 实际确认/营地统一支付/回滚/制造/存取/下一森林Run，10断言与新Run主备档 |
| Verified/Final | 4断言、新进程同后继Run；每阶段原始保存校验及来源账可查 |
| RuntimeAudit | 实际RuntimeForest/敌人/资源/事件实例恢复4项验证，不只比元数据 |
| STATE_TRANSITIONS.json、csv | 从原始v9包独立校验SHA256、提取阶段身份/修订/仓库，区分输入阶段名与输出状态 |
| Unknown-Missing、Unknown-Corrupt | 结果待核对、禁止保存/重提、精确字节恢复后正常Load、重复无收益 |
| Overflow | 15断言，满仓→待领取→显式领取到背包，地面/预览/未领取不混入仓库 |
| Death | 10断言，实际死亡损失，不把新得/地面奖励永久化 |
| Entry、EntryRun | 实际Title与Forest场景生命周期、GameEntry请求及进程回执；不是原生点击 |
| Catalog、Catalog-* | 目录状态、旧档只读、新档故障、归档中断及独立进程恢复 |
| Regression | 输入/观测/双Boss、正常AI三阶段，各实际exit和timeout |
| Regression/Normal-Gather | 实际木5/修渡口/结算/存取制造/再次出征轨迹、审计及恢复断言 |
| Build | 非开发BuildReport全部94警告、PE模块列表、EXE/程序集SHA、实际exit0 |
| FrozenProduct | 最终3产品源精确字节快照 |
| BaselineProduct | 从固定Git基线导出的3源（LF规范化），不冒称首次编译原始字节快照 |
| Bindings | 开工/结束用户与历史SHA、完整源/副本输入差异、执行顺序 |
| SUMMARY.json、ACCEPTANCE.csv | 按验收条目分层统计，原失败不折算成PASS |

新增状态提示只有源码/模型/受控业务验证；没有以截图、Editor或后台关闭冒充发行Player原生操作与人工。D3D12、青色帧、Search、JobTempAlloc与C15继续开放，见ACCEPTANCE。
