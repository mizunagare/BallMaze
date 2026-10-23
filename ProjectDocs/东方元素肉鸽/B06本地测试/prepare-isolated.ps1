[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$SourceProject,[Parameter(Mandatory=$true)][string]$WorkProject,[Parameter(Mandatory=$true)][string]$ArtifactsRoot,[switch]$IncludePlayerSmoke)
$ErrorActionPreference='Stop'
$source=[IO.Path]::GetFullPath($SourceProject);$work=[IO.Path]::GetFullPath($WorkProject)
if($source -eq $work -or $work.StartsWith($source.TrimEnd('\','/')+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'WorkProject must be outside SourceProject'}
if(Test-Path -LiteralPath $work){throw 'WorkProject already exists; refusing to overwrite'}
if(Test-Path -LiteralPath $ArtifactsRoot){throw 'ArtifactsRoot already exists; choose a fresh test directory'}
New-Item -ItemType Directory -Path $work | Out-Null
foreach($part in @('Assets','Packages','ProjectSettings')){Copy-Item -LiteralPath (Join-Path $source $part) -Destination (Join-Path $work $part) -Recurse}
$editor=Join-Path $work 'Assets/CombatPrototype/Editor/B06LocalChecks';New-Item -ItemType Directory -Path $editor | Out-Null
Get-ChildItem -LiteralPath (Join-Path $PSScriptRoot 'TestSources') -Filter '*.cs.txt' | ForEach-Object {Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $editor $_.BaseName)}
if($IncludePlayerSmoke){Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'B06PlayerSmoke.cs.txt') -Destination (Join-Path $work 'Assets/B06PlayerSmoke.cs')}
New-Item -ItemType Directory -Path $ArtifactsRoot | Out-Null
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'fixtures') -Destination (Join-Path $ArtifactsRoot 'fixtures') -Recurse
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'legacy-v3') -Destination (Join-Path $ArtifactsRoot 'legacy-v3') -Recurse
Write-Host "Prepared isolated project: $work"
Write-Host "Only test data will be written under: $ArtifactsRoot"
