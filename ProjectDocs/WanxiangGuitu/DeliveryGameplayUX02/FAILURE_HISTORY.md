# 失败历史（不被后续PASS覆盖）

- 开工审计第一次PowerShell命令使用了不支持的花括号路径列表，解析exit1，未执行任何修改；改用明确文件路径。
- 初次prepare把ArtifactsRoot设为WorkProject父目录，复制后New-Item发现父目录已存在而exit1。GU02-1030-A部分副本保留；GU02-1030-B使用独立Prepare兄弟目录重新准备。无用户文件覆盖。
- 只读搜索最初将内嵌AdventureProjectile误当独立文件、PowerShell的路径通配未由rg扩展，均保留为工具查找失败；实际类在AdventureCombat.cs中，未推断不存在产品能力。
- Before首轮夹具没有关闭StartFresh营地面板，Time.time停在0.02，表现Paused，公开攻击未接受；该轮无效，不能作为小数数字或禁用反馈的产品负例。由既有240秒Editor适配器期限自行exit1，不强杀；日志、事件及输入源码保留。修正只在夹具显式关闭库存/HUD/保存面板并恢复模拟时钟。
- 原始日志若出现UnityEditor.Search/JobTempAlloc/UNKNOWN，单列UNRESOLVED，进程退出码不代表干净运行。旧批次所有失败、U16及人工NOT_RUN保持原状。

FixtureState进一步定位：夹具在Play第1帧、CombatSaveSystem.Start尚未完成时自行Initialize/Depart，下一帧正式Start重新进入营地（scale=0、inventory=True、AtCamp=True）。这不是产品战斗表现缺陷。适配器改为等待Saves.IsInitialized且至少6个实际帧，保留启动与断言标准；之前两个失败/退出不算产品负例。Before2经精确身份/非激活测试桌面的既有editor-close有界正常关闭，非强杀，但无业务完成回执，不能按exit0判PASS。

Before3已取得3个真实表现负例（−0、禁用后新数字/特效、禁用后拖尾），另8项命中失败确认为夹具误关目标唯一Collider。Before4保持真实CharacterController开启，不改HP、攻击几何或断言，重新独立运行；增加实际普通/远程/精英/普通Boss/玩家承伤与死亡反馈覆盖。所有原失败原文保留。

Before4新增角色覆盖编译失败CS0136（夹具局部hp同名），没有进入业务，完整原输入/日志保留。由精确PID/桌面验证的独立线程只点击该自建编译失败Editor的Safe Mode Quit按钮，未激活桌面、未强杀。仅改夹具变量名，后续采用带图形batch Editor防止编译错误停在交互提示，不改变产品或断言。

Before5使用batch图形Editor但未创建GameView，未形成实际运行帧/业务回执，等待既有有界期限自行退出；精确Editor主窗口关闭工具因batch无匹配主窗口返回NOT_RUN，未回退为强杀或激活桌面。后续复用现有UI01Before.Size创建GameView、Repaint/QueuePlayerLoop；使用非batch独立桌面，同输入/断言，不改产品暂停合同。

AfterTrace用既有AdventureProjectile.Observed定位两项法杖近距失败：原始1.5m、偏置相机下Solve返回CAMERA_SURFACE_BEHIND_MUZZLE，真实弹体沿安全方向飞行未接触目标。没有Damage，因此无Hit数字；并非新增反馈回归。原断言/日志不改写。后续明确新增6m远程“命中对照”样本（剑/枪仍1.5m），输入条件另列，不把新成功宣称修复近距瞄准；不修改CombatAim、发射点或命中逻辑。增加不足0.01伤害文案及森林双Boss真实Damage/死亡表现用例。所有旧近距失败保留。

有效复测：Before7 111PASS/4FAIL→After2 115PASS/0FAIL（同115项）。AfterExpanded、MissingGlow、非开发Runtime各119PASS/0FAIL，均为独立执行，未覆盖旧记录。4个修复前FAIL属于真实小数显示和禁用反馈生命周期两类根因。所有早期夹具/编译/无业务回执结果仍为失败或NOT_RUN，不纳入成功。

只读身份探测曾误把payload.game普通标识当JSON，ConvertFrom-Json报Unexpected character F；未写存档。后续从真实profile/activeRun结构读出身份，原封装不变（ToolFailures/metadata-probe-error.txt）。
