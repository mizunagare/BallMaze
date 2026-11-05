# 跨进程恢复审计

测试源由正式保存代码产生，复制阶段逐文件核对 SHA256，启动全新 Player 并经过标题 Continue。另在隔离 Editor 真实采集一份阶段二检查点。原始 v9 封装 checksum、活动 Run 参考地面页的 SHA256、长度和数量由独立工具复核。

| 状态 | 生成及新进程 |
| --- | --- |
| 正常探索、机关门开启、密室箱已开 | R2Rewards → R2Salvage |
| 精英已死亡 | Elite → LoadElite，恢复死亡生命与实体 ID，重复死亡入口无新地面产物 |
| Boss 第一阶段 | Phase1 → LoadPhase1 初测恢复全生命和存档身份。Phase1Injured → LoadPhase1Injured 补证 HP 254，恢复后重新开始一阶段前摇，无旧招补发 |
| Boss 第二阶段 | Phase2 → LoadPhase2，HP 155 恢复，新一轮觉醒后才开始前摇 |
| 特殊待领取、已领取 | R2Boss → R2ResumeBoss，R2Rewards → R2Salvage，跨进程恢复待领取，再经实际领取、读取和拆解。LoadClaimed-R2ResumeBoss 与 LoadClaimed-R2Salvage 从实际已领取档案重新启动并核对整个 Profile |
| 撤离待提交 | R2Rewards → MakePending → LoadPending，真实引导撤离，下一进程核对相同结算 ID、Run ID 与档案 |
| 撤离已提交 | LoadPending → LoadCommitted，重复提交未增加 revision，仓库档案不变，再确认回营 |
| 旧版遗迹 | R2LegacyThree、R2LegacyFive，旧 v9 三区与五区原始检查点 |

二阶段运行时招式队列不写入 v9。验证以正确恢复 Boss 生命、重建阶段且不会补发保存前招式为准。人工重新操作、故意恢复旧外部备份和所有版本旧档迁移 NOT_RUN。

[快照审计](Evidence/Audit/v9-snapshots.json) · [过程与退出回执](Evidence/INDEX.md)
