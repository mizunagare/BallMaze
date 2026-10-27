# S2-R1 复跑

固定任务见[归档原文](../Reviews/Stage2_2ca1aac4_REVIEW_AND_S2R1_TASK.md)。复用 `DeliveryB4/Invoke-Directed.ps1`、`DeliveryUI01/Invoke-Rules.ps1`、`Invoke-NormalAI.ps1`、`DeliveryStage2/Invoke-Matrix.ps1` 的既有隔离/私有非活动桌面/命令与退出码/超时框架，没有另建玩家存档或测试调度器。

所有路径必须为新的、工程外、显式拥有的隔离根。不使用真实玩家目录，不强杀超时进程。私有桌面保持非活动，不注入用户桌面；这里的 InputSystem 受控设备是 **Editor 测试输入，不是原生键鼠验收**。

## 离线

```powershell
$env:PYTHONUTF8='1'
$py='C:/Users/guan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
& $py -B ProjectDocs/WanxiangGuitu/DeliveryStage2R1/Tests/Test-Summary.py --output D:/WanxiangValidationRuns/S2R1/NEW-Summary
& $py -B ProjectDocs/WanxiangGuitu/DeliveryStage2/Summarize-Matrix.py --matrix <已结束的拥有者矩阵根> --output <新的根外输出>
```

35 个断言覆盖 R01～R12/R14（多子例），预期非法子进程 exit1 是断言的输入，不是产品失败。必须同时检查断言退出码、结果 JSON 和每条子进程 stderr。不得用测试脚本 exit0 代替阅读结果。

R13 对旧19条用 `--legacy-audit`，需要旧完整原始目录、事务、检查点、进程与阶段断言。只允许读，不补写旧 attempt 或 stage schema。用当前输入不存在的字段直接标明兼容边界。`Historical19Comparison2.json` 记录214个旧新主要值比较，旧原件从未覆盖。新矩阵不使用 legacy 绕过新协议。

## Unity 定向运行

在仓库根，用现有同版本、已结束拥有者的 Worker/ShaderCache：

```powershell
$methods=@('S2R1ObservationProbe.Run','S2R1BoundaryRules.Run',
 'S2R1Fight.PairOrd1','S2R1Fight.PairOrd745','S2R1Fight.PairOrd1132',
 'S2R1Fight.PairLake1','S2R1Fight.PairLake745','S2R1Fight.PairLake1132',
 'S2R1Fight.CoverageOrdinary','S2R1Fight.CoverageLake',
 'S2R1Recovery.OrdinaryStart','S2R1Recovery.OrdinaryResume',
 'S2R1Recovery.LakeStart','S2R1Recovery.LakeResume',
 'Stage2Rules.DamageMetric','Stage2Rules.Builds','B07Combat.Run','B07Interruptions.Run',
 'B07Rules.Run','B07Rules.Resume','B07Rules.PendingResume','B07Rules.CommittedResume',
 'B07Economy.Run','B3StreamRules.Run','T06RegDualWeaponCheck.Run',
 'WGB1Check.Run','WGB1Check.Resume','RouteScoringRules.Run','RouteScoringRules.Resume',
 'WanxiangBuild.ValidateBuild')
& ./ProjectDocs/WanxiangGuitu/DeliveryB4/Invoke-Directed.ps1 `
 -SourceProject D:/unity/WanxiangGuitu -TestRoot D:/WanxiangValidationRuns/S2R1/NEW-Frozen `
 -Methods $methods -WorkerFrom <已审计的拥有者根> -ShaderCacheSource <同版本已结束Project>
```

R1 的渲染/Play 驱动使用非 batch 的既有私有桌面路径；单方法600秒上限，内部探针另有有限截止。Start失败时跳过对应Resume。正式 Build 为 `BuildOptions.None`，该定向入口产物位于 `Rules/Release/`，不是受控带驱动 Player。检查源副本哈希、构建报告、程序集中的测试名剔除；不能把有驱动测试包当发布包。

运行完全结束、`preserved-processes.json=[]` 后：

```powershell
& $py -B ProjectDocs/WanxiangGuitu/DeliveryStage2R1/Collect-CombatEvidence.py --run <运行根> --output <新收集目录>
& $py -B ProjectDocs/WanxiangGuitu/DeliveryStage2R1/Analyze-Combat.py --run <同一根> --output <新分析目录>
& $py -B ProjectDocs/WanxiangGuitu/DeliveryStage2R1/Publish-Evidence.py --run <同一根> --target <新发布目录>
```

收集器仅在真实父进程结束后按事前 attempt.parentMethod 绑定退出码，不改交易或指标。三/四例共享一个 Editor 进程，明确不是每例独立 OS 进程；普通/Boss恢复是独立启动。绑定不得重复覆盖，重复运行必须新根或只读审计已有绑定。分析器逐区组比较，不将 coverage 或预试混入18主矩阵。日志发布复用既有redactor，原件在外部根，仓库不含完整玩家存档/分页/转储/构建/cache。

## 既有完整冒险与新回执协议

使用已准备且无活动 Editor 的拥有者副本，复用其非活动桌面：

```powershell
& ./ProjectDocs/WanxiangGuitu/DeliveryStage2/Invoke-Matrix.ps1 `
 -OwnerRoot <已准备的拥有者根> -IsolationRoot <其内新的Stage2Protocol> `
 -DesktopName WGTest_<该根已有32位ID> -OnlyCase w0-s1-Safety-Gather `
 -WorkerFrom <既有Worker拥有者根>
```

该流程真实采集/拾取→渡口单次收费→撤离→Pending→跨进程→Commit/ACK→取材制造→不同后继森林→第二次进程恢复。新启动协议在启动前登记 attempt/配置/代码/驱动身份，各阶段回执来自实际检查点。测试不得改用旧 schema 回填。

没有改生成/碰撞/NavMesh算法和原Stage2Physics输入。R1新增受控战斗的可选后撤仅拒绝无完整路径的输入；对受影响三 seed/八武器场景实际运行验证。历史100规则seed与20实际seed证据仅引用，不继承为本轮新PASS，不以Python修复为由无差别扩大矩阵。原生、独立人工、完整性能仍NOT_RUN；历史引擎根因仍UNRESOLVED。
