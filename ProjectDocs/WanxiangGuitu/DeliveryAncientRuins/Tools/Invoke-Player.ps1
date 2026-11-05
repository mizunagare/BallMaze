param([Parameter(Mandatory)][string]$Exe,[Parameter(Mandatory)][string]$Output,[string]$Mode='explore',[string]$Checkpoint='I:/WGCombat/C1-1105-A/unused.json')
$ErrorActionPreference='Stop';$exePath=[IO.Path]::GetFullPath($Exe);$out=[IO.Path]::GetFullPath($Output);$checkpointPath=[IO.Path]::GetFullPath($Checkpoint)
foreach($path in @($exePath,$out,$checkpointPath)){if(!$path.StartsWith('I:\WGCombat\C1-1105-A\')){throw 'Owned research paths required'}}
if(!(Test-Path -LiteralPath $exePath) -or (Test-Path -LiteralPath $out)){throw 'Existing Player/fresh output required'}
New-Item -ItemType Directory $out|Out-Null
$os=Get-CimInstance Win32_OperatingSystem;$free=[double]$os.FreeVirtualMemory/1MB
@{freeCommitGB=$free;minimumGB=3;utc=[datetime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content "$out/resources.json"
if($free -lt 3){throw 'ENV_RESOURCE_BLOCKED: no Unity Player launched'}
$desktop='WGTest_'+[guid]::NewGuid().ToString('N');$worker='I:/WGP2/1028-080504-eef74f/Runtime/Worker/NativeProbe.dll'
$argsList=@('-logFile',"$out/Player.log",'-screen-width','1280','-screen-height','720','-screen-fullscreen','0','-c1-probe','-c1-mode',$Mode,'-wanxiang-storage-root',$out)
@{Exe=$exePath;Arguments=$argsList;Desktop=$desktop;Receipt="$out/Player.desktop-process.json";EnvRoot=$out;ShowInInactiveDesktop=$true}|ConvertTo-Json -Depth 5|Set-Content "$out/Player.launch-spec.json"
$old=$env:UNITY_TEST_ROOT
try{
 $env:UNITY_TEST_ROOT=$out;$psi=[Diagnostics.ProcessStartInfo]::new();$psi.FileName=(Get-Command dotnet).Source;$psi.UseShellExecute=$false;$psi.WindowStyle='Hidden';$psi.RedirectStandardOutput=$true;$psi.RedirectStandardError=$true
 foreach($a in @($worker,'host',"$out/Player.launch-spec.json")){$psi.ArgumentList.Add($a)}
 $p=[Diagnostics.Process]::Start($psi);$stdout=$p.StandardOutput.ReadToEndAsync();$stderr=$p.StandardError.ReadToEndAsync()
 @{exe=$exePath;arguments=$argsList;hostPid=$p.Id;startUtc=[DateTime]::UtcNow.ToString('o');scope='isolated ruins Player; controlled runtime calls, not physical input'}|ConvertTo-Json -Depth 5|Set-Content "$out/Player.command.json"
 $ended=$p.WaitForExit(600000);if($ended){[IO.File]::WriteAllText("$out/host.stdout",$stdout.Result);[IO.File]::WriteAllText("$out/host.stderr",$stderr.Result)}
 @{exited=$ended;exitCode=if($ended){$p.ExitCode}else{$null};timedOut=!$ended;forcedTermination=$false}|ConvertTo-Json|Set-Content "$out/process.json";if(!$ended){throw 'Timeout; process preserved'};exit $p.ExitCode
}finally{$env:UNITY_TEST_ROOT=$old}
