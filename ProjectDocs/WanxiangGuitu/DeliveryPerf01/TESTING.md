# PERF-01 复跑与分析

本批是测量与风险分类，不是优化，不清零警告、不改产品数值或v9。首先读取获准远端完整SHA并核对本地；任务书开工实读为`6f2abca5f89fc80fc5d298623eda12f557654b78`。若远端已前进，停止并报告，不reset。不要将下面的历史输入当成最新授权。

使用现有Unity6000.6.5f1、PowerShell7、.NET、Python，不安装升级依赖。仓库根运行。`DeliveryPlayer02/TESTING.md`中的独立Host编译与Preflight沿用；只在工程外新建短路径根。禁止指向LocalLow或真实存档，不激活私有桌面、不发送全局输入、不强杀。

## 创建拥有者根、Host与构建

```powershell
$source=[IO.Path]::GetFullPath('D:/unity/WanxiangGuitu')
$perf="$source/ProjectDocs/WanxiangGuitu/DeliveryPerf01"
$b01="$source/ProjectDocs/WanxiangGuitu/DeliveryBuild01"
$p02="$source/ProjectDocs/WanxiangGuitu/DeliveryPlayer02"
$root='D:/WGPF/'+(Get-Date -Format 'MMdd-HHmmss')+'-'+[guid]::NewGuid().ToString('N').Substring(0,8)
New-Item -ItemType Directory $root | Out-Null
@{kind='PERF-01 isolated measurements';source=$source;root=$root;head=(git rev-parse HEAD);utc=[datetime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content "$root/owner.json"
$runtime="$root/Runtime"
New-Item -ItemType Directory $runtime,"$runtime/Cases","$runtime/Attempts","$root/HostSource","$root/Host"|Out-Null
@{kind='PLAYER-02 isolated runtime acceptance';purpose='PERF-01 measurements';source=$source;root=$runtime;parent=$root;head=(git rev-parse HEAD)}|ConvertTo-Json|Set-Content "$runtime/owner.json"
Copy-Item "$source/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/NativeProbe/*.cs" "$root/HostSource"
Copy-Item "$source/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/NativeProbe/*.csproj" "$root/HostSource"
dotnet build "$root/HostSource/NativeProbe.csproj" -c Release -o "$root/Host/Worker"
if($LASTEXITCODE){throw 'Worker build failed'}
Copy-Item "$root/Host/Worker" "$runtime/Worker" -Recurse
@{kind='WanxiangGuitu isolated unattended run';source=$source;root="$root/Host";head=(git rev-parse HEAD)}|ConvertTo-Json|Set-Content "$root/Host/owner.json"
$py='C:/Users/guan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$env:PYTHONUTF8='1'
& $py -B "$b01/audit_inputs.py" --source $source --out $root
& "$b01/Test-Preflight.ps1" -SourceProject $source -TestRoot "$root/Preflight"
& "$b01/Invoke-Diagnostic.ps1" -SourceProject $source -TestRoot "$root/R" -Case Short -Variant Release -WorkerFrom "$root/Host"
if($LASTEXITCODE){throw 'Release build failed; preserve root'}
& "$b01/Invoke-Diagnostic.ps1" -SourceProject $source -TestRoot "$runtime/T" -Case Short -Variant Acceptance -AcceptanceProfile Perf01 -WorkerFrom "$root/Host"
if($LASTEXITCODE){throw 'Perf build failed; preserve root'}
$release=(Get-ChildItem "$root/R" -Directory|Sort-Object Name|Select-Object -Last 1).FullName
$build=(Get-ChildItem "$runtime/T" -Directory|Sort-Object Name|Select-Object -Last 1).FullName
```

本轮复用相同源码的已编译PLAYER02 Worker，原始DLL SHA见证据；上述命令可从仓库重新编译，不要求保留历史Host。`audit_inputs.py`历史目录不存在时只记录缺失，不伪造历史导入结果。另存CPU/GPU/驱动/内存/电源方案只读信息；禁止为测试修改系统设置。

Release不注入；仅Perf01临时副本收到partial驱动、PerfSampler、PerfScenarios和`enableFrameTimingStats=true`。Editor构建工具不进入Player，测试驱动不依赖UnityEditor。两个产物均BuildOptions.None，但采样配置不同，不能冒称原发行包无观测开销。完整输入清单包含用户覆盖层，只发布哈希，不发布场景或设置正文。

## 运行固定场景

```powershell
& "$perf/Invoke-PerfSuite.ps1" -Root $root -BuildRoot $build
# 无论退出码为何，读取每项结果和原始回执，不以脚本exit 0推导全通过。
& "$p02/Inspect-P02Build.ps1" -BuildRoot $release -Output "$root/proof-Release.json"
& "$p02/Inspect-P02Build.ps1" -BuildRoot $build -Output "$root/proof-Perf.json"
& $py -B "$perf/audit_warnings.py" --source $source --report "$release/Results/build-report-messages.json" --previous "$source/ProjectDocs/WanxiangGuitu/DeliveryPlayer02/Evidence/Run-1027-205135/Build-R/Runs/20261027-205649-Short-45c00e3c/Results/build-report-messages.json" --output "$root/WarningAudit"
```

警告对照参数须先定位仓库内PLAYER02原BuildReport实际路径；找不到即记录BLOCKED，不改用摘要代替原始91条。工具严格比对完整warning文本集合。`inspect_perf_builds.py`中本次三个构建路径是冻结证据路径；新批次应显式更新路径映射后记录工具SHA，不能扫描旧产物冒充新包。

每项使用完整PLAYER02合成集合新副本；不编辑正例save.json。Running固定来自`220103-Successor-bb698c/StorageAfter/WanxiangGuitu`，Camp来自`220035-Pending-19eb2e/StorageAfter/WanxiangGuitu`。这些均是已归档的虚构测试Profile，不是玩家档。入口、装备、布局、来源账、随机状态见fixture-before、快照和完整合成档。

PrepareFerry由实际采集/拾取/修复生成Loop输入；Loop真实撤离Pending→提交Committed→确认回营→取材→制造→新森林Run→F5；成功Loop的后继档成为三次Resume的同一冻结输入。依赖失败则NOT_RUN，不创建替代正例。

标题/营地60秒、移动/采集/普通/精英首领120秒，预热10秒；Loop为真实链可变时长，不伪称180秒稳态；Resume为标题预热后30秒加载和观察。每组3个独立进程。普通/首领是接近、战斗、击败、耗尽后的混合窗口；实际攻击时间单列，不能称120秒持续Boss输出。额外Title关闭采集3次，仅评估额外计时调用，基础驱动/CSV/构建标志仍存在。

输入由已审计虚拟InputSystem/uGUI与非活动私有桌面队列执行，不是原生键鼠。Application.Quit是驱动正常请求，不是标题栏关闭验收。游戏业务状态只由真实运行时代码产生；不反射业务、不给物品、不改HP、不冻结AI、不传送。

Player内部900秒/外部1000秒、构建1200秒、sidecar有界等待。冲突或超时保留进程与证据，不强杀；独立项继续。首轮文件指纹占用和采集模态失败保持原样，`Invoke-PerfRecovery.ps1`是一次有界定向补跑，单独生成recovery结果，不覆盖suite结果。

## 只读汇总、原始数据与复核

必须在拥有的测量Player和构建全部结束后运行，避免分析/压缩负载污染样本：

```powershell
& $py -B "$perf/test_analysis.py"
& $py -B "$perf/audit_import_logs.py" --root $root --output "$root/import-diagnostics.json"
& $py -B "$perf/audit_runtime_logs.py" --root $root --output "$root/runtime-diagnostics.json"
& $py -B "$perf/summarize_perf.py" --root $root --output "$root/AnalysisFinal"
# 收集器要求已完成本次定向补跑；新运行若无补跑，明确生成说明回执后再归档。
& $py -B "$perf/collect_evidence.py" --root $root --output '<新的仓库Evidence/Run目录>'
& $py -B "$perf/restore_raw_evidence.py" --archive '<上一步目录>' --output '<新的工程外分析根>'
```

归档对大CSV/log采用无损gzip（mtime=0）；MANIFEST记录原始与压缩SHA/大小，每行均保留。StorageAfter字节相同副本用精确SHA映射到已归档正本；不同内容全部保留。恢复脚本逐文件校验并还原原始字节，不复制Player二进制、Library或用户覆盖层正文。重新分析优先使用还原根的`Runtime/System/<case>`和唯一案例名对应的退出回执，历史绝对路径只作身份记录；不会回到原路径读取系统数据。`summarize_perf.py`可直接对还原根执行，结果路径另设新目录，不能覆盖历史汇总。

分布采用线性插值P50/P95/P99，记录缺失和离群原始帧索引。只计in_window，原始预热/超时/失败行仍归档。FTM重复timestamp与非正计时不填补；GC分配不可用不是0；CPU主/渲染/GPU/帧间隔分别统计，不互相替代。所有当前结论与限制见REPORT，不宣称性能预算或独立人工验收通过。
