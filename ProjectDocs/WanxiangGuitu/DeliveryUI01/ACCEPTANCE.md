## B2 独立推进授权（2026-10-24）

用户已接受 d7c879b 环境边界，并明确允许推进 [B2](../DeliveryB2/README.md)。这不关闭 UI-01：UNKNOWN 仍 UNRESOLVED，原生 U16 与人工理解仍 NOT_RUN；历史65/2/20/1及环境边界证据保持不变。B2 的规则/正常AI/受控截图不代替原生验收，无新因果线索不重跑关闭诊断。下方旧门禁建议作为历史保留。

## 最新：独立交互环境边界复核

[本轮逐项状态](ENVIRONMENT_BOUNDARY_REPORT.md#本轮状态不继承历史-pass)、[独立结果](Evidence/EnvironmentBoundary/results.json)。本轮环境发现/历史证据断言 PASS；原生 U16 全部操作、人工理解、新后台关闭、新标题栏关闭、新构建/All 均 NOT_RUN；D3D12 根因 UNRESOLVED。未发现安全获授权的独立会话，已停止窗口操作。历史标题栏 FAIL 和上轮 65/2/20/1 不改写，不作为本轮 PASS。

## 2026-10-24 当前收尾复验

本轮基线 `b3b7f6f75602aec127a44cf7fe1e650c8451de98`。[当前收尾报告](FOLLOWUP_REPORT.md)优先于下方历史记录。固定微软签名ProcDump经单份→exit1、双份→exit2、无效PID→-2校准；保留rawExit1且同时校验工具身份、完成数量和转储结构，未知工具/错误码/截断仍FAIL。旧失败不改写。

新根完整All -FullRegression实际结束：65 PASS / 2预期故障探针FAIL / 20 NOT_RUN / 1 UNRESOLVED，非预期FAIL=0。后台退出9/9、恢复4/4通过。完整All执行PASS，整体验收仍UNRESOLVED；旧UNKNOWN未解决，真实标题栏新复现、原生U16和人工理解NOT_RUN。B2未开始。

| 本轮范围 | 状态 |
|---|---|
| ProcDump工具 | PASS（固定签名/SHA和经验计数合同） |
| 游戏关闭异常 | UNRESOLVED |
| 后台关闭/恢复 | PASS（9/9、4/4） |
| 原生U16 | NOT_RUN |
| 人工理解 | NOT_RUN |
| 最终All | 完整执行PASS；整体验收UNRESOLVED |

以下是旧轮记录，不继承为本轮PASS。

## 2026-10-24 无人值守增量验收

| 项 | 本轮状态 | 依据 |
|---|---|---|
| 编排/环境保护 | PASS（已执行路径） | 退出7/超时继续、错误版本拒绝、私有桌面零输入、实际句柄/日志/报告 |
| 定向规则/正常AI/受控UI/独立构建 | PASS | Business 15项、Normal/Resume、92帧、0错52警告；不是全30重跑 |
| 正式Player后台关闭与同局恢复 | PASS | 最终矩阵9/9与4/4；WM_CLOSE非物理点击，旧失败保留 |
| 原生完整U16 | NOT_RUN | 私有桌面不在输入桌面，无可靠原生语义观察，未借用领域PASS |
| F22人工理解 | NOT_RUN | 未安排独立试玩 |
| 辅助监视器汇总 | PASS（传播回归）；真实工具FAIL | 实际ProcDump exit1→入口exit1；FaultMonitor exit7→入口exit1，无关Player分析继续PASS |
| UNKNOWN根因 | UNRESOLVED | 本轮9次未复现，ProcDump终止dump并未提供因果栈 |
| 最新All整条单次修后运行 | NOT_RUN | All已完整执行，但发现漏记辅助exit1；最后审计修复只定向复测，无全All重跑，不能宣称最终全部PASS |

[本轮报告与限制](UNATTENDED_REPORT.md)。UI-01 完整验收仍未完成；下表为旧轮记录，不被上述后台测试覆盖。

# UI-01 收尾验收表

基线 b67320315ea180b97d6ffe96b5cc00a2829065e2；本次只调查关闭并补原生证据。既有30/30、92帧、正常AI、构建结果保留，标明旧轮，未无差别重跑。产品Assets/Packages无变更；原非开发包与源码/资源哈希重新核对一致。**完整验收尚未通过：默认Player关闭仍有UNRESOLVED异常，U16与F22有NOT_RUN。**

| ID | 状态 | 证据与范围 |
| --- | --- | --- |
| F01 干净导入编译 | PASS（既有） | Evidence/CleanVerified；本轮无产品代码变动，重新导入NOT_RUN |
| F02 非开发构建 | PASS（既有，哈希重核） | Evidence/BuildSummary.txt / CloseInvestigation/source-and-build.json；BuildOptions.None，0错误52警告；本轮重新构建NOT_RUN |
| F03 空地 | PASS（既有受控） | ScreensFinal/empty、visual-layout.jsonl |
| F04 状态 | PASS（受控及原生观察） | ScreensFinal；NativeEmpty合成档100血与实际HUD对应 |
| F05 武器图标 | PASS（既有受控） | UI01Rules四武器断言；原生四武器逐一切换NOT_RUN |
| F06 冷却 | PASS（既有受控） | UI01Rules及cooldowns图；原生完整冷却矩阵NOT_RUN |
| F07 E/H不同 | NOT_RUN（原生） | 原受控PASS保留；本次原生夹具尚无不同目标拾取证据 |
| F08 合并/同帧 | PASS（既有受控；原生部分） | 真实虚拟键盘同帧门控；用户原生E修复/H引导取消后费用仅一次；原生同帧双键NOT_RUN |
| F09 过期目标 | PASS（既有） | UI01Rules过期拒绝，不转付费动作 |
| F10 费用 | PASS（原生协助） | NativeEmpty/resume-assertions：带入木2石1→0/0；回执同Run/区域/出口，重启不再扣费；缺料原回归PASS |
| F11 引导/中断 | NOT_RUN（原生完整项） | 用户确认H引导再H取消，运行phase0；原生移动/受击中断未记录，原受控证据保留 |
| F12 通知错误 | PASS（既有受控故障） | save-failed/uncertain图与规则；未操作真实存档 |
| F13 结算 | PASS（既有受控/领域） | Pending/Committed图、B05/B1；本次原生鼠标结算NOT_RUN |
| F14 溢出 | PASS（既有受控） | overflow图、待领取回归 |
| F15 焦点 | NOT_RUN（原生完整项） | 鼠标帮助开关/背包/分类已执行；路线/角色/技能选择/结算原生完整矩阵未执行 |
| F16 分辨率 | PASS（既有受控） | 92帧与4分辨率/3缩放代表组合，不能冒充人工可读性 |
| F17 原生完整流程 | NOT_RUN（部分已执行） | 下表逐步结果；不以原受控截图补齐原生步骤 |
| F18 正常退出 | FAIL（默认D3D12） | NativeEmpty/close1-analysis与DX12Repeat均失败，即使exit0；D3D11首次PASS，第二次超时、晚关闭退出码未取得，不覆盖默认失败，根因UNRESOLVED |
| F19 新进程 | PASS（原生包恢复） | close2-analysis/resume、resume-assertions；同Run/区域/种子/回执/库存/来源账 |
| F20 A1/B1核心 | PASS（既有） | CleanVerified30/30；本轮哈希一致无业务改动，未继承为新一轮运行 |
| F21 单例生命周期 | PASS（既有受控） | UI01Rules恢复/单例；原生多次死亡/回营全部路径NOT_RUN |
| F22 无提示人工理解 | NOT_RUN | 用户按指定步骤协助键盘/关闭，不等于独立可理解性试玩 |

## U16（本轮请求十步）

| 步骤 | 状态 | 实际执行/未完成 |
| --- | --- | --- |
| 1 启动/HUD | PASS | 同一非开发exe，显式隔离，NativeEmpty真实截图与存档 |
| 2 帮助/路线 | NOT_RUN（部分PASS） | 鼠标帮助开关PASS，不触发F1；路线原生未完成 |
| 3 E/H分别拾取/出口 | NOT_RUN | 只有同目标渡口原生记录，不能借用受控dual图标PASS |
| 4 拾取/修复单扣 | NOT_RUN（修复子项PASS） | 用户E修复木2石1且有回执，恢复未重复扣；原生拾取未完成 |
| 5 引导/取消/受击 | NOT_RUN（取消子项PASS） | 用户H开始/H取消已确认且phase0；原生受击中断未完成 |
| 6 背包/角色/穿透 | NOT_RUN（部分PASS） | 鼠标背包开关与素材分类已记录；角色/完整穿透验证未完成 |
| 7 结算确认 | NOT_RUN | 不用API或测试驱动冒充鼠标确认 |
| 8 窗口正常关闭 | PASS（用户协助操作） | 用户确认标题栏×；无强杀，进程句柄记录 |
| 9 干净退出诊断 | FAIL（默认）；D3D11对照单次PASS | exit0/无超时/审计有，但默认日志UNKNOWN；见调查报告 |
| 10 同局新进程 | PASS | Profile/Run/区域/Run种子/布局种子/修复回执/物品ID/材料来源账全相同 |

## 本次未解决

关闭异常UNRESOLVED；未取得完整原生栈/可确认故障模块。自动化焦点激活失败，用户协助的已完成项单列。人工无提示试玩NOT_RUN。建议先补齐这些验收，不进入B2/B3/B4/B07。本次推送不代表复审通过。
