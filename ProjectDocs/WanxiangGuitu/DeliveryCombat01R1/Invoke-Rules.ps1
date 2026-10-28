param([Parameter(Mandatory)][string]$ParentRoot,[Parameter(Mandatory)][string]$BuildRoot)
$ErrorActionPreference='Stop';$parent=[IO.Path]::GetFullPath($ParentRoot);$project=[IO.Path]::GetFullPath("$BuildRoot/Project")
if((Get-Content "$parent/owner.json" -Raw|ConvertFrom-Json).kind -ne 'PLAYER-02 isolated runtime acceptance' -or !$project.StartsWith($parent+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Owned completed build clone required'}
if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$project*").Count){throw 'Occupied project preserved'}
$root=Join-Path $parent 'Rules';New-Item -ItemType Directory $root|Out-Null
$original=Join-Path $PSScriptRoot '../DeliveryCombat01/Tests/Combat01Checks.cs.txt';$code=Get-Content $original -Raw
$anchor='if(s==null||!s.Saves.IsInitialized)return;run=Cases();'
if(!$code.Contains($anchor)){throw 'Reviewed controlled test initialization anchor changed'}
$code=$code.Replace('view=UI01Before.Size(1280,720);','if(!Application.isBatchMode)view=UI01Before.Size(1280,720);').Replace($anchor,'if(s==null)return;if(!s.Saves.IsInitialized){if(Application.isBatchMode&&s.WorldReady)s.Saves.InitializeStorage(root+"/ControlledSave",false);else return;}run=Cases();')
$target="$project/Assets/CombatPrototype/Editor/B06LocalChecks/Combat01Checks.cs";Set-Content $target $code -NoNewline;Copy-Item $target "$root/Executed-Combat01Checks.cs.txt"
@{source=$original;sourceSha256=(Get-FileHash $original).Hash;forkSha256=(Get-FileHash $target).Hash;change='Batch-mode explicit public storage initialization after WorldReady; skip GUI GameView; no assertions changed';scope='Controlled Editor only; not native UI or Player evidence'}|ConvertTo-Json|Set-Content "$root/test-fork.json"
$ast=[Management.Automation.Language.Parser]::ParseFile((Join-Path $PSScriptRoot '../DeliveryUI01/Automation/Invoke-LocalValidation.ps1'),[ref]$null,[ref]$null)
foreach($n in 'SafePath','WriteReportFile','Flush','Note','StartChild','FinishChild','Step'){$def=$ast.Find({param($x)$x -is [Management.Automation.Language.FunctionDefinitionAst] -and $x.Name -eq $n},$true);Invoke-Expression $def.Extent.Text}
$script:results=[Collections.Generic.List[object]]::new();$script:children=[Collections.Generic.List[object]]::new();$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$true;$script:workerPath="$parent/Host/Worker/NativeProbe.dll";$dotnet=(Get-Command dotnet).Source;$MinimumUnityCommitGB=3
$r=Step 'Combat01Checks.Run' 'C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe' @('-batchmode','-projectPath',$project,'-wanxiang-storage-root',$root,'-executeMethod','Combat01Checks.Run','-logFile',"$root/Unity.log") 600 controlled-editor $root
if((Test-Path "$root/Unity.log") -and (Select-String "$root/Unity.log" -Pattern 'NullReferenceException|MissingReferenceException|error CS[0-9]+' -Quiet)){Note 'unexpected-reference-or-compile-exception' FAIL 'Raw exceptions retained; exit0 alone is insufficient' controlled-editor}
Flush;if(@($script:results|Where-Object status -eq FAIL).Count){exit 1}
