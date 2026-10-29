# RUNLOOP-01-R1 限定验收

结果由本轮新执行产生，不继承历史 PASS。最终机器可读口径见 [status.json](Evidence/status.json)。受控界面命令不是原生鼠标键盘。

| 项目 | 状态 | 证据与判据 |
|---|---|---|
| T01 预期 Committed | PASS | R1Matrix 的 published 与原 RunloopFault：磁盘/内存完整回执、Profile、修订一致，不再次发奖 |
| T02 确切旧 Pending | PASS | exact + retry：保留真实分页，发布前失败允许重试；成功后重复请求不新增修订 |
| T03 同身份不同计划 | PASS | plan：人工候选先完整 v9 校验；冲突进入待核对，不覆盖 |
| T04 受保护内容差异 | PASS | outcome、quantities、checkpoint、source 为四个分立合法 v9 负例，逐项拒绝 |
| T05 身份/修订差异 | PASS | revision、profile、identity，最后者整体替换关联 Run 身份，保持 v9 关系合法 |
| T06 主档缺失/损坏 | PASS | missing/corrupt 与原 Uncertain 两专项，恢复原已发布字节 |
| T07 解析失败 | PASS | parse：主备均不可读时保留读取入口和写入门禁 |
| T08 Committed 运行时失败 | PASS | 一次 before-camp-load 失败后 HasResult 页面仍选择完整读取 |
| T09 相同入口再读 | PASS | 同一个 ExecuteSettlementPrimaryAction；不额外发布修订、增发收益，磁盘语义不变 |
| T10 Pending 运行时失败 | PASS | 一次 before-build 失败后不能提交，解除故障后完整读取再正常结算 |
| T11 保存回调保护 | PASS | 主备档/全部分页 SHA256、Profile/Run 比较；自动、手动、受控 F5、失焦、暂停、退出回调 |
| T12 正常继续 | PASS | Pending 恢复后提交；五个独立进程恢复、确认、制造及后继森林 Run；实体审计另列 |

| 附加范围 | 状态 | 证据 |
|---|---|---|
| 迁移门禁有限回归 | PASS | v1～v8，故障保留原字节/门禁，同命令重试成功，最终 v9、可写 |
| 标题与目录恢复 | PASS | EntryRun、Catalog Run/Resume/Interrupt/Recover，真实入口事务和独立进程 |
| 输入、观测、Boss | PASS | 原有 Input01Rules、S2R1ObservationProbe、B07Combat 新运行 |
| 正常 AI | PASS | 采集、渡口、撤离、入仓制造、后继森林与新进程恢复；不冻结敌人 |
| 非开发构建 | PASS | 原发行 BuildOptions.None，完整 BuildReport 警告与哈希 |
| 发行程序集边界 | PASS | 只读 PE 元数据，无 Editor 夹具/UnityEditor 引用；不是 Player 运行证明 |
| 用户与历史保护 | PASS | user/history before/final SHA256，保留原四 exit1、aggregate 和历次报告 |

两项 findings 在交付方标记 FIXED、等待固定 SHA 独立复审，不能自行标为审核关闭。原任务审核模型结论不冒充 Unity 重跑。

## Deferred

原生 U16、独立人工、性能预算、隔离验收 Player 专项、纯发行 Player 实际操作本轮 NOT_RUN。受控 F5/按钮命令与退出回调不替代这些层级。全部 terminal/ack 发布阶段排列仍未穷尽。

D3D12 UNKNOWN、Editor 青色帧、Editor.Search、JobTempAlloc、旧 C15 根因继续 UNRESOLVED。历史失败不覆盖、不涂绿；attempts 与 current_acceptance 分开统计。没有无新线索的关闭实验或生命周期试探改动。
