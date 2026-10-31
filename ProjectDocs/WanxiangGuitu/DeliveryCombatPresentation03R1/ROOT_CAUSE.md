# 根因与授权边界

## 已修复：语义回执误分类

旧 `Invoke-Runtime.ps1` 对 `rows | Where-Object status -ne PASS` 非空直接记 FAIL，因此 291 PASS + 2 UNRESOLVED 被归为 semantic-receipt FAIL。原 Player exit 0 不与这一脚本错误矛盾。[旧谓词复现](Evidence/before-classification.json)、[原脚本](Evidence/Invoke-Runtime.ps1.before.txt)。

新 [Receipt.py](../DeliveryCombatPresentation03/Receipt.py)分别输出进程、回执完整性、断言和整体状态，校验原始回执，绝不改写它。PASS+UNRESOLVED → 断言 UNRESOLVED / 整体 BLOCKED / 分类退出码 2。真正 FAIL 优先级最高；证据缺失/损坏/未运行 → INCOMPLETE / 3；全通过 → PASS / 0。Player 原始退出码与分类工具退出码分别保存。

## 已修复：宽泛整行删除

旧审计删除含 MeleeTrace 的整行，允许该行额外玩法语句或重复调用被一起忽略。[旧审计原文](Evidence/Audit-Locked.py.before.txt)、[旧审计放行负例输出](Evidence/SelfTestFinal2/old-audit-bypass.txt)。负例是文档目录内的合成源码文本，不曾写入产品。

新审计从冻结旧源码构造唯一精确期望：3 处整行替换、1 处固定位置插入；全部正文比较，不剥离任意字符串。允许差异的函数、行号、全文、数量见 [严格审计回执](Evidence/locked-contract-r1-attempt2.json)。

## 法杖：近距几何原因已定位，产品问题仍 UNRESOLVED / 等待授权

历史 `w2-s0-near` / `w2-s1-near` 未改：原记录 hpLoss=0 / CAMERA_SURFACE_BEHIND_MUZZLE。[原断言](../DeliveryCombatPresentation03/Evidence/Final2/presentation.json)。

[本轮原始三维观测](Evidence/EditorDiagnosis/aim-diagnosis.jsonl.gz)、[实际 Spawn/Flight/Damage](Evidence/EditorDiagnosis/events.jsonl.gz)、[只读分析](Evidence/aim-analysis.json)显示：

| 项目 | 普攻 | 技能 |
|---|---|---|
| 目标 | w2-s0-near | w2-s1-near |
| 实际攻击 ID / shot | 11 / 1 | 14 / 1 |
| 枪口 (x,y,z) | (299.57474,20.64976,300.91852) | (299.58670,20.64341,300.88058) |
| 表面相对 origin 沿相机方向投影 | −0.272345 m | −0.239442 m |
| 速度 / 初始寿命 | 16 / 2.5 s | 14 / 2.5 s |
| 观测到的 flight 事件 | 93 | 90 |
| 目标 Damage | 无 | 无 |

相机位置 `(305,24,295)`，中心射线起点约 `(304.97134,23.98283,295.03717)`；方向约 `(-0.572894,-0.343419,0.744215)`。唯一合法 ray hit 是目标本身，表面约 `(300.19284,21.11838,301.24463)`。目标 Collider 启用、非 Trigger、bounds `(0.8,2,0.8)`；origin 等于杖首实际枪口，barrelBlocked=false，未发生枪口到锚点修正。

[CombatAim.Solve](../../../Assets/CombatPrototype/CombatAim.cs)在 `Dot(intentPoint-origin,cameraDirection)<=.001` 时触发防倒射保护，将 direction 设为 cameraDirection，并把 intentPoint 改为远方。侧置相机的这一投影不能单独代表“朝目标是否会向玩家身后发射”；此样本中平行射线偏离目标，完整距离预测 hasContact=false，实际观测窗口也无碰撞/伤害。valid=true 只表示有限方向和坐标，不等于能命中目标。

这是此固定夹具的确定性解释，不能扩大为全部近距、正式森林视角或人工体验结论。原矩阵只观察约 1 s，之后切换夹具清理弹体；2.5 s 是实例真实初始寿命，不冒称已观察完整 2.5 s 飞行。相机碰撞/遮挡审计在该样本无其他合法遮挡；没有关闭目标 Collider、移动目标、改距离或放宽预期。

### 等待授权的提案（未实现）

仅考虑 CombatAim 中“相机命中点 → 实际枪口”方向的防倒射判定；不移动枪口、不穿墙、不自动选目标。先定义 hero 前半空间/枪口与意图点的几何合同，再决定是否允许合法近距汇聚；锚点→枪口 sweep、初始 overlap 和半径 .16 的实际扫掠继续是唯一遮挡依据。

风险：可能改变近距发射方向、墙边/背后目标处理及多箭扇面，不能作为纯表现修复混入。授权后须以同种子/原目标/原距离/原相机配对普攻与技能，覆盖四武器、低目标、墙边、枪口内嵌、相机与身体之间障碍、背后目标、暂停/死亡/恢复；逐项比对真实发射坐标、方向、碰撞、Damage 唯一性及历史 24 组发射记录。禁止通过旧失败改成 PASS 完成。

## 仍开放

Editor 新日志仍出现 SearchDatabase 内部 ArgumentOutOfRangeException；[Editor 原日志](Evidence/Editor/Unity.log.gz)保留。不能归因为产品，也不能以进程 0 关闭它。UNKNOWN/C15/青色帧/JobTempAlloc 历史根因不变；本轮不做无新线索的关闭实验。
