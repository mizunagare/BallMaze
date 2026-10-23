[CmdletBinding()]
param([Parameter(Mandatory)][string]$ProcDumpPath,[string]$TestRoot="$env:USERPROFILE/Documents/unitytest/ProcDumpFollowup",[string]$PythonPath="$env:USERPROFILE/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe")
$ErrorActionPreference='Stop'
# Reuse the existing process host/receipts. Import definitions only; never execute the All body.
$entry=Join-Path $PSScriptRoot 'Invoke-LocalValidation.ps1'
$ast=[Management.Automation.Language.Parser]::ParseFile($entry,[ref]$null,[ref]$null)
foreach($name in 'SafePath','StartChild','FinishChild'){
 $function=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true)
 Invoke-Expression $function.Extent.Text
}
$base=SafePath $TestRoot;$tool=SafePath $ProcDumpPath
if($base.StartsWith([IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../../..')),[StringComparison]::OrdinalIgnoreCase)){throw 'External test root required'}
$root=Join-Path $base ((Get-Date -Format 'yyyyMMdd-HHmmss')+'-'+[guid]::NewGuid().ToString('N').Substring(0,8));New-Item -ItemType Directory $root -Force|Out-Null
$dotnet=(Get-Command dotnet).Source;$UnityPath='';$script:workerReady=$false;$script:children=[Collections.Generic.List[object]]::new()
$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerPath="$root/Worker/NativeProbe.dll"
@{kind='ProcDump synthetic target controls';root=$root;coordinatorPid=$PID;utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content "$root/owner.json"
@{path=$tool;sha256=(Get-FileHash $tool).Hash;version=(Get-Item $tool).VersionInfo.FileVersion;signature=(Get-AuthenticodeSignature $tool).Status.ToString();signer=(Get-AuthenticodeSignature $tool).SignerCertificate.Subject}|ConvertTo-Json|Set-Content "$root/tool.json"
$rows=[Collections.Generic.List[object]]::new()
function Run($name,$exe,$arguments,$limit=30){
 $start=[DateTime]::UtcNow;$t=StartChild $exe $arguments "$root/$name";$ended=$t.process.WaitForExit($limit*1000)
 if($ended){FinishChild $t}
 $rows.Add(@{name=$name;startUtc=$start.ToString('o');endUtc=[DateTime]::UtcNow.ToString('o');command=@($exe)+@($arguments);exitCode=if($ended){$t.process.ExitCode}else{$null};timedOut=!$ended})
 $rows|ConvertTo-Json -Depth 6|Set-Content "$root/results.json"
 return $t
}
$build=Run 'build' $dotnet @('build',"$PSScriptRoot/NativeProbe/NativeProbe.csproj",'-c','Release','-o',"$root/Worker","-p:BaseIntermediateOutputPath=$root/obj/") 120
if(!$build.process.HasExited -or $build.process.ExitCode -ne 0){throw 'Worker build unavailable'}
$script:workerReady=$true
$target=StartChild $dotnet @($script:workerPath,'fixture-window',"$root/closed.json") "$root/target"
try{
 $until=[DateTime]::UtcNow.AddSeconds(10);while(!(Test-Path "$root/closed.json.ready.json") -and [DateTime]::UtcNow -lt $until){Start-Sleep -Milliseconds 100}
 if(!(Test-Path "$root/closed.json.ready.json")){throw 'Synthetic window not ready'}
 $child=(Get-Content $target.receipt -Raw|ConvertFrom-Json).pid
 foreach($name in 'single','double'){New-Item -ItemType Directory "$root/$name"|Out-Null
  $a=@('-accepteula','-mm');if($name -eq 'double'){$a+=@('-n','2','-s','1')};$a+=@([string]$child,"$root/$name")
  $r=Run $name $tool $a
  if(!$r.process.HasExited){throw 'Monitor timed out; target will receive normal close, no kill'}
 }
 if(Get-Process -Id 2147483646 -ErrorAction SilentlyContinue){throw 'Negative PID unexpectedly exists'}
 Run 'invalid-pid' $tool @('-accepteula','-mm','2147483646',"$root/invalid.dmp")|Out-Null
 $monitor=StartChild $tool @('-accepteula','-mm','-e','-t','-n','1',[string]$child,"$root/termination.dmp") "$root/termination"
 Start-Sleep -Seconds 2
 Run 'close-target' $dotnet @($script:workerPath,'close',[string]$child,"$root/close.json",$dotnet,$script:desktop)|Out-Null
 $ended=$target.process.WaitForExit(15000);if($ended){FinishChild $target}
 if($monitor.process.WaitForExit(15000)){FinishChild $monitor}
 $rows.Add(@{name='termination';exitCode=if($monitor.process.HasExited){$monitor.process.ExitCode}else{$null};timedOut=!$monitor.process.HasExited})
 $rows.Add(@{name='synthetic-target';exitCode=if($ended){$target.process.ExitCode}else{$null};timedOut=!$ended})
}finally{
 $rows|ConvertTo-Json -Depth 6|Set-Content "$root/results.json"
 ConvertTo-Json -InputObject @($script:children|Where-Object {!$_.process.HasExited}|ForEach-Object {$_.process.Id}) -AsArray|Set-Content "$root/preserved-processes.json"
 Write-Host "RESULT_ROOT=$root"
}
& $PythonPath -B "$PSScriptRoot/classify-procdump.py" calibrate $root --output "$root/calibration-proof.json"
exit $LASTEXITCODE
