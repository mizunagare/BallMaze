[CmdletBinding()]
param([Parameter(Mandatory)][string]$ParentRoot,[Parameter(Mandatory)][string]$BuildRoot,[Parameter(Mandatory)][string]$WorkerPath)
$ErrorActionPreference='Stop'
$parent=[IO.Path]::GetFullPath($ParentRoot);$build=[IO.Path]::GetFullPath($BuildRoot)
if((Get-Content "$parent/owner.json" -Raw|ConvertFrom-Json).kind -ne 'PLAYER-02 isolated runtime acceptance' -or !$build.StartsWith($parent+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Owned completed build clone required'}
$project=Join-Path $build 'Project';$bo=Get-Content "$build/owner.json" -Raw|ConvertFrom-Json
if($bo.project -ne $project -or !(Test-Path "$build/Results/build-report-messages.json")){throw 'Project/build identity mismatch'}
if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object {$_.CommandLine -like "*$project*"}).Count){throw 'Owned project occupied; preserved, no test started'}
$ast=[Management.Automation.Language.Parser]::ParseFile((Join-Path $PSScriptRoot '../DeliveryUI01/Automation/Invoke-LocalValidation.ps1'),[ref]$null,[ref]$null)
foreach($n in 'SafePath','WriteReportFile','Flush','Note','StartChild','FinishChild','Step'){$def=$ast.Find({param($x)$x -is [Management.Automation.Language.FunctionDefinitionAst] -and $x.Name -eq $n},$true);Invoke-Expression $def.Extent.Text}
$root=Join-Path $parent ('Rules-'+(Get-Date -Format HHmmss)+'-'+[guid]::NewGuid().ToString('N').Substring(0,8));New-Item -ItemType Directory $root|Out-Null
$driver=Join-Path $PSScriptRoot '../DeliveryInput01/Tests/Input01Rules.cs.txt'
Copy-Item $driver "$project/Assets/CombatPrototype/Editor/B06LocalChecks/Input01Rules.cs";Copy-Item $driver "$root/Executed-Input01Rules.cs.txt"
@{kind='PLAYER-02 supporting Editor regression';project=$project;driverSha256=(Get-FileHash $driver).Hash;scope='Existing Input01Rules only; never a substitute for runtime Player acceptance'}|ConvertTo-Json|Set-Content "$root/owner.json"
$script:results=[Collections.Generic.List[object]]::new();$script:children=[Collections.Generic.List[object]]::new();$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$true;$script:workerPath=SafePath $WorkerPath;$dotnet=(Get-Command dotnet).Source;$MinimumUnityCommitGB=3
$unity='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe'
$r=Step 'Input01Rules.Run' $unity @('-batchmode','-projectPath',$project,'-wanxiang-storage-root',$root,'-executeMethod','Input01Rules.Run','-logFile',"$root/Input01Rules.log") 600 supporting-editor-regression $root
Flush;Write-Output "RULE_ROOT=$root";if($r.status -ne 'PASS'){exit 1};exit 0
