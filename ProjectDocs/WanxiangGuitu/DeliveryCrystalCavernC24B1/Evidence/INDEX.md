# B.1 原始证据索引

所有相对路径位于本目录。完整来源、字节数和SHA256见 `archive-origin.json`。原始二进制保留本机 `I:/WGCombat/C24B1-1107-A`，不替换B历史纯包。归档不包含Unity缓存或供应商受限源码。

|类别|位置|
|---|---|
|开始基线与产品输入|baseline.json、baseline-inputs.json、user-files-before.json|
|最终保护及冻结纯包|protection-final.json；release-audit-PureBuild1.json（完整193文件，不仅EXE）|
|旧Player提前首奖提示|Runs/BeforeNotice1/notices.tsv、截图、实际进程日志|
|旧Player名称不一致|Runs/BeforeNames1Run/names.tsv、names.png|
|首次写入失败与确认丢失|Runs/b1-first-before-A1、Runs/b1-first-after-A1|
|旧首奖待领／领取／拆解后重复击杀|Runs/RepeatPending1、PrepareClaimed1、RepeatClaimed1、RepeatSalvaged1|
|提示独立审核|Runs/NoticeAudit1/inputs.json、results.json|
|候选名称与旧森林负例|Runs/b1-name-cavern-A1、b1-name-forest-A1|
|C24路线实际UI及评分|Runs/b1-name-cavern-A1/arena-route.json、route-ui.txt、route-ui.png、boss-yield-fields.tsv|
|晶环四组原始释放／Damage／LOS／截图|Runs/b1-ring-inner-A1、outer-A1、band-A1、safe-A1|
|Editor提示／名称／边界独立验证|Runs/Editor-b1-*-A2（八个模式）|
|N02参考与候选六组|Runs/ReferenceForest2、ReferenceRuins2、ReferenceC212、ReferenceC222、ReferenceC23Closed2、ReferenceC23Open2及Candidate对应目录|
|N02第一次及修正工具只读审核|Runs/ScoreComparison1、ScoreComparison2；后者按稳定实体ID，不更改原始输入|
|新纯包构建|Runs/PureBuild1/Unity.log、process.json、Editor命令/退出回执、BuildReceipts|
|新纯包启动与退出|Runs/PureTitle2/pure-runtime.json、entry-audit.jsonl、Player日志与退出回执|
|不完整启动失败|Runs/Editor-b1-first-before-A1、Runs/PureTitle1；FAILURE_HISTORY记载原因|
|编译/观测包来源|Runs/Compilation、player-hashes-*.json；Tools/Driver.cs.txt、ScoreDriver.cs.txt|

process.json不是单独成功依据：逐条断言、真实消息、完整回执、画面和工具审核共同支持各自限定结论。截图为自动化采集，不是原生键鼠或人工试玩。
