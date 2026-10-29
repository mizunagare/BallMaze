param([string]$Project='I:/WGCombat/RUN01-1029-A/P/Project',[string]$RunRoot='I:/WGCombat/RUN01-1029-A')
$ErrorActionPreference='Stop';$repo=Split-Path (Split-Path (Split-Path $PSScriptRoot));$pw=(Get-Process -Id $PID).Path;$limit=[DateTime]::UtcNow.AddMinutes(20)
while(!(Test-Path "$RunRoot/Build/results.json")){if([DateTime]::UtcNow -gt $limit){throw 'Prior sequence incomplete; no process stopped'};Start-Sleep 5}
if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){throw 'Occupied clone preserved'}
foreach($f in Get-ChildItem "$PSScriptRoot/Tests" -Filter '*.cs.txt'){Copy-Item $f.FullName "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/$($f.BaseName)"}
foreach($m in 'Missing','Corrupt'){& $pw -NoProfile -File "$repo/ProjectDocs/WanxiangGuitu/DeliveryCombat02/Invoke-Combat02.ps1" -Project $Project -Output "$RunRoot/Unknown-$m" -Method "RunloopUncertain.$m"}
& $pw -NoProfile -File "$repo/ProjectDocs/WanxiangGuitu/DeliveryCombat01/Invoke-Checks.ps1" -Project $Project -Output "$RunRoot/EntryRun" -StorageRoot "$RunRoot/Entry" -Method RunloopEntry.Run
New-Item -ItemType Directory "$RunRoot/Catalog/fixtures" -ErrorAction Stop|Out-Null
Copy-Item "$RunRoot/Prepare/fixtures/v?.json" "$RunRoot/Catalog/fixtures"
foreach($m in 'Run','Resume','Interrupt','Recover'){
 & $pw -NoProfile -File "$repo/ProjectDocs/WanxiangGuitu/DeliveryCombat01/Invoke-Checks.ps1" -Project $Project -Output "$RunRoot/Catalog-$m" -StorageRoot "$RunRoot/Catalog" -Method "B09Rules.$m"
 if($LASTEXITCODE -ne 0){throw 'Dependent catalog chain stopped; raw failure retained'}
}
