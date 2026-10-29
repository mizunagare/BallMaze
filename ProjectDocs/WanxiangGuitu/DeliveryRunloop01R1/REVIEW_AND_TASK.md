# RUNLOOP-01 固定 SHA 复审与 RUNLOOP-01-R1 任务书

## 1. 固定版本与本次结论

- 仓库：`mizunagare/BallMaze`
- 开始提交：`4ae4ca8fa8d8d7ff64aaee388bfc653eb58f76e7`
- 审核提交：`d8a6dbd9f205bae96ff8a55e1f34eb6fa5cf7179`
- 本次读取远端 `main` 时，HEAD 与审核提交一致。
- 审核结论：**保留核心修复和已有成果；需要定向返工两项 P2，本轮不批准扩大为“结算故障恢复已闭环”。**
- 下一批：`RUNLOOP-01-R1`。仅修复本任务书列出的两条分支，不新增游戏系统、不要求人工试玩先完成。

本次结论不是根据“15 PASS / 7 FAIL”机械判定。七个 FAIL 包含历史、修复前负例和工具失败，这些记录应保留，但不能等同于七个当前产品缺陷。要求返工的依据，是下面两项可定位到具体源码的异常处理缺口。

## 2. 已完成的审核及证据边界

实际核查：远端 HEAD、两提交比较、三个变更产品文件及相关验证器、故障测试源、报告、验收表、复跑说明、证据索引、修复前后 fault-result。

审核侧另外执行了两个源码分支的 Python 离线转写模型，共 11 个条件：7 个符合合同，4 个反例，归属 2 个问题。**这不是 11 次游戏运行，不是 Unity/C# 重跑，也没有运行 JsonUtility、完整 v9 校验器或 Windows 文件发布逻辑。** 模型仅验证所审查的布尔条件和界面分支，不替代下面要求的 Unity 故障注入。

本次未执行：Unity/Windows Player 构建、五进程循环、正常 AI、原生输入、独立人工体验及性能测试。交付方提供的这些运行记录按原证据层级保留，不表述为审核方重跑。

### 2.1 本轮主修复值得保留

修复前故障回执为磁盘 `Committed/revision 4`、内存 `Pending/revision 3`；修复后同类故障的回执为内存/磁盘均 `Committed/revision 4`。它们来自不同合成 Run，不是同一 Run 的跨版本继续，但支持原故障路径已经取得修复证据。

`CommitSettlement()` 的成功核对分支检查下一修订号、无活动 Run、结算身份、Committed 状态、未确认标志、完整 Profile 与 Settlement。结果无法确认时阻止提交和保存的方向正确。营地、制造、满仓待领取及正常 AI 成果不要求回滚。

## 3. RL01-RV-01（P2）：允许重试的旧 Pending 核验不完整

### 位置

`Assets/CombatPrototype/AdventureFlow.cs`，`CommitSettlement()`，特别是第 178–186 行左右的失败核对。

成功分支比较完整 Committed 记录；允许重试分支目前主要比较：

- revision 与旧修订相同；
- 有 ActiveRun、Run ID 相同；
- 有 Settlement、状态是 Pending、Settlement ID 相同；
- Profile 与旧 Profile 相同。

它没有比较旧 Pending 的完整 Settlement，也没有证明磁盘 ActiveRun 与原活动 Run 的受保护内容一致。源码注释称“exact prior Pending receipt”，实际检查不足以支持这个结论。

### 反例与影响

保持上述字段相同，仅改变磁盘 `settlement.plan`、`outcome`，或者活动 Run 的检查点内容，当前表达式仍会给出 `unknown=false`，并允许重试。

存档自身通过校验，与“这是这次提交之前的同一份记录”是两个不同问题。现有 `AdventureValidation.Validate` 检查结构、身份关联和若干来源规则，不负责将这份磁盘记录与本次内存的旧记录逐项比较。

这会使冲突记录被误判为“可以安全重试”，而不是要求完整读取。尚未证明真实玩家已经遇到此冲突或损失物品；该结论为源码分支问题及离线模型反例，完整有效 v9 夹具需要在 R1 中验证。

### 修复要求

维持明确的三类结果：

1. **本次预期的 Committed 已发布**：只确认发布结果，不重复应用奖励。
2. **确切的旧 Pending 仍在**：允许原请求安全重试。
3. **其他、冲突、缺失、不可读**：进入结果待核对状态，禁止覆盖/重复提交，保留完整读取入口。

第二类必须绑定可信的发布前状态。可以采用完整语义快照比较，或绑定可信发布前封装指纹；不要只加一两个 ID 比较后继续称为完整核验。需要覆盖完整结算计划、结果类型、来源/数量等结算字段，以及相关活动 Run/检查点/来源状态。

注意 GroundLoot 分页、读回展开、运行时字段、null/空字符串等表示差异，不能误把语义相等判冲突，也不能为了“兼容”忽略真正的收益差异。选择最小且可解释的比较方法，不新建通用事务框架，不增加 v9 字段。

冲突用例只允许在隔离的负例夹具中构造：优先从真实业务生成两个各自合法的快照，再形成冲突对照；人工修改负例时必须通过现有 v9 验证并明确标注。不得修改正例最终存档来伪造成功，也不得操作真实玩家档。

## 4. RL01-RV-02（P2）：完整读取失败后，重试读取入口可能丢失

### 位置

- `AdventureFlow.Restore()`：进入方法时立即 `SettlementNeedsRead=false`，发生在 `RestoreWorld/ApplyCamp` 完成之前。
- `CombatSaveSystem.LoadProgress()`：后续恢复抛错时，catch 设置 `blocked=true` 并调用 `BlockRecovery/MigrationFailed`。
- `AdventureFlow.OnGUI()`：`HasResult` 分支优先于通用 Error 恢复面板。
- `DrawSettlement()`：只有 `SettlementNeedsRead` 为 true 才显示“读取完整存档核对”；否则显示提交或返回营地。

### 可复现的路径

1. 复用 `RunloopUncertain`：提交后主档不可读，形成待核对状态。
2. 放回原已发布 Committed 的精确字节，不修改业务内容。
3. 调用正常 `LoadProgress`；通过已有 `AdventureFlow.ValidationHook` 在 `before-camp-load` **仅抛一次异常**。
4. 文件已经读出，Restore 已清除标记并放入未 acknowledged 的 Committed；随后营地装载失败。
5. `blocked=true`，但 `SettlementNeedsRead=false` 且 `HasResult=true`；界面仍走结算页，通用读取错误面板被遮住。
6. 结算主操作显示返回营地/重试回营，不是完整读取。即使移除临时故障，确认操作也不能自行清除存档系统的 blocked 状态。

这不是已证明的物品损失；风险是恢复过程再次失败后，用户缺少当前页面上的安全恢复路径。退出重启或测试代码直接调用 LoadProgress，不应作为界面正确性的替代证据。

### 修复要求

- 读取开始不代表读取成功。只有完整恢复、状态重建和必要收尾成功后，才能解除待核对状态。
- 读取文件成功但运行时恢复失败，应保留/恢复一个能够阻止写入且可被 UI 识别的恢复状态。
- 即便 `HasResult=true`，存档恢复被阻止时仍需显示正常可用的“重试读取完整存档”；不得诱导用户继续提交或确认。
- 修复不得因为只移动一行赋值而让旧版迁移或内部正常恢复自锁。明确区分恢复中的内部操作与恢复成功后的业务可写状态。
- 故障解除后，经同一界面入口完成第二次读取，恢复正确阶段及身份，不重复奖励、不意外新增修订。
- 不通过关闭 blocked、吞异常、隐藏错误、允许 F5 强制覆盖或重开新档绕过问题。

## 5. 本轮实施范围与顺序

### 5.1 开工

核对远端与工作区。从本审核 SHA 起步；若 HEAD 已前进，先记录差异及影响，不 reset、不覆盖用户改动、不把旧审核套到新产品代码。

保护用户场景、ProjectSettings、Recovery、未提交修改、真实存档与历史证据。复用短路径隔离工程、明确所有权和合成存档。不得复用仍被 Editor 占用的隔离目录，不抢桌面、不强杀用户或历史进程。

### 5.2 实施

先在隔离环境补两个修复前负例；再修现有结算核对和恢复/UI 状态。允许修改这两条路径所需的最小产品代码与测试接线，**本任务不是只写方案，负例确认后可以直接实施，不必再次等待人工试玩或中间审批**。

如果运行实证否定某项源码分析，应交付原始结果和具体原因，不为迎合任务书强行修改。不扩展为所有存档阶段、所有回调组合、全部旧版本迁移的通用重构。

### 5.3 明确不做

不新增地图、武器、永久成长、任务/事件系统；不改伤害、掉落、成本、随机流、地图布局、结算收益规则或 v9 格式；不升级 Unity/URP/依赖，不新增 CI。

terminal/ack 全排列仍可保留为独立未穷尽边界；本批只测试与本次两个发现直接相关的路径，不再安排一轮泛化“完善测量能力”。

## 6. 有限验收矩阵

| ID | 场景 | 必须观察的结果 |
|---|---|---|
| T01 | 原发布后回调异常，磁盘是本次完整 Committed | 正确确认；Profile/revision/回执一致；无重复收益 |
| T02 | 发布前失败，磁盘确为同一旧 Pending | 可重试，原字节与数量保留，成功只提交一次 |
| T03 | 同 revision/ID/Profile，但 Pending 计划不同 | 现有 v9 校验先通过；核对判冲突，禁止重提及保存 |
| T04 | 同 ID 的结果类型/来源数量/受保护检查点不同 | 各负例明确区别；不能只匹配 ID 放行 |
| T05 | 不同 revision、Profile 或结算身份 | 保持待核对，不覆盖冲突数据 |
| T06 | 主档缺失/损坏 | 旧 Missing/Corrupt 保护继续成立 |
| T07 | 完整读取在解析前失败 | 恢复状态、读取入口仍在，不能写入 |
| T08 | 读取 Committed 后 before-camp-load 抛一次异常 | 保存仍受阻；结算页仍有完整读取入口；不能只显示确认 |
| T09 | 移除 T08 故障，经同一 UI 操作再读取 | 成功恢复，清除临时门禁，无额外奖励或修订 |
| T10 | 读取 Pending 后运行时恢复失败 | 仍提供读取；不能继续提交部分恢复状态；使用最小受控故障，不破坏真实档 |
| T11 | 待核对/恢复失败时自动保存、F5、失焦、退出保存 | 不只检查 false；核对主备档、修订、分页引用和物品数量未被错误覆盖 |
| T12 | 完整恢复后正常继续与重复请求 | Pending 能正常提交，Committed 不重发；后继 Run/来源账恢复一致 |

表中包含不同子例，实际断言数量按运行结果填写，不以凑到某个数量作为目标。

直接重跑现有 RunloopFault、RunloopUncertain、五阶段循环及受影响 UI/存档回归。产品改动后做非开发构建，保存完整警告清单。正常 AI 仅按实际影响范围运行；不无差别重跑 100 种子、全部性能窗口或全部武器配对。

Editor、隔离验收 Player、正式发行 Player、物理输入、人工体验分别记录。受控按钮操作可以验证恢复入口，但不能称为原生输入或人工通过。

## 7. 交付和状态口径

推荐目录：`ProjectDocs/WanxiangGuitu/DeliveryRunloop01R1/`。

提交报告、验收表、复跑说明、证据索引、两个修复前负例、修复后独立结果、故障前后存档指纹与账目、实际执行的源码、进程回执、构建消息及保护哈希。

状态区分：

- `attempts`：每次运行原结果，历史 FAIL 永不覆写；
- `findings`：缺陷是 OPEN、FIXED 或已复审关闭；
- `current_acceptance`：当前代码在限定范围的验收结论；
- `deferred`：原生 UI、人工试玩、性能预算及未穷尽组合。

不能因保留一个已修复的负例就机械宣称当前版本整体 FAIL，也不能因新样本成功就把旧失败或尚未闭环的问题变绿。此次请求返工的原因是 RL01-RV-01/02，而不是报告中保留的七个历史 FAIL。

旧 D3D12 UNKNOWN、Editor 青色帧、Search、JobTempAlloc、C15 等继续原状态；新 R1 不顺带关闭它们。不存在重新等待用户能人工操作才可开始的前提。

推送后重新读取远端完整 SHA，返回：开始/产品与测试冻结/最终提交、两项发现的处理、各层测试、未执行项、构建结果、用户保护及报告链接。完成后暂停等固定 SHA 复审。

## 8. 给 Codex 的执行指令

```text
读取本任务书及配套分支模型。

本轮执行 RUNLOOP-01-R1，保留原核心修复，仅处理两个问题：
RL01-RV-01：旧 Pending 的冲突核验不完整；
RL01-RV-02：完整读取中途失败后，恢复标记及读取入口可能丢失。

先在隔离 Unity 中建立真实修复前负例，再做最小产品修复和有限矩阵。
模型只是源码分支推演，不是 Unity 结果；必须验证合法 v9 负例和真实 UI/业务路径。
不重写存档系统，不新增 v9 字段，不扩大到全部回调组合，不等待人工试玩。
不改用户文件、经济、武器、地图或依赖，不新增 CI。
保留旧证据及所有失败，提交推送并核对远端完整 SHA，随后暂停复审。
```

## 9. 固定源码与证据链接

- [RUNLOOP-01 报告](https://github.com/mizunagare/BallMaze/blob/d8a6dbd9f205bae96ff8a55e1f34eb6fa5cf7179/ProjectDocs/WanxiangGuitu/DeliveryRunloop01/REPORT.md)
- [验收表](https://github.com/mizunagare/BallMaze/blob/d8a6dbd9f205bae96ff8a55e1f34eb6fa5cf7179/ProjectDocs/WanxiangGuitu/DeliveryRunloop01/ACCEPTANCE.md)
- [证据索引](https://github.com/mizunagare/BallMaze/blob/d8a6dbd9f205bae96ff8a55e1f34eb6fa5cf7179/ProjectDocs/WanxiangGuitu/DeliveryRunloop01/Evidence/INDEX.md)
- [CommitSettlement 核对与重试](https://github.com/mizunagare/BallMaze/blob/d8a6dbd9f205bae96ff8a55e1f34eb6fa5cf7179/Assets/CombatPrototype/AdventureFlow.cs#L165-L188)
- [Restore 状态重建](https://github.com/mizunagare/BallMaze/blob/d8a6dbd9f205bae96ff8a55e1f34eb6fa5cf7179/Assets/CombatPrototype/AdventureFlow.cs#L90-L111)
- [结算 UI 操作路由](https://github.com/mizunagare/BallMaze/blob/d8a6dbd9f205bae96ff8a55e1f34eb6fa5cf7179/Assets/CombatPrototype/AdventureFlow.UI.cs)
- [保存与读取错误处理](https://github.com/mizunagare/BallMaze/blob/d8a6dbd9f205bae96ff8a55e1f34eb6fa5cf7179/Assets/CombatPrototype/CombatSaveSystem.cs)
- [v9 冒险数据验证](https://github.com/mizunagare/BallMaze/blob/d8a6dbd9f205bae96ff8a55e1f34eb6fa5cf7179/Assets/CombatPrototype/AdventureValidation.cs)
- [现有 Missing/Corrupt 故障夹具](https://github.com/mizunagare/BallMaze/blob/d8a6dbd9f205bae96ff8a55e1f34eb6fa5cf7179/ProjectDocs/WanxiangGuitu/DeliveryRunloop01/Tests/RunloopUncertain.cs.txt)
- [修复前回执](https://github.com/mizunagare/BallMaze/blob/d8a6dbd9f205bae96ff8a55e1f34eb6fa5cf7179/ProjectDocs/WanxiangGuitu/DeliveryRunloop01/Evidence/Before/fault-result.json)
- [修复后回执](https://github.com/mizunagare/BallMaze/blob/d8a6dbd9f205bae96ff8a55e1f34eb6fa5cf7179/ProjectDocs/WanxiangGuitu/DeliveryRunloop01/Evidence/After/fault-result.json)
