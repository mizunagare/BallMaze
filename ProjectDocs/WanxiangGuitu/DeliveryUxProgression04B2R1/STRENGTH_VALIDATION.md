# Strength 真实 Player 验证

独立Run分别使用Strength=0与Strength=3。测试初始化通过现有 `HeroProgression.RestoreProgress`恢复等级数组，绝不直接写最终AttackPower；这验证真实属性计算链，不声称执行了技能升级点击流程。

计算：Strength贡献=`Rank(Strength)×5`；装备贡献=`D-24 Active装备逐件贡献 + 胸挂加成 + 背包加成`；最终AP=`hero.attackDamage + 装备贡献 + Strength贡献`；普攻=`AP × (主武器为长枪 ? 1.25 : 1)`。

必须记录真实rank、×5结果、每件装备原始字段、容器定义、baseDamage、装备贡献、AP、BasicPower及B2 PreviewReplacement before/after。预览应保留同一Strength贡献；用离线float32预言机复算，不直接信任driver PASS。

角色界面验证数值与实际rank文本；关闭背包后保存实际HUD截图，并人工比对HUD攻击数字，不以源码字符串或“普攻”标签存在代替渲染验证。

## 最终A03结果

先通过现有OpenPreparation/Depart进入真实森林ActiveRun，再准备样本并恢复rank。出征内部Restart清理技能发生在恢复rank之前；不更改Flow状态字段、挑战逻辑或正式存档。

| Strength实际rank | ×5 | 装备贡献 | base | 最终AP / 普攻 | Main预览AP |
|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 8 | 25 | 33 | 157 |
| 3 | 15 | 8 | 25 | 48 | 172 |

两者预览增量均124，Strength差15同时体现在实时AP和预览后AP。默认uGUI HUD没有数字攻击字段，保留实际HUD截图但不伪称其显示AP；数值HUD来自显式切换产品既有IMGUI fallback，在真实ActiveRun由CombatSession.OnGUI自然绘制。人工确认攻击33/48，详见[记录](<I:/unity/WanxiangGuitu/Evidence/Runs04B2R1/SESSION-20261116-1115/manual-A03-review.json>)。A01/A02营地截图不足原样保留。

最终结果见 [验收矩阵](<PLAYER_RUN_MATRIX.csv>) 和 [证据索引](<EVIDENCE/INDEX.json>)。
