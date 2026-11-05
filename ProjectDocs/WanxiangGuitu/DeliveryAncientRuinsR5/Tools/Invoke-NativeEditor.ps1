param([Parameter(Mandatory)][ValidateSet('NativeProject')][string]$ProjectName,[Parameter(Mandatory)][ValidateSet('Import','Build')][string]$Mode)
$ErrorActionPreference='Stop'
$root='I:/WGCombat/C1R5-1105-A'
$project=[IO.Path]::GetFullPath("$root/$ProjectName")
$out="$root/$ProjectName-$Mode"
if(!(Test-Path "$project/ProjectSettings/ProjectVersion.txt") -or (Test-Path $out)){throw 'Expected fresh output and isolated input'}
if(Get-CimInstance Win32_Process -Filter "Name='Unity.exe'"|Where-Object {$_.CommandLine -and $_.CommandLine.Replace('/','\').Contains($project,[StringComparison]::OrdinalIgnoreCase)}){throw 'Isolated project occupied'}
$minimum=if($Mode -eq 'Build'){5}else{3}
$free=[double](Get-CimInstance Win32_OperatingSystem).FreeVirtualMemory/1MB
New-Item -ItemType Directory $out,"$out/Observed" -Force|Out-Null
@{freeCommitGB=$free;minimumGB=$minimum}|ConvertTo-Json|Set-Content "$out/resources.json"
if($free -lt $minimum){throw 'Insufficient commit; no Unity launch'}
$manifest=(Get-Content "$root/frozen-inputs.json" -Raw|ConvertFrom-Json).tracked
$watches=@('Assets/Resources/AncientRuins/DarkStone.mat','Assets/Resources/AncientRuins/Inlay.mat','Assets/Resources/AncientRuins/Stone.mat','Assets/Settings/PC_RPAsset.asset','Assets/Settings/UniversalRenderPipelineGlobalSettings.asset','ProjectSettings/EditorBuildSettings.asset','ProjectSettings/GraphicsSettings.asset','ProjectSettings/ProjectSettings.asset','ProjectSettings/UnityConnectSettings.asset','Packages/manifest.json','Packages/packages-lock.json')
function Fingerprint($label){
 $rows=@(foreach($row in $manifest){$path=Join-Path $project $row.path;if(Test-Path -LiteralPath $path){$hash=(Get-FileHash -LiteralPath $path).Hash.ToLower()}else{$hash=$null};if($hash-ne$row.sha256){@{path=$row.path;frozen=$row.sha256;observed=$hash}}})
 @{utc=[DateTime]::UtcNow.ToString('o');tracked=$manifest.Count;differences=$rows}|ConvertTo-Json -Depth 5|Set-Content "$out/$label.json"
}
$seen=@{}
$logSeen=@{}
function ObserveLog {
 if(!(Test-Path "$out/Unity.log")){return}
 foreach($line in Get-Content "$out/Unity.log" -Tail 300 -ErrorAction SilentlyContinue){
  if($line -notmatch 'AssetDatabase Initial Refresh|Initialize engine version|BuildPlayer:|Recompiling scripts for player build|BuildReport|WANXIANG_RELEASE_BUILD_PASS|PlayerBuildInfo|JobTempAlloc|Windows64'){continue}
  if($logSeen.ContainsKey($line)){continue}
  $logSeen[$line]=$true
  @{utc=[DateTime]::UtcNow.ToString('o');line=$line}|ConvertTo-Json -Compress|Add-Content "$out/log-landmarks.jsonl"
 }
}
function Observe($label){
 foreach($relative in $watches){
  $file=Join-Path $project $relative
  try {$bytes=[IO.File]::ReadAllBytes($file)} catch {continue}
  $hash=[Convert]::ToHexString([Security.Cryptography.SHA256]::HashData($bytes)).ToLower()
  if($seen[$relative] -eq $hash){continue}
  $seen[$relative]=$hash
  $name=$relative.Replace('/','_')+'-'+$hash+'.txt'
  [IO.File]::WriteAllBytes("$out/Observed/$name",$bytes)
  @{utc=[DateTime]::UtcNow.ToString('o');phase=$label;path=$relative;sha256=$hash;copy=$name}|ConvertTo-Json -Compress|Add-Content "$out/writes.jsonl"
 }
}
$entry='H:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Invoke-LocalValidation.ps1'
$ast=[Management.Automation.Language.Parser]::ParseFile($entry,[ref]$null,[ref]$null)
foreach($name in 'StartChild','FinishChild'){$f=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true);Invoke-Expression $f.Extent.Text}
$script:children=[Collections.Generic.List[object]]::new()
$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N')
$script:workerReady=$true
$script:workerPath='I:/WGP2/1028-080504-eef74f/Runtime/Worker/NativeProbe.dll'
$dotnet=(Get-Command dotnet).Source
$MinimumUnityCommitGB=$minimum
$exe='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe'
$argsList=@('-batchmode','-projectPath',$project,'-logFile',"$out/Unity.log",'-wanxiang-storage-root',$out)
if($Mode -eq 'Import'){$argsList+='-quit'}else{$argsList+=@('-executeMethod','WanxiangBuild.ValidateBuild')}
Fingerprint 'inputs-before';Observe 'before-launch'
$py='C:/Users/guan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
$priorPythonPath=$env:PYTHONPATH
$env:PYTHONPATH="$root/NativeTools"
try {
 $tracer=Start-Process -FilePath $py -ArgumentList @("$(Join-Path $PSScriptRoot 'Trace-Native.py')",$out,"$(Join-Path $PSScriptRoot 'Trace-Native.js')") -WindowStyle Hidden -PassThru -RedirectStandardOutput "$out/tracer.stdout" -RedirectStandardError "$out/tracer.stderr"
} finally { $env:PYTHONPATH=$priorPythonPath }
$t=StartChild $exe $argsList "$out/Editor" $out $false
$deadline=[DateTime]::UtcNow.AddMinutes(18)
while(!$t.process.HasExited -and [DateTime]::UtcNow -lt $deadline){Observe 'editor-running';ObserveLog;Start-Sleep -Milliseconds 220}
$ended=$t.process.HasExited
Observe 'after-wait';ObserveLog;FinishChild $t;Fingerprint 'inputs-after'
@{exited=$ended;exitCode=if($ended){$t.process.ExitCode}else{$null};timedOut=!$ended;forcedTermination=$false}|ConvertTo-Json|Set-Content "$out/process.json"
if($ended -and !$tracer.WaitForExit(15000)){throw "Native tracer has not detached"}
if($ended){@{traceExit=$tracer.ExitCode}|ConvertTo-Json|Set-Content "$out/tracer-process.json"}
if(!$ended){throw 'Bounded wait expired. Editor preserved'}
exit $t.process.ExitCode
