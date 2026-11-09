# CP06-INTEGRATION-01：证据索引

> 本索引列出支撑「统一可玩候选」的所有证据来源：**git 包含性证明**、**历史交付目录**、
> **保护哈希**与**构建身份**。所有历史 `FAIL` / `NOT_RUN` / `INCOMPLETE` 以链接指向原报告，
> 不在此重写其结论。

---

## 1. Git 包含性证明（候选 tip 已包含全部所需功能）

**候选分支**：`integration/cp06-playable-candidate`
**候选基线**：`e93d6eebc8d8d3e7bee9ffbc056e8781642abad5`（`fix/skill-state-01` 顶端）

下列命令在本仓库可复现（本次审计实测，全部为 `ANCESTOR`）：

```bash
TIP=e93d6eebc8d8d3e7bee9ffbc056e8781642abad5
for b in \
  main \
  fix/cp06-crystal-warden-b1 fix/cp06-crystal-warden-b2 \
  fix/cp06-crystal-warden-b2-r1 fix/cp06-crystal-warden-b2-r2 \
  feature/cp06-skill-expansion feature/cp06-new-weapons \
  feature/cp06-ancient-ruins feature/cp06-crystal-cavern \
  feature/cp06-crystal-cavern-boss feature/cp06-crystal-cavern-c22 \
  feature/cp06-crystal-cavern-c23 ; do
  git merge-base --is-ancestor $(git rev-parse $b) $TIP && echo "ANCESTOR : $b"
done
# 唯一非祖先（正确排除）：research/cp06-map-tools-03 (27a1e815...)
```

| 断言 | 结果 |
|---|---|
| 上述 12 个分支均为候选 tip 的祖先 | **成立（本次实测）** |
| `research/cp06-map-tools-03` 为候选 tip 的祖先 | **不成立 → 正确排除** |
| 线性链 `main→B1→B2→R1→R2→SKILL-STATE-01` 逐段 `is-ancestor` | **成立（本次实测）** |
| 候选相对 `fix/skill-state-01` 仅新增 `ProjectDocs/` | 见 `Evidence/PROTECTION_AUDIT.md`（`git diff --stat`） |

**结论**：单一分支 `integration/cp06-playable-candidate` 已同时包含七武器、八技能、森林、遗迹、
水晶洞窟与 C2.4 Boss，**无需任何 feature 分支合并或 cherry-pick**。

---

## 2. 历史交付目录索引（按内容域）

### 2.1 武器与技能

| 目录 | 内容 | 关键结论（原样保留） |
|---|---|---|
| `DeliveryCP06A/` | 八项扩展技能（弓蓄势贯矢/追点连射、法杖余烬符阵/回响连珠等） | 技能释放/命中衔接已实现 |
| `DeliveryCP06B/` | 七武器（基础四 + 双刃/巨剑/镰刀）独立 motor、definitionId、背包/仓库/品质接入 | 独立追加掉落已授权，旧随机流不变 |
| `DeliverySkillState01/` | 法杖符阵 pending 记录与弹体暂停时钟一致性；UI 暂停/死亡/闪避/切武器/卸载生命周期；新进程读档恢复 | 修复前 `R-4` FAIL-PLAYER（UI-only 4s 负例）→ 修复后 `13/14 PASS-PLAYER + 1 NOT_RUN`；纯发行构建 `errors=0`、Boot=0 |

### 2.2 区域内容

| 目录 | 内容 | 关键结论（原样保留） |
|---|---|---|
| `DeliveryB07*/` | 森林双 Boss、永久徽章、战斗可读性 | 首领预警/半透明已实现 |
| `DeliveryB08/` | 新手引导与营地体验 | 木/石/矿采集、免费出口撤离、结算回营制造、再次出征 |
| `DeliveryAncientRuinsR7/` | 古代遗迹及后续图形/构建取证链 | 遗迹区域当前版本业务闭环 |
| `DeliveryCrystalCavernC22/` | 水晶洞窟 C22 地下湖双路 + 返回桥、晶壳/精英、七武器命中、跨进程撤离入仓 | 14 项验收全部 `PASS`（含 C2.1 旧在途档森林/遗迹入口与读取） |

### 2.3 C2.4 Boss 与 C24 定向修复链

| 目录 | 内容 | 关键结论（原样保留） |
|---|---|---|
| `DeliveryCrystalCavernC24B/` | C24 首奖提示/名称、收益预测基线 | 路线预测与工厂不一致（F1）已记录 |
| `DeliveryCrystalCavernC24B1/` | B1 首奖/名称修补 + 剩余问题取证 | 路线投影 14/14、晶环 6/6，含 `B1-05` FAIL 原样保留 |
| `DeliveryCrystalCavernC24B2/` | 只读收益投影修复、HollowRing 实际受击接触、C05 跨半血证据 | `B2-01~B2-11` 验收；六份旧布局评分与纯发行/原生/人工 `NOT_RUN` 原样保留 |
| `DeliveryCrystalCavernC24B2R1/` | 证据关联工具修正；同一 Run C05 `10/10 PASS-PLAYER`、晶环 `7/7` | 严格重审 B2「10/10」非同 Run 证明 |
| `DeliveryCrystalCavernC24B2R2/` | 晶环剩余四项 Player 合同（高度/暂停/多Collider/取消） | **`R2_PARTIAL_OR_NOT_RUN`：25/27 PASS-PLAYER + 2 NOT_RUN**；未改产品 |

---

## 3. 保护哈希（不变量）

详见 `Evidence/PROTECTION_AUDIT.md`。核心不变量：

| 不变量 | 证明方式 |
|---|---|
| 候选相对 `fix/skill-state-01` 零产品改动 | `git diff --stat` 仅列 `ProjectDocs/WanxiangGuitu/DeliveryCp06Integration01/` |
| v9 存档格式未变 | `CombatSaveData.cs` / `CombatSaveSystem.cs` 无 diff |
| 经济/掉率/随机流未变 | 掉落工厂、`Drop`/`Earn`、三随机流无 diff |
| 用户文件/真实存档未触碰 | 工作树 clean，无本机存档路径写入 |
| 历史分支全部保留 | `git branch -a` 35+ 分支与 `git ls-remote` 复核一致 |

---

## 4. 构建身份（继承自查基线的已验证构建）

- **Unity 版本**：`6000.6.5f1`（URP 17.6.0、Input System 1.20.0、uGUI 2.6.0），固定不升级。
- **纯发行构建 Profile**：`Assets/BuildProfiles/WindowsRelease.asset`
  - `m_Development: 0`、`m_ConnectProfiler: 0`、`m_AllowDebugging: 0`
  - 场景列表：`Boot.unity` → `Title.unity` → `ForestRuins.unity`（Boot=0 验证通过）
  - 菜单「万象归途 → 构建 → Windows 正式版」产出 `Builds/WanxiangGuitu/WanxiangGuitu.exe`
- **已验证纯发行构建（继承 `DeliverySkillState01` A3-2 / A3-3）**：
  - 两次构建 `errors=0`、Boot 验证 `0`；sidecar 仅注入隔离副本 → `PASS-EDITOR`
  - 修复前 `PureBuild1` EXE `001aeebf…` / Assembly `3763776a…` 与 R2 逐字一致
- **说明**：候选 tip 与 `fix/skill-state-01` 源码/资源逐字相同，故上述构建身份直接继承；
  本批次**不重新发起完整 Unity 构建**（源树未变，重构建不新增验证价值，且耗时巨大）。

---

## 5. 远端 SHA 复核基线（开工/收尾对照）

| 分支 | 完整 HEAD（远端，本次复核） |
|---|---|
| `main` | `72db192a527bd256e2ba18cd7ab334d8334051da` |
| `fix/skill-state-01` | `e93d6eebc8d8d3e7bee9ffbc056e8781642abad5` |
| `fix/cp06-crystal-warden-b2-r2` | `28d9fc529ba3bc621f0f7e73a183a18fba69f867` |
| `feature/cp06-new-weapons` | `07e47664101b1e4476b675e2b2163ae2ca9f512f` |
| `feature/cp06-skill-expansion` | `e1f13446601e4324a67c472eecd3419a6c317e65` |

收尾推送后将以 `git ls-remote origin integration/cp06-playable-candidate` 复核新增分支完整 SHA，
并确认 `main` 与全部历史分支 SHA 未被本批次移动。
