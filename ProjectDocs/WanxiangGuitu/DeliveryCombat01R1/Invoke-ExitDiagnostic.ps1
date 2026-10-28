param([Parameter(Mandatory)][string]$ParentRoot,[string]$Case='Close1',[string]$ObserverPath='')
$ErrorActionPreference='Stop';$parent=[IO.Path]::GetFullPath($ParentRoot)
$owner=Get-Content "$parent/owner.json" -Raw|ConvertFrom-Json;if($owner.kind -ne 'PLAYER-02 isolated runtime acceptance'){throw 'Owned isolated parent required'}
if($Case -notmatch '^[a-zA-Z0-9_-]+$'){throw 'Invalid case'}
if(@(Get-CimInstance Win32_Process -Filter "name='WanxiangGuitu.exe'").Count){throw 'Player conflict; preserve all existing processes'}
$root=Join-Path $parent $Case;New-Item -ItemType Directory $root|Out-Null
$ast=[Management.Automation.Language.Parser]::ParseFile((Join-Path $PSScriptRoot '../DeliveryUI01/Automation/Invoke-LocalValidation.ps1'),[ref]$null,[ref]$null)
foreach($n in 'SafePath','WriteReportFile','Flush','Note','StartChild','FinishChild','Step'){$def=$ast.Find({param($x)$x -is [Management.Automation.Language.FunctionDefinitionAst] -and $x.Name -eq $n},$true);Invoke-Expression $def.Extent.Text}
$script:results=[Collections.Generic.List[object]]::new();$script:children=[Collections.Generic.List[object]]::new();$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$true;$script:workerPath="$parent/Host/Worker/NativeProbe.dll";$dotnet=(Get-Command dotnet).Source;$MinimumUnityCommitGB=3
$exe="$parent/Release/WanxiangGuitu.exe";if(!$ObserverPath){$ObserverPath="$parent/Observer/ExitObserver.dll"};$start=[datetime]::UtcNow
@{protocol='Owned exact UnityWndClass WM_CLOSE; independent child and host native handles; no physical input';startUtc=$start.ToString('o');titleDeadlineSeconds=90;exitDeadlineSeconds=90;exeSha256=(Get-FileHash $exe).Hash;originalFailure='COMBAT01/ReleaseSmoke 30-second host-confirmation timeout; never overwritten';desktop=$script:desktop;root=$root}|ConvertTo-Json|Set-Content "$root/protocol-before-run.json"
$token=StartChild $exe @('-force-d3d11','-wanxiang-storage-root',$root,'-wanxiang-entry-evidence','-screen-fullscreen','0','-screen-width','1280','-screen-height','720','-logFile',"$root/player.log") "$root/player" $root $true
$deadline=$start.AddSeconds(90);$ready=$false
while(!$token.process.HasExited -and [datetime]::UtcNow -lt $deadline){if((Test-Path "$root/title-player.png") -and (Test-Path "$root/entry-audit.jsonl")){$ready=$true;break};Start-Sleep -Milliseconds 100}
Note 'pure-release-title' $(if($ready){'PASS'}else{'FAIL'}) 'Actual bit-identical pure release; no runtime acceptance driver' formal-release
if(!$ready){Note 'exit-observation' NOT_RUN 'Title dependency unavailable; preserve process, no guessed window close' exit-diagnostic;Flush;exit 1}
$receipt=Get-Content $token.receipt -Raw|ConvertFrom-Json;New-Item -ItemType Directory "$root/Observer"|Out-Null
@{pid=$receipt.pid;hostPid=$token.process.Id;exe=$exe;desktop=$script:desktop;output="$root/Observer";minimumCreationUtc=$start.ToString('o');timeoutSeconds=90}|ConvertTo-Json|Set-Content "$root/observer-config.json"
$observed=Step 'independent-exit-observer' $dotnet @($ObserverPath,"$root/observer-config.json") 120 exit-observer
if(Test-Path "$root/Observer/exit-observer.json"){
 $v=Get-Content "$root/Observer/exit-observer.json" -Raw|ConvertFrom-Json
 Note 'child-native-exit' $(if($v.childDone -and $v.childKnown -and $v.childCode -eq 0){'PASS'}else{'UNRESOLVED'}) "Retained handle signaled=$($v.childDone), actual code=$($v.childCode); PID disappearance is not proof" formal-release-exit
 Note 'host-native-exit' $(if($v.hostDone -and $v.hostKnown -and $v.hostCode -eq 0){'PASS'}else{'UNRESOLVED'}) "Separate host signal=$($v.hostDone), code=$($v.hostCode)" exit-observer
 if($token.process.HasExited){FinishChild $token}
 $audit=Get-Content "$root/entry-audit.jsonl"|ForEach-Object {$_|ConvertFrom-Json}
 Note 'title-quit-audit' $(if(@($audit|Where-Object phase -eq 'title-quit').Count){'PASS'}else{'FAIL'}) 'Independent product OnApplicationQuit audit; queued request alone is insufficient' formal-release-exit
 $bad=Select-String -LiteralPath "$root/player.log" -Pattern 'Got a UNKNOWN|Native Crash Reporting|Unhandled Exception|Crash!!!'
 Note 'shutdown-log' $(if($bad){'UNRESOLVED'}else{'PASS'}) 'Full log archived; absence here does not resolve historical D3D12 root cause' formal-release-exit
}
Flush
if(@($script:results|Where-Object status -in @('FAIL','UNRESOLVED')).Count){exit 1}
