param([Parameter(Mandatory)][string]$Project,[Parameter(Mandatory)][string]$OwnedRoot,[Parameter(Mandatory)][string]$SourceProject)
$ErrorActionPreference='Stop';$Project=[IO.Path]::GetFullPath($Project);$OwnedRoot=[IO.Path]::GetFullPath($OwnedRoot)
if(!$OwnedRoot.StartsWith('I:\WGCombat\ER1-',[StringComparison]::OrdinalIgnoreCase) -or !$Project.StartsWith($OwnedRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Owned R1 root/project required'}
if(Test-Path "$OwnedRoot/verification-processes.json"){throw 'Preserve previous verification attempts'}
$rows=@()
function Idle($stage){
 $until=(Get-Date).AddSeconds(30)
 do{$p=@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object {$_.CommandLine.Replace('/','\').Contains($Project)});if($p.Count){@{utc=[datetime]::UtcNow.ToString('o');stage=$stage;processes=@($p|Select-Object ProcessId,CommandLine)}|ConvertTo-Json -Depth 4 -Compress|Add-Content "$OwnedRoot/quiescence.jsonl";Start-Sleep -Seconds 1}}while($p.Count -and (Get-Date) -lt $until)
 if($p.Count){throw 'Occupied after bounded wait; preserve process, stop dependent work'}
}
function Run($method,$name,$storage,$graphics=$false){
 Idle $method
 & "$PSScriptRoot/Invoke-Check.ps1" -Project $Project -Output "$OwnedRoot/$name" -StorageRoot $storage -Method $method -Graphics:$graphics
 $code=$LASTEXITCODE;$script:rows+=@{method=$method;name=$name;exitCode=$code;status=if($code -eq 0){'PASS'}else{'FAIL'}}
 $script:rows|ConvertTo-Json -Depth 4|Set-Content "$OwnedRoot/verification-processes.json" -Encoding utf8
 return $code
}
Idle 'apply-authorized-one-line'
Copy-Item -LiteralPath "$SourceProject/Assets/CombatPrototype/ForestBossBrain.cs" -Destination "$Project/Assets/CombatPrototype/ForestBossBrain.cs"
foreach($seed in 418,419,420){
 $store="$OwnedRoot/After$($seed)Store";New-Item -ItemType Directory $store|Out-Null
 @{seed=$seed}|ConvertTo-Json|Set-Content "$store/r1-config.json" -Encoding utf8
 $code=Run 'EncaiR1.Run' "After$seed" $store
 if($code -ne 0){break} # Preserve deterministic failure, do not fish for a passing seed.
}
foreach($method in 'EncaiRepro.Run','EncaiGuard.Run','B3StreamRules.Run','B07Economy.Run','B07Rules.Run','B07Rules.Resume','B07Rules.PendingResume','B07Rules.CommittedResume'){
 $name=$method.Replace('.','-');$store=if($method -like 'B07Rules.*'){"$OwnedRoot/BossRulesStore"}else{"$OwnedRoot/$name"}
 $code=Run $method $name $store
 if($code -ne 0 -and $method -like 'B07Rules.*'){break}
}
$code=Run 'Build01Audit.Run' 'PureBuild' "$OwnedRoot/PureBuild" $true
if($code -eq 0){
 & "$PSScriptRoot/../DeliveryEncounterAI01/Inspect-Build.ps1" -BuildRoot "$OwnedRoot/PureBuild/Release" -Output "$OwnedRoot/PureBuild/release-inspection.json"
 $inspect=$LASTEXITCODE;$rows+=@{method='read-only PE inspection';exitCode=$inspect;status=if($inspect -eq 0){'PASS'}else{'FAIL'}}
 $rows|ConvertTo-Json -Depth 4|Set-Content "$OwnedRoot/verification-processes.json" -Encoding utf8
}
if(@($rows|Where-Object status -eq FAIL).Count){exit 1};exit 0
