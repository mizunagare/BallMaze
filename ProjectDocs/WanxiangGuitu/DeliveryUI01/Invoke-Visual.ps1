[CmdletBinding()]
param([Parameter(Mandatory)][string]$SourceProject,[Parameter(Mandatory)][string]$WorkProject,[Parameter(Mandatory)][string]$IsolationRoot,[ValidateSet('Before','After')][string]$Mode='After',[string]$UnityPath='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe')
$ErrorActionPreference='Stop'
$source=[IO.Path]::GetFullPath($SourceProject);$work=[IO.Path]::GetFullPath($WorkProject);$root=[IO.Path]::GetFullPath($IsolationRoot)
if(![IO.Path]::IsPathFullyQualified($IsolationRoot) -or $root -match '(?i)(^|[\\/])LocalLow([\\/]|$)' -or $work -eq $source -or $work.StartsWith($source+[IO.Path]::DirectorySeparatorChar) -or (Test-Path -LiteralPath $root)){throw 'Use existing isolated copy and fresh explicit results outside source and LocalLow'}
for($a=$root;$a;$a=[IO.Path]::GetDirectoryName($a)){if((Test-Path -LiteralPath $a) -and ((Get-Item -LiteralPath $a -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'Reparse test root rejected'}}
if(Get-CimInstance Win32_Process | Where-Object {$_.Name -eq 'Unity.exe' -and $_.CommandLine -like ('*'+$work+'*')}){throw 'Test copy already open'}
$editor=Join-Path $work 'Assets/CombatPrototype/Editor/B06LocalChecks'
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'Tests/UI01Before.cs.txt') -Destination (Join-Path $editor 'UI01Before.cs')
if($Mode -eq 'After'){Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'Tests/UI01Visual.cs.txt') -Destination (Join-Path $editor 'UI01Visual.cs')}
New-Item -ItemType Directory -Path $root | Out-Null
$method=if($Mode -eq 'Before'){'UI01Before.Run'}else{'UI01Visual.Run'}
$psi=[Diagnostics.ProcessStartInfo]::new();$psi.FileName=$UnityPath;$psi.UseShellExecute=$false;$psi.WindowStyle='Hidden';$psi.Environment['UNITY_TEST_ROOT']=$root
foreach($arg in @('-projectPath',$work,'-wanxiang-storage-root',$root,'-executeMethod',$method,'-logFile',(Join-Path $root 'capture.log'))){$psi.ArgumentList.Add($arg)}
$p=[Diagnostics.Process]::Start($psi);$timeout=!$p.WaitForExit(660000);if($timeout){$p.Kill();$p.WaitForExit()}
$receipt=if($Mode -eq 'Before'){'before-result.txt'}else{'visual-result.txt'}
$pass=!$timeout -and $p.ExitCode -eq 0 -and (Test-Path (Join-Path $root $receipt))
@{method=$method;exitCode=$p.ExitCode;timedOut=$timeout;passed=$pass;source=$source;copy=$work;root=$root;mode=$Mode} | ConvertTo-Json | Set-Content (Join-Path $root 'capture-process.json') -Encoding utf8
if(!$pass){throw 'Screenshot run failed; do not claim PASS'}
