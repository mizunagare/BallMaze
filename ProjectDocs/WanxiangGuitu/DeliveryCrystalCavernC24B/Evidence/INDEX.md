# 原始证据索引

[archive-origin.json](archive-origin.json) 列出本次归档 **1660 文件**的原始绝对路径、大小和 SHA256。原文件仍在 `I:/WGCombat/C24-1106-A`，归档为只读复制；历史目录未覆盖。未来添加必须使用新目录和新 manifest。所有合成存档仅用于隔离验证。

## 入口、构建和保护

- [基准](baseline.json)、[基准产品文件](baseline-inputs.json)、[最终差异](protection-final.json)、[用户文件](user-files-after.json)。
- [冻结发行清单](release-audit-Phase2PureBuild1.json)、[193 文件复核](frozen-release-recheck.json)。本地完整包 `I:/WGCombat/C24-1106-A/Phase2PureBuild1/Release`；未将通用 Unity EXE 当作唯一版本身份。
- [BuildReport/发行回执/Bee](Runs/Phase2PureBuild1/BuildReceipts/)、[Unity 完整日志](Runs/Phase2PureBuild1/Unity.log)、[实际退出](Runs/Phase2PureBuild1/Editor.exit.json)。
- [纯包真实运行](Runs/PureTitleFinal1/pure-runtime.json)、[标题入口事件](Runs/PureTitleFinal1/entry-audit.jsonl)。
- [新材质导入差异](material-import-diffs.txt)、[工作树/隔离工程哈希](current-product-vs-built-project.json)。

## 战斗

- [Player 两阶段](Runs/PlayerPhase1/)、[Player 独立恢复](Runs/PlayerPhaseRestore1/)、[Editor 恢复](Runs/EditorPhaseRestore1/)。
- 七武器：`Runs/PlayerWeapon0A1`、`1A1`、`2A1`、`3A1`、`11A1`、`12A1`、`13A1`，各有 melee/new/projectile/health 原始轨迹、配装及进程证据。
- Boss 配对：`Runs/pair-p1-Claw-hit-A1` / `evade`，P1 Volley、P2 Claw、P2 Volley、P2 CrossLines 同命名；`Runs/pair-p2-HollowRing-hit-A1` / `inner` / `outer`。
- 近战晶柱：`Runs/weapon-clear-{0,1,11,12,13}-A1` 和 `weapon-block-…`；仅指定夹具碰撞体开关，不是对产品地图关碰撞。严格起点差异保留。
- [只读矩阵审核](Runs/CombatMatrixAudit1/summary.json)、[逐项结果](Runs/CombatMatrixAudit1/results.json)、[输入哈希](Runs/CombatMatrixAudit1/inputs.json)。
- [A2/B2 证据不足审核](Runs/WindupNewAudit1/)，原 A1/B1 错误 JSON 与拒绝记录在 PlayerWindupA1/B1、WindupReadOnlyAudit1；不得拼接补证。

## 奖励和正常流程

- 写入失败：`Runs/PlayerRewardBefore2` / `PlayerRewardBeforeRestore1`。
- 已提交确认丢失：`Runs/PlayerRewardAfter1` / `PlayerRewardAfterRestore1`。
- 满包拒领及恢复：`Runs/PlayerPendingFull1` / `PlayerPendingFullRestore1`。
- 实际领取拆解及恢复：`Runs/PlayerClaimSalvage1` / `PlayerSalvageRestore1`。
- [正常 AI 完整流程](Runs/PlayerNormalRepeat1/)，camp-before.json / new-run.json / ordinary-death-proof.json / camp-after.json 为同档案新 Run 两笔账；正常帧轨迹与 75 张采集帧一并保留。
- [新进程入仓核对](Runs/PlayerNormalBankRestore2/)。首次 PlayerNormalBankRestore1 错断言未删除。
- 风险贡献：`Runs/route-three-A2` / `route-dead-A1`；首次 route-three-A1 总风险错误断言保留。

## 画面与失败

- [贴身持剑连续帧](Runs/PlayerSword1/frames/)、[肩后法杖连续帧](Runs/PlayerStaff1/frames/)、[正常 AI 帧](Runs/PlayerNormalRepeat1/frames/)。时间索引各目录 capture.tsv。自动截图序列不代替录制帧率保证、人工可读性或键鼠操作。
- 编译失败及警告：[Compilation](Runs/Compilation/)；每轮精确驱动：[ExecutedDrivers](Runs/ExecutedDrivers/)。
- 全部逐运行断言统计：[run-summary.json](run-summary.json)；[失败说明](../FAILURE_HISTORY.md)。

构建包、Unity 缓存、供应商源码不提交到本证据目录；完整构建输入及包身份通过清单关联。本批只推送独立分支。
