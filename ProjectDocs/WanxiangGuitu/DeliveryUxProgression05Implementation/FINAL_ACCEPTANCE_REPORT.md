# UX-05 v10 最终验收汇总（R2）

**PASS（UX-05-IMGUI-R2授权范围），等待负责人复审。** 跨局目标历史的既有 R1 功能证据保留；本轮修复两项真实 UI 缺陷并完成原生交互。最终混合、空、未知三条Run均退出0，早期回执与滚动截图缺口已由新Run补齐。未自动取得发布或Git操作权限。

## 当前完成与限制

| 层级 | 结论 |
|---|---|
| [S] 产品实现 | R1 已有六字段历史、128条、单事务、迁移、去重及双 UI；本轮仅修正 AdventureFlow.UI.cs 的非活动 canvas 清理与底层 uGUI 点击穿透 |
| [B] 本轮完整构建 | Acceptance A02、NoDefine A02、Release A02 均退出0；发行回执核对通过，NoDefine/Release 查验收标记0且无 sidecar |
| [P] 本轮实际输入 | IMGUI24次、uGUI24次历程操作成功；最终MIXED-A06、EMPTY-A03、UNKNOWN-A03均退出0；55次操作前台验证并投递 |
| [C] 独立核对 | 17对查询状态六字段/排序/分页一致；查询交互期隔离主档及 Profile 不变；退出既存保存仅改变营地运行快照/世代，历史与收益不变；147条旧 Run、4142个旧文件完整；1504份接手源码/配置仅指定 UI 变化 |
| [H] 未扩展验证 | 多 DPI/分辨率矩阵未执行，本轮实际为DPI96、1280×720；物理断电保持原 NOT_RUN；未将早期不完整Run改为PASS |
| [M] 人工验收 | 未以自动化代替手感、可读性和人工体验判断 |

本轮不重新运行已通过的 Schema/迁移/结算矩阵，不将 R1 旧构建的 Player 证据标成 R2 新 DLL 的全量复测。仅有 UI 文件差异，原数据与结算模块指纹保持。实际产品输入到控件后的变化由原生事件、查询状态和截图共同证明。

## 全部历史和本轮判定

总矩阵159条，106条为严格 PASS；另含 FAIL19、FAIL_LAUNCH1、FAIL_TIMEOUT4、FAIL_DRIVER1、EXPECTED_NEGATIVE_BLOCKED2、PROCESS_CUT_WITNESSED13、SUPPLEMENTAL_STOPPED1、OBSERVED_STARTUP_ONLY2、INCOMPLETE_EVIDENCE5、PASS_INTERACTION_INCOMPLETE_EXIT3、INTERACTION_OBSERVED_AUTOSAVE_ACTIVE1、INCOMPLETE_INPUT_TOOL1。失败、预期拒绝、故障切点和不完整运行不能合并为通过率。

原68条、R1新增79条的逐项分类原样保留，见 [总 Run 矩阵](PLAYER_RUN_MATRIX.csv) 和 [分类复算](UX05-IMGUI-R2/EVIDENCE/run-audit.json)。R2 两项产品失败都有新 Run 复测，不回写原 FAIL。前台守卫拒绝与仪器错误未冒充产品失败。

## 存档与保护

只使用明确指定在本轮 evidence 内的隔离根及历史隔离夹具副本，无真实用户存档访问。所有 ProjectSettings、Packages、Schema、迁移和结算文件相对接手快照未变。既有未提交工作区修改保留，Git Index 为空，分支与 HEAD 未变。未 add、commit、push、merge、rebase、restore、reset 或 clean。

构建身份详见 [总身份表](BUILD_IDENTITY.tsv) 和 [本轮精确身份](UX05-IMGUI-R2/EVIDENCE/final-build-identity.json)。本轮产品 DLL 确实因两项已证明的 UI 缺陷变化；Driver 与产品身份分开记录。

## 停止点

本轮IMGUI交互项、独立复算、历史Run分类、构建身份和保护审计已完成。早期工具前台拒绝、Run误关联、自动保存噪声和缺少退出码均有保留证据及新Run替代关系。最有价值的下一步为负责人复审本交付。停止等待复审，不进入 UX-06 或任何 Git 发布操作。

[R2 详细报告](UX05-IMGUI-R2/REPORT.md) · [最终验收矩阵](ACCEPTANCE.md) · [完整证据索引](EVIDENCE/INDEX.json)
