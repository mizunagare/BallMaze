[CmdletBinding()]
param([string]$SourceProject='D:/unity/WanxiangGuitu',[string]$TestRoot='C:/Users/guan/Documents/unitytest/WanxiangB4Directed',
 [string[]]$Methods=@('B4Checks.Topology'),[string[]]$NormalStrategies=@(),[string]$WorkerFrom='C:/Users/guan/Documents/unitytest/WanxiangB3Verified/20261024-120353-057d1bd3',
 [string]$UnityPath='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe')
$ErrorActionPreference='Stop';$entry=Join-Path $PSScriptRoot '../DeliveryUI01/Automation/Invoke-LocalValidation.ps1'
$ast=[Management.Automation.Language.Parser]::ParseFile($entry,[ref]$null,[ref]$null)
foreach($name in 'SafePath','Flush','Note','OwnedMove','StartChild','FinishChild','Step'){$def=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true);Invoke-Expression $def.Extent.Text}
$source=SafePath $SourceProject;$base=SafePath $TestRoot;$workerRoot=SafePath $WorkerFrom
if($base -eq $source -or $base.StartsWith($source+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'External root required'}
$oldOwner=Get-Content "$workerRoot/owner.json" -Raw|ConvertFrom-Json;if($oldOwner.source -ne $source -or $oldOwner.kind -ne 'WanxiangGuitu isolated unattended run'){throw 'Reviewed owned worker required'}
$root=Join-Path $base ((Get-Date -Format 'yyyyMMdd-HHmmss')+'-'+[guid]::NewGuid().ToString('N').Substring(0,8));New-Item -ItemType Directory $root -Force|Out-Null
$script:results=[Collections.Generic.List[object]]::new();$script:children=[Collections.Generic.List[object]]::new();$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$true;$script:workerPath=Join-Path $workerRoot 'Worker/NativeProbe.dll';$dotnet=(Get-Command dotnet).Source
@{kind='B4 directed checks using existing orchestration';source=$source;root=$root;utc=[datetime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content "$root/owner.json"
$project=Join-Path $root 'Project';$data=Join-Path $root 'Rules';$pwsh=(Get-Process -Id $PID).Path
$prep=Step 'prepare' $pwsh @('-NoProfile','-File',(Join-Path $PSScriptRoot '../DeliveryUI01/Invoke-Rules.ps1'),'-SourceProject',$source,'-WorkProject',$project,'-ArtifactsRoot',$data,'-PrepareOnly') 180
if($prep.status -eq 'PASS'){
 $compileBlocked=$false;foreach($method in $Methods){$prior=switch($method){'B07Rules.PendingResume'{'B07Rules.Resume'} 'B07Rules.CommittedResume'{'B07Rules.PendingResume'} default{''}};if($prior -and !@($script:results|Where-Object {$_.name -eq $prior -and $_.status -eq 'PASS'}).Count){Note $method NOT_RUN "Dependency failed: $prior" controlled;continue};if($method.EndsWith(".Resume")){ $dependency=$method.Replace(".Resume",".Run");if($Methods -contains $dependency -and !@($script:results|Where-Object {$_.name -eq $dependency -and $_.status -eq "PASS"}).Count){Note $method NOT_RUN "Dependency failed: $dependency" controlled;continue} };if($compileBlocked){Note $method NOT_RUN "Compilation failed in this isolated copy" controlled;continue};$runArgs=@('-projectPath',$project,'-wanxiang-storage-root',$data,'-executeMethod',$method,'-logFile',"$data/$method.log");if($method -notin @('R1Visual.Run','B07Combat.Run')){$runArgs=@('-batchmode')+$runArgs};$r=Step $method $UnityPath $runArgs 600 'controlled' $data;if($r.timedOut){break};if($r.status -ne 'PASS' -and (Test-Path "$data/$method.log") -and (Select-String -LiteralPath "$data/$method.log" -Pattern 'error CS\d+' -Quiet)){$compileBlocked=$true}}
}
if($NormalStrategies.Count -and !@($script:results|Where-Object status -eq 'FAIL').Count){
 $deferred=Join-Path $root 'Deferred';New-Item -ItemType Directory $deferred|Out-Null;$handoff=@()
 foreach($name in 'WGNormalAICheck.cs','WGA1NormalResume.cs','B06OriginalPlay.cs'){foreach($suffix in @('','.meta')){$from=Join-Path $project ('Assets/CombatPrototype/Editor/B06LocalChecks/'+$name+$suffix);if(Test-Path $from){$to=Join-Path $deferred ($name+$suffix);OwnedMove $from $to;$handoff+=@{from=$from;to=$to}}}}
 foreach($strategy in $NormalStrategies){$passed=$true;foreach($mode in 'Normal','Resume','FinalResume'){
  if(!$passed){Note "normal.$strategy.$mode" NOT_RUN 'Dependency failed' normal-ai;continue}
  if(@(Get-CimInstance Win32_Process|Where-Object {$_.Name -eq 'Unity.exe' -and $_.CommandLine -like ('*'+$project+'*')}).Count){Note "normal.$strategy.$mode" NOT_RUN 'Owned project still occupied; preserve process' normal-ai;$passed=$false;continue}
  $r=Step "normal.$strategy.$mode" $pwsh @('-NoProfile','-File',(Join-Path $PSScriptRoot '../DeliveryUI01/Invoke-NormalAI.ps1'),'-SourceProject',$project,'-IsolationRoot',"$root/Normal-$strategy",'-Mode',$mode,'-UnityPath',$UnityPath,'-LeaveTimedOutProcess','-ExternalWorkerPath',$script:workerPath,'-DesktopName',$script:desktop,$(if($strategy -in @('Land','Lake')){'-B07'}else{'-B4'}),'-Strategy',$strategy) 420 normal-ai
  $passed=$r.status -eq 'PASS'
 }}
 if(!@(Get-CimInstance Win32_Process|Where-Object {$_.Name -eq 'Unity.exe' -and $_.CommandLine -like ('*'+$project+'*')}).Count){foreach($m in $handoff){OwnedMove $m.to $m.from}}
}
$alive=@($script:children|Where-Object {!$_.process.HasExited}|ForEach-Object {$_.process.Id});ConvertTo-Json -InputObject $alive|Set-Content "$root/preserved-processes.json";Flush;Write-Output "RESULT_ROOT=$root"
if(@($script:results|Where-Object status -eq 'FAIL').Count){exit 1};exit 0
