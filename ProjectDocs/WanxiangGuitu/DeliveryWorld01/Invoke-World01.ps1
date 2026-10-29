param([Parameter(Mandatory)][string]$Project,[Parameter(Mandatory)][string]$RunRoot)
$ErrorActionPreference='Stop';$repo=Split-Path (Split-Path (Split-Path $PSScriptRoot));$pw=(Get-Process -Id $PID).Path
if(!(Test-Path "$RunRoot/owner.json") -or !([IO.Path]::GetFullPath($Project).StartsWith('I:\WGCombat\',[StringComparison]::OrdinalIgnoreCase))){throw 'Owned isolated root/project required'}
function Idle{if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){throw 'Occupied clone preserved; no process stopped'}}
function Check($phase,$method,$storage=''){
 Idle;if(!$storage){$storage="$RunRoot/$phase-Store"}
 & $pw -NoProfile -File "$PSScriptRoot/Invoke-WorldCheck.ps1" -Project $Project -Output "$RunRoot/$phase" -StorageRoot $storage -Method $method
 $code=$LASTEXITCODE;@{phase=$phase;method=$method;exitCode=$code;seed=$env:WORLD01_SEED;utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json -Compress|Add-Content "$RunRoot/sequence.jsonl"
 Idle;return $code
}
Idle
# Six independent Runs. The failed initial tool attempts remain separate, never filtered by seed.
foreach($sample in '418-A3','418-B','419-A','419-B','420-A','420-B'){
 $env:WORLD01_SEED=$sample.Split('-')[0];$shared="$RunRoot/Samples/$sample/Shared"
 $methods=if($sample -eq '418-A3'){@('Running','Pending','Committed','Final')}else{@('Run','FinishRun','Final')}
 foreach($method in $methods){$code=Check "Samples/$sample/$method" "WorldCycle.$method" $shared
  foreach($n in 'save.json','save.json.bak'){if(Test-Path "$shared/Store/$n"){Copy-Item "$shared/Store/$n" "$RunRoot/Samples/$sample/$method/$n"}}
  foreach($n in 'expected.json','cycle-run.json','cycle-running.json','cycle-pending.json','cycle-committed.json','cycle-finish.json','cycle-final.json'){if(Test-Path "$shared/$n"){Copy-Item "$shared/$n" "$RunRoot/Samples/$sample/$method/$n"}}
  if($code -ne 0){break}
 }
}
$checks="$Project/Assets/CombatPrototype/Editor/B06LocalChecks"
foreach($delivery in 'DeliveryRunloop01','DeliveryRunloop01R1','DeliveryCombat03','DeliveryB07'){
 foreach($f in Get-ChildItem "$repo/ProjectDocs/WanxiangGuitu/$delivery/Tests" -Filter '*.cs.txt'){Copy-Item $f.FullName "$checks/$($f.BaseName)"}
}
foreach($spec in @(@('Death','WorldCycle.Death'),@('Fault','RunloopFault.Run'),@('Missing','RunloopUncertain.Missing'),@('Corrupt','RunloopUncertain.Corrupt'),@('RecoveryMatrix','R1Matrix.Run'),@('Overflow','RunloopOverflow.Run'),@('BossEconomy','B07Economy.Run'),@('WeaponContracts','Combat03Bench.Contracts'),@('RangedArea','Combat03Area.Run'))){$null=Check $spec[0] $spec[1]}
& $pw -NoProfile -File "$repo/ProjectDocs/WanxiangGuitu/DeliveryCombat01/Invoke-Regression.ps1" -Project $Project -Output "$RunRoot/Regression"
@{phase='Regression';exitCode=$LASTEXITCODE;utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json -Compress|Add-Content "$RunRoot/sequence.jsonl"
Idle
foreach($f in Get-ChildItem "$RunRoot/Regression/Deferred" -File){Move-Item -LiteralPath $f.FullName -Destination "$checks/$($f.Name)"}
Copy-Item "$repo/ProjectDocs/WanxiangGuitu/DeliveryBuild01/Tests/Build01Audit.cs.txt" "$checks/Build01Audit.cs"
$inputs=foreach($folder in 'Assets','Packages','ProjectSettings'){Get-ChildItem "$Project/$folder" -File -Recurse|ForEach-Object {@{path=$_.FullName.Substring(([IO.Path]::GetFullPath($Project)).Length+1);sha256=(Get-FileHash -LiteralPath $_.FullName).Hash;bytes=$_.Length}}}
$inputs|ConvertTo-Json -Depth 4|Set-Content "$RunRoot/build-inputs.json" -Encoding utf8
$null=Check 'Build' 'Build01Audit.Run'
