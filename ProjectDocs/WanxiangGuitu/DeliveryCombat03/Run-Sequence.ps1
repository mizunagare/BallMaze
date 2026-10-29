param([string]$Project='I:/WGCombat/C03-1029-A/P/Project',[string]$RunRoot='I:/WGCombat/C03-1029-A')
$ErrorActionPreference='Stop';$repo=Split-Path (Split-Path (Split-Path $PSScriptRoot));$checks="$Project/Assets/CombatPrototype/Editor/B06LocalChecks";$pw=(Get-Process -Id $PID).Path
$deadline=[DateTime]::UtcNow.AddMinutes(18)
while(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){if([DateTime]::UtcNow -gt $deadline){throw 'Occupied baseline preserved; no dependent launch'};Start-Sleep 5}
if(Test-Path "$RunRoot/Before"){Copy-Item "$checks/Combat03Bench.cs" "$RunRoot/Before/Executed-Combat03Bench.cs.txt"}
function RunMeasurement($phase,$method){& $pw -NoProfile -File "$PSScriptRoot/Invoke-Measure.ps1" -Project $Project -Output "$RunRoot/$phase" -Method $method; if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){throw 'Remaining child preserved'};@{phase=$phase;exitCode=$LASTEXITCODE;utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json -Compress|Add-Content "$RunRoot/sequence.jsonl"}
RunMeasurement BeforeReadability Combat03Readability.Run
RunMeasurement BeforePaired Combat03Bench.Run
foreach($name in 'AdventureCombat.cs','CombatFeedback.cs','PlayerHudPresenter.cs'){Copy-Item "$repo/Assets/CombatPrototype/$name" "$Project/Assets/CombatPrototype/$name"}
RunMeasurement AfterReadability Combat03Readability.Run
RunMeasurement After Combat03Bench.Run
RunMeasurement Contracts Combat03Bench.Contracts
Copy-Item "$repo/ProjectDocs/WanxiangGuitu/DeliveryCombat01/Tests/Combat01Checks.cs.txt" "$checks/Combat01Checks.cs"
$old=[IO.File]::ReadAllText("$checks/Combat01Checks.cs");[IO.File]::WriteAllText("$checks/Combat01Checks.cs",$old.Replace('Mathf.Approximately(loss,s.hero.AttackPower)','Mathf.Approximately(loss,combat.BasicPower)').Replace('"expected="+s.hero.AttackPower','"expected="+combat.BasicPower'))
Copy-Item "$repo/ProjectDocs/WanxiangGuitu/DeliveryUX02/Tests/UX02BatchEntry.cs.txt" "$checks/UX02BatchEntry.cs"
RunMeasurement Legacy UX02BatchEntry.Combat
Copy-Item "$checks/Combat01Checks.cs" "$RunRoot/Legacy/Executed-Combat01Checks.cs.txt"
& $pw -NoProfile -File "$repo/ProjectDocs/WanxiangGuitu/DeliveryCombat01/Invoke-Regression.ps1" -Project $Project -Output "$RunRoot/Regression"
if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){throw 'Regression child remains; no build'}
Get-ChildItem "$RunRoot/Regression/Deferred" -File | ForEach-Object {Move-Item -LiteralPath $_.FullName -Destination "$checks/$($_.Name)"}
Copy-Item "$repo/ProjectDocs/WanxiangGuitu/DeliveryBuild01/Tests/Build01Audit.cs.txt" "$checks/Build01Audit.cs"
RunMeasurement Build Build01Audit.Run
