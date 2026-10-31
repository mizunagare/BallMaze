# R1.1 验收表

| 条目 | 状态 | 证据 |
|---|---|---|
| 独立分支和基准 | PASS | [基线](BASELINE.md) |
| 修复前错误放行保留 | PASS（缺陷复现） | [5 个 guard FAIL](Evidence/Before/regressions.json) |
| 正式 CLI/API 无合同或无 profile 拒绝 | PASS | [33 项](Evidence/BindingSelfTestFinal/selftest.json)，INCOMPLETE/3、有报告 |
| 固定 SHA、layer、scope 绑定 | PASS | [来源](Contracts/PROVENANCE.json)、[代码/源复核](Evidence/consistency-final.json) |
| 跨 Editor/Runtime 合同误用及篡改拒绝 | PASS | [专项](Evidence/BindingSelfTestFinal/selftest.json)、[新真实回执](Evidence/RealCrossContext/results.json) |
| 原工具 50 项全部保留 | PASS | [结果](Evidence/LegacySelfTestFinal/selftest.json) |
| 真实 Editor | UNRESOLVED | [绑定 PASS，原 2 UR](Evidence/Editor/Semantic/acceptance.json)，整体 BLOCKED |
| 真实非开发验收 Player | UNRESOLVED | [绑定 PASS，原 2 UR](Evidence/Runtime/Semantic/acceptance.json)，整体 BLOCKED |
| 原始回执/进程/CSV/Markdown 一致 | PASS | [35 检查](Evidence/consistency-final.json) |
| 用户/旧证据保护与无产品改动 | PASS | [2664 项](Evidence/protected-after.json)、[空 diff](Evidence/product-diff.txt) |
| 法杖与历史引擎根因 | UNRESOLVED | 未改，不关闭旧问题 |
| 原生 UI/U16、独立人工、性能 | NOT_RUN | 不用工具/受控矩阵替代 |
| 新构建/纯发行原生操作 | NOT_RUN | 重跑原非开发验收构建 |

整体仍 BLOCKED。工具通过不表示游戏和人工体验全部通过。[失败历史](FAILURE_HISTORY.md)。
