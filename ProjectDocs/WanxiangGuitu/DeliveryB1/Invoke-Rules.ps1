[CmdletBinding()]
param([Parameter(Mandatory)][string]$SourceProject,[Parameter(Mandatory)][string]$WorkProject,[Parameter(Mandatory)][string]$ArtifactsRoot,[switch]$HistoricalRegression)
$ErrorActionPreference='Stop'
$old=Join-Path $SourceProject 'ProjectDocs/东方元素肉鸽/B06本地测试'
& (Join-Path $old 'prepare-isolated.ps1') -SourceProject $SourceProject -WorkProject $WorkProject -ArtifactsRoot $ArtifactsRoot
$editor=Join-Path $WorkProject 'Assets/CombatPrototype/Editor/B06LocalChecks'
Get-ChildItem (Join-Path $PSScriptRoot '../DeliveryA/Tests') -Filter '*.cs.txt' | Where-Object Name -ne 'WGPlayerFlow.cs.txt' | ForEach-Object {Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $editor $_.BaseName)}
Get-ChildItem (Join-Path $PSScriptRoot 'Tests') -Filter 'WGB1*.cs.txt' | ForEach-Object {Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $editor $_.BaseName)}
Copy-Item -LiteralPath (Join-Path $old 'fixtures/v2.json') -Destination (Join-Path $ArtifactsRoot 'fixtures/container-v2.json')
Copy-Item -LiteralPath (Join-Path $PSScriptRoot '../DeliveryA/Fixtures/LegacyForestV9') -Destination (Join-Path $ArtifactsRoot 'legacy-forest-v9') -Recurse
$methods=@('WGB1Check.Run','WGB1Check.Resume','WGB1Routes.Run','WGDeliveryACheck.Run','WGLegacyForestCheck.Run','B06ForestCheck.Run','WanxiangBuild.ValidateBuild')
if($HistoricalRegression){$methods=@('WGAssetAudit.Run','WGRoutesCheck.Run','B06DropCheck.Run','B06V8MigrationCheck.Run','B05ScenarioCheck.Run','B05FaultCheck.Run','B05LegacyMigrationCheck.Run','B05V7MigrationCheck.Run','B05LiveRegression.Run','T06RegContainerRuntimeCheck.Run','T06RegContainerRuntimeCheck.Final','T06RegDualWeaponCheck.Run','T06RegWorkbenchCheck.Run','WGPotionCheck.Run','B05EditChecks.Run')+$methods}
& (Join-Path $old 'run-release.ps1') -SourceProject $SourceProject -WorkProject $WorkProject -ArtifactsRoot $ArtifactsRoot -Methods $methods -QuitMethods @('B05EditChecks.Run') -TimeoutSeconds 300
exit $LASTEXITCODE
