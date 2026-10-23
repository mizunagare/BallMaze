[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$SourceProject,[Parameter(Mandatory=$true)][string]$WorkProject,[Parameter(Mandatory=$true)][string]$ArtifactsRoot)
$ErrorActionPreference='Stop'
& (Join-Path $PSScriptRoot '../DeliveryA/Invoke-DeliveryA.ps1') -SourceProject $SourceProject -WorkProject $WorkProject -ArtifactsRoot $ArtifactsRoot -PlayerProcesses
if($LASTEXITCODE -ne 0){exit $LASTEXITCODE}
$editor=Join-Path $WorkProject 'Assets/CombatPrototype/Editor/B06LocalChecks'
Get-ChildItem (Join-Path $PSScriptRoot 'Tests') -Filter '*.cs.txt' | ForEach-Object {Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $editor $_.BaseName)}
$target=Join-Path $ArtifactsRoot 'reparse-target';New-Item -ItemType Directory $target | Out-Null
[IO.File]::WriteAllText((Join-Path $target 'sentinel'),'untouched')
New-Item -ItemType Junction -Path (Join-Path $ArtifactsRoot 'reparse-location') -Value $target | Out-Null
$danglingTarget=[IO.Path]::GetFullPath((Join-Path $ArtifactsRoot 'dangling-target'));$moved=[IO.Path]::GetFullPath((Join-Path $ArtifactsRoot 'dangling-target-preserved'))
if(!$danglingTarget.StartsWith([IO.Path]::GetFullPath($ArtifactsRoot)+[IO.Path]::DirectorySeparatorChar) -or !$moved.StartsWith([IO.Path]::GetFullPath($ArtifactsRoot)+[IO.Path]::DirectorySeparatorChar)){throw 'Invalid junction fixture paths'}
New-Item -ItemType Directory $danglingTarget | Out-Null
New-Item -ItemType Junction -Path (Join-Path $ArtifactsRoot 'reparse-dangling') -Value $danglingTarget | Out-Null
Move-Item -LiteralPath $danglingTarget -Destination $moved
& (Join-Path $SourceProject 'ProjectDocs/东方元素肉鸽/B06本地测试/run-release.ps1') -SourceProject $SourceProject -WorkProject $WorkProject -ArtifactsRoot $ArtifactsRoot -Methods @('WGA1Check.Isolation','WGA1Check.Choice','WGA1Check.Empty','WGA1Check.Recovery','WGA1ExtendedCheck.Matrix','WGA1ExtendedCheck.InterruptedWrite','WGA1ExtendedCheck.InterruptedResume') -TimeoutSeconds 180
exit $LASTEXITCODE
