from pathlib import Path
import csv
p=Path('H:/unity/WanxiangGuitu-CP04/ProjectDocs/WanxiangGuitu/DeliveryCP04Privacy')
(p/'DATA_INVENTORY.md').write_text('''# 数据最小化清单（设计）

未来报告只允许schemaVersion、每报告随机reportId、产品构建SHA/版本、Unity版本、粗粒度平台/图形API、枚举faultCode、脱敏产品栈帧、必要计数和粗粒度发生时间。各字段需在预览中可见且可逐项删除；删除必需字段后不得发送不符合schema的报告。

默认不收集自由异常正文或任意用户文字。报告UUID仅用于该报告去重，不作长期玩家身份。栈只保留产品类/方法；绝对路径、用户名、URL查询、参数值必须移除。脱敏失败、未知字段或预览/发送哈希不一致即拒绝发送。

|数据|处理|
|---|---|
|v9存档正文/备份/来源账/库存|禁止包含，绝不默认附件|
|密码/Token/Cookie/账户凭据|禁止包含，传输认证若未来需要另设安全通道且不记日志|
|个人文件、聊天、桌面、截图/录屏|默认禁止；本方案不提供任意文件附件|
|玩家账户/设备序列号/广告ID/机器名/用户名|不收集、不导出|
|完整Player/Editor日志、minidump/内存快照|默认禁止；可能含秘密或大量无关信息|
|本机IP/完整路径/精准位置|不在报告正文收集；网络服务器自然可见源IP，不能宣称完全匿名|
|临时报告ID和内容哈希|仅报告去重/回执，不关联真实玩家身份|

拟议本地保存范围仅Diagnostics独立目录；原子写、访问权限、容量及保留期限需实现和复审。删除不能越出目录/跟随链接，不能动真实存档。服务端尚不存在，访问控制、保留/删除和接收日志策略均未验证。

## 本批证据的范围

本批使用隔离构建、合成/空白存储根，没有读取真实玩家存档。发布日志会移除凭据值和用户路径标识并记录原/发布SHA；原件只留本机独立根。必要进程PID、构建路径、版本、文件哈希与临时网络观测用于调查溯源，不是拟议游戏上报schema，也不会自动进入未来Uploader。

没有上传Unity安装二进制、真实存档或无关个人文件。原生模块、崩溃助手存在不等于本批已发送诊断；完整网络行为仍UNRESOLVED。
''',encoding='utf8')
(p/'SECURITY_TEST_PLAN.md').write_text('''# 安全验证计划

**真实产品的三个模块未实现，以下产品级用例全部NOT_RUN。** Tests/ConsentSpec.py是无网络、内存fake transport的可执行设计说明，12个模型用例通过只说明该简化模型，不验证UI、磁盘、网络、线程race或服务器。

|编号|必须场景|通过条件（未来产品）|本批产品状态|
|---|---|---|---|
|P01|首次无授权|有效状态Denied，无派发|NOT_RUN|
|P02|用户拒绝|Denied，未预选，无派发|NOT_RUN|
|P03|跳过/关闭|Denied，旧回调/ticket不能放行|NOT_RUN|
|P04|授权存储损坏|Denied，损坏内容不进日志或上传|NOT_RUN|
|P05|撤回|提升epoch、撤销ticket、取消在途，重启仍无自动能力|NOT_RUN|
|P06|旧待发报告但无当前授权|可预览/删除，不扫描后自动上传|NOT_RUN|
|P07|上传失败|不自动重试、不误报Sent、保留本地，需新明确操作|NOT_RUN|
|P08|用户删除|本地删除并阻止旧ticket；远端删除单独回执|NOT_RUN|
|P09|重启|按首版设计有效状态Denied，历史Grant仅展示，必须重新确认|NOT_RUN|
|P10|重复点击|单一Sending事务，唯一服务端幂等键，不重复上传|NOT_RUN|

补充模型控制：内容预览后变化应拒绝；有效会话Grant＋明确发送可调用一次fake transport作为正控制。原始结果[model-results](Evidence/Raw/model-results.json)逐行同时标注modelStatus及productStatus，不能混算。

## 真正实施后需要的独立验证

- 故障注入：授权写/读/原子替换失败，未知schema/字段/enum，policy或endpoint变化，报告目录链接/穿越/过大内容。
- race：撤回发生在确认后、派发前、首块后；删除与发送并发；旧异步回调在新epoch返回。检查实际请求和已发送边界，不承诺收回在途字节。
- 崩溃/重启窗口：发出请求但未收到响应、响应已到但回执保存失败；恢复Unknown而非自动重试，服务端幂等真实验证。
- 数据审查：秘密/路径/凭据诱饵不能进入预览与发送正文；预览字节/hash与发送内容一致；HTTPS校验、重定向和服务端删除/保留策略。
- 真实UI：拒绝/跳过/关闭默认值、可发现的撤回和预览、屏幕阅读及双击，不以回调或AI代替。

任何证实的无授权诊断外传为严重FAIL，立即阻断发行。可疑连接但无载荷归属证据则先阻断/UNRESOLVED调查，不能反向宣布安全。不得通过放宽预期或只看HTTP成功码制造通过。

## 本批原生层实证

官方Disabled Profile构建并实际运行两轮，无主动崩溃。服务输入关闭已验证；主/子进程短时端点未观察到连接不是全部路径通过。崩溃发送/OS路径/真实授权Uploader未测，不在本轮触发未经授权的外传来凑负例。
''',encoding='utf8')
(p/'ACCEPTANCE.md').write_text('''# CP04-PRIVACY 验收

交付是调查和设计，不是隐私功能上线。整体仍有UNRESOLVED/NOT_RUN，不发整体PASS。

|项目|状态|依据|
|---|---|---|
|6000.6.5f1官方Profile Disabled|PASS|[前](Evidence/Raw/DisabledBuild/before-build.json)、[后](Evidence/Raw/DisabledBuild/after-build.json)|
|真实纯发行构建/驱动剔除|PASS|[build](Evidence/Raw/DisabledBuild/build.json)、[程序集](Evidence/Raw/assembly-audit.json)，None/0错96警告|
|Bee五服务关闭|PASS|[bee](Evidence/Raw/bee-disabled.json)，按DestinationPath和必需字段核对|
|UnityConnectSettings未修改|PASS|[前后同SHA](Evidence/Raw/DisabledBuild/connect-unchanged.json)，未手工恢复|
|实际Player启动及普通退出|PASS（进程层）|[两轮运行](Evidence/Raw/runtime-summary.json)，exit0，无超时/强杀|
|所有自动诊断路径无外传|UNRESOLVED|CrashHandler仍运行，无包/载荷级证据且未触发崩溃|
|三个自有模块|设计提案|无产品实现、无真实服务器，不标已验证|
|十个产品级授权/上传负例|NOT_RUN|[安全矩阵](SECURITY_TEST_PLAN.md)|
|12项简化设计模型|PASS（模型层）|[fake结果](Evidence/Raw/model-results.json)，没有真实HTTP|
|数据最小化/撤回/删除端到端|NOT_RUN|设计已写，实际实现和服务端未验证|
|原生输入及独立人工|NOT_RUN|无真人，BR3开放|
|产品/用户/v9保护|PASS|[保护](Evidence/Raw/protection.json)，2329项差异0|

旧BR/BR2失败、未知与测试状态不改写。现有正式构建入口未改，Disabled Profile仅在本批外部研究副本；不能将旧Enabled包当作新默认Denied发布。需要复审后的产品实施与发行接入授权，当前停止等待。
''',encoding='utf8')
(p/'FAILURE_HISTORY.md').write_text('''# 失败与限制记录

本批首次Disabled构建成功，0错误/96警告。未升级、未过滤warning。Unity日志的obsolete、JobTempAlloc等保留，不将其直接归因为产品缺陷。

构建和短时进程退出0只用于对应层；端点快照0不当成0发送证明。发现发行包及实际子进程仍有UnityCrashHandler64，已追加独立子进程观察，保持其他自动路径UNRESOLVED，没有制造崩溃来测试上传。

设计模型通过不能代替真实UI/磁盘/网络/撤回race。所有产品级负例NOT_RUN。没有实现或宣称DiagnosticConsent/Store/Uploader。

没有系统防火墙/WFP网络沙箱，也没有管理员权限；没有执行包级追踪。未进行全系统文件/注册表监控，不承诺Unity引擎缓存/PlayerPrefs的全面隔离证明。真实业务存档/用户产品文件采用明确根和哈希保护。

初始API清单曾生成到工作区；确认与独立根镜像哈希相同后将该任务文件移入独立证据根，未清理其他文件。所有原件独立保存，不覆盖BR3或历史证据。
''',encoding='utf8')
(p/'Evidence').mkdir(exist_ok=True)
(p/'Evidence/INDEX.md').write_text('''# CP04-PRIVACY 证据

独立原件根`I:/WGCombat/CP04PRIVACY-1103-A`。[manifest](Raw/manifest.json)记录源SHA、发布SHA与脱敏；脱敏日志不声称能还原原件，原件留本机。未发布真实存档、用户个人目录或Unity安装二进制。

- [真实BuildReport](Raw/DisabledBuild/build.json)、[Profile资产证据文本](Raw/DisabledBuild/DiagnosticsDisabled.asset.txt)、[构建前](Raw/DisabledBuild/before-build.json)、[构建后](Raw/DisabledBuild/after-build.json)、[UnityConnect不变](Raw/DisabledBuild/connect-unchanged.json)。
- [官方UI对应setter IL](Raw/official-ui-setter-il.json)、[6.6实际枚举/API](Raw/profile-api-details.json)、[最终Bee](Raw/bee-disabled.json)、[190文件SHA](Raw/release-files.json)、[纯程序集](Raw/assembly-audit.json)。
- [第一轮实际运行](Raw/DisabledPlayer/runtime-result.json)、[主进程观测](Raw/DisabledPlayer/endpoint-observations.json)、[第二轮含子进程](Raw/DisabledPlayerChildAudit/endpoint-observations.json)、[分层汇总](Raw/runtime-summary.json)。各目录command、desktop、exit、Player.log.gz保留。所有原生/人工项目NOT_RUN。
- [模型12项](Raw/model-results.json)、[源码网络词法扫描](Raw/product-network-source-scan.json)、[无网络强制沙箱说明](Raw/isolation-capabilities.json)、[文件保护](Raw/protection.json)、[历史分支](Raw/remote-baseline.txt)。

[调查](../UNITY_NATIVE_DIAGNOSTICS.md) · [架构](../CONSENT_ARCHITECTURE.md) · [数据](../DATA_INVENTORY.md) · [负例计划](../SECURITY_TEST_PLAN.md) · [验收](../ACCEPTANCE.md)。仅调查副本创建Profile，仓库产品Assets不变。
''',encoding='utf8')
print('remaining reports written')
