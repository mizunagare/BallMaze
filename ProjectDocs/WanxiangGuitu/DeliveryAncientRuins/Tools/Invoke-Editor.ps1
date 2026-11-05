param([Parameter(Mandatory)][string]$Method,[Parameter(Mandatory)][string]$Output,[switch]$NonBatch,[switch]$DiagnosticJobs,[int]$Seconds=600)
$ErrorActionPreference='Stop';$project='I:\WGCombat\CP06C1-1104-A\Validation\Project';$out=[IO.Path]::GetFullPath($Output)
if(!$out.StartsWith('I:\WGCombat\C1-1105-A\')){throw 'Owned fresh research output required'}
if(Test-Path -LiteralPath $out){throw 'Output exists; preserve old evidence'}
if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object {$_.CommandLine -and $_.CommandLine.Replace('/','\') -like "*$project*"}).Count){throw 'Project occupied; do not close/kill/reenter'}
New-Item -ItemType Directory $out|Out-Null
New-Item -ItemType Directory "$out/ExecutedTools"|Out-Null
foreach($p in Get-ChildItem -LiteralPath "$project/Assets/CombatPrototype" -Filter '*.cs'){Get-FileHash -LiteralPath $p.FullName -Algorithm SHA256 | Select-Object Path,Hash | ConvertTo-Json -Compress | Add-Content "$out/product-inputs.jsonl"}
foreach($folder in @("$project/Assets","$project/Assets/Editor")){foreach($f in Get-ChildItem -LiteralPath $folder -Filter 'C1*.cs'){Copy-Item -LiteralPath $f.FullName -Destination "$out/ExecutedTools/$($f.Name)"}}
$entry='H:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Invoke-LocalValidation.ps1';$ast=[Management.Automation.Language.Parser]::ParseFile($entry,[ref]$null,[ref]$null)
foreach($name in 'StartChild','FinishChild'){$f=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst]-and$n.Name-eq$name},$true);Invoke-Expression $f.Extent.Text}
$script:children=[Collections.Generic.List[object]]::new();$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$true;$script:workerPath='I:/WGP2/1028-080504-eef74f/Runtime/Worker/NativeProbe.dll';$dotnet=(Get-Command dotnet).Source;$MinimumUnityCommitGB=3
$exe='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe';$argsList=@('-projectPath',$project,'-executeMethod',$Method,'-wanxiang-storage-root',$out,'-logFile',"$out/Unity.log");if(!$NonBatch){$argsList+='-batchmode'};if($DiagnosticJobs){$argsList+='-diag-job-temp-memory-leak-validation'}
$old=$env:C1_OUTPUT;try{$env:C1_OUTPUT=$out;$t=StartChild $exe $argsList "$out/Editor" $out $false;$ended=$t.process.WaitForExit($Seconds*1000);FinishChild $t;@{exited=$ended;exitCode=if($ended){$t.process.ExitCode}else{$null};timedOut=!$ended;forcedTermination=$false;scope='isolated ruins verification; controlled, not human/native'}|ConvertTo-Json|Set-Content "$out/process.json";if(!$ended){throw 'Timeout; process preserved'};exit $t.process.ExitCode}finally{$env:C1_OUTPUT=$old}
