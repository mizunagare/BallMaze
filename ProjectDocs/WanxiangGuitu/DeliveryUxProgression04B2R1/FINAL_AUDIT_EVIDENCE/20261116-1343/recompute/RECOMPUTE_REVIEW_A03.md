# UX04B2R1-FINAL：A03 独立复算审阅

## 结论与计数口径

- 独立读取九 run 原始 JSONL 与 36 个资产，未执行原 recompute，也未导入其函数；新 oracle 为 [independent_oracle.py](<independent_oracle.py>)。
- 新复算：**15,303 PASS / 0 FAIL / 20 INFO**；详见 [计数与覆盖](<oracle_metrics.json>)、[逐断言 JSON](<oracle_details.json>)、[CSV](<oracle_checks.csv>)、[真实失败清单（空）](<oracle_failures.json>)。
- 原证据明细与 CSV 各 **23,211 行 = 23,191 PASS + 0 FAIL + 20 INFO**，逐行 runId/check/status 序列一致。此为历史计数复核，**不是独立重算了 23,191 条断言**。完整分组见 [历史完整重计数](<historical_recount_complete.json>)。
- [逐条映射 JSON](<historical_oracle_mapping.json>) / [CSV](<historical_oracle_mapping.csv>) 将原 15,298 条 PASS 对应到新 oracle 的独立原始输入计算结果；另 **7,893 条原 PASS 未由新 oracle 同粒度重新断言**。其主要为字段/schema/来源存在性、result/command/input/身份及文件存在性等检查；不能因原 PASS 标志而声称这些已独立重证。新 15,303 = 映射原断言 15,298 + 历史计数交叉核对 5。
- 20 INFO 始终不计入 PASS：9 次 boot 未初始化、4 条排序无结构化 publishedIds、7 条非 Main after 数值不在 C06 目标内。

## 原始输入覆盖

原始输入位于工作区 Evidence/Runs04B2R1/SESSION-20261116-1115/A03（九 run）。共 163 条 observation，154 条含完整本轮 raw。

| mode | observation | raw | 原 PASS | 原 INFO |
|---|---:|---:|---:|---:|
| collection | 24 | 23 | 3477 | 1 |
| golden | 5 | 4 | 355 | 1 |
| guid | 7 | 6 | 494 | 1 |
| preview9 | 22 | 21 | 3772 | 8 |
| restart | 4 | 3 | 529 | 1 |
| sort-imgui | 19 | 18 | 2751 | 1 |
| sort-ugui | 34 | 33 | 5053 | 5 |
| strength0 | 24 | 23 | 3373 | 1 |
| strength3 | 24 | 23 | 3373 | 1 |
| asset/session/global | — | — | 14 | 0 |

注：[首次分类报告](<historical_classification.json>) 总数正确，但 byMode 中空的 asset/session 桶未展示 14 条无 mode 的全局检查；新增的 [完整重计数](<historical_recount_complete.json>) 已明确列出，保留前次工具产物，不改历史。

## 独立算法

1. 活跃装备按 id 首项去重，以索引模拟 C# 身份；排除 worn/overflow，仅 board 或有效背包 Main 入攻击。Reserve 不因标记自动计入。旧装备按 legacyTier/quality 公式，新装备 frozen 值另与 ItemData × QualityData 验算。
2. binary32 对每次加乘及最终比较进行舍入；D24 = baseDamage + loadoutAttack + rank×5；Spear BasicPower 为 AttackPower×1.25。**Rig/Bag attackBonus 各只加一次**，containerBonus 是诊断字段，绝不再次加进总攻击。
3. 排序独立筛选 category/quality/status/favorite/text；数值或 UTF16 ordinal 主键，再以 id UTF16 ordinal 打破平局。
4. FNV 使用 UTF16 code-unit XOR、64bit 乘法模数，不是 UTF8 或 UTF16 字节 FNV。原语独立已知值测试见 [6 项辅助自测](<oracle_primitive_tests.json>)；这 6 PASS 不并入 15,303。

## 数值与只读结果

- 154 raw 的 live AttackPower/BasicPower、rank bonus 和公开 GearAttack/GearDefense/AttackBonus 均复算一致；924 条 D24 +154 条 Strength 断言。
- Strength0：rank=0、bonus=0、loadoutAttack=8、AP/Basic=33。Strength3：rank=3、bonus=15、loadoutAttack=8、AP/Basic=48。Main 候选攻击132：after AP 分别157/172，delta均124；preview9 Main after157，delta124。3 个 Main 评估共117细检（含字段集合断言），全通过。
- 12 条 sort observation 独立生成期望顺序；8 条有 publishedIds 并一致，4 条缺结构化 publishedIds 保留 INFO。没有 renderedIds，因此不声称独立验证渲染顺序。
- 8 个 preview9 评估覆盖九项：72 项 hash before/after 不变，144 次 FNV 前后复算一致，九项 plaintext 不变及 raw.canonical 关联一致。C06 共256断言，FNV144断言。
- **Inventory canonical 无完整 Inventory raw 字段，不能独立重建 canonical**；这里只验证提供的 UTF16 明文与 FNV，以及前后未变，不能升级为完整状态序列化正确性。

## 非 Main 数值风险与 C06 分开

[非 Main 原始诊断](<oracle_nonmain_risks.json>) 保留7例 before/after及候选。A03实际容器候选 rig_light / bag_gather 的攻击与防御bonus均0；新oracle按实现复算一致，按卸旧再换新的数值也无差异。**零差异不意味着风险已修复，更不意味着所有角色完整数值矩阵正确。**

源代码 Preview 追加 worn 候选但不卸下旧同类容器，ContainerFor 取 first-worn，故有既有替换语义风险。新增 [静态风险反例](<nonmain_static_risk_examples.json>)：若同一 A03 初始状态假设换 bag_relic，真实替换应多攻击6但 first-worn保留0；换 rig_heavy 应多防御3但 first-worn保留0。两例明确为静态反例/INFO，**不是 A03 已观察 Player FAIL**，也不计入原20INFO。C06仅证明九项只读，不负责关闭该数值风险。

## SHA 与边界

- 九 run manifest 所列157文件的 bytes、SHA256和清单覆盖均一致；另记录36资产SHA。见 [原始文件与资产SHA](<oracle_files_sha256.json>)；原明细/CSV/summary、源公式、manifest自身SHA另见 [来源SHA](<oracle_additional_source_sha256.json>)。
- 当前资产一致不单独证明历史 Player build 的资产来源；执行结果/输入回执/schema等未全重断言的边界以逐条映射为准。
- 历史原B2黄金21bit与6/6，以及此前container-bonus双计修正记录，由独立黄金分工报告整合，不由本A03计数冒充。
- 无构建、无Player、无git操作；仅新增指定recompute目录内审计脚本/报告/JSON/CSV。脚本采用 -B 执行防止生成目录外pycache。既有代码、原始证据及历史报告未修改。
