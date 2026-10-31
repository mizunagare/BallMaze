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
if(!(Test-Path "$Output/presentation.json")){Note 'semantic-receipt' FAIL 'No runtime receipt' runtime}else{$q=Get-Content "$Output/presentation.json" -Raw|ConvertFrom-Json;if(@($q.rows|Where-Object status -ne PASS).Count){Note 'semantic-receipt' FAIL 'Runtime assertions failed' runtime}}
Flush
if($r.status -ne 'PASS' -or @($script:results|Where-Object status -eq FAIL).Count){exit 1}
exit 0
