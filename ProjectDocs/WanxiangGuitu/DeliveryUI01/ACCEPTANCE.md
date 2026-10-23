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
