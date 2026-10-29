# WORLD-01 验收

以下 PASS 仅指各行明确层级；不构成独立复审、原生体验或发布验收通过。机器明细：[status.json](Evidence/status.json)、[seed-matrix.csv](Evidence/seed-matrix.csv)。

| ID | 状态 | 范围与证据 |
|---|---|---|
| W01 | PASS | WORLD_STATE_MAP + CONTENT_AUDIT 的 87 行源码/内容审计，逐个实体用途和缺失机制 |
| W02 | PASS | WORLD-F01 有 Boss 核心来源提示修复；Before 真实矛盾、After 一致且只读 |
| W03 | PASS | 三 seed×两独立 Run，六份有效纵切；不同身份、同 seed 同布局、三种拓扑 |
| W04 | PASS | 每份77个内容实体 ID（含POI/节点/遭遇/事件/出口）唯一；恢复身份与状态匹配 |
| W05 | PASS | 520 行实际 NavMesh 路径；资源/事件/出口接近点、Boss/普通出生、路线边、绕行；距离校核和水/岩脊几何复核 |
| W06 | PASS | 同状态重复路线评分一致；Profile/Run/库存/Unity及三随机流不因查询而变 |
| W07 | PASS | 六纵切320条受控断言，真实采集拾取、普通敌启用AI实际攻击击败、一次掉落/宝箱、地面与背包分离 |
| W08 | PASS | 祭坛真实交互、正常选择后重复拒绝、新进程恢复 Used/身份/随机流，10条检查 |
| W09 | PASS | 免费撤离、缺料拒绝、引导、取消、受击、修复渡口一次；后者由新正常AI流程验证 |
| W10 | PASS | Death/Abandon、Pending/Committed、满仓待领取、制造回滚、重复提交、Missing/Corrupt/R1恢复入口新运行 |
| W11 | PASS | 剑枪81边界样本与历史最终几何/命中元组一致；15品质/多目标合同、弓杖34项范围检查；非平衡结论 |
| W12 | PASS | 正常AI三阶段与输入/观测/Boss攻击回归，均新进程exit0无超时，非受控纵切或人工 |
| W13 | PASS | 非开发构建与完整警告；1375输入前后稳定复验、PE排除Editor夹具；不是Player运行 |
| W14 | PASS | 五用户文件、3589历史文件哈希不变；仅一产品提示文件与本批文档/工具/计划提交 |

六份导航路径是实际 Unity NavMesh 查询，不是六次原生玩家自由行走。目标普通敌的 AI 启用，其他敌人冻结、角色受控定位；不能将此层级冒充正常 AI 全场冒险。正常 AI Gather/Resume/FinalResume 独立归档。

## 尚未执行 / 开放

| 项目 | 状态 |
|---|---|
| 本批隔离验收 Player 业务流程 | NOT_RUN |
| 本批纯发行 Player 实际游戏操作 | NOT_RUN |
| 原生 U16 | NOT_RUN |
| 独立人工试玩、可发现性与手感 | NOT_RUN |
| 完整性能预算/动态性能基准 | NOT_RUN |
| 核心提示“仅地面来源/全部耗尽/旧无Boss布局”分支独立运行 | NOT_RUN（源码审查，不冒充活Boss正例覆盖） |
| D3D12 UNKNOWN | UNRESOLVED |
| Editor 青色帧 | UNRESOLVED |
| Editor.Search | UNRESOLVED |
| JobTempAlloc | UNRESOLVED |
| 旧 C15 根因 | UNRESOLVED |

v9 格式和旧布局生成/恢复代码未修改；本批当前v9合成档跨进程通过，不继承旧批次全版本迁移 PASS。状态图、规则通过和构建不替代上述开放层级。失败尝试见 FAILURE_HISTORY；不把历史 FAIL 当当前同样数量的产品缺陷，也不删除它们。
