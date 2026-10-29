param([string]$Project='I:/WGCombat/RUN01-1029-A/P/Project',[string]$RunRoot='I:/WGCombat/RUN01-1029-A')
$ErrorActionPreference='Stop';$repo=Split-Path (Split-Path (Split-Path $PSScriptRoot));$pw=(Get-Process -Id $PID).Path
New-Item -ItemType Directory "$RunRoot/VerifiedShared" -ErrorAction Stop|Out-Null
foreach($mode in 'Run','Running','Pending','Committed','Final'){
 if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){throw 'Occupied clone preserved'}
 & $pw -NoProfile -File "$repo/ProjectDocs/WanxiangGuitu/DeliveryCombat01/Invoke-Checks.ps1" -Project $Project -Output "$RunRoot/Verified/$mode" -StorageRoot "$RunRoot/VerifiedShared" -Method "RunloopCycle.$mode"
 $code=$LASTEXITCODE;@{stage=$mode;exitCode=$code}|ConvertTo-Json -Compress|Add-Content "$RunRoot/verified-sequence.jsonl"
 foreach($name in 'save.json','save.json.bak'){if(Test-Path "$RunRoot/VerifiedShared/Store/$name"){Copy-Item "$RunRoot/VerifiedShared/Store/$name" "$RunRoot/Verified/$mode/$name"}}
 Copy-Item "$RunRoot/VerifiedShared/expected.json" "$RunRoot/Verified/$mode/expected-after.json"
 Copy-Item "$RunRoot/VerifiedShared/cycle-$($mode.ToLowerInvariant()).json" "$RunRoot/Verified/$mode/cycle-result.json"
 Copy-Item "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/RunloopCycle.cs" "$RunRoot/Verified/$mode/Executed-RunloopCycle.cs.txt"
 if($code -ne 0){throw 'Dependent frozen cycle stopped; raw failure preserved'}
}
