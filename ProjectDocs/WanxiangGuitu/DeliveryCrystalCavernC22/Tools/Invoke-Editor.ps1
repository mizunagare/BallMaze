param([Parameter(Mandatory)][string]$Method,[Parameter(Mandatory)][string]$Output,[switch]$NonBatch,[switch]$DiagnosticJobs,[switch]$Quit,[string]$Mode='',[int]$Seconds=600,[string]$Seed,[switch]$ValidationCopy)
$ErrorActionPreference='Stop';$project=if($ValidationCopy){'I:\WGCombat\C22-1106-A\EditorProject'}else{'I:\WGCombat\C22-1106-A\Project'};$out=[IO.Path]::GetFullPath($Output)
if(!$out.StartsWith('I:\WGCombat\C22-1106-A\')){throw 'Owned fresh research output required'}
if(Test-Path -LiteralPath $out){throw 'Output exists; preserve old evidence'}
if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object {$_.CommandLine -and $_.CommandLine.Replace('/','\') -like "*$project*"}).Count){throw 'Project occupied; do not close/kill/reenter'}
New-Item -ItemType Directory $out|Out-Null
if($Mode){Set-Content "$out/cavern-test.txt" $Mode}
if($Seed){& "$PSScriptRoot/Copy-TestSeed.ps1" $Seed $out}
$entry='H:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Invoke-LocalValidation.ps1';$ast=[Management.Automation.Language.Parser]::ParseFile($entry,[ref]$null,[ref]$null)
foreach($name in 'StartChild','FinishChild'){$f=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst]-and$n.Name-eq$name},$true);Invoke-Expression $f.Extent.Text}
$script:children=[Collections.Generic.List[object]]::new();$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$true;$script:workerPath='I:/WGP2/1028-080504-eef74f/Runtime/Worker/NativeProbe.dll';$dotnet=(Get-Command dotnet).Source;$MinimumUnityCommitGB=3
$exe='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe';$argsList=@('-projectPath',$project,'-executeMethod',$Method,'-wanxiang-storage-root',$out,'-logFile',"$out/Unity.log");if(!$NonBatch){$argsList+='-batchmode'};if($Quit){$argsList+='-quit'};if($DiagnosticJobs){$argsList+='-diag-job-temp-memory-leak-validation'}
$old=$env:C1_OUTPUT;try{$env:C1_OUTPUT=$out;$t=StartChild $exe $argsList "$out/Editor" $out $false;$ended=$t.process.WaitForExit($Seconds*1000);FinishChild $t;@{exited=$ended;exitCode=if($ended){$t.process.ExitCode}else{$null};timedOut=!$ended;forcedTermination=$false;scope='isolated cavern verification; controlled, not human/native'}|ConvertTo-Json|Set-Content "$out/process.json";if(!$ended){throw 'Timeout; process preserved'};exit $t.process.ExitCode}finally{$env:C1_OUTPUT=$old}
