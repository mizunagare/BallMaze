# 失败与未完成历史

所有原始文件保留，成功重跑没有覆盖旧目录。外层进程0只说明退出，不将中断或缺失语义证据变为PASS。

|尝试|实际结果|处理/剩余|
|---|---|---|
|FixedOpen|未启动Unity，缺B06LocalChecks|保留tool-failure-01；补全现有helpers，另跑FixedOpen2|
|FixedEditorProbe|进程0；线程正分配返回0；GC字节未取得|保留probe与profiler.raw；只承认CPU/原始事件数，不承认字节|
|ReadFixedProfile|LoadProfile=false，Deserializer error，后等待无进展|只关闭已核对的隔离Editor，reader-cleanup；不是Player/native验收|
|Cleanup helper --no-restore|NETSDK1004缺assets文件|保留tool-failure-02；源文档目录误生成的两项ignored obj文件核对创建时间/SHA后移入ToolGeneratedRecovery，不删旧文件|
|BaselineEditorProbe|实际exit1，15分钟有界deadline|原exception/log不改；后独立BaselineScoped成功，不覆盖此失败|
|FixedEditorProbe2|工具CS0117：SetProfilingEnabled不可访问；Safe Mode|保存Unity.log与窗口清单；精确自有隐藏对话框普通关闭。exit0只是清理，不是测量成功|
|首两次关闭助手|Add-Type用法错误 / 跨desktop句柄不匹配 / attach failed|没有发送输入；独立新进程附加自有非活动desktop后才发送WM_CLOSE，safe-mode-normal-close2保留|
|BaselinePlayers/PlayerProbe|缺失脚本警告，无probe；普通关闭中断|进程0不能证明运行成功；性能NOT_RUN，根因未确认，不归因游戏|
|AnalyzeInputs / AnalyzeBuild|Python默认GBK解码错误|改工具显式UTF-8，未改输入|
|Protect首次|历史清单schema假定fullPath，KeyError|修工具按已存在path读取，再核验全部2329+889|
|所有build/运行警告|URP stripping、JobTempAlloc等|完整BuildReport/Unity.log保留；未批量修复、未过滤成PASS|

[原始目录](Evidence/Raw/)、[发布清单](Evidence/Raw/manifest.json)。错误命令可由当前聊天工具记录与原始日志核查；部分早期工具源码在本批开发中迭代，未保存逐次完整源码快照，不能宣称每个失败均有冻结源码包。保留的原始错误日志与输入哈希不改写。

CP04-B旧889项哈希一致；原法杖两项历史失败、CP03旧失败及D3D12 UNKNOWN不变。没有新增授权产品修复。
