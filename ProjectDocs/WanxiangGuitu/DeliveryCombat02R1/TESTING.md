# COMBAT02-R1 复跑

本轮仅文档目录内的隔离Editor诊断；不能作为正常AI、正式Player、原生键鼠或人工。不要升级、启动CI、访问真实档、关闭用户程序或强杀。

## 准备

新建I:/WGCombat/<唯一名称>，owner.json写入本项目基线与用途；记录用户五文件SHA、旧四失败/aggregate SHA和产品输入SHA。用DeliveryUI01/Invoke-Rules.ps1 -SourceProject <repo> -WorkProject <root>/P/Project -ArtifactsRoot <root>/Prepare -PrepareOnly，复用现有准备器。可只读复制已经退出的旧隔离工程Library缓存，禁止复用占用目录；不复制旧玩家档。不要改原C2拥有者根。

将本批Tests/C02R1Trace.cs.txt、C02R1Preflight.cs.txt复制到副本Assets/CombatPrototype/Editor/B06LocalChecks；B07RulesObserved.cs.txt复制为B07Rules.cs。先用原DeliveryCombat02/Invoke-Combat02.ps1 -Project <clone> -Output <root>/Compile -Method C02R1Preflight.Run做batch编译预检。这个预检不进入Play，不计业务样本；编译失败先修工具，避免非batch停在Safe Mode。

## 对照

```powershell
./ProjectDocs/WanxiangGuitu/DeliveryCombat02R1/Invoke-Diagnostic.ps1 -Project <clone> -RunRoot <root> -Phase Observed
./ProjectDocs/WanxiangGuitu/DeliveryCombat02R1/Invoke-Diagnostic.ps1 -Project <clone> -RunRoot <root> -Phase Fixed -ReadyGate
python -B ./ProjectDocs/WanxiangGuitu/DeliveryCombat02R1/Analyze-Diagnostic.py --root <root>
```

每阶段3个独立进程，每个独立空Stores/01～03。复用原Invoke-Checks/Step/NativeProbe；使用原非batch命令和B07Rules.Run。通过已有Editor seed入口在真实Depart前选择975140455，不能改Run ID、最终存档或Boss。每次复制并冻结实际C#测试源，记录命令、PID、start/end、exit/timeout。未就绪Observed预期3个exit1，脚本总体exit1；Fixed预期3个exit0。不能因预期复现而把原始FAIL改成PASS。

源码方法deadline360秒、进程外600秒均不变。若进程仍活着，保留并阻止复用该副本，不能强杀后继续伪造正常退出。只创建独立不激活桌面，不发送物理Esc、改快捷键或抢用户窗口。既有WorkerPath可参数化，缺失则阻断，不退回用户桌面。

观察器记录完整snapshots/scene events/exception stack、两个磁盘封装、实际实例EntityId和raw scene handle、初始化引用、数组与场景对象。保存hook只观察并记录调用栈，不触发保存、不恢复随机。归档时必须同时保留before/after片段、原全量jsonl和原堆栈。42条分析检查不等于业务规则测试数。

## 发布证据

Collect-Evidence.py --root <root> --repository <repo> --compiler-root <可选编译失败根>。需要已有绑定清单；不得对旧证据目录写入。日志/jsonl以gz发布，仅脱敏凭据值，原始/发布SHA各自记录；原字节文件留在拥有者根。源码/命令/退出回执和合成存档均独立归档。Evidence/.gitattributes禁止证据字节换行转换，提交前校验index/LFS oid对manifest。

本轮实用根B为I:/WGCombat/R1-1028-B，初版Observed直接在根的Runs/Stores下（分析器兼容），Fixed在根的Fixed下；A仅编译失败历史。缓存PDB的旧C2路径不是实际运行目录，需结合PID/命令/SavePath与产品DLL哈希判断。

原编译失败副本A留在Safe Mode，PID93960，超时后仍未观察到退出。关闭请求因无可用主窗/身份校验未通过而停止；不激活桌面、不强杀。该进程不算一个已执行业务复现，也不算退出PASS。


## 共用入口回归

最终B07RulesStable.cs.txt不包含观察器或固定seed：非batch等待默认启动就绪；batch按产品原合同自行显式初始化，避免无限等待产品刻意跳过的Start。旧DeliveryB07/Tests/B07Rules.cs.txt保留。DeliveryUI01/Invoke-Rules.ps1在旧测试复制完成后仅将Stable复制为副本B07Rules.cs，不改变Methods列表、退出传播或超时。

Invoke-Diagnostic.ps1 -Phase Integrated -StableFixture运行该最终普通夹具3个非batch进程；可用既有DeliveryUX02/Invoke-UX02.ps1 -Project <clone> -Output <new>/Batch -StorageRoot <new>/Batch/Store -Batch -Method B07Rules.Run补batch兼容（先显式注入Stable，旧包装器不替换B07规则）。相同时限600秒，不强杀；本轮1次batch通过。PrepareOnly在独立新目录验证注入SHA相同，不启动Unity、不冒称业务运行。
