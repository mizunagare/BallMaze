# COMBAT-03 复审结论与 RUNLOOP-01 Codex 任务书

## A. 固定 SHA 复审

- 仓库：`mizunagare/BallMaze`
- 开始基线：`85b8badc4e10679c73e59683f4e92c14fdb27b14`
- 最终提交：`4ae4ca8fa8d8d7ff64aaee388bfc653eb58f76e7`
- 已重新读取远端 `main`，完整 SHA 与最终交付一致。

证据：
- [报告](https://github.com/mizunagare/BallMaze/blob/4ae4ca8fa8d8d7ff64aaee388bfc653eb58f76e7/ProjectDocs/WanxiangGuitu/DeliveryCombat03/REPORT.md)
- [验收表](https://github.com/mizunagare/BallMaze/blob/4ae4ca8fa8d8d7ff64aaee388bfc653eb58f76e7/ProjectDocs/WanxiangGuitu/DeliveryCombat03/ACCEPTANCE.md)
- [复跑说明](https://github.com/mizunagare/BallMaze/blob/4ae4ca8fa8d8d7ff64aaee388bfc653eb58f76e7/ProjectDocs/WanxiangGuitu/DeliveryCombat03/TESTING.md)
- [武器数据](https://github.com/mizunagare/BallMaze/blob/4ae4ca8fa8d8d7ff64aaee388bfc653eb58f76e7/ProjectDocs/WanxiangGuitu/DeliveryCombat03/WEAPON_DATA.md)
- [证据索引](https://github.com/mizunagare/BallMaze/blob/4ae4ca8fa8d8d7ff64aaee388bfc653eb58f76e7/ProjectDocs/WanxiangGuitu/DeliveryCombat03/Evidence/INDEX.md)

### 复审结论

**COMBAT-03 的四武器命中/反馈一致性在交付方证据范围内有条件接受；不能宣称武器平衡、玩家手感或整批所有验收项通过。**

交付方验收表为 `16 PASS / 5 FAIL / 4 NOT_RUN / 5 UNRESOLVED`。5 个 FAIL 包括历史 FAIL、修复前预期负例、首轮工具期限、PowerShell 别名冲突和后置证据复制竞态；不是 5 个新产品缺陷，但必须保留，不能把整批改成全绿。

接受范围：
- 法杖普攻保留直击，不冒称普通攻击具有 AoE；说明补充飞行时间和无爆炸伤害。
- 法杖技能主爆炸、品质半径、侧球分支保留；每弹对每目标按既定规则命中，独立侧球可分别命中。
- 弓保留独立箭、多箭扇形、品质分支与各箭范围伤害；实际方向/箭数与说明对齐。
- 远程释放使用 Cast 反馈，不再误显示近战 Slash 弧光。
- 攻击 ID 与弹体序号只在运行时使用，不写入 v9；每箭有独立 consumed 与目标集合。
- 范围反馈随有效时间推进，UI-only 暂停冻结，恢复后继续；角色死亡/卸载时清理。
- 固定 Run/layout seed 418、revision 5、stream 1 的 96 对样本，命中与伤害差异为 0。
- 发行构建 0 错误、94 警告；用户文件与历史证据哈希不变，产品未改经济、掉落、随机流、地图或 v9 合同。

限制：
- 每种武器/体型短战 n=2，只能支持有限方向判断，不能证明平衡。
- 网格命中/空挥比例是人为选点覆盖率，不是玩家命中率。
- 本次核对报告、数据、失败历史和证据索引，没有在 Windows 上独立运行 Unity；运行结果属于交付方证据。
- 最终发行 Player 实际战斗操作、原生 U16、独立人工试玩、最终平衡和完整性能预算仍 `NOT_RUN`。
- D3D12 UNKNOWN、Editor 青色帧、Editor.Search、JobTempAlloc、旧 C15 关闭超时根因继续 `UNRESOLVED`。
- 构建副本有六项设置资产与用户主工程不逐字节一致，已记录；不能声称所有运行输入都与纯 Git main 字节级一致。

## B. 下一批 RUNLOOP-01：搜打撤核心循环与风险收益审计

开始基线：`4ae4ca8fa8d8d7ff64aaee388bfc653eb58f76e7`。

### 目标
人工试玩暂时无法进行时，继续开发是可行的。建议先审计并完善搜打撤主循环的状态一致性与信息反馈，而不是盲目增加地图或继续调武器伤害。核心体验是：营地准备 → 出征 → 探索/战斗/采集 → 判断继续或撤离 → 结算 → 仓库/制造 → 再次出征。

### 开工条件与保护
- 开工先核对远端 main 完整 SHA；若已变化，停止并报告，不 reset、不覆盖。
- 审计 `AdventureFlow`、`CampRuntime`、`PlayerInventory`、`AdventureLoadout`、`CombatSession`、`CombatEnemy`、出口/撤离、`AdventureRecipes`、HUD/提示和 v9 存档路径。
- 不升级 Unity/URP/依赖，不新增 CI，不改 v9 合同、随机流、地图布局、掉落概率或经济数值。
- 不改用户场景、ProjectSettings、真实存档或未提交修改；使用隔离工程与合成存档。
- 保留 COMBAT-02 原始 FAIL、四个历史 exit 1、R1 修复前失败与旧 aggregate，不回写历史。

### RUN01-01：状态流审计
绘制从标题到后继 Run 的实际状态图：
标题/继续 → 出征准备 → 森林探索 → 战斗/采集 → 携带战利品 → 出口条件未满足/可用 → 撤离请求 → Pending → Committed/失败 → 营地仓库 → 制造 → 下一次出征。

每个状态记录目标、可用行动、进入/退出条件、业务入口、随身物资/永久仓库/待结算/地面掉落边界、UI反馈、退出/恢复行为、现有测试和缺口。只按源码填表；已有能力标“已有实现”，不得重复开发。

### RUN01-02：风险收益审计
使用固定合成输入检查：
- 携带战利品、生命状态、路线、出口条件和撤离机会是否构成可理解的取舍。
- 出口位置、修复/付费条件、剩余资源和路线是否清楚。
- 继续探索是否存在现有机制支持的潜在收益/风险变化。
- 背包空间、药水和装备是否影响决策（不存在的机制标明“当前无此机制”）。
- 撤离成功、失败、Pending、Committed 的反馈是否明确且不重复结算。

不得为审计新增货币、掉落、装备属性或地图。没有现有机制支撑的想法只列为独立设计提案，等待授权。

### RUN01-03：允许的最小修复
只有存在可复现证据时，才修复：
- UI/提示与真实业务状态不一致；
- 撤离/结算存在死路、重复奖励或物资丢失；
- 随身物资、永久仓库、待结算奖励归属混淆；
- 中断/恢复导致已确定世界状态或来源账不一致；
- 已实现的目标/出口条件无法从界面获知。

本批不实现大型任务系统、随机事件框架、永久成长树或新地图。超出范围的缺口只报告，不顺带实现。

### RUN01-04：验收矩阵
至少覆盖：
1. 标题进入并开始 Run。
2. 采集后核对随身物资和来源账。
3. 出口条件不满足时，提示与真实拒绝原因一致。
4. 满足条件后合法撤离。
5. Pending/Committed 保存、退出与新进程恢复。
6. 同一结算不重复发奖/扣费。
7. 仓库只接收合法结算物资，不混入地面未拾取物、未提交 RunLoot 或未领取奖励。
8. 制造使用已审核的背包+营地仓库原子支付规则。
9. 再次出征恢复正确 Profile/Run/区域/seed/layout/revision/随机流。
10. 失败、中断、坏档、保存失败和重复请求状态正确。
11. 正常 AI 三阶段闭环；Editor、隔离验收 Player、正式发行 Player 分层记录。
12. 受影响代码非开发构建，完整记录所有错误和警告。

保留失败、超时、未知终态和离群值，不删除样本或放宽断言。

### 交付与通过条件
提交 `RUNLOOP_STATE_MAP.md`、`REPORT.md`、`ACCEPTANCE.md`、`TESTING.md`、`Evidence/INDEX.md`、状态转换/来源账矩阵、固定合成输入、前后对照、失败历史和哈希。

通过只代表核心业务循环与信息反馈在受控运行层面一致，不代表人工体验或平衡通过。原生 U16、独立人工试玩、最终发行 Player 原生操作和完整性能预算继续单独标记。

只增量更新 `DEVELOPMENT_PLAN.md`，不覆盖旧历史。推送后重新读取远端 main 核对完整 SHA，随后暂停等待独立复审。

### 给 Codex 的执行指令
读取本文件，核对远端 main 完整 SHA，先审计现有搜打撤状态流和风险收益信息，不要直接新增系统。只修复有复现证据的循环断点、结算/恢复不一致或反馈误导。

不改经济、掉落、随机流、地图、v9 合同；不升级依赖、不新增 CI、不覆盖用户文件和真实存档。保留所有历史失败和未执行项。完成后提交状态图、报告、验收表、复跑说明与证据索引，推送并核对远端完整 SHA，随后暂停等待复审。
