param([string]$Project='I:/WGCombat/C03-1029-A/P/Project',[string]$RunRoot='I:/WGCombat/C03-1029-A')
$ErrorActionPreference='Stop';$repo=Split-Path (Split-Path (Split-Path $PSScriptRoot));$pw=(Get-Process -Id $PID).Path
$limit=[DateTime]::UtcNow.AddMinutes(45)
do{if([DateTime]::UtcNow -gt $limit){throw 'Prior sequence incomplete; no process stopped'};Start-Sleep 5;$done=(Test-Path "$RunRoot/sequence.jsonl") -and (Select-String -LiteralPath "$RunRoot/sequence.jsonl" -SimpleMatch '"phase":"Build"' -Quiet)}while(!$done)
if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){throw 'Occupied project preserved'}
function ExecuteEvidence($phase,$method){& $pw -NoProfile -File "$PSScriptRoot/Invoke-Measure.ps1" -Project $Project -Output "$RunRoot/$phase" -Method $method;@{phase=$phase;exitCode=$LASTEXITCODE;utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json -Compress|Add-Content "$RunRoot/completion.jsonl";if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){throw 'Remaining child preserved'}}
ExecuteEvidence Area Combat03Area.Run
ExecuteEvidence VisualAfter Combat03Bench.Visual
# Recreate the baseline only inside the now idle disposable clone. Never edit the main project.
$snapshot="$RunRoot/FrozenProduct";New-Item -ItemType Directory $snapshot -ErrorAction Stop|Out-Null
$changed=@('AdventureCombat.cs','CombatFeedback.cs','PlayerHudPresenter.cs')
try{
 foreach($name in $changed){Copy-Item "$Project/Assets/CombatPrototype/$name" "$snapshot/$name.txt";$old=& git -C $repo show "85b8badc4e10679c73e59683f4e92c14fdb27b14:Assets/CombatPrototype/$name";if($LASTEXITCODE){throw 'Baseline unavailable'};[IO.File]::WriteAllText("$Project/Assets/CombatPrototype/$name",($old -join "`n")+"`n")}
 New-Item -ItemType Directory "$RunRoot/BaselineInputs" -ErrorAction Stop|Out-Null
 foreach($name in $changed){Copy-Item "$Project/Assets/CombatPrototype/$name" "$RunRoot/BaselineInputs/$name.txt"}
 ExecuteEvidence BeforeVerified Combat03Bench.Run
 ExecuteEvidence VisualBefore Combat03Bench.Visual
}finally{
 if(!@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){foreach($name in $changed){if(Test-Path "$snapshot/$name.txt"){Copy-Item "$snapshot/$name.txt" "$Project/Assets/CombatPrototype/$name"}}}
 else{@{status='NOT_RUN';reason='Product source restore deferred: child remains alive, no live-project mutation'}|ConvertTo-Json|Set-Content "$RunRoot/restore-deferred.json"}
}
# Prove the restored final product still compiles and passes the new dedicated rules.
ExecuteEvidence FinalReadability Combat03Readability.Run
