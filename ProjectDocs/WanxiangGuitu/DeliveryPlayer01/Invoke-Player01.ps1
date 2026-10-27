[CmdletBinding()]
param([Parameter(Mandatory)][string]$RunRoot,[string]$SourceProject='D:/unity/WanxiangGuitu',
 [string]$WorkerFrom='D:/WanxiangValidationRuns/Input01/20261027-151043-585c2866/FinalFrozenValidation/20261027-161647-ab2a444e',
 [string]$UnityPath='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe')
$ErrorActionPreference='Stop'
$entry=Join-Path $PSScriptRoot '../DeliveryUI01/Automation/Invoke-LocalValidation.ps1'
$ast=[Management.Automation.Language.Parser]::ParseFile($entry,[ref]$null,[ref]$null)
foreach($name in 'SafePath','WriteReportFile','Flush','Note','StartChild','FinishChild','Step','OwnedMove'){$def=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true);Invoke-Expression $def.Extent.Text}
$root=SafePath $RunRoot;$source=SafePath $SourceProject;$owner=Get-Content "$root/owner.json" -Raw|ConvertFrom-Json
if($owner.kind -ne 'PLAYER-01 isolated vertical-slice validation' -or $owner.source -ne $SourceProject -or (Test-Path "$root/results.json")){throw 'Fresh owned PLAYER-01 root required'}
$b=@(Get-ChildItem "$root/B" -Directory);if($b.Count -ne 1){throw 'One fresh completed build required'};$buildRoot=$b[0].FullName
$bo=Get-Content "$buildRoot/owner.json" -Raw|ConvertFrom-Json;$project=$bo.project;$build=Join-Path $buildRoot 'Results/Release'
$br=Get-Content "$buildRoot/Results/build-report-messages.json" -Raw|ConvertFrom-Json
if($br.result -ne 'Succeeded' -or $br.errors -ne 0 -or (Get-Content "$buildRoot/preserved-processes.json" -Raw|ConvertFrom-Json).Count){throw 'Build quality/process dependency failed'}
$MinimumUnityCommitGB=3;$script:results=[Collections.Generic.List[object]]::new();$script:children=[Collections.Generic.List[object]]::new()
$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$true;$script:workerPath=Join-Path $WorkerFrom 'Worker/NativeProbe.dll';$dotnet=(Get-Command dotnet).Source;$pwsh=(Get-Process -Id $PID).Path
$wo=Get-Content "$WorkerFrom/owner.json" -Raw|ConvertFrom-Json;if($wo.source -ne $source -or $wo.kind -ne 'WanxiangGuitu isolated unattended run'){throw 'Worker provenance mismatch'}
$tools=Join-Path $root 'ExecutedTools';New-Item -ItemType Directory $tools|Out-Null;foreach($p in @($PSCommandPath,$entry,(Join-Path $PSScriptRoot '../DeliveryUI01/Invoke-NormalAI.ps1'))){Copy-Item -LiteralPath $p -Destination $tools}
$data=Join-Path $root 'C';New-Item -ItemType Directory $data|Out-Null
# Existing tests' fixtures were prepared beside the build; copy the entire known fixture inputs.
foreach($name in 'fixtures','legacy-forest-v9','r1-legacy-layout4.json','s2r1-inputs.json'){if(Test-Path "$buildRoot/Results/$name"){Copy-Item -LiteralPath "$buildRoot/Results/$name" -Destination $data -Recurse}}
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'Tests/P01Confirmation.cs.txt') -Destination "$project/Assets/CombatPrototype/Editor/B06LocalChecks/P01Confirmation.cs"
function CheckUnity($method,$storage,$visible=$false,$title=$false){
 if(@(Get-CimInstance Win32_Process|Where-Object {$_.Name -eq 'Unity.exe' -and $_.CommandLine -like ('*'+$project+'*')}).Count){Note $method NOT_RUN 'Owned project occupied; no close or kill' environment;return $false}
 New-Item -ItemType Directory $storage -Force|Out-Null;$args=@('-projectPath',$project,'-wanxiang-storage-root',$storage,'-executeMethod',$method,'-logFile',"$storage/$method.log");if(!$visible){$args=@('-batchmode')+$args};if($title){$args+='-wanxiang-validate-title-entry'}
 $r=Step $method $UnityPath $args 600 editor-controlled $storage;return $r.status -eq 'PASS'
}
Note 'formal-gather-capability' NOT_RUN 'Gather and resume use UnityEditor/A1ValidationDrivers and -executeMethod; final Player strips these. No formal Player AI injection or gameplay bypass will be added.' formal-player-adventure
Note 'formal-settings-input-capability' NOT_RUN 'No authorized independent interactive input desktop. Existing virtual InputSystem and uGUI test driver is Editor-only.' formal-player-input
$ok=CheckUnity 'Input01Rules.Run' $data
if($ok){$ok=CheckUnity 'Input01Play.Run' $data $true}
if($ok){CheckUnity 'Input01Play.Resume' $data $true $true|Out-Null}else{Note 'Input01Play.Resume' NOT_RUN 'Run dependency failed' editor-controlled}
foreach($method in 'B09Rules.Run','B09Rules.Resume','B09Rules.Interrupt','B09Rules.Recover','B09Cases.Run','B09Cases.Pending','B09Cases.Committed'){
 if(!(CheckUnity $method $data)){break}
}
$fixture=Join-Path $root 'Fixture';$fixtureOk=CheckUnity 'U16Fixture.Run' $fixture
if($fixtureOk){
 $confirm=Join-Path $root 'Confirmation';New-Item -ItemType Directory "$confirm/WanxiangGuitu" -Force|Out-Null;Copy-Item -LiteralPath "$fixture/WanxiangGuitu/ForestRuins" -Destination "$confirm/WanxiangGuitu" -Recurse
 CheckUnity 'P01Confirmation.Run' $confirm $false $true|Out-Null
}
# Exact existing normal-AI handoff; all moves are inside this new owner root.
if(@(Get-CimInstance Win32_Process|Where-Object {$_.Name -eq 'Unity.exe' -and $_.CommandLine -like ('*'+$project+'*')}).Count){
 Note 'Gather.all' NOT_RUN 'Owned Editor remains active; preserve its files/process' editor-normal-ai
}else{
$deferred=Join-Path $root 'Deferred';New-Item -ItemType Directory $deferred|Out-Null;$handoff=@()
foreach($name in 'WGNormalAICheck.cs','WGA1NormalResume.cs','B06OriginalPlay.cs'){foreach($suffix in @('','.meta')){$from="$project/Assets/CombatPrototype/Editor/B06LocalChecks/$name$suffix";if(Test-Path $from){$to=Join-Path $deferred ($name+$suffix);OwnedMove $from $to;$handoff+=@{from=$from;to=$to}}}}
$normalPassed=$true
foreach($mode in 'Normal','Resume','FinalResume'){
 if(!$normalPassed){Note "Gather.$mode" NOT_RUN 'Previous Editor AI stage failed' editor-normal-ai;continue}
 $r=Step "Gather.$mode" $pwsh @('-NoProfile','-File',(Join-Path $PSScriptRoot '../DeliveryUI01/Invoke-NormalAI.ps1'),'-SourceProject',$project,'-IsolationRoot',"$root/Gather",'-Mode',$mode,'-UnityPath',$UnityPath,'-LeaveTimedOutProcess','-ExternalWorkerPath',$script:workerPath,'-DesktopName',$script:desktop,'-B4','-Strategy','Gather') 420 editor-normal-ai
 $normalPassed=$r.status -eq 'PASS'
}
if(!@(Get-CimInstance Win32_Process|Where-Object {$_.Name -eq 'Unity.exe' -and $_.CommandLine -like ('*'+$project+'*')}).Count){foreach($m in $handoff){OwnedMove $m.to $m.from}}
}
$exe=Join-Path $build 'WanxiangGuitu.exe';$python=Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
foreach($kind in 'Missing','Ready','Corrupt','Incompatible','Pending','Committed'){
 if(!$fixtureOk){Note "Player.$kind" NOT_RUN 'Synthetic fixture dependency failed' formal-player;continue}
 if(@(Get-CimInstance Win32_Process|Where-Object Name -eq 'WanxiangGuitu.exe').Count){Note "Player.$kind" NOT_RUN 'Existing Player conflict; preserve process' environment;continue}
 $storage=Join-Path $root "Player-$kind";New-Item -ItemType Directory $storage|Out-Null;$dir=Join-Path $storage 'WanxiangGuitu/ForestRuins'
 if($kind -ne 'Missing'){
  New-Item -ItemType Directory (Split-Path $dir) -Force|Out-Null
  if($kind -eq 'Ready'){Copy-Item -LiteralPath "$fixture/WanxiangGuitu/ForestRuins" -Destination $dir -Recurse}
  elseif($kind -in @('Pending','Committed')){if(!(Test-Path "$data/b09-menu-$kind/save.json")){Note "Player.$kind" NOT_RUN 'Terminal controlled fixture unavailable' formal-player;continue};Copy-Item -LiteralPath "$data/b09-menu-$kind" -Destination $dir -Recurse}
  else{New-Item -ItemType Directory $dir|Out-Null;if($kind -eq 'Corrupt'){[IO.File]::WriteAllText("$dir/save.json",'PLAYER01 synthetic corrupt data')}else{$future=Get-Content "$fixture/WanxiangGuitu/ForestRuins/save.json" -Raw|ConvertFrom-Json;$future.version=99;$future|ConvertTo-Json -Depth 100|Set-Content "$dir/save.json"}}
 }
 $snap=@{};if(Test-Path $dir){foreach($f in Get-ChildItem $dir -File -Recurse){$snap[[IO.Path]::GetRelativePath($dir,$f.FullName).Replace('\','/')]=(Get-FileHash $f.FullName).Hash}};$snap|ConvertTo-Json|Set-Content "$storage/save-before.json"
 $start=[datetime]::UtcNow;$token=StartChild $exe @('-force-d3d11','-wanxiang-storage-root',$storage,'-wanxiang-entry-evidence','-screen-fullscreen','0','-screen-width','1280','-screen-height','720','-logFile',"$storage/player.log") "$storage/player" '' $true
 $deadline=$start.AddSeconds(90);$ready=$false
 while(!$token.process.HasExited -and [datetime]::UtcNow -lt $deadline){if((Test-Path "$storage/title-player.png") -and (Test-Path "$storage/entry-audit.jsonl")){$ready=$true;break};Start-Sleep -Milliseconds 200}
 $id=if(Test-Path $token.receipt){(Get-Content $token.receipt -Raw|ConvertFrom-Json).pid}else{$token.process.Id}
 if($kind -eq 'Missing' -and !$token.process.HasExited){Step 'native-environment-check' $dotnet @($script:workerPath,'safe-input',[string]$id,"$storage/native-environment.json",$exe,$script:desktop) 15 native-ui|Out-Null}
 if(!$token.process.HasExited){Step "PlayerClose.$kind" $dotnet @($script:workerPath,'close',[string]$id,"$storage/close.json",$exe,$script:desktop) 10 native-close|Out-Null}
 $ended=$token.process.WaitForExit(30000);if($ended){FinishChild $token}
 @{startUtc=$start.ToString('o');endUtc=[datetime]::UtcNow.ToString('o');pid=$id;ended=$ended;timedOut=!$ended;exitCode=$(if($ended){$token.process.ExitCode}else{$null});forcedTermination=$false;ready=$ready;closeMethod='Owned background WM_CLOSE, NOT titlebar or native input'}|ConvertTo-Json|Set-Content "$storage/process.json"
 Step "PlayerVerify.$kind" $python @('-B',(Join-Path $PSScriptRoot '../DeliveryB09/Verify-Title.py'),'--root',$storage,'--kind',$kind) 30 formal-player|Out-Null
 if(!$ended){Note 'remaining-player-cases' NOT_RUN 'Timed-out Player preserved; no further Player launch' environment;break}
}
Note 'native-U16-human' NOT_RUN 'No independent interactive desktop/tester; no switching or activation allowed' native-human
Note 'full-performance' NOT_RUN 'No fixed gameplay load accessible in final Player automation. Startup/screenshots are not a performance benchmark.' performance
ConvertTo-Json -InputObject @($script:children|Where-Object {!$_.process.HasExited}|ForEach-Object {$_.process.Id})|Set-Content "$root/preserved-processes.json"
Flush;Write-Output "RESULT_ROOT=$root"
if(@($script:results|Where-Object status -eq 'FAIL').Count){exit 1};exit 0
