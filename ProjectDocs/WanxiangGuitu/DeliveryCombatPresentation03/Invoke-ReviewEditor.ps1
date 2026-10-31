param([Parameter(Mandatory)][string]$Project,[Parameter(Mandatory)][string]$Output,[switch]$Diagnosis)
$ErrorActionPreference='Stop'
$Project=[IO.Path]::GetFullPath($Project);$Output=[IO.Path]::GetFullPath($Output)
if(!$Project.StartsWith('I:\WGCombat\CP03-R1-',[StringComparison]::OrdinalIgnoreCase) -or !$Output.StartsWith('I:\WGCombat\CP03-R1-',[StringComparison]::OrdinalIgnoreCase)){throw 'Owned CP03 R1 root required'}
if($Diagnosis){Copy-Item "$PSScriptRoot/Tests/CP03Cases-Diagnosis.cs.txt" "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/CP03Cases.cs";Copy-Item "$PSScriptRoot/Tests/CP03Editor.cs.txt" "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/CP03Editor.cs"}
if($Diagnosis){& "$PSScriptRoot/../DeliveryEncounterAI01/Invoke-Check.ps1" -Project $Project -Output $Output -Method CP03Editor.Run -NonBatch}
else{& "$PSScriptRoot/Invoke-Editor.ps1" -Project $Project -Output $Output -Graphics -NonBatch}
$launcherExit=$LASTEXITCODE
Copy-Item "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/CP03Cases.cs" "$Output/CP03Cases.executed.cs.txt"
Copy-Item $PSCommandPath "$Output/Invoke-ReviewEditor.executed.ps1.txt"
$rows=@(Get-Content "$Output/results.json" -Raw|ConvertFrom-Json);$process=@($rows|Where-Object name -eq CP03Editor.Run)
if($process.Count -ne 1){throw 'Exactly one Editor process receipt required'}
$r=$process[0];$python=(Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe')
Copy-Item -LiteralPath "$Output/results.json" -Destination "$Output/process-results.json" -ErrorAction Stop
@{kind='verbatim actual runner snapshot before semantic append';source="$Output/results.json";snapshot="$Output/process-results.json";sourceSHA256AtSnapshot=(Get-FileHash -LiteralPath "$Output/results.json").Hash;snapshotSHA256=(Get-FileHash -LiteralPath "$Output/process-results.json").Hash;utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content "$Output/process-origin.json"
$args2=@("$PSScriptRoot/Receipt.py",'--receipt',"$Output/presentation.json",'--output',"$Output/Semantic",'--profile','Editor','--contract',"$PSScriptRoot/../DeliveryCombatPresentation03R11/Contracts/Editor.json",'--process-receipt',"$Output/process-results.json",'--exit-receipt',"$Output/CP03Editor.Run.exit.json",'--command-receipt',"$Output/CP03Editor.Run.command.json",'--process-origin',"$Output/process-origin.json",'--desktop-receipt',"$Output/CP03Editor.Run.desktop-process.json")
if($launcherExit -ne 0){$args2+='--external-failure'}
& $python @args2
$semanticExit=$LASTEXITCODE
$q=Get-Content "$Output/Semantic/acceptance.json" -Raw|ConvertFrom-Json
Add-Content "$Output/REPORT.md" "`nOverall semantic acceptance: **$($q.overallStatus)** (classifier exit $semanticExit). See [semantic report](Semantic/REPORT.md)."
exit $semanticExit
