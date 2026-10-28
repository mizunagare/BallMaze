param([Parameter(Mandatory)][string]$Project,[Parameter(Mandatory)][string]$RunRoot,[string]$WorkerPath='I:/WGP2/1028-080504-eef74f/Runtime/Worker/NativeProbe.dll',[int]$Processes=3,[string]$Phase="Observed",[switch]$ReadyGate,[switch]$StableFixture)
$ErrorActionPreference='Stop';$RunRoot=[IO.Path]::GetFullPath($RunRoot);$Project=[IO.Path]::GetFullPath($Project)
if(!$RunRoot.StartsWith('I:\WGCombat\',[StringComparison]::OrdinalIgnoreCase) -or !(Test-Path "$RunRoot/owner.json") -or !$Project.StartsWith($RunRoot+[IO.Path]::DirectorySeparatorChar)){throw 'Owned isolated project required'}
if($Processes -lt 1 -or $Processes -gt 3){throw 'Bounded one to three processes only'}
$pw=(Get-Process -Id $PID).Path;$entry=Join-Path $PSScriptRoot '../DeliveryCombat01/Invoke-Checks.ps1';$summary=@();if($Phase -notmatch "^[A-Za-z0-9-]+$"){throw "Invalid phase"};$phaseRoot=Join-Path $RunRoot $Phase;New-Item -ItemType Directory $phaseRoot -ErrorAction Stop|Out-Null
for($i=1;$i -le $Processes;$i++){
 if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){throw 'Project occupied; preserved'}
 $output="$phaseRoot/Runs/$('{0:00}' -f $i)";$storage="$phaseRoot/Stores/$('{0:00}' -f $i)";New-Item -ItemType Directory $storage -ErrorAction Stop|Out-Null
 $editor="$Project/Assets/CombatPrototype/Editor/B06LocalChecks";Copy-Item (Join-Path $PSScriptRoot $(if($StableFixture){"Tests/B07RulesStable.cs.txt"}elseif($ReadyGate){"Tests/B07RulesReady.cs.txt"}else{"Tests/B07RulesObserved.cs.txt"})) "$editor/B07Rules.cs";Copy-Item "$PSScriptRoot/Tests/C02R1Trace.cs.txt" "$editor/C02R1Trace.cs"
 & $pw -NoProfile -File $entry -Project $Project -Output $output -StorageRoot $storage -Method B07Rules.Run -WorkerPath $WorkerPath
 $exitCode=$LASTEXITCODE
 Copy-Item "$editor/B07Rules.cs" "$output/Executed-B07Rules.cs.txt";Copy-Item "$editor/C02R1Trace.cs" "$output/Executed-C02R1Trace.cs.txt"
 $summary+=@{attempt=$i;exitCode=$exitCode;output=$output;storage=$storage};$summary|ConvertTo-Json -Depth 5|Set-Content "$phaseRoot/process-summary.json" -Encoding utf8
 # A timed-out process is preserved and prevents dependent reuse, never killed.
 if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){throw 'Child remains alive; no further processes launched'}
}
if(@($summary|Where-Object exitCode -ne 0).Count){exit 1};exit 0
