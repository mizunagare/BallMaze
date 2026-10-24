[CmdletBinding()]
param([Parameter(Mandatory)][string]$PreparedRunRoot,[Parameter(Mandatory)][string]$SourceProject,
 [string]$TestRoot='C:/Users/guan/Documents/unitytest/WanxiangB2Visual',
 [string]$UnityPath='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe')
$ErrorActionPreference='Stop'
# Reuse the reviewed orchestration helpers, not a second process/test framework.
$entry=Join-Path $PSScriptRoot '../DeliveryUI01/Automation/Invoke-LocalValidation.ps1'
$ast=[Management.Automation.Language.Parser]::ParseFile($entry,[ref]$null,[ref]$null)
foreach($name in 'SafePath','WriteReportFile','Flush','StartChild','FinishChild','Step'){
 $definition=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true)
 Invoke-Expression $definition.Extent.Text
}
$prepared=SafePath $PreparedRunRoot;$source=SafePath $SourceProject;$base=SafePath $TestRoot
if($base -eq $source -or $base.StartsWith($source+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'External output root required'}
$owner=Get-Content (Join-Path $prepared 'owner.json') -Raw|ConvertFrom-Json
if($owner.source -ne $source -or $owner.kind -ne 'WanxiangGuitu isolated unattended run'){throw 'Only owned isolated prepared projects allowed'}
$project=Join-Path $prepared 'Project'
if(@(Get-CimInstance Win32_Process|Where-Object {$_.Name -eq 'Unity.exe' -and $_.CommandLine -like ('*'+$project+'*')}).Count){throw 'Prepared project occupied; no overwrite or close'}
$root=Join-Path $base ((Get-Date -Format 'yyyyMMdd-HHmmss')+'-'+[guid]::NewGuid().ToString('N').Substring(0,8))
New-Item -ItemType Directory $root -Force|Out-Null
$script:results=[Collections.Generic.List[object]]::new();$script:children=[Collections.Generic.List[object]]::new()
$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$true;$script:workerPath=Join-Path $prepared 'Worker/NativeProbe.dll';$dotnet=(Get-Command dotnet).Source
$from=Join-Path $PSScriptRoot 'Tests/B2Visual.cs.txt';$to=Join-Path $project 'Assets/CombatPrototype/Editor/B06LocalChecks/B2Visual.cs'
if((Test-Path $to) -and (Get-FileHash $to).Hash -ne (Get-FileHash $from).Hash){throw 'Unexpected existing driver; preserve for inspection'}
Copy-Item -LiteralPath $from -Destination $to
@{kind='B2 controlled visual only';prepared=$prepared;source=$source;utc=[datetime]::UtcNow.ToString('o');scope='Synthetic setup, disabled NPC, no native input; not U16'}|ConvertTo-Json|Set-Content "$root/owner.json"
$result=Step 'b2.visual' $UnityPath @('-projectPath',$project,'-wanxiang-storage-root',$root,'-executeMethod','B2Visual.Run','-logFile',"$root/visual.log") 240 'controlled-visual' $root
$alive=@($script:children|Where-Object {!$_.process.HasExited}|ForEach-Object {$_.process.Id});ConvertTo-Json -InputObject $alive|Set-Content "$root/preserved-processes.json"
Write-Output "RESULT_ROOT=$root"
if($result.status -ne 'PASS' -or !(Test-Path "$root/b2-visual-result.txt")){exit 1};exit 0
