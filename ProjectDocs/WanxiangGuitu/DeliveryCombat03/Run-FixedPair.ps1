param([string]$Project='I:/WGCombat/C03-1029-A/P/Project',[string]$RunRoot='I:/WGCombat/C03-1029-A')
$ErrorActionPreference='Stop';$repo=Split-Path (Split-Path (Split-Path $PSScriptRoot));$pw=(Get-Process -Id $PID).Path;$limit=[DateTime]::UtcNow.AddMinutes(25)
do{if([DateTime]::UtcNow -gt $limit){throw 'Evidence sequence incomplete; preserved'};Start-Sleep 5;$done=(Test-Path "$RunRoot/completion.jsonl") -and (Select-String -LiteralPath "$RunRoot/completion.jsonl" -SimpleMatch '"phase":"FinalReadability"' -Quiet)}while(!$done)
$last=Get-Content "$RunRoot/completion.jsonl"|ForEach-Object {$_|ConvertFrom-Json}|Where-Object phase -eq FinalReadability
if($last.exitCode -ne 0){throw 'Final product validation failed; no dependent experiment'}
if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){throw 'Occupied project preserved'}
$changed=@('AdventureCombat.cs','CombatFeedback.cs','PlayerHudPresenter.cs')
try{
 foreach($name in $changed){$old=& git -C $repo show "85b8badc4e10679c73e59683f4e92c14fdb27b14:Assets/CombatPrototype/$name";if($LASTEXITCODE){throw 'Baseline unavailable'};[IO.File]::WriteAllText("$Project/Assets/CombatPrototype/$name",($old -join "`n")+"`n")}
 & $pw -NoProfile -File "$PSScriptRoot/Invoke-Measure.ps1" -Project $Project -Output "$RunRoot/FixedBefore" -Method Combat03Fixed.Run
 @{phase='FixedBefore';exitCode=$LASTEXITCODE}|ConvertTo-Json -Compress|Add-Content "$RunRoot/fixed-pair.jsonl"
 if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){throw 'Baseline process remains; preserved'}
}finally{
 if(!@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){foreach($name in $changed){Copy-Item "$RunRoot/FrozenProduct/$name.txt" "$Project/Assets/CombatPrototype/$name"}}
}
& $pw -NoProfile -File "$PSScriptRoot/Invoke-Measure.ps1" -Project $Project -Output "$RunRoot/FixedAfter" -Method Combat03Fixed.Run
@{phase='FixedAfter';exitCode=$LASTEXITCODE}|ConvertTo-Json -Compress|Add-Content "$RunRoot/fixed-pair.jsonl"
