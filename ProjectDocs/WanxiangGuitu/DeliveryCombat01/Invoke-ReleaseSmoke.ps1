param([Parameter(Mandatory)][string]$BuildRoot,[Parameter(Mandatory)][string]$Output,[Parameter(Mandatory)][string]$WorkerPath)
$ErrorActionPreference='Stop';$Output=[IO.Path]::GetFullPath($Output)
if(!$Output.StartsWith('I:\WGCombat\',[StringComparison]::OrdinalIgnoreCase)){throw 'Owned external output required'}
$bo=Get-Content "$BuildRoot/owner.json" -Raw|ConvertFrom-Json;if($bo.variant -ne 'Release'){throw 'Pure Release build required'}
if(@(Get-CimInstance Win32_Process -Filter "name='WanxiangGuitu.exe'").Count){throw 'Existing Player conflict; preserved'}
New-Item -ItemType Directory $Output | Out-Null
$ast=[Management.Automation.Language.Parser]::ParseFile((Join-Path $PSScriptRoot '../DeliveryUI01/Automation/Invoke-LocalValidation.ps1'),[ref]$null,[ref]$null)
foreach($name in 'SafePath','WriteReportFile','Flush','Note','StartChild','FinishChild','Step'){$def=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true);Invoke-Expression $def.Extent.Text}
$root=$Output;$script:results=[Collections.Generic.List[object]]::new();$script:children=[Collections.Generic.List[object]]::new();$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$true;$script:workerPath=$WorkerPath;$dotnet=(Get-Command dotnet).Source;$MinimumUnityCommitGB=3
$exe=Join-Path $BuildRoot 'Results/Release/WanxiangGuitu.exe';$start=[datetime]::UtcNow
$token=StartChild $exe @('-force-d3d11','-wanxiang-storage-root',$Output,'-wanxiang-entry-evidence','-screen-fullscreen','0','-screen-width','1280','-screen-height','720','-logFile',"$Output/player.log") "$Output/player" '' $true
$ready=$false;$deadline=$start.AddSeconds(90)
while(!$token.process.HasExited -and [datetime]::UtcNow -lt $deadline){if((Test-Path "$Output/title-player.png") -and (Test-Path "$Output/entry-audit.jsonl")){$ready=$true;break};Start-Sleep -Milliseconds 200}
$id=if(Test-Path $token.receipt){(Get-Content $token.receipt -Raw|ConvertFrom-Json).pid}else{$token.process.Id}
if(!$token.process.HasExited){Step 'background-close' $dotnet @($WorkerPath,'close',[string]$id,"$Output/close.json",$exe,$script:desktop) 10 background-close|Out-Null}
$ended=$token.process.WaitForExit(30000);if($ended){FinishChild $token}
@{ready=$ready;ended=$ended;timedOut=!$ended;forcedTermination=$false;hostExitCode=$(if($ended){$token.process.ExitCode}else{$null});closeMethod='Owned inactive-desktop WM_CLOSE; NOT native titlebar/U16';exeSha256=(Get-FileHash $exe).Hash;startUtc=$start.ToString('o');endUtc=[datetime]::UtcNow.ToString('o')}|ConvertTo-Json|Set-Content "$Output/process.json"
Note 'release-title-rendered' $(if($ready){'PASS'}else{'FAIL'}) 'Actual uninstrumented non-development Player; no gameplay asserted' formal-release-player
Flush
if(!$ended -or !$ready -or @($script:results|Where-Object status -eq FAIL).Count){exit 1}
