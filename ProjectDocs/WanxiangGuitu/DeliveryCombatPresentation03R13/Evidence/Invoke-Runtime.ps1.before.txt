param([Parameter(Mandatory)][string]$Build,[Parameter(Mandatory)][string]$Output,[Parameter(Mandatory)][string]$FixtureSave)
$ErrorActionPreference='Stop';$Build=[IO.Path]::GetFullPath($Build);$Output=[IO.Path]::GetFullPath($Output)
if(!$Build.StartsWith('I:\WGCombat\CP03-') -or !$Output.StartsWith('I:\WGCombat\CP03-')){throw 'Owned CP03 paths required'}
if(@(Get-Process WanxiangGuitu -ErrorAction SilentlyContinue).Count){throw 'Player occupied; preserve user process'}
New-Item -ItemType Directory $Output -ErrorAction Stop|Out-Null
'{"synthetic":true,"scope":"CP03 runtime controlled public combat API acceptance"}'|Set-Content "$Output/cp03-owner.json"

$FixtureSave=[IO.Path]::GetFullPath($FixtureSave);if(!$FixtureSave.StartsWith('I:\WGCombat\CP03-') -or [IO.Path]::GetFileName($FixtureSave) -ne 'save.json'){throw 'Owned immutable fixture required'}
$dest=Join-Path $Output 'WanxiangGuitu/ForestRuins';New-Item -ItemType Directory $dest -ErrorAction Stop|Out-Null;Copy-Item -LiteralPath $FixtureSave -Destination "$dest/save.json" -ErrorAction Stop
@{source=$FixtureSave;sourceSHA256=(Get-FileHash $FixtureSave).Hash;copiedSHA256=(Get-FileHash "$dest/save.json").Hash;rule='Original real synthetic checkpoint copied verbatim; no payload edit or reward injection'}|ConvertTo-Json|Set-Content "$Output/fixture-copy.json"
$entry=Join-Path $PSScriptRoot '../DeliveryUI01/Automation/Invoke-LocalValidation.ps1';$ast=[Management.Automation.Language.Parser]::ParseFile($entry,[ref]$null,[ref]$null)
foreach($name in 'SafePath','WriteReportFile','Flush','Note','StartChild','FinishChild','Step'){$def=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true);Invoke-Expression $def.Extent.Text}
$root=$Output;$script:results=[Collections.Generic.List[object]]::new();$script:children=[Collections.Generic.List[object]]::new();$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$true
$script:workerPath='I:/WGP2/1028-080504-eef74f/Runtime/Worker/NativeProbe.dll';$dotnet=(Get-Command dotnet).Source;$MinimumUnityCommitGB=3
$r=Step 'CP03Runtime' "$Build/WanxiangGuitu.exe" @('-wanxiang-storage-root',$Output,'-wanxiang-test-gameplay','-cp03-acceptance','-screen-width','1280','-screen-height','720','-windowed','-logFile',"$Output/Player.log") 600 'nondevelopment-acceptance-player-controlled-combat-API' $Output $true
# Process exit is recorded separately by Step. Semantic classification is read-only.
Flush
$python=(Join-Path $env:USERPROFILE '.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe')
Copy-Item -LiteralPath "$Output/results.json" -Destination "$Output/process-results.json" -ErrorAction Stop
@{kind='verbatim actual runner snapshot before semantic append';source="$Output/results.json";snapshot="$Output/process-results.json";sourceSHA256AtSnapshot=(Get-FileHash -LiteralPath "$Output/results.json").Hash;snapshotSHA256=(Get-FileHash -LiteralPath "$Output/process-results.json").Hash;utc=[DateTime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content "$Output/process-origin.json"
$receiptArgs=@("$PSScriptRoot/Receipt.py",'--receipt',"$Output/presentation.json",'--output',"$Output/Semantic",'--profile','Runtime','--contract',"$PSScriptRoot/../DeliveryCombatPresentation03R11/Contracts/Runtime.json",'--process-receipt',"$Output/process-results.json",'--exit-receipt',"$Output/CP03Runtime.exit.json")
if(@($script:results|Where-Object status -eq FAIL).Count){$receiptArgs+='--external-failure'}
& $python @receiptArgs
$semanticExit=$LASTEXITCODE
$q=Get-Content "$Output/Semantic/acceptance.json" -Raw|ConvertFrom-Json
$noteStatus=if($q.integrity -ne 'PASS'){'NOT_RUN'}else{$q.assertionStatus}
Note 'semantic-receipt' $noteStatus "overall=$($q.overallStatus); classifierExit=$semanticExit; see Semantic/acceptance.json" runtime
Add-Content "$Output/REPORT.md" "`nOverall semantic acceptance: **$($q.overallStatus)** (classifier exit $semanticExit). See [semantic report](Semantic/REPORT.md)."
exit $semanticExit
