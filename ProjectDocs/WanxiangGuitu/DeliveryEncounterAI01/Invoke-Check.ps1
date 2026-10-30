param([Parameter(Mandatory)][string]$Project,[Parameter(Mandatory)][string]$Output,[string]$Method='EncaiRepro.Run',[string]$WorkerPath='I:/WGP2/1028-080504-eef74f/Runtime/Worker/NativeProbe.dll',[string]$DesktopName='',[string]$StorageRoot='',[switch]$NoGraphics,[switch]$NonBatch)
$ErrorActionPreference='Stop'
$Project=[IO.Path]::GetFullPath($Project);$Output=[IO.Path]::GetFullPath($Output)
if(!$StorageRoot){$StorageRoot=$Output};$StorageRoot=[IO.Path]::GetFullPath($StorageRoot);if(!$StorageRoot.StartsWith('I:\WGCombat\',[StringComparison]::OrdinalIgnoreCase)){throw 'Owned storage required'}
if(!$Project.StartsWith('I:\WGCombat\',[StringComparison]::OrdinalIgnoreCase) -or !$Output.StartsWith('I:\WGCombat\',[StringComparison]::OrdinalIgnoreCase)){throw 'Explicit owned isolated COMBAT-AIM01 paths required'}
if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object {$_.CommandLine -like "*$Project*"}).Count){throw 'Project occupied; no user process stopped'}
New-Item -ItemType Directory -Path $Output -ErrorAction Stop|Out-Null
if(!(Test-Path -LiteralPath $StorageRoot)){New-Item -ItemType Directory -Path $StorageRoot -ErrorAction Stop|Out-Null}
$entry=Join-Path $PSScriptRoot '../DeliveryUI01/Automation/Invoke-LocalValidation.ps1'
$ast=[Management.Automation.Language.Parser]::ParseFile($entry,[ref]$null,[ref]$null)
foreach($name in 'SafePath','WriteReportFile','Flush','Note','StartChild','FinishChild','Step'){$def=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true);Invoke-Expression $def.Extent.Text}
$root=$Output;$script:results=[Collections.Generic.List[object]]::new();$script:children=[Collections.Generic.List[object]]::new();$script:desktop=if($DesktopName){if($DesktopName -notmatch '^WGTest_[a-f0-9]{32}$'){throw 'Invalid owned desktop name'};$DesktopName}else{'WGTest_'+[guid]::NewGuid().ToString('N')};$script:workerReady=$true
$script:workerPath=[IO.Path]::GetFullPath($WorkerPath);$dotnet=(Get-Command dotnet).Source;$MinimumUnityCommitGB=3
if($Method -ne "EncaiMatrix.Run" -and (Test-Path "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/EncaiMatrix.cs")){Move-Item -LiteralPath "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/EncaiMatrix.cs" -Destination "$Output/Deferred-EncaiMatrix.cs.txt"}
if($Method -ne 'EncaiGuard.Run' -and (Test-Path "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/EncaiGuard.cs")){Move-Item -LiteralPath "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/EncaiGuard.cs" -Destination "$Output/Deferred-EncaiGuard.cs.txt"}
foreach($f in Get-ChildItem "$PSScriptRoot/Tests" -Filter '*.cs.txt'){if($f.Name -eq 'EncaiGuard.cs.txt' -and $Method -ne 'EncaiGuard.Run'){continue};if($f.Name -in @('WGNormalAICheck.cs.txt','WGA1NormalResume.cs.txt','BAL02NormalObserve.cs.txt')){continue};if($f.Name -eq 'EncaiMatrix.cs.txt' -and $Method -ne 'EncaiMatrix.Run'){continue};if($f.Name -eq 'Aim01Scenarios.cs.txt'){continue};if($f.Name -eq 'BAL01Matrix.cs.txt' -and $Method -ne 'BAL01Matrix.Run'){continue};Copy-Item $f.FullName "$Project/Assets/CombatPrototype/Editor/B06LocalChecks/$($f.BaseName)";Copy-Item $f.FullName $Output}
if($Method -eq 'Build01Audit.Run'){
 $inputs=foreach($folder in 'Assets','Packages','ProjectSettings'){Get-ChildItem "$Project/$folder" -File -Recurse|ForEach-Object {@{path=$_.FullName.Substring($Project.Length+1);sha256=(Get-FileHash -LiteralPath $_.FullName).Hash;bytes=$_.Length}}}
 $inputs|ConvertTo-Json -Depth 4|Set-Content "$Output/build-inputs.json" -Encoding utf8
}
$unityArgs=@('-projectPath',$Project,'-wanxiang-storage-root',$StorageRoot,'-executeMethod',$Method,'-logFile',"$Output/Unity.log");if(!$NonBatch){$unityArgs=@('-batchmode')+$unityArgs};if($NoGraphics){$unityArgs+='-nographics'}
$r=Step $Method 'C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe' $unityArgs 1200 controlled-editor $StorageRoot
if((Test-Path "$Output/Unity.log") -and (Select-String -LiteralPath "$Output/Unity.log" -Pattern 'NullReferenceException|MissingReferenceException|error CS[0-9]+' -Quiet)){Note 'unexpected-reference-or-compile-exception' FAIL 'Raw log contains reference/compiler exception; exit0 is not sufficient' controlled-editor}
if(Test-Path (Join-Path $StorageRoot 'exception.txt')){Note 'semantic-exception-receipt' FAIL 'Test receipt records an exception; OS exit is insufficient' controlled-editor}
if(Test-Path (Join-Path $StorageRoot 'exception.txt')){Note 'semantic-exception-receipt' FAIL 'Test receipt records an exception; OS exit is insufficient' controlled-editor}
Flush
if(@($script:results|Where-Object status -eq FAIL).Count){exit 1}
if($r.status -ne 'PASS'){exit 1}

exit 0
