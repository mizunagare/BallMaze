[CmdletBinding()]
param([Parameter(Mandatory)][string]$Root,[Parameter(Mandatory)][string]$OriginalBuild,[Parameter(Mandatory)][string]$HarvestFixBuild)
$ErrorActionPreference='Stop';$rows=[Collections.Generic.List[object]]::new();$repo=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..'));$runtime=Join-Path $Root 'Runtime'
if((Get-Content "$Root/owner.json" -Raw|ConvertFrom-Json).kind -ne 'PERF-01 isolated measurements'){throw 'Owned root required'}
if(Test-Path "$Root/recovery-results.json"){throw 'Recovery receipts already exist; use a fresh owned run, never overwrite history'}
foreach($b in @($OriginalBuild,$HarvestFixBuild)){if((Get-Content "$b/Build01Audit.Run.exit.json" -Raw|ConvertFrom-Json).exitCode -ne 0){throw 'Completed successful build required'}}
$fixture=Join-Path $repo 'ProjectDocs/WanxiangGuitu/DeliveryPlayer02/Evidence/Run-1027-205135/Attempts/220103-Successor-bb698c/StorageAfter/WanxiangGuitu'
function RunOne($scenario,$n,$inputFixture,$seconds,$build,$off=$false){
 $start=[datetime]::UtcNow;$storage='';$status='FAIL';$why='';$code=$null
 try{& "$PSScriptRoot/Invoke-PerfCase.ps1" -Root $Root -BuildRoot $build -Scenario $scenario -Repetition $n -Fixture $inputFixture -Seconds $seconds -SamplingOff:$off | Out-Host;$code=$LASTEXITCODE
  $d=Get-ChildItem "$runtime/Cases" -Directory|Where-Object {(Test-Path "$($_.FullName)/perf-config.json") -and (Get-Item "$($_.FullName)/perf-config.json").LastWriteTimeUtc -ge $start}|Sort-Object LastWriteTimeUtc -Descending|Select-Object -First 1
  if($d){$storage=$d.FullName};if($d -and (Test-Path "$storage/case-result.json") -and $code -eq 0){$status='PASS'}else{$why='Case failure or missing completion receipt; see original attempt'}
 }catch{$why=$_.Exception.ToString()}
 $rows.Add([pscustomobject]@{scenario=$scenario;repetition=$n;samplingOff=$off;status=$status;exitCode=$code;storage=$storage;build=$build;reason=$why;start=$start.ToString('o');end=[datetime]::UtcNow.ToString('o')});$rows|ConvertTo-Json -Depth 5|Set-Content "$Root/recovery-results.json";$rows|Export-Csv "$Root/recovery-results.csv" -NoTypeInformation
 if($status -eq 'PASS'){return $storage};return ''
}
# Original build for unchanged scenarios: only the post-exit file-sharing defect changed.
$null=RunOne 'Title' 1 '' 60 $OriginalBuild;$null=RunOne 'Title' 1 '' 60 $OriginalBuild $true;$null=RunOne 'Movement' 1 $fixture 120 $OriginalBuild
# All gather repeats use the same rebuilt temporary driver, with real Digit1 skill selection.
$prep=RunOne 'PrepareFerry' 0 $fixture 0 $HarvestFixBuild
for($n=1;$n -le 3;$n++){$null=RunOne 'Gather' $n $fixture 120 $HarvestFixBuild}
$successor=''
for($n=1;$n -le 3;$n++){
 if($prep){$loop=RunOne 'Loop' $n (Join-Path $prep 'WanxiangGuitu') 180 $HarvestFixBuild;if(!$successor -and $loop){$successor=Join-Path $loop 'WanxiangGuitu'}}
 else{$rows.Add([pscustomobject]@{scenario='Loop';repetition=$n;status='NOT_RUN';reason='Actual repaired ferry preparation failed; no fabricated fallback'})}
}
for($n=1;$n -le 3;$n++){
 if($successor){$null=RunOne 'Resume' $n $successor 30 $HarvestFixBuild}
 else{$rows.Add([pscustomobject]@{scenario='Resume';repetition=$n;status='NOT_RUN';reason='No completed actual successor; no fabricated fallback'})}
}
$rows|ConvertTo-Json -Depth 5|Set-Content "$Root/recovery-results.json";$rows|Export-Csv "$Root/recovery-results.csv" -NoTypeInformation
@{utc=[datetime]::UtcNow.ToString('o');complete=$true;meaning='Targeted tool-fix recovery only; original full suite retained separately'}|ConvertTo-Json|Set-Content "$Root/recovery-complete.json"
if(@($rows|Where-Object status -eq FAIL).Count){exit 1};exit 0
