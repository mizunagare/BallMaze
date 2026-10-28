param([Parameter(Mandatory)][string]$Project,[Parameter(Mandatory)][string]$Output,[string]$Method='UX02Checks.Run',[switch]$Batch,[string]$StorageRoot='')
$ErrorActionPreference='Stop'
$Project=[IO.Path]::GetFullPath($Project);$Output=[IO.Path]::GetFullPath($Output)
if(!$Project.StartsWith('I:\WGCombat\',[StringComparison]::OrdinalIgnoreCase) -or !$Output.StartsWith('I:\WGCombat\',[StringComparison]::OrdinalIgnoreCase)){throw 'Explicit owned isolated root required'}
if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object {$_.CommandLine -like "*$Project*"}).Count){throw 'Occupied project; no processes closed'}
New-Item -ItemType Directory $Output -ErrorAction Stop|Out-Null
if(!$StorageRoot){$StorageRoot=$Output};$StorageRoot=[IO.Path]::GetFullPath($StorageRoot);if(!$StorageRoot.StartsWith('I:\WGCombat\',[StringComparison]::OrdinalIgnoreCase)){throw 'Owned shared synthetic storage required'};New-Item -ItemType Directory $StorageRoot -Force|Out-Null
$entry=Join-Path $PSScriptRoot '../DeliveryUI01/Automation/Invoke-LocalValidation.ps1';$ast=[Management.Automation.Language.Parser]::ParseFile($entry,[ref]$null,[ref]$null)
foreach($name in 'SafePath','WriteReportFile','Flush','Note','StartChild','FinishChild','Step'){$def=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true);Invoke-Expression $def.Extent.Text}
$root=$Output;$script:results=[Collections.Generic.List[object]]::new();$script:children=[Collections.Generic.List[object]]::new();$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$true;$script:workerPath='I:/WGP2/1028-080504-eef74f/Runtime/Worker/NativeProbe.dll';$dotnet=(Get-Command dotnet).Source;$MinimumUnityCommitGB=3
Get-ChildItem "$PSScriptRoot/Tests" -Filter '*.cs.txt'|ForEach-Object {Copy-Item -LiteralPath $_.FullName -Destination "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/$($_.BaseName)"}
Copy-Item "$PSScriptRoot/../DeliveryCombat01/Tests/Combat01Checks.cs.txt" "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/Combat01Checks.cs"
Copy-Item "$PSScriptRoot/Tests/UX02Checks.cs.txt" "$Output/Executed-UX02Checks.cs.txt"
$arguments=@('-projectPath',$Project,'-wanxiang-storage-root',$StorageRoot,'-executeMethod',$Method,'-logFile',"$Output/Unity.log");if($Batch){$arguments+='-batchmode'}
$r=Step $Method 'C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe' $arguments 600 controlled-editor $StorageRoot
if((Test-Path "$Output/Unity.log") -and (Select-String -LiteralPath "$Output/Unity.log" -Pattern 'NullReferenceException|MissingReferenceException|error CS[0-9]+|Health observation subscriber failed' -Quiet)){Note 'unexpected-product-reference-or-compile-error' FAIL 'Raw compiler/reference exception; child exit0 alone is insufficient' controlled-editor}
Flush
if($r.status -ne 'PASS' -or @($script:results|Where-Object status -eq 'FAIL').Count){exit 1}
exit 0
