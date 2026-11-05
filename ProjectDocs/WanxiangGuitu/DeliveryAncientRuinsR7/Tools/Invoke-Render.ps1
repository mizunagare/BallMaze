param([Parameter(Mandatory)][ValidateSet('A','B')][string]$Label,[Parameter(Mandatory)][ValidateSet('camp','ruins')][string]$Mode,[string]$Attempt='1',[switch]$Intervention,[switch]$DiagnosticCopy,[switch]$Gpu)
$ErrorActionPreference='Stop'
$root='I:/WGCombat/C1R7-1106-A'
$copy=if($DiagnosticCopy){"Diagnostic$Label"}else{"Render$Label"}
$exe="$root/$copy/Release/WanxiangGuitu.exe"
$out="$root/Frames-$Label-$Mode-$Attempt"
if((Test-Path $out) -or !(Test-Path $exe)){throw 'Fresh R7 output and verified render copy required'}
if([double](Get-CimInstance Win32_OperatingSystem).FreeVirtualMemory/1MB -lt 3){throw 'Insufficient commit; no Unity launch'}
New-Item -ItemType Directory $out|Out-Null
Set-Content "$out/render-mode.txt" $Mode
if($Intervention){Set-Content "$out/intervention.txt" 'separate shadow/post control'}
$seed=if($Mode -eq 'camp'){'I:/WGCombat/C1-1105-A/CampPreparePlayer1/CampPackage'}else{'I:/WGCombat/C1R2-1105-A/R2Rewards/SeedPackage'}
$seed=[IO.Path]::GetFullPath($seed)
$dest=Join-Path $out 'WanxiangGuitu/ForestRuins'
New-Item -ItemType Directory $dest -Force|Out-Null
$receipt=@(foreach($f in Get-ChildItem -LiteralPath $seed -Recurse -File){
 if($f.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Linked fixture rejected'}
 $relative=[IO.Path]::GetRelativePath($seed,$f.FullName);$to=Join-Path $dest $relative
 New-Item -ItemType Directory ([IO.Path]::GetDirectoryName($to)) -Force|Out-Null
 Copy-Item -LiteralPath $f.FullName -Destination $to
 $sha=(Get-FileHash -LiteralPath $f.FullName).Hash
 if($sha-ne(Get-FileHash -LiteralPath $to).Hash){throw 'Fixture mismatch'}
 @{path=$relative;sha256=$sha}
})
@{syntheticFixture=$seed;files=$receipt}|ConvertTo-Json -Depth 5|Set-Content "$out/fixture.json"
$ast=[Management.Automation.Language.Parser]::ParseFile('H:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Invoke-LocalValidation.ps1',[ref]$null,[ref]$null)
foreach($name in 'StartChild','FinishChild'){$f=$ast.Find({param($n)$n-is[Management.Automation.Language.FunctionDefinitionAst]-and$n.Name-eq$name},$true);Invoke-Expression $f.Extent.Text}
$script:children=[Collections.Generic.List[object]]::new();$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$true;$script:workerPath='I:/WGP2/1028-080504-eef74f/Runtime/Worker/NativeProbe.dll';$dotnet=(Get-Command dotnet).Source
if($Gpu){
    $env:PYTHONPATH='I:/WGCombat/C1R5-1105-A/NativeTools'
    $python='C:/Users/guan/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'
    $runner=Join-Path $PSScriptRoot 'Run-GPU.py'
    $t=StartChild $python @($runner,$exe,$out,'fixture-window') "$out/Runner" $out $false
}else{
$t=StartChild $exe @('-logFile',"$out/Player.log",'-screen-width','1280','-screen-height','720','-screen-fullscreen','0','-force-d3d12','-wanxiang-storage-root',$out) "$out/Player" $out $true
}
$ended=$t.process.WaitForExit(120000);FinishChild $t
@{exited=$ended;exitCode=if($ended){$t.process.ExitCode}else{$null};timedOut=!$ended;forcedTermination=$false;scope='Nondevelopment release-copy sidecar, render observation'}|ConvertTo-Json|Set-Content "$out/process.json"
if(!$ended){throw 'Timed out; process retained'}
if($t.process.ExitCode-ne0 -or !(Test-Path "$out/render-complete.txt")){throw 'Render probe failed; preserved'}
