from pathlib import Path
p=Path('H:/unity/WanxiangGuitu-CP04/ProjectDocs/WanxiangGuitu/DeliveryCP04Privacy')
(p/'.gitattributes').write_text('Evidence/** -text whitespace=cr-at-eol\nTests/** -text whitespace=cr-at-eol\n*.ps1 -text whitespace=cr-at-eol\n*.py -text whitespace=cr-at-eol\n')
(p/'.gitignore').write_text('__pycache__/\n*.pyc\n')
(p/'REPORT.md').write_text('''# CP04-PRIVACY：默认拒绝诊断上传调查

用户决策已记录：只有明确同意才允许外部游戏诊断上传；默认Denied，拒绝/跳过/关闭/损坏均Denied，可随时撤回。**本批未实现产品授权UI、报告仓库或上传器，不能宣称该决策已在当前产品全面落地。**

分支`investigate/cp04-privacy-consent`从现有BR3工作基点创建，HEAD起点为BR2 `28a54a2f0554153e96d15202e4228aee3908241a`。本地BR3分支保留在该基点；d8fede51ba719060c1d1f719295ce40bb21768d0是既有BR验收提交，不是已完成的BR3真人记录。产品修复仍cc9，main仍72db192a527bd256e2ba18cd7ab334d8334051da；不合并main。

## 实际完成

|内容|状态|证据边界|
|---|---|---|
|Unity6000.6.5f1官方Build Profile Disabled|PASS|隔离副本创建配置资产；不改仓库产品Assets或用户设置|
|实际非开发构建|PASS|BuildOptions.None，0errors/96warnings，190文件完整SHA清单|
|原生诊断桥配置|PASS|EngineDiagnostics/CrashReporting canUpload/UnityConnect均false；Bee五项全false|
|UnityConnectSettings保护|PASS|隔离副本构建前后SHA也完全相同，没有手工恢复派生字段|
|纯Player两轮实际启动/普通关闭|PASS（进程层）|真实exit0、无超时；无键鼠、无业务/人工验收|
|完全无自动诊断外传|UNRESOLVED|CrashHandler仍启动；端点快照不是抓包或全部路径证明|
|自有三模块设计/数据清单|设计提案|没有产品实现或真实服务器|
|十个产品级安全负例|NOT_RUN|仅离线设计模型12项通过，不冒充产品验证|
|原生输入/人工体验|NOT_RUN|BR3仍开放，无真实操作者证据|

## 关键判断

官方文档明确诊断数据不受UnityConsent的Analytics/Ads授权API控制。因此方案是：原生Diagnostics在发行构建中固定Disabled；未来自有Uploader另行执行“会话有效授权＋逐报告预览确认＋明确发送”。不以用户Grant重新打开原生自动上传。

候选构建通过官方BuildProfile字段和BuildPlayerWithProfileOptions完成，唯一新Unity资产在工程外隔离副本，仓库只归档证据文本。产品Assets/CombatAim、用户ProjectSettings、UnityConnectSettings、依赖和v9均不改。2329项保护文件哈希一致。

两轮纯Player均无输入运行后普通关闭。第一轮13次端点快照；第二轮8次并包括实际UnityCrashHandler64子进程；均未观察到TCP/UDP端点。但没有包级/载荷证据，也未主动触发崩溃，不能证明所有发送路径都关闭。[原生调查](UNITY_NATIVE_DIAGNOSTICS.md)

现有产品正式构建入口未改，不会自动采用这个研究Profile；若以后不用Disabled Profile构建，仍可能沿用原诊断配置。**当前不应据此宣布可按默认Denied策略正式发行。** 后续产品实现、正式Profile接入及完整网络/撤回验证均需另批授权与复审。

[架构](CONSENT_ARCHITECTURE.md) · [数据清单](DATA_INVENTORY.md) · [安全计划](SECURITY_TEST_PLAN.md) · [验收](ACCEPTANCE.md) · [证据](Evidence/INDEX.md)。交付后暂停，不继续BR3真人验收或产品开发。
''',encoding='utf8')
(p/'UNITY_NATIVE_DIAGNOSTICS.md').write_text('''# Unity原生诊断：实际6000.6.5f1

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
''',encoding='utf8')
(p/'CONSENT_ARCHITECTURE.md').write_text('''# 自有诊断架构（设计，未实现）

## 不可变原则

默认Denied；拒绝、跳过、关闭、异常、未知版本或损坏一律Denied。Grant和发送都必须是独立、明确操作；不自动提交旧队列，不因登录、开始游戏、崩溃或重启默认上传。Unity原生诊断固定Disabled，与自有Grant解耦。

## DiagnosticConsent

独立于v9进度、装备/经济及随机流。拟议记录schemaVersion、policyVersion、purpose、endpointOrigin、dataCategoryHash、历史决定和撤回审计；不保存账户凭据。只识别严格枚举，字段缺失/未知/校验失败都拒绝，不进行“true-like”宽松转换。

首版设计选择：**有效授权只在当前进程会话生效，重启仍Denied**；可展示历史决定，但不据此恢复网络能力。这样撤回落盘失败时，不会在下一进程被旧Granted记录反向放行。该选择仍待复审，不把历史Grant预选为本次同意。若以后要求跨进程持续Grant，必须另外解决持久撤回完全写失败的故障模型，不能静默放宽。

Grant须显示目的/类别/服务器/期限，存储成功且读回校验后才开启会话授权；写失败保持Denied。policy、用途、类别或端点变化立即失效。撤回先在内存置Denied、提升epoch、作废所有ticket并取消在途，再持久化；持久化失败必须提示，仍不恢复上传。

## DiagnosticReportStore

独立目录和schema，不迁移/附加v9正文。仅接受固定故障字段，未知字段拒绝；禁止自由附件、完整日志、存档、minidump、凭据或任意个人路径。文件名用每报告UUID，拒绝路径穿越/链接。原子临时写入、验证后替换；读取损坏隔离为不可发送，不复制原文到错误日志。

状态：LocalDraft→Previewed→Ready→Sending→Sent；失败为Failed，结果不确定为Unknown，删除为Deleted。预览后内容变化即作废确认。只有预览的同一规范化字节及哈希可进入Uploader。容量/保留期限是待定产品配置，不新增游戏经济或v9字段。

用户可预览和删除本地报告；删除同时撤销ticket、取消发送，不操作其他目录。已上传副本的服务端删除需明确独立请求及回执；尚无服务器，不能提供假按钮或宣称删除成功。

## DiagnosticUploader

当前没有端点/服务端，默认不可用。未来发送需要：当前Grant且policy/scope匹配＋当前内容哈希匹配＋一次性明确Send ticket＋有效epoch＋未删除且非Sending/Sent/Unknown。UI不自动触发，CLI/旧回调不能当授权。

串行状态机/锁内做最后检查并占用Sending；每次ticket消费一次，连续点击不生成重复请求。服务端以reportId+contentVersion作幂等键；响应丢失/保存回执失败进入Unknown，不自动重试。失败保留本地，重新预览并明确点击才允许新尝试；禁止后台重试。

撤回与发送需共享epoch/cancellation边界并在真正派发及分块前复查。已经进入网络/服务器的字节不能物理收回；必须明确提示在途取消和服务端删除的限制，不能承诺瞬间撤销既有传输。并发、崩溃恢复及真实传输race本批均未验证。

HTTPS正常证书校验，不跨origin重定向，不在报告或日志存Token；若未来需短期传输凭据，单独安全存储并脱敏，不能内嵌长期秘密。IP等传输元数据可能被服务器自然看到，“正文不含IP”不等于完全匿名，预览/说明必须如实表达。

## 迁移与实施门槛

新诊断schema与v9完全分离；旧/未来不识别schema只做Denied，不导入历史隐含授权。不影响游戏、保存、撤离或奖励；诊断失败不能阻断这些路径。所有三个模块均未接入产品，须另批授权、真实产品负例、端到端服务端幂等/删除和独立审核后才可启用。
''',encoding='utf8')
print('reports and architecture written')
