param([Parameter(Mandatory)][string]$Project,[Parameter(Mandatory)][string]$Output,[string]$Method='Combat03Bench.Run')
$ErrorActionPreference='Stop'
if(!(Test-Path -LiteralPath (Join-Path ([IO.DirectoryInfo]$Project).Parent.Parent.FullName 'owner.json'))){throw 'Owned isolated root required'}
if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'" | Where-Object CommandLine -Like "*$Project*").Count){throw 'Occupied project preserved'}
$editor=Join-Path $Project 'Assets/CombatPrototype/Editor/B06LocalChecks'
$inputs=@(Get-ChildItem "$PSScriptRoot/Tests" -Filter '*.cs.txt')
$frozen=Join-Path (Split-Path $Output) ('Inputs-'+(Split-Path $Output -Leaf))
New-Item -ItemType Directory -Path $frozen -ErrorAction Stop|Out-Null
foreach($f in $inputs){Copy-Item -LiteralPath $f.FullName -Destination (Join-Path $editor $f.BaseName)}
foreach($f in $inputs){Copy-Item -LiteralPath (Join-Path $editor $f.BaseName) -Destination (Join-Path $frozen ('Executed-'+$f.Name))}
Get-ChildItem $frozen -File|Get-FileHash -Algorithm SHA256|Select-Object Path,Hash|ConvertTo-Json|Set-Content (Join-Path $frozen 'hashes.json')
& (Join-Path $PSScriptRoot '../DeliveryCombat02/Invoke-Combat02.ps1') -Project $Project -Output $Output -Method $Method
$code=$LASTEXITCODE
Get-ChildItem $frozen -File|ForEach-Object {Copy-Item -LiteralPath $_.FullName -Destination (Join-Path $Output $_.Name)}
exit $code
