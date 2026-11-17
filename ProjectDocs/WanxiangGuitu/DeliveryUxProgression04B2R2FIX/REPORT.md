# UX04B2R2FIX 交付报告

## 结论与冻结身份

**本轮限定范围验收 PASS，六份交付文档最终冻结。** UI-A07 六个独立 WindowsPlayer Run 已全部实测 PASS（641/641 检查），双浮点门均为 0 ULP；独立 [oracle 报告](<EVIDENCE/REPLACEMENT_ORACLE.md>) / [逐项原件](<EVIDENCE/REPLACEMENT_ORACLE.json>) 共 18,306 细检、0 差异，主线程已确认。不是用旧 PASS 替代本轮取证，亦不是发布级结论。详细矩阵见 [验收记录](<ACCEPTANCE.md>)。

- 产品 DLL SHA256：`ab3d5ba4f4a234598056915ab7b1dca4ad4be57f68298fc24d1b718d267a2df1`。
- UI Driver SHA256：`0c44b9c626cbe8d7fa27c83d6369a98c4cb112486e0859713ee57805e719fd45`。
- UI buildId：`ux04b2r2fix-ab3d5ba4-b70442f9-0c44b9c6`。身份、PID、实测结果可对照 [accessory 原件](<../../../Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-accessory/result.json>) 与 [illegal-swap 运行清单](<../../../Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-illegal-swap/run-manifest.json>)。

## 本轮实际修复

1. 唯一算术修改为 [ComputeAttack:111–118](<../../../Assets/CombatPrototype/B2AttackModel.cs#L111>) 恢复 `Active.Sum(i => i.Attack) + Rig + Bag`。防御和 Active 不搭车改动；见 [浮点修复](<FLOAT_FIX.md>)。
2. [显式 PreviewAdd/PreviewReplace](<../../../Assets/CombatPrototype/AdventureLoadout.cs#L33>) 接受真实候选ID、旧件ID、target、role、rotation；Clone 投影、提交重新验证、共用空间规则。旧 Main/Reserve/Container 提交路径保留；见 [替换模型](<REPLACEMENT_MODEL.md>)。
3. [共享会话及 IMGUI 工作面](<../../../Assets/CombatPrototype/ContainerInventoryView.cs#L10>) 与 [uGUI 独立工作面](<../../../Assets/CombatPrototype/CatInventoryPresenter.cs#L86>) 共用请求/结果。模型及 UI 独立源码 review 已通过（主线程确认）；端到端六Run只覆盖 uGUI，不冒充 IMGUI 实测。

## 原始证据与不可变边界

- R03 双门均为真实 Mono 6.13 WindowsPlayer，原 1/2/3 前缀及 7 cases/24 prefixes 位级相等、ULP 0、容差 0：[首门](<../../../Evidence/Runs04B2R2FIX/FLOAT-GATE/UX04B2R2FIX-FLOAT-001/result.json>)、[最终门](<../../../Evidence/Runs04B2R2FIX/FINAL-A02/UX04B2R2FIX-FLOAT-FINAL-001/result.json>)。
- [保护汇总原件](<../../../Evidence/Runs04B2R2FIX/FINAL-PROTECTION/summary.json>) 基线 12808 文件，errors=[]，仅四个产品源 AUTHORIZED；ComputeDefense 387 bytes、Active 526 bytes 与 FIX 前逐字相同。961 **字面清单文件**完全不变；不能解释为清单内全部 payload SHA 不变：四产品源为已授权变化，未回写历史清单。
- Preview/失败 Commit 对九类 canonical fullJSON + UTF16FNV、完整 random、每个 save 文件的 base64/SHA256 均要求全不变。自然存档仍开，取证等待正常 LastSavedAt 推进后在同一 timer 窗口比较；详见 [容量与原子性验证](<CAPACITY_VALIDATION.md>)。

## 历史与范围

本轮共 25 个实际 Runs（含所有 attempt），其中 4 个历史 FAIL：A01 的错误断言、A02/A03 的滚轮失败、A05 的自然保存跨窗失败均完整保留，不将最终成功改写成“从无失败”。见 [验收历史](<ACCEPTANCE.md>)。本轮不是 release，不是全 Unity 资产重构建，也不宣布旧 R1 全部历史归档条件清零。防御外部精度、IMGUI 实测及 Windows 分辨率范围限制见 [风险登记](<RISK_REGISTER.md>)。
