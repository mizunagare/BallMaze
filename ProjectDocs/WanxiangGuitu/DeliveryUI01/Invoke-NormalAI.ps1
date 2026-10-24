[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$SourceProject,[Parameter(Mandatory=$true)][string]$IsolationRoot,[ValidateSet('Normal','Resume','RejectMissing','RejectRelative','RejectLocalLow','FinalResume')][string]$Mode='Normal',[string]$UnityPath='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe',[switch]$LeaveTimedOutProcess,[string]$ExternalWorkerPath='',[string]$DesktopName='',[switch]$B2,[switch]$B3,[switch]$B4,[switch]$B07,[ValidateSet('Gather','Treasure','Bypass','Land','Lake')][string]$Strategy='Gather')
$ErrorActionPreference='Stop'
$source=[IO.Path]::GetFullPath($SourceProject);$root=[IO.Path]::GetFullPath($IsolationRoot)
if(![IO.Path]::IsPathFullyQualified($IsolationRoot) -or $root -match '(?i)(^|[\\/])LocalLow([\\/]|$)' -or $root.StartsWith($source,[StringComparison]::OrdinalIgnoreCase)){throw 'Use absolute isolated storage outside project and player LocalLow'}
for($a=$root;$a;$a=[IO.Path]::GetDirectoryName($a)){if((Test-Path -LiteralPath $a) -and ((Get-Item -LiteralPath $a -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'Reparse point in isolation path'}}
$active=Get-CimInstance Win32_Process | Where-Object {$_.Name -eq 'Unity.exe' -and $_.CommandLine -like ('*'+$source+'*')};if($active){throw 'Close the original project Editor first'}
if($Mode -notin @('Resume','FinalResume') -and (Test-Path -LiteralPath $root)){throw 'Use a fresh root for a new test'}
New-Item -ItemType Directory -Path $root -Force | Out-Null
$protected=Join-Path ([IO.Path]::GetDirectoryName($root)) 'Protected/DoNotTouch';New-Item -ItemType Directory -Path $protected -Force | Out-Null
$sentinel=Join-Path $protected 'sentinel.txt';if(!(Test-Path $sentinel)){[IO.File]::WriteAllText($sentinel,'synthetic player-directory stand-in; never actual player data')};$before=(Get-FileHash $sentinel).Hash
$driver=[IO.Path]::GetFullPath((Join-Path $source 'Assets/CombatPrototype/Editor/A1ValidationDrivers'));if(Test-Path $driver){throw 'Temporary driver folder already exists; refusing overwrite'}
New-Item -ItemType Directory -Path $driver | Out-Null
try{
 Copy-Item -LiteralPath (Join-Path $PSScriptRoot $(if($B07){'../DeliveryB07/Tests/WGNormalAICheck.cs.txt'}elseif($B4){'../DeliveryB4/Tests/WGNormalAICheck.cs.txt'}elseif($B3){'../DeliveryB3/Tests/WGNormalAICheck.cs.txt'}elseif($B2){'../DeliveryB2/Tests/WGNormalAICheck.cs.txt'}else{'../DeliveryB1/Tests/WGNormalAICheck.cs.txt'})) -Destination (Join-Path $driver 'WGNormalAICheck.cs')
 Copy-Item -LiteralPath (Join-Path $PSScriptRoot '../../东方元素肉鸽/B06本地测试/TestSources/B06OriginalPlay.cs.txt') -Destination (Join-Path $driver 'B06OriginalPlay.cs')
 Copy-Item -LiteralPath (Join-Path $PSScriptRoot $(if($B07){'../DeliveryB07/Tests/WGA1NormalResume.cs.txt'}elseif($B4){'../DeliveryB4/Tests/WGA1NormalResume.cs.txt'}elseif($B3){'../DeliveryB3/Tests/WGA1NormalResume.cs.txt'}elseif($B2){'../DeliveryB2/Tests/WGA1NormalResume.cs.txt'}else{'../DeliveryA1/Tests/WGA1NormalResume.cs.txt'})) -Destination (Join-Path $driver 'WGA1NormalResume.cs')
 $method=if($Mode -in @('Resume','FinalResume')){'WGA1NormalResume.Run'}else{'WGNormalAICheck.Run'}
 $arguments=@('-projectPath',$source,'-executeMethod',$method,'-logFile',(Join-Path $root ($Mode+'.log')))
 switch($Mode){'RejectMissing'{} 'RejectRelative'{$arguments+=@('-wanxiang-storage-root','relative')} 'RejectLocalLow'{$arguments+=@('-wanxiang-storage-root',(Join-Path $env:USERPROFILE 'AppData/LocalLow/DoNotAccess'))} default{$arguments+=@('-wanxiang-storage-root',$root)}}
 $psi=[Diagnostics.ProcessStartInfo]::new();$psi.FileName=$UnityPath;$psi.UseShellExecute=$false;$psi.CreateNoWindow=$true;$psi.WindowStyle='Hidden';$psi.Environment['UNITY_TEST_ROOT']=$root;if($B4 -or $B07){$psi.Environment['WG_B4_STRATEGY']=$Strategy}
 foreach($arg in $arguments){$psi.ArgumentList.Add($arg)}
 $proc=[Diagnostics.Process]::Start($psi);$deadline=[DateTime]::UtcNow.AddSeconds(360);$compilerFailure=$false
 while(!$proc.WaitForExit(500) -and [DateTime]::UtcNow -lt $deadline){
  $compileLog=Join-Path $root ($Mode+'.log')
  if($ExternalWorkerPath -and (Test-Path $compileLog) -and (Select-String -LiteralPath $compileLog -Pattern 'error CS\d+' -Quiet)){
   $compilerFailure=$true
   Get-CimInstance Win32_Process -Filter "ProcessId=$($proc.Id)"|Select-Object ProcessId,CommandLine|ConvertTo-Json|Set-Content (Join-Path $root 'compiler-failure-process.json')
   $tool=(Get-Command dotnet).Source
   & $tool $ExternalWorkerPath close ([string]$proc.Id) (Join-Path $root 'compiler-failure-close.json') $UnityPath $DesktopName
   $proc.WaitForExit(15000)|Out-Null;break
  }
 }
 $timeout=!$proc.HasExited;if($timeout -and !$LeaveTimedOutProcess){$proc.Kill();$proc.WaitForExit()};$observedCode=if($proc.HasExited){$proc.ExitCode}else{$null}
 $expected=if($Mode -like 'Reject*'){1}else{0};$unchanged=(Get-FileHash $sentinel).Hash -eq $before
 @{mode=$Mode;exitCode=$observedCode;timedOut=$timeout;compilerFailure=$compilerFailure;expectedExitCode=$expected;sentinelUnchanged=$unchanged;root=$root} | ConvertTo-Json | Set-Content (Join-Path $root ('process-result-'+$Mode+'.json')) -Encoding utf8
 if($Mode -like 'Reject*'){if(!(Select-String -LiteralPath (Join-Path $root ($Mode+'.log')) -Pattern 'A1_ISOLATION_REJECTED' -Quiet)){throw 'Expected pre-Play rejection marker absent'};if(Test-Path (Join-Path $root 'storage-audit.jsonl')){throw 'Rejected launch performed storage operations'}}
 if($Mode -notlike 'Reject*'){
  $records=Get-Content -LiteralPath (Join-Path $root 'storage-audit.jsonl') | ForEach-Object {$_ | ConvertFrom-Json}
  if($records[0].operation -ne 'pre-play' -or $records[0].playing -or !($records | Where-Object operation -eq 'before-exit')){throw 'Missing first-to-exit storage receipts'}
  foreach($record in $records){if($record.path -ne $root -and !$record.path.StartsWith($root+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Storage receipt outside allowed root'}}
 }
 if($compilerFailure -or $timeout -or $observedCode -ne $expected -or !$unchanged){throw 'Normal AI process/guard validation failed'}
}finally{
 # Verify both absolute paths and only known installed files before moving the temporary folder.
 $destination=[IO.Path]::GetFullPath((Join-Path $root ('ExecutedDrivers-'+[guid]::NewGuid().ToString('N'))))
 if($driver -ne [IO.Path]::GetFullPath((Join-Path $source 'Assets/CombatPrototype/Editor/A1ValidationDrivers')) -or !$destination.StartsWith($root+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Invalid driver cleanup paths'}
 $allowed=@('WGNormalAICheck.cs','WGNormalAICheck.cs.meta','B06OriginalPlay.cs','B06OriginalPlay.cs.meta','WGA1NormalResume.cs','WGA1NormalResume.cs.meta')
 if(@(Get-ChildItem -LiteralPath $driver -Force | Where-Object {$_.Name -notin $allowed}).Count){throw 'Unknown files in temporary driver directory; preserving for inspection'}
 if($proc -and !$proc.HasExited){Write-Warning 'Timed-out isolated Editor still active; preserve drivers and directory for diagnosis'}else{
 Move-Item -LiteralPath $driver -Destination $destination
 if(Test-Path -LiteralPath ($driver+'.meta')){Move-Item -LiteralPath ($driver+'.meta') -Destination (Join-Path $destination 'folder.meta')}
 }
}
