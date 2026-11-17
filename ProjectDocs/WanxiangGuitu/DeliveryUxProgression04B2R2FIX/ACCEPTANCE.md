# 验收与历史证据

## 当前状态

**本轮限定范围最终 PASS，文档已冻结。** UI-A07 六独立Run均完成，641/641 检查 PASS、全部 exit 0；主线程确认独立 oracle PASS（18,306 细检、0 差异）。 同产品 `ab3d5ba4f4a234598056915ab7b1dca4ad4be57f68298fc24d1b718d267a2df1`，同 Driver `0c44b9c626cbe8d7fa27c83d6369a98c4cb112486e0859713ee57805e719fd45`，buildId=`ux04b2r2fix-ab3d5ba4-b70442f9-0c44b9c6`。

| 六场景 | PID | 检查 | UI结果与原件 |
|---|---:|---:|---|
| A accessory | 19728 | 96/96 | [PASS](<../../../Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-accessory/result.json>)；同类型共存，只替指定旧件；AP61.5→73.5 |
| B arms | 5132 | 96/96 | [PASS](<../../../Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-arms/result.json>)；同类型共存，AP57.4500008→65.8499985 |
| C main | 11412 | 80/80 | [PASS](<../../../Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-main/result.json>)；真实主武器ID，紫色候选贡献43，AP48→83（非旧R1红装132） |
| D board-insufficient | 31532 | 186/186 | [PASS](<../../../Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-board-insufficient/result.json>)；盘满/多件碰撞拒绝，AP240不变 |
| E legal-swap | 12660 | 94/94 | [PASS](<../../../Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-legal-swap/result.json>)；合法双向交换，AP57.5→69.5 |
| F illegal-swap | 5880 | 89/89 | [PASS](<../../../Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-illegal-swap/result.json>)；双方尺寸不兼容，真实Commit拒绝且全不变 |

证据链：各Run result、run-manifest、input-events、state-changes、checks、original-root/measurement-gates 与截图；示例 [F 输入事件](<../../../Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-illegal-swap/input-events.jsonl>)、[F 全量前后](<../../../Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-illegal-swap/state-changes.jsonl>)、[F 预览截图](<../../../Evidence/Runs04B2R2FIX/UI-A07/UX04B2R2FIX-A07-illegal-swap/original-root/screenshots/02-evaluated.png>)。setup 走正常 GameEntry/New/Add/Place API，六场景请求与 Evaluate/Commit 均鼠标→InputSystem→Raycast→正常按钮，不使用 onClick.Invoke。

无副作用判定和自然保存窗口详见 [容量验证](<CAPACITY_VALIDATION.md>)。额外 Reserve0/Worn本体0且容器槽总6/Strength3/Overflow/BoardAdd保旧均为明确标注的 API 检查，不冒充六场景。

## 独立 oracle 最终确认

[报告](<EVIDENCE/REPLACEMENT_ORACLE.md>) / [JSON逐项原件](<EVIDENCE/REPLACEMENT_ORACLE.json>) / [CSV明细](<EVIDENCE/REPLACEMENT_ORACLE.csv>)：204 个 manifest 成员 SHA/bytes、32 组 query/失败 Commit 的九类完整 JSON/UTF16FNV/random/save 只读验证、12 个自然保存 gate（**163** 项检查）、69 组 raycast/down/up 均通过。独立复核成功 Commit 的实际/预测 Single 位、完整投影、身份保全；D 确认为48格满盘且目标在界内、碰撞其他ID，F 旧件原位回包含越界格 (12,0)。这是原始材料一致性 oracle，不是额外 Unity Run 或外部 OS 遥测认证。

## 历史失败完整保留

本轮 25 个实际 Runs 含全部 attempt，4 个本轮历史 FAIL；最终六UI与两浮点门不覆盖、不重写这些失败。

| 原Run | 原始结论 | 原因与后续（不改写原FAIL） |
|---|---|---|
| UI-A01 accessory | [FAIL 79/80](<../../../Evidence/Runs04B2R2FIX/UI-A01/UX04B2R2FIX-A01-accessory/result.json>) | 验证器把 worn 本体 Attack0 错当总容器贡献0；实际槽加成应6，仅修验证器，产品未改 |
| UI-A02 D | [FAIL](<../../../Evidence/Runs04B2R2FIX/UI-A02/UX04B2R2FIX-A02-board-insufficient/result.json>) | 大滚轮过冲，旧件按钮 top Raycast 失败，未到 Evaluate |
| UI-A03 D | [FAIL](<../../../Evidence/Runs04B2R2FIX/UI-A03/UX04B2R2FIX-A03-board-insufficient/result.json>) | 同类滚轮过冲，未到 Evaluate |
| UI-A04-PROBE D | [PASS 178/178](<../../../Evidence/Runs04B2R2FIX/UI-A04-PROBE/UX04B2R2FIX-A04-board-insufficient/result.json>) | 验证器小数滚轮恢复正常鼠标滚动与点击 |
| UI-A05 | 前五场景PASS；[F 原FAIL 80/81](<../../../Evidence/Runs04B2R2FIX/UI-A05/UX04B2R2FIX-A05-illegal-swap/result.json>) | F 九类/random相同但跨5秒自然autosave，save变；严格保留FAIL，不豁免保存差异 |
| UI-A06-PROBE F | [PASS 89/89](<../../../Evidence/Runs04B2R2FIX/UI-A06-PROBE/UX04B2R2FIX-A06-illegal-swap/result.json>) | 仅验证器等待自然保存边界+不跨timer窗口；保存器/interval/clock/完整字段不变 |

旧 R2 [FLOAT001 1ULP 失败](<../../../Evidence/Runs04B2R2/SESSION-20261116-R2-01/UX04B2R2-FLOAT-001/result.json>) 亦保留。R03 双浮点门、保护原件见 [浮点修复](<FLOAT_FIX.md>)、[报告](<REPORT.md>)。最终成功不取消任何历史失败，不代表旧 R1 全归档条件自动清零。
