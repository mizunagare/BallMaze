# CP06-C2.4-B 晶脊守望者原型交付

本批为带开放项的原型，提交后等待独立复审；不表示正式发行、人工可读性或最终平衡通过。不合并 main，不启动下一地图。

产品基准 `37b25bb641c72deefe4e7e48f19f270711f7fc01`，设计基准 `ed450ccfb6c64973a6e9348767742a18de598f25`，分支 `feature/cp06-crystal-cavern-boss`。交付提交以该文档所在完整 Git 提交及对话回报为准，避免在提交内写入自引用 SHA。本轮重新读取远端 main 为 `72db192a527bd256e2ba18cd7ab334d8334051da`。

## 实际变化

- 独立 C2.4 固定资源、可选支路、前室、战场；原湖岸双路、桥及免费出口保留。内容 `C2.4-CAVERN-1` / revision 10 / generation 13。旧 C2.1–C2.3 使用原资源映射，不在恢复时升级。
- `CrystalCavernBossBrain/Rules`：主动挑战先持久化再启战；晶爪扇扫、晶矢齐射、交叉裂线、空心晶环；半血后在当前攻击恢复完成后转换。实际物理范围、墙体检查及原伤害入口，不由测试注入伤害。
- `CrystalCavernBossRewards`、`AdventureFlow.Bosses`、`CombatEnemy`：专用死亡检查点包含死亡、地面普通掉落、永久首奖回执及营地待领物。写入不确定时比较完整预期快照；不落入通用 Boss 奖励。
- `RuinsSpecialRewards` 注册永久首奖；现有领取、背包容量、拆解与保存事务继续使用。无新增 v9 序列化字段。
- `ForestRegionRuntime.Navigation` 和 `RouteScoring` 按额外授权共用精确 C2.4 版本、稳定 Boss ID 和实际路径暴露判定。不改评分权重。湖岸可能仍有既有晶核精英风险，不能将“Boss 不贡献风险”解释成“所有风险为零”。
- `WorldEventPoint` 接入挑战交互；HUD/SaveCatalog 使用新版本标签；`CrystalCavernAuthoring` 保存新 Prefab、网格和材质。旧内容资源未变。

## 分层结果

完整原始尝试统计见 [run-summary.json](Evidence/run-summary.json)：Editor **185 PASS / 2 FAIL**；非开发测试 Player **1949 PASS / 3 FAIL**。这些计数包含重复的启动/夹具断言，不能当成独立业务用例数量。历史失败没有被成功重跑覆盖。

- Editor：挑战失败不启战、开放/关闭桥返回、贴身剑、肩后杖、两阶段循环和独立进程恢复已有真实结果。保留 Search 内部异常和首次 batch 启动、输入屏障夹具失败。
- 非开发测试 Player：七武器各普攻/default skill 命中，共 14 个请求均有活体生命下降；13 个 Boss 命中/规避样本；5 种近战武器各无遮挡/有障碍配对；完整奖励故障、首奖领取拆解及同档案新 Run 流程。每个运行使用冻结纯包副本加隔离驱动，不能叫无驱动纯发行行为。
- 独立只读矩阵审计 **94 PASS / 8 FAIL**。8 项是严格逐浮点三维初始坐标一致性失败：6 组 Boss 配对、双刃和巨剑的晶柱配对。固定指令位置、平面位置相同，实测 Y 存在落地步进微差；没有事后加容差或删除严格断言。功能命中记录保留，但“逐值完全相同的三维配对”不宣称通过。见 [结果](Evidence/Runs/CombatMatrixAudit1/results.json)。
- 半血扇扫 A2/B2 **INCOMPLETE**：没有足够的同步伤害实例关联和独立恢复结束/转阶段内部顺序事件。按授权不再采样、不用完整击杀反推它通过。
- 无驱动纯发行：BuildReport Succeeded，0 errors、111 warnings；实际 Editor 退出 0；Development=false、Bee 五服务 false、无验收驱动。真实标题绘制及后台关闭后退出 0，合成存档未改。不是原生菜单退出或人工试玩。
- 原生操作、人工体验、最终平衡、有效 GC/GPU 性能：**NOT_RUN**。新增完整战斗矩阵未重复跑 Editor；该层已有结果不外推为新增矩阵通过。

画面复核：PlayerNormalRepeat1/frames/00030.png 可见近身角色淡化、扇形外边界及 Boss；PlayerStaff1/frames/00010.png 可见真实晶柱及杖首关系。但该肩后样本的辅助意图文字仍显示复用角色的“古林狩猎守卫”，与顶部“晶脊守望者”不一致。登记为表现命名开放项，不修改冻结 TargetAssist，也不以截图宣称提示可读性通过。

## 奖励与完整流程

`PlayerRewardBefore2` 为真正 before-publish 写入失败；`PlayerRewardAfter1` 为 after-publish 已写入但确认丢失。两例各有独立新进程复核 Boss、普通地面物品完整数据、首奖回执及待领物。重试不重抽、不双发。

从回营只读基线，经合法容器移动制造无可放入空间，领取失败后新进程确认同一待领物；腾空间、实际领取、实际拆解、再次恢复。这里是目标背包不存在足够连续格，不是宣称每个格子均满；领取到背包的真实 API 无自动仓库转存。

随后 `PlayerNormalRepeat1` 同 profile、新 run，从营地正常走到湖岸、主动挑战、两阶段击杀、真实拾取、免费撤离；出征后没有传送、改血、冻结敌人或注入伤害。首奖 earnedRunId/claimed 回执保持原值，待领区不重现。此局实际新增 **1 件装备、3 铁矿、4 晶石**，与上一局 1/3/5 不混用。`PlayerNormalBankRestore2` 新进程比较完整 Profile；重复结算不改 Profile 或 revision。首次错误要求 CommitSettlement 返回 false 的断言仍保留。

## 构建、保护和限制

冻结包 `I:/WGCombat/C24-1106-A/Phase2PureBuild1/Release`；测试副本、全部原始运行在同一独立根目录下。全文件清单 [release-audit](Evidence/release-audit-Phase2PureBuild1.json)，后验哈希 [frozen-release-recheck](Evidence/frozen-release-recheck.json)。没有因验证驱动变化重建/改写原包。

工作树与隔离构建工程存在 9 个新材质的 `_Color` 导入写回差异，`_BaseColor` 未变；[完整差异](Evidence/material-import-diffs.txt)。记录为构建输入字节差异，**不宣称完整构建语义等同性 PASS**。既有 C1/R7 指纹、GraphicsSettings、像素、JobTempAlloc 等开放项不关闭。Resources.meta 缺少构建前记录，保持 NOT_RUN。

12 个已跟踪产品文件变化均在授权范围，新文件为 Boss 代码与 C24 固定资源。冻结战斗/镜头/输入/旧地图资源、Packages、ProjectSettings 未改。五项用户文件前后 SHA 相同：[保护结果](Evidence/user-files-after.json)。产品差异清单：[protection-final](Evidence/protection-final.json)。

审阅入口：[验收](ACCEPTANCE.md)、[复跑](TESTING.md)、[失败历史](FAILURE_HISTORY.md)、[原始证据索引](Evidence/INDEX.md)。
