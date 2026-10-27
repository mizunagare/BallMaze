[CmdletBinding()]
param([Parameter(Mandatory)][string]$ParentRoot,[Parameter(Mandatory)][string]$StoryRoot,[Parameter(Mandatory)][string]$WorkerPath)
$ErrorActionPreference='Stop'
$parent=[IO.Path]::GetFullPath($ParentRoot);$story=[IO.Path]::GetFullPath($StoryRoot)
if((Get-Content "$parent/owner.json" -Raw|ConvertFrom-Json).kind -ne 'PLAYER-02 isolated runtime acceptance' -or !$story.StartsWith($parent+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Owned synthetic story required'}
$root=Join-Path $parent ('Catalog-'+(Get-Date -Format HHmmss)+'-'+[guid]::NewGuid().ToString('N').Substring(0,8));New-Item -ItemType Directory $root|Out-Null
$rows=[Collections.Generic.List[object]]::new()
function Files($folder){$v=@{};if(Test-Path $folder){Get-ChildItem $folder -File -Recurse|ForEach-Object {$v[[IO.Path]::GetRelativePath($folder,$_.FullName)]=(Get-FileHash $_.FullName).Hash}};return ($v.GetEnumerator()|Sort-Object Name|ConvertTo-Json -Depth 3 -Compress)}
foreach($case in 'Missing','Ready','Corrupt','Incompatible','Uncertain','Pending','Committed','BadPreferences'){
 $storage=Join-Path $root $case;New-Item -ItemType Directory $storage|Out-Null
 $business=Join-Path $storage 'WanxiangGuitu';$folder=Join-Path $business 'ForestRuins';$source='';$expected=$case;$mode='Observe'
 if($case -in @('Ready','Pending','Committed')){
  if($case -eq 'Ready'){$source=Join-Path $story 'WanxiangGuitu'}else{
   $stage=if($case -eq 'Pending'){'Main'}else{'Pending'}
   $hit=Get-ChildItem "$parent/Attempts" -Directory|Where-Object {Test-Path "$($_.FullName)/StorageAfter/result-$stage.json"}|Where-Object {(Get-Content "$($_.FullName)/StorageAfter/result-$stage.json" -Raw|ConvertFrom-Json).status -eq 'PASS'}|Sort-Object Name|Select-Object -Last 1
   if(!$hit){throw "No successful $stage process boundary"};$source=Join-Path $hit.FullName 'StorageAfter/WanxiangGuitu'
  }
  Copy-Item -LiteralPath $source -Destination $business -Recurse;$expected='Ready'
 }elseif($case -in @('Corrupt','Incompatible','Uncertain')){
  New-Item -ItemType Directory $folder -Force|Out-Null
  if($case -eq 'Corrupt'){Set-Content "$folder/save.json" '{"version":9,"payload":"broken","checksum":"bad"}'}
  elseif($case -eq 'Incompatible'){Set-Content "$folder/save.json" '{"version":99}'}
  else{Set-Content "$folder/explicit-negative-sentinel.txt" 'Synthetic uncertain collection; never a positive result'}
 }elseif($case -eq 'BadPreferences'){
  New-Item -ItemType Directory $business -Force|Out-Null;Set-Content "$business/preferences.json" 'malformed synthetic settings';$mode='BadPreferences';$expected=''
 }
 $before=Files $business
 & "$PSScriptRoot/Invoke-P02Case.ps1" -ParentRoot $parent -StorageRoot $storage -Mode $mode -Expected $expected -WorkerPath $WorkerPath
 $code=$LASTEXITCODE;$after=Files $business;$unchanged=$before -ceq $after
 $row=[pscustomobject]@{case=$case;status=$(if($code -eq 0 -and $unchanged){'PASS'}else{'FAIL'});exitCode=$code;collectionUnchanged=$unchanged;source=$source;storage=$storage;before=$before;after=$after;scope='Synthetic catalog-only Player: no Run creation, no positive business JSON editing'}
 $rows.Add($row);$row|ConvertTo-Json -Depth 5|Set-Content "$root/$case.json"
}
$rows|ConvertTo-Json -Depth 5|Set-Content "$root/results.json";$rows|Export-Csv "$root/results.csv" -NoTypeInformation
Write-Output "CATALOG_ROOT=$root";if(@($rows|Where-Object status -eq FAIL).Count){exit 1};exit 0
