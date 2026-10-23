[CmdletBinding()]
param(
 [Parameter(Mandatory=$true)][string]$SourceProject,
 [Parameter(Mandatory=$true)][string]$WorkProject,
 [Parameter(Mandatory=$true)][string]$ArtifactsRoot,
 [string]$UnityPath='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe',
 [switch]$PlayerProcesses
)
$ErrorActionPreference='Stop'
$source=[IO.Path]::GetFullPath($SourceProject)
$work=[IO.Path]::GetFullPath($WorkProject)
$artifacts=[IO.Path]::GetFullPath($ArtifactsRoot)
$localLow=Join-Path ([Environment]::GetFolderPath('UserProfile')) 'AppData/LocalLow'
foreach($path in @($work,$artifacts)){
 if($path.StartsWith($localLow,[StringComparison]::OrdinalIgnoreCase)){throw 'Never use player storage for test data'}
 if($path -eq $source -or $path.StartsWith($source.TrimEnd('\','/')+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Use fresh directories outside the source project'}
}
if($work -eq $artifacts -or $artifacts.StartsWith($work.TrimEnd('\','/')+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Separate work and result directories required'}
$old=Join-Path $source 'ProjectDocs/东方元素肉鸽/B06本地测试'
& (Join-Path $old 'prepare-isolated.ps1') -SourceProject $source -WorkProject $work -ArtifactsRoot $artifacts
$editor=Join-Path $work 'Assets/CombatPrototype/Editor/B06LocalChecks'
Get-ChildItem (Join-Path $PSScriptRoot 'Tests') -Filter '*.cs.txt' | Where-Object Name -ne 'WGPlayerFlow.cs.txt' | ForEach-Object {Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $editor $_.BaseName)}
Copy-Item -LiteralPath (Join-Path $old 'fixtures/v2.json') -Destination (Join-Path $artifacts 'fixtures/container-v2.json')
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'Fixtures/LegacyForestV9') -Destination (Join-Path $artifacts 'legacy-forest-v9') -Recurse
$methods=@('WGDeliveryACheck.Run','WGLegacyForestCheck.Run','WGAssetAudit.Run','WGRoutesCheck.Run','B06DropCheck.Run','B06ForestCheck.Run','B06V8MigrationCheck.Run','B05ScenarioCheck.Run','B05FaultCheck.Run','B05LegacyMigrationCheck.Run','B05V7MigrationCheck.Run','B05LiveRegression.Run','T06RegContainerRuntimeCheck.Run','T06RegContainerRuntimeCheck.Final','T06RegDualWeaponCheck.Run','T06RegWorkbenchCheck.Run','WGPotionCheck.Run','B05EditChecks.Run','WanxiangBuild.ValidateBuild')
& (Join-Path $old 'run-release.ps1') -UnityPath $UnityPath -SourceProject $source -WorkProject $work -ArtifactsRoot $artifacts -Methods $methods -QuitMethods @('B05EditChecks.Run') -TimeoutSeconds 300
if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}
# Release above contains no runtime validation driver. Optional variant is built separately.
if($PlayerProcesses){
 Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'Tests/WGPlayerFlow.cs.txt') -Destination (Join-Path $work 'Assets/WGPlayerFlow.cs')
 $variant=Join-Path $artifacts 'PlayerVariant'
 & (Join-Path $old 'run-release.ps1') -UnityPath $UnityPath -SourceProject $source -WorkProject $work -ArtifactsRoot $variant -Methods @('WanxiangBuild.ValidateBuild') -TimeoutSeconds 300
 if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}
 $root=Join-Path $artifacts 'PlayerFlow';New-Item -ItemType Directory $root | Out-Null
 $results=@()
 foreach($mode in @('zero-save','zero-resume','terminal-resume')){
  $proc=Start-Process -FilePath (Join-Path $variant 'Release/WanxiangGuitu.exe') -ArgumentList @('-batchmode','-wg-validation-root',('"'+$root+'"'),$mode,'-logFile',('"'+$root+'/'+$mode+'.log"')) -WindowStyle Hidden -PassThru
  $timeout=!$proc.WaitForExit(90000);if($timeout){$proc.Kill();$proc.WaitForExit()}
  $results+=@{mode=$mode;exitCode=$proc.ExitCode;timedOut=$timeout}
  $results | ConvertTo-Json | Set-Content (Join-Path $artifacts 'player-process-results.json') -Encoding utf8
  if($timeout -or $proc.ExitCode -ne 0){exit 1}
 }
}
