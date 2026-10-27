[CmdletBinding()]
param([string]$SourceProject='D:/unity/WanxiangGuitu',[string]$TestRoot='D:/WGB01',
 [ValidateSet('Long','Short','Repeat')][string]$Case='Short',[int]$LongProjectLength=104,
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
$project=Join-Path $root 'Project'
if($Case -eq 'Long'){$padding=$LongProjectLength-$project.Length-1;if($padding -lt 1){throw 'Long project target too short'};$project=Join-Path (Join-Path $root ('p'*$padding)) 'Project'}
$data=Join-Path $root 'Results';$pwsh=(Get-Process -Id $PID).Path
$MinimumUnityCommitGB=3;$script:results=[Collections.Generic.List[object]]::new();$script:children=[Collections.Generic.List[object]]::new()
$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$true;$script:workerPath=Join-Path $workerRoot 'Worker/NativeProbe.dll';$dotnet=(Get-Command dotnet).Source
@{kind='BUILD-01 diagnostic using existing coordinator';source=$source;root=$root;project=$project;case=$Case;projectLength=$project.Length;freshLibrary=$true;utc=[datetime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content "$root/owner.json"
$prep=Step 'prepare' $pwsh @('-NoProfile','-File',(Join-Path $PSScriptRoot '../DeliveryUI01/Invoke-Rules.ps1'),'-SourceProject',$source,'-WorkProject',$project,'-ArtifactsRoot',$data,'-PrepareOnly') 240
if($prep.status -eq 'PASS'){
 Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'Tests/Build01Audit.cs.txt') -Destination "$project/Assets/CombatPrototype/Editor/B06LocalChecks/Build01Audit.cs"
 $files=@('Packages/manifest.json','Packages/packages-lock.json','ProjectSettings/ProjectVersion.txt','ProjectSettings/ProjectSettings.asset','Assets/CombatPrototype/ForestRuins.unity')
 $hashes=foreach($f in $files){@{path=$f;source=(Get-FileHash -LiteralPath (Join-Path $source $f)).Hash;copy=(Get-FileHash -LiteralPath (Join-Path $project $f)).Hash}}
 $hashes|ConvertTo-Json|Set-Content "$root/input-hashes.json"
 if(@($hashes|Where-Object {$_.source -ne $_.copy}).Count){throw 'Input copy mismatch'}
 $r=Step 'Build01Audit.Run' $UnityPath @('-batchmode','-projectPath',$project,'-wanxiang-storage-root',$data,'-executeMethod','Build01Audit.Run','-logFile',"$data/Build01Audit.Run.log") 1200 controlled $data
}
ConvertTo-Json -InputObject @($script:children|Where-Object {!$_.process.HasExited}|ForEach-Object {$_.process.Id})|Set-Content "$root/preserved-processes.json"
Flush;Write-Output "RESULT_ROOT=$root"
if(@($script:results|Where-Object status -eq 'FAIL').Count){exit 1};exit 0
