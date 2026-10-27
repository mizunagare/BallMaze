# PLAYER-02 复跑

只使用获准版本和工程外新拥有者根；先读取远端完整SHA。原任务要求开工等于428c41fa4f82e7a95c3163319384cad668b5ef6b，当时已核对。后续复跑必须明确当前获准SHA，不能把历史基线自动当作最新main，不reset用户工程。

需要现有Unity6000.6.5f1、PowerShell7、已安装.NET SDK和Python；不安装/升级依赖。先保存工作区状态与原始输入哈希。所有命令在仓库根运行。

```powershell
$source = [IO.Path]::GetFullPath('D:/unity/WanxiangGuitu')
$p02 = "$source/ProjectDocs/WanxiangGuitu/DeliveryPlayer02"
$b01 = "$source/ProjectDocs/WanxiangGuitu/DeliveryBuild01"
$root = 'D:/WGP02/' + (Get-Date -Format 'MMdd-HHmmss') + '-' + [guid]::NewGuid().ToString('N').Substring(0,8)
New-Item -ItemType Directory $root | Out-Null
@{kind='PLAYER-02 isolated runtime acceptance';source=$source;root=$root;head=(git rev-parse HEAD);utc=[datetime]::UtcNow.ToString('o')} |
 ConvertTo-Json | Set-Content "$root/owner.json"
$py='C:/Users/guan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$env:PYTHONUTF8='1'
& $py -B "$b01/audit_inputs.py" --source $source --out $root

# 复用仓库内的独立桌面worker，不要求机器上存在历史INPUT-01运行目录。
New-Item -ItemType Directory "$root/HostSource","$root/Host" | Out-Null
Copy-Item "$source/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/NativeProbe/*.cs" "$root/HostSource"
Copy-Item "$source/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/NativeProbe/*.csproj" "$root/HostSource"
dotnet build "$root/HostSource/NativeProbe.csproj" -c Release -o "$root/Host/Worker"
if($LASTEXITCODE){throw 'Worker build failed'}
@{kind='WanxiangGuitu isolated unattended run';source=$source;root="$root/Host";head=(git rev-parse HEAD)} |
 ConvertTo-Json | Set-Content "$root/Host/owner.json"
$worker="$root/Host/Worker/NativeProbe.dll"
& "$b01/Test-Preflight.ps1" -SourceProject $source -TestRoot "$root/Preflight"
& "$b01/Invoke-Diagnostic.ps1" -SourceProject $source -Case Short -TestRoot "$root/R" -Variant Release -WorkerFrom "$root/Host"
if($LASTEXITCODE){throw 'Release build failed; keep root'}
& "$b01/Invoke-Diagnostic.ps1" -SourceProject $source -Case Short -TestRoot "$root/T" -Variant Acceptance -WorkerFrom "$root/Host"
if($LASTEXITCODE){throw 'Acceptance build failed; keep root'}

$story="$root/Story"
foreach($mode in 'Setup','Main','Pending','Committed','Manufacture','Successor') {
 & "$p02/Invoke-P02Case.ps1" -ParentRoot $root -StorageRoot $story -Mode $mode -WorkerPath $worker
 if($LASTEXITCODE){break} # 后续业务依赖跳过；不制造空结果，不强杀，不清理原失败
}
# 独立负例继续运行。Pending/Committed需要已生成真实边界；不足时明确失败，不伪造。
& "$p02/Invoke-P02Catalog.ps1" -ParentRoot $root -StoryRoot $story -WorkerPath $worker
$release=(Get-ChildItem "$root/R" -Directory|Sort-Object Name|Select-Object -Last 1).FullName
$accept=(Get-ChildItem "$root/T" -Directory|Sort-Object Name|Select-Object -Last 1).FullName
New-Item -ItemType Directory "$root/ProductIdentity" | Out-Null
& "$p02/Inspect-P02Build.ps1" -BuildRoot $release -Output "$root/ProductIdentity/proof-Release.json"
& "$p02/Inspect-P02Build.ps1" -BuildRoot $accept -Output "$root/ProductIdentity/proof-Acceptance.json"
& $py -B "$p02/inspect_all_modules.py" --build $release --output "$root/ProductIdentity/all-modules-Release.json"
& $py -B "$p02/inspect_all_modules.py" --build $accept --output "$root/ProductIdentity/all-modules-Acceptance.json"
& "$p02/Invoke-P02Rules.ps1" -ParentRoot $root -BuildRoot $accept -WorkerPath $worker
# 仅在实际完成全链时读快照核账，不能凭退出码推导完成。
& $py -B "$p02/audit_story.py" --story $story --output "$root/ProductIdentity/story-business.json"
```

`Invoke-P02Rules`只在已结束构建的拥有者副本追加Editor专用现有Input01Rules；不是正式Player驱动。先检查项目未占用，拒绝关闭用户Editor。所有Player脚本检查已有Player冲突；冲突则跳过/失败并保留进程，不抢桌面。构建每项1200秒、runtime内部900秒/外部1000秒、relay1020秒、现有规则600秒；超时保留，不强杀。

`Invoke-P02Case`和Catalog的显式WorkerPath必须位于拥有者根、来源匹配；参数不依赖旧worker目录。Build包装器的WorkerFrom指向同来源拥有者Host。驱动仅在新Acceptance副本中注入`.cs.txt`，Release默认不注入；不修改主工程define、asmdef、Build Profile或启动场景。

## 真实运行步骤和输入

- Setup：真实uGUI新游戏指纹竞争拒绝、取消、操作设置、虚拟Esc捕获取消、冲突、Forward UpArrow/Dodge Z/Inventory I、.tmp目录故障、重试、恢复默认草稿取消。
- Main：uGUI新游戏、初始长枪、H准备；独立窗口消息确认出征；虚拟按键/鼠标经运行时控制与命中；采木/石/矿，只有DisplayedE精确匹配才拾取；H渡口扣木2石1、引导/取消/重引导；真实Pending后F5保存、退出。
- Pending：从标题读取原自动档；真实.tmp目录阻挡提交，比较原档/Profile；移除自己的空故障目录，原按钮重试；Committed保存退出。
- Committed：新进程继续核对原Profile/结算，无重复奖励。
- Manufacture：再继续、原按钮确认回营，仓库按真实白装成本取材，uGUI制造白剑，再次森林出征，保存退出。
- Successor：再启动Player，实际继续，比对Profile/Run/region/seed/layout/streams/gear/ledger。

标准新游戏初始物品来自游戏自身，不注入库存。角色仅由键位和鼠标移动；NavMesh只读查路径。低矮石矿依现有教程使用近战。敌人AI、伤害、掉落、背包和经济数值均未改。无领域回调、反射、改结果字段的备用成功路径。

## 发布证据

先确认拥有的Unity/Player全部结束，记录`ProductIdentity/live-owned-processes.json`为空数组，保留其他用户进程。保存worker源及产物哈希后，以新的证据目标运行：

```powershell
& $py -B "$p02/collect_player02.py" --run $root --source $source --evidence '<仓库内新的Evidence/运行目录>'
```

收集器拒绝覆盖已有发布目录、拒绝输入变动和存活拥有者进程；只复制日志、回执、哈希、合成集合及截图，不复制Player、Library、Temp或用户场景内容。追加警告逐条对照、账目和验收表后重新计算manifest。`.gitattributes`对本批Evidence/执行驱动保留真实字节，避免Git换行改写损坏哈希核对。

原生输入/人工/完整性能未执行；PostMessage与虚拟设备、Application.Quit退出不得改名为U16、标题栏关闭或试玩。新的复跑不继承本次31 PASS。D3D12、青色帧、Search、JobTempAlloc仍独立开放，不为了本批重复无因果线索的实验。
