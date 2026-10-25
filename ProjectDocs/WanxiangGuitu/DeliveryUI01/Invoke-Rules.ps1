[CmdletBinding()]
param([Parameter(Mandatory)][string]$SourceProject,[Parameter(Mandatory)][string]$WorkProject,[Parameter(Mandatory)][string]$ArtifactsRoot,[switch]$HistoricalRegression,[int]$TimeoutSeconds=600,[switch]$PrepareOnly)
$ErrorActionPreference='Stop'
foreach($path in @($WorkProject,$ArtifactsRoot)){if(![IO.Path]::IsPathFullyQualified($path) -or [IO.Path]::GetFullPath($path) -match '(?i)(^|[\\/])LocalLow([\\/]|$)'){throw 'Explicit isolated work/results paths outside LocalLow required'}}
$old=Join-Path $SourceProject 'ProjectDocs/东方元素肉鸽/B06本地测试'
& (Join-Path $old 'prepare-isolated.ps1') -SourceProject $SourceProject -WorkProject $WorkProject -ArtifactsRoot $ArtifactsRoot
$editor=Join-Path $WorkProject 'Assets/CombatPrototype/Editor/B06LocalChecks'
foreach($folder in @('../DeliveryA/Tests','../DeliveryA1/Tests','Tests')){Get-ChildItem (Join-Path $PSScriptRoot $folder) -Filter '*.cs.txt' | Where-Object Name -ne 'WGPlayerFlow.cs.txt' | ForEach-Object {Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $editor $_.BaseName)}}
Get-ChildItem (Join-Path $PSScriptRoot '../DeliveryB1/Tests') -Filter 'WGB1*.cs.txt' | ForEach-Object {Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $editor $_.BaseName)}
Copy-Item -LiteralPath (Join-Path $old 'fixtures/v2.json') -Destination (Join-Path $ArtifactsRoot 'fixtures/container-v2.json')
Copy-Item -LiteralPath (Join-Path $PSScriptRoot '../DeliveryA/Fixtures/LegacyForestV9') -Destination (Join-Path $ArtifactsRoot 'legacy-forest-v9') -Recurse
$root=[IO.Path]::GetFullPath($ArtifactsRoot)
$target=Join-Path $root 'reparse-target';New-Item -ItemType Directory $target | Out-Null
[IO.File]::WriteAllText((Join-Path $target 'sentinel'),'untouched')
New-Item -ItemType Junction -Path (Join-Path $root 'reparse-location') -Value $target | Out-Null
$dangling=Join-Path $root 'dangling-target';$preserved=Join-Path $root 'dangling-target-preserved'
foreach($path in @($dangling,$preserved)){if(![IO.Path]::GetFullPath($path).StartsWith($root+[IO.Path]::DirectorySeparatorChar)){throw 'Invalid local fixture move'}}
New-Item -ItemType Directory $dangling | Out-Null
New-Item -ItemType Junction -Path (Join-Path $root 'reparse-dangling') -Value $dangling | Out-Null
Move-Item -LiteralPath $dangling -Destination $preserved
$methods=@('WGB1Check.Run','WGB1Check.Resume','WGB1Routes.Run','WGDeliveryACheck.Run','WGLegacyForestCheck.Run','B06ForestCheck.Run','WanxiangBuild.ValidateBuild')
if($HistoricalRegression){$methods=@('WGAssetAudit.Run','WGRoutesCheck.Run','B06DropCheck.Run','B06V8MigrationCheck.Run','B05ScenarioCheck.Run','B05FaultCheck.Run','B05LegacyMigrationCheck.Run','B05V7MigrationCheck.Run','B05LiveRegression.Run','T06RegContainerRuntimeCheck.Run','T06RegContainerRuntimeCheck.Final','T06RegDualWeaponCheck.Run','T06RegWorkbenchCheck.Run','WGPotionCheck.Run','B05EditChecks.Run')+$methods}
Get-ChildItem (Join-Path $PSScriptRoot '../DeliveryB2/Tests') -Filter 'B2*.cs.txt' | ForEach-Object {Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $editor $_.BaseName)}
Get-ChildItem (Join-Path $PSScriptRoot '../DeliveryB3/Tests') -Filter '*.cs.txt' | ForEach-Object {Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $editor $_.BaseName)}
Get-ChildItem (Join-Path $PSScriptRoot '../DeliveryB4/Tests') -Filter '*.cs.txt' | ForEach-Object {Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $editor $_.BaseName)}
Get-ChildItem (Join-Path $PSScriptRoot '../DeliveryB4-R1/Tests') -Filter '*.cs.txt' | ForEach-Object {Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $editor $_.BaseName)}
Copy-Item -LiteralPath (Join-Path $PSScriptRoot '../DeliveryB4-R1/Fixtures/layout-revision4.json') -Destination (Join-Path $ArtifactsRoot 'r1-legacy-layout4.json')
$methods+=@('RouteScoringProbe.Run','RouteScoringRules.Run','RouteScoringRules.Resume','R1Audit.Run','R1Shore.Run','R1Rules.Run','R1Rules.Resume','B4Checks.Topology','B4Physics.Run','B4StateRules.Run','B4PickupRules.Run','B3StreamRules.Run','B3Checks.Run','B3Checks.Resume','B2Rules.Run','B2Rules.Resume','WGA1Check.Isolation','WGA1Check.Choice','WGA1Check.Empty','WGA1Check.Recovery','WGA1ExtendedCheck.Matrix','WGA1ExtendedCheck.InterruptedWrite','WGA1ExtendedCheck.InterruptedResume','UI01Rules.Run')
Get-ChildItem (Join-Path $PSScriptRoot '../DeliveryB07/Tests') -Filter '*.cs.txt' | ForEach-Object {Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $editor $_.BaseName)}
$methods+=@('B07Probe.Run','B07SeedReplay.Run','B07Rules.Run','B07Rules.Resume','B07Rules.PendingResume','B07Rules.CommittedResume','B07Combat.Run','B07Interruptions.Run','B07Economy.Run','B07Liveness.Run')
Get-ChildItem (Join-Path $PSScriptRoot '../DeliveryB07-R1/Tests') -Filter '*.cs.txt' | ForEach-Object {Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $editor $_.BaseName)}
$methods+=@('B07ReadabilityProbe.Run','B07ReadabilityRules.Run','B07ReadabilityVisual.Run','B07OcclusionProbe.Run','B07ActorOcclusion.Run')
if($PrepareOnly){$methods | ConvertTo-Json | Set-Content (Join-Path $ArtifactsRoot 'method-plan.json');return}
& (Join-Path $old 'run-release.ps1') -SourceProject $SourceProject -WorkProject $WorkProject -ArtifactsRoot $ArtifactsRoot -Methods $methods -QuitMethods @('B05EditChecks.Run') -TimeoutSeconds $TimeoutSeconds
exit $LASTEXITCODE
