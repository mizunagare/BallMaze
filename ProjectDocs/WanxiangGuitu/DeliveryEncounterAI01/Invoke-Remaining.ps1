param([Parameter(Mandatory)][string]$Project,[Parameter(Mandatory)][string]$OwnedRoot)
$ErrorActionPreference='Stop';$Project=[IO.Path]::GetFullPath($Project);$OwnedRoot=[IO.Path]::GetFullPath($OwnedRoot)
if(!$OwnedRoot.StartsWith('I:\WGCombat\EAI01-',[StringComparison]::OrdinalIgnoreCase) -or !$Project.StartsWith($OwnedRoot+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Owned isolated project required'}
if(Test-Path "$OwnedRoot/regression-continuation-processes.json"){throw 'Preserve original continuation attempt'}
$rows=@();$blocked=@{}
foreach($method in 'Combat03Area.Run','B07Economy.Run','B07Rules.Run','B07Rules.Resume','B07Rules.PendingResume','B07Rules.CommittedResume','B3StreamRules.Run','WGB1Routes.Run','WGB1Check.Run','WGB1Check.Resume'){
 $deadline=(Get-Date).AddSeconds(30)
 do{
  $active=@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object {$_.CommandLine.Replace('/','\').Contains($Project)})
  if($active.Count){@{utc=[datetime]::UtcNow.ToString('o');stage=$method;processes=@($active|Select-Object ProcessId,CommandLine)}|ConvertTo-Json -Depth 4 -Compress|Add-Content "$OwnedRoot/quiescence.jsonl";Start-Sleep -Seconds 1}
 }while($active.Count -and (Get-Date) -lt $deadline)
 if($active.Count){throw 'Owned project still occupied after bounded diagnostic wait; no kill'}
 $group=$method.Split('.')[0];$dependent=$method -in @('B07Rules.Resume','B07Rules.PendingResume','B07Rules.CommittedResume','WGB1Check.Resume')
 if($dependent -and $blocked[$group]){$rows+=@{method=$method;status='NOT_RUN';reason='previous dependent state failed'};continue}
 $store=if($group -eq 'B07Rules'){"$OwnedRoot/BossRulesStore"}elseif($group -eq 'WGB1Check'){"$OwnedRoot/FerryRulesStore"}else{''}
 & "$PSScriptRoot/Invoke-Check.ps1" -Project $Project -Output "$OwnedRoot/$($method.Replace('.','-'))" -StorageRoot $store -Method $method -NoGraphics
 $code=$LASTEXITCODE;$rows+=@{method=$method;exitCode=$code;status=if($code -eq 0){'PASS'}else{'FAIL'}}
 if($code -ne 0){$blocked[$group]=$true}
 $rows|ConvertTo-Json -Depth 4|Set-Content "$OwnedRoot/regression-continuation-processes.json" -Encoding utf8
}
if(@($rows|Where-Object status -ne PASS).Count){exit 1};exit 0
