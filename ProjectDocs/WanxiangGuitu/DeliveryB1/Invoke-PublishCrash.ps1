[CmdletBinding()]
param([Parameter(Mandatory)][string]$WorkProject,[Parameter(Mandatory)][string]$ArtifactsRoot,[string]$UnityPath='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe')
$ErrorActionPreference='Stop'
$root=[IO.Path]::GetFullPath($ArtifactsRoot)
if(![IO.Path]::IsPathFullyQualified($ArtifactsRoot) -or $root -match '(?i)(^|[\\/])LocalLow([\\/]|$)' -or (Test-Path -LiteralPath $root)){throw 'Fresh isolated artifacts root required'}
New-Item -ItemType Directory -Path $root | Out-Null
$results=@()
foreach($case in @(@{method='WGB1CrashCheck.Publish';expected=29},@{method='WGB1CrashCheck.Resume';expected=0})){
 $psi=[Diagnostics.ProcessStartInfo]::new();$psi.FileName=$UnityPath;$psi.UseShellExecute=$false;$psi.WindowStyle='Hidden';$psi.Environment['UNITY_TEST_ROOT']=$root
 foreach($arg in @('-batchmode','-projectPath',$WorkProject,'-executeMethod',$case.method,'-logFile',(Join-Path $root ($case.method+'.log')))){$psi.ArgumentList.Add($arg)}
 $p=[Diagnostics.Process]::Start($psi);$timeout=!$p.WaitForExit(120000);if($timeout){$p.Kill();$p.WaitForExit()}
 $ok=!$timeout -and $p.ExitCode -eq $case.expected
 if($case.expected -eq 29){$ok=$ok -and (Test-Path (Join-Path $root 'abrupt-exit-intent.txt'))}else{$ok=$ok -and (Select-String -LiteralPath (Join-Path $root ($case.method+'.log')) -Pattern 'B1_V08_ABRUPT_PROCESS_RESTART_PASS' -Quiet)}
 $results+=@{method=$case.method;expectedExit=$case.expected;exitCode=$p.ExitCode;timedOut=$timeout;passed=$ok};$results | ConvertTo-Json | Set-Content (Join-Path $root 'process-results.json') -Encoding utf8
 if(!$ok){throw 'Controlled publication interruption or restart failed'}
}
