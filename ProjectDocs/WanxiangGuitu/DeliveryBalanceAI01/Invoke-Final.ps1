param([Parameter(Mandatory)][string]$Project,[Parameter(Mandatory)][string]$RunRoot,[switch]$SkipRules,[ValidatePattern('^[A-Za-z0-9_-]+$')][string]$OutputName='Final')
$ErrorActionPreference='Stop';$repo=Split-Path (Split-Path (Split-Path $PSScriptRoot));$pw=(Get-Process -Id $PID).Path
if(!(Test-Path "$RunRoot/owner.json") -or !([IO.Path]::GetFullPath($Project).StartsWith('I:\WGCombat\',[StringComparison]::OrdinalIgnoreCase))){throw 'Owned isolated root/project required'}
$script:failed=$false;$final="$RunRoot/$OutputName";New-Item -ItemType Directory -Path $final -ErrorAction Stop|Out-Null
function Idle {if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){throw 'Occupied test project preserved, no child killed'}}
function Check($phase,$method,$store=''){
 Idle;$args=@('-NoProfile','-File',"$PSScriptRoot/Invoke-Check.ps1",'-Project',$Project,'-Output',"$final/$phase",'-Method',$method);if($method -ne 'UX02Checks.Run'){$args+='-NoGraphics'};if($store){$args+=@('-StorageRoot',$store)}
 & $pw @args;$code=$LASTEXITCODE;if($code -ne 0){$script:failed=$true};@{phase=$phase;method=$method;exitCode=$code;utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json -Compress|Add-Content "$final/sequence.jsonl";Idle;return $code -eq 0
}
$checks="$Project/Assets/CombatPrototype/Editor/B06LocalChecks";Idle
if(Test-Path "$Project/Assets/CombatPrototype/BAL01Trace.cs"){throw 'Observation runtime must be removed before final regressions/build'}
foreach($delivery in 'DeliveryUX02','DeliveryCombat01','DeliveryCombat03','DeliveryB07','DeliveryRunloop01','DeliveryRunloop01R1','DeliveryGameplayUX04'){
 foreach($f in Get-ChildItem "$repo/ProjectDocs/WanxiangGuitu/$delivery/Tests" -Filter '*.cs.txt'){if($f.Name -eq 'B07Rules.cs.txt'){continue};Copy-Item -LiteralPath $f.FullName -Destination "$checks/$($f.BaseName)"}
}
# Preserve the previously reviewed non-batch product-start readiness fix.
Copy-Item "$repo/ProjectDocs/WanxiangGuitu/DeliveryCombat02R1/Tests/B07RulesStable.cs.txt" "$checks/B07Rules.cs"
if(!$SkipRules){foreach($spec in @(@('UX02Regression','UX02Checks.Run'),@('MeleeContracts','Combat03Bench.Contracts'),@('RangedArea','Combat03Area.Run'),@('CombatTiming','UX04CombatTiming.Run'),@('BossEconomy','B07Economy.Run'),@('RecoveryMatrix','R1Matrix.Run'),@('Input','Input01Rules.Run'),@('RandomStreams','B3StreamRules.Run'))){Check $spec[0] $spec[1]|Out-Null}
$bossOk=$true;foreach($mode in 'Run','Resume','PendingResume','CommittedResume'){
 if($bossOk){$bossOk=Check "Boss-$mode" "B07Rules.$mode" "$RunRoot/BossStore"}else{@{phase="Boss-$mode";status='NOT_RUN';reason='prior dependent Boss stage failed'}|ConvertTo-Json -Compress|Add-Content "$final/sequence.jsonl"}
}
}
# Reuse the normal-AI entry and pre-launch isolation; no native desktop activation/input.
$deferred="$final/DeferredNormal";New-Item -ItemType Directory -Path $deferred -ErrorAction Stop|Out-Null
foreach($name in 'WGNormalAICheck.cs','WGA1NormalResume.cs','B06OriginalPlay.cs'){foreach($suffix in '','.meta'){$from="$checks/$name$suffix";if(Test-Path -LiteralPath $from){Move-Item -LiteralPath $from -Destination "$deferred/$name$suffix"}}}
$passed=$true
foreach($mode in 'Normal','Resume','FinalResume'){
 if(!$passed){@{phase="AI.$mode";status='NOT_RUN';reason='prior dependent AI stage failed'}|ConvertTo-Json -Compress|Add-Content "$final/sequence.jsonl";continue}
 Idle;$os=Get-CimInstance Win32_OperatingSystem;$capacity=[double]$os.FreeVirtualMemory/1MB
 @{utc=[datetime]::UtcNow.ToString('o');freeCommitGB=$capacity;minimumGB=5;mode=$mode}|ConvertTo-Json|Set-Content "$final/AI-$mode.resources.json"
 if($capacity -lt 5){$passed=$false;$script:failed=$true;@{phase="AI.$mode";status='NOT_RUN';reason='existing heavy Unity 5GB resource guard, no child launched'}|ConvertTo-Json -Compress|Add-Content "$final/sequence.jsonl";continue}
 & $pw -NoProfile -File "$repo/ProjectDocs/WanxiangGuitu/DeliveryUI01/Invoke-NormalAI.ps1" -SourceProject $Project -IsolationRoot "$final/Normal-Gather" -Mode $mode -LeaveTimedOutProcess -ExternalWorkerPath 'I:/WGP2/1028-080504-eef74f/Runtime/Worker/NativeProbe.dll' -B4 -Strategy Gather
 $code=$LASTEXITCODE;$passed=$code -eq 0;if(!$passed){$script:failed=$true};@{phase="AI.$mode";exitCode=$code;utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json -Compress|Add-Content "$final/sequence.jsonl";Idle
}
foreach($f in Get-ChildItem $deferred -File){Move-Item -LiteralPath $f.FullName -Destination "$checks/$($f.Name)"}
Copy-Item "$repo/ProjectDocs/WanxiangGuitu/DeliveryBuild01/Tests/Build01Audit.cs.txt" "$checks/Build01Audit.cs"
Check 'Build' 'Build01Audit.Run'|Out-Null
if($script:failed){exit 1};exit 0
