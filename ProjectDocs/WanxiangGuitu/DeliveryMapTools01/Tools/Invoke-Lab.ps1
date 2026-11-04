param([Parameter(Mandatory)][string]$Method,[Parameter(Mandatory)][string]$Output,[switch]$NonBatch,[int]$Seconds=600,[string]$Project='I:/WGCombat/MAPTOOLS-1104-A/Project')
$ErrorActionPreference='Stop';$project=[IO.Path]::GetFullPath($Project);$out=[IO.Path]::GetFullPath($Output)
if(!$project.StartsWith('I:\WGCombat\MAPTOOLS-1104-A\')){throw 'Owned isolated research project required'}
if(!$out.StartsWith('I:\WGCombat\MAPTOOLS-1104-A\')){throw 'Owned research output required'}
if(Test-Path $out){throw 'Fresh output required'}
if(@(Get-CimInstance Win32_Process -Filter "name='Unity.exe'"|Where-Object {$_.CommandLine.Replace('/','\') -like "*$project*"}).Count){throw 'Research project occupied; no close or kill'}
New-Item -ItemType Directory $out|Out-Null
$entry='H:/unity/WanxiangGuitu/ProjectDocs/WanxiangGuitu/DeliveryUI01/Automation/Invoke-LocalValidation.ps1';$ast=[Management.Automation.Language.Parser]::ParseFile($entry,[ref]$null,[ref]$null)
foreach($name in 'StartChild','FinishChild'){$f=$ast.Find({param($n)$n -is [Management.Automation.Language.FunctionDefinitionAst]-and$n.Name-eq$name},$true);Invoke-Expression $f.Extent.Text}
$script:children=[Collections.Generic.List[object]]::new();$script:desktop='WGTest_'+[guid]::NewGuid().ToString('N');$script:workerReady=$true;$script:workerPath='I:/WGP2/1028-080504-eef74f/Runtime/Worker/NativeProbe.dll';$dotnet=(Get-Command dotnet).Source;$MinimumUnityCommitGB=3
$exe='C:/Program Files/Unity/Hub/Editor/6000.6.5f1/Editor/Unity.exe';$argsList=@('-projectPath',$project,'-executeMethod',$Method,'-logFile',"$out/Unity.log");if(!$NonBatch){$argsList+='-batchmode'}
$old=$env:MAP_LAB_OUTPUT;try{$env:MAP_LAB_OUTPUT=$out;$t=StartChild $exe $argsList "$out/Editor" $out $false;$ended=$t.process.WaitForExit($Seconds*1000);FinishChild $t;@{exited=$ended;exitCode=if($ended){$t.process.ExitCode}else{$null};timedOut=!$ended;forcedTermination=$false;scope='independent map-tool research; not product/native/human acceptance'}|ConvertTo-Json|Set-Content "$out/process.json";if(!$ended){throw 'Bounded timeout; process preserved'};exit $t.process.ExitCode}finally{$env:MAP_LAB_OUTPUT=$old}
