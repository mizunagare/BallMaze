# 失败历史（原始结果不改写）

当前主验证输入冻结在cd820b6363b1df689d9ad639684a5e1f1c04d747。历史结构化probe/rules合计65 FAIL，另有初始基线、作者工具、编译、安全模式超时、反射复现和工具编排错误；因此65不是全部失败的简化总数。每次命令、输入、原始退出码和日志独立保存。

|尝试|实际退出|超时|原始回执|
|---|---:|---|---|
|ArchNavRepro1|1|False|[process](Evidence/ArchNavRepro1/process.json)|
|Authoring1|1|False|[process](Evidence/Authoring1/process.json)|
|Before1|1|False|[process](Evidence/Before1/process.json)|
|CameraCourtyardFixed1|1|False|[process](Evidence/CameraCourtyardFixed1/process.json)|
|CameraFixed1|1|False|[process](Evidence/CameraFixed1/process.json)|
|CameraNavFixed1|1|False|[process](Evidence/CameraNavFixed1/process.json)|
|CameraRepro1|1|False|[process](Evidence/CameraRepro1/process.json)|
|CameraSkirtFixed1|1|False|[process](Evidence/CameraSkirtFixed1/process.json)|
|CameraSlopeFixed1|1|False|[process](Evidence/CameraSlopeFixed1/process.json)|
|CloneRepro1|1|False|[process](Evidence/CloneRepro1/process.json)|
|DeathEditor2|1|False|[process](Evidence/DeathEditor2/process.json)|
|DeathPlayer1|1|False|[process](Evidence/DeathPlayer1/process.json)|
|EliteEditor2|1|False|[process](Evidence/EliteEditor2/process.json)|
|ElitePlayer1|1|False|[process](Evidence/ElitePlayer1/process.json)|
|FrontierEditor1|1|False|[process](Evidence/FrontierEditor1/process.json)|
|FrontierEditor2|1|False|[process](Evidence/FrontierEditor2/process.json)|
|FullEditor2|None|True|[process](Evidence/FullEditor2/process.json)|
|FullEditor3|1|False|[process](Evidence/FullEditor3/process.json)|
|FullEditor4|1|False|[process](Evidence/FullEditor4/process.json)|
|GuardianAssets1|1|False|[process](Evidence/GuardianAssets1/process.json)|
|RulesFull9|1|False|[process](Evidence/RulesFull9/process.json)|
|SealPhysicsRepro1|1|False|[process](Evidence/SealPhysicsRepro1/process.json)|
|TransactionRepro1|1|False|[process](Evidence/TransactionRepro1/process.json)|
|WeaponEditorBow1|1|False|[process](Evidence/WeaponEditorBow1/process.json)|
|WeaponEditorGreat1|1|False|[process](Evidence/WeaponEditorGreat1/process.json)|
|WeaponEditorGreat2|1|False|[process](Evidence/WeaponEditorGreat2/process.json)|
|WeaponEditorScythe1|1|False|[process](Evidence/WeaponEditorScythe1/process.json)|
|WeaponEditorScythe2|1|False|[process](Evidence/WeaponEditorScythe2/process.json)|
|WeaponEditorSpear1|1|False|[process](Evidence/WeaponEditorSpear1/process.json)|
|WeaponEditorStaff1|1|False|[process](Evidence/WeaponEditorStaff1/process.json)|
|WeaponEditorTwin1|1|False|[process](Evidence/WeaponEditorTwin1/process.json)|
|WeaponEditorTwin2|1|False|[process](Evidence/WeaponEditorTwin2/process.json)|
|WeaponPlayerBow1|1|False|[process](Evidence/WeaponPlayerBow1/process.json)|
|WeaponPlayerGreat1|1|False|[process](Evidence/WeaponPlayerGreat1/process.json)|
|WeaponPlayerGreat2|1|False|[process](Evidence/WeaponPlayerGreat2/process.json)|
|WeaponPlayerScythe1|1|False|[process](Evidence/WeaponPlayerScythe1/process.json)|
|WeaponPlayerScythe2|1|False|[process](Evidence/WeaponPlayerScythe2/process.json)|
|WeaponPlayerSpear1|1|False|[process](Evidence/WeaponPlayerSpear1/process.json)|
|WeaponPlayerStaff1|1|False|[process](Evidence/WeaponPlayerStaff1/process.json)|
|WeaponPlayerTwin1|1|False|[process](Evidence/WeaponPlayerTwin1/process.json)|
|WeaponPlayerTwin2|1|False|[process](Evidence/WeaponPlayerTwin2/process.json)|

## 定位和处理

- Before1：产品基线尚无新接口的3项预期失败，不是完成证据。Authoring1的var多声明CS0819、GuardianAssets1资源路径错误及RulesFull9诊断变量名CS0103均保留编译/工具失败。
- FrontierEditor1/CloneRepro1：实际Unity JSON克隆将null内联ForestTerrain变成默认对象，导致新地图出征保存拒绝。改用严格可验证的空规范标记；没有改旧森林生成器或全局序列化。
- FrontierEditor2/FullEditor3：门互动夹具距离/门口占用不合法，调整为正常接近位置，不降低距离或关闭占用检查。FullEditor4确认北侧实际门板遮挡自己的控制点，产品仅允许自己的门板作为该控制点接触；其他墙体不忽略。
- FullEditor1误用仍为stage3的实验输入，虽26 PASS不能冒充五区验证。FullEditor2因Scene句柄隐式转换CS0619进入安全模式，保留原timeout/null退出；外部owned-only正常Quit清理不改写原失败，也不宣称原生Player通过。SafeModeWorker首次编译失败及后续构建、清理回执均保留。
- TransactionRepro1：发布后IOException磁盘revision5而live4。以完整规范化状态和修订绑定确认发布并同步Published；发布前相同旧快照才允许回滚，否则保留读取屏障。Editor/Player真实故障注入重跑通过。
- SealPhysicsRepro1：原导航阻挡掩盖实际封石间隙，真实CapsuleCast暴露。修正新封石中心，保留碰撞。
- CameraRepro1→CameraFixed1/ArchNavRepro1→CameraNavFixed1→CameraSkirtFixed1→CameraSlopeFixed1→CameraCourtyardFixed1：分别保留入口相机卡住、漏收集事件底座碰撞、地下Terrain/墙/柱净空试验。CameraColumnFixed1旧9m宽阈值不能证明正确跟随；最终增加SafePivot/arm一致性，FullEditorFinal1/FullPlayer1三处误差均0。只改新地图空间与资产，不改CP05相机或碰撞开关。
- 第一轮非剑武器与精英夹具装备失败却继续当前武器，全部原FAIL保留，后续战斗行不计入目标武器覆盖。第二轮新三武器装备失败立即停止；证实营地尚未走动时正常业务拒绝关闭背包。第三轮使用Camp.Explore、真实存取/拾取/装备，身份确认后才作战，不直接写库存或上下文。
- DeathEditor2/DeathPlayer1逐帧min漏采8→0，原FAIL不改。原始Health事件已证实真实致死；修正版直接绑定>0→0真实事件并要求实际Dead/Pending，Editor/Player重跑通过。
- 首次程序集审计JSON为PASS，但外层错误地读取未由本地PS脚本设置的LASTEXITCODE而报错；保留assembly-audit-1。改为独立pwsh实际退出，assembly-final-1/2/3通过，无删除检查或扩大白名单。
- GC正分配65536校准返回0：NOT_RUN，不解释为零分配。GPU没有本负载校准：NOT_RUN。JobTempAlloc及Editor.Search异常原日志、警告索引保留，未归因产品或修Unity/供应商源码。

旧CP06C1-1104-A未完成尝试在PriorWork及PriorUnfinished哈希索引保留；原目录未覆盖。已有地图工具/CP04/CP05/CP06历史分支未改写。所有本轮输出唯一根I:/WGCombat/C1-1105-A；源日志只压缩/脱敏发布，原始SHA与发布SHA均在Evidence/manifest.json，原文件仍在本机。

文档更新脚本一次路径变量复用导致FileNotFoundError/exit1，未写产品或父目录文档，修正固定根后完成；见Evidence/doc-generation-attempt1.txt。新辅助专项无新增FAIL。

通用git diff --check对本批按原始字节保留的CRLF记录返回2；原输出保留diff-check-raw.txt。仅源码按明确cr-at-eol及正常空白检查返回0，未为消除lint改写原始记录或降低游戏断言。
