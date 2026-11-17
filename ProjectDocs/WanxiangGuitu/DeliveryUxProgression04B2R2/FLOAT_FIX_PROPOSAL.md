# R-03 位差单独修复方案（待额外授权，未执行）

## 已证问题

同一Unity Mono6.13进程、同三件Single输入、同枚举顺序，旧LINQ Sum与现B2AttackModel.ComputeAttack最终差1 ULP。原始证据见[FLOAT_RUNTIME](<FLOAT_RUNTIME.md>)。根因是原Single Sum内部double累加并在返回转Single，而权威模型目前float局部逐项累加；不能靠UI格式或容差掩盖。

## 建议最小方案

在**现有B2AttackModel权威方法内部**恢复原有累计与转换语义，优先复用原Enumerable.Sum选择器实现；保留Active去重/顺序、rig/bag的原加法顺序和最终Single返回。不可在产品另建第二套LegacyAttack公式供部分UI绕行。

拟议表达式（仅文档，不是已应用补丁）：

```csharp
// Proposed inside existing ComputeAttack, only AFTER separate approval:
return Active(list, mainId).Sum(i => i.Attack)
     + (rig != null ? rig.attackBonus : 0f)
     + (bag != null ? bag.attackBonus : 0f);
```

ComputeDefense有相同float累计形状，但本Run未实测其非零边界，不能声称已发现Defense位差。是否同范围恢复及定向测试，应由负责人另行批准。不能改装备系数、D-24叠加规则、Schema或存档来“修正”。

## 获批后验收建议（本轮未执行）

1. 固定本Run三件原bits、原序和同Mono类型，验证权威方法与原路径逐位相等，容差仍为0。
2. 增加反序/更多Active及非零容器加成、非零Defense的定向边界，明确只验证获批范围。
3. 保留当前差异Run与二进制/源码，不覆盖；新Run用独立ID和目录。
4. 单链数值语义确认后，再恢复已授权R01工作：PreviewAdd不移旧，PreviewReplace显式指定目标，复用真实空间规则并做六场景正常UI操作验收。

**当前没有修改任何产品方法，也未生成可应用的产品补丁。不自行把提案视为新增修复授权。**
