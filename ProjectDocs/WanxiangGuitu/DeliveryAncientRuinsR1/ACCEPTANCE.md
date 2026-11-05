# 验收清单

PASS 需要对应断言和进程退出证据。历史失败保留在失败历史及原始回执中。测试 Player 使用与纯发行相同的非开发构建选项，并额外包含隔离验收驱动。

| 条目 | Editor | 非开发测试 Player | 证据 |
| --- | --- | --- | --- |
| 五区实际往返、关闭门阻断、开启恢复、密室通道 | PASS | PASS | RewardsEditor1、RewardsPlayer1 |
| 四个探索事件永久身份，隐藏箱普通与特殊产物分开 | PASS | PASS | RewardsEditor1、RewardsPlayer1 |
| 事件发布前回滚、发布后识别、同局重复回调 | PASS | PASS | FaultEditor2、FaultPlayer2 |
| 守护者阶段转换、两种新攻击实际命中与规避 | PASS | PASS | BossEditor2、BossPlayer2 |
| 守护者死亡、常规掉落与首次待领取一起保存 | PASS | PASS | BossEditor2、BossPlayer2 |
| 新进程恢复同一 Run、地面物品、随机流与永久回执 | PASS | PASS | ResumeRewardsEditor2、ResumeRewardsPlayer2、ResumeBossEditor2、ResumeBossPlayer2 |
| 满包、持久化待领取、领取故障回滚和已发布确认 | PASS | PASS | ResumeRewardsEditor2、ResumeRewardsPlayer2、ResumeBossEditor2、ResumeBossPlayer2 |
| 下一局普通箱掉落重生、永久遗镰不补发 | PASS | PASS | ResumeRewardsEditor2、ResumeRewardsPlayer2 |
| 下一局真实再次击败守护者，常规物资与装备重生、永久首奖不补发 | PASS | PASS | ResumeBossEditor2、ResumeBossPlayer2 |
| 真实撤离取消、成功撤离、重复结算和主动放弃 | PASS | PASS | ResumeRewardsEditor2、ResumeRewardsPlayer2、ResumeBossEditor2、ResumeBossPlayer2 |
| 玩家被击杀、死亡结算和重新出征 | PASS | PASS | DeathEditor2、DeathPlayer2 |
| 旧三区在途恢复、保存及退出 | PASS | PASS | LegacyFrontierEditor2、LegacyFrontierPlayer2 |
| 石柱遮挡、剑的有限面向、法杖软锁实际弹体接触 | PASS | PASS | AssistEditor2、AssistPlayer2 |
| 七武器五区矩阵与大厅扩展技能 | PASS | PASS | [实际攻击逐项记录](Evidence/Derived/weapon-matrix.json) |
| 法杖、弓走廊实际实体弹体撞墙 | NOT_RUN | PASS | StaffCorridorPlayer3、BowCorridorPlayer3 |
| 旧五区在途存档恢复与结算 | NOT_RUN | PASS | LegacyFivePlayer2 |
| 实际拆解特殊装备，保存、读取和新局后仍不能重新领取 | PASS | PASS | SalvageEditor4、SalvagePlayer4 |
| 旧版 v1–v8 全量迁移复跑 | NOT_RUN | NOT_RUN | 本批使用 v9，旧报告保留 |
| 纯发行启动与关闭 | 不适用 | PASS | PurePlayer1、assembly-audit-r1.json |
| 原生键鼠、U16、人工观感与最终平衡 | NOT_RUN | NOT_RUN | 需要独立操作者 |
| 构建后 JobTempAlloc 来源、历史 Native 漂移、UI-01 D3D12 UNKNOWN、Editor 青色帧根因 | UNRESOLVED | UNRESOLVED | 前批原始日志、本批构建日志 |

独立 C1 规则 33 条通过。隔离发行构建输入存在既有 Unity 序列化差异，纯包证据绑定实际输入与二进制。仓库产品设置等同性另列，不从构建成功推断。
