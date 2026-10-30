# CP03 原始证据索引

[634项证据与原始/发布SHA256](manifest.json)。原日志gzip保留全部错误上下文，未覆盖旧FAIL；不发布缓存、构建二进制或用户覆盖层。

## 冻结与不变合同

- [业务/动画采样/13锁定源码/24真实配对Spawn不变](locked-contract.json)：剥离4类明确表现调用后AdventureCombat原文等价；实际发射点与方向最大差实测0，新增暂停箭另列。
- [最终9源码/两个最终构建全输入/54资产/五用户文件](final-bindings.json)、[开工五文件](user-before.json)、[全部异常原上下文](log-analysis.json)、[工具语法](tool-syntax.json)。
- [资源与调用点审计](../BASELINE_RESOURCE_AUDIT.json)、[设计/挂点与限制](../DESIGN.md)、[原身份/分层汇总](../SUMMARY.json)、[命令/时间/退出/超时CSV](../RUNS.csv)、[数据合同](../EVIDENCE_SCHEMA.md)。

## 基线、修复与中间变体

- [首次Before原结果](Before/presentation.json)：含错误剑slab假设，原文保留，不当产品根因。
- [有效Before2 205PASS/22FAIL/2UNRESOLVED](Before2/presentation.json)、[真实事件](Before2/events.jsonl.gz)、[逐帧时间线](Before2/timeline.csv)、[原执行夹具](Before2/CP03Cases.executed.cs.txt)。
- [同229项After 227PASS/0FAIL/2UNRESOLVED](After/presentation.json)、[After事件](After/events.jsonl.gz)、[After时间线](After/timeline.csv)。
- [Extended生命周期](Extended/presentation.json)、[旧装备色保留版Final](Final/presentation.json)：独立冻结，不继承为最终。
- [启动cue状态负例](VisualCueBefore/presentation.json)、[启动不抢释放cue](VisualCueAfter/presentation.json)：74/4→78/0，不靠改攻速/限流。
- [最终Editor Final2 291PASS/0FAIL/2UNRESOLVED](Final2/presentation.json)、[真实最终事件](Final2/events.jsonl.gz)、[时间线](Final2/timeline.csv)、[原seed418合成检查点](Final2/Game/ForestRuins/save.json)。死亡由真实攻击/敌弹，代际/增量场景资源探针单列，非命中证明。

## 实际受控截图（不裁切）

VisualBefore/VisualAfter与VisualCueBefore/VisualCueAfter均各16张1280×720原图：start/release × 四武器 × 普攻/技能。它们是离地固定夹具实际GameView，不是森林美术或原生/人工验收。

| 武器 | 原普攻/技能 | 新普攻/技能 |
|---|---|---|
| 剑 | [普攻](VisualBefore/w0-s0-release.png) / [技能](VisualBefore/w0-s1-release.png) | [普攻](VisualCueAfter/w0-s0-release.png) / [技能](VisualCueAfter/w0-s1-release.png) |
| 矛 | [普攻](VisualBefore/w1-s0-release.png) / [技能](VisualBefore/w1-s1-release.png) | [普攻](VisualCueAfter/w1-s0-release.png) / [技能](VisualCueAfter/w1-s1-release.png) |
| 法杖 | [普攻启动](VisualBefore/w2-s0-start.png) / [技能启动](VisualBefore/w2-s1-start.png) | [聚能](VisualCueAfter/w2-s0-start.png) / [技能聚能](VisualCueAfter/w2-s1-start.png) |
| 弓 | [普攻](VisualBefore/w3-s0-release.png) / [技能](VisualBefore/w3-s1-release.png) | [普攻](VisualCueAfter/w3-s0-release.png) / [技能](VisualCueAfter/w3-s1-release.png) |

## 非开发Player与纯发行

- [最终验收构建192警告原文](AcceptanceBuild2/build-report-messages.json)、[全部输入](AcceptanceBuild2/build-inputs.json)、[驱动存在/无Editor引用PE及二进制哈希](AcceptanceBuild2/pe-acceptance.json)。
- [原合成检查点复制SHA](Runtime2/fixture-copy.json)、[Boot/Title/正常Continue](Runtime2/entry-audit.jsonl.gz)、[实际291PASS/2UNRESOLVED](Runtime2/presentation.json)、[Player原日志](Runtime2/Player.log.gz)、[事件](Runtime2/events.jsonl.gz)、[逐帧](Runtime2/timeline.csv)、[实际exit0/未强杀](Runtime2/CP03Runtime.exit.json)、[命令/无超时](Runtime2/results.json)。
- [纯发行96警告原文](PureBuild2/build-report-messages.json)、[全部输入](PureBuild2/build-inputs.json)、[无CP03/旧驱动/UnityEditor的PE与exe/程序集哈希](PureBuild2/pe-exclusion.json)。
- 无2后缀的AcceptanceBuild/Runtime/PureBuild为保留的中间变体，不能冒充最终源码。

近距法杖两个样本、历史引擎根因仍UNRESOLVED；原生/人工/观感/音质/舒适度/最终打击感与Profiler等NOT_RUN。[报告](../REPORT.md) · [验收](../ACCEPTANCE.md) · [复跑](../TESTING.md) · [失败历史](../FAILURE_HISTORY.md)。推送不等于复审通过。
