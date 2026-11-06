param([Parameter(Mandatory)][string]$Output,[Parameter(Mandatory)][string]$Mode,[string]$Seed,[string]$Observation='ObservedFinal')
$ErrorActionPreference='Stop'
$r='I:/WGCombat/C24B1-1107-A'
$out=[IO.Path]::GetFullPath($Output)
$exe="$r/$Observation/Release/WanxiangGuitu.exe"
if(!$out.StartsWith('I:\WGCombat\C24B1-1107-A\') -or (Test-Path $out) -or !(Test-Path $exe)){throw 'Fresh isolated Player output required'}
if([double](Get-CimInstance Win32_OperatingSystem).FreeVirtualMemory/1MB -lt 3){throw 'Below 3 GB commit; not launched'}
New-Item -ItemType Directory $out|Out-Null
Set-Content "$out/cavern-test.txt" $Mode
if($Seed){& "$PSScriptRoot/Copy-TestSeed.ps1" $Seed $out}
$entry='H:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Invoke-LocalValidation.ps1'
$ast=[Management.Automation.Language.Parser]::ParseFile($entry,[ref]$null,[ref]$null)
foreach($name in 'StartChild','FinishChild'){
    $f=$ast.Find({param($n)$n-is[Management.Automation.Language.FunctionDefinitionAst]-and$n.Name-eq$name},$true)
    Invoke-Expression $f.Extent.Text
}
$script:children=[Collections.Generic.List[object]]::new()
$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N')
$script:workerReady=$true
$script:workerPath='I:/WGP2/1028-080504-eef74f/Runtime/Worker/NativeProbe.dll'
$dotnet=(Get-Command dotnet).Source
$t=StartChild $exe @('-logFile',"$out/Player.log",'-screen-width','1280','-screen-height','720','-screen-fullscreen','0','-force-d3d12','-wanxiang-storage-root',$out) "$out/Player" $out $true
$ended=$t.process.WaitForExit(360000)
FinishChild $t
@{exited=$ended;exitCode=if($ended){$t.process.ExitCode}else{$null};timedOut=!$ended;forcedTermination=$false;scope='controlled non-development Player'}|ConvertTo-Json|Set-Content "$out/process.json"
if(!$ended){throw 'Timed out; process retained'}
if($t.process.ExitCode-ne0 -or !(Test-Path "$out/complete.txt")){throw "Player $Mode failed; evidence retained"}
