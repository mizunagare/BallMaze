param([Parameter(Mandatory)][string]$Project,[Parameter(Mandatory)][string]$OwnedRoot,[Parameter(Mandatory)][string]$SourceProject)
$ErrorActionPreference='Stop';$OwnedRoot=[IO.Path]::GetFullPath($OwnedRoot);$Project=[IO.Path]::GetFullPath($Project)
if(!$OwnedRoot.StartsWith('I:\WGCombat\EAI01-',[StringComparison]::OrdinalIgnoreCase) -or !$Project.StartsWith($OwnedRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Owned isolated root required'}
$rows=@()
foreach($mode in 'Normal','Resume','FinalResume'){
 & "$PSScriptRoot/Invoke-NormalAI.ps1" -Project $Project -RunRoot "$OwnedRoot/Normal-Gather" -Output "$OwnedRoot/Normal-$mode-Launch" -Mode $mode
 $code=$LASTEXITCODE;$rows+=@{stage=$mode;exitCode=$code;status=if($code -eq 0){'PASS'}else{'FAIL'}}
 $rows|ConvertTo-Json -Depth 4|Set-Content "$OwnedRoot/normal-build-processes.json" -Encoding utf8
 if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object {$_.CommandLine.Replace('/','\').Contains($Project)}).Count){throw 'Owned Unity remains: preserve and stop dependent stages'}
 if($code -ne 0){break} # Resume depends on the actual previous checkpoint.
}
# Remove isolated runtime observation injection before the pure shipping build.
foreach($name in 'CombatEnemy','EnemyProjectile','ForestBossBrain','BossBrain'){Copy-Item -LiteralPath "$SourceProject/Assets/CombatPrototype/$name.cs" -Destination "$Project/Assets/CombatPrototype/$name.cs"}
$trace="$Project/Assets/CombatPrototype/BAL01Trace.cs";$editor="$Project/Assets/CombatPrototype/Editor/B06LocalChecks"
if(Test-Path $trace){Move-Item -LiteralPath $trace -Destination "$editor/BAL01Trace.cs";if(Test-Path "$trace.meta"){Move-Item -LiteralPath "$trace.meta" -Destination "$editor/BAL01Trace.cs.meta"}}
& "$PSScriptRoot/Invoke-Check.ps1" -Project $Project -Output "$OwnedRoot/PureBuild" -Method Build01Audit.Run
$code=$LASTEXITCODE;$rows+=@{stage='PureBuild';exitCode=$code;status=if($code -eq 0){'PASS'}else{'FAIL'}}
if(Test-Path "$OwnedRoot/PureBuild/Release/WanxiangGuitu.exe"){
 & "$PSScriptRoot/Inspect-Build.ps1" -BuildRoot "$OwnedRoot/PureBuild/Release" -Output "$OwnedRoot/PureBuild/release-inspection.json"
 $inspect=$LASTEXITCODE;$rows+=@{stage='ReleaseAssemblyInspection';exitCode=$inspect;status=if($inspect -eq 0){'PASS'}else{'FAIL'}}
}
$rows|ConvertTo-Json -Depth 4|Set-Content "$OwnedRoot/normal-build-processes.json" -Encoding utf8
if(@($rows|Where-Object status -eq FAIL).Count){exit 1};exit 0
