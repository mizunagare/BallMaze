[CmdletBinding()]
param([Parameter(Mandatory)][string]$PlayerExe,[Parameter(Mandatory)][string]$IsolationRoot,
 [string]$SyntheticFixtureRoot,[switch]$Resume,[ValidateSet('Default','D3D11')][string]$Renderer='Default',
 [int]$TimeoutSeconds=600)
$ErrorActionPreference='Stop'
function CheckPath([string]$path){
 if(![IO.Path]::IsPathFullyQualified($path)){throw 'Absolute path required'}
 $full=[IO.Path]::GetFullPath($path)
 if($full -match '(?i)(^|[\\/])LocalLow([\\/]|$)' -or !$full.TrimEnd('\','/').Contains([IO.Path]::DirectorySeparatorChar)){throw 'Player directory or drive root rejected'}
 for($a=$full;$a;$a=[IO.Path]::GetDirectoryName($a)){if((Test-Path -LiteralPath $a) -and ((Get-Item -LiteralPath $a -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'Reparse path rejected'}}
 return $full
}
$root=CheckPath $IsolationRoot;$exe=[IO.Path]::GetFullPath($PlayerExe)
if(!(Test-Path -LiteralPath $exe) -or $TimeoutSeconds -lt 1){throw 'Missing Player or invalid timeout'}
if($Resume){if(!(Test-Path (Join-Path $root 'synthetic-test.json'))){throw 'Resume only a launcher-created synthetic root'}}
else{
 if(Test-Path -LiteralPath $root){throw 'New launch requires fresh root'}
 $fixture=CheckPath $SyntheticFixtureRoot
 if(!(Test-Path (Join-Path $fixture 'fixture.txt')) -or (Get-Content (Join-Path $fixture 'fixture.txt') -Raw) -notmatch '^SYNTHETIC'){throw 'Explicit synthetic fixture marker required; never copy a player directory'}
 if(Get-ChildItem -LiteralPath $fixture -Recurse -Force | Where-Object { $_.Attributes -band [IO.FileAttributes]::ReparsePoint }){throw 'Linked fixture content rejected'}
 New-Item -ItemType Directory $root|Out-Null
 Copy-Item -LiteralPath (Join-Path $fixture 'WanxiangGuitu') -Destination $root -Recurse
 @{fixture=$fixture;createdUtc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content (Join-Path $root 'synthetic-test.json')
}
$stamp=Get-Date -Format 'yyyyMMdd-HHmmss-fff';$save=Join-Path $root 'WanxiangGuitu/ForestRuins/save.json'
Copy-Item -LiteralPath $save -Destination (Join-Path $root ("before-$stamp.json"))
$log=Join-Path $root ("player-$stamp.log")
$psi=[Diagnostics.ProcessStartInfo]::new();$psi.FileName=$exe;$psi.UseShellExecute=$false
# Visible window is required for the explicitly requested native UI test.
foreach($arg in @('-wanxiang-storage-root',$root,'-screen-fullscreen','0','-screen-width','1280','-screen-height','720','-logFile',$log)){$psi.ArgumentList.Add($arg)}
if($Renderer -eq 'D3D11'){$psi.ArgumentList.Add('-force-d3d11')}
$start=[DateTime]::UtcNow;$p=[Diagnostics.Process]::Start($psi);$handle=$p.Handle
@{pid=$p.Id;startUtc=$start.ToString('o');exe=$exe;sha256=(Get-FileHash $exe -Algorithm SHA256).Hash;renderer=$Renderer;log=$log;closeMethod='Operator clicks normal window close button; no automated close or kill';arguments=@($psi.ArgumentList)}|ConvertTo-Json -Depth 4|Set-Content (Join-Path $root ("launch-$stamp.json"))
Write-Host "Native test PID $($p.Id). Use visible in-game buttons; close with the title-bar X. Do not press physical Escape or kill the process."
$ended=$p.WaitForExit($TimeoutSeconds*1000)
@{pid=$p.Id;startUtc=$start.ToString('o');endUtc=[DateTime]::UtcNow.ToString('o');exitCode=if($ended){$p.ExitCode}else{$null};timedOut=!$ended;forcedTermination=$false}|ConvertTo-Json|Set-Content (Join-Path $root ("process-$stamp.json"))
if($ended){Copy-Item -LiteralPath $save -Destination (Join-Path $root ("after-$stamp.json"))}
# Deliberately do not kill on timeout and never infer clean exit merely from zero.
if(!$ended){throw 'Timed out; process not killed. Record FAIL/NOT_RUN and arrange normal close.'}
if($p.ExitCode -ne 0){throw "Player exit code $($p.ExitCode)"}
Write-Host 'Exit observed; run analyze-player-close.py to validate audit, save and native error markers before claiming PASS.'
