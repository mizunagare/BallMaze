param([Parameter(Mandatory)][string]$Project,[Parameter(Mandatory)][string]$Output,[string]$StorageRoot='',[string]$Method='GUXEditor.Run',[switch]$Graphics,[switch]$NonBatch)
$ErrorActionPreference='Stop';$Project=[IO.Path]::GetFullPath($Project);$Output=[IO.Path]::GetFullPath($Output)
if(!$Project.StartsWith('I:\WGCombat\GU02-',[StringComparison]::OrdinalIgnoreCase) -or !$Output.StartsWith('I:\WGCombat\GU02-',[StringComparison]::OrdinalIgnoreCase)){throw 'Owned UX-TECH paths required'}
if(!$StorageRoot){$StorageRoot=$Output}
if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object {$_.CommandLine.Replace('/','\').Contains($Project)}).Count){throw 'Project occupied; preserve process'}
foreach($n in 'GUXCases','GUXEditor'){Copy-Item "$PSScriptRoot/Tests/$n.cs.txt" "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/$n.cs"}
& "$PSScriptRoot/../DeliveryEncounterAI01/Invoke-Check.ps1" -Project $Project -Output $Output -StorageRoot $StorageRoot -Method $Method -NoGraphics:(!$Graphics) -NonBatch:$NonBatch
$code=$LASTEXITCODE
foreach($n in 'GUXCases','GUXEditor'){Copy-Item "$PSScriptRoot/Tests/$n.cs.txt" "$Output/$n.executed.cs.txt"}
foreach($n in 'CombatFeedback','FantasyActorVisual','CombatFeedbackEffect','CombatHealth'){Copy-Item "$Project/Assets/CombatPrototype/$n.cs" "$Output/$n.executed.cs"}
Copy-Item $PSCommandPath "$Output/Invoke-Editor.executed.ps1.txt"
exit $code
