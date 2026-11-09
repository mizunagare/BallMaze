# CP06-INTEGRATION-01：保护审计

> 目的：用可复现的 `git` 证据证明本批次**未改动任何受保护对象**，
> 满足「保护 v9、经济、掉落、随机流和用户文件；保留所有历史 FAIL / NOT_RUN / UNRESOLVED」。
>
> 候选基线：`fix/skill-state-01` = `e93d6eebc8d8d3e7bee9ffbc056e8781642abad5`
> 候选分支：`integration/cp06-playable-candidate`

---

## 1. 不变量清单

| 类别 | 受保护对象 | 处置 |
|---|---|---|
| 存档格式 | `Assets/CombatPrototype/CombatSaveData.cs`、`CombatSaveSystem.cs` | 不改 v9 |
| 技能/弹体 | `WeaponSkillExpansion.cs`、`AdventureProjectile.cs`、`AdventureCombat.cs`、`SkillPhysicalEffects.cs` | 仅 SKILL-STATE 既有修复，本批不动 |
| 玩家/装备 | `ThirdPersonHero.cs`、`PlayerHudPresenter.cs`、`AdventureLoadout.cs`、`CombatAim.cs` | 本批不动 |
| 掉落/经济/随机流 | 掉落工厂、`Drop`/`Earn`、评分权重、三随机流 | 本批不动 |
| 工程/配置 | `ProjectSettings/`、`Packages/`、`ProjectSettings/ProjectVersion.txt` | 不升级 Unity/依赖 |
| 用户文件 | `%USERPROFILE%/AppData/LocalLow/DefaultCompany/万象归途/...` 真实存档 | 不读写 |
| 历史分支 | 全部 35+ 远端分支 | 不删除/不 force/不 reset |
| 历史结论 | 各 `Delivery*/` 报告中的 FAIL/NOT_RUN/INCOMPLETE | 仅引用，不重写 |

---

## 2. 实测验证（本批次进行）

### 2.1 工作树变更范围

```bash
git status --porcelain
# 结果：
# ?? ProjectDocs/WanxiangGuitu/DeliveryCp06Integration01/
```

即**唯一新增**是本次集成文档目录，无任何产品/配置/用户文件改动。

### 2.2 产品源码相对基线的差异

```bash
git diff --stat fix/skill-state-01 -- Assets/ ProjectSettings/ Packages/
# 结果：（空）—— 候选相对基线零产品改动
```

### 2.3 完整差异（收尾推送前复核）

收尾推送前将执行：

```bash
git diff --stat fix/skill-state-01 integration/cp06-playable-candidate
```

预期仅包含 `ProjectDocs/WanxiangGuitu/DeliveryCp06Integration01/` 下的文档与
`ProjectDocs/WanxiangGuitu/CURRENT_STATUS.md`、`README.md` 顶部增量指针。
**实际输出将在推送前填入本文件末尾的「收尾复核」一节**，作为最终不可变证据。

---

## 3. 历史结论保护确认

| 历史状态 | 是否保留 | 说明 |
|---|---|---|
| `DeliveryCrystalCavernC24B1` `B1-05` FAIL | 保留 | 不在本批重写 |
| `DeliveryCrystalCavernC24B2R2` 2 NOT_RUN | 保留 | `R2_PARTIAL_OR_NOT_RUN` 不改写 |
| `DeliveryCrystalCavernC24B2` 多项 NOT_RUN | 保留 | 纯发行/原生/人工/平衡/性能 NOT_RUN |
| `DeliverySkillState01` 修复前 `R-4` FAIL（已修复） | 保留 | 负例本身保留 |
| 历史 C02/C04 严格三维起点 FAIL | 保留 | 不因新容差试验改 PASS |
| `WindupNewAudit1` C05 INCOMPLETE | 保留 | B2 只新增定向证据 |

---

## 4. 分支与合并约束

| 约束 | 验证 |
|---|---|
| 不合并 `main` | 候选从 `fix/skill-state-01` 派生；`main` SHA 复核不变 |
| 不丢弃历史分支 | 仅 `git checkout -b` 新增一个分支；无删除/force/reset |
| 无未提交修改丢失 | 开工时工作树 clean；本批只新增文档 |
| 不启用 CI / 不升级依赖 | 无 `ProjectSettings`/`Packages`/`CI` 配置改动 |

---

## 5. 收尾复核（推送前实际 `git diff --stat` 输出）

命令：

```bash
git diff --stat fix/skill-state-01 integration/cp06-playable-candidate
```

实际输出：

```
 ProjectDocs/WanxiangGuitu/CURRENT_STATUS.md        |  24 ++-
 .../DeliveryCp06Integration01/ACCEPTANCE_MATRIX.md |  67 +++++++++
 .../DeliveryCp06Integration01/EVIDENCE_INDEX.md    | 114 +++++++++++++++
 .../Evidence/PROTECTION_AUDIT.md                   |  85 +++++++++++
 .../INTEGRATION_CANDIDATE.md                       |  92 ++++++++++++
 .../DeliveryCp06Integration01/INTEGRATION_PLAN.md  | 162 +++++++++++++++++++++
 .../DeliveryCp06Integration01/STATE_DIAGRAM.md     |  35 +++++
 .../DeliveryCp06Integration01/STATE_DIAGRAM.svg    |  70 ++++++++++
 README.md                                          |   2 +-
 9 files changed, 647 insertions(+), 4 deletions(-)
```

产品源码差异复核（必须为空）：

```bash
git diff --stat fix/skill-state-01 integration/cp06-playable-candidate -- Assets/ ProjectSettings/ Packages/
# 输出：空 → 候选相对基线零产品改动
```

**结论**：候选分支相对 `fix/skill-state-01` 仅新增/修改 `ProjectDocs/` 文档（含两个入口文件顶部增量），
无任何 `Assets/` 源码、`ProjectSettings/` 配置、`Packages/` 依赖或用户文件改动。
v9 / 经济 / 掉落 / 随机流 / 用户文件全部未触碰，保护边界成立。
