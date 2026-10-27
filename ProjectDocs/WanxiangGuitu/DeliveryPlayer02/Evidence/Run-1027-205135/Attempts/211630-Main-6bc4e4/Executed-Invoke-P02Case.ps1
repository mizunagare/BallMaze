[CmdletBinding()]
param([Parameter(Mandatory)][string]$ParentRoot,[Parameter(Mandatory)][string]$StorageRoot,
 [ValidateSet('Setup','Main','Pending','Committed','Manufacture','Successor','Observe','BadPreferences')][string]$Mode,
 [string]$Expected='', [string]$BuildRoot='',
 [string]$WorkerFrom='D:/WanxiangValidationRuns/Input01/20261027-151043-585c2866/FinalFrozenValidation/20261027-161647-ab2a444e')
$ErrorActionPreference='Stop'
$entry=Join-Path $PSScriptRoot '../DeliveryUI01/Automation/Invoke-LocalValidation.ps1'
$ast=[Management.Automation.Language.Parser]::ParseFile($entry,[ref]$null,[ref]$null)
foreach($name in 'SafePath','WriteReportFile','Flush','Note','StartChild','FinishChild','Step'){$def=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true);Invoke-Expression $def.Extent.Text}
$parent=SafePath $ParentRoot;$storage=SafePath $StorageRoot
if((Get-Content "$parent/owner.json" -Raw|ConvertFrom-Json).kind -ne 'PLAYER-02 isolated runtime acceptance' -or !$storage.StartsWith($parent+'\',[StringComparison]::OrdinalIgnoreCase)){throw 'Owned PLAYER-02 child storage required'}
if(!$BuildRoot){$BuildRoot=@(Get-ChildItem "$parent/T" -Directory|Where-Object {Test-Path "$($_.FullName)/Results/build-report-messages.json"}|Sort-Object Name)[-1].FullName}
$build=SafePath $BuildRoot;$bo=Get-Content "$build/owner.json" -Raw|ConvertFrom-Json;$br=Get-Content "$build/Results/build-report-messages.json" -Raw|ConvertFrom-Json
if($bo.variant -ne 'Acceptance' -or $br.result -ne 'Succeeded' -or $br.errors -ne 0){throw 'Completed error-free acceptance build required'}
New-Item -ItemType Directory $storage -Force|Out-Null
if(!(Test-Path "$storage/p02-owner.json")){@{kind='PLAYER-02 synthetic storage';root=$storage;utc=[datetime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content "$storage/p02-owner.json"}
$root=Join-Path $parent ('Attempts/'+(Get-Date -Format 'HHmmss')+'-'+$Mode+'-'+[guid]::NewGuid().ToString('N').Substring(0,6));New-Item -ItemType Directory $root|Out-Null
$script:results=[Collections.Generic.List[object]]::new();$script:children=[Collections.Generic.List[object]]::new();$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$true;$script:workerPath=Join-Path $WorkerFrom 'Worker/NativeProbe.dll';$dotnet=(Get-Command dotnet).Source;$MinimumUnityCommitGB=3
$wo=Get-Content "$WorkerFrom/owner.json" -Raw|ConvertFrom-Json;if($wo.source -ne $bo.source -or $wo.kind -ne 'WanxiangGuitu isolated unattended run'){throw 'Worker source identity mismatch'}
$exe=Join-Path $build 'Results/Release/WanxiangGuitu.exe'
@{kind='PLAYER-02 acceptance runtime attempt';mode=$Mode;storage=$storage;build=$build;exeSha256=(Get-FileHash $exe).Hash;assemblySha256=(Get-FileHash "$build/Results/Release/WanxiangGuitu_Data/Managed/Assembly-CSharp.dll").Hash;desktop=$script:desktop;utc=[datetime]::UtcNow.ToString('o');scope='Temporary non-development acceptance Player, virtual input; NOT native/human'}|ConvertTo-Json|Set-Content "$root/owner.json"
Copy-Item -LiteralPath $PSCommandPath -Destination "$root/Executed-Invoke-P02Case.ps1"
function Fingerprint($label){$files=Get-ChildItem -LiteralPath $storage -Recurse -File|ForEach-Object {@{path=[IO.Path]::GetRelativePath($storage,$_.FullName);bytes=$_.Length;sha256=(Get-FileHash -LiteralPath $_.FullName).Hash}};ConvertTo-Json -InputObject @($files)|Set-Content "$root/storage-$label.json"}
Fingerprint before
if(@(Get-CimInstance Win32_Process|Where-Object Name -eq 'WanxiangGuitu.exe').Count){Note 'player' NOT_RUN 'Player conflict: preserve user/previous process' environment;exit 3}
$start=[datetime]::UtcNow;$args=@('-force-d3d11','-wanxiang-storage-root',$storage,'-p02-mode',$Mode,'-wanxiang-entry-evidence','-screen-fullscreen','0','-screen-width','1280','-screen-height','720','-logFile',"$root/player.log");if($Expected){$args+=@('-p02-expect',$Expected)}
$r=Step "runtime.$Mode" $exe $args 1000 acceptance-player $storage $true
if($r.timedOut){Note 'stage-receipt' NOT_RUN 'Process timeout preserved; unknown technical outcome; no force kill' acceptance-player;Flush;exit 1}
Fingerprint after
$receipt=Join-Path $storage "result-$Mode.json"
if(Test-Path $receipt){$value=Get-Content $receipt -Raw|ConvertFrom-Json;$fresh=(Get-Item $receipt).LastWriteTimeUtc -ge $start;$status=if($fresh -and $value.status -eq 'PASS' -and $r.status -eq 'PASS'){'PASS'}else{'FAIL'};Note 'stage-receipt' $status "Fresh=$fresh; actual status=$($value.status); terminal=$($value.terminal); OS exit=$($r.exitCode); no result inferred from exit alone" acceptance-player}
else{Note 'stage-receipt' FAIL 'Missing runtime receipt; OS exit is not stage success' acceptance-player}
# Freeze the whole synthetic set at this process boundary; never overwrite a prior attempt.
Copy-Item -LiteralPath $storage -Destination "$root/StorageAfter" -Recurse
Flush;Write-Output "ATTEMPT_ROOT=$root"
if(@($script:results|Where-Object status -eq FAIL).Count){exit 1};exit 0
