param([Parameter(Mandatory)][string]$Exe,[Parameter(Mandatory)][string]$Output)
$ErrorActionPreference='Stop';$exePath=[IO.Path]::GetFullPath($Exe);$out=[IO.Path]::GetFullPath($Output)
foreach($p in @($exePath,$out)){if(!$p.StartsWith('I:\WGCombat\MAPTOOLS-1104-A\')){throw 'Owned lab paths required'}}
if(!(Test-Path -LiteralPath $exePath) -or (Test-Path -LiteralPath $out)){throw 'Existing executable and fresh output required'}
New-Item -ItemType Directory $out|Out-Null
$desktop='WGTest_'+[guid]::NewGuid().ToString('N');$worker='I:/WGP2/1028-080504-eef74f/Runtime/Worker/NativeProbe.dll'
$argsList=@('-logFile',"$out/Player.log",'-screen-width','1280','-screen-height','720','-screen-fullscreen','0')
@{Exe=$exePath;Arguments=$argsList;Desktop=$desktop;Receipt="$out/Player.desktop-process.json";EnvRoot=$out;ShowInInactiveDesktop=$true}|ConvertTo-Json -Depth 5|Set-Content "$out/Player.launch-spec.json"
$old=$env:MAP_LAB_OUTPUT
try{
 $env:MAP_LAB_OUTPUT=$out;$psi=[Diagnostics.ProcessStartInfo]::new();$psi.FileName=(Get-Command dotnet).Source;$psi.UseShellExecute=$false;$psi.WindowStyle='Hidden';$psi.RedirectStandardOutput=$true;$psi.RedirectStandardError=$true
 foreach($a in @($worker,'host',"$out/Player.launch-spec.json")){$psi.ArgumentList.Add($a)}
 $proc=[Diagnostics.Process]::Start($psi);$stdout=$proc.StandardOutput.ReadToEndAsync();$stderr=$proc.StandardError.ReadToEndAsync()
 @{exe=$exePath;arguments=$argsList;hostPid=$proc.Id;utc=[DateTime]::UtcNow.ToString('o');scope='isolated nondevelopment plugin test Player; no native input'}|ConvertTo-Json -Depth 5|Set-Content "$out/Player.command.json"
 $ended=$proc.WaitForExit(240000)
 if($ended){[IO.File]::WriteAllText("$out/host.stdout",$stdout.Result);[IO.File]::WriteAllText("$out/host.stderr",$stderr.Result)}
 @{exited=$ended;exitCode=if($ended){$proc.ExitCode}else{$null};timedOut=!$ended;forcedTermination=$false}|ConvertTo-Json|Set-Content "$out/process.json"
 if(!$ended){throw 'Timeout; owned process preserved'};exit $proc.ExitCode
}finally{$env:MAP_LAB_OUTPUT=$old}
