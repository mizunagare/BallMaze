# R2 验收结论

| 项目 | 状态 | 来源 |
| --- | --- | --- |
| 永久 ID、档案归属、满包、跨进程待领和已领 | PASS | R2Rewards、R2Salvage、R2ResumeBoss、LoadClaimed 系列与 v9 文件 |
| 实际拆解后重启、新 Run 再开箱、重复领取拒绝 | PASS | R2Salvage、LoadClaimed-R2Salvage |
| 旧在途 v9 三区与五区 | PASS | R2LegacyThree、R2LegacyFive |
| 白、绿、紫重复获得以及铁矿、晶屑、兽皮和核心 | PASS | WhiteRetry、Green、R2Boss、R2ResumeBoss |
| 白装备首次限额抽样 | FAIL | White 18 局仅 1 件，重跑另列 |
| 真实死亡、同 Run 回调幂等、新 Run 常规 Boss 掉落 | PASS | R2Boss、R2ResumeBoss、Elite、LoadElite |
| 两阶段、两新增招式命中和规避 | PASS | R2Boss、R2Death、EditorPhase2 |
| 玩家五区物理往返、门、转角、楼梯、石柱墙体 | PASS | R2Rewards、R2Assist、R2WallStaff、R2WallBow |
| 精英与守护者实际导航位移 | PASS | Elite、R2Boss、Audit/enemy-movement.json |
| 敌种与每个门洞及楼梯的全排列 | NOT_RUN | 本轮只验证选定活体遭遇 |
| 七武器五区、真实 Boss 普攻、暂停取消与切换 | PASS | 七武器矩阵 |
| 典型目标辅助及远程实体遮挡 | PASS | R2Assist、R2WallStaff、R2WallBow |
| 七武器分别完成 Boss 两阶段、各辅助和遮挡组合 | NOT_RUN | 真实完成两阶段的样本使用长剑 |
| 探索、门、密室、精英死亡、活体两阶段、奖励与撤离跨进程 | PASS | 跨进程恢复审计 |
| 旧 v1–v8 全量迁移、人工体验、原生键鼠 | NOT_RUN | 未使用真实用户档或物理输入 |
| 冻结纯发行包启动及退出、诊断关闭保护 | PASS | 冻结构建哈希、R2PureBoot、Build Bee、IL 核查 |
| 仓库与隔离构建输入字节等同性 | UNRESOLVED | 16 项隔离输入差异，构建绑定实际输入 |
| 历史内存漂移 | UNRESOLVED | 继承既有观察，本轮无独立长时性能实验 |
| JobTempAlloc 根因 | UNRESOLVED | 实际构建日志及既有记录 |
| MapMagic 版本标签 | UNRESOLVED | 商店与源码/旧标签差异，未获新上游证据 |
| GC/GPU 校准与性能预算 | NOT_RUN | 本轮不以零计数或静态推断通过 |

本轮没有产品缺陷被这些样本证实。表中未执行或未解决的范围保留给后续独立复审。
