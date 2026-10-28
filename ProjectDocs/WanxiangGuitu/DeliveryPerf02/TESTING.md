# PERF-02 复跑

本轮仅ProjectDocs工具/证据，不改产品、场景、ProjectSettings、包或v9；先核对获准完整SHA94dcc009ff971272fc46d8c5b323cbb3251619b5与远端main，若已前进停止，不reset。原PERF01证据只读保留；[冻结口径](METRICS_POLICY.md)先于本轮窗口执行。

需要已安装的Unity6000.6.5f1、PowerShell7、.NET SDK及Python，不安装升级。使用工程外短根；本轮D盘空间不足改用I盘，不能清理用户程序或真实档。请检查所选驱动器有足够构建空间；不复制Library，不并行编译与采样。所有路径先GetFullPath规范化，避免拥有者检查中的斜杠差异。

```powershell
$source=[IO.Path]::GetFullPath('D:/unity/WanxiangGuitu')
$p2="$source/ProjectDocs/WanxiangGuitu/DeliveryPerf02"
$b1="$source/ProjectDocs/WanxiangGuitu/DeliveryBuild01"
$root=[IO.Path]::GetFullPath('I:/WGP2/'+(Get-Date -Format 'MMdd-HHmmss')+'-'+[guid]::NewGuid().ToString('N').Substring(0,6))
New-Item -ItemType Directory $root,"$root/Runtime","$root/Runtime/Cases","$root/Runtime/Attempts","$root/Host","$root/HostSource"|Out-Null
@{kind='PERF-02 isolated capability validation';source=$source;root=$root;head=(git rev-parse HEAD);utc=[datetime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content "$root/owner.json"
@{kind='PLAYER-02 isolated runtime acceptance';source=$source;root="$root/Runtime";parent=$root;purpose='PERF-02'}|ConvertTo-Json|Set-Content "$root/Runtime/owner.json"
Copy-Item "$source/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/NativeProbe/*.cs" "$root/HostSource"
Copy-Item "$source/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/NativeProbe/*.csproj" "$root/HostSource"
dotnet build "$root/HostSource/NativeProbe.csproj" -c Release -o "$root/Host/Worker"
if($LASTEXITCODE){throw 'Worker build failed'}
Copy-Item "$root/Host/Worker" "$root/Runtime/Worker" -Recurse
@{kind='WanxiangGuitu isolated unattended run';source=$source;root="$root/Host"}|ConvertTo-Json|Set-Content "$root/Host/owner.json"
$py='C:/Users/guan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$env:PYTHONUTF8='1'
& $py -B "$b1/audit_inputs.py" --source $source --out $root
foreach($v in 'A','B','C'){
 & "$p2/Invoke-Perf02Build.ps1" -PerfVariant $v -Variant Acceptance -TestRoot "$root/$v" -WorkerFrom "$root/Host"
 if($LASTEXITCODE){throw "Build $v failed; preserve evidence, do not run dependent cases"}
}
& "$p2/Invoke-Perf02Matrix.ps1" -Root $root
# Actual exit/timeout and every case receipt must be read; script exit 0 is not metric availability.
& $py -B "$p2/test_analysis.py"
& $py -B "$p2/analyze_perf02.py" --root $root --output "$root/Analysis"
& $py -B "$source/ProjectDocs/WanxiangGuitu/DeliveryPerf01/verify_inputs.py" --source $source --root $root
& $py -B "$p2/collect_evidence.py" --root $root --output '<新的仓库Evidence/Run目录>'
```

本轮实际复用了已审计Worker2二进制（源文件未变化）；新机器按上述命令从仓库构建，不依赖旧测试目录。实际工具/二进制SHA、每份隔离构建ExecutedTools与profile回执均留证。新包装器复用BUILD01的短路径准备、资源/目录/进程保护、独立桌面和超时函数，仅向自己新副本加入Perf02源码；没有修改旧PERF01工具或默认产品入口。

## 输入与边界

全部是Missing合成目录，真实标题渲染，不创建Profile或Run、不点击Continue/New。预热10秒、窗口60秒，ABC/BCA/CAB各轮换一次；C能力探针×3在前，独立于九个稳态窗口。C-PROBE的已知分配不能当成产品自然GC；临时2×2纹理只在窗口外做实际适配器身份确认，自己的资源/COM引用按明确所有权释放。不给奖励、不修改正例档或业务字段。

A没有逐帧观察对象和Recorder，不能获取内部CPU/GPU分布或逐帧间隔；这些为NOT_RUN。共同边界仅Win32进程CPU/内存、GC0与frameCount；不能用两点平均伪造帧时间分布。B的struct缓冲预分配200000行，窗口内不写字符串/CSV；C保留PERF01完整采样器并加系统sidecar。FTM构建标志A=false、B/C=true，是被测配置差异，不能把三包差值直接称因果或发行包开销。

Native host始终SW_SHOWNOACTIVATE/inputDesktopActive=false；Unity isFocused可为true，两者都记录。不修改快捷键、不用物理Esc、不抢桌面、不强杀。所有构建/进程超时沿原工具保留，不以强杀后的exit或技术中断当正常游戏结果。构建1200秒，Player内部900/外部1000秒，sidecar等待有上限。保存指纹仍由PLAYER02旧入口执行，系统日志放在外层System目录，避免占用被指纹读取的CSV。

## 能力结果分析

`probe-counters.json`是实际名称、category、unit与句柄可用性；`probe-samples.jsonl`含同帧/下一帧/EndOfFrame的Valid/Running/Count/CurrentValue/LastValue、选项和单位。不要把GC Used/Reserved Memory当成GC Alloc，或把GPU字样的CPU等待marker当GPU执行时间。`probe-worker.json`记录不同线程、payload和是否真正完成，API已知正分配仍0时判UNAVAILABLE。

FTM只纳入新timestamp且正值的GPU有效子集，其余保留缺失；原始CSV有全部行。PDH按真实PID记录全部匹配实例、Status/CookedValue/RawValue，WMI以全查询后client PID筛选。读取失败、零用量、设备容量各自独立。DXGI local/nonlocal CurrentUsage只表示当前应用段用量；Budget是OS应用预算，不能称为整张显卡可用容量。必须按实际Unity LUID匹配，多逻辑适配器不靠名称猜测。

`summary.json/CSV`包含每个独立窗口与缺失信息，outliers保存>P99原帧索引，不删除离群行。CPU/GPU/帧间隔/CPU累计时间不是可互相替换的指标。GC次数含驱动/采样器自身影响，不据此归因产品；无硬件预算不宣称性能达标。

## 无损证据与复核

只在全部拥有者进程结束后收集。沿PERF01无损gzip和SHA清单机制，精确去重StorageAfter副本；不上传Player/Library/Temp、用户覆盖层正文或真实档。可用`DeliveryPerf01/restore_raw_evidence.py --archive <本批Run> --output <工程外新分析根>`校验/还原，汇总另设新输出，不能覆盖第一次结果。

所有首轮失败与后续定向诊断见FAILURE_HISTORY及原始目录。原生U16、人工/预算NOT_RUN；D3D12 UNKNOWN、青色帧、Search、JobTempAlloc根因不关闭。完成后固定SHA提交并暂停独立复审。
