# A03 独立复算补充：完整覆盖原23,211行

本补充取代 [首轮A03报告](<RECOMPUTE_REVIEW_A03.md>) 中“7,893条未重断言”的阶段性覆盖边界；首轮报告保留，不覆盖或删除任何审计产物。

## 最终结论

- 原明细全部23,211行现在都有独立新计算证据：**23,191 PASS / 0 FAIL / 20 INFO**。
- 独立新oracle总计：**23,196 PASS / 0 FAIL / 20 INFO**，其中额外5 PASS是历史计数/CSV一致性交叉检查。
- 组成：数值/指纹/SHA等原PASS映射15,298 + 新增结构/回执原PASS映射7,893 = 原PASS共23,191。剩余未映射原行 **0**。
- 20 INFO 也逐条关联新oracle独立读取的 observation：boot9、排序缺publishedIds4、非Main后值非验收目标7，绝未转成PASS。
- 另有6项数值/FNV原语自测PASS和2例静态风险INFO，不并入上述原明细或新oracle总数。

最终机器汇总：[A03_COMBINED_SUMMARY.json](<A03_COMBINED_SUMMARY.json>)。

完整逐原行新证据映射：[JSON](<A03_COMPLETE_ORIGINAL_CHECK_MAPPING.json>) / [CSV](<A03_COMPLETE_ORIGINAL_CHECK_MAPPING.csv>)。每行包含原明细行索引、check、独立结论、独立证据来源与新oracle行索引；独立结论来自新断言结果，不从原PASS、expected或actual字段推断。

## 新增结构oracle

新增 [supplemental_structure_oracle.py](<supplemental_structure_oracle.py>) 不执行/导入原审计器，也不使用历史expected/actual数值来生成断言。它直接读取原资产、九run的manifest、result、command、input与observation，独立核验：

- session存在、九runId不重复；资产目录有数据。
- manifest runId/pid/files结构，157项文件存在。
- result与manifest内回执副本一致、runId/mode关联、成功结论、失败数、detail计数、逐条result记录。
- command与manifest runId/mode/buildId一致。
- 输入JSONL存在、模式所需真实鼠标/射线或native事件类型、native-window的PID归属。
- observation runId、raw存在及必须字段、live输出字段。
- rig/bag完整字段集合及ContainerData来源存在。
- items/warehouse必需字段，非legacy frozen装备ItemData/QualityData来源存在。
- 每个run至少一条含raw的observation。

新结构细检：**7,893 PASS / 0 FAIL / 0 INFO**。证据：[summary](<supplemental_structure_summary.json>)、[details](<supplemental_structure_details.json>)、[CSV](<supplemental_structure_checks.csv>)、[逐原行补充映射](<supplemental_structure_mapping.json>)。全部此前未覆盖原PASS均已覆盖；[剩余清单](<supplemental_remaining.json>) 为空，remainingUniqueChecks为空对象。

## 仍然成立的真实性边界

**覆盖原断言不等于扩张其证明能力。** 原断言本就没有Inventory完整raw，故即使全部原检查可独立复核，也仍不能重建Inventory canonical；只证明提供的UTF16明文FNV及前后不变。资产SHA一致仍不能单独证明历史Player build资产来源。

C06九项只读与非Main替换数值风险继续分开：A03零加成候选未显示差异，不证明first-worn风险消失；[静态风险反例](<nonmain_static_risk_examples.json>)明确保留，非Player实测FAIL。完整原B2黄金21bit/6PASS与此前工具container双计修正记录由主报告合并独立黄金分工。

全部行为只读原件；仅在授权recompute目录新增脚本和报告，无构建、Player或git操作。
