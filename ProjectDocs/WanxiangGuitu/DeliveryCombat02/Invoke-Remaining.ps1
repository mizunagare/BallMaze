param([string]$Project='I:/WGCombat/C2-1028-2140/P/Project',[string]$RunRoot='I:/WGCombat/C2-1028-2140')
$ErrorActionPreference='Stop'
if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){throw 'Occupied clone, preserved'}
$pw=(Get-Process -Id $PID).Path;$repo='D:/unity/WanxiangGuitu';$checks="$Project/Assets/CombatPrototype/Editor/B06LocalChecks"
Copy-Item "$repo/Assets/CombatPrototype/CombatInventoryView.cs" "$Project/Assets/CombatPrototype/CombatInventoryView.cs"
foreach($pair in @(@('AfterBoundary','Combat02Bench.Boundary'),@('Contracts','Combat02Bench.Contracts'),@('VisualAfter','Combat02Bench.Visual'))){ & $pw -NoProfile -File "$PSScriptRoot/Invoke-Combat02.ps1" -Project $Project -Output "$RunRoot/$($pair[0])" -Method $pair[1] }
# Comparable baseline presentation only, in the same disposable clone. Restore in finally.
$changed=@('AdventureCombat.cs','CombatFeedback.cs','CombatFeedbackEffect.cs','FantasyActorVisual.cs','PlayerHudPresenter.cs','CatInventoryPresenter.cs','CombatInventoryView.cs')
try {
 foreach($name in $changed){$old= & git -C $repo show "71877635f3b5891abeccaff4032045156ce8af85:Assets/CombatPrototype/$name";if($LASTEXITCODE){throw 'Baseline source unavailable'};[IO.File]::WriteAllText("$Project/Assets/CombatPrototype/$name",($old -join "`n"))}
 & $pw -NoProfile -File "$PSScriptRoot/Invoke-Combat02.ps1" -Project $Project -Output "$RunRoot/VisualBefore" -Method Combat02Bench.Visual
} finally {foreach($name in $changed){Copy-Item "$repo/Assets/CombatPrototype/$name" "$Project/Assets/CombatPrototype/$name"}}
Copy-Item "$repo/ProjectDocs/WanxiangGuitu/DeliveryCombat01/Tests/Combat01Checks.cs.txt" "$checks/Combat01Checks.cs"
Copy-Item "$repo/ProjectDocs/WanxiangGuitu/DeliveryUX02/Tests/UX02BatchEntry.cs.txt" "$checks/UX02BatchEntry.cs"
& $pw -NoProfile -File "$PSScriptRoot/Invoke-Combat02.ps1" -Project $Project -Output "$RunRoot/LegacyOriginal" -Method UX02BatchEntry.Combat
Copy-Item "$checks/Combat01Checks.cs" "$RunRoot/LegacyOriginal/Executed-Combat01Checks.cs.txt"
# Only the newly measured basic spear multiplier changes this historical expectation.
$original=Get-Content "$checks/Combat01Checks.cs" -Raw
$adapted=$original.Replace('Mathf.Approximately(loss,s.hero.AttackPower)','Mathf.Approximately(loss,combat.BasicPower)').Replace('"expected="+s.hero.AttackPower','"expected="+combat.BasicPower')
[IO.File]::WriteAllText("$checks/Combat01Checks.cs",$adapted)
& $pw -NoProfile -File "$PSScriptRoot/Invoke-Combat02.ps1" -Project $Project -Output "$RunRoot/LegacyAdapted" -Method UX02BatchEntry.Combat
Copy-Item "$checks/Combat01Checks.cs" "$RunRoot/LegacyAdapted/Executed-Combat01Checks.cs.txt"
# Normal AI and other historical rules: same existing coordinator, no user-window input.
& $pw -NoProfile -File "$repo/ProjectDocs/WanxiangGuitu/DeliveryCombat01/Invoke-Regression.ps1" -Project $Project -Output "$RunRoot/Regression"
# Restore only files deferred by that existing script; never touch occupied clone.
if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){throw 'Timed-out/remaining child preserved; dependent work blocked'}
Get-ChildItem "$RunRoot/Regression/Deferred" -File | ForEach-Object {Move-Item -LiteralPath $_.FullName -Destination "$checks/$($_.Name)"}
New-Item -ItemType Directory "$RunRoot/Recovery" -ErrorAction Stop|Out-Null
$recoveryPassed=$true
foreach($mode in 'Run','Resume','PendingResume','CommittedResume'){
 if(!$recoveryPassed){[IO.File]::WriteAllText("$RunRoot/Recovery-$mode.NOT_RUN.json",(@{status='NOT_RUN';reason='Prior dependent recovery stage failed'}|ConvertTo-Json));continue}
 & $pw -NoProfile -File "$repo/ProjectDocs/WanxiangGuitu/DeliveryCombat01/Invoke-Checks.ps1" -Project $Project -Output "$RunRoot/Recovery-$mode" -StorageRoot "$RunRoot/Recovery" -Method "B07Rules.$mode"
 $recoveryPassed=$LASTEXITCODE -eq 0
}
Copy-Item "$repo/ProjectDocs/WanxiangGuitu/DeliveryBuild01/Tests/Build01Audit.cs.txt" "$checks/Build01Audit.cs"
& $pw -NoProfile -File "$PSScriptRoot/Invoke-Combat02.ps1" -Project $Project -Output "$RunRoot/Build" -Method Build01Audit.Run

& $pw -NoProfile -File "$PSScriptRoot/Invoke-Combat02.ps1" -Project $Project -Output "$RunRoot/Slope" -Method Combat02Bench.Slope
