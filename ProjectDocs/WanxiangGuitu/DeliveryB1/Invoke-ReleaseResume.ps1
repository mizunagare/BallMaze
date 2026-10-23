[CmdletBinding()]
param([Parameter(Mandatory)][string]$Executable,[Parameter(Mandatory)][string]$IsolationRoot,[Parameter(Mandatory)][string]$FixtureDirectory)
$ErrorActionPreference='Stop'
$root=[IO.Path]::GetFullPath($IsolationRoot);$fixture=[IO.Path]::GetFullPath($FixtureDirectory)
if(![IO.Path]::IsPathFullyQualified($IsolationRoot) -or $root -match '(?i)(^|[\\/])LocalLow([\\/]|$)' -or $fixture -match '(?i)(^|[\\/])LocalLow([\\/]|$)' -or (Test-Path -LiteralPath $root)){throw 'Fresh explicit test root and synthetic fixture required'}
for($a=$root;$a;$a=[IO.Path]::GetDirectoryName($a)){if((Test-Path -LiteralPath $a) -and ((Get-Item -LiteralPath $a -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'Reparse root rejected'}}
$target=Join-Path $root 'WanxiangGuitu/ForestRuins';New-Item -ItemType Directory -Path ([IO.Path]::GetDirectoryName($target)) -Force | Out-Null
Copy-Item -LiteralPath $fixture -Destination $target -Recurse
function Snapshot{
 $e=Get-Content -LiteralPath (Join-Path $target 'save.json') -Raw | ConvertFrom-Json;$d=$e.payload | ConvertFrom-Json
 if(!$d.hasActiveRun){throw 'Fixture must be a synthetic active run'}
 return [ordered]@{profile=$d.profile.profileId;run=$d.activeRun.runId;instance=$d.activeRun.regionInstanceId;seed=$d.activeRun.checkpoint.forest.seed;exits=($d.activeRun.checkpoint.forest.exits | ConvertTo-Json -Compress);materials=($d.activeRun.checkpoint.materials -join ',');brought=($d.activeRun.broughtRemaining -join ',');earned=($d.activeRun.earnedRemaining -join ',')}
}
Add-Type @'
using System;using System.Runtime.InteropServices;
public static class B1Close {
 public delegate bool EnumProc(IntPtr h,IntPtr p);
 [DllImport("user32.dll")] static extern bool EnumWindows(EnumProc cb,IntPtr p);
 [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr h,out uint pid);
 [DllImport("user32.dll")] static extern bool PostMessage(IntPtr h,uint m,IntPtr w,IntPtr l);
 public static int Close(int process){int count=0;EnumWindows((h,p)=>{uint id;GetWindowThreadProcessId(h,out id);if(id==process&&PostMessage(h,0x10,IntPtr.Zero,IntPtr.Zero))count++;return true;},IntPtr.Zero);return count;}
}
'@
$expected=Snapshot;$results=@()
foreach($pass in 1,2){
 $psi=[Diagnostics.ProcessStartInfo]::new();$psi.FileName=[IO.Path]::GetFullPath($Executable);$psi.UseShellExecute=$false;$psi.WindowStyle='Hidden'
 foreach($arg in @('-screen-fullscreen','0','-screen-width','1280','-screen-height','720','-wanxiang-storage-root',$root,'-logFile',(Join-Path $root ('release-'+$pass+'.log')))){$psi.ArgumentList.Add($arg)}
 $proc=[Diagnostics.Process]::Start($psi);$watch=[Diagnostics.Stopwatch]::StartNew();$ready=$false
 while($watch.Elapsed.TotalSeconds -lt 60 -and !$proc.HasExited){
  if(Test-Path (Join-Path $root 'storage-audit.jsonl')){$audit=@(Get-Content (Join-Path $root 'storage-audit.jsonl') | ForEach-Object {$_ | ConvertFrom-Json});if(@($audit | Where-Object operation -eq 'initialize').Count -ge $pass){$ready=$true;break}}
  Start-Sleep -Milliseconds 200
 }
 if(!$ready){throw 'Release initialization not observed'}
 Start-Sleep -Seconds 2
 $windows=[B1Close]::Close($proc.Id);$timeout=!$proc.WaitForExit(30000)
 if($timeout){$proc.Kill();$proc.WaitForExit()}
 $actual=Snapshot;$same=($expected | ConvertTo-Json -Compress) -eq ($actual | ConvertTo-Json -Compress)
 $audit=@(Get-Content (Join-Path $root 'storage-audit.jsonl') | ForEach-Object {$_ | ConvertFrom-Json});$quit=@($audit | Where-Object operation -eq 'quit').Count -ge $pass
 $results+=@{pass=$pass;exitCode=$proc.ExitCode;timedOut=$timeout;ownedWindowsSentWmClose=$windows;quitReceipt=$quit;sameRunAndRepairAndLedger=$same;snapshot=$actual}
 $results | ConvertTo-Json -Depth 8 | Set-Content (Join-Path $root 'release-resume-results.json') -Encoding utf8
 if($timeout -or $proc.ExitCode -ne 0 -or !$quit -or !$same -or $windows -eq 0){throw 'Release normal close/resume failed (forced timeout is never PASS)'}
}
