param([Parameter(Mandatory)][string]$Project,[Parameter(Mandatory)][string]$RunRoot,[switch]$PairOnly)
$ErrorActionPreference='Stop'
$Project=[IO.Path]::GetFullPath($Project);$RunRoot=[IO.Path]::GetFullPath($RunRoot)
if(!$Project.StartsWith('I:\WGCombat\',[StringComparison]::OrdinalIgnoreCase) -or !$RunRoot.StartsWith('I:\WGCombat\',[StringComparison]::OrdinalIgnoreCase) -or !(Test-Path "$RunRoot/owner.json")){throw 'Explicit owned isolated project/root required'}
$repo=Split-Path (Split-Path (Split-Path $PSScriptRoot));$pw=(Get-Process -Id $PID).Path
function Idle {if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){throw 'Occupied clone preserved; no process stopped'}}
function Run([string]$Name,[string]$Method,[bool]$Batch=$true,[string]$Storage=''){
 Idle
 $start=[DateTime]::UtcNow.ToString('o')
 if($Batch){& $pw -NoProfile -File "$repo/ProjectDocs/WanxiangGuitu/DeliveryCombat02/Invoke-Combat02.ps1" -Project $Project -Output "$RunRoot/$Name" -Method $Method}
 else{if(!$Storage){$Storage="$RunRoot/$Name-Store"}; & $pw -NoProfile -File "$repo/ProjectDocs/WanxiangGuitu/DeliveryCombat01/Invoke-Checks.ps1" -Project $Project -Output "$RunRoot/$Name" -StorageRoot $Storage -Method $Method}
 $code=$LASTEXITCODE
 @{name=$Name;method=$Method;started=$start;ended=[DateTime]::UtcNow.ToString('o');exitCode=$code}|ConvertTo-Json -Compress|Add-Content "$RunRoot/r1-sequence.jsonl"
 Idle # Timed-out/running children block further use of this clone, never terminate them.
 $snap="$RunRoot/$Name/ExecutedSources";New-Item -ItemType Directory $snap -Force|Out-Null
 foreach($n in 'AdventureFlow.cs','AdventureFlow.UI.cs','CombatSaveSystem.cs'){Copy-Item "$Project/Assets/CombatPrototype/$n" "$snap/$n"}
 foreach($n in 'R1Matrix.cs','R1Migration.cs'){Copy-Item "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/$n" "$snap/$n"}
 return $code
}
Idle
foreach($delivery in 'DeliveryRunloop01','DeliveryRunloop01R1'){
 foreach($f in Get-ChildItem "$repo/ProjectDocs/WanxiangGuitu/$delivery/Tests" -Filter '*.cs.txt'){Copy-Item $f.FullName "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/$($f.BaseName)"}
}
# Same final test against the archived baseline, only in the disposable clone.
$names=@('AdventureFlow.cs','AdventureFlow.UI.cs','CombatSaveSystem.cs')
foreach($n in $names){$lines=& git -C $repo show "d8a6dbd9f205bae96ff8a55e1f34eb6fa5cf7179:Assets/CombatPrototype/$n";if($LASTEXITCODE){throw 'Baseline unavailable'};[IO.File]::WriteAllText("$Project/Assets/CombatPrototype/$n",($lines -join "`n")+"`n")}
$null=Run 'Before06' 'R1Matrix.Run'
foreach($n in $names){Copy-Item "$repo/Assets/CombatPrototype/$n" "$Project/Assets/CombatPrototype/$n"}
$null=Run 'After04' 'R1Matrix.Run'
$null=Run 'Migration03' 'R1Migration.Run'
if($PairOnly){return}
foreach($m in 'RunloopFault.Run','RunloopUncertain.Missing','RunloopUncertain.Corrupt'){$null=Run ($m.Replace('.','-')) $m}
# Existing five-process controlled adventure and independent runtime entity audit.
& $pw -NoProfile -File "$repo/ProjectDocs/WanxiangGuitu/DeliveryRunloop01/Invoke-FrozenCycle.ps1" -Project $Project -RunRoot $RunRoot
@{name='FiveProcessCycle';exitCode=$LASTEXITCODE}|ConvertTo-Json -Compress|Add-Content "$RunRoot/r1-sequence.jsonl"
Idle
if(Test-Path "$RunRoot/VerifiedShared/cycle-final.json"){$null=Run 'RuntimeAudit' 'RunloopRuntimeAudit.Run' $false "$RunRoot/VerifiedShared"}
$null=Run 'EntryRun' 'RunloopEntry.Run' $false
# Catalog process chain owns its separate synthetic fixtures and exact interrupted archives.
New-Item -ItemType Directory "$RunRoot/Catalog/fixtures" -ErrorAction Stop|Out-Null
Copy-Item "$RunRoot/Prepare/fixtures/v?.json" "$RunRoot/Catalog/fixtures"
foreach($m in 'Run','Resume','Interrupt','Recover'){$code=Run "Catalog-$m" "B09Rules.$m" $false "$RunRoot/Catalog";if($code -ne 0){break}}
& $pw -NoProfile -File "$repo/ProjectDocs/WanxiangGuitu/DeliveryCombat01/Invoke-Regression.ps1" -Project $Project -Output "$RunRoot/Regression"
@{name='AffectedRegressionAndNormalAI';exitCode=$LASTEXITCODE}|ConvertTo-Json -Compress|Add-Content "$RunRoot/r1-sequence.jsonl"
Idle
foreach($f in Get-ChildItem "$RunRoot/Regression/Deferred" -File){Move-Item -LiteralPath $f.FullName -Destination "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/$($f.Name)"}
Copy-Item "$repo/ProjectDocs/WanxiangGuitu/DeliveryBuild01/Tests/Build01Audit.cs.txt" "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/Build01Audit.cs"
$inputs=foreach($folder in 'Assets','Packages','ProjectSettings'){Get-ChildItem "$Project/$folder" -File -Recurse|ForEach-Object {@{path=$_.FullName.Substring($Project.Length+1);sha256=(Get-FileHash -LiteralPath $_.FullName).Hash;bytes=$_.Length}}}
$inputs|ConvertTo-Json -Depth 4|Set-Content "$RunRoot/build-inputs.json" -Encoding utf8
$null=Run 'Build' 'Build01Audit.Run'
