[CmdletBinding()]
param([Parameter(Mandatory)][string]$SourceProject,[Parameter(Mandatory)][string]$TestRoot,[Parameter(Mandatory)][string]$Fixture,[Parameter(Mandatory)][string]$PendingFixture,[Parameter(Mandatory)][string]$WorkerPath,[Parameter(Mandatory)][ValidatePattern('^WGTest_[0-9a-f]{32}$')][string]$DesktopName,[string]$UnityPath='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe',[string]$ShaderCacheSource='')
$ErrorActionPreference='Stop';$main=Join-Path $PSScriptRoot '../DeliveryUI01/Automation/Invoke-LocalValidation.ps1';$ast=[Management.Automation.Language.Parser]::ParseFile($main,[ref]$null,[ref]$null)
foreach($name in 'SafePath','WriteReportFile','Flush','Note','OwnedMove','StartChild','FinishChild','Step'){$def=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true);Invoke-Expression $def.Extent.Text}
$source=SafePath $SourceProject;$root=SafePath $TestRoot;if(Test-Path $root){throw 'Fresh controlled Player root required'};if($root.StartsWith($source+'\',[StringComparison]::OrdinalIgnoreCase) -or $root -match '(?i)LocalLow'){throw 'External isolated root required'}
New-Item -ItemType Directory $root|Out-Null;$script:results=[Collections.Generic.List[object]]::new();$script:children=[Collections.Generic.List[object]]::new();$script:desktop=$DesktopName;$script:workerReady=$true;$script:workerPath=$WorkerPath;$dotnet=(Get-Command dotnet).Source;$MinimumUnityCommitGB=3;$project=Join-Path $root 'Project';$data=Join-Path $root 'Rules';$pwsh=(Get-Process -Id $PID).Path
@{kind='B10 separate controlled nondevelopment Player';source=$source;root=$root;scope='uGUI callbacks, not native input';utc=[datetime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content "$root/owner.json"
function CopyFixture($from,$storage){$from=SafePath $from;if($from -match '(?i)LocalLow' -or !(Test-Path "$from/save.json")){throw 'Explicit synthetic fixture required'};if(@(Get-ChildItem -LiteralPath $from -Recurse -Force|Where-Object {($_.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0}).Count){throw 'Fixture links refused'};$dest=Join-Path $storage 'WanxiangGuitu/ForestRuins';New-Item -ItemType Directory $dest -Force|Out-Null;Copy-Item -Path "$from/*" -Destination $dest -Recurse}
try{
 $r=Step 'prepare' $pwsh @('-NoProfile','-File',"$PSScriptRoot/../DeliveryUI01/Invoke-Rules.ps1",'-SourceProject',$source,'-WorkProject',$project,'-ArtifactsRoot',$data,'-PrepareOnly') 180
 if($r.status -eq 'PASS'){
  if($ShaderCacheSource){$cache=SafePath $ShaderCacheSource;if(@(Get-CimInstance Win32_Process|Where-Object {$_.Name -eq 'Unity.exe' -and $_.CommandLine -like ('*'+$cache+'*')}).Count){throw 'Shader cache occupied'};New-Item -ItemType Directory "$project/Library" -Force|Out-Null;Copy-Item -LiteralPath "$cache/Library/ShaderCache" -Destination "$project/Library" -Recurse}
  $env:B10_PLAYER_DRIVER_TEMPLATE=Join-Path $PSScriptRoot 'Tests/B10ControlledPlayer.cs.source'
  $prep=Step 'controller.prepare' $UnityPath @('-batchmode','-projectPath',$project,'-wanxiang-storage-root',$root,'-executeMethod','B10ControlledBuild.Prepare','-logFile',"$root/prepare-controller.log") 600 controlled-build $root
  if($prep.status -eq 'PASS'){$build=Step 'controller.build' $UnityPath @('-batchmode','-projectPath',$project,'-wanxiang-storage-root',$root,'-executeMethod','B10ControlledBuild.Build','-logFile',"$root/build-controller.log") 600 controlled-build $root}else{Note 'controller.build' NOT_RUN 'Preparation failed' controlled-build}
  if($build.status -eq 'PASS'){
   $exe=Join-Path $root 'Build/Validation/WanxiangGuitu.exe';@{exe=(Get-FileHash -LiteralPath $exe).Hash;assembly=(Get-FileHash "$root/Build/Validation/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll").Hash;scope='separate nondevelopment validation build, controller included; NOT shipping binary'}|ConvertTo-Json|Set-Content "$root/build-hashes.json"
   $canResume=$false
   foreach($case in @('read','continue','new','pending')){
    if($case -eq 'continue' -and !$canResume){Note 'player.continue' NOT_RUN 'First process failed; do not claim resume' controlled-player;continue}
    if(@(Get-CimInstance Win32_Process|Where-Object Name -eq 'WanxiangGuitu.exe').Count){Note "player.$case" NOT_RUN 'Player conflict; preserve process' environment;continue}
    $storage=Join-Path $root $(if($case -eq 'continue'){'Case-read'}else{"Case-$case"});if($case -ne 'continue'){New-Item -ItemType Directory $storage|Out-Null;if($case -eq 'read'){CopyFixture $Fixture $storage};if($case -eq 'pending'){CopyFixture $PendingFixture $storage}}
    $result=Join-Path $storage 'b10-controlled-result.json';if($case -eq 'continue'){Move-Item -LiteralPath $result -Destination "$storage/b10-controlled-first-result.json"}
    $w=if($case -eq 'continue'){1920}else{1280};$h=if($case -eq 'continue'){1080}else{720}
    $r=Step "player.$case" $exe @('-force-d3d11','-wanxiang-storage-root',$storage,'-wanxiang-controlled-player','-wanxiang-entry-evidence','-wanxiang-controlled-case',$case,'-screen-fullscreen','0','-screen-width',[string]$w,'-screen-height',[string]$h,'-logFile',"$storage/player-$case.log") 180 controlled-player $storage
    $ok=$r.status -eq 'PASS' -and (Test-Path $result) -and (Get-Content $result -Raw|ConvertFrom-Json).status -eq 'PASS'
    if($ok){Note "player.$case.receipt" PASS 'Actual self exit0 and real uGUI callbacks completed; no native input claim' controlled-player}else{Note "player.$case.receipt" FAIL 'Missing/failed completion receipt or abnormal/timeout exit; no kill' controlled-player};if($ok){$verify=Step "player.$case.audit" (Join-Path $env:USERPROFILE ".cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe") @('-B',"$PSScriptRoot/Verify-ControlledPlayer.py",'--root',$storage,'--case',$case) 30 controlled-player;$ok=$verify.status -eq 'PASS'};if($case -eq 'read'){$canResume=$ok}
    if($r.timedOut){break}
   }
  }else{Note 'controlled-player-cases' NOT_RUN 'Separate build unavailable' controlled-player}
 }
}catch{Note 'controller.exception' FAIL $_.Exception.ToString() controlled-build}finally{foreach($child in $script:children){if($child.process.HasExited){try{FinishChild $child}catch{}}};Flush;Write-Output "RESULT_ROOT=$root"}
if(@($script:results|Where-Object status -eq 'FAIL').Count){exit 1};exit 0
