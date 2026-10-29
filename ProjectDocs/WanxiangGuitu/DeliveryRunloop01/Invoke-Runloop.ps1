param([string]$Project='I:/WGCombat/RUN01-1029-A/P/Project',[string]$RunRoot='I:/WGCombat/RUN01-1029-A',[string]$StartStage='Running',[string]$Attempt='2')
$ErrorActionPreference='Stop';$repo=Split-Path (Split-Path (Split-Path $PSScriptRoot));$pw=(Get-Process -Id $PID).Path
if(!(Test-Path "$RunRoot/owner.json")){throw 'Owned unique root required'}
$stages=@('Running','Pending','Committed','Final');$index=[Array]::IndexOf($stages,$StartStage);if($index -lt 0){throw 'Invalid start stage'};foreach($mode in $stages[$index..3]){
 if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){throw 'Occupied project preserved'}
 & $pw -NoProfile -File "$repo/ProjectDocs/WanxiangGuitu/DeliveryCombat01/Invoke-Checks.ps1" -Project $Project -Output "$RunRoot/Stages/$mode-$Attempt" -StorageRoot "$RunRoot/Shared" -Method "RunloopCycle.$mode"
 $code=$LASTEXITCODE;@{stage=$mode;exitCode=$code}|ConvertTo-Json -Compress|Add-Content "$RunRoot/sequence.jsonl"
 Copy-Item "$RunRoot/Shared/cycle-$($mode.ToLowerInvariant()).json" "$RunRoot/Stages/$mode-$Attempt/cycle-result.json"
 Copy-Item "$RunRoot/Shared/expected.json" "$RunRoot/Stages/$mode-$Attempt/expected-after.json"
 Copy-Item "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/RunloopCycle.cs" "$RunRoot/Stages/$mode-$Attempt/Executed-RunloopCycle.cs.txt"
 if($code -ne 0){throw 'Dependent cycle blocked; original failure preserved'}
}
& $pw -NoProfile -File "$repo/ProjectDocs/WanxiangGuitu/DeliveryCombat02/Invoke-Combat02.ps1" -Project $Project -Output "$RunRoot/Death" -Method RunloopCycle.Death
& $pw -NoProfile -File "$repo/ProjectDocs/WanxiangGuitu/DeliveryCombat01/Invoke-Regression.ps1" -Project $Project -Output "$RunRoot/Regression"
if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){throw 'Remaining child; no further launch'}
Get-ChildItem "$RunRoot/Regression/Deferred" -File | ForEach-Object {Move-Item -LiteralPath $_.FullName -Destination "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/$($_.Name)"}
Copy-Item "$repo/ProjectDocs/WanxiangGuitu/DeliveryBuild01/Tests/Build01Audit.cs.txt" "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/Build01Audit.cs"
& $pw -NoProfile -File "$repo/ProjectDocs/WanxiangGuitu/DeliveryCombat02/Invoke-Combat02.ps1" -Project $Project -Output "$RunRoot/Build" -Method Build01Audit.Run
