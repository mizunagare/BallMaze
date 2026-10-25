[CmdletBinding()]
param([string]$TestRoot='D:/WanxiangValidationRuns/B09MemoryGuard')
$ErrorActionPreference='Stop'
$entry=Join-Path $PSScriptRoot '../DeliveryUI01/Automation/Invoke-LocalValidation.ps1'
$ast=[Management.Automation.Language.Parser]::ParseFile($entry,[ref]$null,[ref]$null)
foreach($name in 'SafePath','WriteReportFile','Flush','StartChild','FinishChild','Step'){
 $def=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true)
 Invoke-Expression $def.Extent.Text
}
$base=SafePath $TestRoot
$source=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot "../../.."));if($base -eq $source -or $base.StartsWith($source+"\",[StringComparison]::OrdinalIgnoreCase)){throw "External test root required"}
$root=Join-Path $base ((Get-Date -Format 'yyyyMMdd-HHmmss')+'-'+[guid]::NewGuid().ToString('N').Substring(0,8))
New-Item -ItemType Directory $root -Force|Out-Null
$script:results=[Collections.Generic.List[object]]::new();$script:children=[Collections.Generic.List[object]]::new()
$script:workerReady=$false;$script:workerPath='';$script:reportRetryCount=0
$MinimumUnityCommitGB=100000
@{kind='B09 isolated memory-guard tool check';root=$root;scriptSha256=(Get-FileHash $PSCommandPath).Hash;orchestratorSha256=(Get-FileHash $entry).Hash;policy='Impossible requested headroom, no Unity process should launch'}|ConvertTo-Json|Set-Content "$root/owner.json"
$r=Step 'memory-rejection' 'C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe' @('-batchmode','-wanxiang-storage-root',$root,'-projectPath',"$root/UnusedProject",'-executeMethod','B09Probe.Run') 10 controlled
$ok=$r.status -eq 'NOT_RUN' -and $null -eq $r.exitCode -and !$r.timedOut -and $script:children.Count -eq 0 -and $r.reason.Contains('ENV_RESOURCE_BLOCKED:')
@{status=$(if($ok){'PASS'}else{'FAIL'});childCount=$script:children.Count;actualResult=$r;scope='Existing orchestrator safety guard only; no Unity or product acceptance'}|ConvertTo-Json -Depth 8|Set-Content "$root/b09-memory-guard.json"
Write-Output "RESULT_ROOT=$root"
if(!$ok){exit 1};exit 0
