param([Parameter(Mandatory)][string]$Project,[Parameter(Mandatory)][string]$Output,[string]$StorageRoot='',[string]$Method='CP03Editor.Run',[switch]$Graphics,[switch]$NonBatch)
$ErrorActionPreference='Stop';$Project=[IO.Path]::GetFullPath($Project);$Output=[IO.Path]::GetFullPath($Output)
if(!$Project.StartsWith('I:\WGCombat\CP03-',[StringComparison]::OrdinalIgnoreCase) -or !$Output.StartsWith('I:\WGCombat\CP03-',[StringComparison]::OrdinalIgnoreCase)){throw 'Owned UX-TECH paths required'}
if(!$StorageRoot){$StorageRoot=$Output}
if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object {$_.CommandLine.Replace('/','\').Contains($Project)}).Count){throw 'Project occupied; preserve process'}
foreach($n in 'CP03Cases','CP03Editor'){Copy-Item "$PSScriptRoot/Tests/$n.cs.txt" "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/$n.cs"}
& "$PSScriptRoot/../DeliveryEncounterAI01/Invoke-Check.ps1" -Project $Project -Output $Output -StorageRoot $StorageRoot -Method $Method -NoGraphics:(!$Graphics) -NonBatch:$NonBatch
$code=$LASTEXITCODE
foreach($n in 'CP03Cases','CP03Editor'){Copy-Item "$PSScriptRoot/Tests/$n.cs.txt" "$Output/$n.executed.cs.txt"}
foreach($n in 'CombatFeedback','FantasyActorVisual','CombatFeedbackEffect','AdventureCombat','CombatHealth'){Copy-Item "$Project/Assets/CombatPrototype/$n.cs" "$Output/$n.executed.cs"}
Copy-Item $PSCommandPath "$Output/Invoke-Editor.executed.ps1.txt"
exit $code
