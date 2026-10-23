[CmdletBinding()]
param(
 [string]$UnityPath='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe',
 [Parameter(Mandatory=$true)][string]$SourceProject,
 [Parameter(Mandatory=$true)][string]$WorkProject,
 [Parameter(Mandatory=$true)][string]$ArtifactsRoot,
 [string[]]$Methods=@('B06DropCheck.Run'),
 [int]$TimeoutSeconds=240,
 [string[]]$QuitMethods=@(),
 [switch]$PrepareCopy,
 [switch]$RunnerSelfTest
)
$ErrorActionPreference='Stop'
$source=[IO.Path]::GetFullPath($SourceProject);$work=[IO.Path]::GetFullPath($WorkProject)
if($source.TrimEnd('\','/') -eq $work.TrimEnd('\','/') -or $work.StartsWith($source.TrimEnd('\','/')+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw '必须使用项目外部的隔离副本'}
if($TimeoutSeconds -lt 1){throw '超时必须为正数'}
New-Item -ItemType Directory -Path $ArtifactsRoot -Force | Out-Null
$runStamp=Get-Date -Format 'yyyyMMdd-HHmmss-fff'
@{unity=$UnityPath;source=$source;work=$work;artifacts=[IO.Path]::GetFullPath($ArtifactsRoot);methods=$Methods;timeoutSeconds=$TimeoutSeconds;quitMethods=$QuitMethods;prepareCopy=[bool]$PrepareCopy;selfTest=[bool]$RunnerSelfTest} | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $ArtifactsRoot ('invocation.'+$runStamp+'.json')) -Encoding utf8
$results=[Collections.Generic.List[object]]::new()
function Run-Child($label,$exe,$arguments,$timeout,$expected=0){
 $log=Join-Path $ArtifactsRoot ($label+'.'+$runStamp+'.log');$watch=[Diagnostics.Stopwatch]::StartNew();$p=$null;$code=$null;$timedOut=$false;$errorText=''
 try {
  $info=[Diagnostics.ProcessStartInfo]::new();$info.FileName=$exe;$info.UseShellExecute=$false;$info.CreateNoWindow=$true
  # Windows quoting: arguments are passed directly to the child, never to a shell.
  $info.Arguments=($arguments | ForEach-Object {'"'+($_ -replace '(\\*)"','$1$1\"' -replace '(\\+)$','$1$1')+'"'}) -join ' '
  $info.EnvironmentVariables['UNITY_TEST_ROOT']=[IO.Path]::GetFullPath($ArtifactsRoot)
  $p=[Diagnostics.Process]::Start($info)
  if(-not $p.WaitForExit($timeout*1000)){$timedOut=$true;$p.Kill();$p.WaitForExit()}
  $code=$p.ExitCode
 }catch{$errorText=$_.Exception.Message}finally{if($p){$p.Dispose()};$watch.Stop()}
 $passed=(!$timedOut -and $errorText -eq '' -and $code -eq $expected)
 $results.Add([pscustomobject]@{method=$label;exitCode=$code;timedOut=$timedOut;launchError=$errorText;seconds=$watch.Elapsed.TotalSeconds;passed=$passed;log=$log})
 if(!(Test-Path -LiteralPath $log)){$results[-1] | ConvertTo-Json | Set-Content -LiteralPath $log -Encoding utf8}
 $results[-1] | Format-List | Out-String | Write-Host
}
try {
 if($RunnerSelfTest){
  $shell=(Get-Process -Id $PID).Path
  Run-Child 'self-success' $shell @('-NoProfile','-Command','exit 0') 10
  Run-Child 'self-failure' $shell @('-NoProfile','-Command','exit 7') 10
  Run-Child 'self-timeout' $shell @('-NoProfile','-Command','Start-Sleep -Seconds 20') 1
 }else{
  if($PrepareCopy){
   if(Test-Path -LiteralPath $work){throw '隔离副本目标已存在，拒绝覆盖'}
   New-Item -ItemType Directory -Path $work | Out-Null
   foreach($part in @('Assets','Packages','ProjectSettings')){Copy-Item -LiteralPath (Join-Path $source $part) -Destination (Join-Path $work $part) -Recurse}
  }
  if(!(Test-Path (Join-Path $work 'ProjectSettings/ProjectVersion.txt'))){throw '隔离副本不是 Unity 项目'}
  foreach($method in $Methods){$childArgs=@('-batchmode','-projectPath',$work,'-executeMethod',$method,'-logFile',(Join-Path $ArtifactsRoot ($method+'.'+$runStamp+'.log')));if($QuitMethods -contains $method){$childArgs+='-quit'};Run-Child $method $UnityPath $childArgs $TimeoutSeconds}
 }
}catch{$results.Add([pscustomobject]@{method='runner';exitCode=$null;timedOut=$false;launchError=$_.Exception.Message;seconds=0;passed=$false;log=''})}
$results | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $ArtifactsRoot ("results."+(Get-Date -Format "yyyyMMdd-HHmmss-fff")+".json")) -Encoding utf8
$results | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $ArtifactsRoot 'results.json') -Encoding utf8
$results | Export-Csv (Join-Path $ArtifactsRoot 'results.csv') -NoTypeInformation -Encoding utf8
$failed=@($results | Where-Object {!$_.passed}).Count
"total=$($results.Count) failed=$failed timeouts=$(@($results | Where-Object timedOut).Count)" | Tee-Object -FilePath (Join-Path $ArtifactsRoot 'summary.txt')
if($failed -gt 0){exit 1};exit 0
