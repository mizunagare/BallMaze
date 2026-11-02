param([Parameter(Mandatory)][string]$Root,[Parameter(Mandatory)][string]$Build,[Parameter(Mandatory)][string]$Fixture,[ValidateSet("Probe","Core")][string[]]$Suites=@("Probe","Core"))
$ErrorActionPreference='Stop';$Root=[IO.Path]::GetFullPath($Root);$Build=[IO.Path]::GetFullPath($Build);$Fixture=[IO.Path]::GetFullPath($Fixture)
if(!$Root.StartsWith('I:\WGCombat\CP04BR-') -or !$Build.StartsWith('I:\WGCombat\CP04BR-') -or !$Fixture.StartsWith('I:\WGCombat\CP03-')){throw 'Owned isolation paths required'}
if(@(Get-Process WanxiangGuitu -ErrorAction SilentlyContinue).Count){throw 'Player occupied; no user process closed'}
$entry=Join-Path $PSScriptRoot '../DeliveryUI01/Automation/Invoke-LocalValidation.ps1';$ast=[Management.Automation.Language.Parser]::ParseFile($entry,[ref]$null,[ref]$null)
foreach($name in 'SafePath','WriteReportFile','Flush','Note','StartChild','FinishChild','Step'){$def=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst] -and $n.Name -eq $name},$true);Invoke-Expression $def.Extent.Text}
$batchRoot=$Root;$all=@()
foreach($suite in $Suites){
 $output=Join-Path $batchRoot ('Player'+$suite);New-Item -ItemType Directory -Path $output -ErrorAction Stop|Out-Null;$save=Join-Path $output 'WanxiangGuitu/ForestRuins';New-Item -ItemType Directory -Path $save|Out-Null;Copy-Item -LiteralPath $Fixture -Destination "$save/save.json"
 @{source=$Fixture;sourceSHA256=(Get-FileHash $Fixture).Hash;copiedSHA256=(Get-FileHash "$save/save.json").Hash;rule='Verbatim immutable synthetic Continue; no reward or payload edit'}|ConvertTo-Json|Set-Content "$output/fixture-copy.json"
 '{"owner":"CP04BR isolated acceptance only"}'|Set-Content "$output/br-owner.json"
 $root=$output;$script:results=[Collections.Generic.List[object]]::new();$script:children=[Collections.Generic.List[object]]::new();$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$true;$script:workerPath='I:/WGP2/1028-080504-eef74f/Runtime/Worker/NativeProbe.dll';$dotnet=(Get-Command dotnet).Source;$MinimumUnityCommitGB=3
 $arguments=@('-wanxiang-storage-root',$output,'-wanxiang-test-gameplay','-br-acceptance','-screen-width','1280','-screen-height','720','-windowed','-logFile',"$output/Player.log");if($suite -eq 'Core'){$arguments+='-br-core'}
 $p=Step ('CP04BRPlayer'+$suite) "$Build/WanxiangGuitu.exe" $arguments 1100 'nondevelopment-isolated-acceptance-real-combat-API' $output $true;Flush
 $all+=@{suite=$suite;status=$p.status;exitCode=$p.exitCode};$all|ConvertTo-Json|Set-Content "$batchRoot/player-batch-progress.json"
 if($p.timedOut){throw 'Timed out process preserved; do not launch conflict'}
}

