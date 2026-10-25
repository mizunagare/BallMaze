# B08 验收表

结果仅来自本次最终完整All；历史失败保留，未执行不继承。

| 编号 | 检查 | 状态 | 证据类型 |
|---|---|---|---|
| B08-01 | 新增契约/旧档显式可选状态 | PASS | 受控规则；包括未完成禁止推进、错序设施、保存故障、只读帮助与图标；`B08Probe.Run`, `B08Rules.Run` |
| B08-02 | 真实采集拾取/账目/撤离取消/结算/取材制造 | PASS | 受控NPC关闭；调用实际业务与真实倒计时，不是原生输入；`B08Rules.Run`, `B08Rules.Resume` |
| B08-03 | 在途/营地/完成阶段跨进程继续 | PASS | 独立Editor进程；Run/装备/来源账/随机/教程；`B08Rules.Resume`, `B08Rules.FinalResume`, `B08Rules.CompleteResume` |
| B08-04 | 死亡/放弃重试、跳过后完整循环与继续 | PASS | 受控业务；无补偿或教程奖励；`B08Recovery.Run`, `B08Recovery.Resume` |
| B08-04A | 营地真实移动/E交互、战斗时钟和五类冷却暂停 | PASS | 受控一秒时钟/真实控制器；不重置技能或制造物资；`B08CampPause.Run` |
| B08-05 | 40分辨率/缩放/帮助/错误/仓库布局 | PASS | 实际渲染的受控夹具；边界/4标签/主目标/只读断言，不是人工可理解性；`B08Visual.Run` |
| B08-06 | 首次正常冒险、制造、第二森林及继续 | PASS | 正常NPC AI+Editor领域机器人；实际移动/普攻/显示E目标/撤离；`normal-ai.Tutorial.Normal`, `normal-ai.Tutorial.Resume`, `normal-ai.Tutorial.FinalResume` |
| B08-07 | 最终非开发Player恢复教程完成的森林Run | PASS | 显式隔离合成档；启动/后台WM_CLOSE/审计；不是原生UI；`B08-Player.B08-Tutorial.1`, `B08-Player.B08-Tutorial.2` |
| REG-01 | B1/B2/B3/路线评分规则与恢复 | PASS | 本轮实际重跑；`WGB1Check.Run`, `WGB1Check.Resume`, `WGB1Routes.Run`, `B2Rules.Run`, `B2Rules.Resume`, `B3StreamRules.Run`, `B3Checks.Run`, `B3Checks.Resume`, `RouteScoringRules.Run`, `RouteScoringRules.Resume` |
| REG-02 | 旧档、容器、双武器/冷却、仓库与配方 | PASS | 完整明细含其他历史用例，见results.json；`T06RegContainerRuntimeCheck.Run`, `T06RegContainerRuntimeCheck.Final`, `T06RegDualWeaponCheck.Run`, `T06RegWorkbenchCheck.Run`, `B05LegacyMigrationCheck.Run`, `B05V7MigrationCheck.Run`, `B06V8MigrationCheck.Run`, `WGLegacyForestCheck.Run` |
| REG-03 | Boss战斗/奖励/经济/新进程兼容 | PASS | 规则/真实物理受控；不冒称原生Boss战；`B07Rules.Run`, `B07Rules.Resume`, `B07Rules.PendingResume`, `B07Rules.CommittedResume`, `B07Combat.Run`, `B07Economy.Run` |
| REG-04 | 原五策略正常冒险与继续 | PASS | 正常NPC；15个独立Editor进程；`normal-ai.Gather.Normal`, `normal-ai.Gather.Resume`, `normal-ai.Gather.FinalResume`, `normal-ai.Treasure.Normal`, `normal-ai.Treasure.Resume`, `normal-ai.Treasure.FinalResume`, `normal-ai.Bypass.Normal`, `normal-ai.Bypass.Resume`, `normal-ai.Bypass.FinalResume`, `normal-ai.Land.Normal`, `normal-ai.Land.Resume`, `normal-ai.Land.FinalResume`, `normal-ai.Lake.Normal`, `normal-ai.Lake.Resume`, `normal-ai.Lake.FinalResume` |
| BUILD | 非开发Windows64构建 | PASS | BuildOptions.None；警告/源码/构建哈希单列；`WanxiangBuild.ValidateBuild` |
| U16 | 最终Player原生键鼠与标题栏关闭 | NOT_RUN | 无安全独立交互环境；后台关闭不可替代 |
| HUMAN | 独立人工可理解性 | NOT_RUN | 未安排，不用截图/机器人冒充 |
| UNKNOWN | D3D12 UNKNOWN根因 | UNRESOLVED | 无新因果证据，不重复实验或改生命周期 |
| RENDER | 既有Editor青色帧内部原因 | UNRESOLVED | 40%像素阈值只是大面积纯青帧检测；不能证明局部渲染无异常 |

## All实际状态行

{"PASS": 138, "FAIL": 2, "NOT_RUN": 31, "UNRESOLVED": 2}

非预期FAIL：0。标准负探针FAIL单独保留。协调器exit0不等于全部验收通过。

[完整命令/时间/退出码/超时](Evidence/FinalAll/results.json) · [失败历史](FAILURE_HISTORY.md) · [证据索引](Evidence/INDEX.md)
