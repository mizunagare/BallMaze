# 独立验收项

以下为结论范围，不把所有启动断言相加冒充完成度。严格失败和证据不足保持原状态；没有整批总 PASS。

| ID | 项目 | 状态 | 原始证据 / 边界 |
|---|---|---|---|
| B01 | 非开发发行构建 | PASS | Runs/Phase2PureBuild1；BuildReport、实际进程 0、111 warnings；Bee 五服务关闭 |
| B02 | 无驱动纯包标题、合成存档保护、真实退出 | PASS | Runs/PureTitleFinal1；后台关闭，不是原生菜单退出 |
| B03 | 无驱动纯包原生战斗/菜单操作 | NOT_RUN | 不将测试 sidecar Player 结果移植到本层 |
| E01 | Editor 挑战/返回/剑杖/两阶段 | PASS | EditorStage1NonBatch、EditorStage1Open、EditorSword2、EditorStaff1、EditorPhase1 |
| E02 | Editor 新进程恢复 9 断言 | PASS | EditorPhaseRestore1；同 Run/内容、HP/阶段、安全窗、不重放 |
| P01 | 测试 Player 新进程恢复 9 断言 | PASS | PlayerPhaseRestore1；独立于 Editor |
| P02 | 测试 Player 不挑战、开闭桥、失败保存不启战 | PASS | PlayerStage1Bypass、PlayerStage1Open、PlayerStage1 |
| C01 | 七武器普攻和默认技能实际命中 | PASS | PlayerWeapon0/1/2/3/11/12/13A1；活 Boss，真实碰撞轨迹和 HP |
| C02 | 五近战晶柱配对严格三维起点一致性 | FAIL | CombatMatrixAudit1；双刃、巨剑 Y 浮点微差。全部无遮挡命中/阻挡无伤记录保留，不宣称逐值同位通过 |
| C03 | 13 个 Boss 释放、命中/规避及分区样本 | PASS | pair-*-A1；Cross 两击分记；Ring band/inner/outer；限观察样本 |
| C04 | Boss 配对严格三维起点一致性 | FAIL | CombatMatrixAudit1 六组严格比较失败；同指令/同平面、不同落地 Y 微差，不事后加容差 |
| C05 | P1 扇扫前摇跨半血精确顺序 | INCOMPLETE | WindupNewAudit1；不再重复采样，不以 C03 或正常击杀补证 |
| R01 | 写入失败、同批重试和新进程核对 | PASS | PlayerRewardBefore2 / PlayerRewardBeforeRestore1 |
| R02 | 已写入但确认丢失、完整奖励检查点读回 | PASS | PlayerRewardAfter1 / PlayerRewardAfterRestore1 |
| R03 | 目标无可容纳空间、拒领与重启 | PASS | PlayerPendingFull1 / PlayerPendingFullRestore1；实际目标背包无足够空间、无自动转存 |
| R04 | 实际领取、实际拆解、重启永久回执仍在 | PASS | PlayerClaimSalvage1 / PlayerSalvageRestore1 |
| R05 | 同档案新 Run 正常 AI 两阶段击杀再获普通掉落 | PASS | PlayerNormalRepeat1；首奖 earnedRunId 不覆盖；不改血/传送/冻结/注入 |
| R06 | 拾取、撤离、入仓及新进程重复确认幂等 | PASS | PlayerNormalBankRestore2；完整 Profile 与 revision |
| N01 | C24 风险三态与导航/评分贡献一致 | PASS | route-three-A2、route-dead-A1；旧晶核精英风险不归因于新 Boss |
| N02 | 旧地图完整同输入评分数值配对 | NOT_RUN | 只执行旧布局排除 C24 判定，未重跑旧完整评分矩阵；不继承历史 PASS |
| V01 | 连续肩后采集序列 | PASS | PlayerSword1、PlayerStaff1、PlayerNormalRepeat1 的 frames + capture.tsv；是自动采集，不是人工体验 |
| V02 | 原生输入 | NOT_RUN | 未由真实操作者执行 |
| V03 | 人工可读性和手感 | NOT_RUN | 等待独立试玩 |
| V04 | 最终平衡 | NOT_RUN | 参数仅候选，样本不证明平衡 |
| V05 | 校准 CPU/GC/GPU 性能预算验收 | NOT_RUN | 未用计数器 0 宣称性能通过 |
| H01 | 用户文件和冻结产品边界 | PASS | user-files-after、protection-final；无 ProjectSettings/依赖/镜头/武器变化 |
| H02 | 冻结发行包未变 | PASS | frozen-release-recheck；193 文件逐项哈希 |
| H03 | 构建输入完整语义等同性 | UNRESOLVED | 新材质 _Color 写回及历史构建开放项；Resources.meta 前记录另缺证 |
| H04 | 历史引擎、C1/R7 图形调查 | UNRESOLVED | 原记录不关闭、不重开同范围调查 |

本表统计由同目录工具生成到 `Evidence/acceptance-counts.json`。原始尝试统计与本表不同，参见 `Evidence/run-summary.json`。所有证据均位于 [Evidence/INDEX.md](Evidence/INDEX.md)。
