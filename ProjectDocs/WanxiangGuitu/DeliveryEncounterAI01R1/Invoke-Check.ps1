param([Parameter(Mandatory)][string]$Project,[Parameter(Mandatory)][string]$Output,[Parameter(Mandatory)][string]$StorageRoot,[string]$Method='EncaiR1.Run',[switch]$Graphics)
$ErrorActionPreference='Stop'
$Project=[IO.Path]::GetFullPath($Project);$Output=[IO.Path]::GetFullPath($Output);$StorageRoot=[IO.Path]::GetFullPath($StorageRoot)
if(!$Project.StartsWith('I:\WGCombat\ER1-',[StringComparison]::OrdinalIgnoreCase) -or !$Output.StartsWith('I:\WGCombat\ER1-',[StringComparison]::OrdinalIgnoreCase) -or !$StorageRoot.StartsWith('I:\WGCombat\ER1-',[StringComparison]::OrdinalIgnoreCase)){throw 'Explicit owned R1 paths required'}
if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object {$_.CommandLine.Replace('/','\').Contains($Project)}).Count){throw 'Project occupied; preserve process'}
Copy-Item -LiteralPath "$PSScriptRoot/Tests/EncaiR1.cs.txt" -Destination "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/EncaiR1.cs"
& "$PSScriptRoot/../DeliveryEncounterAI01/Invoke-Check.ps1" -Project $Project -Output $Output -StorageRoot $StorageRoot -Method $Method -NoGraphics:(!$Graphics)
$code=$LASTEXITCODE
Copy-Item -LiteralPath "$PSScriptRoot/Tests/EncaiR1.cs.txt" -Destination "$Output/EncaiR1.cs.txt"
Copy-Item -LiteralPath $PSCommandPath -Destination "$Output/Invoke-R1.executed.ps1.txt"
Copy-Item -LiteralPath "$Project/Assets/CombatPrototype/ForestBossBrain.cs" -Destination "$Output/ForestBossBrain.executed.cs"
exit $code
