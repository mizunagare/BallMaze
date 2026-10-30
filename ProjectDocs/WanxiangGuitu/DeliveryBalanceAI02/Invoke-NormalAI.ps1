param([Parameter(Mandatory)][string]$Project,[Parameter(Mandatory)][string]$RunRoot,[Parameter(Mandatory)][string]$Output,[ValidateSet('Normal','Resume','FinalResume')][string]$Mode='Normal')
$ErrorActionPreference='Stop';$Project=[IO.Path]::GetFullPath($Project);$RunRoot=[IO.Path]::GetFullPath($RunRoot)
if(!$Project.StartsWith('I:\WGCombat\BAL02-',[StringComparison]::OrdinalIgnoreCase) -or !(Test-Path (Join-Path (Split-Path $RunRoot) 'owner.json'))){throw 'Owned BAL02 project/root required'}
if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object {$_.CommandLine.Replace('/','\').Contains($Project)}).Count){throw 'Owned project occupied; preserve process'}
$checks=Join-Path $Project 'Assets/CombatPrototype/Editor/B06LocalChecks';$base=Split-Path $RunRoot;$deferred=Join-Path $base ('DriverSetup/'+[guid]::NewGuid().ToString('N'));New-Item -ItemType Directory $deferred|Out-Null
foreach($n in 'WGNormalAICheck.cs','WGA1NormalResume.cs','B06OriginalPlay.cs'){if(Test-Path "$checks/$n"){Move-Item -LiteralPath "$checks/$n" -Destination "$deferred/$n"}}
Copy-Item "$PSScriptRoot/Tests/WGNormalAICheck.cs.txt" "$checks/WGNormalAICheck.cs"
Copy-Item "$PSScriptRoot/Tests/WGA1NormalResume.cs.txt" "$checks/WGA1NormalResume.cs"
Copy-Item "$PSScriptRoot/../../东方元素肉鸽/B06本地测试/TestSources/B06OriginalPlay.cs.txt" "$checks/B06OriginalPlay.cs"
Copy-Item "$PSScriptRoot/Tests/BAL02NormalObserve.cs.txt" "$checks/BAL02NormalObserve.cs"
$method=if($Mode -eq 'Normal'){'WGNormalAICheck.Run'}else{'WGA1NormalResume.Run'}
# Existing Step launches in a non-activated private desktop. No physical Esc or kill fallback.
& "$PSScriptRoot/Invoke-Check.ps1" -Project $Project -Output $Output -StorageRoot $RunRoot -Method $method -NonBatch
exit $LASTEXITCODE
