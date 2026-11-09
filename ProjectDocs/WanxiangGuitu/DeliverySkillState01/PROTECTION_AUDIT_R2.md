# CP06-C24-B2-R2 保护哈希文档核对（独立勘误，不改写历史）

> 本文件是 `SKILL-STATE-01` 开工前的第一项核对，针对用户指出的矛盾：
> `DeliveryCrystalCavernC24B2R2/Evidence/After/protection.json` 中
> `b1b2r1HistoryModified = true`，但 `protectedViolations = []` 且 `verdict = PROTECTION_PASS`。
>
> **结论：这是汇总工具判据的假阳性，不是历史被修改。** R2 的 `protectedViolations=[]`
> 与 `PROTECTION_PASS` 是正确的；`b1b2r1HistoryModified=true` 是字段名与判据不一致造成的误报。
> R2 已提交的 `protection.json` 及其全部历史文件**原样保留，未改写**。

---

## 1. 核对基线与对象

| 项目 | 值 |
|---|---|
| 仓库 | `https://github.com/mizunagare/BallMaze.git` |
| R1 tip（R2 汇总基线） | `c388e9b7ecf9b5619a65fac81227eba68f61b832` |
| R2 tip（被核对提交） | `28d9fc529ba3bc621f0f7e73a183a18fba69f867` |
| 被核对文件 | `28d9fc529…:ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R2/Evidence/After/protection.json` |
| 生成工具 | `DeliveryCrystalCavernC24B2R2/Evidence/Tools/finalize_evidence.py`（`protection()`） |
| 本批核对工具 | `DeliverySkillState01/Evidence/Tools/audit_r2_protection.py`（只读） |
| 原始证据 | `DeliverySkillState01/Evidence/Before/r2-protection-audit.json` |

## 2. 矛盾的精确成因

R2 `finalize_evidence.py` 中两个字段使用了**不同粒度**的前缀：

```python
PROTECTED_PREFIXES = [
    "ProjectSettings/", "Packages/",
    "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B/",
    "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B1/",
    "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2/",
    "ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B2R1/",
]
...
"b1b2r1HistoryModified": any(
    p.startswith("ProjectDocs/WanxiangGuitu/DeliveryCrystalCavernC24B")
    for p in changed),
```

`b1b2r1HistoryModified` 的前缀 **`DeliveryCrystalCavernC24B` 没有尾部斜杠**，
且不排除本批自身目录。因此它同时匹配：

- `DeliveryCrystalCavernC24B/`、`…B1/`、`…B2/`、`…B2R1/`（真正的历史）
- **`DeliveryCrystalCavernC24B2R2/`（R2 本批自己新增的交付目录）** ← 误报来源

`PROTECTED_PREFIXES` 使用带尾斜杠的精确前缀且不包含 `…B2R2/`，
所以 `protectedViolations` 只统计真实受保护路径，结果为空是**正确**的。

## 3. 严格核对结果

| 检查 | 结果 |
|---|---|
| R1 tip → R2 tip 的全部变更文件 | **601** |
| 其中 `DeliveryCrystalCavernC24B2R2/` 自身新增 | **601（100%）** |
| B1 / B2 / R1 / 原 B 历史目录变更 | **0** |
| `ProjectSettings/` / `Packages/` 变更 | **0** |
| `.unity` / `.asset` 变更 | **0** |
| `Assets/` 产品源码变更 | **0** |
| 交付目录之外的变更 | **0** |
| 宽松前缀 `DeliveryCrystalCavernC24B` 命中 | **601** |
| 其中真正属于历史目录 | **0** |
| 全部命中都属于 R2 自身目录 | **true** |

**更强的树级证据**：分别取 R1 tip 与 R2 tip 的 tree object SHA，
`DeliveryCrystalCavernC24B/`、`…B1/`、`…B2/`、`…B2R1/`、`ProjectSettings/`、`Packages/`、`Assets/`
**全部逐一相同**（`allProtectedTreesIdentical = true`）。这排除了"文件被改回原样而 diff 看不到"的可能。

`r2-protection-audit.json` 记录了逐路径分类、树 SHA、两个判据的复算结果与被核对文件的 SHA256。

## 4. 判定

| 字段 | 是否正确 | 说明 |
|---|---|---|
| `protectedViolations = []` | ✅ 正确 | 真实受保护路径零改动 |
| `verdict = PROTECTION_PASS` | ✅ 正确 | 由上项直接得出 |
| `productSourceModified = false` | ✅ 正确 | `Assets/` 树 SHA 未变 |
| `projectSettingsModified = false` / `dependenciesModified = false` | ✅ 正确 | 对应树 SHA 未变 |
| `b1b2r1HistoryModified = true` | ❌ **假阳性** | 判据把本批自身 601 个新增文件计入"历史修改" |

因此两个字段并非描述同一事实的矛盾，而是**一个字段正确、另一个字段的判据/命名错误**。
不存在"B1/B2/R1 历史被修改却未计入违规"的情况。

## 5. 处置（遵循历史保护）

1. **保留** `28d9fc529…` 中 `protection.json` 及 R2 全部交付文件原文，不做任何改写、不重新生成、不 amend。
2. 本勘误与 `r2-protection-audit.json` 作为 `SKILL-STATE-01` 的**新增独立证据**提交，供复审时对照。
3. 本批自己的汇总工具使用**带尾斜杠的精确前缀**，并显式排除本批交付目录；
   字段名改为 `historicalDeliveryModified`，使名称与判据一致（见
   `DeliverySkillState01/Evidence/Tools/finalize_evidence.py`）。
4. 不因本勘误重新判定 R2 的任何 `PASS-PLAYER` / `NOT_RUN` 结论。

## 6. 建议给复审方

- R2 的 `PROTECTION_PASS` 可继续采信；`b1b2r1HistoryModified` 应视为无效字段，以
  `protectedViolations=[]` 与本文档的树级核对为准。
- 若希望 R2 交付文档自身也消除歧义，应由**后续独立批次**在 R2 目录下新增勘误文件，
  而不是修改已提交内容——本批未授权、也未执行该操作。
