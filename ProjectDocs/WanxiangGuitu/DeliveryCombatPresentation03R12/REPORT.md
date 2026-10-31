# CP03-R1.2 交付报告

基准 `00a8d740b824f9eb97c892da5195385517446e60`，独立 `fix/cp03-review-r1.2`。main 不改，R1/R1.1 提交和原证据不变；最终 SHA 由所属交付提交及回复绑定。[基线](BASELINE.md)。

## 已修复

仅修改 Receipt.py 和两个正式包装器，新增文档目录内的测试/验证工具。移除全部默认进程成功值；实际状态从运行器原字节快照与同次 NativeProbe 退出回执共同取得。手工参数不能授权成功、不能补缺字段。检查合法性、一致性、作用域、运行目录/配对和时间；报告完整记录来源与 SHA。[进程合同](PROCESS_EVIDENCE.md)。

## 本轮实际结果（分层，不合并为游戏通过率）

| 集合 | 结果 |
|---|---|
| 修复前8个场景 | 6 个 guard FAIL（旧误判），2 个原有正确拒绝对照；全部保留 |
| 原工具检查 | 50 PASS，旧源码不改，新副本仅适配进程输入 |
| R1.1 工具检查 | 33 PASS，旧源码/证据不改 |
| R1.2 专项 | 60 PASS /0 FAIL，包含全部要求及手工参数不能补缺字段 |
| 真实退出证据读核 | 8 PASS；其中293 PASS输入是明确标记合成副本 |
| 一致性 | 38 PASS |
| 真实 Editor | 进程证据 PASS/exit0；291 PASS/2 UNRESOLVED；整体 BLOCKED/分类与宿主 exit2 |
| 真实非开发验收 Player | 进程证据 PASS/exit0；291 PASS/2 UNRESOLVED；整体 BLOCKED/分类与宿主 exit2 |

[汇总](Evidence/consistency.json)、[Editor](Evidence/Editor/Semantic/acceptance.json)、[Runtime](Evidence/Runtime/Semantic/acceptance.json)。实际回执来源字段完整，claims 全为 null，说明成功不是从手工默认值取得。[真实来源读核](Evidence/RealEvidenceChecks/results.json)不修改原始三个文件，不是额外8次 Unity 运行。

正式矩阵均无超时、forcedTermination=false。Player 重跑原不可变非开发验收构建，经 Boot/Title 受控 Continue 原合成检查点，非原生键鼠或人工。未做新构建。旧50/33、专项初轮57与补强后60均独立保存，不覆盖。

## 保护与开放项

[3,476 文件](Evidence/protected-after.json) SHA 一致，用户状态未变；[1,147 产品输入/二进制](Evidence/input-binding.json)一致；[产品 diff](Evidence/product-diff.txt)为空。没有修改 Assets、CombatAim、数值、碰撞、AI、经济、存档、依赖或 CI。

法杖两项、UNKNOWN/C15/青色帧/Search/JobTempAlloc 仍 UNRESOLVED；原生 U16、人工、性能仍 NOT_RUN。本轮进程证据整改已验证，整体验收仍 BLOCKED；不因推送关闭开放项。完成独立分支交付后暂停。

[验收](ACCEPTANCE.md) · [复跑](TESTING.md) · [失败历史](FAILURE_HISTORY.md) · [证据](Evidence/INDEX.md)。
