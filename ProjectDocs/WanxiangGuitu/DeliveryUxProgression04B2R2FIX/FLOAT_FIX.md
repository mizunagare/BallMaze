# R03 浮点修复

## 原因及最小修复

旧 R2 [FLOAT001 原件](<../../../Evidence/Runs04B2R2/SESSION-20261116-R2-01/UX04B2R2-FLOAT-001/result.json>) 在真实 Mono 6.13 WindowsPlayer 报 BIT_DIFFERENCE_STOP：旧链 `418B999A`，重写链 `418B9999`，差 1 ULP。该失败保留，不以显示均为 17.45 判等。

[当前 ComputeAttack](<../../../Assets/CombatPrototype/B2AttackModel.cs#L111>) 恢复原 `Enumerable.Sum(Single)` 语义（该运行时用 Double 累加，最终转 Single），随后按原顺序加 Rig，再加 Bag；不是提升容差，也不是逐步 Single 累加后再补偿。此为唯一算术修改。

[保护原件](<../../../Evidence/Runs04B2R2FIX/FINAL-PROTECTION/summary.json>) 记录 ComputeDefense 与 Active byteIdentical=true；前者 387 bytes，后者 526 bytes，均与 FIX 前逐字不变。**不声称 ComputeDefense 已修复其外部浮点精度风险。**

## 真实运行门

| 门 | 原件 | 结论 |
|---|---|---|
| UX04B2R2FIX-FLOAT-001 | [result](<../../../Evidence/Runs04B2R2FIX/FLOAT-GATE/UX04B2R2FIX-FLOAT-001/result.json>) | 418B999A = 418B999A，ULP 0 |
| UX04B2R2FIX-FLOAT-FINAL-001 | [result](<../../../Evidence/Runs04B2R2FIX/FINAL-A02/UX04B2R2FIX-FLOAT-FINAL-001/result.json>) / [运行身份](<../../../Evidence/Runs04B2R2FIX/FINAL-A02/UX04B2R2FIX-FLOAT-FINAL-001/run-manifest.json>) | 同产品 ab3d5ba4…，BITWISE_EQUAL，exit 0 |

两个门均覆盖原 1/2/3 前缀，另列 7 cases / 24 prefixes：正序、反序、6 Active、非零 Rig 3.25、BagRelic 6、双方加法顺序及 repeat。全部位级相等，接受容差严格为 0；每步旧/新实际前缀与累加轨迹可回查原件。Rig 3.25 是瞬态输入，不是修改目录资产；目录 Rig 的 attackBonus 仍均为 0。BagRelic 使用现有加成 6。

最终门记录 fixtureBefore/After 与 randomBefore/After 相同；最终 [独立 oracle](<EVIDENCE/REPLACEMENT_ORACLE.md#L14>) 复核既有真实 Mono 七用例/24前缀/ULP0，没有另做Python数值门或新增产品执行。结论限所测运行时和输入；不可扩展成所有平台、所有数值组合或防御链的通用数值证明。
