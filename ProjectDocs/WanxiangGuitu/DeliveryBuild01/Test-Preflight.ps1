[CmdletBinding()]
param([string]$SourceProject='D:/unity/WanxiangGuitu',[string]$TestRoot='D:/WGB01')
$ErrorActionPreference='Stop'
$root=Join-Path $TestRoot ('Preflight-'+(Get-Date -Format yyyyMMdd-HHmmss)+'-'+[guid]::NewGuid().ToString('N').Substring(0,8));New-Item -ItemType Directory $root|Out-Null
@{kind='BUILD-01 offline preflight tests';source=$SourceProject;root=$root;utc=[datetime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content "$root/owner.json"
$rows=[Collections.Generic.List[object]]::new()
function Check($name,$actual){$rows.Add([pscustomobject]@{name=$name;status=$(if($actual){'PASS'}else{'FAIL'})})}
$policy=Join-Path $PSScriptRoot 'Test-PackagePathBudget.ps1'
$short=& $policy -SourceProject $SourceProject -WorkProject (Join-Path $root 'Project')
Check 'short known input allowed' $short.allowed
Check 'all probes below MAX_PATH' (!@($short.paths|Where-Object length -ge 260).Count)
$maximum=($short.paths|ForEach-Object {$_.length-$short.project.Length}|Measure-Object -Maximum).Maximum
foreach($length in 259,260,261){
 $prefix='D:\'+('x'*($length-$maximum-3));$test=& $policy -SourceProject $SourceProject -WorkProject $prefix
 Check "longest importer path $length boundary" (($test.paths|Measure-Object length -Maximum).Maximum -eq $length -and $test.allowed -eq ($length -lt 260))
}
$old=[IO.Path]::GetFullPath('D:/WanxiangValidationRuns/Input01/20261027-151043-585c2866/FinalFrozenValidation/20261027-161647-ab2a444e/Project')
$bad=& $policy -SourceProject $SourceProject -WorkProject $old
Check 'historical failing prefix rejected read-only' (!$bad.allowed)
$fixture=Join-Path $root 'Unreviewed';New-Item -ItemType Directory "$fixture/ProjectSettings","$fixture/Packages"|Out-Null
Set-Content "$fixture/ProjectSettings/ProjectVersion.txt" 'm_EditorVersion: 6000.6.4f1'
Copy-Item -LiteralPath "$SourceProject/Packages/packages-lock.json" -Destination "$fixture/Packages"
$unknown=& $policy -SourceProject $fixture -WorkProject "$root/Unused"
Check 'different Unity version not silently certified' (!$unknown.allowed -and !$unknown.supportedInput)
# Exercise the actual prepare entry: failure must occur before project/results creation.
$pwsh=(Get-Process -Id $PID).Path;$longProject=Join-Path (Join-Path $root ('y'*95)) 'Project';$result=Join-Path $root 'NotCreated'
$psi=[Diagnostics.ProcessStartInfo]::new();$psi.FileName=$pwsh;$psi.UseShellExecute=$false;$psi.WindowStyle='Hidden';$psi.RedirectStandardOutput=$true;$psi.RedirectStandardError=$true
foreach($x in @('-NoProfile','-File',(Join-Path $PSScriptRoot '../DeliveryUI01/Invoke-Rules.ps1'),'-SourceProject',$SourceProject,'-WorkProject',$longProject,'-ArtifactsRoot',$result,'-PrepareOnly')){$psi.ArgumentList.Add($x)}
$p=[Diagnostics.Process]::Start($psi);$stdout=$p.StandardOutput.ReadToEndAsync();$stderr=$p.StandardError.ReadToEndAsync()
if(!$p.WaitForExit(30000)){throw 'Preflight tool timeout; process preserved'}
$stdout.Result|Set-Content "$root/rejected-prepare.stdout";$stderr.Result|Set-Content "$root/rejected-prepare.stderr"
@{arguments=@($psi.ArgumentList);exitCode=$p.ExitCode;timedOut=$false;forcedTermination=$false;utc=[datetime]::UtcNow.ToString('o')}|ConvertTo-Json -Depth 5|Set-Content "$root/rejected-prepare.exit.json"
Check 'real prepare refuses unsafe length' ($p.ExitCode -ne 0 -and $stderr.Result -match 'PACKAGE_PATH_BUDGET_EXCEEDED')
Check 'unsafe project not created' (!(Test-Path -LiteralPath $longProject))
Check 'unsafe results directory not created' (!(Test-Path -LiteralPath $result))
@{short=$short;historical=$bad;unreviewed=$unknown}|ConvertTo-Json -Depth 6|Set-Content "$root/policy-cases.json"
$rows|ConvertTo-Json|Set-Content "$root/results.json";$rows|Export-Csv "$root/results.csv" -NoTypeInformation
Write-Output "RESULT_ROOT=$root";$rows|Format-Table
if(@($rows|Where-Object status -eq FAIL).Count){exit 1};exit 0
