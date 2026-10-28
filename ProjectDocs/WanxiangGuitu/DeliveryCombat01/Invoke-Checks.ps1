param([Parameter(Mandatory)][string]$Project,[Parameter(Mandatory)][string]$Output,[string]$Method='Combat01Checks.Run',[string]$WorkerPath='I:/WGP2/1028-080504-eef74f/Runtime/Worker/NativeProbe.dll',[string]$DesktopName='',[string]$StorageRoot='')
$ErrorActionPreference='Stop'
$Project=[IO.Path]::GetFullPath($Project);$Output=[IO.Path]::GetFullPath($Output)
if(!$StorageRoot){$StorageRoot=$Output};$StorageRoot=[IO.Path]::GetFullPath($StorageRoot);if(!$StorageRoot.StartsWith('I:\WGCombat\',[StringComparison]::OrdinalIgnoreCase)){throw 'Owned storage required'}
if(!$Project.StartsWith('I:\WGCombat\',[StringComparison]::OrdinalIgnoreCase) -or !$Output.StartsWith('I:\WGCombat\',[StringComparison]::OrdinalIgnoreCase)){throw 'Explicit owned isolated COMBAT01 paths required'}
if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object {$_.CommandLine -like "*$Project*"}).Count){throw 'Project occupied; no user process stopped'}
New-Item -ItemType Directory -Path $Output -ErrorAction Stop|Out-Null
$entry=Join-Path $PSScriptRoot '../DeliveryUI01/Automation/Invoke-LocalValidation.ps1'
$ast=[Management.Automation.Language.Parser]::ParseFile($entry,[ref]$null,[ref]$null)
foreach($name in 'SafePath','WriteReportFile','Flush','Note','StartChild','FinishChild','Step'){$def=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true);Invoke-Expression $def.Extent.Text}
$root=$Output;$script:results=[Collections.Generic.List[object]]::new();$script:children=[Collections.Generic.List[object]]::new();$script:desktop=if($DesktopName){if($DesktopName -notmatch '^WGTest_[a-f0-9]{32}$'){throw 'Invalid owned desktop name'};$DesktopName}else{'WGTest_'+[guid]::NewGuid().ToString('N')};$script:workerReady=$true
$script:workerPath=[IO.Path]::GetFullPath($WorkerPath);$dotnet=(Get-Command dotnet).Source;$MinimumUnityCommitGB=3
if($Method.StartsWith("Combat01Save.")){Copy-Item -LiteralPath "$PSScriptRoot/Tests/Combat01Save.cs.txt" -Destination "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/Combat01Save.cs"}
Copy-Item -LiteralPath "$PSScriptRoot/Tests/Combat01Checks.cs.txt" -Destination "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/Combat01Checks.cs"
Copy-Item -LiteralPath "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/Combat01Checks.cs" -Destination "$Output/Executed-Combat01Checks.cs.txt"
$r=Step $Method 'C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe' @('-projectPath',$Project,'-wanxiang-storage-root',$StorageRoot,'-executeMethod',$Method,'-logFile',"$Output/Unity.log") 600 controlled-editor $StorageRoot
if((Test-Path "$Output/Unity.log") -and (Select-String -LiteralPath "$Output/Unity.log" -Pattern 'NullReferenceException|MissingReferenceException|error CS[0-9]+' -Quiet)){Note 'unexpected-reference-or-compile-exception' FAIL 'Raw log contains reference/compiler exception; exit0 is not sufficient' controlled-editor}
Flush
if(@($script:results|Where-Object status -eq FAIL).Count){exit 1}
if($r.status -ne 'PASS'){exit 1}
