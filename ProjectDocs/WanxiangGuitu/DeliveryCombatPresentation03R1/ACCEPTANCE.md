# CP03-R1 验收表

**整体验收仍 BLOCKED，未宣称独立复审通过。** 本轮仅工具整改与只读法杖调查，无产品玩法修改。

| 项目 | 状态 | 可核对证据 / 限制 |
|---|---|---|
| 基准/远端/分支与用户保护 | PASS | [BASELINE](BASELINE.md)、[1,802 文件复核](Evidence/protected-after.json) |
| 原错误谓词与宽过滤放行复现 | PASS | [谓词](Evidence/before-classification.json)、[旧审计负例](Evidence/PostStyle/SelfTest/old-audit-bypass.txt)；这是缺陷复现，不是旧工具通过 |
| 分类器规定 9 场景及新增边界 | PASS | [50 项工具自测](Evidence/PostStyle/SelfTest/selftest.json)，每个 CLI 场景保留 JSON/CSV/Markdown/退出码 |
| 区分进程/断言/整体 | PASS | [20 项一致性检查](Evidence/result-summary.json)，验证报告一致，不等于产品通过 |
| 精确 4 处允许差异和审计负例 | PASS | [严格审计](Evidence/locked-contract-delivery.json)、[负例](Evidence/PostStyle/SelfTest/selftest.json) |
| 13 锁定源码及动画采样区段 | PASS | [严格审计](Evidence/locked-contract-delivery.json)；产品 Git diff 空 |
| 24 组发射点与方向 | PASS | [逐组数据](Evidence/locked-contract-delivery.json)，新增暂停箭单列，拒绝重复键 |
| EditorFinal 真实重跑 | UNRESOLVED | [语义回执](Evidence/EditorFinal/Semantic/acceptance.json)：进程 PASS/exit0、291 PASS/2 UNRESOLVED、整体 BLOCKED/2 |
| 非开发验收 Player 真实重跑 | UNRESOLVED | [RuntimeFinal](Evidence/RuntimeFinal/Semantic/acceptance.json)：同上；不是原生点击、纯发行 UI 或人工 |
| 法杖只读根因调查 | PASS | [完整调查](ROOT_CAUSE.md)、[原始观测](Evidence/EditorDiagnosis/aim-diagnosis.jsonl.gz)、[实际事件](Evidence/EditorDiagnosis/events.jsonl.gz) |
| w2-s0-near / w2-s1-near 产品缺陷 | UNRESOLVED | 两项 hpLoss=0，未改 CombatAim；修复等待单独授权 |
| 冻结构建产品输入 | PASS | [1,147 项 0 差异](Evidence/frozen-build-product-binding.json)，旧隔离设置差异来源另外列出 |
| 历史失败/旧 JSON/原输入完整保留 | PASS | [保护复核](Evidence/protected-after.json)、[失败历史](FAILURE_HISTORY.md) |
| CPU/GC/GPU/粒子/池/声道/加载卸载/长战斗 | NOT_RUN | [性能专项](PERFORMANCE.md)：8 类无实际 Profiler 对照，不用理论数据替代 |
| 原生键鼠/U16 | NOT_RUN | 无安全独立交互验收，不以驱动或后台进程代替 |
| 独立人工观感/可读性/音质/打击感 | NOT_RUN | 未执行，不以截图或自动化代替 |
| 本轮新构建/纯发行原生运行 | NOT_RUN | 复用不可变原非开发验收构建，没有新构建或纯发行 UI 通过声明 |
| UNKNOWN/C15/青色帧/Search/JobTempAlloc 根因 | UNRESOLVED | [新日志异常](Evidence/log-findings.json)及原历史，未修改生命周期或日志过滤 |

待授权：CombatAim 发射点/近距防倒射合同提案见 [ROOT_CAUSE](ROOT_CAUSE.md)。未授权前不实施。后续性能与人工验收独立安排，不能因本分支推送关闭开放项。
