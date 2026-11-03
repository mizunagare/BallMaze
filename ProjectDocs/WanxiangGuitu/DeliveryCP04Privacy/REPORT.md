# CP04-PRIVACY：默认拒绝诊断上传调查

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
