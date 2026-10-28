[CmdletBinding()]
param([Parameter(Mandatory)][string]$Root)
$ErrorActionPreference='Stop';$rows=[Collections.Generic.List[object]]::new();$builds=@{}
if(Test-Path "$Root/matrix-results.json"){throw 'Existing matrix preserved; new run root required'}
foreach($v in @('A','B','C')){$b=Get-ChildItem "$Root/$v" -Directory|Sort-Object Name|Select-Object -Last 1;if(!$b -or !(Test-Path "$($b.FullName)/Build01Audit.Run.exit.json") -or (Get-Content "$($b.FullName)/Build01Audit.Run.exit.json" -Raw|ConvertFrom-Json).exitCode -ne 0){throw "Build $v incomplete; no measurement during build"};$builds[$v]=$b.FullName}
function RunOne($variant,$scenario,$rep){$start=[datetime]::UtcNow;$status='FAIL';$why='';$exitCode=$null;try{& "$PSScriptRoot/Invoke-Perf02Case.ps1" -Root $Root -BuildRoot $builds[$variant] -Scenario $scenario -Repetition $rep|Out-Host;$exitCode=$LASTEXITCODE;if($exitCode -eq 0){$status='PASS'}}catch{$why=$_.Exception.ToString()};$rows.Add([pscustomobject]@{variant=$variant;scenario=$scenario;repetition=$rep;status=$status;exitCode=$exitCode;reason=$why;start=$start.ToString('o');end=[datetime]::UtcNow.ToString('o')});$rows|ConvertTo-Json -Depth 5|Set-Content "$Root/matrix-results.json";$rows|Export-Csv "$Root/matrix-results.csv" -NoTypeInformation}
# Capability probes are separate experiments, not samples of zero-cost product GC.
for($i=1;$i -le 3;$i++){RunOne C Probe $i}
foreach($group in @(@('A','B','C'),@('B','C','A'),@('C','A','B'))){$rep=1+@($rows|Where-Object {$_.variant -eq 'A' -and $_.scenario -eq 'Title'}).Count;foreach($v in $group){RunOne $v Title $rep}}
@{utc=[datetime]::UtcNow.ToString('o');complete=$true;meaning='All attempts independently recorded, not availability or performance budget inference'}|ConvertTo-Json|Set-Content "$Root/matrix-complete.json"
if(@($rows|Where-Object status -eq FAIL).Count){exit 1};exit 0
