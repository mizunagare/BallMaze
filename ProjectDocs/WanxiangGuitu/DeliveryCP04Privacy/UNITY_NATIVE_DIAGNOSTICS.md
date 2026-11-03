# Unity原生诊断：实际6000.6.5f1

## 官方能力与实施方式

6.6文档提供Build Profile的Disabled和Use Project Settings选项；该覆盖按构建生效。[Unity6.6说明](https://docs.unity.com/en-us/engine/6000.6/manual/building-and-publishing/build-settings/build-profiles-reference)

官方另明确：诊断数据不走UnityConsent API，而是项目/构建配置控制。因此不能只设置AnalyticsIntent/AdsIntent=Denied就宣称阻断诊断。[官方授权说明](https://docs.unity.com/en-us/cloud/developer-data/user-consent)

实测Unity6000.6.5f1（3ff58d469c8a），URP/Core17.6.0、Input System1.20.0、uGUI2.6.0。本机枚举BuildProfileEngineDiagnosticsState：Disabled=0、Enabled=1、ProjectSettings=2。只在新隔离项目创建DiagnosticsDisabled.asset：使用与本版本官方UI相同的platformBuildProfile.insightsSettingsContainer字段setter保存Disabled，然后BuildPlayerWithProfileOptions；没有调用UnityConnectSettings setter或EngineDiagnostics全局setter。

[实际API/枚举](Evidence/Raw/profile-api-details.json)、[官方UI setter IL](Evidence/Raw/official-ui-setter-il.json)、[已执行工具](../DeliveryCP04Privacy/Tests/PrivacyBuild.cs.txt)、[Profile资产文本](Evidence/Raw/DisabledBuild/DiagnosticsDisabled.asset.txt)。这不是人工点击UI证据。

## 构建实证

[构建前](Evidence/Raw/DisabledBuild/before-build.json)、[构建后](Evidence/Raw/DisabledBuild/after-build.json)：ProfileState=Disabled；EngineDiagnostics=false、CrashReporting.canUploadReports=false、UnityConnect.enabled=false。

[精确匹配本轮输出的Bee](Evidence/Raw/bee-disabled.json)：Development=false；EnableUnityConnect、EnableInsights、EnableCrashReporting、EnableAnalytics、EnablePerformanceReporting全部false。不能把缺少字段或空集合当关闭，运行器检查五个必需字段。

[UnityConnect文件](Evidence/Raw/DisabledBuild/connect-unchanged.json)：前后SHA `7f2112b8c6ea0885dcc72b312c9726ffcd909f2e89d1eead61889274a4e5d1c0`，相同。未手动把m_Enabled改回false。用户原项目同样未改。

实际构建Succeeded、None、0错96警告；190文件SHA完整记录，纯程序集无CP03/BR2/隐私测试驱动、无UnityEditor引用。[构建](Evidence/Raw/DisabledBuild/build.json)、[文件清单](Evidence/Raw/release-files.json)、[程序集](Evidence/Raw/assembly-audit.json)。诊断Profile是调查候选，不接入仓库产品Assets。

## 实际运行与旁路

只在新合成存储根按正式入口启动，无测试游戏参数、无注入驱动、无按键/点击，私有非活动桌面。不启动诊断上传操作、不故意触发异常或崩溃；按时向自己的窗口发送普通WM_CLOSE，实际退出码单独记录。

[两轮汇总](Evidence/Raw/runtime-summary.json)：exit0、未超时，原生输入和人工状态NOT_RUN。第一轮仅主PID，第二轮增加子进程：实际启动UnityCrashHandler64.exe，构建包中仍存在该文件。这说明Disabled不会简单删除所有崩溃处理二进制；也不能单凭该文件/进程存在断言发生上传。

共13/8次端点快照，主进程与第二轮子进程均无观察到的TCP或UDP本地端点。**不是零发送证明**：不是包/内容采集，短连接、UDP数据、后续异常、子进程更深层/系统级路径均可能不在观测范围。无管理员权限，未改系统防火墙/WFP，也没有声称建立了强制网络沙箱。

运行时CrashHandler所有原生分支、OS错误报告和其他未来SDK自动路径未充分验证，保持UNRESOLVED。源码词法检索没有发现所列网络/UnityConsent调用，只能作为辅助，不能排除引擎native、依赖或系统行为。[源码扫描](Evidence/Raw/product-network-source-scan.json)

## 发行结论

此版本可用官方Profile将本轮标准桥接的上传能力配置关闭。默认Denied目标建议固定该构建策略，不动态恢复原生自动诊断。仍需后续批准的无外传环境及更完整观测；本批不能证明当前所有发行路径符合“无授权绝不发送”。禁止以本轮短测、进程0或m_Enabled=false替代完整隐私验收。

用户项目仍保持原配置；Unity Editor自身许可/包管理等网络行为不属于本轮Player诊断关闭证明，也未擅改用户Editor诊断设置。BR3真实键鼠/独立试玩继续NOT_RUN。
