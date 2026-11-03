param([Parameter(Mandatory)][string]$Build,[Parameter(Mandatory)][string]$Output,[switch]$Probe,[switch]$ShowInactive,[switch]$HiddenControl,[ValidateSet("default","d3d11")][string]$Graphics="default")
$ErrorActionPreference='Stop';if($HiddenControl-and$ShowInactive){throw 'Contradictory window controls'};$out=[IO.Path]::GetFullPath($Output);$build=[IO.Path]::GetFullPath($Build);if(!$out.StartsWith('I:\WGCombat\CP05BR-')-or !$build.StartsWith('I:\WGCombat\CP05BR-')){throw 'Owned roots required'};if(Test-Path $out){throw 'Fresh output required'};if(Get-Process WanxiangGuitu -ErrorAction SilentlyContinue){throw 'Player conflict'}
$exe=Join-Path $build 'WanxiangGuitu.exe';$receipt=Get-Content "$exe.release.json" -Raw|ConvertFrom-Json;if((Get-FileHash $exe).Hash.ToLowerInvariant() -ne $receipt.executableSHA256){throw 'Release identity mismatch'};$bee=(Get-Content "$exe.bee.json" -Raw|ConvertFrom-Json).'PlayerBuildProgramLibrary.Data.PlayerBuildConfig';foreach($n in 'EnableUnityConnect','EnableCrashReporting','EnableInsights','EnableAnalytics','EnablePerformanceReporting'){if($bee.Services.$n -ne $false){throw 'Unsafe diagnostic config'}}
New-Item -ItemType Directory $out|Out-Null;$entry='H:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Invoke-LocalValidation.ps1';$ast=[Management.Automation.Language.Parser]::ParseFile($entry,[ref]$null,[ref]$null);foreach($name in 'StartChild','FinishChild'){$d=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst]-and $n.Name -eq $name},$true);Invoke-Expression $d.Extent.Text}
$script:children=[Collections.Generic.List[object]]::new();$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$true;$script:workerPath='I:/WGP2/1028-080504-eef74f/Runtime/Worker/NativeProbe.dll';$dotnet=(Get-Command dotnet).Source;$MinimumUnityCommitGB=3
$argsList=@('-wanxiang-storage-root',$out,'-cp05-training','-windowed','-screen-width','1280','-screen-height','720','-logFile',"$out/Player.log");if($Graphics -eq "d3d11"){$argsList+="-force-d3d11"};if($Probe){$argsList+='-cp05-br';};$t=StartChild $exe $argsList "$out/Player" $out (!$HiddenControl)
$deadline=[datetime]::UtcNow.AddSeconds($(if($Probe){420}else{25}));while(!$t.process.HasExited-and[datetime]::UtcNow-lt$deadline){Start-Sleep -Milliseconds 200}
if(!$Probe-and !$t.process.HasExited){$d=Get-Content "$out/Player.desktop-process.json" -Raw|ConvertFrom-Json;dotnet $script:workerPath close $d.pid "$out/close.json" $exe $d.desktop|Out-Null;$null=$t.process.WaitForExit(20000)}
$ended=$t.process.HasExited;FinishChild $t;@{exited=$ended;exitCode=if($ended){$t.process.ExitCode}else{$null};timedOut=!$ended;forcedTermination=$false;layer=if($Probe){'isolated nondevelopment API probe'}else{'pure playable training smoke; no native input'}}|ConvertTo-Json|Set-Content "$out/runtime.json"
if(!$ended){throw 'Bounded timeout, no kill'};if(Select-String "$out/Player.log" -Pattern 'NullReferenceException|MissingReferenceException|CP05_TRAINING_FAILED' -Quiet){throw 'Runtime semantic failure; see raw log'}
if($t.process.ExitCode-ne 0){throw 'Player exit failure'}


if($Probe){if(!(Test-Path "$out/br-probe.json")){throw 'INCOMPLETE: missing semantic receipt'};$r=Get-Content "$out/br-probe.json" -Raw|ConvertFrom-Json;if($r.status-ne'MEASURED'-or !$r.calibrationValid-or @($r.phases).Count-ne 6){throw 'Measurement failed or incomplete'}}


if($Probe){
 $py='C:/Users/guan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
 & $py "$PSScriptRoot/Tools/Analyse.py" $out "$out/measurement-receipt.json" --stress
 if($LASTEXITCODE-ne 0){throw 'Invalid allocation measurement'}
 $a=Get-Content "$out/measurement-receipt.json" -Raw|ConvertFrom-Json
 if($a.workloadCoverage-ne 'PASS'){throw 'Required workload not observed'}
 & $py "$PSScriptRoot/Tools/RenderReceipt.py" $out "$out/render-receipt.json"
 $renderExit=$LASTEXITCODE
 if($HiddenControl){if($renderExit-ne 1){throw 'Expected hidden-window negative control did not classify FAIL'}}elseif($renderExit-ne 0){throw 'Visible frame verification failed or incomplete'}
}
