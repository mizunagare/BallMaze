# 风险与适用范围

| 项 | 当前处理及残余风险 | 原始依据 |
|---|---|---|
| R03 Attack 浮点回归 | 已恢复 Active.Sum，双门严格0 ULP；只证明所测 Mono 6.13 WindowsPlayer 与输入，不承诺全平台/任意输入 | [最终浮点原件](<../../../Evidence/Runs04B2R2FIX/FINAL-A02/UX04B2R2FIX-FLOAT-FINAL-001/result.json>) |
| Defense 外部精度 | **未修复**；ComputeDefense 387 bytes 与 FIX 前一致，不能把 Attack 门推广至 Defense | [防御实现](<../../../Assets/CombatPrototype/B2AttackModel.cs#L120>) / [方法保护](<../../../Evidence/Runs04B2R2FIX/FINAL-PROTECTION/summary.json>) |
| Active 与规则漂移 | Active 526 bytes 逐字不变；没有借修复重写叠加、目录数值或来源规则 | [Active](<../../../Assets/CombatPrototype/B2AttackModel.cs#L96>) |
| 自然自动存档干扰 | 未关闭保存器。等待自然保存后仅在同timer窗口比较完整save；跨窗仍失败。A05 FAIL永久保留，不能说“关闭保存获得PASS” | [原FAIL](<../../../Evidence/Runs04B2R2FIX/UI-A05/UX04B2R2FIX-A05-illegal-swap/result.json>) / [自然保存原件](<../../../Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-illegal-swap/original-root/measurement-gates.jsonl>) |
| UI 覆盖 | 两套源码工作面，共享模型/会话；六端到端仅uGUI。IMGUI、更多分辨率/DPI/平台仍需独立回归 | [IMGUI](<../../../Assets/CombatPrototype/ContainerInventoryView.cs#L117>) / [uGUI](<../../../Assets/CombatPrototype/CatInventoryPresenter.cs#L86>) |
| 验证器误判与交互失败 | A01 worn断言与A02/A03滚轮失败均留档；A04/A06为probe，不能偷算成最终六Run | [完整历史](<ACCEPTANCE.md>) |
| 保护口径 | 12808基线仅4产品源授权；961字面清单文件不变≠列内payload全不变，四产品合法变化不回写历史清单 | [保护原件](<../../../Evidence/Runs04B2R2FIX/FINAL-PROTECTION/summary.json>) |
| 发布/历史归档 | 本次为限定UX修复取证，不是release/全Unity资产重构建，也不清零旧R1全部历史归档条件 | [交付范围](<REPORT.md>) |
| 最终交付门 | 六Run641/641与独立oracle18,306细检/0差异均通过，主线程已确认，本轮限定范围PASS；不扩展为发布保证或外部OS认证 | [oracle原件](<EVIDENCE/REPLACEMENT_ORACLE.md>) / [验收状态](<ACCEPTANCE.md>) |

附加API的Reserve0、Worn本体0/槽总6、Strength3、Overflow0、BoardAdd保旧只提供对应模型/权威性证据，不扩大真实UI六场景或发布级覆盖范围。
