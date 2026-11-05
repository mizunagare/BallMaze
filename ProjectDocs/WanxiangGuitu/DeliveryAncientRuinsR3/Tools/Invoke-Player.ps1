param([Parameter(Mandatory)][string]$Exe,[Parameter(Mandatory)][string]$Output,[string]$Mode='explore',[string]$SeedPackage='',[string]$Checkpoint='I:/WGCombat/C1R3-1105-A/unused.json')
$ErrorActionPreference='Stop';$exePath=[IO.Path]::GetFullPath($Exe);$out=[IO.Path]::GetFullPath($Output);$checkpointPath=[IO.Path]::GetFullPath($Checkpoint)
foreach($path in @($exePath,$out,$checkpointPath)){if(!$path.StartsWith('I:\WGCombat\C1R3-1105-A\')){throw 'Owned research paths required'}}
if(!(Test-Path -LiteralPath $exePath) -or (Test-Path -LiteralPath $out)){throw 'Existing Player/fresh output required'}
New-Item -ItemType Directory $out|Out-Null
if($SeedPackage){$seed=[IO.Path]::GetFullPath($SeedPackage);if(!$seed.StartsWith('I:\WGCombat\C1R3-1105-A\') -or !(Test-Path -LiteralPath $seed -PathType Container)){throw 'Owned synthetic package required'};$dest=Join-Path $out 'WanxiangGuitu/ForestRuins';New-Item -ItemType Directory -Path $dest -Force|Out-Null;$copied=@();foreach($file in Get-ChildItem -LiteralPath $seed -Recurse -File){if($file.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Linked source rejected'};$relative=[IO.Path]::GetRelativePath($seed,$file.FullName);$target=Join-Path $dest $relative;New-Item -ItemType Directory -Path ([IO.Path]::GetDirectoryName($target)) -Force|Out-Null;Copy-Item -LiteralPath $file.FullName -Destination $target;$a=(Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash;$b=(Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash;if($a-ne$b){throw 'Synthetic copy hash mismatch'};$copied+=@{source=$file.FullName;target=$target;sha256=$a}};$expected=Join-Path (Split-Path -Parent $seed) 'expected.json';if(Test-Path -LiteralPath $expected){Copy-Item -LiteralPath $expected -Destination "$out/expected.json"};@{scope='Byte-identical copy of actual product synthetic checkpoint; no payload editing';files=$copied}|ConvertTo-Json -Depth 5|Set-Content "$out/seed-copy.json"}

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
