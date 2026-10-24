# B3 验收

结果为本机实际运行范围，推送不代表复审通过。完整命令/退出码/超时/日志见Evidence各轮。

| 验收项 | 状态 | 依据 |
|---|---|---|
| 全项目随机调用分类、增量方案 | PASS | RANDOM_AUDIT；73源码对应 |
| 固定种子/初始状态/操作可重复，不同种子合法差异 | PASS | B3StreamRules、B3Checks |
| 布局、奖励、表现/全局隔离 | PASS | 原局部布局生成；500噪声、Placement/Events扰动与奖励比较 |
| 查询前后状态和下一奖励结果 | PASS | 完整Run与Unity状态比较，实际24段装备/材料序列比较 |
| 已开遗迹、装备ID、地面材料不重抽 | PASS | 实际开箱与恢复，重复开启拒绝 |
| 旧v9缺字段、旧森林夹具、原随机语义 | PASS | 显式has标志；WGLegacyForest及B3旧语义 |
| 损坏/未知随机状态拒绝、写盘失败恢复 | PASS | B3StreamRules及实际失败写盘/重载 |
| B2必出/概率边界、重复敌人掉落、目标和来源账 | PASS | 本轮B2Rules Run/Resume |
| B1收费、回执和新进程 | PASS | 本轮WGB1Check Run/Resume；保留Before通行失败 |
| A1隔离、迁移、空目标及恢复 | PASS | 本轮A1选定矩阵 |
| 装备、容器、双武器、制造、分页/结算故障 | PASS | 选定历史回归 |
| 正常AI采集修复撤离入仓制造再出征/新进程随机状态 | PASS | Normal/Resume真实exit0，无超时；不是原生输入 |
| 非开发构建 | PASS | 0错误63警告，完整哈希 |
| 92帧受控UI矩阵 | PASS | 实际capture及布局断言，非原生U16 |
| 未选完整历史矩阵 | NOT_RUN | 17项如实列出 |
| 原生U16/人工理解/正式Player标题栏关闭 | NOT_RUN | 没有安全独立交互环境，不替代 |
| UI-01 UNKNOWN根因 | UNRESOLVED | 无新诊断，不重复实验 |
| Before偶发B1通行失败根因 | UNRESOLVED | seed10失败保留，后续通过不证明根因解决 |

最终汇总37 PASS、2预期探针FAIL、17 NOT_RUN、1 UNRESOLVED；非预期FAIL=0。历史失败和独立开放风险不从记录中删除。详细边界及历史见REPORT。
