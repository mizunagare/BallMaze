param([Parameter(Mandatory)][string]$Exe,[Parameter(Mandatory)][string]$Output,[Parameter(Mandatory)][string]$SeedPackage)
$ErrorActionPreference='Stop';$out=[IO.Path]::GetFullPath($Output);$exePath=[IO.Path]::GetFullPath($Exe);$seed=[IO.Path]::GetFullPath($SeedPackage)
foreach($p in @($out,$exePath,$seed)){if(!$p.StartsWith('I:\WGCombat\C1R4-1105-A\')){throw 'Owned isolated paths required'}}
if(Test-Path -LiteralPath $out){throw 'Fresh output required'};New-Item -ItemType Directory $out|Out-Null
Copy-Item -LiteralPath (Join-Path (Split-Path $out -Parent) "resource-keys.txt") -Destination "$out/resource-keys.txt"
$dest=Join-Path $out 'WanxiangGuitu/ForestRuins';New-Item -ItemType Directory $dest -Force|Out-Null;$before=@()
foreach($f in Get-ChildItem -LiteralPath $seed -Recurse -File){$relative=[IO.Path]::GetRelativePath($seed,$f.FullName);$to=Join-Path $dest $relative;New-Item -ItemType Directory ([IO.Path]::GetDirectoryName($to)) -Force|Out-Null;Copy-Item -LiteralPath $f.FullName -Destination $to;$hash=(Get-FileHash -LiteralPath $f.FullName).Hash;if($hash-ne(Get-FileHash -LiteralPath $to).Hash){throw 'Copy mismatch'};$before+=@{relative=$relative;sha256=$hash}}
$before|ConvertTo-Json -Depth 5|Set-Content "$out/seed-before.json"
$os=Get-CimInstance Win32_OperatingSystem;if([double]$os.FreeVirtualMemory/1MB-lt3){throw 'Below 3GB; no Player launched'}
$ast=[Management.Automation.Language.Parser]::ParseFile('H:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Invoke-LocalValidation.ps1',[ref]$null,[ref]$null)
foreach($name in 'StartChild','FinishChild'){$f=$ast.Find({param($n)$n-is[Management.Automation.Language.FunctionDefinitionAst]-and$n.Name-eq$name},$true);Invoke-Expression $f.Extent.Text}
$script:children=[Collections.Generic.List[object]]::new();$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$true;$script:workerPath='I:/WGP2/1028-080504-eef74f/Runtime/Worker/NativeProbe.dll';$dotnet=(Get-Command dotnet).Source
$t=StartChild $exePath @('-logFile',"$out/Player.log",'-screen-width','1280','-screen-height','720','-screen-fullscreen','0','-wanxiang-storage-root',$out) "$out/Player" $out $true
$until=[DateTime]::UtcNow.AddSeconds(45);$ready=$false
while([DateTime]::UtcNow-lt$until-and!$t.process.HasExited){if(Test-Path "$out/entry-audit.jsonl"){$rows=@(Get-Content "$out/entry-audit.jsonl"|ConvertFrom-Json);$ready=@($rows|Where-Object phase -eq 'title-ready').Count-eq1;if($ready){break}};Start-Sleep -Milliseconds 250}
$launch=Get-Content "$out/Player.desktop-process.json" -Raw|ConvertFrom-Json
& dotnet $script:workerPath close $launch.pid "$out/close-delivery.json" $exePath $launch.desktop
$closeDelivery=$LASTEXITCODE;$ended=$t.process.WaitForExit(30000);FinishChild $t
$changes=@(foreach($f in $before){$path=Join-Path $dest $f.relative;if(!(Test-Path -LiteralPath $path)-or(Get-FileHash -LiteralPath $path).Hash-ne$f.sha256){$f.relative}})
$rows=@(Get-Content "$out/entry-audit.jsonl"|ConvertFrom-Json);$title=$rows|Where-Object phase -eq 'title-ready'
@{scope='Instrumented copy, separate resource-probe assembly and startup lists. Product DLL and serialized data unchanged. Owned inactive desktop; background close delivery is not native menu interaction or human play.';titleReady=$ready;titleOnly=(@($rows|Where-Object phase -eq 'game-ready').Count-eq0-and$title.gameObjects-eq0);canContinue=$title.canContinue;unchangedSyntheticFiles=$changes.Count-eq0;changedFiles=$changes;closeMessageDeliveryExit=$closeDelivery;actualProcessExited=$ended;exitCode=if($ended){$t.process.ExitCode}else{$null};forcedTermination=$false;nativeInput='NOT_RUN';humanExperience='NOT_RUN'}|ConvertTo-Json -Depth 5|Set-Content "$out/pure-runtime.json"
if(!$ended){throw 'Player close timeout: preserved, not killed'}
if(!(Test-Path "$out/resource-runtime.tsv") -or !$ready-or$changes.Count-or$t.process.ExitCode-ne0){throw 'Pure startup/exit evidence incomplete or failed'}
