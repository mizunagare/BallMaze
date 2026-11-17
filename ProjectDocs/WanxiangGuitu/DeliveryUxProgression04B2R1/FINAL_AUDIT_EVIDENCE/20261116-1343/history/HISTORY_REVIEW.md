# UX04B2R1-FINAL G/I 历史文档独立审计

## 结论

**CONDITIONAL / 历史完整性部分通过，不可宣称全部历史二进制可重验证。** 本附件仅给出历史审计与准确候选文件列表，不生成最终提交白名单，不授权提交。未改产品、工具、历史证据、历史INDEX或历史文档；未构建、未新增Player、未暂存。唯一写入范围为本 history 审计附件目录。

## 方法与可复核附件

- [审计脚本](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/history/history_audit.py>)按实际文件读取字节并计算SHA-256，检查INDEX中每一条path/bytes/hash、45个历史运行manifest中的文件表、CSV路径与27次R1运行身份、Markdown链接、历史driver receipt与实际归档/live DLL。
- [路径/哈希/缺失完整JSON](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/history/HISTORY_PATH_HASH_MISSING.json>)含每项源位置、预期/实际SHA、bytes、存在性、异常；候选列表字段为 candidateFormalFiles_NOT_FINAL_WHITELIST、candidateEvidenceFiles_NOT_FINAL_WHITELIST、mustPreserveFailureFiles。这些是核查候选，不是最终白名单。
- [摘要](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/history/audit_summary.json>)与[glob发现输入清单](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/FINAL_AUDIT_EVIDENCE/20261116-1343/history/discovered_inputs.json>)。
- 共13472个核查关系：13253个hash匹配、160个仅路径存在而无历史预期hash、13个设计组合/通配表达式非字面路径、46个当前产品对历史基线摘要差异。关系数量含重复引用，绝不等同独立证据文件数。
- 不运行历史recompute、不重新计算产品逻辑；本项只审计其原件、路径与摘要。当前hash自洽不等于独立证明“此前从未改写”；没有可信先验digest的文档仅记录当前hash。

## B2 INDEX / 六个最终PASS / 历史FAIL

[B2 INDEX](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2/EVIDENCE/INDEX.json>)当前SHA256为 a0c209b8257678b6a1061dbe7993d7f80cc6f4a8c839cf97a08351a76497c9f7，与R1历史引用匹配。不是信任totalEvidenceFiles=80：逐核6个final Run的80条文件SHA/bytes全匹配；另4个receipt全匹配。六个最终Run为GOLDEN/UGUI/IMGUI/FAVSEED/RESTART/READBACK-FINAL，均与实际manifest的完成/exit 0状态一致。

全部18个B2运行manifest及其文件表均检查；唯一原始失败为[UGUI-01 manifest](<Evidence/Runs04B2/UX04-B2-UGUI-01/run-manifest.json>)，exit=3，driver=827877e4…，失败文本与日志原件存在且hash匹配。不能用6个final PASS抹掉它。IMGUI-01/02/03虽然manifest为COMPLETED，INDEX明确标为不确定诊断（合成输入不改变IMGUI）；不能把它们重新归类成功验收。

[B2报告](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2/REPORT.md#L43-L48>)“80份”指六个final Run文件，而非全部历史。其[CSV](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2/PLAYER_RUN_MATRIX.csv>)是41条检查汇总，不是18次运行的逐次真值表。旧报告的“全部实施完成”必须和[B2 FINAL审计](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2/FINAL_AUDIT.md#L13-L26>)CONDITIONAL_PASS/七项条件及R1当前声明一起阅读，不能把旧结论当现状。

## R1 A01 / A02 / A03及旧复算

[R1 INDEX](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/EVIDENCE/INDEX.json>)共550个path/hash核查关系全部匹配（含历史B2 INDEX引用），没有缺失的INDEX列出文件。27次CSV身份字段与各自manifest无差异；A01 8/9、A02 9/9、A03 9/9为原始结果状态，不是本次新运行。

- A01原生失败：[result](<Evidence/Runs04B2R1/SESSION-20261116-1115/A01/sort-imgui/result.json#L4-L14>) FAIL，8 checks/7 PASS/1 FAIL；[原生输入](<Evidence/Runs04B2R1/SESSION-20261116-1115/A01/sort-imgui/r1-input-events.jsonl#L17-L18>)两次foreground-request result=False，与保留条排序未改变的[失败原件](<Evidence/Runs04B2R1/SESSION-20261116-1115/A01/sort-imgui/r1-failure.txt>)相符。不得覆盖或把失败改名为PASS。
- [A02人工审查](<Evidence/Runs04B2R1/SESSION-20261116-1115/manual-A02-review.json>)明确区分自动9/9和数值HUD不足；其4个截图path/hash均核查。营地fallback无数值HUD，不因recompute PASS自动关闭C05。
- [A03人工审查](<Evidence/Runs04B2R1/SESSION-20261116-1115/manual-A03-review.json>)原件及其截图path/hash已核查；本历史项没有另行视觉复审，不能冒称本代理目视确认33/48。A03通过记录与A02不足记录共存。
- 旧复算原件：[A01](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/EVIDENCE/recompute-A01/summary.json>) FAIL/31、[A01-schema2](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/EVIDENCE/recompute-A01-schema2/summary.json>) FAIL/10、[A02](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/EVIDENCE/recompute-A02/summary.json>) PASS/0、[A03](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/EVIDENCE/recompute-A03/summary.json>) PASS/0全部保留并记录当前hash；每批details/failures/checks也在候选列表，不能仅交最终summary。

## 显式 supersededBy 关系：缺失

历史两个INDEX、运行manifest、receipt/人工审查及所核文档没有显式supersededBy字段，检出0项。因此不能判为“显式关系存在且正确”。B2只有supersededDiagnosticRuns的自然语言分组，R1只有报告的A01→A02→A03叙述；缺少机器可读的逐run/逐条件替代链。尤其A01失败不能由A02某个非对应模式一笔覆盖；A02数值HUD不足应关联A03 strength0/strength3及人工通过审查，而不是只关联最终总体PASS。此轮不补写旧INDEX；主线程可在新审计附件中记录缺口/限定解释，但不得声称原索引已有字段。

## 历史driver源 / 二进制 / receipt

各版executed driver源的SHA均与对应receipt匹配；当前交付源为最新版本，不能反向替代旧executed源。下面只说明字节可取得性，不代表本次重跑成功。

| 批次 | receipt driver SHA256 | 当前可取得性 |
|---|---|---|
| B2初版/UGUI-01失败 | 827877e4cbb944223c16247fa1a1b8f5f9070217e8f302648e7695ef2fe761d3 | 未找到归档；receipt live路径已非该hash；不可声称可重验证 |
| B2 r2 | 2f18b8eb2618ff2571bef5118dfc3df00f60c8756a35597dc26edf9b2cfd66e7 | 同上 |
| B2 r3 | 3ba56e1914fa5c027409acbae64f06a768ebd38b838163e71f2119815b535d9b | 同上 |
| B2 r4/final | b7a46b0ab05b237cdfb1e57ad9cc5f822c753fc1b094e282d453544abc694c7b | receipt live路径匹配，但无Evidence归档DLL |
| R1早期r2（非SESSION批次） | 408df57e2ce821f2f860671e7bd9a1b9fa0963b7a49eb2c06ac3cbccf0cbad3e | live匹配，无Evidence归档DLL |
| R1 A01 | d47dcfb8ac2d43c5b64c60dc5c62b242260148f5e8118ceaced4b4025e5a972e | [归档DLL](<Evidence/Runs04B2R1/SESSION-20261116-1115/_build/driver/B2R1ObservationDriver-A01.dll>)与receipt一致；live已更新，不应当作A01缺失 |
| R1 A02 | e222298a514e7ca73769b3094c684f8219b18925be2d9a8385fc2072b75ea9da | [归档DLL](<Evidence/Runs04B2R1/SESSION-20261116-1115/_build/driver-A02/B2R1ObservationDriver-A02.dll>)与receipt一致 |
| R1 A03 | 5a2654dead65d59485ad4810dc44a8746609a8546e7c93c068fa8867e55da384 | [live DLL](<Builds/ux04b2r1/SESSION-20261116-1115/player/WanxiangGuitu_Data/Managed/B2R1ObservationDriver.dll>)与receipt一致，但Evidence未归档该DLL |

完整receipt路径、live目标路径、每个归档匹配path/hash及缺失状态见JSON driverReceipts。产品B2/R1 Assembly-CSharp归档存在并已hash核查。B2前三版缺失结论范围是已发现Evidence归档与receipt明确目标，并非对整台机器任意目录的不可证伪断言。不得用相同源码“重新编译一下”冒充历史二进制；本轮也未做任何复制/构建。

## 文档 / PreImplementationAudit / 保护摘要

70个正式文档/工具/基线备份文件逐项hash登记，其中[PreImplementationAudit文件矩阵](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2/PreImplementationAudit/IMPLEMENTATION_FILE_MATRIX.csv>)的字面路径核实存在；13个组合表达式/通配符不是物理路径，已专门标注，不虚报为缺失。该设计期目录有7份MD及1份CSV，没有独立INDEX文件；不能强造一个INDEX存在性通过。所有可解析Markdown本地链接均存在，但历史绝对I盘链接的跨机器可移植性仍有风险。

[B2保护表](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2/PROTECTION_SHA256.tsv>)对当前产品原始字节有39个hash差异：32个当前CRLF文件转换为LF后匹配历史值，另7个为R1已改变源文件。不能将文本换行归一化等价表述为原始SHA相等，也不能以此认定历史证据被篡改。[R1保护表](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/PROTECTION_SHA256.tsv>)11609项current_sha256均与当前文件匹配。[_baseline_snapshot](<ProjectDocs/WanxiangGuitu/DeliveryUxProgression04B2R1/_baseline_snapshot/snapshot.json>)的8份backup本身全部匹配历史hash；其中7个原产品路径与历史基线不同是已实施R1的预期差异，JSON保留该差异，不篡改旧快照。

## Ignore / sparse / 提交候选建议

- git core.sparseCheckout=true、core.sparseCheckoutCone=false；实际worktree sparse规则没有B2/B2R1文档或Evidence范围。B2/B2R1正式文件均未被git跟踪，简单暂存可能受sparse范围阻拦。主线程须据最终白名单另行处理，不能本轮悄悄改sparse配置。
- 对845个正式/证据候选（70+775）逐项git check-ignore -v --stdin无匹配；退出1表示“没有任何忽略项”，不是命令故障。不能因此忽略sparse问题。
- Builds和Library被根ignore规则排除；当前部分driver仅保存在被忽略的Builds，复制整个Builds作为提交证据既无关又不安全。应在后续显式授权下只归档确实可取得且匹配receipt的必要DLL；本轮权限仅新增脚本/报告，故未新增任何二进制。缺失版本仍须登记不可取得。
- JSON给出70个正式文件精确候选（B2/PreImplementationAudit、两版报告与INDEX/CSV/保护表、R1语义文档、历史工具、基线备份、四批recompute原件），775个严格在B2规范运行目录/两版_build/R1 SESSION内的证据候选。排除运行时重复roots和runs目录。不要递归纳入整个历史Evidence目录。
- 41个mustPreserveFailureFiles是最低失败原件集合，包含B2 UGUI-01整套证据、R1 A01 sort-imgui整套证据、两个旧FAIL复算的summary/details/failures/checks和A02人工不足记录。除此必须保留A02人工引用截图、A03相应补证和B2 IMGUI不确定诊断，均在完整证据候选内，不能只挑PASS或摘要。
- 排除无关PH-R2、Runs03/04B0/B1等历史Evidence、用户churn、所有Builds/Library、真实用户存档、无关历史ProjectDocs；本候选不意味着把保护表列出的11609项全部加入提交。产品源码/meta由主线程独立审计后给最终白名单，此代理不越权生成。

## 适用限制

未独立视觉重审HUD，未复跑历史Player，未检查远端提交，未重新执行产品数值复算。发现的真实缺口是显式替代关系缺失与部分历史driver不可取得/只有忽略区live副本；这些不能被路径hash匹配率或最终PASS计数掩盖。本报告建议保持条件结论，直到主线程明确披露这些限制并作出最终判断。
