# CP06-INTEGRATION-01：统一可玩候选说明

> 本文件定义**单一、可复现的统一可玩候选版本**。它不是新功能实现，而是把已通过定向复审的
> 七武器、八扩展技能、森林、古代遗迹、水晶洞窟与 C2.4 Boss 收口到**一个分支**，
> 并记录其构建身份、启动方式与已知限制。

---

## 1. 候选身份

| 字段 | 值 |
|---|---|
| 候选分支 | `integration/cp06-playable-candidate` |
| 候选完整 SHA | `e93d6eebc8d8d3e7bee9ffbc056e8781642abad5`（`fix/skill-state-01` 顶端） |
| 相对 `fix/skill-state-01` 的产品改动 | **无**——仅新增本目录 `ProjectDocs` 文档 |
| 是否包含全部 feature 分支 | **是**（git 包含性证明见 `EVIDENCE_INDEX.md` §1） |
| 是否合并 `main` | **否**（`main` 已是祖先，不移动其指针） |

---

## 2. 技术栈与构建身份（固定）

| 项 | 值 | 说明 |
|---|---|---|
| Unity | `6000.6.5f1`（`3ff58d469c8a`） | **固定不升级** |
| URP | `17.6.0` | 随 Unity 锁定 |
| Input System | `1.20.0` | 随 Unity 锁定 |
| uGUI | `2.6.0` | 随 Unity 锁定 |
| 纯发行构建 Profile | `Assets/BuildProfiles/WindowsRelease.asset` | `m_Development:0`、Boot=0 验证 |
| 场景链 | `Boot.unity` → `Title.unity` → `ForestRuins.unity` | 标题菜单进入，不绕过 |
| 正式产物 | `Builds/WanxiangGuitu/WanxiangGuitu.exe` | 菜单「万象归途 → 构建 → Windows 正式版」 |
| 存档格式 | **v9**（兼容 v1～v8 链） | `Company Name=DefaultCompany` |
| 存档路径 | `%USERPROFILE%/AppData/LocalLow/DefaultCompany/万象归途/ForestRuins` | 标题目录摘要只读检查 |

> 已验证纯发行构建（继承自 `DeliverySkillState01` A3-2/A3-3）：两次构建 `errors=0`、Boot 验证 `0`；
> 修复前 `PureBuild1` EXE `001aeebf…` / Assembly `3763776a…` 与 R2 逐字一致。候选 tip 源码/资源
> 与 `fix/skill-state-01` 逐字相同，构建身份直接继承。

---

## 3. 启动与入口

1. **标题菜单**：正式 Windows 包默认进入标题。提供「继续 / 新游戏确认 / 读取当前自动档 / 设置 / 退出」。
2. **营地**：进入营地后可选择森林探索或保留的波次测试；靠近四个设施按 `E` 交互。
3. **区域选择 / 出征**：森林、古代遗迹、水晶洞窟（含 C22 地下湖、C23）。
4. **七武器入口**：基础四武器（CP05）+ 双刃 / 巨剑 / 镰刀（`feature/cp06-new-weapons`）。
5. **八扩展技能选择**：原四武器各 +2 槽技能（`feature/cp06-skill-expansion`）；
   注意 CP06-A 明示设计限制——技能选择读取后回槽 0，非存档缺陷。
6. **操作**：WASD 移动、Shift 跑、左键普攻、F 技能、V 切武器、空格翻滚、E 交互拾取、
   H 出口引导撤离、Q 药水、Tab/B 背包、C 角色、R 确认放弃。
7. **存档**：F5/自动存档与下次启动继续原局；新游戏确认后全部重置并归档旧集合。

---

## 4. 完整循环（候选须覆盖）

营地准备 → 出征 → 探索 → 战斗 → Boss → 撤离 → 结算 → 制造 → 再次出征（读档回到营地）。

各阶段证据映射见 [STATE_DIAGRAM.md](STATE_DIAGRAM.md) 与 [ACCEPTANCE_MATRIX.md](ACCEPTANCE_MATRIX.md)。

---

## 5. 包含内容清单（已被候选 tip 包含，无需再合）

- **七武器**：基础四（CP05）+ 双刃、巨剑、镰刀（独立 motor / definitionId / 背包仓库品质接入）。
- **八扩展技能**：原四武器各新增槽 1/2（弓蓄势贯矢/追点连射、法杖余烬符阵/回响连珠等），实际释放与命中衔接已实现。
- **森林**：双 Boss、永久徽章、战斗可读性、新手引导与营地体验。
- **古代遗迹**：区域当前版本业务闭环（`feature/cp06-ancient-ruins` + `DeliveryAncientRuinsR7`）。
- **水晶洞窟**：基础（`feature/cp06-crystal-cavern`）、C22 地下湖双路 + 返回桥、C23。
- **C2.4 Boss**：晶脊守望者，含 C24 首奖、HollowRing 实际受击接触、跨半血阶段证据。
- **技能生命周期修复**：符阵 pending 记录与弹体暂停时钟一致；UI 暂停/死亡/闪避/切武器/卸载生命周期；新进程读档恢复（`fix/skill-state-01`）。

---

## 6. 已知限制（不因本批次关闭）

| 限制 | 状态 | 来源 |
|---|---|---|
| 完整手动循环原生键鼠试玩 | `NOT_RUN` | 各交付 `TESTING.md`；本批次未运行 |
| 独立人工可理解性 / 最终平衡 / 性能 | 开放 | 主计划 §7.2；不在本批次范围 |
| 技能选择回槽 0 持久化 | 设计限制（非缺陷） | `DeliveryCP06A`；是否持久化属独立设计决定 |
| 晶环竖直带（±1.2m）图形化 | 开放 | 现有 2D 指示圆只表达水平环带地面投影 |
| 历史 C02/C04 严格三维起点失败 | 保留 `FAIL` | 不因新容差试验改成 PASS |
| 研究线 `research/cp06-map-tools-03` | 不纳入游戏集成 | 正确排除（非祖先） |

---

## 7. 保护边界（硬约束）

不改 v9 存档格式、经济、掉率、随机流、用户文件、`ProjectSettings`、依赖或 CI；
不合并 `main`、不强推、不丢弃任何历史分支、不覆盖历史 `FAIL`/`NOT_RUN`/`INCOMPLETE`。
产品零改动证明见 [Evidence/PROTECTION_AUDIT.md](Evidence/PROTECTION_AUDIT.md)。
