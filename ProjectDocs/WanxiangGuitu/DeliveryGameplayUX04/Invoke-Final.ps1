param([Parameter(Mandatory)][string]$Project,[Parameter(Mandatory)][string]$RunRoot,[switch]$SkipRules)
$ErrorActionPreference='Stop';$repo=Split-Path (Split-Path (Split-Path $PSScriptRoot));$pw=(Get-Process -Id $PID).Path
if(!(Test-Path "$RunRoot/owner.json") -or !([IO.Path]::GetFullPath($Project).StartsWith('I:\WGCombat\',[StringComparison]::OrdinalIgnoreCase))){throw 'Owned isolated root/project required'}
$script:failed=$false
function Idle {if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){throw 'Occupied test project preserved, no child killed'}}
function Check($phase,$method){Idle;& $pw -NoProfile -File "$PSScriptRoot/Invoke-Check.ps1" -Project $Project -Output "$RunRoot/$phase" -Method $method;$code=$LASTEXITCODE;if($code -ne 0){$script:failed=$true};@{phase=$phase;method=$method;exitCode=$code;utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json -Compress|Add-Content "$RunRoot/sequence.jsonl";Idle}
$checks="$Project/Assets/CombatPrototype/Editor/B06LocalChecks"
Idle
foreach($delivery in 'DeliveryUX02','DeliveryCombat01','DeliveryCombat03','DeliveryB07','DeliveryRunloop01','DeliveryRunloop01R1'){
 foreach($f in Get-ChildItem "$repo/ProjectDocs/WanxiangGuitu/$delivery/Tests" -Filter '*.cs.txt'){Copy-Item -LiteralPath $f.FullName -Destination "$checks/$($f.BaseName)"}
}
if(!$SkipRules){foreach($spec in @(@('UX02Regression','UX02Checks.Run'),@('MeleeContracts','Combat03Bench.Contracts'),@('RangedArea','Combat03Area.Run'),@('CombatTiming','UX04CombatTiming.Run'),@('BossEconomy','B07Economy.Run'),@('RecoveryMatrix','R1Matrix.Run'),@('Input','Input01Rules.Run'))){Check $spec[0] $spec[1]}}
# Reuse the existing normal-AI entry, startup isolation and safety switches.
$deferred="$RunRoot/Deferred";New-Item -ItemType Directory -Path $deferred -ErrorAction Stop|Out-Null
foreach($name in 'WGNormalAICheck.cs','WGA1NormalResume.cs','B06OriginalPlay.cs'){foreach($suffix in '','.meta'){$from="$checks/$name$suffix";if(Test-Path -LiteralPath $from){Move-Item -LiteralPath $from -Destination "$deferred/$name$suffix"}}}
$passed=$true
foreach($mode in 'Normal','Resume','FinalResume'){
 if(!$passed){@{phase="AI.$mode";status='NOT_RUN';reason='prior dependent stage failed'}|ConvertTo-Json -Compress|Add-Content "$RunRoot/sequence.jsonl";continue}
 Idle;& $pw -NoProfile -File "$repo/ProjectDocs/WanxiangGuitu/DeliveryUI01/Invoke-NormalAI.ps1" -SourceProject $Project -IsolationRoot "$RunRoot/Normal-Gather" -Mode $mode -LeaveTimedOutProcess -ExternalWorkerPath 'I:/WGP2/1028-080504-eef74f/Runtime/Worker/NativeProbe.dll' -B4 -Strategy Gather
 $code=$LASTEXITCODE;$passed=$code -eq 0;if(!$passed){$script:failed=$true};@{phase="AI.$mode";exitCode=$code;utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json -Compress|Add-Content "$RunRoot/sequence.jsonl";Idle
}
foreach($f in Get-ChildItem $deferred -File){Move-Item -LiteralPath $f.FullName -Destination "$checks/$($f.Name)"}
Copy-Item "$repo/ProjectDocs/WanxiangGuitu/DeliveryBuild01/Tests/Build01Audit.cs.txt" "$checks/Build01Audit.cs"
Check 'Build' 'Build01Audit.Run'

if($script:failed){exit 1};exit 0
