[CmdletBinding()]
param([string]$SourceProject=(Resolve-Path (Join-Path $PSScriptRoot '../../../..')).Path,
 [string]$TestRoot=(Join-Path $env:USERPROFILE 'Documents/unitytest/WanxiangUnattended'),
 [string]$UnityPath='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe',
 [string]$PythonPath=(Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'),
 [string]$ProcDumpPath='', [string]$ShaderCacheSource='', [ValidateSet('All','PlayerMatrix','DumpOnly')][string]$Phase='All',[string]$ArtifactsFrom='', [switch]$FullRegression,[switch]$GameplayOnly,[switch]$Stage2,[switch]$B4,[switch]$B07,[switch]$B08,[switch]$B09,[switch]$B10,[switch]$EntryOnly,[int]$UnityTimeoutSeconds=600,[int]$MinimumFreeGB=8,[int]$MinimumUnityCommitGB=3)
$ErrorActionPreference='Stop';if($Stage2 -and $EntryOnly){throw 'Stage2 cannot use entry-only subset'};if($Stage2){$B10=$true};if($B10){$B09=$true};if($EntryOnly -and !$B10){throw 'EntryOnly requires B10'};if($B09){$B08=$true};if($B08){$B07=$true};if($B07){$B4=$true};$ui=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
function SafePath([string]$value){if(![IO.Path]::IsPathFullyQualified($value)){throw 'Absolute path required'};$full=[IO.Path]::GetFullPath($value).TrimEnd('\','/');if($full -match '(?i)(^|[\\/])LocalLow([\\/]|$)' -or [string]::IsNullOrEmpty([IO.Path]::GetDirectoryName($full))){throw 'Player directory or drive root rejected'};for($a=$full;$a;$a=[IO.Path]::GetDirectoryName($a)){if((Test-Path -LiteralPath $a) -and ((Get-Item -LiteralPath $a -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'Linked parent rejected'}};return $full}
$source=SafePath $SourceProject;$base=SafePath $TestRoot
if($base -eq $source -or $base.StartsWith($source+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Tests must be outside source'}
New-Item -ItemType Directory -Path $base -Force|Out-Null
$root=Join-Path $base ((Get-Date -Format 'yyyyMMdd-HHmmss')+'-'+[guid]::NewGuid().ToString('N').Substring(0,8));New-Item -ItemType Directory $root|Out-Null
$project=Join-Path $root 'Project';$data=Join-Path $root 'Rules';$script:results=[Collections.Generic.List[object]]::new();$script:children=[Collections.Generic.List[object]]::new()
$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$false;$script:workerPath='';$script:compileBlocked=$false;$script:reportRetryCount=0
@{kind='WanxiangGuitu isolated unattended run';coordinatorPid=$PID;source=$source;root=$root;utc=[DateTime]::UtcNow.ToString('o');cleanup='No automatic deletion; no kill; owned processes only'}|ConvertTo-Json|Set-Content "$root/owner.json"
function WriteReportFile([string]$name,[string]$content) {
 if($name -notin @('results.json','results.csv','REPORT.md','counts.json')){throw 'Unknown report target'}
 $target=Join-Path $root $name;$temporary=$target+'.pending-'+[guid]::NewGuid().ToString('N')
 [IO.File]::WriteAllText($temporary,$content+"`n",[Text.UTF8Encoding]::new($false))
 for($attempt=0;$attempt -lt 6;$attempt++){
  try{[IO.File]::Move($temporary,$target,$true);return}
  catch [IO.IOException],[UnauthorizedAccessException] {if($attempt -eq 5){throw};$script:reportRetryCount++;Start-Sleep -Milliseconds (50*($attempt+1))}
 }
}
function Flush {
 WriteReportFile 'results.json' ($script:results|ConvertTo-Json -Depth 12)
 WriteReportFile 'results.csv' (($script:results|Select-Object name,scope,status,startUtc,endUtc,exitCode,timedOut,reason,log|ConvertTo-Csv -NoTypeInformation) -join "`n")
 $lines=@('# Local unattended validation',"Root: $root",'', '| Stage | Scope | Status | Exit | Timeout | Reason |','|---|---|---|---|---|---|')
 foreach($r in $script:results){$lines+="| $($r.name) | $($r.scope) | $($r.status) | $($r.exitCode) | $($r.timedOut) | $(($r.reason -replace '\|','/' -replace "`r|`n",' ')) |"}
 $lines+=@('', 'Native WM_CLOSE delivery is not a physical mouse click. Domain/controlled/native categories never substitute for one another. Human usability is NOT_RUN. No user confirmation is requested.');WriteReportFile 'REPORT.md' ($lines -join "`n")
 $counts=@{};foreach($s in 'PASS','FAIL','NOT_RUN','UNRESOLVED'){$counts[$s]=@($script:results|Where-Object status -eq $s).Count};WriteReportFile 'counts.json' ($counts|ConvertTo-Json)
}
function Note($name,$status,$reason,$scope='environment'){$now=[DateTime]::UtcNow.ToString('o');$script:results.Add([pscustomobject]@{name=$name;scope=$scope;status=$status;startUtc=$now;endUtc=$now;exitCode=$null;timedOut=$false;reason=$reason;log='';command=@()});Flush}
function StartChild($exe,$arguments,$log,$envRoot='',[bool]$showInactive=$false){
 $originalExe=$exe;$originalArguments=$arguments;$receipt=''
 $requiresDesktop=[IO.Path]::GetFileName($exe) -in @('Unity.exe','WanxiangGuitu.exe')
 $unityWork=[IO.Path]::GetFileName($exe) -eq 'Unity.exe' -or @($arguments|Where-Object {$_ -match 'Invoke-NormalAI.ps1$'}).Count -gt 0
 if($unityWork){
  $os=Get-CimInstance Win32_OperatingSystem;$free=[double]$os.FreeVirtualMemory/1MB;$heavy=@($arguments|Where-Object {$_ -match 'Visual|ValidateBuild|Invoke-NormalAI.ps1$'}).Count -gt 0;$minimum=$MinimumUnityCommitGB+$(if($heavy){2}else{0})
  @{utc=[datetime]::UtcNow.ToString('o');freeCommitGB=$free;minimumGB=$minimum;availablePhysicalGB=[double]$os.FreePhysicalMemory/1MB;policy='Read-only per-launch resource guard; never close programs/change pagefile/kill. No crash causality claim.'}|ConvertTo-Json|Set-Content ($log+'.resources-before.json')
  if($free -lt $minimum){throw ('ENV_RESOURCE_BLOCKED: free committed-memory capacity '+[math]::Round($free,2)+'GB below '+$minimum+'GB; no Unity child launched')}
 }

 if($requiresDesktop -and (!$script:workerReady -or !(Test-Path -LiteralPath $script:workerPath))){throw 'Private desktop worker required; refusing direct Unity/Player launch'}
 if($script:workerReady -and ($requiresDesktop -or 'fixture-window' -in $arguments -or @($arguments|Where-Object {$_ -match 'Invoke-NormalAI.ps1$'}).Count)){
  $receipt=$log+'.desktop-process.json';$spec=$log+'.launch-spec.json'
  if($showInactive -and [IO.Path]::GetFileName($exe) -ne 'WanxiangGuitu.exe'){throw 'Visible inactive launch restricted to owned test Player'}
  @{Exe=$exe;Arguments=@($arguments);Desktop=$script:desktop;Receipt=$receipt;EnvRoot=$envRoot;ShowInInactiveDesktop=$showInactive}|ConvertTo-Json -Depth 4|Set-Content $spec
  $exe=$dotnet;$arguments=@($script:workerPath,'host',$spec)
 }
 $psi=[Diagnostics.ProcessStartInfo]::new();$psi.FileName=$exe;$psi.UseShellExecute=$false;$psi.WindowStyle='Hidden';$psi.RedirectStandardOutput=$true;$psi.RedirectStandardError=$true
 foreach($a in $arguments){$psi.ArgumentList.Add([string]$a)};if($envRoot){$psi.Environment['UNITY_TEST_ROOT']=$envRoot}
 $p=[Diagnostics.Process]::Start($psi);$h=$p.Handle
 @{exe=$originalExe;arguments=@($originalArguments);hostExe=$exe;hostArguments=@($arguments);hostPid=$p.Id;startUtc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json -Depth 5|Set-Content ($log+'.command.json')
 $stdout=[IO.File]::Open($log+'.stdout',[IO.FileMode]::Create,[IO.FileAccess]::Write,[IO.FileShare]::ReadWrite);$stderr=[IO.File]::Open($log+'.stderr',[IO.FileMode]::Create,[IO.FileAccess]::Write,[IO.FileShare]::ReadWrite)
 $token=[pscustomobject]@{process=$p;stdout=$stdout;stderr=$stderr;outTask=$p.StandardOutput.BaseStream.CopyToAsync($stdout);errTask=$p.StandardError.BaseStream.CopyToAsync($stderr);exe=$originalExe;arguments=$originalArguments;log=$log;receipt=$receipt};$script:children.Add($token);return $token
}
function FinishChild($token){if($token.process.HasExited){@{hostPid=$token.process.Id;exitCode=$token.process.ExitCode;exitObservedUtc=[DateTime]::UtcNow.ToString('o');forcedTermination=$false}|ConvertTo-Json|Set-Content ($token.log+'.exit.json');$token.outTask.Wait(3000)|Out-Null;$token.errTask.Wait(3000)|Out-Null;$token.stdout.Dispose();$token.stderr.Dispose()}}
function Step($name,$exe,$arguments,$timeout=120,$scope='tool',$envRoot=''){
 $log=Join-Path $root ($name -replace '[^a-zA-Z0-9_.-]','_');$start=[DateTime]::UtcNow;$token=$null;$code=$null;$timed=$false;$reason='';$status='FAIL'
 try{$token=StartChild $exe $arguments $log $envRoot;$ended=$token.process.WaitForExit($timeout*1000);$timed=!$ended
  if($ended){$code=$token.process.ExitCode;$status=if($code -eq 0){'PASS'}elseif($code -eq 3 -and $scope -eq 'native-ui'){'NOT_RUN'}else{'FAIL'};FinishChild $token}
  else{$reason='Timeout; process preserved. Dependent project stages must skip.';Get-CimInstance Win32_Process -Filter "ProcessId=$($token.process.Id)"|Select-Object ProcessId,ParentProcessId,ExecutablePath,CommandLine,CreationDate|ConvertTo-Json|Set-Content ($log+'.timeout-process.json');$token.process|Select-Object Id,Responding,CPU,WorkingSet64,HandleCount|ConvertTo-Json|Set-Content ($log+'.timeout-state.json')}
 }catch{$reason=$_.Exception.ToString();if($_.Exception.Message.StartsWith('ENV_RESOURCE_BLOCKED:')){$status='NOT_RUN'}}
 $row=[pscustomobject]@{name=$name;scope=$scope;status=$status;startUtc=$start.ToString('o');endUtc=[DateTime]::UtcNow.ToString('o');exitCode=$code;timedOut=$timed;reason=$reason;log=$log;command=@($exe)+@($arguments)};$script:results.Add($row);Flush;return $row
}
function UnityFree {return !@(Get-CimInstance Win32_Process|Where-Object {$_.Name -eq 'Unity.exe' -and $_.CommandLine -like ('*'+$project+'*')}).Count}
function AuditTime($value){if($value -is [DateTime]){return $value.ToUniversalTime()};return [DateTime]::Parse([string]$value,[Globalization.CultureInfo]::InvariantCulture,[Globalization.DateTimeStyles]::RoundtripKind).ToUniversalTime()}
function ObserveNative($path,$phase,$observations){
 if(Test-Path -LiteralPath $path){foreach($line in Select-String -LiteralPath $path -Pattern 'Native Crash Reporting|Got a UNKNOWN|Crash!!!|Unhandled Exception:'){
  if(!($observations|Where-Object line -eq $line.LineNumber)){$observations.Add(@{line=$line.LineNumber;text=$line.Line;firstObservedUtc=[DateTime]::UtcNow.ToString('o');observedPhase=$phase;precision='Polling observation, not exception occurrence timestamp'})}
 }}
}
function OwnedMove($from,$to){foreach($p in @($from,$to)){if(!([IO.Path]::GetFullPath($p)).StartsWith($root+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Move outside owned run rejected'}};Move-Item -LiteralPath $from -Destination $to}
function UnityStep($method,$storage,$quit=$false){
 if($method -in @("B09Visual.Run","B10EntryVisual.Run","B10Cats.Run","B10Comparison.Run","B10Rules.Run","B10Rules.Resume")){$storage=Join-Path $storage ($method.Split('.')[0]);New-Item -ItemType Directory $storage -Force|Out-Null}
 if($script:compileBlocked){Note $method 'NOT_RUN' 'Compilation dependency failed; do not repeat identical compiler failure' 'controlled';return $false}
 if(!$script:workerReady){Note $method 'NOT_RUN' 'Private desktop worker unavailable; do not launch GUI onto user desktop' 'controlled';return $false}
 if(!(UnityFree)){Note $method 'NOT_RUN' 'Owned isolated Editor still active; no close/overwrite' 'controlled';return $false}
 New-Item -ItemType Directory $storage -Force|Out-Null
 $args=@('-batchmode','-projectPath',$project,'-wanxiang-storage-root',$storage,'-executeMethod',$method,'-logFile',(Join-Path $storage ($method+'.log')));if($method -in @('B07Combat.Run','B07ReadabilityVisual.Run','B07ActorOcclusion.Run','B08Visual.Run','B09Visual.Run','B10EntryVisual.Run','B10Cats.Run','B10Comparison.Run','B10Rules.Run','B10Rules.Resume')){$args=@($args|Where-Object {$_ -ne '-batchmode'})};if($method -eq 'B10EntryVisual.Run'){$args+='-wanxiang-validate-title-entry'};if($quit){$args+='-quit'}
 $r=Step $method $UnityPath $args $UnityTimeoutSeconds 'controlled' $storage
 if($r.status -ne 'PASS' -and (Test-Path (Join-Path $storage ($method+'.log'))) -and (Select-String -LiteralPath (Join-Path $storage ($method+'.log')) -Pattern 'error CS\d+|Scripts have compiler errors|Compilation failed' -Quiet)){$script:compileBlocked=$true}
 return $r.status -eq 'PASS'
}
try {
 $drive=[IO.DriveInfo]::new([IO.Path]::GetPathRoot($root));$pwsh=(Get-Process -Id $PID).Path;$dotnet=(Get-Command dotnet -ErrorAction SilentlyContinue).Source
 $pre=@{unity=$UnityPath;unityExists=(Test-Path -LiteralPath $UnityPath);python=$PythonPath;pythonExists=(Test-Path -LiteralPath $PythonPath);dotnet=$dotnet;freeBytes=$drive.AvailableFreeSpace;requiredGB=$MinimumFreeGB;processes=@(Get-CimInstance Win32_Process|Where-Object {$_.Name -in 'Unity.exe','WanxiangGuitu.exe'}|Select-Object ProcessId,CommandLine);sourceStatus=(& git -C $source status --porcelain);sourceHead=(& git -C $source rev-parse HEAD);projectVersion=(Get-Content "$source/ProjectSettings/ProjectVersion.txt")};$pre|ConvertTo-Json -Depth 5|Set-Content "$root/preflight.json"
 $installed=if($pre.unityExists){(Get-Item -LiteralPath $UnityPath).VersionInfo.ProductVersion}else{''};$expected=((Get-Content "$source/ProjectSettings/ProjectVersion.txt"|Select-String '^m_EditorVersion:').Line -split ':',2)[1].Trim();$pre.installedUnity=$installed;$pre|ConvertTo-Json -Depth 5|Set-Content "$root/preflight.json"
 if($installed -and !$installed.StartsWith($expected+'_')){Note 'preflight.unity-version' 'FAIL' 'Exact Unity version mismatch; refuse implicit upgrade';throw 'Unity version blocked'}
 if(!$pre.unityExists -or !$pre.pythonExists -or !$dotnet -or $drive.AvailableFreeSpace -lt $MinimumFreeGB*1GB){Note 'preflight' 'FAIL' 'Missing required tool or insufficient space';throw 'Preflight blocked'};Note 'preflight' 'PASS' 'Tools and space available; source/user processes will not be closed'
 # Deterministic harness negative controls. Keep failures in results; a separate assertion checks recovery/continuation.
 $bad=Step 'probe.nonzero' $pwsh @('-NoProfile','-Command','exit 7') 10 'harness-negative'
 $slow=Step 'probe.timeout' $pwsh @('-NoProfile','-Command','Start-Sleep -Seconds 3') 1 'harness-negative'
 $good=Step 'probe.after-failure' $pwsh @('-NoProfile','-Command','exit 0') 10 'harness-negative'
 Note 'orchestrator.self-check' $(if($bad.exitCode -eq 7 -and $slow.timedOut -and $good.status -eq 'PASS' -and (Test-Path "$root/probe.timeout.timeout-state.json")){'PASS'}else{'FAIL'}) 'Expected failure retained, timeout diagnosed without kill, independent next task ran' 'harness'
 $readerScript=Join-Path $root 'report-lock-reader.ps1'
 @'
param([string]$Target,[string]$Ready)
$stream=[IO.FileStream]::new($Target,[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::Read)
try{[IO.File]::WriteAllText($Ready,'held');Start-Sleep -Milliseconds 300}finally{$stream.Dispose()}
'@ | Set-Content $readerScript
 $readerReady=Join-Path $root 'report-lock-ready.txt';$reader=StartChild $pwsh @('-NoProfile','-File',$readerScript,'-Target',"$root/results.json",'-Ready',$readerReady) "$root/report-lock-reader"
 $readerDeadline=[DateTime]::UtcNow.AddSeconds(10);while(!(Test-Path $readerReady) -and !$reader.process.HasExited -and [DateTime]::UtcNow -lt $readerDeadline){Start-Sleep -Milliseconds 15}
 $retryBefore=$script:reportRetryCount;Flush;$readerEnded=$reader.process.WaitForExit(5000);$reportParsed=$null;try{$reportParsed=Get-Content "$root/results.json" -Raw|ConvertFrom-Json}catch{}
 if($readerEnded){FinishChild $reader}
 Note 'orchestrator.report-reader-lock' $(if($readerEnded -and $reader.process.ExitCode -eq 0 -and $reportParsed -and $script:reportRetryCount -gt $retryBefore){'PASS'}else{'FAIL'}) 'Independent read lock released; bounded atomic report publication retried; old JSON remained intact. No test/product failure reclassification.' 'harness'
 $dateProbe='{"utc":"2026-10-23T15:59:41.4554268Z"}'|ConvertFrom-Json;$dateStart=AuditTime '2026-10-23T15:59:35.4661228Z';Note 'orchestrator.utc-self-check' $(if((AuditTime $dateProbe.utc) -ge $dateStart -and (AuditTime '2026-10-23T15:59:34Z') -lt $dateStart){'PASS'}else{'FAIL'}) 'ISO JSON date/object boundary compared in UTC, never DateTime versus formatted string' 'harness'
 $guardCount=$script:children.Count;$guardRejected=$false;try{StartChild (Join-Path $root 'guard-never-exists/Unity.exe') @() (Join-Path $root 'worker.guard')|Out-Null}catch{$guardRejected=$_.Exception.Message -like 'Private desktop worker required*'}
 if(!$guardRejected -or $script:children.Count -ne $guardCount){Note 'worker.no-direct-unity' 'FAIL' 'Missing-worker gate did not reject before spawning';throw 'Unsafe Unity launch gate'};Note 'worker.no-direct-unity' 'PASS' 'Unity basename requires private worker even without UnityPath binding; missing executable probe starts no process' 'harness'
 $buildProbe=Step 'native-worker.build' $dotnet @('build',"$PSScriptRoot/NativeProbe/NativeProbe.csproj",'-c','Release','-o',"$root/Worker","-p:BaseIntermediateOutputPath=$root/WorkerObj/") 120
 $worker=Join-Path $root 'Worker/NativeProbe.dll'
 $script:workerPath=$worker;$script:workerReady=$buildProbe.status -eq 'PASS'
 if($script:workerReady){
  $nativeTest=StartChild $dotnet @($worker,'fixture-window',"$root/native-window-closed.json") "$root/native-window"
  $limit=[DateTime]::UtcNow.AddSeconds(10);while((!(Test-Path $nativeTest.receipt) -or !(Test-Path "$root/native-window-closed.json.ready.json")) -and !$nativeTest.process.HasExited -and [DateTime]::UtcNow -lt $limit){Start-Sleep -Milliseconds 100}
  if(Test-Path $nativeTest.receipt){
   $receipt=Get-Content $nativeTest.receipt -Raw|ConvertFrom-Json
   Step 'worker.safe-input-rejection' $dotnet @($worker,'ui',[string]$receipt.pid,"$root/worker-ui.json",$dotnet,$script:desktop) 10 'native-ui'|Out-Null
   Step 'worker.normal-close' $dotnet @($worker,'close',[string]$receipt.pid,"$root/worker-close.json",$dotnet,$script:desktop) 10 'harness'|Out-Null
   $exited=$nativeTest.process.WaitForExit(10000);$safe=Get-Content "$root/worker-ui.json" -Raw|ConvertFrom-Json
   Note 'worker.private-desktop-self-check' $(if($exited -and $nativeTest.process.ExitCode -eq 0 -and !$receipt.inputDesktopActive -and $safe.status -eq 'NOT_RUN' -and !@($safe.events|Where-Object method -like '*SendInput*').Count -and (Test-Path "$root/native-window-closed.json")){'PASS'}else{'FAIL'}) 'Synthetic worker only: inactive desktop, zero input, owned normal close, actual exit0. Not U16.' 'harness'
  }else{Note 'worker.private-desktop-self-check' 'FAIL' 'Private desktop/window creation receipt absent' 'harness'}
 }
 if($Phase -eq 'All'){
 $prep=Step 'prepare' $pwsh @('-NoProfile','-File',"$ui/Invoke-Rules.ps1",'-SourceProject',$source,'-WorkProject',$project,'-ArtifactsRoot',$data,'-PrepareOnly','-HistoricalRegression') 180
 if($prep.status -ne 'PASS'){throw 'Isolated preparation failed'}
 if($ShaderCacheSource){
  $cacheProject=SafePath $ShaderCacheSource;$cache=Join-Path $cacheProject 'Library/ShaderCache'
  $busy=@(Get-CimInstance Win32_Process|Where-Object {$_.Name -eq 'Unity.exe' -and $_.CommandLine -like ('*'+$cacheProject+'*')}).Count
  if(!$busy -and (Test-Path $cache) -and (Get-Content "$cacheProject/ProjectSettings/ProjectVersion.txt" -Raw) -eq (Get-Content "$source/ProjectSettings/ProjectVersion.txt" -Raw) -and !@(Get-ChildItem $cache -Recurse -Force|Where-Object {$_.Attributes -band [IO.FileAttributes]::ReparsePoint}).Count){
   New-Item -ItemType Directory "$project/Library" -Force|Out-Null;Copy-Item -LiteralPath $cache -Destination "$project/Library" -Recurse
   @{source=$cache;type='ShaderCache only; no AssetDatabase, assemblies or saves';freshShaderCompilation=$false}|ConvertTo-Json|Set-Content "$root/shader-cache-provenance.json";Note 'shader-cache' 'PASS' 'Copied matching-version shader cache read-only; not a clean shader-compilation claim' 'environment'
  }else{Note 'shader-cache' 'NOT_RUN' 'Cache occupied, linked, missing or wrong version; fresh compilation continues' 'environment'}
 }
 $methods=Get-Content "$data/method-plan.json" -Raw|ConvertFrom-Json
 $allMethods=@($methods)
 if(!$FullRegression){$methods=@('RouteScoringProbe.Run','RouteScoringRules.Run','RouteScoringRules.Resume','R1Audit.Run','R1Shore.Run','R1Rules.Run','R1Rules.Resume','B4Checks.Topology','B4Physics.Run','B4StateRules.Run','B4PickupRules.Run','B3StreamRules.Run','B3Checks.Run','B3Checks.Resume','B2Rules.Run','B2Rules.Resume','WGAssetAudit.Run','T06RegContainerRuntimeCheck.Run','T06RegDualWeaponCheck.Run','T06RegWorkbenchCheck.Run','WGB1Check.Run','WGB1Check.Resume','WGB1Routes.Run','WGLegacyForestCheck.Run','B06ForestCheck.Run','B06DropCheck.Run','B05FaultCheck.Run','WGA1Check.Isolation','WGA1Check.Choice','WGA1Check.Empty','WGA1Check.Recovery','UI01Rules.Run')}
 if($EntryOnly){$methods=@('WGAssetAudit.Run','B10EntryVisual.Run','B09Cases.Run','B09Cases.Pending','B09Cases.Committed')}
 $plannedStrategies=if($B4){@('Gather','Treasure','Bypass')}else{@('Legacy')};if($B07){$plannedStrategies+=@('Land','Lake')};if($B08){$plannedStrategies+=@('Tutorial')};if($B09){$plannedStrategies+=@('Entry')};if($EntryOnly){$plannedStrategies=@()}
 @{allMethods=$allMethods;selectedMethods=$methods;fullRegression=[bool]$FullRegression;b4=[bool]$B4;normalStrategies=$plannedStrategies;b07=[bool]$B07}|ConvertTo-Json -Depth 4|Set-Content "$root/test-plan.json"
 foreach($omitted in $allMethods|Where-Object {$_ -notin $methods -and $_ -ne 'WanxiangBuild.ValidateBuild'}){Note $omitted 'NOT_RUN' 'Not selected in focused suite; use -FullRegression; existing regression retained' 'suite-selection'}
  $dependencies=@{'B10Rules.Resume'='B10Rules.Run';'B09Cases.Pending'='B09Cases.Run';'B09Cases.Committed'='B09Cases.Run';'B09Rules.Resume'='B09Rules.Run';'B09Rules.Interrupt'='B09Rules.Resume';'B09Rules.Recover'='B09Rules.Interrupt';'B08Recovery.Resume'='B08Recovery.Run';'B08Rules.Resume'='B08Rules.Run';'B08Rules.FinalResume'='B08Rules.Resume';'B08Rules.CompleteResume'='B08Rules.FinalResume';'B07Rules.Resume'='B07Rules.Run';'B07Rules.PendingResume'='B07Rules.Resume';'B07Rules.CommittedResume'='B07Rules.PendingResume';'RouteScoringRules.Resume'='RouteScoringRules.Run';'R1Rules.Resume'='R1Rules.Run';'B3Checks.Resume'='B3Checks.Run';'B2Rules.Resume'='B2Rules.Run';'WGB1Check.Resume'='WGB1Check.Run';'T06RegContainerRuntimeCheck.Final'='T06RegContainerRuntimeCheck.Run';'WGA1ExtendedCheck.InterruptedResume'='WGA1ExtendedCheck.InterruptedWrite'}
 foreach($method in $methods){
  if($method -eq 'WanxiangBuild.ValidateBuild'){continue}
  if($dependencies.ContainsKey($method) -and !($script:results|Where-Object {$_.name -eq $dependencies[$method] -and $_.status -eq 'PASS'})){Note $method 'NOT_RUN' ('Dependency did not pass: '+$dependencies[$method]) 'controlled';continue}
  UnityStep $method $data ($method -eq 'B05EditChecks.Run')|Out-Null
 }
 if($B10 -and !$EntryOnly){Step 'B10.icon-alpha' $PythonPath @('-B',"$ui/../DeliveryB10/Check-Icons.py",'--icons',"$project/Assets/CombatPrototype/Resources/CatWorld/Icons",'--output',"$root/b10-icon-alpha.json") 30 'asset-alpha'|Out-Null}
 $fixture=Join-Path $root 'Fixture';$fixtureOk=UnityStep 'U16Fixture.Run' $fixture
 $build=Join-Path $root 'Build';$buildOk=UnityStep 'WanxiangBuild.ValidateBuild' $build
 $normalOk=$false;$deferred=Join-Path $root 'DeferredNormalDrivers';New-Item -ItemType Directory $deferred|Out-Null;$handoff=[Collections.Generic.List[object]]::new()
 if((UnityFree) -and !$script:compileBlocked){foreach($file in 'WGNormalAICheck.cs','WGA1NormalResume.cs','B06OriginalPlay.cs'){foreach($suffix in @('','.meta')){$from=Join-Path $project ('Assets/CombatPrototype/Editor/B06LocalChecks/'+$file+$suffix);$to=Join-Path $deferred ($file+$suffix);if(Test-Path -LiteralPath $from){OwnedMove $from $to;$handoff.Add(@{from=$from;to=$to})}}}}
 $handoff|ConvertTo-Json|Set-Content "$root/normal-driver-handoff.json"
 $strategies=if($B4){@('Gather','Treasure','Bypass')}else{@('Legacy')};if($B07){$strategies+=@('Land','Lake')};if($B08){$strategies+=@('Tutorial')};if($B09){$strategies+=@('Entry')};if($EntryOnly){$strategies=@()}
 foreach($strategy in $strategies){$normalOk=$false;$normalRoot=if($B4){"$root/Normal-$strategy"}else{"$root/Normal"};$modes=if($B4){@('Normal','Resume','FinalResume')}else{@('Normal','Resume')}
 foreach($mode in $modes){
  $label=if($B4){"normal-ai.$strategy.$mode"}else{"normal-ai.$mode"}
  if(!(UnityFree) -or $script:compileBlocked -or !$script:workerReady){Note $label 'NOT_RUN' 'Isolated Editor occupied or compile/desktop dependency blocked' 'normal-ai';continue}
  if($mode -ne 'Normal' -and !$normalOk){Note $label 'NOT_RUN' 'Previous strategy stage did not finish successfully' 'normal-ai';continue}
  $normalArgs=@('-NoProfile','-File',"$ui/Invoke-NormalAI.ps1",'-SourceProject',$project,'-IsolationRoot',$normalRoot,'-Mode',$mode,'-UnityPath',$UnityPath,'-LeaveTimedOutProcess','-ExternalWorkerPath',$worker,'-DesktopName',$script:desktop)
  if($strategy -eq 'Entry'){$normalArgs+=@('-B09','-Strategy',$strategy)}elseif($strategy -eq 'Tutorial'){$normalArgs+=@('-B08','-Strategy',$strategy)}elseif($strategy -in @('Land','Lake')){$normalArgs+=@('-B07','-Strategy',$strategy)}elseif($B4){$normalArgs+=@('-B4','-Strategy',$strategy)}else{$normalArgs+='-B3'}
  $nr=Step $label $pwsh $normalArgs 420 'normal-ai';$normalOk=$nr.status -eq 'PASS'
 }}
 if($Stage2){
  if((UnityFree) -and !$script:compileBlocked -and $script:workerReady){Step 'stage2.normal-matrix' $pwsh @('-NoProfile','-File',"$ui/../DeliveryStage2/Invoke-Matrix.ps1",'-OwnerRoot',$root,'-IsolationRoot',"$root/Stage2Matrix",'-DesktopName',$script:desktop,'-UnityPath',$UnityPath) 24480 'normal-ai-matrix'|Out-Null}
  else{Note 'stage2.normal-matrix' NOT_RUN 'Owned project/compile/private worker dependency blocked; never use user desktop' normal-ai-matrix}
  if(Test-Path "$root/Stage2Matrix/owner.json"){Step 'stage2.metrics-audit' $PythonPath @('-B',"$ui/../DeliveryStage2/Summarize-Matrix.py",'--matrix',"$root/Stage2Matrix",'--output',"$root/Stage2Summary") 60 'normal-ai-evidence'|Out-Null}
  else{Note 'stage2.metrics-audit' NOT_RUN 'No owned matrix evidence; never inherit prior trial outcomes' normal-ai-evidence}
  Step 'stage2.log-gate-probes' $PythonPath @('-B',"$ui/../DeliveryStage2/Test-LogGate.py",'--output',"$root/Stage2LogGateProbes") 60 'harness'|Out-Null
 }
 if(UnityFree){foreach($entry in $handoff){OwnedMove $entry.to $entry.from}}else{Note 'normal-driver-restore' 'NOT_RUN' 'Editor still active; preserve deferred files, do not mutate occupied project' 'environment'}
 if(!$EntryOnly -and (UnityFree) -and !$script:compileBlocked -and $script:workerReady){$terrainScreens=Join-Path $root 'TerrainScreens';New-Item -ItemType Directory $terrainScreens|Out-Null;Step 'controlled.terrain' $UnityPath @('-projectPath',$project,'-wanxiang-storage-root',$terrainScreens,'-executeMethod','R1Visual.Run','-logFile',"$terrainScreens/terrain-visual.log") 360 'controlled-visual' $terrainScreens|Out-Null}else{Note 'controlled.terrain' 'NOT_RUN' 'Isolated visual dependency unavailable' 'controlled-visual'}
 if(!$EntryOnly -and (UnityFree) -and !$script:compileBlocked -and $script:workerReady){$screens=Join-Path $root 'ControlledScreens';New-Item -ItemType Directory $screens|Out-Null;$r=Step 'controlled.visual' $UnityPath @('-projectPath',$project,'-wanxiang-storage-root',$screens,'-executeMethod','UI01Visual.Run','-logFile',"$screens/visual.log") 660 'controlled-visual' $screens;if(!(Test-Path "$screens/visual-result.txt")){Note 'controlled.visual.marker' 'FAIL' 'Missing completed screenshot matrix' 'controlled-visual'}}else{Note 'controlled.visual' 'NOT_RUN' 'Isolated Editor/compile/desktop dependency blocked' 'controlled-visual'}
 }else{
  $previous=SafePath $ArtifactsFrom;$owner=Get-Content "$previous/owner.json" -Raw|ConvertFrom-Json;$priorResults=Get-Content "$previous/results.json" -Raw|ConvertFrom-Json
  if($owner.source -ne $source -or $owner.kind -ne 'WanxiangGuitu isolated unattended run' -or !($priorResults|Where-Object {$_.name -eq 'WanxiangBuild.ValidateBuild' -and $_.status -eq 'PASS'}) -or !($priorResults|Where-Object {$_.name -eq 'U16Fixture.Run' -and $_.status -eq 'PASS'})){throw 'Only successful build/fixture from an owned run can be reused'}
  if((Get-Content "$previous/Fixture/fixture.txt" -Raw) -notmatch '^SYNTHETIC'){throw 'Synthetic fixture marker absent'}
  $fixture=Join-Path $root 'Fixture';$build=Join-Path $root 'Build';Copy-Item "$previous/Fixture" $fixture -Recurse;Copy-Item "$previous/Build" $build -Recurse;$fixtureOk=$true;$buildOk=$true
  $a=(Get-FileHash "$previous/Build/Release/WanxiangGuitu.exe").Hash;$b=(Get-FileHash "$build/Release/WanxiangGuitu.exe").Hash;if($a -ne $b){throw 'Copied build hash mismatch'}
  @{source=$previous;exeSha256=$b;scope='Reuse independent synthetic build/fixture only; rules/AI/visual not rerun or inherited as PASS'}|ConvertTo-Json|Set-Content "$root/reused-artifacts.json";Note 'reuse.build-fixture' 'PASS' 'Owned independent build copied and hashed; other phases NOT_RUN in matrix-only mode' 'artifact'
  foreach($stage in 'rules','normal-ai','controlled.visual'){Note $stage 'NOT_RUN' 'Matrix-only invocation; see original run, do not inherit PASS' 'suite-selection'}
 }
 if($fixtureOk -and $buildOk){
  $release=Join-Path $build 'Release'
  @(Get-ChildItem -LiteralPath $release -File -Recurse|ForEach-Object {@{file=[IO.Path]::GetRelativePath($release,$_.FullName);bytes=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName).Hash}})|ConvertTo-Json -Depth 4|Set-Content "$root/build-manifest.json"
  Note 'build.hashes' 'PASS' 'Complete independent Release file manifest; applies to every Player command in this run' 'artifact'
 }
 # B09 formal startup is deliberately NOT the -wanxiang-test-gameplay bypass.
 if($B09 -and $Phase -eq 'All' -and $buildOk -and $script:workerReady){
  $exe=Join-Path $build 'Release/WanxiangGuitu.exe'
  # Relative roots already fail the original parser before default-path construction.
  # Never launch a missing-root negative process that could touch real player storage on regression.
  foreach($flag in 'entry-evidence','test-gameplay'){
   if(@(Get-CimInstance Win32_Process|Where-Object Name -eq 'WanxiangGuitu.exe').Count){Note "B09-Reject.$flag" NOT_RUN 'Player conflict; preserve existing process' environment;continue}
   $storage=Join-Path $root "B09-Reject-$flag";New-Item -ItemType Directory $storage|Out-Null
   $token=StartChild $exe @('-force-d3d11',('-wanxiang-'+$flag),'-wanxiang-storage-root','relative','-screen-fullscreen','0','-screen-width','1280','-screen-height','720','-logFile',"$storage/player.log") "$storage/player"
   $ended=$token.process.WaitForExit(15000);$fallback=$false
   if(!$ended){$fallback=$true;$id=(Get-Content $token.receipt -Raw|ConvertFrom-Json).pid;Step "B09-RejectClose.$flag" $dotnet @($worker,'close',[string]$id,"$storage/close.json",$exe,$script:desktop) 10 native-close|Out-Null;$ended=$token.process.WaitForExit(10000)}
   if($ended){FinishChild $token}
   @{exitCode=if($ended){$token.process.ExitCode}else{$null};timedOut=!$ended;forcedTermination=$false;normalCloseFallback=$fallback;expectedExit=2;scope='Intentional relative-root startup rejection, not a normal exit'}|ConvertTo-Json|Set-Content "$storage/process.json"
   Step "B09-RejectVerify.$flag" $PythonPath @('-B',"$ui/../DeliveryB09/Verify-Rejection.py",'--root',$storage) 30 startup-safety|Out-Null
  }
  $titleKinds=@('Missing','Ready','Corrupt','Incompatible','Pending','Committed');if($B10){$titleKinds+=@('LegacyFlag','Uncertain')};foreach($kind in $titleKinds){
   $catalogKind=if($kind -eq 'LegacyFlag'){'Missing'}else{$kind}
   if(@(Get-CimInstance Win32_Process|Where-Object Name -eq 'WanxiangGuitu.exe').Count){Note "B09-Title.$kind" NOT_RUN 'Player conflict; preserve existing process' environment;continue}
   $storage=Join-Path $root "B09-Title-$kind";New-Item -ItemType Directory $storage|Out-Null
   if($kind -in @('Pending','Committed') -and !(Test-Path "$data/b09-menu-$kind/save.json")){Note "B09-Title.$kind" NOT_RUN 'Controlled terminal fixture did not pass' formal-player;continue}
   if($catalogKind -ne 'Missing'){$dir=Join-Path $storage 'WanxiangGuitu/ForestRuins';New-Item -ItemType Directory $dir -Force|Out-Null
    if($kind -in @('Ready','Uncertain')){Copy-Item "$fixture/WanxiangGuitu/ForestRuins/*" $dir -Recurse}
    elseif($kind -in @('Pending','Committed')){Copy-Item "$data/b09-menu-$kind/*" $dir -Recurse}
    elseif($kind -eq 'Corrupt'){[IO.File]::WriteAllText("$dir/save.json",'B09 synthetic corrupt collection')}
    else{$future=Get-Content "$fixture/WanxiangGuitu/ForestRuins/save.json" -Raw|ConvertFrom-Json;$future.version=99;$future|ConvertTo-Json -Depth 100|Set-Content "$dir/save.json"}
   }
   if($kind -eq 'Uncertain'){[IO.File]::WriteAllText("$dir/save.json.tmp",'B10 synthetic unpublished write')}
   $snap=@{};$saveDir=Join-Path $storage 'WanxiangGuitu/ForestRuins';if(Test-Path $saveDir){foreach($f in Get-ChildItem $saveDir -File -Recurse){$snap[[IO.Path]::GetRelativePath($saveDir,$f.FullName).Replace('\','/')]=(Get-FileHash $f.FullName).Hash}};$snap|ConvertTo-Json|Set-Content "$storage/save-before.json"
   $titleArgs=@('-force-d3d11','-wanxiang-storage-root',$storage,'-wanxiang-entry-evidence','-screen-fullscreen','0','-screen-width','1280','-screen-height','720','-logFile',"$storage/player.log");if($kind -eq 'LegacyFlag'){$titleArgs+='-wanxiang-test-gameplay'};$token=StartChild $exe $titleArgs "$storage/player" '' $true
   $start=[datetime]::UtcNow;$deadline=$start.AddSeconds(90);$ready=$false
   while(!$token.process.HasExited -and [datetime]::UtcNow -lt $deadline){if((Test-Path "$storage/title-player.png") -and (Test-Path "$storage/entry-audit.jsonl")){$ready=$true;break};Start-Sleep -Milliseconds 200}
   $id=if(Test-Path $token.receipt){(Get-Content $token.receipt -Raw|ConvertFrom-Json).pid}else{$token.process.Id}
   if(!$token.process.HasExited){Step "B09-TitleClose.$kind" $dotnet @($worker,'close',[string]$id,"$storage/close.json",$exe,$script:desktop) 10 native-close|Out-Null}
   $ended=$token.process.WaitForExit(30000);if($ended){FinishChild $token}
   @{pid=$id;ended=$ended;timedOut=!$ended;exitCode=if($ended){$token.process.ExitCode}else{$null};forcedTermination=$false;closeMethod='Owned background WM_CLOSE, NOT native titlebar input';ready=$ready}|ConvertTo-Json|Set-Content "$storage/process.json"
   Step "B09-TitleVerify.$kind" $PythonPath @('-B',$(if($B10){"$ui/../DeliveryB10/Verify-Title.py"}else{"$ui/../DeliveryB09/Verify-Title.py"}),'--root',$storage,'--kind',$catalogKind) 30 formal-player|Out-Null
  }
 }
 # Every matrix cell starts from identical synthetic files. Monitor experiments use separate roots/cells.
 if((!$GameplayOnly -or $B09) -and $fixtureOk -and $buildOk -and $buildProbe.status -eq 'PASS'){
  $exe=Join-Path $build 'Release/WanxiangGuitu.exe';$plan=@();foreach($renderer in 'Default','D3D11'){foreach($iteration in 1,2){$plan+=@{name="$renderer-$iteration";renderer=$renderer;dump=$false}}};$plan+=@{name='Default-dump';renderer='Default';dump=$true};if($Phase -eq 'DumpOnly'){$plan=@($plan|Where-Object dump)};if($GameplayOnly){$plan=@()}
  if($B07 -and !$GameplayOnly -and $Phase -eq 'All'){foreach($strategy in 'Land','Lake'){$readyRun=@($script:results|Where-Object {$_.name -eq "normal-ai.$strategy.FinalResume" -and $_.status -eq 'PASS'}).Count;if($readyRun -and (Test-Path "$root/Normal-$strategy/WanxiangGuitu/ForestRuins/save.json")){$plan+=@{name="B07-$strategy";renderer='D3D11';dump=$false;sourceFixture="$root/Normal-$strategy";badge=$(if($strategy -eq 'Land'){'forest:warden'}else{'forest:tide'})}}else{Note "B07-Player.$strategy" NOT_RUN 'Normal adventure checkpoint dependency did not pass' 'player-smoke'}}}
  if($B08 -and !$GameplayOnly -and $Phase -eq 'All'){if(@($script:results|Where-Object {$_.name -eq 'normal-ai.Tutorial.FinalResume' -and $_.status -eq 'PASS'}).Count){$plan+=@{name='B08-Tutorial';renderer='D3D11';dump=$false;sourceFixture="$root/Normal-Tutorial";tutorial=$true}}else{Note 'B08-Player.Tutorial' NOT_RUN 'Tutorial normal adventure dependency not passed' 'player-smoke'}}
  if($B09 -and !$B10 -and $Phase -eq 'All' -and @($script:results|Where-Object {$_.name -eq 'normal-ai.Entry.FinalResume' -and $_.status -eq 'PASS'}).Count){$plan+=@{name='B09-Entry';renderer='D3D11';dump=$false;sourceFixture="$root/Normal-Entry";tutorial=$true}}
  foreach($cell in $plan){
   $name=$cell.name;if($cell.dump -and ([string]::IsNullOrWhiteSpace($ProcDumpPath) -or !(Test-Path -LiteralPath $ProcDumpPath))){Note "matrix.$name" 'NOT_RUN' 'Optional ProcDump unavailable; non-monitored cells unaffected' 'diagnostic';continue}
   $conflicts=@(Get-CimInstance Win32_Process|Where-Object {$_.Name -eq 'WanxiangGuitu.exe'});if($conflicts.Count){$conflicts|Select-Object ProcessId,ExecutablePath|ConvertTo-Json|Set-Content "$root/$name-resource-conflict.json";Note "matrix.$name" 'NOT_RUN' 'Existing Player resource conflict; never close another run or user program' 'environment';continue}
   $storage=Join-Path $root $name;New-Item -ItemType Directory $storage|Out-Null;$fixtureSource=if($cell.ContainsKey('sourceFixture')){$cell.sourceFixture}else{$fixture};Copy-Item "$fixtureSource/WanxiangGuitu" $storage -Recurse
   if($cell.ContainsKey('sourceFixture')){@{source=$fixtureSource;scope='Complete synthetic save set from actual normal adventure final continuation. Startup/recovery only; not native input or Player combat.'}|ConvertTo-Json|Set-Content "$storage/b07-fixture-provenance.json"}
   foreach($pass in 1,2){
    if($cell.dump -and $pass -eq 2){continue}
    $save=Join-Path $storage 'WanxiangGuitu/ForestRuins/save.json';$before=Join-Path $storage "before-$pass.json";Copy-Item $save $before
    $start=[DateTime]::UtcNow;$observations=[Collections.Generic.List[object]]::new();$playerLog="$storage/player-$pass.log";$closeUtc=$null;$playerArgs=@('-wanxiang-test-gameplay','-wanxiang-storage-root',$storage,'-screen-fullscreen','0','-screen-width','1280','-screen-height','720','-logFile',"$storage/player-$pass.log");if($cell.renderer -eq 'D3D11'){$playerArgs+='-force-d3d11'}
    $player=StartChild $exe $playerArgs "$storage/player-$pass";$p=$player.process;$deadline=[DateTime]::UtcNow.AddSeconds(60);$ready=$false
    while(!$p.HasExited -and [DateTime]::UtcNow -lt $deadline){if(Test-Path "$storage/storage-audit.jsonl"){$events=Get-Content "$storage/storage-audit.jsonl"|ForEach-Object {$_|ConvertFrom-Json};if($events|Where-Object {$_.operation -eq 'initialize' -and (AuditTime $_.utc) -ge $start}){$ready=$true;break}};Start-Sleep -Milliseconds 200}
    $loaded=Join-Path $storage "loaded-$pass.json";if($ready){Copy-Item $save $loaded}
    $ownedId=if($player.receipt -and (Test-Path $player.receipt)){(Get-Content $player.receipt -Raw|ConvertFrom-Json).pid}else{$p.Id}
    $monitor=$null;if($cell.dump -and $ready){New-Item -ItemType Directory "$storage/Dumps"|Out-Null
     @{path=$ProcDumpPath;sha256=(Get-FileHash $ProcDumpPath).Hash;version=(Get-Item $ProcDumpPath).VersionInfo.FileVersion;signature=(Get-AuthenticodeSignature $ProcDumpPath).Status.ToString()}|ConvertTo-Json|Set-Content "$storage/procdump-tool.json"
     $monitor=StartChild $ProcDumpPath @('-accepteula','-mm','-e','-t','-n','1',[string]$ownedId,"$storage/Dumps") "$storage/procdump";Start-Sleep -Seconds 2}
    if($ready){Step "native.$name.$pass" $dotnet @($worker,'ui',[string]$ownedId,"$storage/ui-$pass.json",$exe,$script:desktop) 15 'native-ui'|Out-Null}
    ObserveNative $playerLog 'before-close' $observations; $closeUtc=[DateTime]::UtcNow.ToString('o')
    if(!$p.HasExited){Step "close-request.$name.$pass" $dotnet @($worker,'close',[string]$ownedId,"$storage/close-$pass.json",$exe,$script:desktop) 10 'native-close'|Out-Null}
    $closeDeadline=[DateTime]::UtcNow.AddSeconds(30);while(!$p.HasExited -and [DateTime]::UtcNow -lt $closeDeadline){ObserveNative $playerLog 'close-wait' $observations;Start-Sleep -Milliseconds 200};$ended=$p.HasExited;ObserveNative $playerLog 'after-wait' $observations
    @{launchUtc=$start.ToString('o');closeRequestedUtc=$closeUtc;exitObservedUtc=[DateTime]::UtcNow.ToString('o');ended=$ended;markers=@($observations.ToArray());precision='Observed UTC bounds; full Player log preserves order; no invented exception timestamp'}|ConvertTo-Json -Depth 5|Set-Content "$storage/timeline-$pass.json"
    $process=@{pid=$ownedId;hostPid=$p.Id;desktop=$script:desktop;startUtc=$start.ToString('o');endUtc=[DateTime]::UtcNow.ToString('o');exitCode=if($ended){$p.ExitCode}else{$null};timedOut=!$ended;ready=$ready;forcedTermination=$false;closeMethod='Owned-window WM_CLOSE';renderer=$cell.renderer;monitor=$cell.dump};$process|ConvertTo-Json|Set-Content "$storage/process-$pass.json"
    if(!$ended){Get-CimInstance Win32_Process -Filter "ProcessId=$($p.Id)"|Select-Object ProcessId,CommandLine,ExecutablePath|ConvertTo-Json|Set-Content "$storage/timeout-$pass.json";Note "player.$name.$pass" 'FAIL' 'Timeout: preserved owned process and snapshot; no forced normal-exit PASS' 'native-close';break}
    FinishChild $player;if($monitor){if($monitor.process.WaitForExit(30000)){
      FinishChild $monitor
      $checked=Step "dump-validation.$name" $PythonPath @('-B',"$PSScriptRoot/classify-procdump.py",'classify','--calibration',"$PSScriptRoot/procdump-calibration.json",'--tool-info',"$storage/procdump-tool.json",'--exit-code',[string]$monitor.process.ExitCode,'--dump-dir',"$storage/Dumps",'--stdout',($monitor.log+'.stdout'),'--stderr',($monitor.log+'.stderr'),'--output',"$storage/dump-validation.json") 30 'diagnostic'
      $script:results.Add([pscustomobject]@{name="dump.$name";scope='diagnostic';status=$checked.status;startUtc=(Get-Content ($monitor.log+'.command.json') -Raw|ConvertFrom-Json).startUtc;endUtc=[DateTime]::UtcNow.ToString('o');exitCode=$monitor.process.ExitCode;timedOut=$false;reason='Raw exit retained; classification requires signed pinned binary, calibrated exit/count and structurally valid completed dumps; see dump-validation.json';log=$monitor.log;command=@($monitor.exe)+@($monitor.arguments)});Flush
     }else{Note "dump.$name" 'UNRESOLVED' 'Monitor still writing; preserve diagnostic process' 'diagnostic'}}
    $after=Join-Path $storage "after-$pass.json";Copy-Item $save $after
    $args=@("$ui/Tests/analyze-player-close.py",'--root',$storage,'--process',"process-$pass.json",'--log',"player-$pass.log",'--since',$start.ToString('o'),'--before',$before,'--save',$after,'--output',"$storage/analysis-$pass.json")
    if($pass -eq 2){$args+=@('--previous',"$storage/after-1.json",'--current',$loaded)}
    Step "analyze.$name.$pass" $PythonPath $args 30 'native-close'|Out-Null
    if($cell.ContainsKey('badge')){Step "B07-Player.$name.$pass" $PythonPath @('-B',"$ui/../DeliveryB07/Verify-Player.py",'--root',$storage,'--before',$before,'--after',$after,'--badge',$cell.badge,'--output',"$storage/b07-analysis-$pass.json") 30 'player-smoke'|Out-Null}
    if($cell.ContainsKey('tutorial')){Step "B08-Player.$name.$pass" $PythonPath @('-B',"$ui/../DeliveryB08/Verify-Player.py",'--before',$before,'--after',$after,'--output',"$storage/b08-analysis-$pass.json") 30 'player-smoke'|Out-Null}
    $uiResult=Get-Content "$storage/ui-$pass.json" -Raw -ErrorAction SilentlyContinue|ConvertFrom-Json;if($uiResult){Note "U16.$name.$pass" $uiResult.status $uiResult.reason 'native-ui'}
   }
  }
 }else{Note 'player-matrix' 'NOT_RUN' $(if($GameplayOnly){'GameplayOnly: shutdown diagnostic matrix intentionally not repeated; historical evidence retained'}else{'Fixture/build/external worker dependency not available'}) 'native-close'}
 if($B10 -and !$EntryOnly -and $Phase -eq 'All'){
  $b10Fixture=Join-Path $data 'B10Rules/b10-rules-store';$b10Pending=Join-Path $data 'b09-menu-Pending'
  if((UnityFree) -and !$script:compileBlocked -and $script:workerReady -and (Test-Path "$b10Fixture/save.json") -and (Test-Path "$b10Pending/save.json")){
   Step 'B10.controlled-player' $pwsh @('-NoProfile','-File',"$ui/../DeliveryB10/Invoke-ControlledPlayer.ps1",'-SourceProject',$source,'-TestRoot',"$root/ControlledPlayer",'-Fixture',$b10Fixture,'-PendingFixture',$b10Pending,'-WorkerPath',$script:workerPath,'-DesktopName',$script:desktop,'-UnityPath',$UnityPath,'-ShaderCacheSource',$project) 1500 'controlled-player'|Out-Null
  }else{Note 'B10.controlled-player' NOT_RUN 'Owned fixture/build/worker dependency unavailable' 'controlled-player'}
 }
 if($B10){Step 'B10.runtime-log-gate' $PythonPath @('-B',"$ui/../DeliveryB10/Check-RuntimeLogs.py",'--run',$root,'--output',"$root/b10-runtime-log-gate.json") 60 'runtime-log-audit'|Out-Null}
 if($GameplayOnly){Note 'U16.native' 'NOT_RUN' 'No authorized independent interactive environment; gameplay checks and controlled screenshots are not native UI acceptance' 'native-ui'}
 Note 'shutdown.root-cause' 'UNRESOLVED' 'Keep original native diagnostics/dumps. No symbolized causal stack proven; no renderer/engine blame inferred from exit0 or dump absence.' 'diagnostic'
 if($Phase -eq 'All' -and $allMethods -contains 'B07ReadabilityVisual.Run'){Note 'render.first-frame-root-cause' 'UNRESOLVED' 'Earlier controlled Editor captures briefly showed solid cyan; stable-frame captures have a separate pixel assertion. Internal cause not proven; no product lifecycle or renderer patch inferred.' 'diagnostic'}
 Note 'human-usability' 'NOT_RUN' 'Requires independent real human judgment; never substituted by automation' 'human'
}catch{Note 'orchestrator.exception' 'FAIL' $_.Exception.ToString() 'orchestrator'}finally{
 foreach($child in $script:children){if($child.process.HasExited){try{FinishChild $child}catch{}}}
 $alive=@($script:children|Where-Object {!$_.process.HasExited}|ForEach-Object {@{pid=$_.process.Id;exe=$_.exe;arguments=$_.arguments}});ConvertTo-Json -InputObject $alive -Depth 5|Set-Content "$root/preserved-processes.json"
 Note 'report.finalized' 'PASS' 'Report written, not a claim that tests passed; no source reset, global settings, CI, deletion or user-process termination' 'orchestrator';Flush;Write-Host "RESULT_ROOT=$root"
}
if(@($script:results|Where-Object {$_.status -eq 'FAIL' -and $_.scope -ne 'harness-negative'}).Count){exit 1};exit 0
