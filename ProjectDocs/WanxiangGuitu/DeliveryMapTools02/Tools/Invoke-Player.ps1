param([Parameter(Mandatory)][string]$Exe,[Parameter(Mandatory)][string]$Output,[ValidateSet('write','read')][string]$Mode='write',[string]$Checkpoint='I:/WGCombat/MAPTOOLS02-A/Synthetic/PlayerCheckpoint.json')
$ErrorActionPreference='Stop';$exePath=[IO.Path]::GetFullPath($Exe);$out=[IO.Path]::GetFullPath($Output);$checkpointPath=[IO.Path]::GetFullPath($Checkpoint)
foreach($path in @($exePath,$out,$checkpointPath)){if(!$path.StartsWith('I:\WGCombat\MAPTOOLS02-A\')){throw 'Owned research paths required'}}
if(!(Test-Path -LiteralPath $exePath) -or (Test-Path -LiteralPath $out)){throw 'Existing Player/fresh output required'}
New-Item -ItemType Directory $out|Out-Null
$os=Get-CimInstance Win32_OperatingSystem;$free=[double]$os.FreeVirtualMemory/1MB
@{freeCommitGB=$free;minimumGB=3;utc=[datetime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content "$out/resources.json"
if($free -lt 3){throw 'ENV_RESOURCE_BLOCKED: no Unity Player launched'}
$desktop='WGTest_'+[guid]::NewGuid().ToString('N');$worker='I:/WGP2/1028-080504-eef74f/Runtime/Worker/NativeProbe.dll'
$argsList=@('-logFile',"$out/Player.log",'-screen-width','1280','-screen-height','720','-screen-fullscreen','0','-mt02-mode',$Mode,'-mt02-checkpoint',$checkpointPath)
@{Exe=$exePath;Arguments=$argsList;Desktop=$desktop;Receipt="$out/Player.desktop-process.json";EnvRoot=$out;ShowInInactiveDesktop=$true}|ConvertTo-Json -Depth 5|Set-Content "$out/Player.launch-spec.json"
$old=$env:MT02_OUTPUT
try{
 $env:MT02_OUTPUT=$out;$psi=[Diagnostics.ProcessStartInfo]::new();$psi.FileName=(Get-Command dotnet).Source;$psi.UseShellExecute=$false;$psi.WindowStyle='Hidden';$psi.RedirectStandardOutput=$true;$psi.RedirectStandardError=$true
 foreach($a in @($worker,'host',"$out/Player.launch-spec.json")){$psi.ArgumentList.Add($a)}
 $p=[Diagnostics.Process]::Start($psi);$stdout=$p.StandardOutput.ReadToEndAsync();$stderr=$p.StandardError.ReadToEndAsync()
 @{exe=$exePath;arguments=$argsList;hostPid=$p.Id;startUtc=[DateTime]::UtcNow.ToString('o');scope='isolated plugin Player; no real saves or native input'}|ConvertTo-Json -Depth 5|Set-Content "$out/Player.command.json"
 $ended=$p.WaitForExit(300000);if($ended){[IO.File]::WriteAllText("$out/host.stdout",$stdout.Result);[IO.File]::WriteAllText("$out/host.stderr",$stderr.Result)}
 @{exited=$ended;exitCode=if($ended){$p.ExitCode}else{$null};timedOut=!$ended;forcedTermination=$false}|ConvertTo-Json|Set-Content "$out/process.json";if(!$ended){throw 'Timeout; process preserved'};exit $p.ExitCode
}finally{$env:MT02_OUTPUT=$old}
