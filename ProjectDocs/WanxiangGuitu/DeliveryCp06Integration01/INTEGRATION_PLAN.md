# CP06-INTEGRATION-01：集成计划与分支整合方案

> 本文件是 **分支整合方案 + 集成设计**。它先于任何产品改动编写；本批次**不修改任何产品源码**，
> 仅新增 `ProjectDocs` 文档与证据索引。所有结论均可由 `git` 命令在本仓库复现。
>
> 状态定义（沿用全局规则）：`PASS` / `PASS-PLAYER` / `PASS-EDITOR` / `PASS-STATIC` /
> `FAIL` / `NOT_RUN` / `INCOMPLETE`。历史 `FAIL` / `NOT_RUN` / `INCOMPLETE` **原样保留**，
> 本文件不重写旧批次结论。

---

## 0. 本批次目标与边界

| 项目 | 内容 |
|---|---|
| 目标 | 建立**单一、可复现的统一可玩候选版本**，整合七武器、八项扩展技能、森林、古代遗迹、水晶洞窟与 C2.4 Boss |
| 候选分支 | `integration/cp06-playable-candidate`（本文件所在分支） |
| 候选基线 SHA | `e93d6eebc8d8d3e7bee9ffbc056e8781642abad5`（`fix/skill-state-01` 顶端） |
| 是否改动产品 | **否**——本分支相对 `fix/skill-state-01` 仅新增 `ProjectDocs` 文档 |
| 是否合并 `main` | **否**——`main` 已是候选基线的祖先，不移动 `main` 指针 |
| 是否丢弃历史分支 | **否**——所有 35+ 远端分支保留；本批次只**新增**一个集成分支 |
| 是否覆盖历史结论 | **否**——C24 B2/R1/R2、SKILL-STATE-01 的 `FAIL`/`NOT_RUN`/`INCOMPLETE` 原样保留 |

---

## 1. 提交关系审计（本次 `git merge-base --is-ancestor` 实测）

审计命令（节选，可在本仓库复现）：

```bash
TIP=$(git rev-parse fix/skill-state-01)   # e93d6eeb...
for b in main fix/cp06-crystal-warden-b1 fix/cp06-crystal-warden-b2 \
         fix/cp06-crystal-warden-b2-r1 fix/cp06-crystal-warden-b2-r2 \
         feature/cp06-skill-expansion feature/cp06-new-weapons \
         feature/cp06-ancient-ruins feature/cp06-crystal-cavern \
         feature/cp06-crystal-cavern-boss feature/cp06-crystal-cavern-c22 \
         feature/cp06-crystal-cavern-c23; do
  git merge-base --is-ancestor $(git rev-parse $b) $TIP && echo "ANCESTOR : $b"
done
```

### 1.1 被测结果（全部为 `ANCESTOR`）

| 分支 | 完整 HEAD | 与候选的关系 | 承载内容 |
|---|---|---|---|
| `main` | `72db192a527bd256e2ba18cd7ab334d8334051da` | 祖先 | 四武器表现批次（**非** CP06 完成度） |
| `fix/cp06-crystal-warden-b1` | `a013c15aae15e17af6a7596a022f01f56a745c34` | 祖先 | C24 首奖提示/名称修补 + 剩余问题取证 |
| `fix/cp06-crystal-warden-b2` | `98924a34b6df817aa5a979b50439a4515881744b` | 祖先 | 路线只读收益投影 + 晶环实际接触 + C05 证据 |
| `fix/cp06-crystal-warden-b2-r1` | `c388e9b7ecf9b5619a65fac81227eba68f61b832` | 祖先 | 证据关联工具修正 + 同一 Run C05/晶环 |
| `fix/cp06-crystal-warden-b2-r2` | `28d9fc529ba3bc621f0f7e73a183a18fba69f867` | 祖先 | 晶环剩余四项 Player 合同（25/27 PASS + 2 NOT_RUN） |
| `feature/cp06-skill-expansion` | `e1f13446601e4324a67c472eecd3419a6c317e65` | 祖先 | 原四武器各 +2 技能 = **八项扩展技能** |
| `feature/cp06-new-weapons` | `07e47664101b1e4476b675e2b2163ae2ca9f512f` | 祖先 | 双刃/巨剑/镰刀 = **新增三武器**（共七武器） |
| `feature/cp06-ancient-ruins` | `31950f7bbd1f7946157632a52f1efd3854780340` | 祖先 | **古代遗迹** 区域 |
| `feature/cp06-crystal-cavern` | `093d0bfebd33747d4a2b035b22b26a701778a8ca` | 祖先 | **水晶洞窟** 基础 + 森林内容承接 |
| `feature/cp06-crystal-cavern-boss` | `acbfbe3f567f1b0928559741f8370478bec6502c` | 祖先 | **C2.4 晶脊守望者 Boss** |
| `feature/cp06-crystal-cavern-c22` | `35efda203b0b36801139fa2cc80ab7ba895207af` | 祖先 | C22 地下湖双路 + 返回桥 |
| `feature/cp06-crystal-cavern-c23` | `37b25bb641c72deefe4e7e48f19f270711f7fc01` | 祖先 | C23 |

### 1.2 明确排除（非祖先，正确不纳入游戏集成）

| 分支 | 完整 HEAD | 处置 |
|---|---|---|
| `research/cp06-map-tools-03` | `27a1e8159439b5c3d6fa7badcf932f3df7ba2c3c` | **不机械合并**——独立地图工具研究线，与 `fix/skill-state-01` 已分叉；研究成果可查，不冒充正式游戏内容 |

### 1.3 线性 fix 链（逐段 `is-ancestor` 验证通过）

```
main ──► B1 ──► B2 ──► R1 ──► R2 ──► SKILL-STATE-01(tip = 候选基线)
72db192a  a013c15a  98924a34  c388e9b7  28d9fc52     e93d6eeb
```

`main → B1 → B2 → R1 → R2 → fix/skill-state-01` 每一段均通过
`git merge-base --is-ancestor <prev> <next>`，即严格线性，无分叉回退。

---

## 2. 集成基线决策

### 2.1 结论

**最佳（且唯一需要）集成基线 = `fix/skill-state-01` 顶端 `e93d6eebc8d8d3e7bee9ffbc056e8781642abad5`。**

### 2.2 决策依据

1. **包含性已证明**：§1.1 显示所有承载「七武器 / 八技能 / 森林 / 遗迹 / 洞窟 / Boss」的 feature 分支
   均为该 tip 的祖先，因此该 tip 已包含全部所需功能，**无需任何 cherry-pick 或 feature 分支合并**。
2. **避免重复集成**（呼应主计划 §7.1）：主计划明确警示「避免重复 cherry-pick 已包含的技能/武器/地图」。
   由于内容已含于祖先，再合并 feature 分支只会制造无意义的合并提交与潜在冲突。
3. **包含全部定向修复**：C24 收益投影、晶环实际接触、C05 跨半血证据、证据关联工具修正、
   晶环剩余 Player 合同、SKILL-STATE-01 技能生命周期修复，全部位于该 tip 的祖先链上。
4. **研究线正确隔离**：`research/cp06-map-tools-03` 非祖先，自然排除，符合主计划对「研究 ≠ 正式游戏」的要求。
5. **不移动 main**：`main` 已是祖先；候选分支从 `fix/skill-state-01` 派生，不 fast-forward `main`，
   不合并 `main` 进入候选（它本来就在）。

### 2.3 为什么不采用其他候选

| 候选方案 | 否决原因 |
|---|---|
| 从 `main` 重建 | `main` 停留在四武器表现批次，缺少全部 CP06 功能；重建 = 重做已有工作，违反主计划 §1 |
| 从 `feature/cp06-*` 逐个合并 | 内容已含于 `fix/skill-state-01` 祖先；逐个合并产生冗余提交与冲突风险 |
| 从 `research/cp06-map-tools-03` 合并 | 非游戏正式集成线，含开放的内存/原生分配/包版本项，主计划明确不机械合并 |
| 合并 `main` 最新 | `main` 无新 CP06 内容，合并无收益且会移动/混淆基线；本批次禁止 |

---

## 3. 分支整合映射（需求 → 源分支 → 证据）

| 统一候选所需内容 | 来源分支（候选 tip 的祖先） | 历史交付证据目录 |
|---|---|---|
| 基础四武器 + CP05 镜头/辅助瞄准/翻滚 | `main` + `design/cp05-third-person-combat` | `DeliveryB07*`、`DeliveryInput01`、`DeliveryUI01` |
| **八项扩展技能**（原四武器各 +2） | `feature/cp06-skill-expansion` | `DeliveryCP06A`、`DeliverySkillState01` |
| **七武器**（基础四 + 双刃/巨剑/镰刀） | `feature/cp06-new-weapons` | `DeliveryCP06B` |
| **森林** | `main` / `feature/cp05-*` | `DeliveryB07*`、`DeliveryB08` |
| **古代遗迹** | `feature/cp06-ancient-ruins` | `DeliveryAncientRuinsR7` |
| **水晶洞窟** 基础 | `feature/cp06-crystal-cavern` | `DeliveryCrystalCavernC22` |
| C22 地下湖双路 + 返回桥 | `feature/cp06-crystal-cavern-c22` | `DeliveryCrystalCavernC22` |
| C23 | `feature/cp06-crystal-cavern-c23` | 见 `DeliveryCrystalCavernC23*`（如有） |
| **C2.4 Boss + C24**（首奖/晶环/跨半血） | `feature/cp06-crystal-cavern-boss` + fix 链 | `DeliveryCrystalCavernC24B/B1/B2/R1/R2` |
| 技能生命周期修复（符阵/弹体/暂停/读档） | `fix/skill-state-01` | `DeliverySkillState01` |

> 该映射证明：**单一分支 `integration/cp06-playable-candidate` 即同时包含上述全部内容**，
> 而非把多个分支再拼合。

---

## 4. 保护策略（硬约束）

| 保护项 | 措施 | 验证 |
|---|---|---|
| v9 存档格式 | 不修改 `CombatSaveData` / `CombatSaveSystem`；候选相对 `fix/skill-state-01` 仅新增文档 | `git diff --stat fix/skill-state-01 integration/cp06-playable-candidate` 仅含 `ProjectDocs/` |
| 经济 / 掉率 / 随机流 | 不触碰掉落工厂、权重、`Drop`/`Earn`、三随机流 | 同上；C24 B2 已证明查询不写盘/不消耗 RNG |
| 用户文件 / 真实存档 | 不读写 `%USERPROFILE%/AppData/LocalLow/.../万象归途`；不回写本机文件 | 工作树 clean，无用户文件改动 |
| 历史 FAIL / NOT_RUN / INCOMPLETE | 仅引用，不重写旧批次报告 | `DeliveryCrystalCavernC24B2R2`（R2_PARTIAL_OR_NOT_RUN）、`DeliveryCrystalCavernC24B2`（NOT_RUN 项）原样保留 |
| 历史分支 | 不删除、不 force、不 reset | 仅 `git checkout -b` 新增一个分支 |
| `ProjectSettings` / 依赖 / CI | 不改动；Unity 固定 `6000.6.5f1` | 无相关 diff |
| 不合并 main | 候选从 `fix/skill-state-01` 派生，不 fast-forward `main` | `main` SHA 复核不变 |

---

## 5. 实施批次划分（本批次内部分批提交，非跨批）

| 批 | 交付物 | 是否改产品 |
|---|---|---|
| 批 1（本文件 + `EVIDENCE_INDEX.md`） | 集成设计、分支整合方案、包含性证明、证据索引 | 否 |
| 批 2（`INTEGRATION_CANDIDATE.md` + `STATE_DIAGRAM.md`） | 统一候选说明、完整循环状态图 | 否 |
| 批 3（`ACCEPTANCE_MATRIX.md` + `Evidence/PROTECTION_AUDIT.md`） | 验收矩阵、保护审计 | 否 |
| 批 4（`CURRENT_STATUS.md` + `README.md` 顶指针增量） | 入口索引更新 | 否 |
| 末步 | `git push` 独立分支 + `git ls-remote` 复核完整 SHA + 暂停复审 | 否 |

每批单独提交，便于逐批复审；全部完成后推送并核对 SHA。

---

## 6. 退出条件（本批次）

- [x] 提交关系审计完成，基线决策有 `git` 实测支撑
- [x] 候选分支建立于 `e93d6eeb`，工作树无未提交改动丢失
- [ ] 五个交付文档（候选说明 / 状态图 / 集成计划 / 验收矩阵 / 证据索引）齐备
- [ ] 保护审计证明产品零改动
- [ ] 入口文档增量更新
- [ ] 独立分支推送，远端完整 SHA 复核通过
- [ ] 暂停等待复审，**不合并 main、不丢弃任何历史分支**
