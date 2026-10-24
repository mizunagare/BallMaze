# B07 验收表

以下全部取自最终新 All；历史失败单独保留，不拼接旧 PASS。

| 编号 | 检查 | 状态 | 实际证据类型 |
|---|---|---|---|
| S01 | Editor隔离固定种子仅使用一次、全局随机状态不变 | PASS | Editor专用测试入口；正式Player不含入口；`B07SeedReplay.Run` |
| B01 | 非开发Windows64构建 | PASS | BuildOptions.None；完整警告另存；`WanxiangBuild.ValidateBuild` |
| C01 | 定义、固定种子、合法导航、首次/重复、原子故障 | PASS | 受控规则/物理导航；`B07Rules.Run` |
| C02 | 六攻击命中/闪避/越界、四武器普攻和主动技能 | PASS | 受控真实伤害/物理；`B07Combat.Run` |
| C03 | 逐攻击前摇中断、恢复时钟、冲锋抗硬直但受伤 | PASS | 受控真实伤害；不宣称胜利；`B07Interruptions.Run` |
| C04 | 两个seed×两首领×满血/半血，攻击及脱战返巢 | PASS | 8组受控AI，不是正常冒险；`B07Liveness.Run` |
| C05 | 满包保留地面装备、整理拾取、穿戴不保护、死亡后重复收益 | PASS | 受控经济/真实死亡提交；`B07Economy.Run` |
| P01 | Running/Pending/Committed新进程恢复、实际对象及防重复 | PASS | 三个独立Editor进程；`B07Rules.Resume`, `B07Rules.PendingResume`, `B07Rules.CommittedResume` |
| N01 | 陆地Boss采集/制作/战斗/撤离/入仓/再制造/再次出征/继续 | PASS | 正常NPC AI与领域机器人；不是原生输入；`normal-ai.Land.Normal`, `normal-ai.Land.Resume`, `normal-ai.Land.FinalResume` |
| N02 | 湖中Boss同一完整循环与免费出口 | PASS | 正常NPC AI与领域机器人；不是原生输入；`normal-ai.Lake.Normal`, `normal-ai.Lake.Resume`, `normal-ai.Lake.FinalResume` |
| N03 | 采集、遗迹、绕行三种既有策略 | PASS | 9个正常AI进程；`normal-ai.Gather.Normal`, `normal-ai.Gather.Resume`, `normal-ai.Gather.FinalResume`, `normal-ai.Treasure.Normal`, `normal-ai.Treasure.Resume`, `normal-ai.Treasure.FinalResume`, `normal-ai.Bypass.Normal`, `normal-ai.Bypass.Resume`, `normal-ai.Bypass.FinalResume` |
| R01 | B1费用/回执、B2目标、B3随机流、R1路线评分 | PASS | 本轮重新执行，非继承；`WGB1Check.Run`, `WGB1Check.Resume`, `WGB1Routes.Run`, `B2Rules.Run`, `B2Rules.Resume`, `B3StreamRules.Run`, `B3Checks.Run`, `B3Checks.Resume`, `RouteScoringRules.Run`, `RouteScoringRules.Resume` |
| R02 | 旧档迁移、旧森林、合法空状态与恢复 | PASS | 合成旧档/历史夹具；`B05LegacyMigrationCheck.Run`, `B05V7MigrationCheck.Run`, `B06V8MigrationCheck.Run`, `WGLegacyForestCheck.Run`, `WGA1Check.Empty`, `WGA1Check.Recovery` |
| P02 | B07实际冒险派生存档在正式Player保存与新进程继续 | PASS | 非开发Player；后台WM_CLOSE；非原生战斗；`B07-Player.B07-Land.1`, `B07-Player.B07-Land.2`, `B07-Player.B07-Lake.1`, `B07-Player.B07-Lake.2` |
| U01 | 最终Player的原生鼠标键盘U16 | NOT_RUN | 无安全独立交互环境，不以截图/WM_CLOSE替代 |
| U02 | 独立人工可理解性与原工程人工试玩 | NOT_RUN | 未安排，不以机器人替代 |
| U03 | 最终Player原生Boss战 | NOT_RUN | 最终Player仅启动/退出/恢复，Boss实战来自隔离Editor正常AI |
| D01 | D3D12 UNKNOWN根因 | UNRESOLVED | 沿用UNRESOLVED，不作无新线索实验 |

## 本轮 All 状态行统计

{"PASS": 115, "FAIL": 2, "NOT_RUN": 27, "UNRESOLVED": 1}

非预期失败：0。两个标准负探针单列，不改写为PASS。

协调器成功结束只表示编排完成且无非预期失败，不等于原生UI、人工理解或发布验收通过。

完整命令、时间、退出码、超时与原始分类：[FinalAll/results.json](Evidence/FinalAll/results.json)。
输入/构建/截图：[证据索引](Evidence/INDEX.md)。历史：[失败记录](FAILURE_HISTORY.md)。

首次奖励“已领取”字段表示已生成首奖一次，不表示自动拾取或已入仓；徽章永久，物质战利品仍可因失败损失。
两首领任意顺序；双首领纪念标记不开放未经授权的后续地图。
