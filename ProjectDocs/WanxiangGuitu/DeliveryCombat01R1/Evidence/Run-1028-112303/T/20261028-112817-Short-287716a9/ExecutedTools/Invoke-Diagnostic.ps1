[CmdletBinding()]
param([string]$SourceProject='D:/unity/WanxiangGuitu',[string]$TestRoot='D:/WGB01',[ValidateSet('Release','Acceptance')][string]$Variant='Release',[ValidateSet('Player02','Perf01','Combat01','CombatR1')][string]$AcceptanceProfile='Player02',
 [ValidateSet('Long','Short','Repeat')][string]$Case='Short',[int]$LongProjectLength=113,
 [string]$WorkerFrom='D:/WanxiangValidationRuns/Input01/20261027-151043-585c2866/FinalFrozenValidation/20261027-161647-ab2a444e',
 [string]$UnityPath='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe')
$ErrorActionPreference='Stop'
# Reuse the reviewed coordinator's process/timeout/isolation/receipt functions.
$entry=Join-Path $PSScriptRoot '../DeliveryUI01/Automation/Invoke-LocalValidation.ps1'
$ast=[Management.Automation.Language.Parser]::ParseFile($entry,[ref]$null,[ref]$null)
foreach($name in 'SafePath','WriteReportFile','Flush','Note','StartChild','FinishChild','Step') {
 $def=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true);Invoke-Expression $def.Extent.Text
}
$source=SafePath $SourceProject;$base=SafePath $TestRoot;$workerRoot=SafePath $WorkerFrom
if($base -eq $source -or $base.StartsWith($source+'\',[StringComparison]::OrdinalIgnoreCase) -or $base -match '(?i)[\\/]LocalLow([\\/]|$)'){throw 'External explicit test root required'}
$owner=Get-Content "$workerRoot/owner.json" -Raw|ConvertFrom-Json
if($owner.source -ne $source -or $owner.kind -ne 'WanxiangGuitu isolated unattended run'){throw 'Reviewed worker owner required'}
$root=Join-Path $base ((Get-Date -Format 'yyyyMMdd-HHmmss')+'-'+$Case+'-'+[guid]::NewGuid().ToString('N').Substring(0,8))
New-Item -ItemType Directory $root|Out-Null
$toolsDir=Join-Path $root 'ExecutedTools';New-Item -ItemType Directory $toolsDir|Out-Null
foreach($f in @($PSCommandPath,$entry,(Join-Path $PSScriptRoot '../DeliveryUI01/Invoke-Rules.ps1'),(Join-Path $PSScriptRoot 'Test-PackagePathBudget.ps1'),(Join-Path $PSScriptRoot 'Tests/Build01Audit.cs.txt'))){Copy-Item -LiteralPath $f -Destination $toolsDir}
Get-ChildItem $toolsDir -File|ForEach-Object {@{name=$_.Name;sha256=(Get-FileHash $_.FullName).Hash}}|ConvertTo-Json|Set-Content "$root/tool-hashes.json"
$project=Join-Path $root 'Project'
if($Case -eq 'Long'){$padding=$LongProjectLength-$project.Length-1;if($padding -lt 1){throw 'Long project target too short'};$project=Join-Path (Join-Path $root ('p'*$padding)) 'Project'}
$data=Join-Path $root 'Results';$pwsh=(Get-Process -Id $PID).Path
$MinimumUnityCommitGB=3;$script:results=[Collections.Generic.List[object]]::new();$script:children=[Collections.Generic.List[object]]::new()
$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$true;$script:workerPath=Join-Path $workerRoot 'Worker/NativeProbe.dll';$dotnet=(Get-Command dotnet).Source
@{kind='BUILD-01 diagnostic using existing coordinator';variant=$Variant;source=$source;head=(& git -C $source rev-parse HEAD);root=$root;project=$project;case=$Case;projectLength=$project.Length;freshLibrary=$true;utc=[datetime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content "$root/owner.json"
$prepareArgs=@('-NoProfile','-File',(Join-Path $PSScriptRoot '../DeliveryUI01/Invoke-Rules.ps1'),'-SourceProject',$source,'-WorkProject',$project,'-ArtifactsRoot',$data,'-PrepareOnly')
if($Case -eq 'Long'){$prepareArgs+='-AllowLongPackagePathsForDiagnosis'}
$prep=Step 'prepare' $pwsh $prepareArgs 240
if($prep.status -eq 'PASS'){
 Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'Tests/Build01Audit.cs.txt') -Destination "$project/Assets/CombatPrototype/Editor/B06LocalChecks/Build01Audit.cs"
 if($Variant -eq 'Acceptance'){
  # PLAYER-02 opt-in: only this freshly owned clone receives a runtime component.
  $driver=Join-Path $PSScriptRoot '../DeliveryPlayer02/Tests/PlayerAcceptanceDriver.cs.txt'
  New-Item -ItemType Directory "$project/Assets/Player02AcceptanceOnly"|Out-Null
  Copy-Item -LiteralPath $driver -Destination "$project/Assets/Player02AcceptanceOnly/PlayerAcceptanceDriver.cs"
  Copy-Item -LiteralPath $driver -Destination $toolsDir
  @{variant=$Variant;source=$driver;sha256=(Get-FileHash $driver).Hash;injected='Assets/Player02AcceptanceOnly/PlayerAcceptanceDriver.cs';scope='Disposable acceptance build only; release variant does not inject'}|ConvertTo-Json|Set-Content "$root/runtime-injection.json"
  if($AcceptanceProfile -eq 'CombatR1'){
   $target="$project/Assets/Player02AcceptanceOnly/PlayerAcceptanceDriver.cs";$code=Get-Content $target -Raw
   if(!$code.Contains('public sealed class PlayerAcceptanceDriver') -or !$code.Contains('if(mode=="Observe")')){throw 'Reviewed PLAYER02 partial fork anchors changed'}
   $code=$code.Replace('public sealed class PlayerAcceptanceDriver','public sealed partial class PlayerAcceptanceDriver').Replace('if(mode=="Observe")','if(File.Exists(Path.Combine(root,"combat-r1-config.json"))){yield return R1Run();yield break;}if(mode=="Observe")')
   Set-Content $target $code -NoNewline;Copy-Item $target "$toolsDir/R1ForkedPlayerAcceptanceDriver.cs.txt"
   $extra=Join-Path $PSScriptRoot '../DeliveryCombat01R1/Tests/R1Scenarios.cs.txt';Copy-Item $extra "$project/Assets/Player02AcceptanceOnly/R1Scenarios.cs";Copy-Item $extra $toolsDir
   @{profile=$AcceptanceProfile;sourcePlayer02Sha256=(Get-FileHash $driver).Hash;forkSha256=(Get-FileHash $target).Hash;scenarioSha256=(Get-FileHash $extra).Hash;change='Opt-in isolated partial runtime scenario; virtual attack/F5/Continue inputs; immediate audited Quit; no product inputs changed'}|ConvertTo-Json|Set-Content "$root/combat-r1-profile.json"
  }
  if($AcceptanceProfile -eq 'Combat01'){
   # Reuse the PERF01-discovered fix: respond to the real level-choice UI while harvesting.
   # No inventory/health/reward injection and no changed failure deadline.
   $target="$project/Assets/Player02AcceptanceOnly/PlayerAcceptanceDriver.cs";$code=Get-Content $target -Raw
   $anchor='while(node.Health>0){if(Threat()!=null)'
   if(($code.Split($anchor).Count-1) -ne 1){throw 'Exact reviewed harvest choice anchor changed'}
   $code=$code.Replace($anchor,'while(node.Health>0){if(s.hero.Progression.IsChoosing){Log("combat01-level-choice","real upgrade UI via Digit1");yield return Keys(Key.Digit1);continue;}if(Threat()!=null)')
   Set-Content $target $code -NoNewline;Copy-Item $target "$toolsDir/Combat01ForkedPlayerAcceptanceDriver.cs.txt"
   @{profile=$AcceptanceProfile;sourcePlayer02Sha256=(Get-FileHash $driver).Hash;forkSha256=(Get-FileHash $target).Hash;change='Handle real upgrade choice via existing input consumer; product inputs and 30-second resource failure deadline unchanged'}|ConvertTo-Json|Set-Content "$root/combat-profile.json"
  }
  if($AcceptanceProfile -eq 'Perf01'){
   $perf=Join-Path $PSScriptRoot '../DeliveryPerf01/Tests';$target="$project/Assets/Player02AcceptanceOnly/PlayerAcceptanceDriver.cs";$code=Get-Content $target -Raw
   if(!$code.Contains('public sealed class PlayerAcceptanceDriver') -or !$code.Contains('if(mode=="Observe")')){throw 'Reviewed Player02 injection anchor changed'}
   $code=$code.Replace('public sealed class PlayerAcceptanceDriver','public sealed partial class PlayerAcceptanceDriver').Replace('if(mode=="Observe")','if(File.Exists(Path.Combine(root,"perf-config.json"))){yield return PerfRun();yield break;}if(mode=="Observe")');$code=$code.Replace('while(node.Health>0){if(Threat()!=null)','while(node.Health>0){if(s.hero.Progression.IsChoosing){yield return Keys(Key.Digit1);continue;}if(Threat()!=null)');Set-Content $target $code -NoNewline
   Copy-Item $target "$toolsDir/PerfForkedPlayerAcceptanceDriver.cs.txt"
   foreach($name in 'PerfSampler','PerfScenarios'){Copy-Item "$perf/$name.cs.txt" "$project/Assets/Player02AcceptanceOnly/$name.cs";Copy-Item "$perf/$name.cs.txt" $toolsDir}
   $audit="$project/Assets/CombatPrototype/Editor/B06LocalChecks/Build01Audit.cs";$c=Get-Content $audit -Raw;$c=$c.Replace('string root=Root();Inspect(root,"asset-before.json");','string root=Root();PlayerSettings.enableFrameTimingStats=true;File.WriteAllText(Path.Combine(root,"perf-instrumentation-settings.json"),"FrameTimingStats=true; isolated acceptance only; BuildOptions.None");Inspect(root,"asset-before.json");');Set-Content $audit $c -NoNewline;Copy-Item $audit "$toolsDir/PerfBuild01Audit.cs.txt"
   @{profile=$AcceptanceProfile;sourcePlayer02Sha256=(Get-FileHash $driver).Hash;forkSha256=(Get-FileHash $target).Hash;change='Only isolated test sources and enableFrameTimingStats in owned clone; no product source edit'}|ConvertTo-Json|Set-Content "$root/perf-profile.json"
  }
 }
 $files=@('Packages/manifest.json','Packages/packages-lock.json','ProjectSettings/ProjectVersion.txt','ProjectSettings/ProjectSettings.asset','Assets/CombatPrototype/ForestRuins.unity')
 $hashes=foreach($f in $files){@{path=$f;source=(Get-FileHash -LiteralPath (Join-Path $source $f)).Hash;copy=(Get-FileHash -LiteralPath (Join-Path $project $f)).Hash}}
 $hashes|ConvertTo-Json|Set-Content "$root/input-hashes.json"
 if(@($hashes|Where-Object {$_.source -ne $_.copy}).Count){throw 'Input copy mismatch'}
 $manifest=foreach($folder in 'Assets','Packages','ProjectSettings'){Get-ChildItem -LiteralPath (Join-Path $source $folder) -File -Recurse|ForEach-Object {$relative=[IO.Path]::GetRelativePath($source,$_.FullName);@{path=$relative;source=(Get-FileHash -LiteralPath $_.FullName).Hash;copy=(Get-FileHash -LiteralPath (Join-Path $project $relative)).Hash}}}
 $manifest|ConvertTo-Json|Set-Content "$root/copied-source-files.json"
 if(@($manifest|Where-Object {$_.source -ne $_.copy}).Count){throw 'Full source clone mismatch'}
 $r=Step 'Build01Audit.Run' $UnityPath @('-batchmode','-projectPath',$project,'-wanxiang-storage-root',$data,'-executeMethod','Build01Audit.Run','-logFile',"$data/Build01Audit.Run.log") 1200 controlled $data
}
ConvertTo-Json -InputObject @($script:children|Where-Object {!$_.process.HasExited}|ForEach-Object {$_.process.Id})|Set-Content "$root/preserved-processes.json"
Flush;Write-Output "RESULT_ROOT=$root"
if(@($script:results|Where-Object status -eq 'FAIL').Count){exit 1};exit 0
