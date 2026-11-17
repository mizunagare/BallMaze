# 三Active装备累加精度边界（静态补充）

## 结果

在1125个有序三Active组合（5品质主剑 × 15种盘内候选 × 15种盘内候选）中，找到**34个可布局的数学模型差异**。这仅是未覆盖的**累加精度/舍入风险**，不是系数、叠加规则改变，也不是历史Player运行差异已证。

本附件限定/澄清[黄金报告](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/golden/GOLDEN_REVIEW.md>)关于旧LINQ double累加的表述：**历史Player所用Mono Enumerable.Sum(float)的实际IL未由本次现有二进制确认，double累加是假设**。仅当该假设成立且新循环按逐步float32执行时，以下边界成立；若旧Mono同样逐步float32累加则该反例不构成新旧差异。未运行Player、未构建或加载产品程序集。

## 最小示例：3个Active，1 ULP差异

按items顺序依次为主武器、盘内护臂1、盘内护臂2，三者ID互异：

| 装备 | 品质 | Power × 因子 | float32 Attack | 状态/布局 |
|---|---|---|---:|---|
| Sword | White | 8 × 1 | 8 | InBag且Main；非board/worn/overflow |
| Arms | Green | 19 × .35f | 6.650000095367432 | board，(0,0)，1×2 |
| Arms | White | 8 × .35f | 2.799999952316284 | board，(1,0)，1×2 |

- double累加后一次float32：**17.450000762939453，uint32=1099667866**。
- 每项加法后float32：**17.44999885559082，uint32=1099667865**。
- 差异=**1 ULP**，逐步结果减一次结果=-0.0000019073486328125。
- 加基础25后，模型AP分别42.45000076293945与42.44999694824219；历史三位小数文本可能均显示42.45，因此低精度文本不能排除该边界。

## 输入合法性与可布局性

- 数值来自现有[五品质资产](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/golden/GOLDEN_REVIEW.json>)所记录的power与[护臂资产](<Assets/CombatPrototype/Resources/ItemData/arms.asset#L21-L27>) factor=.35、尺寸1×2、occupiedCells=[]、可旋转；不是捏造savedAttack常数。DataRevision=1按[FreezeNewStats](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/golden/old_HEAD_AdventureItems.cs.txt#L52>)冻结。
- [标准胸挂](<Assets/CombatPrototype/Resources/ContainerData/rig_standard.asset#L20-L25>)为8×6、无阻塞格、attackBonus=0。两护臂共占(0,0)/(0,1)/(1,0)/(1,1)，完全在界内且不重叠。主剑1×3可在空背包中，主武器不占盘格。
- [旧CanPlace](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/golden/old_HEAD_AdventureLoadout.cs.txt#L93-L100>)禁止容器与Carried武器入盘，但未限制同类型护臂仅一件；此例护臂不是容器或Carried，主剑仍InBag，因此静态放置门禁不排除此布局。
- 这里证明“合法数据/布局可构造”，**不宣称UI实际操作已走通**。

## 对21行原矩阵的影响

原矩阵最多2个非零Active项，无法覆盖此类3项累加舍入边界；原有21/21 Attack与Defense对其输入的复算结论仍成立，但不能外推全部合法装备组合的位等价。

结果：[ROUNDING_BOUNDARY.json](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/golden/ROUNDING_BOUNDARY.json>)（前10个差异样例、计数、假设）；复现：[rounding_boundary.py](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/golden/rounding_boundary.py>)。只新增本目录附件，未改产品及历史证据。
