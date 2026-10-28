# R1复跑

固定获准SHA，先读取远端main、本地与用户修改哈希；不reset。所有路径用新的工程外拥有者根，例如 `I:/WCR1/<唯一时间-ID>`，保护原场景/设置/Recovery与真实存档。不抢桌面、不发送物理Esc、不强杀超时进程。不安装或升级运行时/Unity依赖。

## 准备与构建

1. 根目录owner.json采用现有PLAYER02所有权格式：kind=`PLAYER-02 isolated runtime acceptance`，source是工程绝对路径，root是新根，head记录完整获准SHA。保存1152项Assets/Packages/ProjectSettings输入哈希及全部用户未提交文件哈希。
2. 使用 `Prepare-Tools.ps1 -ParentRoot <新根>`，复用已有NativeProbe源码并仅在子进程句柄信号后、宿主清理前增加native-exit回执。观测器目标与既有工具一致，要求机器上**已经存在**的.NET10；缺少则记阻断，不安装。
3. 现有 `DeliveryBuild01/Invoke-Diagnostic.ps1 -Variant Acceptance -AcceptanceProfile CombatR1 -Case Short -WorkerFrom <根/Host> -SourceProject <工程> -TestRoot <根/T>`。R1 partial与PLAYER02 fork只注入这个隔离副本，正式源Assets不变。构建输入逐项核对并归档完整警告。
4. 纯发行测试使用经过批准的BUILD01短路径发行包，复制到新根/Release。逐文件核对SHA并保留原构建出处。不能把此复制说成本轮重建，也不能把验收构建当纯发行包。

## 前摇保存与恢复

`Invoke-StartupPair.ps1 -ParentRoot <根> -BuildRoot <已结束验收构建目录> -Story <新名>` 复用P02Case与窗口消息relay。Save与Resume是两次实际Player进程，共享的仅是合成存档集合。每次结束都保存独立StorageAfter、日志、游戏回执与Win32实际子进程退出码；失败则跳过依赖阶段。

运行时partial只读查询状态，游戏变更全部通过真实uGUI/虚拟输入消费者。F5不直接调用保存API，未反射内部方法或改最终存档；退出使用测试拥有者Application.Quit，不等待0.4秒截图延迟，保留原产品退出保存回调。不是物理键鼠或标题栏操作。

检查：pending1和Startup仍在、LastReleaseFrame=-1、HP/弹体/物资未改；最终v9文件校验和、修订、来源账和冷却；全新PID恢复同一局；首个恢复帧冷却等于最终退出文件；观察超过完整弹体寿命无重放；实际新攻击仍命中。保存末尾可能再形成退出修订，须以实际退出文件作冷却基准，不拿F5前较早冷却强行匹配。

## 有界关闭诊断

`Invoke-ExitDiagnostic.ps1 -ParentRoot <根> -Case <唯一新名> -ObserverPath <根/Observer/ExitObserver.dll>`。

每个样本事先写协议：标题90秒、退出90秒；确切PID、镜像、创建时间、会话、非活动测试桌面、UnityWndClass。独立工具在WM_CLOSE之前持有Player和宿主句柄，WM_NULL响应、请求排队、窗口销毁、Win32信号/退出码、产品退出审计和PID列表观测分别记录。任何PID缺席都不作为退出码证明。

本轮严格限定三次纯发行启动：首例工具配置错误后仅修复观测工具并结束同一拥有者进程；第二例完整复验；第三例补PID列表观测字段后停止。后续复跑先做工具预检，正常只需新的单样本；出现无新证据的异常不得无限重复。后台WM_CLOSE不冒充物理标题栏或原生U16。

## 直接规则与只读审计

`Invoke-Rules.ps1 -ParentRoot <根> -BuildRoot <已结束验收构建目录>` 运行原188条，测试副本仅增加batch下WorldReady之后的公开隔离初始化，断言不变。Editor控制夹具不替代Player。

`python -B audit_r1.py --root <根> --repo <工程> --out <新的分析目录>` 只读重核原始保存、HP、冷却、双PID/句柄、产品输入和用户保护。本轮最终证据使用Analysis2；不覆盖Analysis1。自定义复跑需保持明确样本命名或在独立副本调整审计路径，不修改游戏数据凑结果。

结束清点本轮拥有者进程；未结束则保留、不清理、不强杀。`collect_r1.py`只发布拥有者根中的文本、原始日志无损压缩、合成集合、哈希和截图，排除Project/Library/Temp/Release/工具二进制，拒绝覆盖已有发布目录。历史COMBAT结果按固定SHA原字节保留。
