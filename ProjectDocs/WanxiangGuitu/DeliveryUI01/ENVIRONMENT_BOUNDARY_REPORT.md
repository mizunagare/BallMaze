# UI-01 独立交互环境与关闭诊断边界（2026-10-24）

开始本地 HEAD、fetch 后 origin/main 均为 `c120d231eebd6bdcabd5aa569e218e424025f336`，无后续提交。既有 `ProjectSettings/ProjectSettings.asset` 修改标记保留，不暂存。本轮不修改产品代码或已有编排，不升级依赖、不启用 CI、不进入 B2～B4/B07。最终 SHA 以本报告所在提交及远端核对为准。

## 新执行与环境阻塞

本轮实际运行只读环境检查与历史证据断言，没有启动 Editor/Player、访问玩家存档、发送输入或创建/切换桌面。可复跑入口为 `Automation/Inspect-InteractiveEnvironment.ps1 -OutputDirectory <全新目录>`；拒绝复用已有目录，不将检查脚本成功当作 U16 通过。

[本轮环境原始结果](Evidence/EnvironmentBoundary/environment.json)：只有 guan 的 console 1 Active，会话检查命令退出0；观察进程也在会话1。HypervisorPresent=false；未发现 vmms/vmcompute、VMware/VirtualBox 管理工具或运行中的虚拟机进程；Sandbox 可执行文件不存在。仅发现 TermService 和 mstsc 客户端。有限本机发现不能证明世界上没有可用远程机器；但现有项目配置与已提供授权中没有独占测试主机、会话租约或可验证的远程执行入口。

**原生 U16 阻塞明确且仍未消除。** 当前唯一交互桌面属于用户工作会话；私有非输入桌面不能满足真实输入验收，也不能擅自激活。没有安全、已授权的独立输入环境，本轮依用户要求停止此部分，不要求用户守候，不操作用户窗口或全局快捷键。即使日后获得独立会话，还需验证输入确实送达及 Canvas/UI 和业务状态确实变化；现有领域接口与截图不能代替这一证据。

## 有边界的 UNKNOWN 复核

[只读证据断言与 SHA256](Evidence/EnvironmentBoundary/artifact-review.json)新执行通过：确认旧 Player 日志顺序为 Input System Shutdown → `Got a UNKNOWN while executing native code` → CodeReloadManager destroyed；同次 pid23856 的实际退出码0、未超时。原始日志和退出回执未修改。[原完整调查](CLOSE_INVESTIGATION.md)保留 quit→before-exit→save、修订80→93及后续进程结束时间。它不是 Editor Search 异常；现有证据仍不能定位某个 OnDestroy、引擎模块或驱动。

旧 D3D12 两次已确认标题栏关闭出现 UNKNOWN；旧 D3D11 干净样本附加过监视器，另一次未附加样本超时且缺退出码。这些对照不足以宣布 D3D12 为根因或 D3D11 为已验证稳定修复。后台 WM_CLOSE 9/9 是不同路径，不能替代真实标题栏关闭。

复核上轮正式 Player 转储摘要：ProcDump rawExit1 经固定签名/SHA、数量与结构校准分类通过，但转储没有异常流6，是终止捕获，未提供旧 UNKNOWN 的因果调用栈。校准证明原始字节 SHA 与绑定值一致。当前 PATH 未找到 cdb/WinDbg/dumpchk；本轮没有取得新的故障瞬间转储或匹配栈。**没有新的可验证诊断方向，因此未追加游戏实验，根因继续 UNRESOLVED。** 不吞异常、不放宽分析器、不改生命周期或默认图形后端。

后续实验门槛：取得专用交互环境及相同构建/合成初始档/真实标题栏关闭步骤，或取得与 UNKNOWN 同次、同时间的异常上下文和可用调用栈。监视器实验独立于未附加对照；仅有模块名单、终止转储或退出0不够。满足门槛前不重复大量相同后台实验。

## 本轮状态（不继承历史 PASS）

| 分项 | 本轮 | 历史保留与含义 |
|---|---|---|
| 环境只读检查、旧证据字节/顺序断言 | PASS | 本轮新执行；不是游戏运行验收 |
| 原生 U16：帮助/路线、E/H、拾取/修复、单次扣费、引导/取消/受击、背包/结算、关闭/恢复 | NOT_RUN（全部） | 无安全独立交互环境；没有输入送达或状态变化新证据 |
| 人工可理解性 | NOT_RUN | 未安排独立人员；自动化不代替 |
| 后台关闭/恢复 | NOT_RUN | 上轮9/9关闭、4/4恢复 PASS 原样保留，本轮未重跑 |
| 真实标题栏关闭 | NOT_RUN | 旧 D3D12 干净关闭 FAIL 保留，未取得新样本 |
| D3D12 UNKNOWN 根因 | UNRESOLVED | 没有新的因果栈或修复证据 |
| ProcDump 捕获、构建、规则/AI/装备等回归、完整 All | NOT_RUN | 上轮结果保留；本轮仅复核证据，不继承执行 PASS |

[本轮独立结果](Evidence/EnvironmentBoundary/results.json)与[上轮完整 All](Evidence/Followup/FinalAll/results.json)分开。历史 **65 PASS / 2 个预期探针 FAIL / 20 NOT_RUN / 1 UNRESOLVED** 不改写；上轮正式 exe SHA256 为 `001aeebfb92718f8b49f0c0e0a03e313c54669552b08e952b2fee3ddd143683a`，本轮未构建或运行该程序。没有新退出码、退出审计、恢复断言或运行截图可交付，不伪装成已重新验证。

## 交付及限制

新增只读检查脚本、独立环境结果/证据断言和本报告，更新报告入口、验收表、复跑说明与索引。没有存档、转储、构建、凭据或缓存上传；旧失败日志及校准证明保持原字节。没有 reset/force push/覆盖用户修改。提交推送后另核对远端完整 SHA，推送不代表复审通过。

U16 与关闭根因仍是阻塞项；不建议将 UI-01 标为完成或进入 B2 验收。本轮交付的是可复核的环境边界，未宣称消除该阻塞。
