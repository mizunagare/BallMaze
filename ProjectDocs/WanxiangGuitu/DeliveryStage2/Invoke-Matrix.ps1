[CmdletBinding()]
param([Parameter(Mandatory)][string]$OwnerRoot,[Parameter(Mandatory)][string]$IsolationRoot,
 [Parameter(Mandatory)][string]$DesktopName,[string]$OnlyCase='',[string]$WorkerFrom='',
 [string]$UnityPath='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe')
$ErrorActionPreference='Stop'
# Reuse the existing command/timeout/exit reporting and private-desktop launcher.
$entry=Join-Path $PSScriptRoot '../DeliveryUI01/Automation/Invoke-LocalValidation.ps1'
$ast=[Management.Automation.Language.Parser]::ParseFile($entry,[ref]$null,[ref]$null)
foreach($name in 'SafePath','WriteReportFile','Flush','Note','OwnedMove','StartChild','FinishChild','Step'){
 $def=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true)
 Invoke-Expression $def.Extent.Text
}
$owned=SafePath $OwnerRoot;$root=SafePath $IsolationRoot
if(!(Test-Path "$owned/owner.json") -or !$root.StartsWith($owned+'\',[StringComparison]::OrdinalIgnoreCase) -or (Test-Path $root)){throw 'Fresh contained child of an owned isolated run required'}
if($DesktopName -notmatch '^WGTest_[a-f0-9]{32}$'){throw 'Reviewed inactive desktop required'}
$project=SafePath (Join-Path $owned 'Project');$script:desktop=$DesktopName
$owner=Get-Content "$owned/owner.json" -Raw|ConvertFrom-Json
if($owner.kind -notin @('WanxiangGuitu isolated unattended run','B4 directed checks using existing orchestration')){throw 'Unknown project owner'}
$worker=Join-Path $owned 'Worker/NativeProbe.dll'
if(!(Test-Path $worker)){
 if(!$WorkerFrom){throw 'Explicit reviewed WorkerFrom required when owner has no built worker'};$workerRoot=SafePath $WorkerFrom;$workerOwner=Get-Content "$workerRoot/owner.json" -Raw|ConvertFrom-Json;if($workerOwner.kind -ne 'WanxiangGuitu isolated unattended run'){throw 'Unknown reused worker owner'};$worker=Join-Path $workerRoot 'Worker/NativeProbe.dll'
}
if(!(Test-Path $worker)){throw 'Existing private desktop worker missing'}
$script:workerPath=$worker;$script:workerReady=$true
$script:results=[Collections.Generic.List[object]]::new();$script:children=[Collections.Generic.List[object]]::new()
$dotnet=(Get-Command dotnet).Source;$pwsh=(Get-Process -Id $PID).Path
New-Item -ItemType Directory $root|Out-Null
@{kind='Stage2 matrix using existing Step/private worker';parent=$owned;source=$project;utc=[datetime]::UtcNow.ToString('o');scope='Editor normal AI, synthetic camp, not native or human'}|ConvertTo-Json|Set-Content "$root/owner.json"
$helperInputs=@();foreach($name in 'Stage2Builds','Stage2Rules','Stage2Experiment','Stage2Physics'){
 $actual=Join-Path $project ('Assets/CombatPrototype/Editor/B06LocalChecks/'+$name+'.cs');$declared=Join-Path $PSScriptRoot ('Tests/'+$name+'.cs.txt')
 $a=(Get-FileHash $actual).Hash;$b=(Get-FileHash $declared).Hash;if($a -ne $b){throw ('Prepared helper input differs from declared source: '+$name)}
 $helperInputs+=@{name=$name;actualSha256=$a;declaredSha256=$b}
}
@{helpers=$helperInputs;driverSha256=(Get-FileHash "$PSScriptRoot/Tests/WGNormalAICheck.cs.source").Hash;launcherSha256=(Get-FileHash "$PSScriptRoot/../DeliveryUI01/Invoke-NormalAI.ps1").Hash;matrixSha256=(Get-FileHash $PSCommandPath).Hash;workerSha256=(Get-FileHash $worker).Hash;planSha256=(Get-FileHash "$PSScriptRoot/MATRIX_INPUTS.json").Hash}|ConvertTo-Json -Depth 6|Set-Content "$root/execution-inputs.json"
$plan=Get-Content "$PSScriptRoot/MATRIX_INPUTS.json" -Raw|ConvertFrom-Json
$cases=@($plan.cases|Where-Object {!$OnlyCase -or $_.id -eq $OnlyCase});if(!$cases.Count){throw 'Unknown explicit case'}
$cases|ConvertTo-Json -Depth 5|Set-Content "$root/selected-inputs.json"
$productRows=@(Get-ChildItem "$project/Assets/CombatPrototype" -Recurse -Filter '*.cs'|Where-Object {$_.FullName -notmatch '[\\/]Editor[\\/]'}|Sort-Object FullName|ForEach-Object {$_.FullName.Substring($project.Length)+':'+(Get-FileHash $_.FullName).Hash})
$codeInput=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData([Text.Encoding]::UTF8.GetBytes(($productRows -join "`n")))).ToLowerInvariant()
$driverInput=(Get-FileHash "$PSScriptRoot/Tests/WGNormalAICheck.cs.source").Hash.ToLowerInvariant()
@{cases=$cases;inputIdentity=@{codeInput=$codeInput;driverInput=$driverInput};scope='New attempts registered before launch; not historical backfill'}|ConvertTo-Json -Depth 8|Set-Content "$root/selected-plan.json"

$deferred=Join-Path $root 'Deferred';New-Item -ItemType Directory $deferred|Out-Null;$handoff=@()
if(@(Get-CimInstance Win32_Process|Where-Object {$_.Name -eq 'Unity.exe' -and $_.CommandLine -like ('*'+$project+'*')}).Count){throw 'Owned test project occupied; never close it'}
function MoveDriver([string]$from,[string]$to){
 $from=SafePath $from;$to=SafePath $to;$name=[IO.Path]::GetFileName($from)
 if($name -notin @('WGNormalAICheck.cs','WGNormalAICheck.cs.meta','WGA1NormalResume.cs','WGA1NormalResume.cs.meta','B06OriginalPlay.cs','B06OriginalPlay.cs.meta') -or [IO.Path]::GetFileName($to) -ne $name){throw 'Unknown driver handoff'}
 $a=[IO.Path]::GetFullPath((Join-Path $project ('Assets/CombatPrototype/Editor/B06LocalChecks/'+$name)));$b=[IO.Path]::GetFullPath((Join-Path $deferred $name))
 if(!(($from -eq $a -and $to -eq $b) -or ($from -eq $b -and $to -eq $a))){throw 'Driver handoff outside exact reviewed pair'}
 Move-Item -LiteralPath $from -Destination $to
}
foreach($name in 'WGNormalAICheck.cs','WGA1NormalResume.cs','B06OriginalPlay.cs'){
 foreach($suffix in @('','.meta')){$from=Join-Path $project ('Assets/CombatPrototype/Editor/B06LocalChecks/'+$name+$suffix);if(Test-Path $from){$to=Join-Path $deferred ($name+$suffix);MoveDriver $from $to;$handoff+=@{from=$from;to=$to}}}
}
foreach($case in $cases){
 $config=Join-Path $root ($case.id+'.json');$case|ConvertTo-Json -Depth 4|Set-Content $config -Encoding utf8
 $caseRoot=Join-Path $root $case.id;$passed=$true
 $attemptPath=Join-Path $root ($case.id+'.attempt.json')
 @{schemaVersion=2;caseId=$case.id;attemptId=[guid]::NewGuid().ToString('N');blockId='legacy-strategy-'+$case.seed;configSha256=(Get-FileHash $config).Hash.ToLowerInvariant();codeInput=$codeInput;driverInput=$driverInput;launchedUtc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content $attemptPath

 foreach($mode in 'Normal','Resume','FinalResume'){
  $name=$case.id+'.'+$mode
  if(!$passed){Note $name NOT_RUN 'Prior case stage failed; preserve first failure' normal-ai;continue}
  if(@(Get-CimInstance Win32_Process|Where-Object {$_.Name -eq 'Unity.exe' -and $_.CommandLine -like ('*'+$project+'*')}).Count){Note $name NOT_RUN 'Owned project occupied; preserve process and skip dependent stage' environment;$passed=$false;continue}
  $r=Step $name $pwsh @('-NoProfile','-File',"$PSScriptRoot/../DeliveryUI01/Invoke-NormalAI.ps1",'-SourceProject',$project,'-IsolationRoot',$caseRoot,'-Mode',$mode,'-UnityPath',$UnityPath,'-LeaveTimedOutProcess','-ExternalWorkerPath',$worker,'-DesktopName',$script:desktop,'-B07','-Stage2','-ExperimentConfig',$config,'-AttemptManifest',$attemptPath,'-Strategy',$case.strategy) 420 normal-ai
  $passed=$r.status -eq 'PASS'
 }
}
if(!@(Get-CimInstance Win32_Process|Where-Object {$_.Name -eq 'Unity.exe' -and $_.CommandLine -like ('*'+$project+'*')}).Count){foreach($h in $handoff){MoveDriver $h.to $h.from}}
else{Note 'restore-deferred' NOT_RUN 'Owned timed-out Editor still active; do not mutate occupied project' environment}
$alive=@($script:children|Where-Object {!$_.process.HasExited}|ForEach-Object {$_.process.Id});ConvertTo-Json -InputObject $alive|Set-Content "$root/preserved-processes.json";Flush
Write-Output "RESULT_ROOT=$root"
if(@($script:results|Where-Object status -eq 'FAIL').Count){exit 1};exit 0
