[CmdletBinding()]
param([Parameter(Mandatory)][string]$Root,[Parameter(Mandatory)][string]$BuildRoot)
$ErrorActionPreference='Stop';$source=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..'));$runtime=Join-Path $Root 'Runtime';$rows=[Collections.Generic.List[object]]::new()
if((Get-Content "$Root/owner.json" -Raw|ConvertFrom-Json).kind -ne 'PERF-01 isolated measurements'){throw 'Owned measurement root required'}
$until=[datetime]::UtcNow.AddMinutes(25)
while(!(Test-Path "$BuildRoot/Build01Audit.Run.exit.json") -and [datetime]::UtcNow -lt $until){Start-Sleep -Seconds 5}
if(!(Test-Path "$BuildRoot/Build01Audit.Run.exit.json") -or (Get-Content "$BuildRoot/Build01Audit.Run.exit.json" -Raw|ConvertFrom-Json).exitCode -ne 0){throw 'Completed successful build required; no fallback to old input'}
$e=Join-Path $source 'ProjectDocs/WanxiangGuitu/DeliveryPlayer02/Evidence/Run-1027-205135/Attempts';$running=Join-Path $e '220103-Successor-bb698c/StorageAfter/WanxiangGuitu';$camp=Join-Path $e '220035-Pending-19eb2e/StorageAfter/WanxiangGuitu'
function RunCase($scenario,$repetition,$fixture,$seconds,$off=$false){
 $start=[datetime]::UtcNow;$outcome='NOT_RUN';$reason='';$storage=''
 try{& "$PSScriptRoot/Invoke-PerfCase.ps1" -Root $Root -BuildRoot $BuildRoot -Scenario $scenario -Repetition $repetition -Fixture $fixture -Seconds $seconds -SamplingOff:$off | Out-Host;$code=$LASTEXITCODE
  $d=Get-ChildItem "$runtime/Cases" -Directory|Where-Object {Test-Path "$($_.FullName)/case-result.json"}|Where-Object {(Get-Item "$($_.FullName)/case-result.json").LastWriteTimeUtc -ge $start}|Sort-Object Name|Select-Object -Last 1
  if($d){$storage=$d.FullName;$outcome=if($code -eq 0){'PASS'}else{'FAIL'}}else{$outcome='FAIL';$reason='No completed case receipt'}
 }catch{$outcome='FAIL';$reason=$_.Exception.ToString();$code=$null}
 $rows.Add([pscustomobject]@{scenario=$scenario;repetition=$repetition;samplingOff=$off;status=$outcome;exitCode=$code;storage=$storage;reason=$reason;start=$start.ToString('o');end=[datetime]::UtcNow.ToString('o')});$rows|ConvertTo-Json -Depth 5|Set-Content "$Root/suite-results.json";return $storage
}
# Fixture preparation is a separate actual runtime operation, not counted as a performance window.
$prep=RunCase 'PrepareFerry' 0 $running 0;$ferry='';if($prep -and (Get-Content "$prep/case-result.json" -Raw|ConvertFrom-Json).exitCode -eq 0){$ferry=Join-Path $prep 'WanxiangGuitu'}
$resume=''
for($n=1;$n -le 3;$n++){
 $null=RunCase 'Title' $n '' 60;$null=RunCase 'Title' $n '' 60 $true;$null=RunCase 'Camp' $n $camp 60
 foreach($scenario in 'Movement','Gather','Combat','Boss'){$null=RunCase $scenario $n $running 120}
 if($ferry){$loop=RunCase 'Loop' $n $ferry 180;if(!$resume -and $loop -and (Get-Content "$loop/case-result.json" -Raw|ConvertFrom-Json).exitCode -eq 0){$resume=Join-Path $loop 'WanxiangGuitu'}}else{$rows.Add([pscustomobject]@{scenario='Loop';repetition=$n;status='NOT_RUN';reason='Real repaired ferry fixture preparation failed; no injected fallback'})}
}
for($n=1;$n -le 3;$n++){if($resume){$null=RunCase 'Resume' $n $resume 30}else{$rows.Add([pscustomobject]@{scenario='Resume';repetition=$n;status='NOT_RUN';reason='No actual current-batch successor from completed Loop; no fabricated fallback'})}}
$rows|ConvertTo-Json -Depth 5|Set-Content "$Root/suite-results.json";$rows|Export-Csv "$Root/suite-results.csv" -NoTypeInformation
@{utc=[datetime]::UtcNow.ToString('o');completed=$true;meaning='All independent planned attempts finished or explicitly blocked; per-window/data acceptance is separate, not inferred from script exit'}|ConvertTo-Json|Set-Content "$Root/suite-complete.json"
if(@($rows|Where-Object status -eq FAIL).Count){exit 1};exit 0
