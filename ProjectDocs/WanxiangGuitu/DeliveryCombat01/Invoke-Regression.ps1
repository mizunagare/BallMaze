param([Parameter(Mandatory)][string]$Project,[Parameter(Mandatory)][string]$Output,[string]$WorkerPath='I:/WGP2/1028-080504-eef74f/Runtime/Worker/NativeProbe.dll')
$ErrorActionPreference='Stop';$Project=[IO.Path]::GetFullPath($Project);$Output=[IO.Path]::GetFullPath($Output)
if(!$Project.StartsWith('I:\WGCombat\',[StringComparison]::OrdinalIgnoreCase) -or !$Output.StartsWith('I:\WGCombat\',[StringComparison]::OrdinalIgnoreCase)){throw 'Owned external COMBAT01 paths required'}
if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object CommandLine -Like "*$Project*").Count){throw 'Project occupied'}
New-Item -ItemType Directory $Output | Out-Null
$ast=[Management.Automation.Language.Parser]::ParseFile((Join-Path $PSScriptRoot '../DeliveryUI01/Automation/Invoke-LocalValidation.ps1'),[ref]$null,[ref]$null)
foreach($name in 'SafePath','WriteReportFile','Flush','Note','StartChild','FinishChild','Step'){$def=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true);Invoke-Expression $def.Extent.Text}
$root=$Output;$script:results=[Collections.Generic.List[object]]::new();$script:children=[Collections.Generic.List[object]]::new();$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$true;$script:workerPath=[IO.Path]::GetFullPath($WorkerPath);$dotnet=(Get-Command dotnet).Source;$MinimumUnityCommitGB=3
foreach($method in 'Input01Rules.Run','S2R1ObservationProbe.Run','B07Combat.Run'){
 $data=Join-Path $Output $method;New-Item -ItemType Directory $data|Out-Null
 $r=Step $method 'C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe' @('-projectPath',$Project,'-wanxiang-storage-root',$data,'-executeMethod',$method,'-logFile',"$data/Unity.log") 600 controlled-editor $data
 if($r.timedOut){Flush;exit 1}
}
# Existing normal-AI driver classes are temporarily moved only in this disposable clone.
$deferred=Join-Path $Output 'Deferred';New-Item -ItemType Directory $deferred|Out-Null
foreach($name in 'WGNormalAICheck.cs','WGA1NormalResume.cs','B06OriginalPlay.cs'){foreach($suffix in '','.meta'){$from="$Project/Assets/CombatPrototype/Editor/B06LocalChecks/$name$suffix";if(Test-Path $from){Move-Item -LiteralPath $from -Destination "$deferred/$name$suffix"}}}
$pwsh=(Get-Process -Id $PID).Path;$passed=$true
foreach($mode in 'Normal','Resume','FinalResume'){
 if(!$passed){Note "AI.$mode" NOT_RUN 'Previous dependent stage failed' normal-ai;continue}
 $r=Step "AI.$mode" $pwsh @('-NoProfile','-File',(Join-Path $PSScriptRoot '../DeliveryUI01/Invoke-NormalAI.ps1'),'-SourceProject',$Project,'-IsolationRoot',"$Output/Normal-Gather",'-Mode',$mode,'-LeaveTimedOutProcess','-ExternalWorkerPath',$script:workerPath,'-DesktopName',$script:desktop,'-B4','-Strategy','Gather') 420 normal-ai
 $passed=$r.status -eq 'PASS'
}
Flush
if(@($script:results|Where-Object status -eq FAIL).Count){exit 1}
