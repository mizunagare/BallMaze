[CmdletBinding()]
param([string]$SourceProject='D:/unity/WanxiangGuitu',[string]$TestRoot='D:/WGB01',[ValidateSet('Release','Acceptance')][string]$Variant='Release',
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
