[CmdletBinding()]
param([Parameter(Mandatory)][string]$Root,[Parameter(Mandatory)][string]$WorkerPath,[ValidateSet('Comparison','Boss')][string]$Case='Comparison',[string]$ShaderCacheSource='',[string]$UnityPath='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe')
$ErrorActionPreference='Stop';$entry=Join-Path $PSScriptRoot '../DeliveryUI01/Automation/Invoke-LocalValidation.ps1';$ast=[Management.Automation.Language.Parser]::ParseFile($entry,[ref]$null,[ref]$null)
foreach($name in 'SafePath','WriteReportFile','Flush','Note','OwnedMove','StartChild','FinishChild','Step'){$def=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true);Invoke-Expression $def.Extent.Text}
$root=SafePath $Root;$project=Join-Path $root 'Project';if(!(Test-Path "$root/baseline-export.json") -or ($Case -eq 'Comparison' -and (Test-Path "$root/results.json"))){throw 'Fresh exact baseline export required'}
$export=Get-Content "$root/baseline-export.json" -Raw|ConvertFrom-Json;if($export.commit -ne 'b474765dc9c28aaf7d2d267bc0362f828f1902b0'){throw 'Wrong baseline'}
if($Case -eq 'Boss'){$root=Join-Path $root 'BossComparison';if(Test-Path $root){throw 'Fresh Boss comparison required'};New-Item -ItemType Directory $root|Out-Null}
$script:results=[Collections.Generic.List[object]]::new();$script:children=[Collections.Generic.List[object]]::new();$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$true;$script:workerPath=$WorkerPath;$dotnet=(Get-Command dotnet).Source;$MinimumUnityCommitGB=3
$data=Join-Path $root 'Rules';New-Item -ItemType Directory $data|Out-Null;$editor=Join-Path $project 'Assets/CombatPrototype/Editor/B10Comparison';New-Item -ItemType Directory $editor -Force|Out-Null
Copy-Item -LiteralPath "$PSScriptRoot/Tests/B10Comparison.cs.txt" -Destination "$editor/B10Comparison.cs"
Copy-Item -LiteralPath "$PSScriptRoot/../DeliveryUI01/Tests/UI01Before.cs.txt" -Destination "$editor/UI01Before.cs"
if($Case -eq 'Boss'){Copy-Item -LiteralPath "$PSScriptRoot/../DeliveryB07-R1/Tests/B07ReadabilityVisual.cs.txt" -Destination "$editor/B07ReadabilityVisual.cs"}
if($ShaderCacheSource -and !(Test-Path "$project/Library/ShaderCache")){$cache=SafePath $ShaderCacheSource;if(@(Get-CimInstance Win32_Process|Where-Object {$_.Name -eq 'Unity.exe' -and $_.CommandLine -like ('*'+$cache+'*')}).Count){throw 'Cache occupied'};New-Item -ItemType Directory "$project/Library" -Force|Out-Null;Copy-Item -LiteralPath "$cache/Library/ShaderCache" -Destination "$project/Library" -Recurse}
try{Step 'baseline.comparison' $UnityPath @('-projectPath',$project,'-wanxiang-storage-root',$data,'-executeMethod',$(if($Case -eq 'Boss'){'B07ReadabilityVisual.Run'}else{'B10Comparison.Run'}),'-logFile',"$data/B10Comparison.log") 780 controlled-baseline $data|Out-Null}finally{Flush;Write-Output "RESULT_ROOT=$root"}
if(@($script:results|Where-Object status -eq 'FAIL').Count){exit 1};exit 0
